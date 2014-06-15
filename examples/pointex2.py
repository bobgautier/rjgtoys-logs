
import sys

from rjgtoys.logs.core import getLogger

from rjgtoys.logs.logpoint.core import LogPoint, PrintHandler, INFO, ERROR, wrapper, Handlers, LoggerHandler

class LogHello(LogPoint):
    level = INFO
    text = "Hello logging"

def print_repr(lpt):
    print repr(lpt)


def main():
    with wrapper("** {logpoint} {message} **"):
        with wrapper("{module}:{function} {message}"):
            LogHello()

if __name__ == "__main__":
    
    Handlers.extend((
        LoggerHandler(),
        PrintHandler(ERROR,sys.stderr),
        PrintHandler(INFO,sys.stdout)
        ))
    
    with wrapper("{filename}:{lineno} {message}"):
        LogHello()

    Handlers.append(LoggerHandler())

    main()
    LogHello()
    
