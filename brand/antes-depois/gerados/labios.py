import numpy as np, math, sys
from PIL import Image
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/final/'
W,PH=1080,960                  # story 9:16, antes em cima e depois embaixo
# pontos fora da área tratada: canto da boca (comissura) e ponta do queixo, em px da foto original
A1,A2=(515,1519),(1313,1597)   # antes
D1,D2=(502,1545),(1275,1545)   # depois
gira=float(sys.argv[1]) if len(sys.argv)>1 else 1.0   # fração da correção de inclinação
dist=lambda p,q: math.hypot(q[0]-p[0],q[1]-p[1]); ang=lambda p,q: math.atan2(q[1]-p[1],q[0]-p[0])
k=dist(D1,D2)/dist(A1,A2)
th=(ang(A1,A2)-ang(D1,D2))*gira
BX,BY,BW=40,690,1360; BH=round(BW*PH/W)
before=Image.open(IMG+'20.jpg'); after=Image.open(IMG+'21.jpg'); icc=before.info.get('icc_profile')
c,s=math.cos(th)/k,math.sin(th)/k
a_,b_,d_,e_=c,-s,s,c
cx=A1[0]+a_*(BX-D1[0])+b_*(BY-D1[1]); cy=A1[1]+d_*(BX-D1[0])+e_*(BY-D1[1])
corners=[(cx+a_*u+b_*v, cy+d_*u+e_*v) for u,v in [(0,0),(BW,0),(0,BH),(BW,BH)]]
print('k',round(k,3),'graus',round(math.degrees(th),2),'cantos',[tuple(round(z) for z in p) for p in corners])
top=before.convert('RGB').transform((BW,BH),Image.AFFINE,(a_,b_,cx,d_,e_,cy),resample=Image.BICUBIC)
bot=after.convert('RGB').crop((BX,BY,BX+BW,BY+BH))
img=Image.new('RGB',(W,PH*2))
img.paste(top.resize((W,PH),Image.LANCZOS),(0,0)); img.paste(bot.resize((W,PH),Image.LANCZOS),(0,PH))
img.save(OUT+f'labios-story-9x16-fundo-original.png',icc_profile=icc); print(img.size)
