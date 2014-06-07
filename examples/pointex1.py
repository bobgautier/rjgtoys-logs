
from rjgtoys.logs import getLogger, LogPoint, INFO, ERROR, wrapping, enable_action

class LogHello(LogPoint):
    level = INFO
    text = "Hello logging"

def print_repr(lpt):
    print repr(lpt)

class LogTricky(LogPoint):
    level = ERROR
    text = "Missing param: {missing}"

if __name__ == "__main__":
    with wrapping("{filename}:{lineno} {message}"):
        LogHello()

    with wrapping("** {logpoint} {message} **"):
        with wrapping("{module}:{function} {message}"):
            LogHello()
        
    LogTricky()

    enable_action(print_repr)
    
    LogHello()
    
