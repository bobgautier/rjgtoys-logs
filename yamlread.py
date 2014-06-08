import yaml
import gzip

from filters import Filter, SimpleFilter,EQ, NOT

class YamlReader(object):
    
    def __init__(self,path="log.yaml.gz"):
        self.f = gzip.GzipFile(fileobj=open(path,"r"))

    def find_all(self):
        return yaml.load_all(stream=self.f)
        
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
        
j = YamlReader()

f = NOT(EQ('a',2))

ff = f.to_yaml()
print ff
g = Filter.from_yaml(ff)

print g.to_yaml()

for r in j.find(g):
    print r

j.close()

