
import sys

from rjgtoys.logs import getLogger, LogPoint, LogPointPrint, LogPointJSON, INFO, ERROR, append_action, wrapping, log_pid, log_time

class LogHello(LogPoint):
    level = INFO
    text = "Hello logging"


def main():
    with wrapping("** {logpoint} {message} **"):
        with wrapping("{module}:{function} {message}"):
            LogHello()

if __name__ == "__main__":
    
    append_action(log_pid)
    append_action(log_time)
    append_action(LogPointJSON(ERROR,sys.stdout))
    append_action(LogPointJSON(INFO,sys.stdout))
    append_action(LogPointPrint(INFO,sys.stdout))
    
    with wrapping("{filename}:{lineno} {message}"):
        LogHello()

    main()
    LogHello()
    
