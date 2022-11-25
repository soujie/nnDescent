from joblib  import delayed , Parallel
import random
import time 
import copy

test = {k:random.sample(range(10),5) for k in range(100000)}

def fn1(test):
    t1 = time.time()
    for i in range(len(test)):
        test[i] = random.sample(test[i],2)
    print(f'raw {time.time()-t1}')

def fn2(k,v):
    v = random.sample(v,2)
    return (k,v)

fn1(copy.deepcopy(test))

t1 = time.time()
pool = Parallel(5)
out = pool(delayed(fn2)(k,v) for k,v in test.items())
print(time.time()-t1)
    
