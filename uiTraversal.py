# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import time

#生成树，把xml中所有的节点取出来放在列表中
def xmlToTree(xml):  #root[0]
    f = open(xml, 'rt')
    tree = ET.parse(f)
    root = tree.getroot()
    visitList=[]
    visitList.append(root[0])
    waitforHandlingNotes=[]
    waitforHandlingNotes.append(root[0])
    while len(waitforHandlingNotes)>=1:
            for i in waitforHandlingNotes:
                for j in i:
                    visitList.append(j)
                    if len(j)>=1:
                        waitforHandlingNotes.append(j)
                waitforHandlingNotes.remove(i)
    return visitList

#扫描树，把上面列表中的节点挨个检查属性，如果是clickable=true就把该节点的text resourceid bound值组成tuple，加入列表返回
def clickableE(treeList):
    clickableList = []
    for i in treeList:
         if i.attrib["clickable"]=='true':
             clickableList.append((i.attrib["text"],i.attrib["resource-id"],i.attrib["bounds"]))
    return clickableList

def getXML():
    os.popen("adb shell uiautomator dump /sdcard/abc.xml")
    os.popen("adb pull /sdcard/abc.xml")
    os.popen("adb shell rm /sdcard/abc.xml")
    file=os.path.join(os.getcwd(),"abc.xml")
    return file

if __name__ == '__main__':
    #xml = r'C:\Users\maxh\Documents\GitHub\yutu\uidump.xml'
    xml=getXML()
    treeList = xmlToTree(xml)
    print clickableE(treeList)
    print len(clickableE(treeList))