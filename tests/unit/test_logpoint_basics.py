
from rjgtoys.logs.logpoint.core import LogPoint, Builders, Handlers, StringFormatters, ReprFormatters, Actions, ERROR, NOTSET

from mock import Mock

def test_log_construction():
    
    na = len(Actions)
    assert na
    
    with Actions.disabled():
        
        p = LogPoint()
        assert p.text is None
        assert p.level == NOTSET
        assert p.logpoint == "LogPoint"
        
        p = LogPoint(level=ERROR,text="Error")
        assert p.text == "Error"
        assert p.level == ERROR
        assert p.logpoint == "LogPoint"
    
    assert len(Actions) == na
        
def test_log_hello_world():
    
    m = Mock()
    
    Builders.append(m)
    
    v = LogPoint(text="Hello, world")
    
    assert m.called_once_with(v)
    
def test_str_defaults():
    
    with Actions.disabled(), StringFormatters.disabled(), ReprFormatters.disabled():
        p = LogPoint()
        
        s = str(p)
        # I don't care what it is, but it has to be something
        assert len(s)
        
        # And it has to be consistent
        s1 = str(p)
        assert s == s1
        
def test_repr_defaults():
    
    with Actions.disabled(), ReprFormatters.disabled():
        p = LogPoint()
        
        r = repr(p)
        assert len(r)
        
        r1 = repr(p)
        assert r1 == r
        
def simple_repr(lpt):
    lpt._repr = "lpt repr %d" % (id(lpt))

def simple_string(lpt):
    lpt._string = "lpt string %d" % (id(lpt))

def test_repr_caching():

    with Actions.disabled(), ReprFormatters.disabled():
        p = LogPoint()

        # Get default repr
        
        r = repr(p)
        assert len(r)
    
        # Install an action to change it
        ReprFormatters.append(simple_repr)
        
        r1 = repr(p)
        
        # It should have changed
        
        assert r1 != r
    
        # Disable creation of reprs
        
        ReprFormatters.remove(simple_repr)
        
        assert len(ReprFormatters) == 0
        
        # Ask for it anyway
        
        r2 = repr(p)
        assert r2 == r1

        # Finally, this is why
        
        assert p._repr == r1

def test_str_caching():

    with Actions.disabled(), StringFormatters.disabled(), ReprFormatters.disabled():
        p = LogPoint()

        # Get default str
        
        s = str(p)
        assert len(s)
    
        # Install an action to change it
        StringFormatters.append(simple_string)
        
        s1 = str(p)
        
        # It should have changed
        
        assert s1 != s
    
        # Disable creation of reprs
        
        StringFormatters.remove(simple_string)
        
        assert len(StringFormatters) == 0
        
        # Ask for it anyway
        
        s2 = str(p)
        assert s2 == s1

        # Finally, this is why
        
        assert p._string == s1
