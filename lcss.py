# A Naive recursive Python implementation of LCS problem
 
def lcs(X , Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)
 
    # making matrix of m+1 * n+1 and with 0 in all cells
    L = [[None]*(n+1) for i in xrange(m+1)]
 
    # matching each character of s1 with s2 and incrementing lower diagonal cell by 1 on a match
    # or the max of right and lower cell on a mismatch
    result = 0;
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
                result = max(result, L[i][j])
            else:
                L[i][j] = 0
    return result



def lcss(pattern,string, filename,counter,s1):
    
    lcss_length = lcs(pattern , string)
    
    if lcss_length==len(pattern):
        s1[counter]=1
        return (pattern,counter,s1)
    else:
        return (None,counter,s1)
    
    