__author__ = 'huang'

import numpy as np
import operator
from numpy import *
import os

def createDataSet():

    group = np.array([ [1.0, 1.1], [1.0, 1.0],
                    [0, 0], [0, 0.1] ])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):

    # compute the distances of inX between every point
    # distances =  sqrt((x1 - inX.x)^2 + (y1 - inX.y)^2)
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet  # 相减
    sqDiffMat = diffMat ** 2  # 平方
    sqDistances = sqDiffMat.sum(axis=1)  # 相加
    distances = sqDistances ** 0.5  # 开根号

    # return the index of the float numbers by orders
    # such as distances = array([1.48660687, 1.41421356, 0. , 0.1]) into array([2, 3, 1, 0])
    sortedDistIndicies = distances.argsort()


    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    returnMat = np.zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1

    return returnMat, classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    # normDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - np.tile(minVals, (m, 1))
    normDataSet = normDataSet / np.tile(ranges, (m, 1))
    return normDataSet, ranges, minVals

def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print('the classifier came back with: %d, the real answer is %d' % (classifierResult, datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print('the total error rate is %f' % (errorCount/float(numTestVecs)))

def classifyPerson():

    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input('percentage of time spend playing video games?'))
    ffMiles = float(input('frequent flier miles earned per year?'))
    iceCream = float(input('liters of ice cream consumed per year?'))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals) / ranges, normMat, datingLabels, 3)

    print('You will probably like this person: ', resultList[classifierResult - 1])

def img2vector(filename):
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('digits/trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros( (m,1024) )
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classStr = int(fileStr.split('_')[0])
        hwLabels.append(classStr)
        trainingMat[i, :] = img2vector('digits/trainingDigits/%s' % fileNameStr)
    testFileList = os.listdir('digits/testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('digits/testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print('the classifier came back with: %d, the real answer is: %d' % (classifierResult, classStr))
        if(classifierResult != classStr): errorCount += 1.0
    print('\nthe total numbers of errors is : %d' % errorCount)
    print('\nthe total error rate is : %f' % (errorCount/float(mTest)))
