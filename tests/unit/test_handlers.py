"""

Tests for handlers

"""

from rjgtoys.logs.logpoint.core import LoggerHandler, PrintHandler

from mock import Mock, patch, sentinel

import sys
import StringIO

def test_logger_handler():
    
    lpt = Mock()
    lpt.level = sentinel.level
    lpt.module = sentinel.module
    
    logger = Mock()

    getLogger = Mock(return_value=logger)
    with patch('rjgtoys.logs.logpoint.core._handlers.getLogger',getLogger):
        handler = LoggerHandler()
        
        handler(lpt)
        
    getLogger.assert_called_once_with(sentinel.module)
    logger.log.assert_called_once_with(sentinel.level,lpt)
    
def test_print_handler_matches():
    
    lpt = Mock()
    lpt.level = sentinel.level

    lpt.__str__ = Mock(return_value=str(sentinel.lptstring))
    
    stream = StringIO.StringIO()
    
    p = PrintHandler(level=sentinel.level,stream=stream)
    
    p(lpt)
    
    assert stream.getvalue() == str(sentinel.lptstring)+'\n'
    
def test_print_handler_stream_default():
    p = PrintHandler()
    
    assert p.stream is sys.stdout

def test_print_handler_filters():
        
    lpt = Mock()
    lpt.level = 1
    
    stream = StringIO.StringIO()
    
    p = PrintHandler(level=2,stream=stream)
    
    p(lpt)
    
    # Nothing was output
    
    assert not stream.getvalue()
    
    # Check the reason
    
    assert not p.match(lpt)
    
