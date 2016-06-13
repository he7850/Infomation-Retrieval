# -*- coding:utf-8 -*-

import copy

#file_test = r'test.txt'

tag_list = ['DOC','DOCNO']



class DocStream():
    token_stream = dict()
    docNo = ''
    doc_token = []
    doc_token_str=''
    docnum = 0

    def __splitter__(self,filename):
        context_temp = ''       #暂存标签正文
        tag_stack = []          #标签栈
        with open(filename) as doc_file:
            for row in doc_file:
                #print(row)
                i= 0
                #print(context_temp)
                row_len = len(row)
                #print(row_len)
                while i < row_len:
                    #print(row[i])
                    #逐字判断
                    #后标签
                    if row[i] == '<' and row[i+1] =='/' :
                        #i += 1
                        while row[i] != '>':
                            i += 1
                            continue
                        temp = tag_stack.pop()
                        if temp == 'DOC':
                            self.doc_token_str =  copy.deepcopy(context_temp)
                            self.token_stream.setdefault(self.docnum,self.doc_token_str)
                            #print('doc num is ',self.docNo)
                            self.docNo = ''
                            context_temp = ''
                        elif temp == 'DOCNO':
                            self.docnum +=1
                            self.docNo  = copy.deepcopy(context_temp)
                    #前标签
                    elif row[i] == '<':
                        tag_context=''
                        i += 1
                        while row[i] !='>':
                            tag_context += row[i]
                            i += 1
                        #if tag_context in tag_list:
                        tag_stack.append(tag_context)
                        tag_context = ''
                    elif row[i].isdigit():
                        i += 1
                        continue
                    elif row[i].isupper() or row[i].islower():
                        context_temp += row[i].lower()
                    elif row[i] == ' ' or row[i] == '\t':
                        i += 1
                        while (row[i] == ' 'or row[i] == '\t') and i < row_len:
                            i += 1
                        context_temp += ' '
                        i -= 1
                    elif row[i] == '\n':
                        i += 1
                        while i < row_len and row[i] == '\n':
                            i += 1
                        i -= 1
                        context_temp += ' '
                    i += 1
        return

    def __stream_token__(self):
        for i in self.token_stream:
            row = self.token_stream.get(i)
            if ' ' not in row:
                row_split = row
            else:
                row_split = row.split(' ')
            while '' in row_split:
                row_split.remove('')
            self.token_stream[i] = row_split
        return
    def getTokenStream(self,filename):
        self.__splitter__(filename)
        self.__stream_token__()
        return self.token_stream
'''
stream = DocStream()
test_dic = stream.getTokenStream(filename_1)
for i in test_dic:
    print(i,':',test_dic.get(i))
'''