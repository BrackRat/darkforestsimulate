from manimlib.imports import *
import random 
import numpy as np
# for name in [s for s in list(COLOR_MAP.keys()) if s.endswith("_C")]:
#     locals()[name.replace("_C", "")] = locals()[name]
POINT_FIGNT = 0.2
POINT_FIGHTWIN = 1.5
POINT_FIGHTLOSE = 1

POINT_COOPERATION = 1.2

class Civilization:
    mark = 10000 # 随机起始分
    state = 1 # 0死亡 1存活
    attitude = 1 # 0友善 1中立 2好斗
    isPositive = 1 # 1积极探索 0消极保守
    
    position = [0,0,0] # 动画制作，位置向量
    op = Circle() # 动画制作，样本
    id = 0 # 动画制作，物体唯一id
    def __init__(self,mark,attitude,isPositive,position,op,id):
        self.mark = mark
        self.attitude = attitude
        self.isPositive = isPositive
        self.position = position
        self.op = op
        self.id = id


def analyzeList(uniList):
    n0 = 0
    n1 = 0
    n2 = 0
    nPos = 0
    nNeg = 0
    nTotal = 0
    for cv in uniList:
        nTotal = nTotal+1
        if(cv.attitude == 0 and cv.state == 1):
            n0 = n0+1
        elif(cv.attitude == 1 and cv.state == 1):
            n1 = n1+1
        elif(cv.attitude == 2 and cv.state == 1):
            n2 = n2+1

        if(cv.isPositive == 1 and cv.state == 1):
            nPos = nPos + 1
        elif(cv.isPositive == 0 and cv.state == 1):
            nNeg = nNeg + 1
    
    print('nTotal:{} n0:{} n1:{} n2:{} nPos:{} nNeg:{}'.format(nTotal,n0,n1,n2,nPos,nNeg))

def activeCv(cv1,cv2):

    if(cv1.attitude == 2 or cv2.attitude == 2): # 双方任意一个好斗，则直接战斗
        if(cv1.mark > cv2.mark): # cv1分数更高
            n = (cv1.mark+cv2.mark)*POINT_FIGHTWIN # 双方的delta分数
            cv1.mark = cv1.mark + n*POINT_FIGHTWIN
            cv2.mark = cv2.mark - n*POINT_FIGHTLOSE
        else:
            n = (cv1.mark+cv2.mark)*POINT_FIGHTWIN # 双方的delta分数
            cv2.mark = cv2.mark + n*POINT_FIGHTWIN
            cv1.mark = cv1.mark - n*POINT_FIGHTLOSE
    
    #如果双方都不好斗，且有任何一方友善
    if(cv1.attitude == 0):
        if(cv2.attitude == 0 or cv2.attitude == 1): # 对方友善或中立
            n = (cv1.mark+cv2.mark)*POINT_COOPERATION # 合作分变化值
            cv1.mark = cv1.mark + n
            cv2.mark = cv2.mark + n
    elif(cv2.attitude == 0):
        if(cv1.attitude == 0 or cv1.attitude == 1): # 对方友善或中立
                n = (cv1.mark+cv2.mark)*POINT_COOPERATION # 合作分变化值
                cv1.mark = cv1.mark + n
                cv2.mark = cv2.mark + n
    
    #如果双方都中立... 不会互动

    reList = [cv1,cv2]
    return reList

def v_getActiveColor(cv1,cv2):
    if(cv1.attitude == 2 or cv2.attitude == 2): # 双方任意一个好斗，则直接战斗
        return RED
    
    #如果双方都不好斗，且有任何一方友善
    if(cv1.attitude == 0):
        return GREEN
    return GRAY
    


def checkDead(cv):
    if(cv.mark <=0):
        cv.state = 0
    return cv

def getNoActiveList(uniList,posList,fightList): # 获取未互动的文明List
    noActivedList = []
    for cv in uniList:
        if(cv not in posList and cv not in fightList): # 如果cv不在两个表里，就放到未互动列表
            noActivedList.append(cv)
    # print('noActivedListLen:{}'.format(len(noActivedList)))
    return noActivedList
    

def getPositiveCvs(uniList):# 获取宇宙里积极的文明
    posList = []
    for cv in uniList: # 遍历
        if(cv.isPositive == 1 and cv.state == 1):
            posList.append(cv) # 积极且存活文明加入posLit
    return posList

def findOther(cv,uniList):# 返回互动的文明
    maxs = len(uniList)-1
    while True: # 避免获取到自身
        i = random.randint(1,maxs)
        # print(i,uniList[i].mark)

        try:
            cvFight = uniList[i]
        except:
            print(i,len(uniList))
        if(cvFight != cv and cvFight.state == 1): # 不是自身并且存活
            return cvFight 
            # break

def isAllDead(uniList): #是否仅剩唯一文明
    alive = 0
    for cv in uniList:
        if (cv.state == 1):
            alive = alive+1
    if(alive != 1):
        return False
    else:
        return True

# def v_getScale(cv): # 获取大小变化 # 不会做 根本不会做！
#     d1 = cv.mark - 10000
#     mark = cv.mark - d1
#     if(d1<0):
#         return 0.4
#     else:
#         dd = 10000
#         sd = 0
#         while True:
#             delta = mark - dd
#             if(delta > 10000):
#                 sd = sd +0.01
#             else:
#                 break
#     print(0.4+sd)
#     return 0.4+sd



    size = 0.4 + scDetlta
    print(size,sc)
    return size


# initUniverse()

class darkForest(Scene):

    def construct(self):

        originList = []
        group1 = VGroup()
        group2 = VGroup()
        group3 = VGroup()
        id= 0
        for i in range(200): # 建立源宇宙文明
            id=id+1
            mark = random.randint(8000,12000)
            attitude = random.randint(0,2)
            isPositive = random.randint(0,1)
            position=[random.randint(-700,700)/100,random.randint(-400,400)/100,0]
            # print(position)
            dot = Dot()
            
            dot.shift(position)
            dot.scale(0.4)


            cv_i = Civilization(mark,attitude,isPositive,position,dot,id)
            originList.append(cv_i)
            if(attitude == 0):
                dot.set_color(GREEN)
                dot.set_fill(GREEN,opacity=1)
                group1.add(dot)
                
            elif(attitude == 1):
                dot.set_color(YELLOW)
                dot.set_fill(YELLOW,opacity=1)
                group2.add(dot)
                
            else:
                dot.set_color(RED)
                dot.set_fill(RED,opacity=1)
                group3.add(dot)
            
        group = VGroup()
        group.add(group1)
        group.add(group2)
        group.add(group3)
        self.play(
            DrawBorderThenFill(group,lag_ratio=0.2,run_time=10)
        )
        self.wait(2)
       
        #好戏开始
        roundList = originList
        print('-'*40)
        print('Origin Uni:')
        analyzeList(originList)
        print('-'*40)

        playedList = [] # 已经死过的文明

        while True:
            posList = getPositiveCvs(roundList)
            fightList = []
            _roundAnim = []# 载入线条
            
            _roundAnim2=[]# 载出线条
            
            for posCv in posList:
                fightList.append(findOther(posCv,roundList)) # 为posList 建立一个对应的figthList

            # print('pos:{} fight:{}'.format(len(posList),len(fightList)))
            noAcvitedList = getNoActiveList(roundList,posList,fightList)

            reList = [] # 存储互动结果
            for i in range(0,len(posList)):
                activedCv = activeCv(posList[i],fightList[i]) # 让文明互动 返回结果
                line = Line(posList[i].position,fightList[i].position,stroke_width=1,color=v_getActiveColor(posList[i],fightList[i]))
                
                _roundAnim.append(line)
                _roundAnim2.append(line)
                for cv in activedCv:
                    reList.append(cv) # 将互动后的文明放回reList

            

            roundedList = []
            for re in reList:
                if(re not in roundedList):
                    roundedList.append(re)
            for noAc in noAcvitedList:
                if(noAc not in roundedList):
                    roundedList.append(noAc)
            # roundedList = reList + noAcvitedList 不能这么写！
            for cv in roundedList:
                cv = checkDead(cv)

            # 检查死亡后，播放动画
            anim1 = LaggedStart(*[FadeIn(mob) for mob in _roundAnim])
            anim2 = AnimationGroup(*[FadeOut(mob) for mob in _roundAnim2])
            

            _roundAnim3=[]# 让死亡的文明变暗
            # _roundAnim4=[] #大小变化动画 已放弃
            for cv in roundedList: 
                if(cv.state == 0 and cv not in playedList):
                    playedList.append(cv)
                    _roundAnim3.append(cv.op)
                # if (cv.state == 1):  #大小变化动画 已放弃
                #     # scale = v_getScale(cv)
                #     _roundAnim4.append(cv)
            anim3 = LaggedStart(*[FadeOutAndShift(mob,DOWN*0.5) for mob in _roundAnim3])
            
            # anim4 = LaggedStart(*[ApplyMethod(mob.op.scale, v_getScale(mob)) for mob in _roundAnim4]) #大小变化动画 已放弃
            self.play(anim1)
            self.wait(2)
            self.play(anim3)
            self.wait(2)
            self.play(anim2)

            analyzeList(roundedList)
            if(isAllDead(roundedList)== True):
                break
            roundList = roundedList
        
        self.wait()