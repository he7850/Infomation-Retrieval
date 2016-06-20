import Query
from Tokenizer import Tokenizer
from InvertIndex_Builder import InvertIndex_Builder

file_test = r'data.txt'

# tokenLizer = Tokenizer()
# tokenLizer.countDocs()
# tokenLizer.parseDocs()
#
# postList_Builder = InvertIndex_Builder()
# postList_Builder.spimi_build(tokenLizer.doc_word_stream)

while(1):
    input_line = raw_input("input key words:")
    Query.query(input_line)
