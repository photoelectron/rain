class drop():
    def __init__(self,pos,vel,r):
        self.pos = pos
        self.vel = vel
        self.acc = PVector(0,0,0)
        self.r = r
        self.pts = [self.pos for _ in xrange(10)]
        print pos
        print self.pts
    
    def show(self):
        stroke(.5,1,1)
        with beginShape():
            for i in xrange(10):
                R = map(i,0,10,1,self.r)
                strokeWeight(R)
                vertex(self.pts[i].x,self.pts[i].y)
    
    def addF(self,F):
        self.acc.add(F)
    
    def update(self):
        self.vel.add(self.acc)
        npos = PVector.add(self.pts[len(self.pts)-1],self.vel)
        self.pts.append(npos)
        self.pts.pop(0)
        self.acc.mult(0)
