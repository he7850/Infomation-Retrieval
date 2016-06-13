# -*- coding:utf-8 -*-
from Linklist import LinkList
import Gamma
import math

# 词典节点
class Dict_Node():
    def __init__(self,df,post_point,dict_point):
        self.df = df                    #词项文档频率
        self.post_point = post_point    #倒排表指针
        self.dict_point = dict_point    #词典字符串指针
    def __set_df__(self,df):
        self.df = df

    def __outNode__(self):
        s = ''
        s += str(self.df)
        s+=','
        s += str(self.dict_point)
        return s


# 词典-倒排表
# ps 链表的Node init的数据，为双层list
class Dict_Postlist():
    token_dict={}
    #token_dict_all = {}
    #post_list = LinkList() # 倒排索引表
    dic_string=''           # 单一字符串字典
    tail = 0;               # dic_string 的指针

    # 添加到倒排表
    # para term  添加的词项
    #      docno 词项所在文档id
    def __addToPostList__(self,term,docno):
       # if term in self.token_dict:
        templink = self.token_dict[term].post_point
        if not templink.increase(docno):
            item = [docno,1]
            templink.append(item)
            self.token_dict[term].df += 1
            return
        self.token_dict[term].df += 1
        return

    # 添加到词典，
    # para term
    #      docno
    def __addToDict__(self,term,docno):
        post_list = LinkList()
        node = Dict_Node(0,post_list,self.tail)
        #print(node.df,' ',node.post_point,' ',node.dict_point)
        self.token_dict[term] = node
        self.tail+=len(term)
        self.dic_string+=term
        #print(node.df,' ',node.post_point,' ',node.dict_point)
        self.__addToPostList__(term,docno)
        return

    # spimi单步
    # token_stream 为字典，key=docno, value = [term1,term2,...]
    # return flag 是否还有未输出内容
    def __spimi_invert__(self,token_stream,filename):
        doc_pointer = 1         #token_stream 中，指向doc的索引
        term_pointer = 0        #token_stream中，指向term的索引
        line_index = 0
        max_line = 10000
        flag = False
        while line_index <= max_line:
            if doc_pointer > len(token_stream):
                flag = True
                break
            elif term_pointer >= len(token_stream[doc_pointer]):
                doc_pointer +=1
                term_pointer = 0
                continue
            # 判断是否在词典中
            temp_term = token_stream[doc_pointer][term_pointer]
            if temp_term in self.token_dict:
                self.__addToPostList__(temp_term,doc_pointer)
            else:
                self.__addToDict__(temp_term,doc_pointer)

            line_index+=1
            term_pointer+=1
        #print(self.token_dict.get('of').df)
        with open("output.txt",'w+') as outfile:
            for item in self.token_dict:
                s = self.token_dict[item].__outNode__()
                # 输出词项 以及 df，词项指针
                out = ''.join([item,'|',s,'   '])
                outfile.write(out)
                outfile.write('\n')
                temp_link = self.token_dict[item].post_point
                outfile.write(temp_link.output())
                outfile.write('\n')
        return flag

    #TODO get set method


    # spimi算法
    def spimi_build(self,token_stream):
        fileindex = 0
        suff = 'Spimi-output/'
        while(not self.__spimi_invert__(token_stream,suff+str(fileindex))):
            fileindex+=1
        return

'''
t = Gamma.__gamma__(9)
#print(bin(t))
t = Gamma.__gammaUncompress__(t)
print(t)
'''