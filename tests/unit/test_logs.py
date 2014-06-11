
import rjgtoys.logs.core as logs

from argparse import ArgumentParser

def check_verbose(log):
    orig = log.set_verbose()
    assert log.set_verbose() is orig   # no change
    
    assert log.set_verbose(not orig) is orig # return prev
    
    assert log.set_verbose() is not orig # change was made

def check_debug(log):
    orig = log.set_debug()
    assert log.set_debug() is orig   # no change
    
    assert log.set_debug(not orig) is orig # return prev
    
    assert log.set_debug() is not orig # change was made

def test_set_verbose():
    check_verbose(logs)
    
    inst = logs.getLogger('__main__')
    
    check_verbose(inst)
    
def test_set_debug():
    check_debug(logs)
    
    inst = logs.getLogger('__main__')
    
    check_debug(inst)

def test_parse_args():
    
    log = logs.getLogger('__main__')
    
    p = ArgumentParser()
    
    log.add_options(p)
    
    opts = p.parse_args([])
    assert opts._logdebug is None
    assert opts._logverbose is None
    
    log.set_debug(False)
    log.set_verbose(False)
    
    log.handle_options(opts)
    
    assert log.set_debug() is False     # Oddly written to echo the set() calls above
    assert log.set_verbose() is False
    
    opts = p.parse_args(['--verbose','--debug'])
    
    assert opts._logverbose
    assert opts._logdebug
    
    log.handle_options(opts)
    
    assert log.set_verbose()
    assert log.set_debug()

def test_logging():
    
    log = logs.getLogger('__main__')
    
    log.set_verbose(False)
    log.verbose('Eaten')
    log.set_verbose(True)
    log.verbose('Not eaten')
    
    log.set_debug(False)
    log.debug('Eaten')
    log.set_debug(True)
    log.debug('Not eaten')

    # FIXME: check that the output is what we expect
    
