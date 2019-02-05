import nltk
import collections
import glob
import string
import os
import json


def main():
    
    filelist = glob.glob("input/*.txt")

    illegalchars = str.maketrans('', '', string.punctuation + string.digits)
    docnamelist = []
    index = 0
    worddict = {}
    worddict["count"] = len(filelist)
    worddict["word"] = {}
    for fi in filelist:
        docnamelist.append(fi[6:])
        with open(fi) as f:
            dat = f.read()
        dat = dat.lower()
        dat = dat.translate(illegalchars)
        
        tokens = nltk.word_tokenize(dat)
        
        porterstemmer = nltk.PorterStemmer()
        for i in range(len(tokens)):
            tokens[i] = porterstemmer.stem(tokens[i])
        

        for token in tokens:
            if token in worddict["word"] :
                if docnamelist[index] in worddict["word"][token]["appears"] :
                    worddict["word"][token]["appears"][docnamelist[index]] += 1
                else:
                    worddict["word"][token]["numdocs"] += 1
                    worddict["word"][token]["appears"][docnamelist[index]] = 1
            else:
                worddict["word"][token] = {}
                worddict["word"][token]["numdocs"] = 1
                worddict["word"][token]["appears"] = {}
                worddict["word"][token]["appears"][docnamelist[index]] = 1

        index = index + 1
    jsonout = open("inverted-index.json", 'w')
    json.dump(worddict, jsonout)
    jsonout.close()
    

if __name__ == "__main__":
    main()