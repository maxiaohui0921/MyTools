# -*- coding: utf-8 -*-
import uniout
'''
对树状结构数组进行处理，直接生成rotine，用例路径图
'''

def note(parent,value,children):
    return [parent,value,children]

treeE=[note(False,"webchat",["我","通信录","微信","发现"]),note("webchat","我",False),note("webchat","发现",["朋友圈"]),note("发现","朋友圈",False),note("webchat","通信录",False)]
treeE.append(note("webchat","微信",False))

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
    endNotes=ends(treeE)
    for i in endNotes:
        routine=findRoutine(treeE,i)
        print valueList(routine)
