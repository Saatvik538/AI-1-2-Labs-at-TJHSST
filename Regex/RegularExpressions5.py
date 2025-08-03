import sys; args = sys.argv[1:] #get the arguments

myRegexLst = [""] * 10
myRegexLst[0] = r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)[a-z]*$/m" #finished
myRegexLst[1] = r"/^(?!(.*[iouae]){6})([a-z]*[iouae]){5}\w*$/m" #shorter version 
myRegexLst[2] = r"/^(?=\w*[^iouae\n]w[^iouae]{2})[a-z]*$/m" #shorter version
myRegexLst[3] = r"/^(?=([a-z])(\w)(\w))\w*\3\2\1$|^a{1,2}$/m" #finished
myRegexLst[4] = r"/^[^tA-Zb\n']*(tb|bt)[^tA-Zb\n']*$/m" #finished
myRegexLst[5] = r"/^(?=.*(.)\1)[a-z]*$/m" #finished
myRegexLst[6] = r"/^(?=.*(\w)(\w*\1){5})\w*$/m" #shorter version
myRegexLst[7] = r"/^\w*((\w)\2){3}\w*$/m" #finished
myRegexLst[8] = r"/^(?=(.*[^iouae\n]){13})\w*$/m" #finished
myRegexLst[9] = r"/^(([a-z])(?!.*\2.*\2))*$/m" #finished


#FINAL VERSION (need to check on grader)

print(myRegexLst[int(args[0])-70])
'''
70: ... where each vowel occurs at least once
71: ... containing exactly 5 vowels
72: ... with w acting as vowel
73: ... where if all but the first 3 and last 3 letters are removed, a palindrome results
74: ... where there is exactly one b and one t, and they are adjacent to each other
75: ... with the longest contiguous block of one letter
76: ... with the greatest number of a repeated letter
77: ... with the greatest number of adjacent pairs of identical letters
78: ... with the greatest number of consonants
79: ... where no letter is repeated more than once
'''
#Saatvik Kesarwani, pd 1, 2026