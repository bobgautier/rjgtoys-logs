#
# Actions on logpoints
#


__all__ = \
    "LogAction,LogActionList,Actions".split(",")


import time
import os
import string
import re

from logging import NOTSET

from contextlib import contextmanager


class LogAction(object):
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



"""
Handlers and Builders: Both are actions, and moderately interchangeable,
but builders all run before the handlers, so the former are for collecting
information and the latter are for saving or presenting it.

The order of execution of handlers relative to each other, and of builders
relative to each other is not expected to matter.

"""

class LogActionList(list,LogAction):
    
    def __init__(self,*actions):
        list.__init__(self,actions)

    def prepend(self,action):
        self.insert(0,action)
        return self

    def add_after(self,actions,after=None):

        if not after:
            self.extend(actions)
            return self
            
        pos = self.index(after)+1

        self[pos:pos] = actions
        return self

    @contextmanager
    def use_after(self,actions,after=None):
        
        self.add_after(actions,after=after)
        yield self
        self.remove(*actions)

        
    def add_before(self,actions,before=None):
        """ Add some actions to precede another """
 
        pos = 0
        if before:
            pos = self.index(before)
        
        self[pos:pos] = actions
        return self

    @contextmanager
    def use_before(self,actions,before=None):
        
        self.add_before(actions,before=before)
        yield self
        self.remove(*actions)

    def discard(self,action):
        try:
            self.remove(action)
        except ValueError:
            pass

    def remove(self,*actions):
        """ Removes all references to each action """
        
        for a in set(actions):
            list.remove(self,a)    # This one might raise an exception
            try:
                while True:
                    list.remove(self,a)
            except ValueError:
                pass

    def __call__(self,lpt):
        for a in self:
            a(lpt)

    @contextmanager
    def disabled(self):
        """ Primarily for testing, allows all actions to be disabled
        and then restored """
        
        temp = self[0:]
        self[0:] = []
        yield
        self[0:] = temp
        
Actions = LogActionList()
