def hloop(h):
    return h - floor(h)

def sign(k):
    if k >= 0: return 1
    else: return -1

def ploop(i,r):
    if not(0 <= i < r):
        return i - r*sign(i)
    else: return i
