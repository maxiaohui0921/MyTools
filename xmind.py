# -*- coding: utf-8 -*-
'''
抓取xmind文件中的内容，生成树状结构数组
'''
from mekk.xmind import XMindDocument
import time

xfile=r'C:\Users\maxh\Documents\GitHub\yutu\webchat.xmind'

def getSheet(file):
    xmindf=XMindDocument.open(file)
    sheet=xmindf.get_first_sheet()
    print "画布名称：",sheet.get_title()
    return sheet

def getRoot(sheet):
    root=sheet.get_root_topic()
    return root

def getSubs(parent):
    children=[]
    for i in parent.get_subtopics():
        children.append(i)
    if len(children)>0:
        return children
    else:
        return None


if __name__ == '__main__':
    sheet=getSheet(xfile)
    print getRoot(sheet).get_title()
    for i in getSubs(getRoot(sheet)):
        print i.get_title()
