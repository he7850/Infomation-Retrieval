# -*- coding:utf-8 -*-

import os

class DocStream():
    token_stream = dict()   # filename为key，token数组为value
    docs = []               # 存放所有文档的filename
    total = 0               # 给分析过的文档计数

    def parseDocs(self):
        path = "data"  # 文件夹目录
        files = os.listdir(path)  # 得到文件夹下的所有文件名称
        for filename in files:  # 遍历文件夹
            self.docs.append(filename)
            if not os.path.isdir(path+'/'+filename):  # 判断是否是文件夹，不是文件夹才打开
                self.token_stream[self.total] = self.parseTokenList(path+'/'+filename)
                print filename+" completed"
            self.total = self.total + 1

    def parseTokenList(self, filename): # 返回文件所有token组成的一个数组
        context_temp = ''  # 暂存标签正文
        with open(filename) as doc_file:
            for row in doc_file:
                current = 0
                row_len = len(row)
                while current < row_len:  # 逐字判断
                    if row[current].isdigit():
                        context_temp += row[current]
                    elif row[current].isupper() or row[current].islower():  # 字母全部转为小写
                        context_temp += row[current].lower()
                    elif row[current] == ' ' or row[current] == '\t' or row[
                        current] == '\n':  # 分隔符
                        current = current + 1
                        while (current < row_len and (row[current] == ' ' or row[current] == '\t' or row[
                            current] == '\n')):
                            current += 1
                        context_temp += ' '
                        current = current - 1
                    elif row[current] == ',' or row[current] == '.':  # 如果在数字中出现则忽略
                        if current > 0 and current < row_len-1 and row[current - 1].isdigit() and \
                                row[current + 1].isdigit():
                            pass
                        else:
                            context_temp += ' '
                    current += 1
        return context_temp.split(' ')

#
# stream = DocStream()
# stream.parseDocs()
# for filename in stream.token_stream:
#     print(filename,stream.token_stream.get(filename))
