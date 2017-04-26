import os
import csv
from nvd3 import discreteBarChart
import glob
import bm as moore
import naive as naive
import lcss as lcss
import time
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():



    chart_algo = []
    loop10Time = []

    def getSize(filename):
        st = os.stat(filename)
        return st.st_size

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


    def comparefile(inputfile,targetfile,sentences,s1,algo):
        global filecontent
        global searchcontent
        input = open(inputfile, "rb")
        test = open(targetfile, "rb")
        filecontent = input.read()
        searchcontent = test.read()
        #global sentences



        #print s1
        print "FILE: "+ targetfile+" SIZE: "+str(getSize(targetfile))

        #global counter
        counter = 0
        plagarized_sentences=[]
        all_time = []
        for run10 in range(0,10):
            counter = 0
            before= time.time()
            for sentence in sentences:
                if sentence!="":
                    #print str(counter)+" ) "+sentence+"\n"
                    if algo=="NAIVE":
                        plagarized_sentence,counter,s1 = naive.search(sentence,searchcontent,os.path.basename(targetfile),counter,s1)
                    if algo=="KMP":
                        plagarized_sentence,counter,s1 = KMPSearch(sentence, searchcontent,os.path.basename(targetfile),counter,s1)
                    if algo=="LCSS":
                        plagarized_sentence,counter,s1 = lcss.lcss(sentence, searchcontent,os.path.basename(targetfile),counter,s1)
                    if algo=="BM":
                        plagarized_sentence,counter,s1 = moore.BMSearch(searchcontent,sentence,os.path.basename(targetfile),counter,s1)
                    counter=counter+1
                    if(str(plagarized_sentence)!="None"):
                        plagarized_sentences.append(plagarized_sentence)
            after = time.time()
            timetaken = after- before
            all_time.append(timetaken)
            print timetaken
                    #print "----------------------------------------------------------------------"
        #print "\n\n\nPlagarized from file : "+os.path.basename(targetfile) +"\n"
        #print plagarized_sentences
        avgtime = sum(all_time)/ len(all_time)
        all_time = []
        loop10Time.append(avgtime)
        print "Average Time Taken : "+str(avgtime)
        print "---------------------------------------------------------------------"
        return (sentences,s1)


    def reset_s1_and_counter(sentences,s1,counter):
        s1 = []
        for i in range(len(sentences)): # This is just to tell you how to create a list.
            s1.append(0)
        counter = 0
        return (sentences,s1,counter)

    def compareallfiles(inputfile,sentences,s1,algo):
        global filecontent
        global searchcontent
        print "---------------------------------------------------------------------"
        print "Algorithm = "+algo+"\n\n"
        sentences,s1,counter = reset_s1_and_counter(sentences,s1=[],counter=0)
        for filepath in allfiles:
            #outputfile = relativefolder+"/A.txt"

            sentences,s1 =  comparefile(inputfile,filepath,sentences,s1,algo)
        #print s1
        sum=0
        for s in s1:
            sum=sum+s
        prob = float(sum)*100/len(s1)
        #print sum
        #print len(s1)
        print str(prob) +" % Plagarized"
        return (sentences,s1)


    inputfile="input.txt"
    relativefolder="target"
    allfiles= glob.glob(relativefolder+"/*.txt")

    #print os.path.basename(a[0])
    input = open(inputfile, "rb")

    sentences = []
    sentences = filter(None,input.read().split("."))

    sentences,s1,counter = reset_s1_and_counter(sentences,s1=[],counter=0)

    algo="NAIVE"
    sentences,s1 = compareallfiles(inputfile,sentences,s1,algo)

    algo="KMP"
    sentences,s1 = compareallfiles(inputfile,sentences,s1,algo)

    algo="LCSS"
    sentences,s1 = compareallfiles(inputfile,sentences,s1,algo)

    algo="BM"
    sentences,s1= compareallfiles(inputfile,sentences,s1,algo)





    chart_algo = ["Naive String : " + str(loop10Time[0]), "KMP : " + str(loop10Time[1]), "LCSS : " + str(loop10Time[2]), "BM : " + str(loop10Time[3])]

    chart = discreteBarChart(name='multiBarChart', height=800, width=1800, margin_bottom=30,margin_top=40, margin_left=260, margin_right=300)
    chart.add_serie(y=loop10Time, x=chart_algo)
    chart.buildhtml()
    return chart.htmlcontent + "Pattern Size: "+ str(len(filecontent)) + "<br>File Size: "+ str(len(searchcontent))

port = os.getenv('VCAP_APP_PORT', '5010')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=True)