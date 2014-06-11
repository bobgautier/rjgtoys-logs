"""
Extends the standard :mod:`logging` interface with some UI support.

.. autofunction:: getLogger

.. autoclass:: LogAdapter
   :members:

You'll normally access the functionality of this module via
methods on a :class:`LogAdapter` but stand-alone functions are also provided:

.. autofunction:: set_verbose
.. autofunction:: set_debug


"""


import sys
import logging


from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL


_debug = False
_verbose = False

def configure():
    logging.basicConfig(stream=sys.stdout,level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s")

def set_verbose(verbose=None):
    global _verbose
    
    #print "set_verbose: prev %s new %s" % (_verbose,verbose)
    v = _verbose
    if verbose is not None:
        _verbose = verbose
    return v
    
def set_debug(debug=None):
    global _debug

    #print "set_debug: prev %s new %s" % (_debug,debug)
    d = _debug
    if debug is not None:
        _debug = debug
    return d

# FIXME: define a VERBOSE priority level

class LogAdapter(logging.LoggerAdapter):
    """This wraps a standard :mod:`logging` logger object to
    provide some additional methods.
    """
    
    def verbose(self,msg):
        """ Make an INFO log entry, if 'verbose' logging is enabled
        
        Args:
            msg: The message to log
        """
        
        #print "VERBOSE: %s" % (msg)
        global _verbose
        if _verbose:
            self.info(msg)
            
    def debug(self,msg):
        """ Make a DEBUG log entry, if 'debug' logging is enabled
        
        Args:
            msg: The message to log
        """
        
        global _debug
        if _debug:
            super(LogAdapter,self).debug(msg)

    def add_options(self,p):
        """ Add options to an :class:`argparse.ArgumentParser` to allow it
        to handle ``--debug`` and ``--verbose`` options.
        
        Args:
            p: the :class:`argparse.ArgumentParser` to modify
            
        Returns:
            p
        """
        
        p.add_argument("--debug",help="Enable debug",
            dest="_logdebug", action="store_true", default=None)
            
        p.add_argument("--verbose",help="Verbose output",
            dest="_logverbose", action="store_true", default=None)

        return p
    
    def handle_options(self,opts):
        """
        Handle options returned by :meth:`argparse.ArgumentParser.parse_args`
        and set verbose and debug modes accordingly.
        
        Args:
            opts: Options returned from :meth:`argparse.ArgumentParser.parse_args`
        """
        
        self.set_verbose(opts._logverbose)
        self.set_debug(opts._logdebug)
        
    def set_verbose(self,verbose=None):
        """Set, clear and return verbose mode setting.
        
        Args:
            verbose: None means don't modify the setting, True means set it, False means clear it.
            
        Returns:
            The original verbose mode flag (before any cnange was made)
        """
        
        return set_verbose(verbose)
    
    def set_debug(self,debug=None):
        """Set, clear and return debug mode setting.
        
        Args:
            debug: None means don't modify the setting, True means set it, False means clear it.
            
        Returns:
            The original debug mode flag (before any change was made)
            
        """
        return set_debug(debug)


def getLogger(name):
    """ Like the standard :func:`logging.getLogger` this finds a
    suitable logger object.
    
    Args:
        name: name of the logger object to find.  This parameter
            is usually passed :data:`__name__`, i.e. the name of
            the current module.
            
    Returns:
        A :class:`LogAdapter` object that encapsulates a standard
        logger object and adds a few methods.
        
    """

    if name == "__main__":
        configure()
    return LogAdapter(logging.getLogger(name),{})
