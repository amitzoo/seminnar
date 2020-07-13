
class Person:
    def __init__(self, height, weight, age):
        self.height = height
        self.weight = weight
        self.age = age

    def __repr__(self):
            return '({}, {}, {})'.format(self.height, self.weight, self.age)

    def __lt__(self, other):
        if self.height < other.height:
            return True
        elif self.height > other.height:
            return False
        else: # equals
            if self.weight < other.weight:
                return True
            elif self.weight > other.weight:
                return False
            else: # length equals
                return self.age < other.age

    def __gt__(self, other):	# >
        if self.height > other.height:
            return True
        elif self.height < other.height:
            return False
        else: # equals
            if self.weight > other.weight:
                return True
            elif self.weight < other.weight:
                return False
            else: # length equals
                return self.age > other.age

    '''
        def __eq__(self, other):
            return not self < other and not other < self'''

    '''def __ne__(self, other):
        return self < other or other < self'''

    '''def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self'''
