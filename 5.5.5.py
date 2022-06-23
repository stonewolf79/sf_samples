a = ["asd", "bbd", "ddfa", "mcsa"]

b = [len(x) for x in a]
print(b)

c = list(map(len,a))
print(c)