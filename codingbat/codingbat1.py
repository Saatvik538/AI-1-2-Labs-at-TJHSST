#warmup 1
def sleep_in(weekday, vacation):
    return not weekday or vacation

def monkey_trouble(a_smile, b_smile):
    return a_smile==b_smile

def sum_double(a, b):
    return (a + b) * (2 if a == b else 1)

def diff21(n):
    return abs(21-n) *(2 if n>21 else 1)

def parrot_trouble(talking, hour):
    return talking and (hour<7 or hour>20)

def makes10(a, b):
    return a+b == 10 or (a==10 or b == 10)

def near_hundred(n):
    return abs(100 - n) <= 10 or abs(200 - n) <= 10

def pos_neg(a, b, negative):
    return negative and a<0 and b<0 or not negative and(a<=0) != (b<=0) and a!=0 and b!=0

#string-1
def hello_name(name):
    return 'Hello ' + name + '!'

def make_abba(a, b):
    return a+b+b+a

def make_tags(tag, word):
    return '<'+tag+'>'+word+'</'+tag+'>'

def make_out_word(out, word):
    return out[:len(out)//2] + word + out[len(out)//2:]

def extra_end(str):
    return str[-2:] * 3

def first_two(str):
    return str if len(str) <= 2 else str[:2]

def first_half(str):
    return str[:len(str)//2]

def without_end(str):
    return str[1:-1]

#List-1
def first_last6(nums):
    return str(6) in (str(nums[0]), str(nums[-1]))

def same_first_last(nums):
    return len(nums)>0 and str(nums[0]) == str(nums[-1])

def make_pi(n):
    return [int(d) for d in str(3141592653589)[:n]]

def common_end(a, b):
    return str(a[0]) == str(b[0]) or str(a[-1]) == str(b[-1])

def sum3(nums):
    return sum(nums)

def rotate_left3(nums):
    return nums if len(nums) <= 1 else nums[1:] + [nums[0]]

def reverse3(nums):
    return nums[::-1]

def max_end3(nums):
    return [max(nums[0], nums[-1])] * len(nums)

#Logic-1
def cigar_party(cigars, is_weekend):
    return cigars >= 40 if is_weekend else 40 <= cigars <= 60

def date_fashion(you, date):
    return 2 if you >= 8 and date > 2 or date >= 8 and you > 2 else 0 if you <= 2 or date <= 2 else 1

def squirrel_play(temp, is_summer):
    return 60<=temp<=(90 if not is_summer else 100)

def caught_speeding(speed, is_birthday):
    return 0 if speed <= 60 + 5 * is_birthday else 1 if speed <= 80 + 5 * is_birthday else 2

def sorta_sum(a, b):
    return 20 if 10 <= a + b < 20 else a + b

def alarm_clock(day, vacation):
    return 'off' if vacation and day in [0, 6] else '10:00' if vacation or day in [0, 6] else '7:00'

def love6(a, b):
    return 6 in (a, b, a+b, abs(a-b))

def in1to10(n, outside_mode):
    return n in range(1, 11) if not outside_mode else n <= 1 or n >= 10
   
#Saatvik Kesarwani, PD 1, 2026