
#
# Abstract syntax for log filters
#

import yaml

class _FilterMeta(type):
    """
    Metaclass for filter classes,
    just to build the registry
    """
    
    nodetypes = {}
    
    def __init__(cls,name,bases,dct):
        super(_FilterMeta,cls).__init__(name,bases,dct)
        cls.nodetypes[name] = cls

    @classmethod
    def lookup(cls,name):
        return cls.nodetypes[name]

class Filter(object):

    __metaclass__ = _FilterMeta

    @property
    def nodename(self):
        return self.__class__.__name__

    @classmethod
    def unflatten(cls,spec):
        cls = _FilterMeta.lookup(spec[0])
        
        return cls.unflatten(spec[1:])

    def to_yaml(self):
        return yaml.dump(self.flatten(),default_flow_style=False)
    
    @classmethod
    def from_yaml(cls,spec):
        return cls.unflatten(yaml.load(spec))

class EQ_ALL(Filter):
    """ Match records on multiple attributes """

    def __init__(self,**kwds):
        super(EQ_ALL,self).__init__()
        self.matches = kwds

    def flatten(self):
        return [self.nodename] + self.matches.items()

    @classmethod
    def unflatten(cls,spec):
        return cls(**dict(spec))

class Relation(Filter):
    
    def __init__(self,name,value):
        super(Relation,self).__init__()
        self.name = name
        self.value = value
        
    def flatten(self):
        return [self.nodename, self.name, self.value]

    @classmethod
    def unflatten(cls,spec):
        return cls(*spec)

# Define the relations

class LT(Relation):
    """ Match records with an attribute less than a value """
    pass
    
class LE(Relation):
    """ Match records with an attribute less or equal to a value """ 
    pass
    
class GT(Relation):
    """ Match records with an attribute greater than a value """
    pass
    
class GE(Relation):
    """ Match records with an attribute greater or equal to a value """
    pass

class EQ(Relation):
    """ Match records with an attribute equal to a value """
    pass

class NE(Relation):
    """ Match records with an attribute not equal to a value """
    pass

class Unary(Filter):
    def __init__(self,filter):
        super(Unary,self).__init__()
        self.op1 = filter

    def flatten(self):
        return [self.nodename, self.op1.flatten()]

    @classmethod
    def unflatten(cls,spec):
        return cls(Filter.unflatten(spec[0]))
        
class NOT(Unary):
    """ Match records that do not match some other filter """
    pass

class Nary(Filter):
    def __init__(self,*filters):
        super(Nary,self).__init__()
        self.ops = filters

    def flatten(self):
        return [self.nodename] + [op.flatten() for op in self.ops]

    @classmethod
    def unflatten(cls,spec):
        filters = [Filter.unflatten(f) for f in spec]
        return cls(*filters)

class AND(Nary):
    """ Match records that pass all of a set of other filters """
    pass

class OR(Nary):
    """ Match records that pass at least one of a set of other filters """
    pass

#
# Simple interpreter for the above filters
#

class _SimpleFilterMeta(type):
    """
    Metaclass for simple filter implementation classes,
    just to build the registry
    """
    
    subclasses = {}
    
    def __init__(cls,name,bases,dct):
        super(_SimpleFilterMeta,cls).__init__(name,bases,dct)
        cls.subclasses[name] = cls

    @classmethod
    def lookup(cls,filter):
        return cls.subclasses['_Simple_'+filter.nodename]
    
class _SimpleFilter(object):

    __metaclass__ = _SimpleFilterMeta
    
    def __init__(self,filter):
        self.filter = filter
        
    def read(self,pipe):
        for r in pipe:
            if self.match(r):
                yield r

class _Simple_EQ_ALL(_SimpleFilter):
        
    def match(self,r):
        try:
            m = dict((k,r[k]) for k in self.filter.matches.keys())
        except KeyError:
            return False

        return m == self.filter.matches

class _Simple_EQ(_SimpleFilter):
    
    def match(self,r):
#        print "match EQ %s=%s %s" % (self.filter.name, self.filter.value,r)
        try:
            m = r[self.filter.name]
        except:
            return False
            
        return m == self.filter.value

class _Simple_Unary(_SimpleFilter):
    
    def __init__(self,filter):
        super(_Simple_Unary,self).__init__(filter)
        
        self.op1 = SimpleFilter(self.filter.op1)

class _Simple_NOT(_Simple_Unary):
    
    def match(self,r):
        return not self.op1.match(r)

class _Simple_Nary(_SimpleFilter):
    
    def __init__(self,filter):
        super(_Simple_Nary,self).__init__(filter)
        self.ops = [SimpleFilter(op) for op in self.filter.ops]

class _Simple_AND(_Simple_Nary):
    
    def match(self,r):
        for op in self.ops:
            if not op.match(r):
                return False
        return True
        
class _Simple_OR(_Simple_Nary):
    
    def match(self,r):
        for op in self.ops:
            if op.match(r):
                return True
                
        return False


def SimpleFilter(filter):
    
    a = _SimpleFilterMeta.lookup(filter)
    return a(filter)

if __name__ == "__main__":
    
    eq=EQ_ALL(a=1,b=2)
    
    p = SimpleFilter(eq)
    
    print p.match(dict(a=1,b=2))
    print p.match(dict(x=2,b=2))
    
    print _SimpleFilterMeta.subclasses
    
