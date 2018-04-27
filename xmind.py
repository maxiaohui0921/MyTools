# -*- coding: utf-8 -*-
'''
抓取xmind文件中的内容，生成树状结构数组
'''
from mekk.xmind import XMindDocument

xfile=r'C:\Users\maxh\Documents\GitHub\yutu\webchat.xmind'

def note(parent,value,children):
    return [parent,value,children]

def getSheet(file):
    xmindf=XMindDocument.open(file)
    sheet=xmindf.get_first_sheet()
    print "画布名称：",sheet.get_title()
    return sheet

def getRoot(sheet):
    root=sheet.get_root_topic()
    return root

def getValue(xmindNote):
    return xmindNote.get_title()


def getSubs(parent):  #返回子节点列表，第一个放的是节点，第二个放的是节点的值
    children=[]
    childrenValue=[]
    for i in parent.get_subtopics():
        children.append(i)
        childrenValue.append(getValue(i))
    if len(children)>0:
        return children,childrenValue
    else:
        return False,False

def arrayTBD(parent,children):  #把子节点分离后，都加上一个父节点，组成一个数组,例如 [[p,c1],[p,c2]]
    tag=[]
    for i in children:
        tag.append([parent,i])
    return tag

def getTreeData(sheet):
    tbdNotes=[]  #该列表存放待添加的节点，节点的结构是[parentNote,childNote],其中子节点是待添加的节点
    xTree=[]  #最后获取的列表

    root = getRoot(sheet)     #初始化数据
    xTree.append(note(False,getValue(root),getSubs(root)[1])) #添加初始节点
    tbdArray=arrayTBD(root,getSubs(root)[0])
    for i in tbdArray:
        tbdNotes.append(i)

    while len(tbdNotes)>=1:
        fnoteXmind=tbdNotes[0][0]  #父节点，xmind类型
        cnoteXmind=tbdNotes[0][1]  #子节点，xmind类型
        sNoteXmindList=getSubs(tbdNotes[0][1])[0]   #子节点的子节点，xmind类型，list
        sNoteValueList=getSubs(tbdNotes[0][1])[1]#子节点的子节点，value类型，list
        xTree.append(note(getValue(fnoteXmind),getValue(cnoteXmind),sNoteValueList)) #把值加入到目标列表中
        if sNoteXmindList!=False:#把子和孙加入到待处理列表中
            sList=arrayTBD(cnoteXmind,sNoteXmindList)
            for j in sList:
                tbdNotes.append(j)
        tbdNotes.pop(0)

    return xTree

if __name__ == '__main__':
    sheet=getSheet(xfile)
    print(getTreeData(sheet))
