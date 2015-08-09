import os
import inspect


class ClassDigger(object):
    def __init__(self, cls):
        self.cls = cls
        self.structure = self.get_structure(cls)

    def is_excluded(self, name):
        return name.startswith('__')

    def get_file(self, member):
        try:
            f = inspect.getabsfile(member)
        except TypeError:
            f = None
        return f

    def get_structure(self, cls):
        supers = list(inspect.getmro(cls))
        supers.pop(0)
        structure = {'cls': cls, 'supers': supers, 'members': []}
        for name, member in inspect.getmembers(cls):
            if self.is_excluded(name):
                continue
            structure_member = {
                'obj': member,
                'name': name,
                'file': self.get_file(member)}
            try:
                structure_member['lines'] = inspect.getsourcelines(
                    member)
                structure_member['type'] = 'method'
            except:
                structure_member['lines'] = [
                    ['    %s = %s\n' % (name, member)]]
                structure_member['type'] = 'attr'
            for _super in supers:
                for _sname, _smember in inspect.getmembers(_super):
                    if self.is_excluded(_sname):
                        continue
                    if _sname == name and _smember == member:
                        structure_member['root'] = {
                            'obj': _smember,
                            'cls': _super,
                            'file': self.get_file(_super)}
            if structure_member['type'] == 'attr':
                structure['members'].insert(0, structure_member)
            else:
                structure['members'].append(structure_member)
        inherited = map(lambda x: x.__name__, structure['supers'])
        if len(inherited) > 1:
            inherited.pop(inherited.index('object'))
        structure['inherited'] = 'class %s(%s):\n' % (
            structure['cls'].__name__, ','.join(inherited))
        return structure

    def as_text(self):
        txt = self.structure['inherited']
        for member in self.structure['members']:
            lines = member['lines'][0][:]
            if member.get('root'):
                lines[0] = lines[0].replace(
                    '\n', '  # %s %s \n' % (
                        member['root']['file'],
                        member['root']['cls']))
            txt += '\n' + ''.join(lines)

        return txt

    def as_html(self):
        from jinja2 import Template
        template = Template(open('template.html', 'r').read())
        return template.render(structure=self.structure)

    def write(self, path, overwrite=False, contents=None):
        if not overwrite and os.path.exists(path):
            raise IOError('File exists!')
        with open(path, 'w') as f:
            if not contents:
                f.write(self.as_text())
            else:
                f.write(contents)


if __name__ == '__main__':
    from examples.d import D
    from pprint import pprint
    parser = ClassDigger(D)
    pprint(parser.structure)
    print('\n\n')
    print(parser.as_html())
    parser.write('examples/results.py', overwrite=True)
    parser.write('examples/results.html', overwrite=True,
                 contents=parser.as_html())
