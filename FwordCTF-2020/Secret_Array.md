# Secret Array (Misc)

We are given the following information:

```
I have a 1337 long array of secret positive integers. The only information I can provide is the sum of two elements. You can ask for that sum up to 1337 times by specifing two different indices in the array.

[!] - Your request should be in this format : "i j". In this case, I'll respond by arr[i]+arr[j]

[!] - Once you figure out my secret array, you should send a request in this format: "DONE arr[0] arr[1] ... arr[1336]"

[*] - Note 1: If you guessed my array before 1337 requests, you can directly send your DONE request.
[*] - Note 2: The DONE request doesn't count in the 1337 requests you are permitted to do.
[*] - Note 3: Once you submit a DONE request, the program will verify your array, give you the flag if it's a correct guess, then automatically exit.
```

We know this is solvable because we basically have a system of 1337 equations with 1337 unknowns. If we query in the following way
```
0 1
1 2
...
1336 0
```
then we get the following equations:
```
x0 + x1 = q0
x1 + x2 = q1
...
x1336 + x0 = q1336
```
where `q0` to `q1336` are the results of the queries.

There is a simple pattern we can take advantage of to solve this system easily. If we have five equations,
```
x0 + x1 = q0
x1 + x2 = q1
x2 + x3 = q2
x3 + x4 = q3
x4 + x0 = q4
```
then we can observe that
```
q0 - q1 + q2 - q3 + q4
= x0 + x1 - x1 - x2 + x2 + x3 - x3 - x4 + x4 + x0
= 2 * x0
```
and
```
q1 - q2 + q3 - q4 + q0
= x1 + x2 - x2 - x3 + x3 + x4 - x4 - x0 + x0 + x1
= 2 * x1
```
So to get each value we can add and subtract alternating queries starting from the query for that value, wrapping around if we go past the end, until we reach the starting query again, then divide by 2. We wrote a Python script that runs `nc`, provides the necessary input, performs the calculations, sends the results back, and finally outputs the flag.
```python
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
```
