# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from uiautomator import Device
import re
import time

phone = '192.168.219.101:5555'
d = Device(phone)
uiClickableTree=[]
waitForVisitList=[]

def getXML():
    d.dump("abc.xml")
    file = os.path.join(os.getcwd(), "abc.xml")
    return file

#生成树，把xml中所有的节点取出来放在列表中
def xmlToTree(xml):  #root[0]
    f = open(xml, 'rb')
    tree = ET.parse(f)
    root = tree.getroot()
    visitList=[]
    visitList.append(root)
    waitforHandlingNotes=[]
    waitforHandlingNotes.append(root)
    while len(waitforHandlingNotes)>=1:
            for i in waitforHandlingNotes:
                for j in i:
                    visitList.append(j)
                    if len(j)>=1:
                        waitforHandlingNotes.append(j)
                waitforHandlingNotes.remove(i)
    f.close()
    os.remove(xml)
    visitList.pop(0)
    return visitList

#扫描树，把上面列表中的节点挨个检查属性，如果是clickable=true就把该节点的text resourceid bound值组成tuple，加入列表返回
def clickableE(treeList):
    clickableList = []
    for i in treeList:
         if i.attrib["clickable"]=='true':
             clickableList.append((i.attrib["text"],i.attrib["resource-id"],i.attrib["bounds"]))
    return clickableList

def note(parent,value,children):
    return [parent,value,children]

def getUIcheckable():
    time.sleep(1)
    xml = getXML()
    treeList = xmlToTree(xml)
    clickableList = clickableE(treeList)
    return clickableList

def getRootNode(rootText):
    rootList=getUIcheckable()
    for i in rootList:
        if i[0]==rootText:
            break
    return i

def getToRoot(root):
    while not d(text=root).exists:
        d.press.back()
    d(text=root).click()

def clickUI(node):
    if node[0]=="" and node[1]=="":
        bound=re.findall("\d+",node[2])
        x=int(bound[0])+int((int(bound[2]) - int(bound[0])) / 2)
        y=int(bound[1])+int((int(bound[3]) - int(bound[1])) / 2)
        d.click(x,y)
        time.sleep(2)
        print("坐标点击到我了")
    elif node[0]!="" and node[0]!=False:
        d(text=node[0]).click()
        print("文本点击到我了")
    else:
        d(resourceId=node[1]).click()
    time.sleep(2)  #等待界面跳转加载的时间

def father(tree,node):
    for i in tree:
        if node in i[2]:
            break
    return i

def brother(tree,node):
    return father(tree,node)[2]

def findRoutine(tree,note):
    routine = [note]
    while father(tree, note)[0] != False:
        father1 = father(tree, note)
        routine.insert(0, father1)
        note = father1
    #routine.insert(0, tree[0])
    return routine

def gotoAIMui(tree,note,root):
    getToRoot(root)
    routine=findRoutine(tree,note)
    for i in routine:
        clickUI(i)

def clearList(nodeList):
    removeList=[('', 'com.android.systemui:id/back', '[120,1776][360,1920]'), ('', 'com.android.systemui:id/home', '[420,1776][660,1920]'), ('', 'com.android.systemui:id/recent_apps', '[720,1776][960,1920]')]
    for i in removeList:
        if i in nodeList:
            nodeList.remove(i)


def findChildren(tree,node,root):
    print("要测试的node："+str(node))
    gotoAIMui(tree,node,root)
    clickableAfter=getUIcheckable()
    clickableBefore=brother(tree,node)
    for i in clickableBefore:
        if i != note and i in clickableAfter:
            clickableAfter.remove(i)
    if len(clickableAfter)<=1:
        children=[]
    else:
        children=clickableAfter
    return children   #对于点击之后界面上元素跟上一个界面不变的部分，不在重复加入为child

def doUITraval(root):
    root1=getRootNode(root)
    d(text=root).click()
    waitForVisitList = getUIcheckable()
    clearList(waitForVisitList)
    uiClickableTree.append(note(False, root1, waitForVisitList))

    while len(waitForVisitList) >= 1:
        selfNode = waitForVisitList[0]
        fNode = father(uiClickableTree, selfNode)
        cNode = findChildren(uiClickableTree, selfNode,root)
        clearList(cNode)
        if len(cNode)>=2:
            for j in cNode:
                waitForVisitList.append(j)
        uiClickableTree.append(note(fNode, selfNode, cNode))
        waitForVisitList.pop(0)

if __name__ == '__main__':

    doUITraval("Settings")
