import time

def search(pattern,string, filename,counter,s1):
    for m in range(len(string)):
        for n in range(len(pattern)):
            if string[m+n] != pattern[n]:
                break
            elif n == len(pattern) - 1:
                s1[counter]=1
                return (pattern,counter,s1)
    return (None,counter,s1)
    
    
def naive_algo(pattern,string, filename,counter,s1):
                n = len(pattern)
                m = len(string)
                if m > n:
                        for s in range(0,(int(m)-int(n))+1):
                                #print string[s:s+n]+"\n"
                                #time.sleep(0.5)
                                if string[s:s+n] == pattern:
                                        #print string[s:s+n]+"\n"
                                        #print pattern+"\n"
                                        #print "---"+"\n"
                                        s1[counter]=1
                                        return (pattern,counter,s1)
                                else:
                                        #print string[s:s+m] + "\n"
                                        #print pattern+"\n"
                                        #print "-a-"+"\n"
                                        pass
                        
                elif n == m:
                        if pattern == string:
                                s1[counter]=1
                                return (pattern,counter,s1)
                else:
                        
                        return (None,counter,s1)
                return (None,counter,s1)