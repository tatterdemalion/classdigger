import os
import inspect


class ClassDigger(object):
    def __init__(self, cls):
        self.cls = cls
        self.structure = self.get_structure(cls)

    def is_excluded(self, name):
        return name.startswith('__')

    def get_structure(self, cls):
        supers = list(inspect.getmro(cls))
        supers.pop(0)
        structure = {'cls': cls, 'supers': supers, 'members': {}}
        for name, member in inspect.getmembers(cls):
            if self.is_excluded(name):
                continue
            structure['members'][name] = {'obj': member}
            try:
                structure['members'][name]['lines'] = inspect.getsourcelines(
                    member)
            except:
                structure['members'][name]['lines'] = [['']]
            for _super in supers:
                for _sname, _smember in inspect.getmembers(_super):
                    if self.is_excluded(_sname):
                        continue
                    if _smember == member:
                        structure['members'][name]['root'] = {
                            'obj': _smember,
                            'cls': _super}
                        try:
                            f = inspect.getabsfile(_super)
                            structure['members'][name]['root']['file'] = f
                        except TypeError:
                            structure['members'][name]['root']['file'] = None
        return structure

    def as_text(self):
        inherited = map(lambda x: x.__name__, self.structure['supers'])
        if len(inherited) > 1:
            inherited.pop(inherited.index('object'))
        txt = 'class %s(%s):\n' % (
            self.structure['cls'].__name__, ','.join(inherited))
        for name, member in self.structure['members'].items():
            lines = member['lines'][0][:]
            if member.get('root'):
                lines[0] = lines[0].replace(
                    '\n', '  # %s %s \n' % (
                        member['root']['file'],
                        member['root']['cls']))
            txt += ''.join(lines)

        return txt

    def write(self, path, overwrite=False):
        if not overwrite and os.path.exists(path):
            raise IOError('File exists!')
        with open(path, 'w') as f:
            f.write(self.as_text())


if __name__ == '__main__':
    from examples.d import D
    from pprint import pprint
    parser = ClassDigger(D)
    pprint(parser.structure)
    print('\n\n')
    print(parser.as_text())
    parser.write('examples/results.py', overwrite=True)
