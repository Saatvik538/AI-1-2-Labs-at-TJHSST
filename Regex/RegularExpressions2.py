import sys; args = sys.argv[1:] # get the arguments

myRegexLst = [""] * 10
myRegexLst[0] = r"/^[xo.]{64}$/i"
myRegexLst[1] = r"/^[xo]*[.][xo]*$/i"
myRegexLst[2] = r"/^(x+o*)?[.]|[.](o*x+)?$/i"
myRegexLst[3] = r"/^(..)*.$/s"
myRegexLst[4] = r"/^(0|1[01])([01]{2})*$/"
myRegexLst[5] = r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i"
myRegexLst[6] = r"/^(1?0+|1+$)*$/"
myRegexLst[7]= r"/^\b[bc]*a?[bc]*\b$/"
myRegexLst[8] = r"/^\b([bc]|(a[bc]*){2})*\b$/"
myRegexLst[9] = r"/^(2[02]*|(1[02]*){2})+$/"

print(myRegexLst[int(args[0])-40])
'''
Q40: Write a regular expression that will match on an Othello board represented as a string.
Q41: Given a string of length 8, determine whether it could represent an Othello edge with exactly one hole.
Q42: Given an Othello edge as a string, determine whether there is a hole such that if X plays to the hole (assuming it could), it will be connected to one of the corners through X tokens.  Specifically, this means that one of the ends must be a hole, or starting from an end there is a sequence of at least one x followed immediately by a sequence (possibly empty) of o, immediately followed by a hole.
Q43: Match on all strings of odd length.
Q44: Match on all odd length binary strings starting with 0, and on even length binary strings starting with 1.
Q45: Match all words having two adjacent vowels that differ.
Q46: Match on all binary strings which DONT contain the substring 110.
Q47: Match on all non-empty strings over the alphabet {a, b, c} that contain at most one a.
Q48: Match on all non-empty strings over the alphabet {a, b, c} that contain an even number of a's.
Q49: Match on all positive, even, base 3 integer strings.
'''
#Saatvik Kesarwani, pd 1, 2026