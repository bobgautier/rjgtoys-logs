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
            "LogError,LogWarning,LogInfo,LogDebug,"\
            "log_pid,log_time,log_bigpid,log_ugid,send_to_logger,LogPointPrint,LogPointJSON,wrapper,add_handler,remove_handler,add_builder,remove_builder".split(",")

from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

from rjgtoys.logs import getLogger
import string
import inspect
import re

import time
import os

from contextlib import contextmanager

@contextmanager
def wrapper(m):
    """
    Creates a context in which logpoint messages are
    wrapped in another message
    """

    with use_builders(wrapper=LogPointWrapMessage(m)):
        yield

class MsgFormatter(string.Formatter):
    
    def __init__(self):
        super(MsgFormatter,self).__init__()
        self.missed = set()
            
    def get_value(self,key,args,kwargs):

        try:
            return super(MsgFormatter,self).get_value(key,args,kwargs)
        except:
            pass
        self.missed.add(key)
        return '{%s}' % (key)

class LogPointAction(object):
    """
    Base class for things that operate
    on :class:``LogPoint``s
    """

    def __call__(self,lpt):
        if self.match(lpt):
            self.act(lpt)

    def match(self,lpt):
        return True

    def act(self,lpt):
        pass

class LogPointActionGroup(LogPointAction):
    """
    A set of actions to be taken when
    processing a :class:`LogPoint`.
    Each action has a name.
    """
    
    def __init__(self,**actions):
        self.actions = actions
        
    def update(self,**actions):
        self.actions.update(actions)

    def match(self,lpt):
        if not self.match_group(lpt):
            return False

        for (n,a) in self.actions.iteritems():
            try:
                if a.match(lpt):
                    return True
            except:
                return True
        return False

    def match_group(self,lpt):
        return True

    def act(self,lpt):
        for n,a in self.actions.iteritems():
            a(lpt)

    def __getitem__(self,n):
        return self.actions[n]

    def __setitem__(self,n,a):
        self.actions[n] = a

"""
Handlers and Builders: Both are actions, and moderately interchangeable,
but builders all run before the handlers, so the former are for collecting
information and the latter are for saving or presenting it.

The order of execution of handlers relative to each other, and of builders
relative to each other is not expected to matter.

"""

_handler = []
_builder = []

def add_handler(a):
    _add_action(_handler,a)
    
def remove_handler(a):
    _remove_action(_handler,a)

def add_builder(b):
    _add_action(_builder,b)
    
def remove_builder(b):
    _remove_action(_builder,b)

def _add_action(stack,a):
    stack.insert(0,a)

def _remove_action(stack,a):
    stack.remove(a)

def _run_actions(stack,lpt):
    for a in stack:
        a(lpt)

@contextmanager
def use_handlers(**handlers):
    
    with _use_actions(_handler,handlers):
        yield

@contextmanager
def use_builders(**builders):
    with _use_actions(_builder,builders):
        yield

@contextmanager
def _use_actions(stack,actions):
    if len(actions) > 1:
        act = LogPointActionGroup(**actions)
    else:
        act = actions.values()[0]
    
    _add_action(stack,act)
    yield
    _remove_action(stack,act)

class LogPointLoggerAction(LogPointAction):
    
    def act(self,lpt):
        print "getting logger for %s" % (lpt.module)
        log = getLogger(lpt.module)
    
        log.log(lpt.level,lpt)

class LogPointWrapMessage(LogPointAction):
    """
    Wraps the message of any logpoints it handles
    in another message.
    
    This can be used to include more fields in
    the message but can also convert to other
    formats such as HTML or XML
    """

    _target = re.compile(r"{message}")

    def __init__(self,wrapper):
        super(LogPointWrapMessage,self).__init__()
        self.wrapper = wrapper
        
    def act(self,lpt):
        lpt.text = self._target.sub(lpt.text,self.wrapper)
        

class LogPointPrint(LogPointAction):
    
    def __init__(self,level=NOTSET,stream=None):
        super(LogPointPrint,self).__init__()
        if stream is None:
            stream = sys.stdout
        self.level = level
        self.stream = stream

    def match(self,lpt):
        return lpt.level == self.level

    def act(self,lpt):
            
        print >> self.stream, str(lpt)

import json

class LogPointJSON(LogPointPrint):
    
    def __call__(self,lpt):
        if lpt.level != self.level:
            return

        print >>self.stream, json.dumps(lpt.dict())

def log_pid(lpt):
    """ A builder that adds 'pid' and 'ppid' """
    
    lpt.pid = os.getpid()
    lpt.ppid = os.getppid()
    
def log_time(lpt):
    """ A builder that adds the current epoch time ``time.time()`` """
    lpt.time = time.time()

def log_ugid(lpt):
    """ A builder that adds uid, gid, euid and egid """
    
    lpt.uid = os.getuid()
    lpt.gid = os.getgid()
    lpt.euid = os.geteuid()
    lpr.egid = os.getegid()
    
def log_bigpid(lpt):
    """ A builder that adds a "bigpid", which is a quantity
    derived from the PID and the current time so that it is unique
    for the lifetime of a machine.  It can therefore be used to refer
    to sections of a long log that might cover such a long period that
    PIDs are not unique.
    
    A bigpid is a hexadecimal string.
    """
    
    lpt.bigpid = hex(int(time.time()*os.getpid()))[2:] 
    
def send_to_logger(lpt):
    """ An action that sends the logpoint to a :mod:`logging` logger. """

    log = getLogger(lpt.module)

    log.log(lpt.level,lpt)

def print_repr(lpt):
    """ An action that prints the ``repr()`` of the logpoint """
    print repr(lpt)

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

        _run_actions(_builder,self)
        _run_actions(_handler,self)

    def dict(self):
        return dict((n,v) for (n,v) in self.__dict__.items() if not n.startswith('_') and not callable(v))

    def __str__(self):
        fmt = MsgFormatter()
        msg = fmt.vformat(self.text,(),self.dict())

        if fmt.missed:
            raise Exception("missing parameters: %s" % (",".join(list(fmt.missed))))

        return msg
        
    def __repr__(self):
        params = ",".join("%s=%r" % (k,v) for (k,v) in self.__dict__.items() if not k.startswith('_'))
        
        return "%s(%s)" % (self.__class__.__name__,params)

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
