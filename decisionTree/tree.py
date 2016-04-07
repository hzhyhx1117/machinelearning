__author__ = 'huang'

from math import log
import operator

def calcShannonEnt(dataSet):
    # calculate the shannonentropy

    numEntries = len(dataSet)
    labelCounts = {}

    # 统计每个label的个数
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1

    # 计算 shannonentropy sum(-p*log2(p))
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
   """
   :param dataSet: 原始的DataSet
   :param axis: 划分数据集的第几个特征
   :param value: 第axis个特征需要返回的值
   :return: 分好的retDataSet
   """
   retDataSet = []
   for featVec in dataSet:
       if featVec[axis] == value:
          reducedFeatVec = featVec[:axis]
          reducedFeatVec.extend(featVec[axis+1:])
          retDataSet.append(reducedFeatVec)
   return retDataSet

def chooseBestFeatureToSplit(dataSet):
    # 找到最好的特征划分集，根据信息上来划分

    numFeatures = len(dataSet[0]) - 1 # 计算有几个特征
    baseEntropy = calcShannonEnt(dataSet) # 初始化最好的信息熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        # 获得每一个特征的所有数值
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            # 按照每一种数值来计算每一个特征的信息熵
            subDataSet = splitDataSet(dataSet, i ,value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy # 总体的信息增益 g(D, A) = H(D) - H(D | A)
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain # 最佳信息增益
            bestFeature = i # 最佳特征
    return bestFeature

def majorityCnt(classList):
    # 采用多数表决的方法来决定特征
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
            classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):

    # 类别完全相同则停止继续划分
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    # 遍历完所有特征后仍然无法完成数据集的唯一划分，于是返回出现最多的特征的标签值
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)

    # 递归生成特征树
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {
        bestFeatLabel:{}
    }
    del(labels[bestFeat]) # 删除当前的特征
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree)[0]
    secondDic = inputTree[firstStr]
    featIndex = featLabels.index(firstStr) # 将标签字符转化为索引
    for key in secondDic.keys():
        if testVec[featIndex] == key:
            if type(secondDic[key]).__name__=='dict':
                classLabel = classify(secondDic[key], featLabels, testVec)
            else:
                classLabel = secondDic[key]
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    with open(filename, 'wb') as fw:
        pickle.dump(inputTree, fw)

def grabTree(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

if __name__ == '__main__':
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = createTree(lenses, lensesLabels)
    import treePlotter
    treePlotter.createPlot(lensesTree)