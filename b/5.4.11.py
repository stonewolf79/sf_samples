def e(n,s):
    if s<0: return False
    if n<10: return n==s
    return e(n//10, s-n%10)

print(e(123,6))
print(e(123,7))