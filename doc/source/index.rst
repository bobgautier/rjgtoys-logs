Logs: Extended Logging Interface
================================

.. automodule:: rjgtoys.logs
   
Example
-------

The following simple program demonstrates how to use this module::


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

Output::
    
    $ python example.py 
    2014-04-28 19:38:27,005 INFO: Starting up
    $ python example.py --verbose
    2014-04-28 19:38:33,119 INFO: Starting up
    2014-04-28 19:38:33,122 INFO: You'll only see this if --verbose was used
    $ python example.py --debug
    2014-04-28 19:38:36,807 INFO: Starting up
    2014-04-28 19:38:36,810 DEBUG: You'll only see this if --debug was used
    $ python example.py --debug --verbose
    2014-04-28 19:38:40,755 INFO: Starting up
    2014-04-28 19:38:40,758 INFO: You'll only see this if --verbose was used
    2014-04-28 19:38:40,758 DEBUG: You'll only see this if --debug was used
     
    
To Do
=====

There is currently no way to configure the output format

Add more options, to control output file(s), --quiet

