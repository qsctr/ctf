import time
import subprocess
level1 = [('initial', 'target')]
level2 = [('hello', 'goodbye'), ('ginkoid', 'ginky')]
level3 = [('aa', 'a'), ('aaa','a')]
level4 = [('gg', 'z'), ('zz','z'), ('zg','ginkoid'), ('z','ginkoid')]
level5 = [('1not_palindrome0', 'not_palindrome'), ('0not_palindrome1', 'not_palindrome'), ('1not_palindrome1', 'not_palindrome'), ('0not_palindrome0', 'not_palindrome'), ('1palindrome0', 'not_palindrome'), ('0palindrome1', 'not_palindrome'), ('1palindrome1', 'palindrome'), ('0palindrome0', 'palindrome'), ('^$','palindrome'), ('^1$','palindrome'), ('^0$','palindrome'), ('^0', '0^z'), ('0$', 'z$0'), ('^1', '1^z'), ('1$', 'z$1'), ('z', '')]
level6 = [('=','TeqZ'),('^+', '^'),('+', 'addf'), ('0addf','f0add'),('1addf','f1add'),
                    ('0add0','00add'),('0add1','10add'),('1add0','01add'),('1add1','11add'), 
                    ('00add','ans0'), ('01add','ans1'), ('10add','ans1'), ('11add','car0'), ('1add','1'),('0add','0'), ('fans', 'f0ans'), ('fcar','f0car'),('f', '+'),
                    ('^f','^0'),('ans0T','T0'), ('ans1T','T1'), ('car0car0T','car1T0'),('ans0car0T','T10'), ('ans1car0T','car0T0'), ('ans0car1T','T11'), ('ans1car1T','car0T1'), ('car1car0T', 'car1T0'), ('car0car1T','car1T1'), ('0car0','10'), ('1car0','car00'), ('0car1','11'), ('1car1','car01'), ('car0', '10'), ('car1','11'), ('T',''),
                    ('0eqZ', 'Z0eq'), ('1eqZ', 'Z1eq'),
                    ('0eq0','00eq'), ('0eq1','10eq'), ('1eq0','01eq'), ('1eq1','11eq'),
                    ('^Z$', 'correct'), ('0incorrect', 'incorrect'), ('1incorrect', 'incorrect'), ('Zincorrect', 'incorrect'), ('^incorrect$', 'incorrect'),
                    ('00eq', ''), ('11eq', ''), ('10eq', 'incorrect'), ('01eq', 'incorrect'), ('^Z', '^0Z'), ('Z$', 'Z0$'), ('Z', 'eqZ')]

def convert(subs):
    num = len(subs)
    count = 0
    for a,b in subs:
        print(f'{a} => {b}')
        count = count+1
        if not count == len(subs):
            print('y')
        else:
            print('n')


time.sleep(0.4)
print('y')

for i in range(6):
    time.sleep(0.4)
    if i == 0:
        convert(level1)
    elif i == 1:
        convert(level2)
    elif i == 2:
        convert(level3)
    elif i == 3:
        convert(level4)
    elif i == 4:
        convert(level5)
    elif i == 5:
        convert(level6)
    time.sleep(0.4)
    print('y')