import csv
import re
import time
import os

# Boyer Moore String Search implementation in Python
def read_text(filepath):
    with open(filepath,'rb') as flobj:
        content = flobj.read()
        return content

# Generate the Bad Character Skip List
def generateBadCharShift(term):
    skipList = {}
    for i in range(0, len(term)-1):
        skipList[term[i]] = len(term)-i-1
    return skipList


# Generate the Good Suffix Skip List
def findSuffixPosition(badchar, suffix, full_term):
    for offset in range(1, len(full_term)+1)[::-1]:
        flag = True
        for suffix_index in range(0, len(suffix)):
            term_index = offset-len(suffix)-1+suffix_index
            if term_index < 0 or suffix[suffix_index] == full_term[term_index]:
                pass
            else:
                flag = False
        term_index = offset-len(suffix)-1
        if flag and (term_index <= 0 or full_term[term_index-1] != badchar):
            return len(full_term)-offset+1


# def generateSuffixShift(key):
#     skipList = {}
#     buffer = ""
#     for i in range(0, len(key)):
#         skipList[len(buffer)] = findSuffixPosition(key[len(key)-1-i], buffer, key)
#         buffer = key[len(key)-1-i] + buffer
#     return skipList


# Actual Search Algorithm
def BMSearch(text, pattern):
    for pline in pattern:
        if len(pline) == 0:
            continue
        #goodSuffix = generateSuffixShift(pline)
        badChar = generateBadCharShift(pline)
        tpos = 0
        while tpos < len(text)-len(pline)+1:
            ppos = len(pline)
            while ppos > 0 and pline[ppos-1] == text[tpos+ppos-1]:
                ppos -= 1
            if ppos > 0:
                badCharShift = badChar.get(text[tpos+ppos-1], len(pline))
                #goodSuffixShift = goodSuffix[len(pline)-ppos]
                #if badCharShift > goodSuffixShift:
                tpos += badCharShift
                #else:
                #    tpos += goodSuffixShift
            else:
                print pline
                break



def lcss(pat, txt, filename,counter,s1):
    m = len(pat)
    n = len(txt)
    # making matrix of m+1 * n+1 and with 0 in all cells
    matrix = [[0]*(n+1) for i in range(m+1)]
    # matching each character of s1 with s2 and incrementing lower diagonal cell by 1 on a match
    # or the max of right and lower cell on a mismatch
    for i in range(m):
        for j in range(n):
            if pat[i] == txt[j]:
                matrix[i+1][j+1] = matrix[i][j] + 1
            else:
                matrix[i+1][j+1] = max(matrix[i+1][j], matrix[i][j+1])
    match = ""
    longest = ""
    #starting from the last cell, see where the cells got incremented(take element from every diagonal move)
    #also keeping the longest
    while m and n:
        if matrix[m][n] == matrix[m-1][n]:
            m -= 1
            match = ""
        elif matrix[m][n] == matrix[m][n-1]:
            n -= 1
            match = ""
        elif pat[m-1] == txt[n-1]:
            match = s1[m-1] + match
            m -= 1
            n -= 1
        if len(match)>len(longest):
            longest = match
            
        

    return longest

delimiters = ".", "?"
regexPattern = '|'.join(map(re.escape, delimiters))
input_file = open("input.txt", 'r').read()
input_file = input_file.replace("\n", "")
input_file = re.split(regexPattern, input_file)
file_A = open("A.txt", 'r').read()
file_A = file_A.replace("\n", "")
file_A = re.split(regexPattern, file_A)
file_B = open("B.txt", 'r').read()
file_B = file_B.replace("\n", "")
file_B = re.split(regexPattern, file_B)

input_file = input_file[0]
for row in file_A:
    if row.startswith(" "): row = row[1:]
    start_time = time.time()
    match = lcss(input_file, row)
    if match and len(match) >= 0.6*len(input_file):
        print '---------file_A---------'
        print match
print("--- %s seconds ---" % (time.time() - start_time))


block = read_text(os.getcwd() + '/A.txt')
block = block.replace('\n','')
block = block.replace('\r','')
pattern = read_text(os.getcwd() + '/input.txt')
pattern = pattern.replace('\n','')
pattern = pattern.replace('\r','')
patdata = pattern.split('.')
patdata = patdata[:1]
diff1 = time.time()
BMSearch(block, patdata)
diff2 = time.time()
diffvalue = diff2 - diff1
print("--- Boyer-Moore Time = %s seconds ---" % diffvalue)