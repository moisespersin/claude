import numpy as np, math
from PIL import Image
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad'); from cor import abrir, P3
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/final/'
W,PH=1080,960                  # story 9:16, antes em cima e depois embaixo
# pupilas medidas na resolução original (1450 x 2576)
A_L,A_R=(680,1115),(935,1058)  # antes
D_L,D_R=(640,903),(910,860)  # depois
mid=lambda p,q: ((p[0]+q[0])/2,(p[1]+q[1])/2)
ang=lambda p,q: math.atan2(q[1]-p[1],q[0]-p[0])
mA,mD=mid(A_L,A_R),mid(D_L,D_R)
k=math.dist(D_L,D_R)/math.dist(A_L,A_R)
th=ang(A_L,A_R)-ang(D_L,D_R)   # diferença de inclinação da linha dos olhos
# caixa do depois na foto original
BX,BY,BW=175,470,1150; BH=round(BW*PH/W)
before=abrir('22.jpg'); after=abrir('23.jpg')
icc=P3
# antes: escala, gira e alinha pelas pupilas para casar com a caixa do depois
c,s=math.cos(th)/k,math.sin(th)/k
# saída (u,v) -> ponto no depois p=(u+BX,v+BY) -> antes = mA + R(th)(p-mD)/k
a_,b_=c,-s; d_,e_=s,c
cx=mA[0]+a_*(BX-mD[0])+b_*(BY-mD[1]); cy=mA[1]+d_*(BX-mD[0])+e_*(BY-mD[1])
top=before.transform((BW,BH),Image.AFFINE,(a_,b_,cx,d_,e_,cy),resample=Image.BICUBIC)
bot=after.crop((BX,BY,BX+BW,BY+BH))
img=Image.new('RGB',(W,PH*2))
img.paste(top.resize((W,PH),Image.LANCZOS),(0,0)); img.paste(bot.resize((W,PH),Image.LANCZOS),(0,PH))
img.save(OUT+'montagem-3-story-9x16.png',icc_profile=icc)
print(img.size, math.degrees(th), 'cantos do antes:', cx, cy, cx+a_*BW+b_*BH, cy+d_*BW+e_*BH)
