# -*- coding:utf-8 -*-
import fnmatch
import os
import Gamma
import math
import json

# 词典-倒排表
class InvertIndex_Builder():
    token_postList = dict()  # 倒排表集合，key为单词本身
    token_dict = []  # 字典

    # 添加到倒排表
    # para token    添加的词项
    #      docno    词项所在文档id
    #      position 词项所在文档出现位置
    # 倒排表格式：
    # {
    #   'someword':[ xx, [         [ xx,    xx, [xx,xx..] ]  ] ]
    #                df  post_list   docid  tf  position
    #       ],
    #   ...
    # }
    def addToPostList(self, token, docId, position):
        # print self.token_postList.keys()
        postlist = self.token_postList[token][1]
        list_len = len(postlist)
        if docId not in [ docNode[0] for docNode in postlist]:
            postlist.append([docId, 1, [position]])
            self.token_postList[token][0] += 1
        else:
            docNodeIndex = [docNode[0] for docNode in postlist].index(docId)
            postlist[docNodeIndex][1] +=1
            postlist[docNodeIndex][2].append(position)

    # 添加到词典
    def addToDict(self, token):
        self.token_postList[token] = [0,[]]
        self.token_dict.append(token)

    # spimi:内存式单遍扫描索引构建方法（Single-pass in-memeory indexing）
    # token_stream 为文档集数组：key=docId, value = [token1,token2,...]
    def spimi_build(self, token_stream):
        doc_pointer = 0  # token_stream中，指向doc的索引
        token_pointer = 0  # token_stream中，指向token的索引

        max_index_size = 4096
        index_size = 0
        index_number = 0

        while doc_pointer < len(token_stream):
            while token_pointer < len(token_stream[doc_pointer]):
                temp_token = token_stream[doc_pointer][token_pointer]
                if not temp_token in self.token_dict:  # 判断是否在词典中
                    self.addToDict(temp_token)
                self.addToPostList(temp_token, doc_pointer, token_pointer)  # 添加至倒排记录表

                token_pointer += 1
                index_size += 1
            print "doc " + str(doc_pointer) + " postList insert completed"

            doc_pointer += 1
            token_pointer = 0

            if index_size > max_index_size:
                with open("index/index_" + str(index_number) + ".json", 'w+') as outfile:
                    try:
                        json.dump(self.token_postList, outfile)
                    except UnicodeDecodeError:
                        print self.token_postList
                        json.dump(self.token_postList, outfile)
                    finally:
                        outfile.close()
                self.token_postList = dict()
                self.token_dict = []
                index_size = 0
                index_number += 1

        if index_size != max_index_size:
            with open("index/index_" + str(index_number) + ".json", 'w+') as outfile:
                try:
                    json.dump(self.token_postList, outfile)
                except UnicodeDecodeError:
                    print self.token_postList
                    json.dump(self.token_postList, outfile)
                finally:
                    outfile.close()

'''
t = Gamma.__gamma__(9)
#print(bin(t))
t = Gamma.__gammaUncompress__(t)
print(t)
'''
