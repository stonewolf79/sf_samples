def min_list(L):
    l0 = L[0]
    if len(L) == 1:
        return l0
    return l0 if l0 < min_list(L[1:]) else min_list(L[1:])

print(min_list([1,3,2]))