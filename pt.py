class pt():
    def __init__(self,pos,v,c,tstep):
        self.pos = pos
        self.v = v
        self.a = 0
        self.c = c
        self.tstep = tstep
    
    def addF(self,F):
        self.a += F
    
    def update(self):
        self.v += self.a
        self.v *= .975
        self.pos.y += self.v*self.tstep
        self.a = 0
