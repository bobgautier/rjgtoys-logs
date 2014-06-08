import json
import gzip

from filters import SimpleFilter,EQ, NOT

class JsonReader(object):
    
    def __init__(self,path="log.json.gz"):
        self.f = gzip.GzipFile(fileobj=open(path,"r"))

    def read(self):
        n = int(self.f.readline().strip())
        s = self.f.read(n)
        nl = self.f.read(1) # skip newline
        d = json.loads(s)
        return d

    def find_all(self):
        while True:
            try:
                yield self.read()
            except:
                break

    def find(self,filter=None):
        if filter:
            p = SimpleFilter(filter)
        else:
            p = None
            
        for r in self.find_all():
            if (p is None) or p.match(r):
                yield r
        
    def close(self):
        self.f.close()
        
j = JsonReader()

f = NOT(EQ('a',2))

for r in j.find(f):
    print r

j.close()

