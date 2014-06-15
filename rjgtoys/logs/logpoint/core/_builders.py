"""

Library of :class:`LogPoint` builders

"""

import time
import os

__all__ = "Builders,build_pid,build_time,build_ugid,build_bigpid".split(",")

from ._actions import LogActionList, Actions

Builders = LogActionList()

Actions.prepend(Builders)

def build_pid(lpt):
    """ A builder that adds 'pid' and 'ppid' """
    
    lpt.pid = os.getpid()
    lpt.ppid = os.getppid()
    
def build_time(lpt):
    """ A builder that adds the current epoch time ``time.time()`` """
    lpt.time = time.time()

def build_ugid(lpt):
    """ A builder that adds uid, gid, euid and egid """
    
    lpt.uid = os.getuid()
    lpt.gid = os.getgid()
    lpt.euid = os.geteuid()
    lpt.egid = os.getegid()
    
def build_bigpid(lpt):
    """ A builder that adds a "bigpid", which is a quantity
    derived from the PID and the current time so that it is unique
    for the lifetime of a machine.  It can therefore be used to refer
    to sections of a long log that might cover such a long period that
    PIDs are not unique.
    
    A bigpid is a hexadecimal string.
    """
    
    lpt.bigpid = hex(int(time.time()*os.getpid()))[2:] 
