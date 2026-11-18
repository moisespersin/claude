import numpy as np
from PIL import Image
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/final/'
C=np.array([0xC7,0xCD,0xD3])/255
lum=lambda x: x[...,0]*0.2126+x[...,1]*0.7152+x[...,2]*0.0722
W,PH=1080,675
BW=1125; BH=round(BW*PH/W)   # caixa de 1125 x 703 da foto, reduzida para 1080 x 675 (só redução)
rows=[]
for f,y0 in [('14.jpg',754),('15.jpg',695)]:
    im=Image.open(IMG+f); icc=im.info.get('icc_profile')
    I=np.asarray(im.convert('RGB')).astype(float)/255
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)[...,None]/255
    G=np.clip(lum(I)[...,None]*C/lum(C),0,1)
    out=(I*a+G*(1-a))[y0:y0+BH,0:BW]
    rows.append(Image.fromarray((np.clip(out,0,1)*255+0.5).astype('uint8')).resize((W,PH),Image.LANCZOS))
img=Image.new('RGB',(W,PH*2)); img.paste(rows[0],(0,0)); img.paste(rows[1],(0,PH))
img.save(OUT+'perfil-4x5-C7CDD3.png',icc_profile=icc); print(img.size)
