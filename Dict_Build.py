# -*- coding:utf-8 -*-
from Linklist import LinkList
import Gamma
import math


# 词典节点
class Dict_Node():
    def __init__(self, df, post_list):
        self.df = df  # 词项文档频率
        self.post_list = post_list  # 倒排表指针,倒排表格式：[[docid,tf],..]

    def set_df(self, df):
        self.df = df

    def outputNode(self):
        return str(self.df)


# 词典-倒排表
class Dict_Postlist():
    token_postList = {}  # 倒排表集合，key为单词本身
    token_dict = []  # 字典
    docs = []

    # 添加到倒排表
    # para token    添加的词项
    #      docno    词项所在文档id
    #      position 词项所在文档出现位置
    def addToPostList(self, token, docno, position):
        templink = self.token_postList[token].post_list
        if not templink.increase(docno):  # docno词项频率加一
            item = [docno, 1]
            templink.append(item)
        self.token_postList[token].df += 1

    # 添加到词典
    def addToDict(self, token):
        post_list = LinkList()
        node = Dict_Node(0, post_list)
        self.token_postList[token] = node
        self.token_dict.append(token)

    # spimi单步
    # token_stream 为文档集数组：key=docno, value = [token1,token2,...]
    def spimi_invert(self, token_stream):
        doc_pointer = 0  # token_stream中，指向doc的索引
        token_pointer = 0  # token_stream中，指向token的索引
        while doc_pointer < len(token_stream):
            while token_pointer < len(token_stream[doc_pointer]):
                temp_token = token_stream[doc_pointer][token_pointer]
                if not temp_token in self.token_dict:  # 判断是否在词典中
                    self.addToDict(temp_token)
                self.addToPostList(temp_token, doc_pointer, token_pointer)  # 添加至倒排记录表

                token_pointer += 1

            doc_pointer += 1
            token_pointer = 0
            print "doc " + str(doc_pointer) + " postList insert completed"
            # print(self.token_dict.get('of').df)
            # with open("output.txt", 'w+') as outfile:
            #     for item in self.token_dict:
            #         s = self.token_dict[item].outputNode()
            #         # 输出词项 以及 df，词项指针
            #         out = item + '|' + s
            #         outfile.write(out)
            #         outfile.write('\n')
            #         temp_link = self.token_dict[item].post_list
            #         outfile.write(temp_link.output())
            #         outfile.write('\n')

    # spimi算法
    def spimi_build(self, docStream):
        self.spimi_invert(docStream.token_stream)
        self.docs = docStream.docs[:]

    def query(self, keyword):
        res = self.token_postList.get(keyword).post_list
        p = res.head
        if p == 0:
            print('not found')
        count = p.docno
        print "filename:" + str(count) + ',' + "token frequency:" + str(p.tf)
        p = p.next
        while p != 0:
            count += Gamma.__gammaUncompress__(p.docno)
            print "filename:" + self.docs[count] + "(id:" + str(count) + '),' + "token frequency:" + str(p.tf)
            p = p.next


'''
t = Gamma.__gamma__(9)
#print(bin(t))
t = Gamma.__gammaUncompress__(t)
print(t)
'''
