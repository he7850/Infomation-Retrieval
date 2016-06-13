from TokenLize import DocStream
from Dict_Build import Dict_Postlist
from Linklist import LinkList

file_test = r'data.txt'

stream = DocStream()
stream.parseDocs()

dict_post = Dict_Postlist()
dict_post.spimi_build(stream)
while(1):
    keyword = raw_input("input key word:")
    dict_post.query(keyword)
