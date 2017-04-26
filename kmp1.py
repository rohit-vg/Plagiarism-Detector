import glob
import os


# Python program for KMP Algorithm
def KMPSearch(pat, txt, filename,counter,s1):
    M = len(pat)
    N = len(txt)
 
    # create lps[] that will hold the longest prefix suffix 
    # values for pattern
    lps = [0]*M
    j = 0 # index for pat[]
 
    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)
 
    i = 0 # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i+=1
            j+=1
 
        if j==M:
            #print "Found pattern at index " + str(i-j)
            #global s1
            #global counter
            s1[counter]=1
            #print "Plagarized from file : "+filename
            #print "Plagarized sentence : "+pat+"\n\n"
            j = lps[j-1]
            return (pat,counter,s1)
 
        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i+=1
    return (None,counter,s1)
 
def computeLPSArray(pat, M, lps):
    len = 0 # length of the previous longest prefix suffix
 
    lps[0] # lps[0] is always 0
    i = 1
 
    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i]==pat[len]:
            len+=1
            lps[i] = len
            i+=1
        else:
            if len!=0:
                # This is tricky. Consier the example AAACAAAA
                # and i = 7
                len = lps[len-1]
 
                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i+=1
 

def comparefile(inputfile,targetfile,sentences,s1):
    #global s1
    input = open(inputfile, "rb")
    test = open(targetfile, "rb")
    filecontent = input.read()
    searchcontent = test.read()
    #global sentences
    
    
    

    
    

    
    print s1
    print targetfile
        
    #global counter
    counter = 0
    plagarized_sentences=[]
    for sentence in sentences:
        if sentence!="":   
            #print str(counter)+" ) "+sentence+"\n"
            
            plagarized_sentence,counter,s1 = KMPSearch(sentence, searchcontent,os.path.basename(targetfile),counter,s1)
            counter=counter+1
            if(str(plagarized_sentence)!="None"):
                plagarized_sentences.append(plagarized_sentence)
            #print "----------------------------------------------------------------------"
    print "\n\n\nPlagarized from file : "+os.path.basename(targetfile) +"\n"     
    print plagarized_sentences
    return (sentences,s1)

    
def reset_s1_and_counter(sentences,s1,counter):
    s1 = []
    for i in range(len(sentences)): # This is just to tell you how to create a list.
        s1.append(0)
    counter = 0
    return (sentences,s1,counter)
    
    
inputfile="input.txt"
relativefolder="target"
allfiles= glob.glob(relativefolder+"/*.txt")

#print os.path.basename(a[0])
input = open(inputfile, "rb")

sentences = []
sentences = filter(None,input.read().split("."))

sentences,s1,counter = reset_s1_and_counter(sentences,s1=[],counter=0)

print s1
for filepath in allfiles:
    
    #outputfile = relativefolder+"/A.txt"
   sentences,s1 =  comparefile(inputfile,filepath,sentences,s1)
print s1
sum=0
for s in s1:
    sum=sum+s
prob = float(sum)*100/len(s1)
#print sum
#print len(s1)
print str(prob) +" % Plagarized"

