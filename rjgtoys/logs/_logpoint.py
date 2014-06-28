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
    "log_pid,log_time,send_to_logger,"\
    "LogPointPrint,LogPointJSON,wrapping,"\
    "append_action,remove_action".split(",")

from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

from _logs import getLogger
import string
import inspect
import json
import time
import os

from contextlib import contextmanager

_wrappers = []


@contextmanager
def wrapper(m):
    """
    Creates a context in which logpoint messages are
    wrapped in another message
    """

    wrap(m)
    yield
    unwrap()


def wrap(m):
    """
    Adds a wrapper message to logpoint messages
    """

    _wrappers.insert(0, m)


def unwrap():
    _wrappers.pop(0)


class MsgFormatter(string.Formatter):

    def __init__(self):
        super(MsgFormatter, self).__init__()
        self.missed = set()

    def get_value(self, key, args, kwargs):

        try:
            return super(MsgFormatter, self).get_value(key, args, kwargs)
        except:
            pass
        self.missed.add(key)
        return '{%s}' % (key)


class LogPointAction(object):

    """
    Base class for things that record
    :class:``LogPoint``s when they are
    invoked
    """

    def __call__(self, lpt):
        pass


class LogPointActionChain(LogPointAction):

    """
    A set of actions to be taken when
    processing a :class:`LogPoint`.
    Each action has a name.
    """

    def __init__(self, **actions):
        self.actions = actions

    def update(self, **actions):
        self.actions.update(actions)

    def __call__(self, lpt):
        for n, a in self.actions.iteritems():
            a(lpt)

    def __getitem__(self, n):
        return self.actions[n]

    def __setitem__(self, n, a):
        self.actions[n] = a


class LogPointLoggerAction(LogPointAction):

    def __call__(self, lpt):
        print "getting logger for %s" % (lpt.module)
        log = getLogger(lpt.module)

        log.log(lpt.level, lpt)


class LogPointPrint(LogPointAction):

    def __init__(self, level, stream):
        super(LogPointPrint, self).__init__()
        self.level = level
        self.stream = stream

    def __call__(self, lpt):
        if lpt.level != self.level:
            return

        print >> self.stream, str(lpt)


class LogPointJSON(LogPointPrint):

    def __call__(self, lpt):
        if lpt.level != self.level:
            return

        print >>self.stream, json.dumps(lpt.dict())


def log_pid(lpt):
    lpt.pid = os.getpid()


def log_time(lpt):
    lpt.time = time.time()


def send_to_logger(lpt):
    print "getting logger for %s" % (lpt.module)
    log = getLogger(lpt.module)

    log.log(lpt.level, lpt)


def print_repr(lpt):
    print repr(lpt)

#_actions = set((send_to_logger,))
_actions = []


def append_action(a):
    _actions.append(a)


def remove_action(a):
    _actions.remove(a)


class LogPoint(object):

    level = NOTSET

    text = None

    def __init__(self, name=None, text=None, level=None, **kwargs):

        if name is None:
            name = self.__class__.__name__

        self.logpoint = name

        if text is not None:
            self.text = text

        if level is not None:
            self.level = level

        self._frame = inspect.stack()[1]

        (mod, self.filename, self.lineno, self.function, __, __) = self._frame

        self.module = inspect.getmodule(mod).__name__

        for a in _actions:
            a(self)

    def dict(self):
        return dict((n, getattr(self, n))
                    for n in dir(self) if not n.startswith('_'))

    def __str__(self):
        fmt = MsgFormatter()
        msg = fmt.vformat(self.text, (), self.dict())
        for w in _wrappers:
            msg = fmt.format(w, message=msg, **self.dict())

        if fmt.missed:
            raise Exception("missing parameters: %s"
                            % (",".join(list(fmt.missed))))

        return msg

    def __repr__(self):
        params = ",".join("%s=%r" % (k, v)
                          for (k, v) in self.__dict__.items()
                          if not k.startswith('_'))

        return "%s(%s)" % (self.__class__.__name__, params)


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
