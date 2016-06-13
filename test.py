from TokenLize import DocStream
from Dict_Build import Dict_Postlist
from Linklist import LinkList

file_test = r'data.txt'

stream = DocStream()
test_dic = stream.getTokenStream(file_test)
for i in test_dic:
    print(i,':',test_dic.get(i))

dict_post = Dict_Postlist()
dict_post.spimi_build(test_dic)
print(dict_post.token_dict.get('of').post_point.output())
