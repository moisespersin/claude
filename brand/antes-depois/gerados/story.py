import numpy as np, sys
from PIL import Image
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/final/'
C=np.array([0xC7,0xCD,0xD3])/255
lum=lambda x: x[...,0]*0.2126+x[...,1]*0.7152+x[...,2]*0.0722
W,PH=1080,960   # story 1080 x 1920 (9:16): antes em cima, depois embaixo
# (foto, x0, y0, largura da caixa). O depois foi fotografado mais perto (~13%),
# então a caixa do antes é menor para os rostos ficarem do mesmo tamanho (alinhados pelos olhos).
boxes=[('18.jpg',97,632,1283),('19.jpg',0,682,1450)]
rows=[]; icc=None
for f,x0,y0,bw in boxes:
    bh=round(bw*PH/W)
    im=Image.open(IMG+f); icc=icc or im.info.get('icc_profile')
    I=np.asarray(im.convert('RGB')).astype(float)/255
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)[...,None]/255
    G=np.clip(lum(I)[...,None]*C/lum(C),0,1)
    out=(I*a+G*(1-a))[y0:y0+bh,x0:x0+bw]
    assert out.shape[:2]==(bh,bw), (f,out.shape)
    rows.append(Image.fromarray((np.clip(out,0,1)*255+0.5).astype('uint8')).resize((W,PH),Image.LANCZOS))
img=Image.new('RGB',(W,PH*2)); img.paste(rows[0],(0,0)); img.paste(rows[1],(0,PH))
img.save(OUT+'story-9x16-C7CDD3.png',icc_profile=icc); print(img.size)
