#-*-coding:utf-8-*-
#__author__='maxh'
import time
from functools import wraps

def timefn(fn):
    """计算性能的修饰器"""
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("@timefn：" + fn.__name__ + "took" + str(t2 - t1) + "second")
        return result
    return measure_time

class brokenLed(object):
    led0=[0,1,2,3,4,5,6,7,8,9]
    led1=[0,4,5,6,8,9]
    led2=[0,2,3,5,6,7,8,9]
    led3=[0,1,2,3,4,7,8,9]
    led4=[0,1,3,4,5,6,7,8,9]
    led5=[0,2,6,8]
    led6=[0,2,3,5,6,8,9]
    led7=[2,3,4,5,6,8,9]
    leds=[led0,led1,led2,led3,led4,led5,led6,led7]
    ledtag=[0,1,2,3,4,5,6,7]
    ledDict=dict(zip(ledtag,leds))

    # 构造一个bus车灯显示数字， n1=[0] 没有灯亮  n2=[6,7] 显示第六个和第七个灯
    def __init__(self,ledImage1,ledImage2,ledImage3):
        self.ledImage1=ledImage1 #第一个数字显示的笔画 [2,3,4]
        self.ledImage2=ledImage2 #第二个数字显示的笔画 [2,3,4]
        self.ledImage3=ledImage3 #第三个数字显示的笔画 [2,3,4]

    def getOneLedList(self,ledImage):
        imageList=[]
        for i in ledImage:
            imageList.append(brokenLed.ledDict[i])
        return imageList

    def getSameFromLists(self,numberList):  #args = [[1,2,3],[4,5,3]]  列表去重
        temp=numberList[0]
        if len(numberList)==1:
            return numberList[0]
        elif len(numberList)>1:
            for i in range(1,len(numberList)):
                temp=self.getSameFrom2List(temp,numberList[i])
            return temp

    def getSameFrom2List(self,list1,list2):  #两个列表求合集
       # same=[]          列表就交集用时：0.009999513626098633
       #  for i in list1:
       #      if i in list2:
       #          same.append(i)
        same=list(set(list1)&set(list2))   #集合求交集用时：0.0009949207305908203
        return same

    @timefn
    def getBusNumber(self):
        busNumber=[]
        def getOne(ledImage):
            ledList=self.getOneLedList(ledImage)
            return self.getSameFromLists(ledList)
        n1=getOne(self.ledImage1)
        n2=getOne(self.ledImage2)
        n3=getOne(self.ledImage3)
        for i in n1:
            for j in n2:
                for k in n3:
                    busNumber.append(i*100+j*10+k)
        print("当前车牌号可能是：")
        print(busNumber)
        print("共有%d趟车"%len(busNumber))
        return busNumber,len(busNumber)

if __name__ == "__main__":
    b=brokenLed([0],[0],[0])
    b.getBusNumber()
