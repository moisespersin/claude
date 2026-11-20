import numpy as np, math, sys
from PIL import Image, ImageFilter
sys.path.insert(0,'/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad')
from feed34_tom import tom, P3      # fundo no tom #C7CDD3, paciente na cor original
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
P=1000
def expandir(im):
    """Estende a foto em todas as bordas continuando parede/camiseta, sem mexer no original."""
    a=np.asarray(im).astype(float)
    e=np.pad(a,((P,P),(P,P),(0,0)),mode='edge')
    b=np.stack([np.asarray(Image.fromarray(e[...,c].astype('uint8')).filter(ImageFilter.GaussianBlur(60))).astype(float) for c in range(3)],-1)
    H,W=a.shape[:2]; yy,xx=np.mgrid[0:H+2*P,0:W+2*P]
    d=np.maximum.reduce([P-yy,yy-(H+P-1),P-xx,xx-(W+P-1),np.zeros_like(yy)]).astype(float)
    w=np.clip(d/40,0,1)[...,None]               # funde 40 px a partir da borda real
    out=e*(1-w)+b*w+np.random.default_rng(3).normal(0,1.2,e.shape)*w
    # embaixo: espelha a camiseta (mantém a textura do tecido), fundindo 60 px na emenda
    r=np.pad(a,((0,P),(P,P),(0,0)),mode='symmetric')[H:]
    t=np.clip((np.arange(P)/60.0),0,1)[:,None,None]
    out[H+P:]=r*1.0
    out[P:P+H,P:P+W]=a
    return Image.fromarray(np.clip(out+0.5,0,255).astype('uint8'))
before,after=expandir(tom('18.jpg')),expandir(tom('19.jpg'))
CW,H=540,1350                                  # feed 4:5, antes à esquerda e depois à direita
A_L,A_R=(430,1117),(625,1127); D_L,D_R=(380,1235),(610,1243)
mid=lambda p,q: ((p[0]+q[0])/2,(p[1]+q[1])/2); ang=lambda p,q: math.atan2(q[1]-p[1],q[0]-p[0])
mA,mD=mid(A_L,A_R),mid(D_L,D_R); k=1.15; th=ang(A_L,A_R)-ang(D_L,D_R)
BW=int(sys.argv[1]) if len(sys.argv)>1 else 1250; BH=round(BW*H/CW)
BX=int(sys.argv[2]) if len(sys.argv)>2 else 85; BY=int(sys.argv[3]) if len(sys.argv)>3 else -78
mA=(mA[0]+P,mA[1]+P); mD=(mD[0]+P,mD[1]+P); BX+=P; BY+=P
a_,b_=math.cos(th)/k,-math.sin(th)/k; d_,e_=-b_,a_
cx=mA[0]+a_*(BX-mD[0])+b_*(BY-mD[1]); cy=mA[1]+d_*(BX-mD[0])+e_*(BY-mD[1])
L=before.transform((BW,BH),Image.AFFINE,(a_,b_,cx,d_,e_,cy),resample=Image.BICUBIC)
R=after.crop((BX,BY,BX+BW,BY+BH))
img=Image.new('RGB',(CW*2,H)); img.paste(L.resize((CW,H),Image.LANCZOS),(0,0)); img.paste(R.resize((CW,H),Image.LANCZOS),(CW,0))
img.save(SP+'entregas/feed-4x5-lado-a-lado-C7CDD3.png',icc_profile=P3); print(img.size)
