# -*- coding: utf-8 -*-
import uniout
import xmind

def ends(tree):
    endNote=[]
    for i in tree:
        if i[2]==False:
            endNote.append(i)
    return endNote   #返回所有 end note列表

def findfather(tree,note):
	for j in tree:
		if j[1]==note[0] and note[1] in j[2]:
			break
	return j

def findRoutine(tree,note):
    routine=[note]
    while findfather(tree,note)[0]!=False:
        father=findfather(tree, note)
        routine.insert(0,father)
        note=father
    routine.insert(0, tree[0])
    return routine #返回的还是note列表

def valueList(tree):
    value=[]
    for i in tree:
        value.append(i[1])
    return value

if __name__ == '__main__':

    xfile = r'C:\Users\maxh\Documents\GitHub\yutu\webchat.xmind'
    sheet = xmind.getSheet(xfile)
    treeE=xmind.getTreeData(sheet)

    endNotes=ends(treeE)
    for i in endNotes:
        routine=findRoutine(treeE,i)
        print valueList(routine)