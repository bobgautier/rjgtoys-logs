
# 'spare' bits of code that are not needed (yet)

class LogActionGroup(dict,LogAction):
    """
    A set of actions to be taken when
    processing a :class:`LogPoint`.
    Each action has a name.
    """
    
    def __init__(self,**actions):
        dict.__init__(self,**actions)

    def match(self,lpt):
        if not self.match_group(lpt):
            return False

        for (n,a) in self.iteritems():
            try:
                if a.match(lpt):
                    return True
            except:
                return True
        return False

    def match_group(self,lpt):
        return True

    def act(self,lpt):
        for n,a in self.iteritems():
            a(lpt)


import json

class PrintJSONHandler(PrintHandler):
    
    def act(self,lpt):
        print >>self.stream, json.dumps(lpt.dict())

class PrintReprHandler(PrintHandler):
    """ An action that prints the ``repr()`` of the logpoint """

    def act(self,lpt):
        print repr(lpt)
