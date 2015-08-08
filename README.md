# classdigger
Flatten Python classes with multiple inheritance

# What is this?
I sometimes wonder where those methods and attributes are coming from when working on a python class which extends multiple super classes. This simple script flattens given class and adds informative comments beside method definitions.

#Example

Create a file with following code
```
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
```
from something import B
parser = ClassDigger(B)
print(parser.as_text())
```

will result:

```
class B(A):
  def b_method(self):
    print('b')
  def a_method(self):  # /home/someuser/something.py <class '__main__.A'>
    print('a')
```

