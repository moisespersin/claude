import numpy as np, math, sys
from PIL import Image, ImageFilter
sys.path.insert(0,'/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad')
from feed34_tom import tom, P3      # fundo no tom #C7CDD3, paciente na cor original
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
P=1000
def expandir(im):
    """Estende a foto continuando parede/camiseta sem listras; o rosto não é tocado."""
    a=np.asarray(im).astype(float); H,W=a.shape[:2]
    S=np.stack([np.asarray(Image.fromarray(a[...,c].astype('uint8')).filter(ImageFilter.GaussianBlur(30))).astype(float) for c in range(3)],-1)
    out=np.pad(S,((P,P),(P,P),(0,0)),mode='edge')
    out[H+P:]=np.pad(a,((0,P),(P,P),(0,0)),mode='symmetric')[H:]   # embaixo: espelha a camiseta
    # dentro da foto, as últimas 40 px de parede fundem suavemente com a extensão
    yy,xx=np.mgrid[0:H,0:W]; d=np.minimum.reduce([yy,xx,W-1-xx]).astype(float)
    w=np.clip(d/40,0,1)[...,None]
    out[P:P+H,P:P+W]=a*w+S*(1-w)
    out+=np.random.default_rng(3).normal(0,1.0,out.shape)*(1-np.pad(np.ones((H,W,1)),((P,P),(P,P),(0,0))))
    return Image.fromarray(np.clip(out+0.5,0,255).astype('uint8'))
before,after=expandir(tom('26.jpg')),expandir(tom('27.jpg'))
W,PH=1080,675                                   # feed 4:5, antes em cima e depois embaixo
# pupila, ponta do nariz, orelha, sobrancelha, queixo (px da foto original)
A=np.array([(605,1224),(869,1204),(502,1752),(554,1133),(1088,1481)],float)   # antes
D=np.array([(567,1133),(837,1108),(451,1662),(515,1030),(1063,1391)],float)  # depois
Dc,Ac=D-D.mean(0),A-A.mean(0); zD=Dc[:,0]+1j*Dc[:,1]; zA=Ac[:,0]+1j*Ac[:,1]
m=(np.conj(zD)@zA)/(np.conj(zD)@zD)
print('escala',round(abs(m),3),'graus',round(math.degrees(math.atan2(m.imag,m.real)),2),'erro',np.abs(zA-m*zD).round(1))
BW=int(sys.argv[1]); BH=round(BW*PH/W); BX=int(sys.argv[2]); BY=int(sys.argv[3])
a_,b_,d_,e_=m.real,-m.imag,m.imag,m.real
cx=A.mean(0)[0]+P+a_*(BX-D.mean(0)[0])+b_*(BY-D.mean(0)[1]); cy=A.mean(0)[1]+P+d_*(BX-D.mean(0)[0])+e_*(BY-D.mean(0)[1])
BX+=P; BY+=P
T=before.transform((BW,BH),Image.AFFINE,(a_,b_,cx,d_,e_,cy),resample=Image.BICUBIC)
B=after.crop((BX,BY,BX+BW,BY+BH))
img=Image.new('RGB',(W,PH*2)); img.paste(T.resize((W,PH),Image.LANCZOS),(0,0)); img.paste(B.resize((W,PH),Image.LANCZOS),(0,PH))
img.save(SP+'entregas/feed-4x5-perfil-deitado-empilhado-C7CDD3.png',icc_profile=P3); print(img.size)
