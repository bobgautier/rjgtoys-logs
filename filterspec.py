
import yaml

info = ['EQ','level','INFO']
role = ['EQ','role','USER']

spec = ['AND',info,role]

sy = yaml.dump(spec)

print sy

sp = yaml.load(sy)

print sp
