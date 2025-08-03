import sys; args = sys.argv[1:] # get the arguments

myRegexLst = [""] * 10
myRegexLst[0] = r"/^(?!.*010)[01]*$/"
myRegexLst[1] = r"/^(?!.*101)(?!.*010)[01]*$/"
myRegexLst[2] = r"/^((\d)[01]*\2|0|1)$/"
myRegexLst[3] = r"/\b(?!\w*(\w)\w*\1\b)\w+\b/i"
myRegexLst[4] = r"/((\w)*(\w*\2){3}|\w*(?=(\w)\w*\4)\w+(?!\4)(\w)\w*\5)\w*/i"
myRegexLst[5] = r"/\b(?=(\w)*(\w*\1){2})((\w)(?!\w*\4)|\1)+\b/i"
myRegexLst[6] = r"/\b(?!(\w*([aeiou])\w*\2))(\w*[aeiou]){5}\w*/i"
myRegexLst[7]= r"/^(?=1*0(01*0|1)*$)(10*1|0)*$/"
myRegexLst[8] = r"/^(0|(1(01*0)*10*)+)$/"
myRegexLst[9] = r"/^(?!(1(01*0)*1|0)+$)[10]+$/"

print(myRegexLst[int(args[0])-60])
'''
Q60: Match all binary strings that do not contain the forbidden substring 010.  (14)
Q61: Match all binary strings containing neither 101 nor 010 as substrings.  (20)
Q62: Match on all non-empty binary strings with the same number of 01 substrings as 10 substrings.  (14)
Q63: Match all words whose final letter is not to be found elsewhere in the word.  (21)  
Q64: Match all words that have at least two pairs of doubled letters (two pairs of distinct letters or four of the same letter are both OK).  (43)
Q65: Match all words that have no duplicate letter, except for one, which occurs at least 3 times.  (42)
Q66: Match all words where each of the five vowels occurs exactly once.  (39)
Q67: Match all binary strings that have an odd number of 0s and an even number of 1s.  (22)
Q68: Match all binary integer strings that are divisible by 3.  (19)
Q69: Match all binary integer strings that are not divisible by 3.  (19)
'''
#Saatvik Kesarwani, pd 1, 2026