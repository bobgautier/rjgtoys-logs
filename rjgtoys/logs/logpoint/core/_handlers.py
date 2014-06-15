"""

Library of :class:`LogPoint` handlers.

"""


__all__ = "Handlers,LoggerHandler,PrintHandler".split(",")

import sys
from logging import NOTSET

from rjgtoys.logs.core import getLogger
from ._actions import LogAction,LogActionList, Actions

Handlers = LogActionList()

Actions.append(Handlers)

class LoggerHandler(LogAction):
    """ An action that sends the logpoint to a :mod:`logging` logger. """
    
    def act(self,lpt):
        print "getting logger for %s" % (lpt.module)
        log = getLogger(lpt.module)
    
        log.log(lpt.level,lpt)


class PrintHandler(LogAction):
    
    def __init__(self,level=NOTSET,stream=None):
        super(PrintHandler,self).__init__()
        if stream is None:
            stream = sys.stdout
        self.level = level
        self.stream = stream

    def match(self,lpt):
        return lpt.level == self.level

    def act(self,lpt):
            
        print >> self.stream, str(lpt)

