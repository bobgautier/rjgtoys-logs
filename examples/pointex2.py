
import sys

from rjgtoys.logs import getLogger

from rjgtoys.logs.logpoint.core import LogPoint, LogPointPrint, INFO, ERROR, wrapper, add_handler, remove_handler, send_to_logger

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
    
    add_handler(send_to_logger)
    add_handler(LogPointPrint(ERROR,sys.stderr))
    add_handler(LogPointPrint(INFO,sys.stdout))
    
    with wrapper("{filename}:{lineno} {message}"):
        LogHello()

    add_handler(print_repr)

    main()
    LogHello()
    
