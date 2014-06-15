"""

Tests on LogAction and friends

"""

from rjgtoys.logs.logpoint.core import LogAction, LogActionList

from mock import Mock

def test_logaction_base_for_coverage():
    
    a = LogAction()
    lpt = Mock()
    
    a(lpt)
    

def test_logactionlist_ops():
    
    ll = LogActionList()
    
    # Basic list-like properties
    
    assert len(ll) == 0
    
    assert not ll
    
    ll.append(5)
    
    assert ll == [5]
    
    ll.prepend(4)
    
    assert ll == [4,5]
    
    # add to end
    
    ll.add_after((8,9))
    
    assert ll == [4,5,8,9]
    
    ll.add_before((1,2))
    
    assert ll == [1,2,4,5,8,9]
    
    ll.add_before((3,),before=4)
    
    assert ll == [1,2,3,4,5,8,9]
    
    ll.add_after((6,),after=5)
    
    assert ll == [1,2,3,4,5,6,8,9]
    
    with ll.use_after((7,),after=6):
        assert ll == [1,2,3,4,5,6,7,8,9]
    
    assert ll == [1,2,3,4,5,6,8,9]
    
    with ll.use_before((7,),before=8):
        assert ll == [1,2,3,4,5,6,7,8,9]
    
    assert ll == [1,2,3,4,5,6,8,9]
    
def test_logactionlist_discard():
    """ Test discard and implicitly, remove """
    
    ll = LogActionList()
    
    assert not ll
    
    ll.append(2)
    ll.prepend(1)
    
    assert ll == [1,2]
    
    ll.discard(3)   # does not raise
    
    assert ll == [1,2]
    
    ll.discard(1)
    
    assert ll == [2]
    
    ll.append(2)
    assert ll == [2,2]  # duplicate
    
    ll.discard(2)
    
    assert ll == []     # All occurences gone

