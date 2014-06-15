"""

Log points are objects that capture the business of making
log entries.

They are an attempt to get away from logging in a primarily
human-oriented way, in order to support building on top of
the logging mechanism such things as monitoring, fault
detection and metric collection.

.. autoclass:: LogPoint

"""

__all__ = "NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL,LogPoint,LogCritical," \
            "LogError,LogWarning,LogInfo,LogDebug".split(",")

from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

from ._actions import Actions
from ._formatters import StringFormatters, ReprFormatters

import string
import inspect
import re

class LogPoint(object):

    level = NOTSET

    text = None
    
    def __init__(self,name=None,text=None,level=None,**kwargs):

        if name is None:
            name = self.__class__.__name__
        
        self.__dict__.update(kwargs)

        self.logpoint = name
        
        if text is not None:
            self.text = text
        
        if level is not None:
            self.level = level

        self._frame = inspect.stack()[1]
        
        (mod,self.filename,self.lineno,self.function,_,_) = self._frame

        self.module = inspect.getmodule(mod).__name__

        Actions(self)

    def dict(self):
        return dict((n,v) for (n,v) in self.__dict__.items() if not n.startswith('_') and not callable(v))

    def __str__(self):
        
        try:
            return self._string
        except AttributeError:
            pass
        
        StringFormatters(self)
        try:
            return self._string
        except AttributeError:
            return super(LogPoint,self).__str__()
        
    def __repr__(self):
        try:
            return self._repr
        except AttributeError:
            pass
            
        ReprFormatters(self)
        try:
            return self._repr
        except AttributeError:
            return super(LogPoint,self).__repr__()
            
class LogCritical(LogPoint):
    level = CRITICAL

class LogError(LogPoint):    
    level = ERROR

class LogWarning(LogPoint):
    level = WARNING

class LogInfo(LogPoint):
    level = INFO

class LogDebug(LogPoint):
    level = DEBUG
