import random 

POINT_FIGNT = 0.2
POINT_FIGHTWIN = 1.5
POINT_FIGHTLOSE = 1

POINT_COOPERATION = 1.2

class Civilization:
    mark = 10000 # 随机起始分
    state = 1 # 0死亡 1存活
    attitude = 1 # 0友善 1中立 2好斗
    isPositive = 1 # 1积极探索 0消极保守
    def __init__(self,mark,attitude,isPositive):
        self.mark = mark
        self.attitude = attitude
        self.isPositive = isPositive


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

def initUniverse(): # 初始化宇宙

    originList = []
    for i in range(200): # 建立源宇宙文明
        mark = random.randint(8000,12000)
        attitude = random.randint(0,2)
        isPositive = random.randint(0,1)
        cv_i = Civilization(mark,attitude,isPositive)
        originList.append(cv_i)
    
    # 接下来,按回合制抽出积极探索的文明,随机与其他文明互动
    roundList = originList
    print('-'*40)
    print('Origin Uni:')
    analyzeList(originList)
    print('-'*40)
    while True:
        posList = getPositiveCvs(roundList)
        fightList = []

        for posCv in posList:
            fightList.append(findOther(posCv,roundList)) # 为posList 建立一个对应的figthList

        # print('pos:{} fight:{}'.format(len(posList),len(fightList)))
        noAcvitedList = getNoActiveList(roundList,posList,fightList)

        reList = [] # 存储互动结果
        for i in range(0,len(posList)):
            activedCv = activeCv(posList[i],fightList[i]) # 让文明互动 返回结果
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
        

        analyzeList(roundedList)
        highest=0
        lowest = 0
        for cv in roundedList:
            cv = checkDead(cv)
            if(cv.mark > highest):
                highest = cv.mark
            if(cv.mark < lowest and cv.mark >0):
                lowest = cv.mark
        print('high:{} low:{}'.format(highest,lowest))
        
        if(isAllDead(roundedList)==True):
            break
        roundList = roundedList


initUniverse()