import json
import gzip

class JsonWriter:
    
    def __init__(self,path="log.json.gz"):
        self.f = gzip.GzipFile(fileobj=open(path,"a"))

    def write(self,**d):
        s = json.dumps(d)
        n = len(s)
        self.f.write("%s\n" % n)
        self.f.write("%s\n"% s)

    def close(self):
        self.f.close()
        
j = JsonWriter()
j.write(a=2,b='abc')
j.write(x='x',y=[1,2,3])
j.close()

