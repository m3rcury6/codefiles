''' Objective: go into some detail about stranger things that are possible in python.

assumptions:
working in python3. if a concept requires a specific version, will denote
topics: 


SOURCES:
Decorators: https://realpython.com/primer-on-python-decorators/
F-Strings: https://cito.github.io/blog/f-strings/
Class Iterator: (note, assumes Python2) https://anandology.com/python-practice-book/iterators.html 
Iterators, pt2: (note, assumes Python2) https://www.programiz.com/python-programming/iterator

'''

# initializations ##########################################
import sys


print('''
################################################################################
# Some Special Kinds of Strings ################################################
''')

name='Fred'
age=42
print('his name is {} and he is {} years old'.format(name,age))
#>> his name is Fred and he is 42 years old

# post python3.6 thing: f-string literal. functionally same 
# as above, but with following formatting:
# >> print(f'He said his name is {name} and he is {age} years old.')


print('''
################################################################################
# Decorators ###################################################################
''')

# long method:

def say_whee():
    print("Whee!")

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

print('0th time')
say_whee()

print('1st time')
say_whee = my_decorator(say_whee)
say_whee()

print('2nd time')
say_whee = my_decorator(say_whee)
say_whee()

# short method
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

print('short method')

print('0th time')
def say_whee():
    print("Whee!")
say_whee()

print('1st time')
@my_decorator
def say_whee():
    print("Whee!")
say_whee()


print('2nd time')
@my_decorator
@my_decorator
def say_whee():
    print("Whee!")
say_whee()



print('''
################################################################################
# Built-In Class Methods #######################################################
''')

# looking at: init, repr, iter, and call

class Dog:
    def __init__(self,n=10,name='spike'):
        ''' __init__ is the instatiation function for a class. when a class is 
            called, such as here with "newdog = Dog('spike')", then the object 
            is created from the class, with any object/class specific 
            properties.
        '''
        self.name=name # the dog's name, duh
        self.i=0
        self.n = n
    def __repr__(self):
        ''' __repr__ officially "computes the official string reputation of an 
            object. note: MUST be a string.
        '''
        return self.name
    def __iter__(self):
        ''' __iter__ enables the object to be iterable. complimented by 
            __next__ in order to achieve some sort of iteration.
        '''
        return self
    def __next__(self):
        ''' __next__ is a python3-specific function that accompanies __iter__ 
            in order to allow iteration. custom-defined function that allows 
            object to be iterated on.
        '''
        if(self.i<self.n):
            i=self.i
            self.i+=1
            return i
        else:
            raise StopIteration() # usually necessary to prevent infinite iteration
            #self.i=0
            #return self.i
# class Dog


d=Dog()
print(d)
print(sum(d)) #sums up from 0 to n-1




print('''
################################################################################
# "property" built-in decorator in a class #####################################
''')


class Rect:
    def __init__(self,ht=0,wd=0):
        # pass # optionally, can just leave everything blank, uninitialized, until user sets them
        self.ht=ht
        self.wd=wd
    
    @property
    def ht(self):
        return self._ht

    def check(self,x):
        if(x<0.0):
            raise ValueError("Can't have negative value")
        return x
        
    @ht.setter
    def ht(self,value):
        self._ht=self.check(value)
    
    @property
    def wd(self):
        return self._wd
    @wd.setter
    def wd(self,value):
        self._wd=self.check(value)
    
    @property
    def area(self):
        return self.ht*self.wd

    def perim(self):
        return 2*(self.ht+self.wd)

a=Rect()
a.ht=2
a.wd=3
try:
    a.ht=-1
except ValueError:
    print("can't set negative height")

try:
    a.wd=-1
except ValueError:
    print("can't set negative width")

print("height:{}, width:{}, area:{}".format(a.ht,a.wd,a.area))
print("perimeter:",a.perim())



print('''
################################################################################
# decorator for function that takes arguments ##################################
''')

def dec2(fn):
    def wrapper(*args,**kwargs):
        print('before')
        res = fn(*args,**kwargs)
        print('after')
        return res
    return wrapper

# @dec2 # can also do it this way
def pyt(a,b):
    return (a**2+b**2)**0.5


pyt=dec2(pyt)

print(pyt(3,4))


print('\n\nDone.')
#eof