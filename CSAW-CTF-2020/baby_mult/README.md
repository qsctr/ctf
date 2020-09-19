# baby_mult (rev)

We are given the following text file:
```
85, 72, 137, 229, 72, 131, 236, 24, 72, 199, 69, 248, 79, 0, 0, 0, 72, 184, 21, 79, 231, 75, 1, 0, 0, 0, 72, 137, 69, 240, 72, 199, 69, 232, 4, 0, 0, 0, 72, 199, 69, 224, 3, 0, 0, 0, 72, 199, 69, 216, 19, 0, 0, 0, 72, 199, 69, 208, 21, 1, 0, 0, 72, 184, 97, 91, 100, 75, 207, 119, 0, 0, 72, 137, 69, 200, 72, 199, 69, 192, 2, 0, 0, 0, 72, 199, 69, 184, 17, 0, 0, 0, 72, 199, 69, 176, 193, 33, 0, 0, 72, 199, 69, 168, 233, 101, 34, 24, 72, 199, 69, 160, 51, 8, 0, 0, 72, 199, 69, 152, 171, 10, 0, 0, 72, 199, 69, 144, 173, 170, 141, 0, 72, 139, 69, 248, 72, 15, 175, 69, 240, 72, 137, 69, 136, 72, 139, 69, 232, 72, 15, 175, 69, 224, 72, 15, 175, 69, 216, 72, 15, 175, 69, 208, 72, 15, 175, 69, 200, 72, 137, 69, 128, 72, 139, 69, 192, 72, 15, 175, 69, 184, 72, 15, 175, 69, 176, 72, 15, 175, 69, 168, 72, 137, 133, 120, 255, 255, 255, 72, 139, 69, 160, 72, 15, 175, 69, 152, 72, 15, 175, 69, 144, 72, 137, 133, 112, 255, 255, 255, 184, 0, 0, 0, 0, 201
```
It seems like all the numbers are between 0 and 255, so maybe this is a decimal representation of some bytes. But if we turn it into actual bytes and put it in a file, we can't run it.
```
$ ./program
zsh: exec format error: ./program
```
Nor can we disassemble it.
```
$ objdump -d program
objdump: program: file format not recognized
```
Maybe it is just a fragment of machine code instead of a full ELF. We can guess that it is probably x86-64 code, so we can tell `objdump` the format.
```
$ objdump -b binary -m i386:x86-64 -D program
```
This worked. Now let's look at the disassembly.
```
program:     file format binary


Disassembly of section .data:

0000000000000000 <.data>:
   0:	55                   	push   %rbp
   1:	48 89 e5             	mov    %rsp,%rbp
   4:	48 83 ec 18          	sub    $0x18,%rsp
   8:	48 c7 45 f8 4f 00 00 	movq   $0x4f,-0x8(%rbp)
   f:	00 
  10:	48 b8 15 4f e7 4b 01 	movabs $0x14be74f15,%rax
  17:	00 00 00 
  1a:	48 89 45 f0          	mov    %rax,-0x10(%rbp)
  1e:	48 c7 45 e8 04 00 00 	movq   $0x4,-0x18(%rbp)
  25:	00 
  26:	48 c7 45 e0 03 00 00 	movq   $0x3,-0x20(%rbp)
  2d:	00 
  2e:	48 c7 45 d8 13 00 00 	movq   $0x13,-0x28(%rbp)
  35:	00 
  36:	48 c7 45 d0 15 01 00 	movq   $0x115,-0x30(%rbp)
  3d:	00 
  3e:	48 b8 61 5b 64 4b cf 	movabs $0x77cf4b645b61,%rax
  45:	77 00 00 
  48:	48 89 45 c8          	mov    %rax,-0x38(%rbp)
  4c:	48 c7 45 c0 02 00 00 	movq   $0x2,-0x40(%rbp)
  53:	00 
  54:	48 c7 45 b8 11 00 00 	movq   $0x11,-0x48(%rbp)
  5b:	00 
  5c:	48 c7 45 b0 c1 21 00 	movq   $0x21c1,-0x50(%rbp)
  63:	00 
  64:	48 c7 45 a8 e9 65 22 	movq   $0x182265e9,-0x58(%rbp)
  6b:	18 
  6c:	48 c7 45 a0 33 08 00 	movq   $0x833,-0x60(%rbp)
  73:	00 
  74:	48 c7 45 98 ab 0a 00 	movq   $0xaab,-0x68(%rbp)
  7b:	00 
  7c:	48 c7 45 90 ad aa 8d 	movq   $0x8daaad,-0x70(%rbp)
  83:	00 
  84:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
  88:	48 0f af 45 f0       	imul   -0x10(%rbp),%rax
  8d:	48 89 45 88          	mov    %rax,-0x78(%rbp)
  91:	48 8b 45 e8          	mov    -0x18(%rbp),%rax
  95:	48 0f af 45 e0       	imul   -0x20(%rbp),%rax
  9a:	48 0f af 45 d8       	imul   -0x28(%rbp),%rax
  9f:	48 0f af 45 d0       	imul   -0x30(%rbp),%rax
  a4:	48 0f af 45 c8       	imul   -0x38(%rbp),%rax
  a9:	48 89 45 80          	mov    %rax,-0x80(%rbp)
  ad:	48 8b 45 c0          	mov    -0x40(%rbp),%rax
  b1:	48 0f af 45 b8       	imul   -0x48(%rbp),%rax
  b6:	48 0f af 45 b0       	imul   -0x50(%rbp),%rax
  bb:	48 0f af 45 a8       	imul   -0x58(%rbp),%rax
  c0:	48 89 85 78 ff ff ff 	mov    %rax,-0x88(%rbp)
  c7:	48 8b 45 a0          	mov    -0x60(%rbp),%rax
  cb:	48 0f af 45 98       	imul   -0x68(%rbp),%rax
  d0:	48 0f af 45 90       	imul   -0x70(%rbp),%rax
  d5:	48 89 85 70 ff ff ff 	mov    %rax,-0x90(%rbp)
  dc:	b8 00 00 00 00       	mov    $0x0,%eax
  e1:	c9                   	leaveq 
```
The function itself does not seem to return anything. However, it does manipulate some values in memory. In particular, it does some multiplications and stores results in `-0x78(%rbp)`, `-0x80(%rbp)`, `-0x88(%rbp)`, and `-0x90(%rbp)`, which are otherwise unused. I translated the program into C and printed out the values of those variables as strings. The output of the C code is
```
flag{sup3r_v4l1d_pr0gr4m}
```
