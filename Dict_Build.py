# -*- coding:utf-8 -*-
import fnmatch
import os
from Linklist import LinkList
import Gamma
import math
import json

# 词典-倒排表
class Dict_Postlist():
    token_postList = dict()  # 倒排表集合，key为单词本身
    token_dict = []  # 字典
    docs = []  # 文档ID对应文档名

    # 添加到倒排表
    # para token    添加的词项
    #      docno    词项所在文档id
    #      position 词项所在文档出现位置
    # 倒排表格式：
    # {
    #   'someword':{
    #       'df':xx,
    #       'post_list':[ { 'docno':xx,'tf':xx,'position':[xx,...] },... ]
    #       },
    #   ...
    # }
    def addToPostList(self, token, docno, position):
        # print self.token_postList.keys()
        temp_postlist = self.token_postList[token]['post_list']
        list_len = len(temp_postlist)
        temp_index = 0
        while temp_index < list_len:
            if temp_postlist[temp_index]['docno'] == docno:
                temp_postlist[temp_index]['tf'] = temp_postlist[temp_index]['tf'] + 1
                temp_postlist[temp_index]['position'].append(position)
                break
            temp_index = temp_index + 1
        if temp_index == list_len:
            temp_postlist.append({'docno': docno, 'tf': 1, 'position': [position]})
            self.token_postList[token]['df'] += 1

    # 添加到词典
    def addToDict(self, token):
        self.token_postList[token] = {'df': 0, 'post_list': []}
        self.token_dict.append(token)

    # spimi单步
    # token_stream 为文档集数组：key=docno, value = [token1,token2,...]
    def spimi_invert(self, token_stream):
        doc_pointer = 0  # token_stream中，指向doc的索引
        token_pointer = 0  # token_stream中，指向token的索引

        max_index_size = 2333
        index_size = 0
        index_order = 0

        while doc_pointer < len(token_stream):
            while token_pointer < len(token_stream[doc_pointer]):
                temp_token = token_stream[doc_pointer][token_pointer]
                if not temp_token in self.token_dict:  # 判断是否在词典中
                    self.addToDict(temp_token)
                self.addToPostList(temp_token, doc_pointer, token_pointer)  # 添加至倒排记录表

                token_pointer += 1
                index_size += 1

            doc_pointer += 1
            token_pointer = 0
            print "doc " + str(doc_pointer) + " postList insert completed"

            if index_size > max_index_size:
                with open("index/index_" + str(index_order) + ".json", 'w+') as outfile:
                    json.dump(self.token_postList, outfile, indent=4)
                    outfile.close()
                self.token_postList = {}
                self.token_dict = []
                index_size = 0
                index_order = index_order + 1

        if index_size != max_index_size:
            with open("index/index_" + str(index_order) + ".json", 'w+') as outfile:
                # print self.token_postList
                json.dump(self.token_postList, outfile, indent=4)
                outfile.close()

    # spimi算法建立倒排索引
    def spimi_build(self, docStream):
        self.spimi_invert(docStream.token_stream)
        self.docs = docStream.docs[:]
        self.saveDocIndexFile()

    def saveDocIndexFile(self):
        f = open("doc_filename_index", 'w')
        json.dump(self.docs, f)
        f.close()



'''
t = Gamma.__gamma__(9)
#print(bin(t))
t = Gamma.__gammaUncompress__(t)
print(t)
'''
