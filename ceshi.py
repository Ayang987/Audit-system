a=None
b=[1]
print(type(b))
print((a if a else [])+(b if b else []))
print(type((a if a else [])+(b if b else [])))