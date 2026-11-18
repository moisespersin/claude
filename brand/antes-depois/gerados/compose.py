import sys
from PIL import Image, ImageDraw, ImageFont, ImageCms
import numpy as np
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
B=Image.open(IMG+'11.jpg'); A=Image.open(IMG+'12.jpg')
icc=B.info.get('icc_profile')
H=1800; CW=int(H*0.8/2)  # 720
before=B.crop((160,0,160+CW,H)); after=A.crop((125,40,125+CW,40+H))
W=CW*2
neutral = '--neutral' in sys.argv
def neutralize(im):
    a=np.asarray(im.convert('RGB')).astype(float)/255
    mx=a.max(2); mn=a.min(2); s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
    # background: low saturation, not dark
    m=np.clip((0.27-s)/0.08,0,1)*np.clip((mx-0.30)/0.1,0,1)
    from PIL import ImageFilter
    m=np.asarray(Image.fromarray((m*255).astype('uint8')).filter(ImageFilter.GaussianBlur(3))).astype(float)/255
    lum=(0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2])[...,None]
    grey=lum*np.array([0.985,1.0,1.02])  # cinza levemente frio
    out=a*(1-m[...,None]*0.9)+grey*(m[...,None]*0.9)
    return Image.fromarray((np.clip(out,0,1)*255+0.5).astype('uint8'))
if neutral: before,after=neutralize(before),neutralize(after)
c=Image.new('RGB',(W,H)); c.paste(before,(0,0)); c.paste(after,(CW,0))
d=ImageDraw.Draw(c)
CHUMBO=(46,50,54)
F='/usr/share/fonts/opentype/inter/'
reg=ImageFont.truetype(F+'Inter-Light.otf',62); bold=ImageFont.truetype(F+'Inter-SemiBold.otf',62)
script=ImageFont.truetype('fonts/InstrumentSerif.ttf',190)
parts=[('Um ',reg),('perfil',bold),(' que te',reg)]
tw=sum(d.textlength(t,font=f) for t,f in parts)
x=(W-tw)/2; y=58
for t,f in parts:
    d.text((x,y),t,font=f,fill=CHUMBO); x+=d.textlength(t,font=f)
word='valoriza.'
ww=d.textlength(word,font=script)
d.text(((W-ww)/2,96),word,font=script,fill=CHUMBO)
# assinatura no depois
logo=Image.open('logo_alpha.png'); lw=190; logo=logo.resize((lw,int(logo.height*lw/logo.width)),Image.LANCZOS)
c.paste((255,255,255),(W-lw-40,H-logo.height-50),logo)
out=sys.argv[1]
c.save(out,quality=100,subsampling=0,icc_profile=icc) if out.endswith('.jpg') else c.save(out,icc_profile=icc)
print(c.size)
