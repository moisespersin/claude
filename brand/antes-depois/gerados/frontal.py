import numpy as np
from PIL import Image
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/final/'
C=np.array([0xC7,0xCD,0xD3])/255
lum=lambda x: x[...,0]*0.2126+x[...,1]*0.7152+x[...,2]*0.0722
W,PH=1080,675
# caixas (x0,y0,largura) com a mesma proporção 1080:675; o depois está mais longe da câmera,
# então a caixa dele é menor para os rostos ficarem do mesmo tamanho (alinhados pelas pupilas)
boxes=[('16.jpg',-83,686,1302),('17.jpg',-8,751,1136)]
rows=[]
for f,x0,y0,bw in boxes:
    bh=round(bw*PH/W)
    im=Image.open(IMG+f); icc=im.info.get('icc_profile')
    I=np.asarray(im.convert('RGB')).astype(float)/255
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)[...,None]/255
    G=np.clip(lum(I)[...,None]*C/lum(C),0,1)
    out=I*a+G*(1-a)
    # margem lateral: continua a parede da borda (só onde a caixa passa da foto)
    pl=max(0,-x0); pr=max(0,x0+bw-out.shape[1])
    def ext(col,n):
        c=np.asarray(Image.fromarray((col*255).astype('uint8')).filter(__import__('PIL.ImageFilter',fromlist=['x']).GaussianBlur(6))).astype(float)/255
        e=np.repeat(c,n,1)+np.random.default_rng(n).normal(0,0.004,(col.shape[0],n,3))
        return np.clip(e,0,1)
    L_=ext(out[:,:1],pl) if pl else out[:,:0]; R_=ext(out[:,-1:],pr) if pr else out[:,:0]
    out=np.concatenate([L_,out,R_],1)
    x0+=pl
    out=out[y0:y0+bh,x0:x0+bw]
    rows.append(Image.fromarray((np.clip(out,0,1)*255+0.5).astype('uint8')).resize((W,PH),Image.LANCZOS))
img=Image.new('RGB',(W,PH*2)); img.paste(rows[0],(0,0)); img.paste(rows[1],(0,PH))
img.save(OUT+'frontal-4x5-C7CDD3.png',icc_profile=icc); print(img.size)
