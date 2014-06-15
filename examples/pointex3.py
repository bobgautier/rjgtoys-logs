
import sys

from rjgtoys.logs.core import getLogger
from rjgtoys.logs.logpoint.core import LogPoint, PrintHandler, PrintJSONHandler, INFO, ERROR, Handlers, Builders, wrapper, build_pid, build_time, build_bigpid

class LogHello(LogPoint):
    level = INFO
    text = "Hello logging"


def main():
    with wrapper("** {logpoint} {message} **"):
        with wrapper("{module}:{function} {message}"):
            LogHello()

if __name__ == "__main__":

    Builders.extend((build_pid,build_time,build_bigpid))
    
    Handlers.extend((
        PrintJSONHandler(ERROR,sys.stdout),
        PrintJSONHandler(INFO,sys.stdout),
        PrintJSONHandler(INFO,sys.stdout)
    ))
    
    with wrapper("{filename}:{lineno} {message}"):
        LogHello()

    main()
    LogHello()
    
