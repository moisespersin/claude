import numpy as np, sys
from PIL import Image
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
OUT='/home/user/claude/brand/antes-depois/gerados/final/'
C=np.array([0xC7,0xCD,0xD3])/255
lum=lambda x: x[...,0]*0.2126+x[...,1]*0.7152+x[...,2]*0.0722
SH,EXT,CW=1960,290,900          # 4:5 -> 1800 x 2250
mode=sys.argv[1] if len(sys.argv)>1 else 'espelho'
cols=[]
for f,x0,y0 in [('11.jpg',40,0),('12.jpg',25,40)]:
    im=Image.open(IMG+f); icc=im.info.get('icc_profile')
    I=np.asarray(im.convert('RGB')).astype(float)/255
    a=np.asarray(Image.open(SP+f'm_birefnet-portrait_{f[:2]}.png')).astype(float)/255
    I=I[y0:y0+SH,x0:x0+CW]; a=a[y0:y0+SH,x0:x0+CW]
    if mode=='espelho':
        top=I[1:EXT+1][::-1]
    else:  # esticar: continua as linhas verticais da parede
        m0=I[:6].mean(0); m1=I[120:130].mean(0)
        slope=(m1-m0)/122
        k=np.ones(81)/81                              # suaviza na horizontal, evita listras
        slope=np.stack([np.convolve(np.pad(slope[:,c],40,mode='edge'),k,'valid') for c in range(3)],1)
        m0=np.stack([np.convolve(np.pad(m0[:,c],1,mode='edge'),np.ones(3)/3,'valid') for c in range(3)],1)
        d=np.arange(EXT,0,-1)[:,None,None]+2.5      # distância até a primeira linha real
        top=m0[None]-slope[None]*d*np.exp(-d/400)  # continua o degradê natural, amortecido
        top=np.clip(top,0,1)+np.random.default_rng(1).normal(0,0.004,(EXT,CW,3))
    I=np.concatenate([top,I]); a=np.concatenate([np.zeros((EXT,CW)),a])
    G=np.clip(lum(I)[...,None]*C/lum(C),0,1)
    cols.append(I*a[...,None]+G*(1-a[...,None]))
img=Image.fromarray((np.clip(np.concatenate(cols,1),0,1)*255+0.5).astype('uint8'))
img.save(OUT+f'antes-depois-4x5-C7CDD3-respiro-{mode}.png',icc_profile=icc); print(img.size)
