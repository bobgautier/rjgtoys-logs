
import sys

from rjgtoys.logs import getLogger
from rjgtoys.logs.logpoint.core import LogPoint, LogPointPrint, LogPointJSON, INFO, ERROR, add_handler, add_builder, wrapper, log_pid, log_time, log_bigpid

class LogHello(LogPoint):
    level = INFO
    text = "Hello logging"


def main():
    with wrapper("** {logpoint} {message} **"):
        with wrapper("{module}:{function} {message}"):
            LogHello()

if __name__ == "__main__":

    add_builder(log_pid)
    add_builder(log_time)
    add_builder(log_bigpid)
    
    add_handler(LogPointJSON(ERROR,sys.stdout))
    add_handler(LogPointJSON(INFO,sys.stdout))
    add_handler(LogPointPrint(INFO,sys.stdout))
    
    with wrapper("{filename}:{lineno} {message}"):
        LogHello()

    main()
    LogHello()
    
