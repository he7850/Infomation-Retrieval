# coding=utf-8
import math

__author__ = 'HUBIN'

import os
import json
import word_corrector

diction = word_corrector.Dictionary()

def getWordPostList(keyword):  # 得到一个词的倒排表
    finalPostList = []
    for filename in os.listdir('index'):  # 遍历文件夹
        file = open('index/' + filename, 'r')
        postlist = json.load(file)
        # print filename + " loaded"
        if postlist.has_key(keyword):  # 在索引中匹配到keyword
            # print(postlist)
            for docNode in postlist.get(keyword).get('post_list'):  # 合并倒排表至finalPostList
                # print(docNode)
                if len(finalPostList) == 0 or docNode['docno'] > finalPostList[-1][
                    'docno']:  # 大部分docId更大的可以直接添加在finalPostList之后
                    finalPostList.append(docNode)
                else:  # 插入中间某个位置
                    for i in range(len(finalPostList)):
                        if docNode['docno'] < finalPostList[i]['docno']:
                            finalPostList.insert(i, docNode)
        file.close()
    return finalPostList
    # # finalPostList.sort(compDocIndex)
    # docIndexFile = open("doc_filename_index", 'r')
    # docIndex = json.load(docIndexFile)  # get docIndex
    # if len(finalPostList) == 0:
    #     print "keyword not found in docs"
    # for eachNode in finalPostList:
    #     print "filename:" + docIndex[eachNode['docno']] + "(id:" + str(
    #         eachNode['docno']) + '),' + "token frequency:" + str(eachNode['tf'])


def getCombinePostList(left, right, logic='AND'):  # 返回合并倒排表，格式为[{'docno':xx},...]
    res = []
    i = j = 0
    if logic == 'AND':
        while i < len(left) and j < len(right):
            if left[i]['docno'] < right[j]['docno']:
                i += 1
            elif left[i]['docno'] > right[j]['docno']:
                j += 1
            elif left[i]['docno'] == right[j]['docno']:
                res.append({'docno': left[i]['docno']})
                i += 1
                j += 1
    elif logic == 'OR':
        while i < len(left) or j < len(right):
            if i < len(left) and j < len(right) and left[i]['docno'] < right[j]['docno'] or j == len(right):
                res.append({'docno': left[i]['docno']})
                i += 1
            elif i < len(left) and j < len(right) and left[i]['docno'] > right[j]['docno'] or i == len(left):
                res.append({'docno': right[j]['docno']})
                j += 1
            else:
                res.append({'docno': right[j]['docno']})
                i += 1
                j += 1
    return res


class BoolQuery(object):
    res = ''
    left = ''
    right = ''
    logic = ''
    isLeaf = False

    def __init__(self, *args):
        if len(args) == 1:  # 单参数为树叶节点
            self.left = args[0]
            self.isLeaf = True
        elif len(args) == 3:  # 3参数为逻辑节点
            self.logic = args[0]  # logic
            self.left = args[1]  # left
            self.right = args[2]  # right

    def searchQueryResult(self):  # 搜索结果
        if self.isLeaf:
            self.res = getWordPostList(self.left)
        else:
            self.left.searchQueryResult()
            self.right.searchQueryResult()
            self.res = getCombinePostList(self.left.res, self.right.res, self.logic)

    def getQueryResult(self):  # 返回当前查询结果
        print self.res
        return self.res

    def printTree(self):  # 打印boolquery树
        if self.isLeaf:
            print self.left
        else:
            print "logic:", self.logic
            print "left:"
            self.left.printTree()
            print "right:"
            self.right.printTree()


def getBoolQueryTree(line):  # 解析bool查询语句，生成查询树返回，line格式为 xx AND xx OR xx...
    root = BoolQuery(line[1], BoolQuery(line[0].lower()), BoolQuery(line[2].lower()))
    i = 2
    while i < len(line) - 2:
        if line[i + 1] == 'AND':  # AND优先级较高，纳入右子树
            root.right = BoolQuery(line[i + 1], root.right, BoolQuery(line[i + 2].lower()))
        else:  # OR优先级较低，原树作为左子树生成新树
            root = BoolQuery(line[i + 1], root, BoolQuery(line[i + 2].lower()))
        i += 2  # 下一个词
    root.printTree()
    return root


class PhraseQuery(object):
    wordPostList = []  # 存放每个词的postList
    docs = []  # 存放符合的文档集
    keywords = []
    res = []

    def __init__(self, words):
        for word in words:
            self.keywords.append(diction.getCorrectWord(word.lower()))
        self.res = []
        print self.keywords

    def getAllWordsPostList(self):  # postList格式：[{"tf": 2, "position": [231, 400], "docno": 0},...]
        self.wordPostList = []
        for keyword in self.keywords:
            self.wordPostList.append(getWordPostList(keyword))
        print "word number:", len(self.wordPostList)

    def getMatchedDocIndex(self):  # 得到可能匹配的文档（包含这些单词）
        self.docs = []
        self.docs = self.wordPostList[0]
        i = 1
        while i < len(self.wordPostList):
            self.docs = getCombinePostList(self.wordPostList[i], self.docs)
            i += 1
        print "matched docs:", self.docs

    def sortByWordDistanceAndFrequency(self):
        points = []  # 存放各文档打分
        position = []  # 存放各文档各word的position，格式：[     [     [1,10,15],...],...]
        #                                               各文档 各单词 各位置

        for i in range(len(self.docs)):  # 给每篇文档记录word位置
            j = 0
            position.append([])
            points.append(0)
            while j < len(self.keywords):  # 得到每个单词的位置
                # print "word ", j, ":", self.wordPostList[j]
                for docNode in self.wordPostList[j]:
                    # print "docNode:",docNode
                    if docNode['docno'] == self.docs[i]['docno']:  # 在第i个文档中出现
                        print "keyword ", self.keywords[j], " found in doc:", docNode
                        print "position ", docNode['position'], " added to record"
                        position[i].append(docNode['position'])
                j += 1

        for i in range(len(self.docs)):  # 给每篇文档打分
            print "set point for doc:", self.docs[i]
            for wordPositions in position[i]:  # 关键词出现次数越多，得分越高
                points[i] += len(wordPositions)
            for k in range(len(self.keywords) - 1):  # 关键词距离越近，得分越高，距离大于5就不加分
                (dis, pos1, pos2) = findLeastDistance(position[i][k], position[i][k + 1])
                points[i] += 50 * max(0, (5 - abs(dis)))
            print "doc ", self.docs[i], "'s point is:", points[i]

        for i in range(len(self.docs)):  # 记录结果并排序
            self.res.append({'docno': self.docs[i], 'point': points[i]})
        print "res:", self.res
        self.res.sort(pointCmp)
        print "res after sort:", self.res


def findLeastDistance(positions1, positions2):
    i = j = 0
    pos1 = pos2 = 0
    res = 9999
    while i < len(positions1) and j < len(positions2):
        if abs(positions1[i] - positions2[j]) < abs(res):
            (res, pos1, pos2) = (positions1[i] - positions2[j], i, j)
        if positions1[i] < positions2[j]:
            i += 1
        elif positions1[i] > positions2[j]:
            j += 1
        else:
            i += 1
            j += 1
    return (res, pos1, pos2)


def compDocIndex(x, y):  # 比较文档出现频率，用于给倒排表排序
    if x['tf'] < y['tf']:
        return 1  # return 1表示需要调整顺序
    elif x['tf'] > y['tf']:
        return -1
    else:
        return 0


def pointCmp(x, y):
    if x['point'] < y['point']:
        return 1
    elif x['point'] > y['point']:
        return -1
    else:
        return 0


def query(input_line):  # 输入一行进行查询
    keywords = input_line.split()
    print "keywords:", keywords
    if 'AND' in keywords or 'OR' in keywords:  # bool查询
        print 'bool query!'
        for i in range(len(keywords)):
            if not keywords[i]=='AND' and not keywords[i]=='OR':
                keywords[i] = diction.getCorrectWord(keywords[i])
        boolQueryTree = getBoolQueryTree(keywords)
        boolQueryTree.searchQueryResult()
        res = boolQueryTree.getQueryResult()
        for docIndexNode in res:
            print(docIndexNode['docno'])
    elif len(keywords) == 1:  # 单词查询
        postList = getWordPostList(diction.getCorrectWord(keywords[0].lower()))
        print(postList)
    elif len(keywords) > 1:  # 短语查询
        phraseQuery = PhraseQuery(keywords)
        phraseQuery.getAllWordsPostList()
        phraseQuery.getMatchedDocIndex()
        phraseQuery.sortByWordDistanceAndFrequency()
        # print phraseQuery.res
        for docIndexNode in phraseQuery.res:
            print(docIndexNode['docno'], docIndexNode['point'])
