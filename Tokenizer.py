# -*- coding:utf-8 -*-
import fnmatch

import os
import json

import re

skipCharacters = " !#$%^&*();:\n\t\\\"?!{}[]<>"

class Tokenizer():
    doc_word_stream = []  # docId为key，token数组为value
    doc_names = []  # 存放所有文档的filename
    path = "data"  # 文件夹目录

    def countDocs(self):
        files = os.listdir(self.path)  # 得到文件夹下的所有文件名称
        for filename in files:  # 遍历文件夹
            if fnmatch.fnmatch(filename, "*.html"):
                self.doc_names.append(filename)
        f = open("doc_names", 'w')
        json.dump(self.doc_names, f)
        f.close()

    def parseDocs(self):
        for docId in range(len(self.doc_names)):  # 遍历文件夹
            self.doc_word_stream.append(self.parseTokenList(self.path + '/' + self.doc_names[docId]))
            print "doc " + str(docId) + " tokenize completed"

    def parseTokenList(self, filename):  # 返回文件所有token组成的一个数组
        token_list = []  # 暂存标签正文
        doc_file = open(filename)
        for row in doc_file:
            token_list += [ unicode( token , errors='ignore') for token in row.strip().lower().
                replace('\'',' ').replace('"',' ').replace(',', ' ').replace('.', ' ').replace(';', '').
                replace('<', '').replace('>', ' ').replace('!', ' ').replace('#', ' ').replace('&', ' ').
                replace('%', ' ').replace('*', ' ').replace(':', ' ').replace('\\', ' ').replace('?', ' ').
                replace('/', ' ').replace('[', ' ').replace(']', ' ').replace('-', ' ').replace('_', ' ').
                replace('=', ' ').replace('+', ' ').replace('|', ' ').
                split() if len(token.strip(skipCharacters))!=0]
        doc_file.close()
        return token_list

#
# stream = DocStream()
# stream.parseDocs()
# for filename in stream.token_stream:
#     print(filename,stream.token_stream.get(filename))
