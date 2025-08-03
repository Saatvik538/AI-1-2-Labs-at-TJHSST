def string_times(str, n):
  return str*n

def front_times(str, n):
  return str[:3]*n

def string_bits(str):
  return str[::2]

def string_splosion(str):
  return ''.join([str[:n] for n in range(len(str)+1)])

def last2(str):
  return sum(str[i:i+2] == str[-2:] for i in range(len(str)-2))

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
  return nums[:4].count(9)>=1

def array123(nums):
  return any(nums[i:i+3] == [1,2,3] for i in range(len(nums)-2))

def string_match(a, b):
  return sum(1 for x in range(0,len(b)-1) if x<len(a) and b[x:x+2] == a[x:x+2])

def make_bricks(small, big, goal):
  return goal%5<=small and goal<=small+5*big

def lone_sum(a, b, c):
  return sum([a,b,c].count(x) == 1 and x for x in [a,b,c])

def lucky_sum(a, b, c):
  return sum([a,b,c][:([a,b,c]+[13]).index(13)])

def no_teen_sum(a, b, c):
  return sum(x for x in [a,b,c] if x not in [13,14,17,18,19])

def round_sum(a, b, c):
  return sum(10*((x+5)//10) for x in [a,b,c])

def close_far(a, b, c):
  return (abs(a-b) <= 1) != (abs(a-c) <= 1) and abs(b-c) >= 2

def make_chocolate(small, big, goal):
  return max(0, goal - 5 * min(big, goal // 5)) if small >= goal - 5 * min(big, goal // 5) else -1

def count_evens(nums):
  return sum(1 for x in nums if x % 2 == 0)

def big_diff(nums):
  return max(nums) - min(nums)

def centered_average(nums):
  return (sum(nums) - max(nums) - min(nums)) // (len(nums) - 2)

def sum13(nums):
  return sum(val for idx,val in enumerate(nums) if val != 13 and (idx == 0 or nums[idx-1]!=13))

def sum67(nums):
  return (sum(nums) if not nums else (sum67(nums[nums.index(7)+1:]) if nums[0] == 6 else nums[0]+sum67(nums[1:])))

def has22(nums):
    return any(x == y == 2 for x, y in zip(nums, nums[1:]))

def double_char(str):
  return ''.join([x*2 for x in str])

def count_hi(str):
  return str.count("hi")

def cat_dog(str):
  return str.count("cat") == str.count("dog")

def count_code(str):
  return sum(str[i:i+2] == "co" and str[i+3] == "e" for i in range(len(str)-3))

def end_other(a, b):
  return ((a.lower()).endswith(b.lower())) or ((b.lower()).endswith(a.lower()))

def xyz_there(str):
  return any(str[i:i+3] == 'xyz' and (i == 0 or str[i-1] != '.') for i in range(len(str)))

#Saatvik Kesarwani, pd 1, 2026




