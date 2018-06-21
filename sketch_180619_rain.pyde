from rain import drop
from grid import grid

N_PHI = 1500; N_save = N_PHI
fc = 2
wd = 1080/fc; ht = 1080/fc
dropF = -300
tstep = 1e-1

def settings():
    size(wd,ht,P3D)

def setup():
    global water,dro
    frameRate(10)
    colorMode(HSB,1.)
    background(0)
    water = grid(PVector(30,30),PVector(wd,wd),tstep)
    cx = map(cos(TWO_PI*0),-1,1,-height*.5,height*1.5)
    cz = map(sin(TWO_PI*0),-1,1,-height*.5,height*1.5)
    camera(cx,height/2.,cz,
           width/2.,0,height/2.,0,-1,0)
    dro = drop(PVector(width/2.,540,height/2.),PVector(0,0,0),5)

def draw():
    background(0)
    dro.update()
    dro.show()
    dro.addF(PVector(0,-.1,0))
    water.update()
    water.show()
    stroke(1)
    line(dro.pos.x,dro.pos.y,dro.pos.z,width/2.,0,height/2.)
    ### CAMERA
    # cx = map(cos(TWO_PI*frameCount/N_PHI),-1,1,-width*.5,width*1.5)
    # cz = map(sin(TWO_PI*frameCount/N_PHI),-1,1,-height*.5,height*1.5)
    # camera(cx,height/2.,cz,width/2.,height/2.*0,height/2.,0,-1,0)

###

def hloop(h):
    return h - floor(h)

def sign(k):
    if k >= 0: return 1
    else: return -1

def ploop(i,r):
    if not(0 <= i < r):
        return i - r*sign(i)
    else: return i

def mouseClicked():
    water.drop(mouseX,mouseY,dropF)
    
def mouseWheel(event):
    global dropF
    dropF += event.getCount()
    print dropF
