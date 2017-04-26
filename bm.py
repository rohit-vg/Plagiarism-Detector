# Boyer Moore String Search implementation in Python

import time
# Generate the Bad Character Skip List
def generateBadCharTable(pattern):
    bcdList = {}
    for i in range(0, len(pattern)-1):
        bcdList[pattern[i]] = len(pattern)-i-1
    return bcdList

# Generate the Good Suffix Skip List
def findSuffixPos(badchar, suffix, pattern):
    for offset in range(1, len(pattern)+1)[::-1]:
        flag = True
        for suffix_index in range(0, len(suffix)):
            term_index = offset-len(suffix)-1+suffix_index
            if term_index < 0 or suffix[suffix_index] == pattern[term_index]:
                pass
            else:
                flag = False
        term_index = offset-len(suffix)-1
        if flag and (term_index <= 0 or full_term[term_index-1] != badchar):
            return len(pattern)-offset+1

def generateSuffixTable(pattern):
    suffList = {}
    buffer = ""
    for i in range(0, len(pattern)):
        suffList[len(buffer)] = findSuffixPos(pattern[len(pattern)-1-i], buffer, pattern)
        buffer = key[len(pattern)-1-i] + buffer
    return suffList
    
# Actual Search Algorithm
def BMSearch(text, pattern,filename,counter,s1):

    badChar = generateBadCharTable(pattern)
    
    i = 0
    while i < len(text)-len(pattern)+1:
        j = len(pattern)
        while j > 0 and pattern[j-1] == text[i+j-1]:
            j -= 1
        if j > 0:
            badCharShift = badChar.get(text[i+j-1], len(pattern))
            i += badCharShift
        else:
            s1[counter]=1
            return (pattern,counter,s1)
    return (None,counter,s1)
