# -*- coding:utf-8 -*-

alphabet = "abcdefghijklmnopqrstuvwxyz"

class Dictionary(object):
    def __init__(self):
        self.diction_file = open('google-10000-english-usa.txt')
        self.diction = self.diction_file.read()
        self.all_words = self.diction.strip().split()

    def __del__(self):
        self.diction_file.close()

    def isCorrectWord(self,word):
        return word in self.all_words

    def getCorrectWords(self, word):
        result = []
        for candidate in getProbableWord(word):
            if candidate in self.all_words:
                result.append(candidate)
        return result

    def getCorrectWord(self,word):
        if word in self.all_words:
            return word
        for candidate in getProbableWord(word):
            if candidate in self.all_words:
                return candidate
        return word


def getProbableWord(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return list(transposes + deletes + replaces + inserts)


# diction = Dictionary()
# word = "wednsday"
# if diction.isCorrectWord(word):
#     print word
# else:
#     print diction.getCorrectWords(word)