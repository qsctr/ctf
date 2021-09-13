import subprocess
import sys

proc = subprocess.Popen(['nc', 'chal.imaginaryctf.org', '42015'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

for _ in range(11):
    proc.stdout.readline()

for _ in range(300):
    expr = proc.stdout.readline()
    if expr.startswith('__import__'):
        proc.stdin.write('\n')
        proc.stdin.flush()
        proc.stdout.readline()
    else:
        print(expr, file=sys.stderr)
        ans = str(eval(expr.replace('i', 'j'))).replace('j', 'i').strip('()')
        print(ans, file=sys.stderr)
        proc.stdin.write(ans + '\n')
        proc.stdin.flush()
        proc.stdout.readline()

while True:
    print(proc.stdout.readline(), file=sys.stderr, end='')
