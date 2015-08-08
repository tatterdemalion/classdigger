class A(object):
    an_attr = True
    another_attr = False

    def a_method(self):
        self.a = 4
        return self.a

    def overridden(self):
        print('This is A')
