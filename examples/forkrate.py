import time
import os
import sys

t = time.time()

t1 = t+10

nf = 0
while time.time() < t1:
    nf += 1
    p = os.fork()
    
    if p == 0:
        sys.exit(0)

    os.wait()
    
print nf
