import sys; args = sys.argv[1:] # get the arguments

myRegexLst = [""] * 10
myRegexLst[0] = r"/\w*(\w)\w*\1\w*/i"
myRegexLst[1] = r"/\w*(\w)(\w*\1){3}\w*/i"
myRegexLst[2] = r"/^(0|1)([01]*\1)*$/"
myRegexLst[3] = r"/\b(?=\w*cat)\w{6}\b/i"
myRegexLst[4] = r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i"
myRegexLst[5] = r"/\b(?!\w*cat)\w{6}\b/i"
myRegexLst[6] = r"/\b((\w)(?!\w*\2))+\b/i"
myRegexLst[7]= r"/^((?!10011)[01])*$/"
myRegexLst[8] = r"/\w*([aeiou])(?!\1)[aeiou]\w*/i"
myRegexLst[9] = r"/^((?!101|111)[01])*$/"

print(myRegexLst[int(args[0])-50])
'''
Q50: Match all words where some letter appears twice in the same word.
Q51: Match all words where some letter appears four times in the same word.
Q52: Match all non-empty binary strings with the same number of 01 substrings as 10 substrings.
Q53: Match all six letter words containing the substring cat.
Q54: Match all 5 to 9 letter words containing both the substrings bri and ing.
Q55: Match all six letter words not containing the substring cat.
Q56: Match all words with no repeated characters.
Q57: Match all binary strings not containing the forbidden substring 10011.
Q58: Match all words having two different adjacent vowels.
Q59: Match all binary strings containing neither 101 nor 111 as substrings.
'''
#Saatvik Kesarwani, pd 1, 2026