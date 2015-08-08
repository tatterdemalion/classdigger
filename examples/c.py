from examples.a import A
from examples.b import B


class C(A, B):
    override_this_attr = False

    def c_method(self):
        pass

    def overridden(self):
        print('This is C')
