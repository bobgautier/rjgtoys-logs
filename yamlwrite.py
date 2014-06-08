import yaml
import gzip

class YamlWriter:
    
    def __init__(self,path="log.yaml.gz"):
        self.f = gzip.GzipFile(fileobj=open(path,"a"))

    def write(self,**d):
        yaml.dump(d,stream=self.f,explicit_start=True, default_flow_style=True)

    def close(self):
        self.f.close()
        
j = YamlWriter()
j.write(a=2,b='abc')
j.write(x='x',y=[1,2,3])
j.close()

