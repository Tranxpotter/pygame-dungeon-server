class test:
    def __repr__(self) -> str:
        return "pass"
    
    def s(self):
        print("helo")

x = []
a = test()
x.append(a)
del a

print(x)
print(x[0])
x[0].s()