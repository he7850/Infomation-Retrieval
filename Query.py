# coding=utf-8
import fnmatch
import vsm

__author__ = 'HUBIN'

import os
import json
import word_corrector

diction = word_corrector.Dictionary()


# 倒排表格式：
# {
#   'someword':[ xx, [         [ xx,    xx, [xx,xx..] ]  ] ]
#                df  post_list   docId  tf  position
#       ],
#   ...
# }
def getWordPostList(keyword):  # 得到一个词的倒排表
    finalPostList = []
    for filename in os.listdir('index'):  # 遍历文件夹
        if fnmatch.fnmatch(filename, "index_*.json"):
            file = open('index/' + filename, 'r')
            # print filename + " loaded"
            postlist = json.load(file)
            if postlist.has_key(keyword):  # 在索引中匹配到keyword
                # print(postlist)
                for docNode in postlist[keyword][1]:  # 合并倒排表至finalPostList
                    # print(docNode)
                    if len(finalPostList) == 0 or docNode[0] > finalPostList[-1][
                        0]:  # 大部分docId更大的可以直接添加在finalPostList之后
                        finalPostList.append(docNode)
                    else:  # 插入中间某个位置
                        for i in range(len(finalPostList)):
                            if docNode[0] < finalPostList[i][0]:
                                finalPostList.insert(i, docNode)
                                break
            file.close()
    return finalPostList


def getCombinePostList(left, right, logic='AND'):  # 返回合并倒排表，格式为[ [xx]   ,...] 与原始倒排表保持一致
    #                                                                      docId
    res = []
    i = j = 0
    if logic == 'AND':
        while i < len(left) and j < len(right):
            if left[i][0] < right[j][0]:
                i += 1
            elif left[i][0] > right[j][0]:
                j += 1
            elif left[i][0] == right[j][0]:
                res.append([left[i][0]])
                i += 1
                j += 1
    elif logic == 'OR':
        while i < len(left) or j < len(right):
            if i < len(left) and j < len(right) and left[i][0] < right[j][0] or j == len(right):
                res.append([left[i][0]])
                i += 1
            elif i < len(left) and j < len(right) and left[i][0] > right[j][0] or i == len(left):
                res.append([right[j][0]])
                j += 1
            else:
                res.append([right[j][0]])
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
        self.keywords = [diction.getCorrectWord(word.lower()) for word in words]
        self.res = []
        # print self.keywords
        # print "word number:", len(self.keywords)

    def getAllWordsPostList(self):  # postList格式：[[2,  [231, 400], 0],...]
        #                                            tf   position    docId
        self.wordPostList = [getWordPostList(keyword) for keyword in self.keywords]
        # print "length of self.wordPostList:",len(self.wordPostList)
        # for postList in self.wordPostList:
            # print "length of postList:",len(postList)

    def getMatchedDocIndex(self):  # 得到可能匹配的文档（包含这些单词）
        self.docs = self.wordPostList[0]
        i = 1
        while i < len(self.wordPostList):
            self.docs = getCombinePostList(self.wordPostList[i], self.docs, logic='OR')
            i += 1
        print "matched docs:", self.docs

    def sortByWordDistanceAndFrequency(self):
        scores = []  # 存放各文档打分
        position = []  # 存放各文档各word的position，格式：[     [     [1,10,15],...],...]
        #                                               各文档 各单词 各位置

        for i in range(len(self.docs)):  # 给每篇文档记录word位置
            # print "record position for docid:", self.docs[i][0]
            j = 0
            position.append([])
            scores.append(0)
            while j < len(self.keywords):  # 得到每个单词的位置
                # print "for word ", self.keywords[j]
                position[i].append([])
                for docNode in self.wordPostList[j]:
                    if docNode[0] == self.docs[i][0]:  # 在第i个文档中出现
                        # print "keyword ", self.keywords[j], " found in doc:", docNode
                        # print "position ", docNode[2], " added to record"
                        position[i][j] = docNode[2]
                j += 1
            # print "docid:",i," position:",position[i]

        for i in range(len(self.docs)):  # 给每篇文档打分
            # print "set point for doc:", self.docs[i][0]
            for wordPositions in position[i]:  # 关键词出现次数越多，得分越高
                scores[i] += len(wordPositions)
            for k in range(len(self.keywords) - 1):  # 关键词距离越近，得分越高，距离大于5就不加分
                (dis, pos1, pos2) = findLeastDistance(position[i][k], position[i][k + 1])
                scores[i] += 20 * max(0, (5 - abs(dis)))
            # print "doc ", self.docs[i][0], "'s point is:", scores[i]

        vsmscore = vsm.do_search(self.keywords)
        for i in range(len(self.docs)):
            scores[i] += vsmscore[self.docs[i]][1] * 50

        for (id,score) in vsmscore:
           scores[id] += vsmscore*50

        for i in range(len(self.docs)):  # 记录结果并排序
            self.res.append([self.docs[i][0], scores[i]])
        # print "res:", self.res
        self.res.sort(scoreCmp)
        if len(self.res)>10:
            self.res = self.res[0:10]
        print "res after sort:", self.res


def findLeastDistance(positions1, positions2):
    i = j = 0
    pos1 = pos2 = -1
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
    if x[1] < y[1]:
        return 1  # return 1表示需要调整顺序
    elif x[1] > y[1]:
        return -1
    else:
        return 0


def scoreCmp(x, y):
    if x[1] < y[1]:
        return 1
    elif x[1] > y[1]:
        return -1
    else:
        return 0


def query(input_line):  # 输入一行进行查询
    keywords = input_line.split()
    print "keywords:", keywords
    if 'AND' in keywords or 'OR' in keywords:  # bool查询
        print 'bool query!'
        for i in range(len(keywords)):
            if not keywords[i] == 'AND' and not keywords[i] == 'OR':
                keywords[i] = diction.getCorrectWord(keywords[i])
        boolQueryTree = getBoolQueryTree(keywords)
        boolQueryTree.searchQueryResult()
        res = boolQueryTree.getQueryResult()
        for docIndexNode in res:
            print(docIndexNode[0])
    elif len(keywords) == 1:  # 单词查询
        postList = getWordPostList(diction.getCorrectWord(keywords[0].lower()))
        print(postList)
    elif len(keywords) > 1:  # 短语查询
        phraseQuery = PhraseQuery(keywords)
        phraseQuery.getAllWordsPostList()
        phraseQuery.getMatchedDocIndex()
        phraseQuery.sortByWordDistanceAndFrequency()
        # print phraseQuery.res
        for (docId,score) in phraseQuery.res:
            print docId, ':%d' % score
