"""

Test the formatters

"""

from rjgtoys.logs.logpoint.core import repr_by_kwargs, string_by_formatting, LogPoint, WrapMessage, StringFormatters


from mock import Mock
import pytest

class Tester(LogPoint):
    
    # Override the base class constructor
    
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
    
    # I just want to use the dict() method    
    
def test_repr_by_kwargs():
    
    m = Tester(a=2)
    
    repr_by_kwargs(m)
    
    assert m._repr == "Tester(a=2)"
    
def test_string_by_formatting_ok():
    
    m = Tester(a=1,b='b')
    
    m.text = "test a={a} b={b} done"
    
    string_by_formatting(m)
    
    assert m._string == "test a=1 b=b done"
    
    # We don't have to use all attributes
    
    m.text = "test only a: {a}"
    
    string_by_formatting(m)
    
    assert m._string == "test only a: 1"
    
    # but we may not use attrs that are not present
    
    with pytest.raises(Exception) as e:
        m.text = "no such attribute: {c}"
        string_by_formatting(m)

    e = e.value
    
    assert e.message == "missing parameters: c"
    
def test_wrap_message():
    
    m = Tester(a=1,text="tester a={a}")
    
    w = WrapMessage("wrapped ({reason}) {message}")
    
    m.reason = "testing"
    
    w(m)
    
    assert m.text == "wrapped ({reason}) tester a={a}"
    
    string_by_formatting(m)
    
    assert m._string == "wrapped (testing) tester a=1"
    
def test_wrapper():

    m = Tester(a=1,text="tester a={a}")

    assert str(m) == "tester a=1"
    
    with StringFormatters.use_wrapper("wrapped ({reason}) {message}"):
        m = Tester(a=1,text="tester a={a}")
        m.reason = "testing"
        assert str(m) == "wrapped (testing) tester a=1"
    
