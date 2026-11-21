import numpy as np, math, io, sys
from PIL import Image, ImageCms
sys.path.insert(0,'/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad'); from cor import abrir, P3
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
OUT=SP+'entregas/'
# cor-base #C7CDD3 (sRGB) convertida para Display P3, o perfil de trabalho
px=Image.new('RGB',(1,1),(0xC7,0xCD,0xD3))
px=ImageCms.profileToProfile(px,ImageCms.createProfile('sRGB'),ImageCms.ImageCmsProfile(io.BytesIO(P3)),outputMode='RGB')
C=np.array(px.getpixel((0,0)),float)/255
lum=lambda x: x[...,0]*0.2126+x[...,1]*0.7152+x[...,2]*0.0722
import os
ESCURO=float(os.environ.get('ESCURO','1'))   # <1 escurece só o fundo
def tom(f):  # teste 1: só o fundo ganha o tom; paciente fica com a cor original
    I=np.asarray(abrir(f)).astype(float)/255
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)[...,None]/255
    G=np.clip(lum(I)[...,None]*C/lum(C)*ESCURO,0,1)
    return Image.fromarray((np.clip(I*a+G*(1-a),0,1)*255+0.5).astype('uint8'))
if __name__=='__main__':
    W,PH=1080,675
    A_L,A_R=(430,1117),(625,1127); D_L,D_R=(380,1235),(610,1243)
    mid=lambda p,q: ((p[0]+q[0])/2,(p[1]+q[1])/2); ang=lambda p,q: math.atan2(q[1]-p[1],q[0]-p[0])
    mA,mD=mid(A_L,A_R),mid(D_L,D_R); k=1.15; th=ang(A_L,A_R)-ang(D_L,D_R)
    BX,BY,BW=0,990,1450; BH=round(BW*PH/W)
    before,after=tom('18.jpg'),tom('19.jpg')
    a_,b_=math.cos(th)/k,-math.sin(th)/k; d_,e_=-b_,a_
    cx=mA[0]+a_*(BX-mD[0])+b_*(BY-mD[1]); cy=mA[1]+d_*(BX-mD[0])+e_*(BY-mD[1])
    top=before.transform((BW,BH),Image.AFFINE,(a_,b_,cx,d_,e_,cy),resample=Image.BICUBIC)
    bot=after.crop((BX,BY,BX+BW,BY+BH))
    img=Image.new('RGB',(W,PH*2)); img.paste(top.resize((W,PH),Image.LANCZOS),(0,0)); img.paste(bot.resize((W,PH),Image.LANCZOS),(0,PH))
    img.save(OUT+'feed-4x5-perfil-34-C7CDD3.png',icc_profile=P3); print(img.size)
