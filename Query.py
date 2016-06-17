# coding=utf-8
__author__ = 'HUBIN'

import os
import json


def getWordPostList(keyword):
    # read index file
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


def getCombinePostList(left, right, logic='AND'):  # 返回合并倒排表，格式为[{'docno':xx},...]，与原倒排表保持一致
    res = []
    i = j = 0
    if logic == 'AND':
        while i < len(left) or j < len(right):
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
            if left[i]['docno'] < right[j]['docno']:
                res.append({'docno': left[i]['docno']})
                i += 1
            elif right[j]['docno'] < left[i]['docno']:
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
        if len(args) == 1:  # 树叶节点
            self.left = args[0]
            self.isLeaf = True
        elif len(args) == 3:  # 逻辑节点
            self.logic = args[0]  # logic
            self.left = args[1]  # left
            self.right = args[2]  # right

    def searchQueryResult(self):
        if self.isLeaf:
            self.res = getWordPostList(self.left)
        else:
            self.left.searchQueryResult()
            self.right.searchQueryResult()
            self.res = getCombinePostList(self.left, self.right, self.logic)

    def getQueryResult(self):
        print self.res
        return self.res

    def printTree(self):
        if self.isLeaf:
            print self.left
        else:
            print "logic:",self.logic
            print "left:"
            self.left.printTree()
            print "right:"
            self.right.printTree()

def getBoolQueryTree(line):  # 解析bool查询语句，生成查询树返回，line格式为 xx AND xx OR xx...
    root = BoolQuery(line[1], BoolQuery(line[0]), BoolQuery(line[2]))
    i = 2
    while i < len(line) - 2:
        if line[i + 1] == 'AND':  # AND优先级较高，纳入右子树
            root.right = BoolQuery(line[i + 1], root.right, BoolQuery(line[i + 2]))
        else:  # OR优先级较低，原树作为左子树生成新树
            root = BoolQuery(line[i + 1], root, line[i + 2])
        i += 2  # 下一个词
    root.printTree()
    return root


class PhraseQuery(object):
    def __init__(self, words):
        self.keywords = words[:]

    def getPostList(self):
        finalPostList = getWordPostList(self.keywords[0])
        i = 1
        while i < len(self.keywords):
            finalPostList = getCombinePostList(finalPostList, getWordPostList(self.keywords[i]))
            i += 1
        return finalPostList

    def sortByWordDistance(self):
        i = j = 0
        while i < len(self.keywords):
            while j < len(self.keywords):
                # TODO:给得到的文档排序
                pass


def compDocIndex(x, y):  # 比较文档出现频率，用于给倒排表排序
    if x['tf'] < y['tf']:
        return 1
    elif x['tf'] > y['tf']:
        return -1
    else:
        return 0


def query(input_line):
    keywords = input_line.split()
    if 'AND' in keywords or 'OR' in keywords:  # bool查询
        print 'bool query!'
        boolQueryTree = getBoolQueryTree(keywords)
        res = boolQueryTree.getQueryResult()
        for docIndexNode in res:
            print(docIndexNode['docno'])
    elif len(keywords) == 1:  # 单词查询
        postList = getWordPostList(keywords[0])
        print(postList)
    elif len(keywords) > 1:  # 短语查询
        res = PhraseQuery(keywords)
        for docIndexNode in res:
            print(docIndexNode['docno'])
