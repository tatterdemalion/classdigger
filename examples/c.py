from examples.a import A
from examples.b import B


class C(A, B):
    def c_method(self):
        pass

    def overridden(self):
        print('This is C')
