'''Representing a Station entity and can be hashed
'''


class Station:
    def __init__(self, code, name):
        self.code = code
        self.line = code[:2]
        self.index = int(code[2:])
        self.name = name

    def __str__(self):
        return 'Station[{},{}]'.format(self.code, self.name)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)
