# classdigger
Flatten Python classes with multiple inheritance

# What is this?
I sometimes wonder where those methods and attributes are coming from when working on a python class which extends multiple super classes. This is especially very painful when you are working on libraries which excessively use Mixin pattern. This simple script flattens given class and adds informative comments beside method definitions.

#Example

Here is the screencast of html output for ```D``` in  ```examples/d.py```:

![output](https://raw.githubusercontent.com/tatterdemalion/classdigger/master/output.gif)


Create a file with following code
```python
# something.py

class A(object):
  def a_method(self):
    print('a')

class B(A):
  def b_method(self):
    print('b')
    
from classdigger import ClassDigger
```

In python interpreter
```python
from something import B
parser = ClassDigger(B)
print(parser.as_text())
```

will result:

```python
class B(A):
  def b_method(self):
    print('b')
  def a_method(self):  # /home/someuser/something.py <class '__main__.A'>
    print('a')
```

Or you can just run classdigger

```
python classdigger.py
```

And take a look at ```examples/results.py``` and ```examples/results.html``` afterwards.
