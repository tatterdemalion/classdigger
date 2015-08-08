from examples.c import C


class D(C):
    def d_method(self):
        if getattr(self, 'a'):
            return self.a
        return

    def overridden(self):
        print('This is D')
