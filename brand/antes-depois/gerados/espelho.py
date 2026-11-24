import numpy as np, sys
from PIL import Image, ImageFilter
sys.path.insert(0,'/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad')
from feed34_tom import C, lum, P3
from cor import abrir
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
I=np.asarray(abrir('32.jpg')).astype(float)/255
a=np.asarray(Image.open(SP+'m_birefnet-portrait_32.png')).astype(float)/255
mx,mn=I.max(2),I.min(2); s=(mx-mn)/np.maximum(mx,1e-6)
# só áreas claras e neutras (paredes e reflexo delas); madeira (saturada) e pessoa ficam originais
import colorsys
r,g,b=I[...,0],I[...,1],I[...,2]
hue=(np.degrees(np.arctan2(np.sqrt(3)*(g-b),2*r-g-b))%360)
madeira=np.clip((s-0.10)/0.05,0,1)*((hue>12)&(hue<40))
w=np.clip((0.22-s)/0.08,0,1)*(1-madeira)*np.clip((mx-0.25)/0.15,0,1)*(1-a)
w=np.asarray(Image.fromarray((w*255).astype('uint8')).filter(ImageFilter.GaussianBlur(2))).astype(float)[...,None]/255
G=np.clip(lum(I)[...,None]*C/lum(C),0,1)
out=I*(1-w)+G*w
Image.fromarray((np.clip(out,0,1)*255+0.5).astype('uint8')).save(SP+'entregas/espelho-C7CDD3.png',icc_profile=P3)
Image.fromarray((w[...,0]*255).astype('uint8')).resize((281,500)).save(SP+'w32.png')
