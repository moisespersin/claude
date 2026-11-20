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
# pontos que não mudam com o procedimento: pupilas, ponta do nariz, orelha e queixo
A=np.array([(427,1115),(643,1130),(385,1295),(1090,1250),(535,1670)],float)  # antes
D=np.array([(377,1232),(605,1238),(310,1415),(1112,1430),(400,1850)],float)  # depois
# transformação de similaridade (escala, rotação, deslocamento) por mínimos quadrados: depois -> antes
Dc,Ac=D-D.mean(0),A-A.mean(0)
zD=Dc[:,0]+1j*Dc[:,1]; zA=Ac[:,0]+1j*Ac[:,1]
m=(np.conj(zD)@zA)/(np.conj(zD)@zD)                 # escala*e^(i*ângulo)
res=np.abs(zA-m*zD); print('escala',round(abs(m),3),'graus',round(math.degrees(math.atan2(m.imag,m.real)),2),'erro px',res.round(1))
BW=int(sys.argv[1]) if len(sys.argv)>1 else 1120; BH=round(BW*H/CW)
BX=int(sys.argv[2]) if len(sys.argv)>2 else 240; BY=int(sys.argv[3]) if len(sys.argv)>3 else 330
a_,b_,d_,e_=m.real,-m.imag,m.imag,m.real
# antes(x,y) = A.mean + m*((x,y)-D.mean), com tudo deslocado pela margem P
cx=A.mean(0)[0]+P+a_*(BX-D.mean(0)[0])+b_*(BY-D.mean(0)[1]); cy=A.mean(0)[1]+P+d_*(BX-D.mean(0)[0])+e_*(BY-D.mean(0)[1])
BX+=P; BY+=P
L=before.transform((BW,BH),Image.AFFINE,(a_,b_,cx,d_,e_,cy),resample=Image.BICUBIC)
R=after.crop((BX,BY,BX+BW,BY+BH))
img=Image.new('RGB',(CW*2,H)); img.paste(L.resize((CW,H),Image.LANCZOS),(0,0)); img.paste(R.resize((CW,H),Image.LANCZOS),(CW,0))
img.save(SP+'entregas/feed-4x5-lado-a-lado-C7CDD3.png',icc_profile=P3); print(img.size)
