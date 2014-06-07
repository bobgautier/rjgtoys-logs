
import sys

from rjgtoys.logs import getLogger, LogPoint, LogPointPrint, INFO, ERROR, wrapping, enable_action, disable_action, send_to_logger

class LogHello(LogPoint):
    level = INFO
    text = "Hello logging"

def print_repr(lpt):
    print repr(lpt)


def main():
    with wrapping("** {logpoint} {message} **"):
        with wrapping("{module}:{function} {message}"):
            LogHello()

if __name__ == "__main__":
    
    disable_action(send_to_logger)
    enable_action(LogPointPrint(ERROR,sys.stderr))
    enable_action(LogPointPrint(INFO,sys.stdout))
    
    with wrapping("{filename}:{lineno} {message}"):
        LogHello()

    enable_action(print_repr)

    main()
    LogHello()
    
