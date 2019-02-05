import json
import nltk
import string
import collections
import math

def main():
    jsonin = open("inverted-index.json", "r")
    worddict = {}
    worddict = json.load(jsonin)
    jsonin.close()

    keyworddict = {}



    keywordstotal = open("keywords.txt").readlines()
    illegalchars = str.maketrans('', '', string.punctuation + string.digits)
    for keyline in keywordstotal:
        keyline = keyline.rstrip()
        keyword = keyline.split(" ")
        keyworddict[keyline] = {}
        for subkey in keyword:
            

            word = subkey.lower()
            word = word.translate(illegalchars)

            tokens = nltk.word_tokenize(word)
        
            porterstemmer = nltk.PorterStemmer()
            for i in range(len(tokens)):
                tokens[i] = porterstemmer.stem(tokens[i])
            
            numoccurances = worddict["word"][tokens[0]]["numdocs"]
            totdocs = worddict["count"]
            docs = worddict["word"][tokens[0]]["appears"].keys()
            for doc in docs:
                if doc not in keyworddict[keyline]:
                    keyworddict[keyline][doc] = {}
                if subkey not in keyworddict[keyline][doc]:
                    keyworddict[keyline][doc][subkey] = 0
                freq = worddict["word"][tokens[0]]["appears"][doc]
                weight = (1 + math.log2(freq)) * math.log2(totdocs / numoccurances)

                keyworddict[keyline][doc][subkey] = weight
            
            
    for keyline in keyworddict:
        keyline = keyline.rstrip()
        for doc in keyworddict[keyline]:
            keyworddict[keyline][doc]["--weight--"] = 0
            for key in keyline.split():
                if key in keyworddict[keyline][doc]:
                    keyworddict[keyline][doc]["--weight--"] += keyworddict[keyline][doc][key]
                else:
                    keyworddict[keyline][doc][key] = 0
                
            
    
    for keyline in keyworddict:
        keyline = keyline.rstrip()
        listr = []
        listr = sorted(keyworddict[keyline].keys(), key=lambda x: (-keyworddict[keyline][x]["--weight--"], x))
        
        print("------------------------------------------------------------")
        print("keywords : " + keyline + "\n")
        keywords = keyline.split(" ")

        index = 1
        while len(listr) > 0:
            temp = listr.pop(0)
            ##print('%.6f'%keyworddict[keyline][temp]["--weight--"])
            print("[" + "{0}".format(index) + "] file=" + temp + "\tscore="  + "{0:.6f}".format(keyworddict[keyline][temp]["--weight--"]))
            for word in keywords:
                print("\tweight("+word+")=" + "{0:.6f}".format(keyworddict[keyline][temp][word]))
            index += 1
            print()            

        
        

        
    
                
                


            
            
            

if __name__ == "__main__":
    main()
