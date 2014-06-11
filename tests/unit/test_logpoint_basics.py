
from rjgtoys.logs.logpoint.core import LogPoint, add_builder, add_handler

from mock import Mock

def test_log_hello_world():
    
    m = Mock()
    
    add_builder(m)
    
    v = LogPoint(text="Hello, world")
    
    assert m.called_once_with(v)
    
    
