import random

def SEED(seed = None):
    if seed == None:
        return int((abs(random.random()) % 1) * 10**9)
    else: 
        random.seed(seed)
        return int((abs(random.random()) % 1) * 10**9)
        