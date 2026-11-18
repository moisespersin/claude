import numpy as np
from PIL import Image, ImageFilter
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/final/'
C=np.array([0xC7,0xCD,0xD3])/255
lum=lambda x: x[...,0]*0.2126+x[...,1]*0.7152+x[...,2]*0.0722
W,PH=1080,675
def gblur(x,r):  # blur vertical de um array (H,1,3) ou (H,N,3)
    return np.stack([np.asarray(Image.fromarray((x[...,c]*255).astype('uint8')).filter(ImageFilter.GaussianBlur(r))).astype(float)/255 for c in range(3)],-1)
def side(out,a,n,left,rng):
    band=out[:,:40] if left else out[:,-40:]; ab=a[:,:40,0] if left else a[:,-40:,0]
    col=np.zeros((out.shape[0],3)); last=band[:,:,:].mean(1)[0]
    Lb=lum(band); Lm=np.median(Lb[ab<0.05])
    for y in range(out.shape[0]):
        m=(ab[y]<0.05)&(Lb[y]<Lm*1.10)&(Lb[y]>Lm*0.80)   # ignora reflexos e manchas
        if m.sum()>8: last=np.median(band[y][m],0)
        col[y]=last
    col=gblur(col[:,None,:],60)[:,0]
    e=np.repeat(col[:,None,:],n,1)
    # luz cai suavemente para fora, como na parede
    t=np.linspace(1,0,n)[None,:,None] if left else np.linspace(0,1,n)[None,:,None]
    e=e*(1-0.06*t)+rng.normal(0,0.005,e.shape)
    # emenda: funde 60 px com a borda original
    k=min(90,n); edge=out[:,:k] if left else out[:,-k:]
    w=np.linspace(0,1,k)[None,:,None]
    if left: e[:,-k:]=e[:,-k:]*(1-w)+edge*w; return np.clip(e,0,1),k
    e[:,:k]=edge*(1-w)+e[:,:k]*w; return np.clip(e,0,1),k
boxes=[('16.jpg',-282,420,1700),('17.jpg',-182,519,1483)]
rows=[]
for f,x0,y0,bw in boxes:
    bh=round(bw*PH/W); rng=np.random.default_rng(len(f)+bw)
    im=Image.open(IMG+f); icc=im.info.get('icc_profile')
    I=np.asarray(im.convert('RGB')).astype(float)/255
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)[...,None]/255
    G=np.clip(lum(I)[...,None]*C/lum(C),0,1)
    out=(I*a+G*(1-a))[y0:y0+bh]; a=a[y0:y0+bh]
    pl=-x0; pr=x0+bw-out.shape[1]
    L_,kl=side(out,a,pl+90,True,rng); R_,kr=side(out,a,pr+90,False,rng)
    out=np.concatenate([L_,out[:,90:-90],R_],1)
    rows.append(Image.fromarray((np.clip(out,0,1)*255+0.5).astype('uint8')).resize((W,PH),Image.LANCZOS))
img=Image.new('RGB',(W,PH*2)); img.paste(rows[0],(0,0)); img.paste(rows[1],(0,PH))
img.save(OUT+'frontal-medio-4x5-C7CDD3.png',icc_profile=icc); print(img.size)
