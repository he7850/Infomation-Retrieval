"""vsm.py implements a toy search engine to illustrate the vector
space model for documents.
It asks you to enter a search query, and then returns all documents
matching the query, in decreasing order of cosine similarity,
according to the vector space model."""

from collections import defaultdict
import math
import sys
import numpy
import os
import pickle

# We use a corpus of four documents.  Each document has an id, and
# these are the keys in the following dict.  The values are the
# corresponding filenames.
info = "data"
listfile=os.listdir(info)
listfile.remove(".DS_Store")
print len(listfile)
document_filenames = {}
for i in range(len(listfile)):
    document_filenames[i] = listfile[i]
print document_filenames[1]
# document_filenames = {0 : "1.txt",
#                       1 : "2.txt",
#                       2 : "3.txt",
#                       3 : "4.txt"}

# The size of the corpus
N = len(document_filenames) - 4
# ....................................................# dictionary: a set to contain all terms (i.e., words) in the document
# # corpus.
dictionary = set()

# postings: a defaultdict whose keys are terms, and whose
# corresponding values are the so-called "postings list" for that
# term, i.e., the list of documents the term appears in.
#
# The way we implement the postings list is actually not as a Python
# list.  Rather, it's as a dict whose keys are the document ids of
# documents that the term appears in, with corresponding values equal
# to the frequency with which the term occurs in the document.
#
# As a result, postings[term] is the postings list for term, and
# postings[term][id] is the frequency with which term appears in
# document id.
postings = defaultdict(dict)

# document_frequency: a defaultdict whose keys are terms, with
# corresponding values equal to the number of documents which contain
# the key, i.e., the document frequency.
document_frequency = defaultdict(int)

# length: a defaultdict whose keys are document ids, with values equal
# to the Euclidean length of the corresponding document vector.
length = defaultdict(float)

# The list of characters (mostly, punctuation) we want to strip out of
# terms in the document.
characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"

def main():
    # initialize_terms_and_postings()
    # initialize_lengths()
    # print inverse_document_frequency("dog")
    global dictionary, document_frequency, postings, length
    pk_file = open('word.pkl', 'rb')
    dictionary = pickle.load(pk_file)

    pk_file1 = open('dict.pkl', 'rb')
    postings = pickle.load(pk_file1)
    # initialize_document_frequencies()
    pk_file2 = open('doc_freq.pkl', 'rb')
    document_frequency = pickle.load(pk_file2)
    print document_frequency["week"]
    pk_file3 = open('length.pkl', 'rb')
    length = pickle.load(pk_file3)
    print length
    while True:
        do_search()


def initialize_terms_and_postings():
    """Reads in each document in document_filenames, splits it into a
    list of terms (i.e., tokenizes it), adds new terms to the global
    dictionary, and adds the document to the posting list for each
    term, with value equal to the frequency of the term in the
    document."""
    global dictionary, postings
    for id in document_filenames:
        f = open(document_filenames[id],'r')
        document = f.read()
        f.close()
        terms = tokenize(document)
        unique_terms = set(terms)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
            postings[term][id] = terms.count(term) # the value is the
                                                   # frequency of the
                                                   # term in the
                                                   # document
    # print postings["and"]
    # f2 = file("dict.txt", "w")
    # s = repr(postings)
    # f2.writelines(s)
    # f2.close()
    output = open("word.pkl","wb")
    pickle.dump(dictionary, output)
    output.close()
    print "pickle sucess"
    output1 = open("dict.pkl","wb")
    pickle.dump(postings, output1)
    output1.close()
    print "pickle1 sucess"


def tokenize(document):
    """Returns a list whose elements are the separate terms in
    document.  Something of a hack, but for the simple documents we're
    using, it's okay.  Note that we case-fold when we tokenize, i.e.,
    we lowercase everything."""
    terms = document.lower().split()
    return [term.strip(characters) for term in terms]

def initialize_document_frequencies():
    """For each term in the dictionary, count the number of documents
    it appears in, and store the value in document_frequncy[term]."""
    global document_frequency
    for term in dictionary:
        document_frequency[term] = len(postings[term])
    # f3 = file("dict_frequency.txt", "w")
    # s = repr(document_frequency)
    # f3.writelines(s)
    # f3.close()
    print document_frequency
    output2 = open("doc_freq.pkl","wb")
    pickle.dump(document_frequency, output2)
    output2.close()
    print "pickle2 sucess"

def initialize_lengths():
    """Computes the length for each document."""
    global length
    for id in document_filenames:
        l = 0
        for term in dictionary:
            l += imp(term,id)**2
        length[id] = math.sqrt(l)
    output3 = open("length.pkl","wb")
    pickle.dump(length, output3)
    output3.close()
    print "pickle3 sucess"

def imp(term,id):
    """Returns the importance of term in document id.  If the term
    isn't in the document, then return 0."""
    if id in postings[term]:
        return postings[term][id]*inverse_document_frequency(term)
    else:
        return 0.0

def inverse_document_frequency(term):
    """Returns the inverse document frequency of term.  Note that if
    term isn't in the dictionary then it returns 0, by convention."""
    if term in dictionary:
        return math.log(N * 1.0/document_frequency[term],10)
    else:
        return 0.0

def do_search(words):
    global dictionary, document_frequency, postings, length
    pk_file = open('word.pkl', 'rb')
    dictionary = pickle.load(pk_file)

    pk_file1 = open('dict.pkl', 'rb')
    postings = pickle.load(pk_file1)
    # initialize_document_frequencies()
    pk_file2 = open('doc_freq.pkl', 'rb')
    document_frequency = pickle.load(pk_file2)
    print document_frequency["week"]
    pk_file3 = open('length.pkl', 'rb')
    length = pickle.load(pk_file3)
    
    """Asks the user what they would like to search for, and returns a
    list of relevant documents, in decreasing order of cosine
    similarity."""
    #query = tokenize(raw_input("Search query >> "))
    query = words
    if query == []:
        sys.exit()
    # find document ids containing all query terms.  Works by
    # intersecting the posting lists for all query terms.
    # relevant_document_ids = intersection(
    #         [set(postings[term].keys()) for term in query])
    # print relevant_document_ids
    # if not relevant_document_ids:
    #     print "No documents matched all query terms."
    # else:
    set_files = []
    for i in range(N):
        set_files.append(i)
    print set_files[-1]
    set_files = set(set_files)
    scores = sorted([(id,similarity(query,id))
                     for id in set_files],
                    key=lambda x: x[1],
                    reverse=False)
    #print "Score: filename"
    return  scores
    #for (id,score) in scores:
     #   print str(score)+": "+document_filenames[id]

def intersection(sets):
    """Returns the intersection of all sets in the list sets. Requires
    that the list sets contains at least one element, otherwise it
    raises an error."""
    return reduce(set.intersection, [s for s in sets])

def similarity(query,id):
    """Returns the cosine similarity between query and document id.
    Note that we don't bother dividing by the length of the query
    vector, since this doesn't make any difference to the ordering of
    search results."""
    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*imp(term,id)
    print id, similarity
    print document_filenames[id]
    print length[id]
    similarity = similarity / length[id]
    return similarity

if __name__ == "__main__":
    main()