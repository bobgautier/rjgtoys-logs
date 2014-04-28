# example.py

from rjgtoys.logs import getLogger

from argparse import ArgumentParser

log = getLogger(__name__)

def main(argv):
    log.info("Starting up")
    
    p = ArgumentParser()
    
    log.add_options(p)
    
    opts = p.parse_args(argv)
    
    log.handle_options(opts)
    
    log.verbose("You'll only see this if --verbose was used")
    log.debug("You'll only see this if --debug was used")
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
