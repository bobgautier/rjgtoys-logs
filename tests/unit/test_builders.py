"""
test the builders
"""

from rjgtoys.logs.logpoint.core import LogPoint,build_pid,build_ugid,build_time,build_bigpid, Builders

from mock import patch, Mock

from contextlib import nested

def test_builders():
    with nested(
        patch('os.getpid', Mock(return_value=123)),
        patch('os.getppid', Mock(return_value=122)),
        patch('os.getuid', Mock(return_value=234)),
        patch('os.geteuid', Mock(return_value=235)),
        patch('os.getgid', Mock(return_value=345)),
        patch('os.getegid', Mock(return_value=346)),
        patch('time.time', Mock(return_value=999))
        ):
        lpt = Mock()
        Builders.extend((build_pid,build_ugid,build_time,build_bigpid))
        
        Builders(lpt)
        
    assert lpt.pid == 123
    assert lpt.ppid == 122
    
    assert lpt.uid == 234
    assert lpt.euid == 235
    assert lpt.gid == 345
    assert lpt.egid == 346
    
    assert lpt.time == 999
    
    assert lpt.bigpid == hex(999*123)[2:] 
        
