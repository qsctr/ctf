import subprocess

n = 1337
proc = subprocess.Popen(['nc', 'secretarray.fword.wtf', '1337'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

# skip intro
for _ in range(12):
    proc.stdout.readline()

proc.stdin.write(''.join(f'{i} {(i+1) % n}\n' for i in range(n)))
qs = [int(proc.stdout.readline()) for _ in range(n)] * 2
proc.stdin.write('DONE ' + ' '.join(str((sum(qs[i:i+n:2]) - sum(qs[i+1:i+n:2])) // 2) for i in range(n)) + '\n')
print(proc.stdout.readline())
