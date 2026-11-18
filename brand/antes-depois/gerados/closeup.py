import numpy as np
from PIL import Image
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/final/'
C=np.array([0xC7,0xCD,0xD3])/255
lum=lambda x: x[...,0]*0.2126+x[...,1]*0.7152+x[...,2]*0.0722
W,PH=1080,675   # 1080 x 1350 (4:5), antes em cima e depois embaixo, sem ampliar
rows=[]
for f,x0,y0 in [('11.jpg',40,650),('12.jpg',5,690)]:
    im=Image.open(IMG+f); icc=im.info.get('icc_profile')
    I=np.asarray(im.convert('RGB')).astype(float)[y0:y0+PH,x0:x0+W]/255
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)[y0:y0+PH,x0:x0+W,None]/255
    G=np.clip(lum(I)[...,None]*C/lum(C),0,1)
    rows.append(I*a+G*(1-a))
img=Image.fromarray((np.clip(np.concatenate(rows,0),0,1)*255+0.5).astype('uint8'))
img.save(OUT+'antes-depois-4x5-C7CDD3-close.png',icc_profile=icc); print(img.size)
