import numpy as np, sys
from PIL import Image, ImageFilter
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/'
hexc=sys.argv[1] if len(sys.argv)>1 else 'C7CDD3'
BG=np.array([int(hexc[i:i+2],16) for i in (0,2,4)],float)
CW,H,TOP,SH=900,2250,290,1960
W=CW*2
def blur_fill(I,m,r):
    w=np.asarray(Image.fromarray((m*255).astype('uint8')).filter(ImageFilter.GaussianBlur(r))).astype(float)/255
    ch=[np.asarray(Image.fromarray((I[...,c]*m).astype('uint8')).filter(ImageFilter.GaussianBlur(r))).astype(float) for c in range(3)]
    return np.stack(ch,2)/np.maximum(w[...,None],1e-3)
# fundo: cor base com luz suave atrás das cabeças e leve vinheta, mais grão fino
yy,xx=np.mgrid[0:H,0:W].astype(float)
g=np.zeros((H,W))
for cx in (CW*0.5,CW*1.5):
    g+=np.exp(-(((xx-cx)/700)**2+((yy-H*0.36)/900)**2))
g=g/g.max()
v=np.sqrt(((xx-W/2)/(W*0.75))**2+((yy-H*0.45)/(H*0.75))**2)
shade=1+0.035*g-0.06*np.clip(v,0,1)**2
rng=np.random.default_rng(7)
N=BG[None,None,:]*shade[...,None]+rng.normal(0,1.6,(H,W,1))
canvas=N.copy()
for k,(f,x0,y0) in enumerate([('11.jpg',60,0),('12.jpg',40,40)]):
    src=Image.open(IMG+f); icc=src.info.get('icc_profile')
    I=np.asarray(src.convert('RGB')).astype(float)
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)/255
    B=blur_fill(I,a<0.03,30); B2=blur_fill(I,a<0.03,150)
    w=np.asarray(Image.fromarray(((a<0.03)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(30))).astype(float)/255
    B=np.where(w[...,None]>0.08,B,B2)
    sl=(slice(y0,y0+SH),slice(x0,x0+CW))
    Ic,ac,Bc=I[sl],a[sl][...,None],B[sl]
    Nc=N[TOP:TOP+SH,k*CW:(k+1)*CW]
    Ff=blur_fill(I,a>0.97,12)[sl]
    Fd=np.clip((Ic-(1-ac)*Bc)/np.maximum(ac,1e-3),0,255)
    t=np.clip((ac-0.35)/0.4,0,1)
    F=t*Fd+(1-t)*Ff
    canvas[TOP:TOP+SH,k*CW:(k+1)*CW]=ac*F+(1-ac)*Nc
img=Image.fromarray(np.clip(canvas+0.5,0,255).astype('uint8'))
logo=Image.open(OUT+'assinatura-provisoria.png'); lw=230
logo=logo.resize((lw,int(logo.height*lw/logo.width)),Image.LANCZOS)
img.paste((255,255,255),(W-lw-50,H-logo.height-60),logo)
name=OUT+f'antes-depois-4x5-{hexc}'
img.save(name+'.png',icc_profile=icc); img.save(name+'.jpg',quality=100,subsampling=0,icc_profile=icc)
print(img.size)
