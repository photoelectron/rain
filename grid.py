import itertools
from pt import pt
from funcs import hloop

dg = 2*1

class grid():
    def __init__(self,n,sz,tstep):
        self.n = n
        self.sz = sz
        self.g = []
        self.grad = PVector(0,0)
        self.gstiff = .05
        self.pstiff = .05
        for i, j in itertools.product(xrange(self.n.x), xrange(self.n.y)):
            x = map(i,0,self.n.x,0,self.sz.x)
            z = map(j,0,self.n.y,0,self.sz.y)
            pos = PVector(x,0,z)
            h = .6
            c = color(h,1,1)
            v = 0
            p = pt(pos,v,c,tstep)
            self.g.append(p)
    
    def show(self):
        strokeWeight(2)
        for i in xrange(len(self.g)):
            x = i%int(self.n.x)
            y = i/int(self.n.x)
            xp = x+1
            yp = y+1
            ym = y-1
            if xp < self.n.x:
                ### diags
                if yp < self.n.y:
                    ipp = xp + yp*int(self.n.x)
                    c = lerpColor(self.g[i].c,self.g[ipp].c,.5)
                    stroke(c)
                    line(self.g[i].pos.x,self.g[i].pos.y,self.g[i].pos.z,
                         self.g[ipp].pos.x,self.g[ipp].pos.y,self.g[ipp].pos.z)
                if ym >= 0:
                    ipm = xp + ym*int(self.n.x)
                    c = lerpColor(self.g[i].c,self.g[ipm].c,.5)
                    stroke(c)
                    line(self.g[i].pos.x,self.g[i].pos.y,self.g[i].pos.z,
                         self.g[ipm].pos.x,self.g[ipm].pos.y,self.g[ipm].pos.z)
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
            # xp = int(ploop(x+1,self.n.x)); xm = int(ploop(x-1,self.n.x))
            # yp = int(ploop(y+1,self.n.y)); ym = int(ploop(y-1,self.n.y))
            xp = int(constrain(x+1,0,self.n.x-1)); xm = int(constrain(x-1,0,self.n.x-1))
            yp = int(constrain(y+1,0,self.n.y-1)); ym = int(constrain(y-1,0,self.n.y-1))
            ### 4 NEIGHBOURS
            if xm >= 0 and ym >= 0 and xp < self.n.x and yp < self.n.y:
                ### RECTS
                imo = xm + y*int(self.n.x); dz = self.g[imo].pos.y - z
                F = dz*self.pstiff; self.g[i].addF(F)
            
                ipo = xp + y*int(self.n.x); dz = self.g[ipo].pos.y - z
                F = dz*self.pstiff; self.g[i].addF(F)
                
                iom = x + ym*int(self.n.x); dz = self.g[iom].pos.y - z
                F = dz*self.pstiff; self.g[i].addF(F)
                
                iop = x + yp*int(self.n.x); dz = self.g[iop].pos.y - z
                F = dz*self.pstiff; self.g[i].addF(F)
                ### DIAGS
                imm = xm + ym*int(self.n.x); dz = self.g[imm].pos.y - z
                F = dz*self.pstiff; self.g[i].addF(F)
                
                imp = xm + yp*int(self.n.x); dz = self.g[imp].pos.y - z
                F = dz*self.pstiff; self.g[i].addF(F)
                
                ipm = xp + ym*int(self.n.x); dz = self.g[ipm].pos.y - z
                F = dz*self.pstiff; self.g[i].addF(F)
                
                ipp = xp + yp*int(self.n.x); dz = self.g[ipp].pos.y - z
                F = dz*self.pstiff; self.g[i].addF(F)
                
                gradx = (self.g[ipo].pos.y-self.g[imo].pos.y)/dg
                grady = (self.g[iop].pos.y-self.g[iom].pos.y)/dg
                self.grad = PVector(gradx,grady)
                # if random(0,1) < 0.00005: self.g[i].addF(random(-15,-3))
                

            dz = 0 - z
            F = dz*self.gstiff
            self.g[i].addF(F)
            
            tg[i].update()
            h = map(self.g[i].pos.y,-300,30,.75,.7)
            # b = constrain(abs(map(self.g[i].pos.y,-3,3,-1,1)),0,1)
            b = map(self.grad.mag(),0,10,0,1)
            self.g[i].c = color(h,1,b)
            # stroke(1)
            # self.grad.div(100)
            # self.grad.setMag(constrain(self.grad.mag(),0,10))
            # line(self.g[i].pos.x,self.g[i].pos.y,self.g[i].pos.z,
            #      self.g[i].pos.x+self.grad.y,self.g[i].pos.y+self.grad.mag(),self.g[i].pos.z-self.grad.x)
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
    
    def drop(self,x,y,dF):
        # i = int(random(self.n.x)) + int(random(self.n.y)*self.n.x)
        i = int(map(x,0,width,0,self.n.x)) + int(int(map(y,0,height,0,self.n.y))*self.n.x)
        self.g[i].addF(dF)
