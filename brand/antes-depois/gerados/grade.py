import numpy as np
from PIL import Image, ImageDraw, ImageFont
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/testes-tom/'
import os; os.makedirs(OUT,exist_ok=True)
hx=lambda h: np.array([int(h[i:i+2],16) for i in (0,2,4)],float)/255
P={k:hx(k) for k in ['EDF0F0','C7CDD3','9198A0','454953','1F2228']}
def lum(x): return x[...,0]*0.2126+x[...,1]*0.7152+x[...,2]*0.0722
def tint(L,c):  # cor da paleta com a luminosidade original (modo "cor")
    return np.clip(L[...,None]*c/lum(c),0,1)
def overlay(b,c): return np.where(b<0.5,2*b*c,1-2*(1-b)*(1-c))
def softlight(b,c): return (1-2*c)*b*b+2*c*b
def gmap(L,stops):
    xs=np.linspace(0,1,len(stops)); cs=np.array([P[s] for s in stops])
    return np.stack([np.interp(L,xs,cs[:,i]) for i in range(3)],-1)
T={
 '1-cor-C7CDD3':     lambda x,L: tint(L,P['C7CDD3']),
 '2-overlay-C7CDD3': lambda x,L: overlay(L[...,None],P['C7CDD3']),
 '3-softlight-9198A0':lambda x,L: softlight(L[...,None],P['9198A0']),
 '4-mapa-paleta':    lambda x,L: gmap(L,['1F2228','454953','9198A0','C7CDD3','EDF0F0']),
 '5-mapa-escuro':    lambda x,L: gmap(L,['1F2228','454953','9198A0']),
 '6-pb-neutro':      lambda x,L: np.repeat(L[...,None],3,-1),
}
H=1960; CW=int(H*0.4)
crops=[('11.jpg',88,0),('12.jpg',63,40)]
srcs=[]
for f,x0,y0 in crops:
    im=Image.open(IMG+f); icc=im.info.get('icc_profile')
    I=np.asarray(im.convert('RGB')).astype(float)/255
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)/255
    sl=(slice(y0,y0+H),slice(x0,x0+CW)); srcs.append((I[sl],a[sl][...,None]))
logo=Image.open('/home/user/claude/brand/antes-depois/gerados/assinatura-provisoria.png'); lw=200
logo=logo.resize((lw,int(logo.height*lw/logo.width)),Image.LANCZOS)
thumbs=[]
for name,fn in T.items():
    cols=[]
    for I,a in srcs:
        L=lum(I); G=fn(I,L)
        cols.append(I*a+G*(1-a))
    out=np.concatenate(cols,1)
    img=Image.fromarray((np.clip(out,0,1)*255+0.5).astype('uint8'))
    img.paste((255,255,255),(img.width-lw-45,img.height-logo.height-55),logo)
    img.save(OUT+name+'.png',icc_profile=icc)
    thumbs.append((name,img.resize((392,490),Image.LANCZOS)))
sheet=Image.new('RGB',(3*392+40,2*(490+40)+10),(237,240,240)); d=ImageDraw.Draw(sheet)
fnt=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf',22)
for i,(n,t) in enumerate(thumbs):
    x=10+(i%3)*(392+10); y=10+(i//3)*(490+45)
    sheet.paste(t,(x,y)); d.text((x,y+495),n,font=fnt,fill=(31,34,40))
sheet.save(OUT+'00-comparativo.png'); print(img.size)
