import Query
from TokenLize import DocStream
import Dict_Build

file_test = r'data.txt'

# stream = DocStream()
# stream.parseDocs()

# dict_post = Dict_Build.Dict_Postlist()
# dict_post.spimi_build(stream)

while(1):
    input_line = raw_input("input key words:")
    Query.query(input_line)
