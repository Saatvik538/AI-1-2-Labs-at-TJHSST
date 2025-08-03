import sys; args = sys.argv[1:] # get the arguments

myRegexLst = [""] * 10
myRegexLst[0] = r"/^0$|^10[01]$/"
myRegexLst[1] = r"/^[01]*$/"
myRegexLst[2] = r"/0$/"
myRegexLst[3] = r"/\w*[aeiou]\w*[aeiou]\w*/i"
myRegexLst[4] = r"/^1[10]*0$|^0$/"
myRegexLst[5] = r"/^[01]*110[01]*$/"
myRegexLst[6] = r"/^.{2,4}$/s"
myRegexLst[7]= r"/^\d{3} *-? *\d\d *-? *\d{4}$/"
myRegexLst[8] = r"/^.*?d\w*/im"
myRegexLst[9] = r"/^[01]?$|^0[01]*0$|^1[01]*1$/"

print(myRegexLst[int(args[0])-30])

#Saatvik Kesarwani, pd 1, 2026



