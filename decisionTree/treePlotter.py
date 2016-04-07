__author__ = 'huang'

import matplotlib.pyplot as plt

# 定义文本框和箭头格式
decisionNode = dict(boxstyle='sawtooth', fc='0.8')
leafNode = dict(boxstyle='round4', fc='0.8')
arrow_args = dict(arrowstyle='<-')

def plotNode(nodeText, centerPt, parentPt, nodeType):

    # 绘制带箭头的注解
    createPlot.ax1.annotate(nodeText, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)

def createPlot(inTree):

    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])

    # 绘图区
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()

def getNumLeafs(myTree):

    # myTree = { 'no surfacing': {0: 'no', 1: {'flippers': {...}}}}

    numLeafs = 0
    firstStr = list(myTree)[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else: numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):

    # 获得树的深度
    maxDepth = 0
    firstStr = list(myTree)[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:  thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees = [{
        'no surfacing': {
                0: 'no',
                1: {
                    'flippers': {
                        0: 'no',
                        1: 'yes'
                    }
                }
            }
        },
        {
           'no surfacing': {
               0: 'no',
               1: {
                   'flippers': {
                       0: {'head': {0: 'no', 1: 'yes'}},
                       1: 'no'
                   }
                }
           }
        }]
    return listOfTrees[i]

def plotMidText(cntrPt, parentPt, txtString):

    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):

    # 计算树长和树高
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)

    firstStr = list(myTree)[0]

    # 计算出当前的绘制节点的位置
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)

    # 标记子节点属性值，添加文本标签信息
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    # 减少y的偏移
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD

    for key in secondDict.keys():
        # 对两种情况惊醒递归
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
