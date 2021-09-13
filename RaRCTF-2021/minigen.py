from z3 import *

x = Int('x')

s = Solver()

def f(n):
    return (n*n + n + 1) % 727

def g(n, k, c):
    return f(n) == k ^ ord(c)

for i, (k, c) in enumerate(zip([281, 547, 54, 380, 392, 98, 158], 'rarctf{')):
    s.add(g(x + i, k, c))

print(s)
print(s.check())
print(s.model())

xs = [440, 724, 218, 406, 672, 193, 457, 694, 208, 455, 745, 196, 450, 724]

b = 470

for a in xs:
    i += 1
    print(chr(f(b + i) ^ a), end='')
