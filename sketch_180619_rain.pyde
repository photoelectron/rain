import itertools

N_PHI = 300; N_save = N_PHI
fc = 1
wd = 1080/fc; ht = 1080/fc

ns = 3e-2
nt = 3e-1

def settings():
    size(wd,ht,P3D)

def setup():
    global water
    colorMode(HSB,1.)
    background(0)
    water = grid(PVector(50,50),PVector(wd,wd))
    camera(width*1.5,height/2.,-width*.5,width/2.,height/2.*0,height/2.,0,-1,0)

def draw():
    background(0)
    translate(0,height/2.*0)
    water.update()
    water.show()
    ### CAMERA
    # cx = map(cos(TWO_PI*frameCount/N_PHI),-1,1,-width*.5,width*1.5)
    # cz = map(sin(TWO_PI*frameCount/N_PHI),-1,1,-height*.5,height*1.5)
    # camera(cx,height/2.,cz,width/2.,height/2.*0,height/2.,0,-1,0)

##########################

class pt():
    def __init__(self,pos,v,c):
        self.pos = pos
        self.v = v
        self.a = 0
        self.c = c
    
    def addF(self,F):
        self.a += F
    
    def update(self):
        self.v += self.a
        self.pos.y += self.v
        self.v *= .95
        self.a = 0

class grid():
    def __init__(self,n,sz):
        self.n = n
        self.sz = sz
        self.g = []
        self.gstiff = .001
        self.pstiff = .005
        for i, j in itertools.product(xrange(self.n.x), xrange(self.n.y)):
            x = map(i,0,self.n.x,0,self.sz.x)
            z = map(j,0,self.n.y,0,self.sz.y)
            pos = PVector(x,0,z)
            h = .6
            c = color(h,1,1)
            v = 0
            p = pt(pos,v,c)
            self.g.append(p)
    
    def show(self):
        for i in xrange(len(self.g)):
            x = i%int(self.n.x)
            y = i/int(self.n.x)
            xp = x+1
            yp = y+1
            ym = y-1
            if xp < self.n.x:
                ### diags
                # if yp < self.n.y:
                #     ipp = xp + yp*int(self.n.x)
                #     line(self.g[i].pos.x,self.g[i].pos.y,self.g[i].pos.z,
                #          self.g[ipp].pos.x,self.g[ipp].pos.y,self.g[ipp].pos.z)
                # if ym >= 0:
                #     ipm = xp + ym*int(self.n.x)
                #     line(self.g[i].pos.x,self.g[i].pos.y,self.g[i].pos.z,
                #          self.g[ipm].pos.x,self.g[ipm].pos.y,self.g[ipm].pos.z)
                ipo = xp + y*int(self.n.x)
                c = lerpColor(self.g[i].c,self.g[ipo].c,.5)
                stroke(c)
                line(self.g[i].pos.x,self.g[i].pos.y,self.g[i].pos.z,
                         self.g[ipo].pos.x,self.g[ipo].pos.y,self.g[ipo].pos.z)
            if yp < self.n.y:
                iop = x + yp*int(self.n.x)
                c = lerpColor(self.g[i].c,self.g[iop].c,.5)
                stroke(c)
                line(self.g[i].pos.x,self.g[i].pos.y,self.g[i].pos.z,
                         self.g[iop].pos.x,self.g[iop].pos.y,self.g[iop].pos.z)
    
    def update(self):
        ### DROPS
        tg = self.g[:]
        for i in xrange(len(self.g)):
            z = self.g[i].pos.y
            x = i%int(self.n.x)
            y = i/int(self.n.x)
            xp = x+1; xm = x-1
            yp = y+1; ym = y-1
            if xm >= 0 and ym >= 0 and xp < self.n.x and yp < self.n.y:
                ixm = xm + y*int(self.n.x)
                dz = self.g[ixm].pos.y - z
                F = dz*self.pstiff
                self.g[i].addF(F)
            
                ixp = xp + y*int(self.n.x)
                dz = self.g[ixp].pos.y - z
                F = dz*self.pstiff
                self.g[i].addF(F)
                
                iym = x + ym*int(self.n.x)
                dz = self.g[iym].pos.y - z
                F = dz*self.pstiff
                self.g[i].addF(F)
                
                iyp = x + yp*int(self.n.x)
                dz = self.g[iyp].pos.y - z
                F = dz*self.pstiff
                self.g[i].addF(F)
                
                if random(0,1) < 0.000025: self.g[i].addF(random(-15,-3))            
            dz = 0 - z
            F = dz*self.gstiff
            self.g[i].addF(F)
            
            tg[i].update()
            h = map(self.g[i].pos.y,-5,5,.3,.8)
            self.g[i].c = color(h,1,1)
        self.g = tg[:]
       
            
        ### PERLIN
        # t = TWO_PI*frameCount/N_PHI
        # for i in xrange(len(self.g)):
        #     x = i%self.n.x
        #     z = i/self.n.x
        #     # y = map(noise(x*ns+t*nt,z*ns+t*nt,t*nt),0,.8,-height*.1,height*.1)
        #     # h = map(y,-height*.1,height*.1,.49,.7)
        #     self.g[i].pos.y = 0
        #     self.g[i].c = color(.6,1,1)
