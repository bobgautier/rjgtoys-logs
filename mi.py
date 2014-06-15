
#
# Doodling with multiple inheritance
#

class Base(object):
    pass
    
class ParentA(object):
    def __init__(self, c):
        print('ParentA called by {0}'.format(c))

class ParentB(dict):
    def __init__(self, c):
        print('ParentB called by {0}'.format(c))
        super(ParentB,self).__init__()

class Child(ParentA, ParentB):
    def __init__(self, c):
        print('Child called by {0}'.format(c))
        ParentA.__init__(self,'Child')
        ParentB.__init__(self,'Child')
        
Child('Main')
