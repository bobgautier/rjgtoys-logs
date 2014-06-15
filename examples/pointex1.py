
from rjgtoys.logs.core import getLogger, INFO, ERROR
from rjgtoys.logs.logpoint.core import  LogPoint, wrapper, Handlers, PrintHandler, Builders

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
    Handlers.append(PrintHandler(stream=sys.stdout,level=INFO))
    with wrapper("{filename}:{lineno} {message}"):
        LogHello()

    with wrapper("** {logpoint} {message} **"):
        with wrapper("{module}:{function} {message}"):
            LogHello()
        
    LogTricky()

    Handlers.append(print_repr)
    
    LogHello()
    
