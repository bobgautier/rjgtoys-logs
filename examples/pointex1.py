
from rjgtoys.logs import getLogger, INFO, ERROR
from rjgtoys.logs.logpoint.core import  LogPoint, wrapper, add_handler, LogPointPrint

class LogHello(LogPoint):
    level = INFO
    text = "Hello logging"

def print_repr(lpt):
    print repr(lpt)

class LogTricky(LogPoint):
    level = ERROR
    text = "Missing param: {missing}"

if __name__ == "__main__":
    import sys
    add_handler(LogPointPrint(stream=sys.stdout,level=INFO))
    with wrapper("{filename}:{lineno} {message}"):
        LogHello()

    with wrapper("** {logpoint} {message} **"):
        with wrapper("{module}:{function} {message}"):
            LogHello()
        
    LogTricky()

    add_handler(print_repr)
    
    LogHello()
    
