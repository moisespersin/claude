import sys
from PIL import Image
sys.path.insert(0,'/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad')
from feed34_tom import tom, P3
SP='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/scratchpad/'
W,RH=1080,450                      # 4:5 com 3 faixas de 1080 x 450
k=1450/1126
# (foto, centro vertical dos lábios em px da tela 1126 de largura)
fotos=[('37.jpg',float(sys.argv[1])),('36.jpg',float(sys.argv[2])),('38.jpg',float(sys.argv[3]))]
img=Image.new('RGB',(W,RH*3))
for i,(f,cy) in enumerate(fotos):
    im=tom(f); w=im.width; h=round(w*RH/W); y0=round(cy*k-h/2)
    img.paste(im.crop((0,y0,w,y0+h)).resize((W,RH),Image.LANCZOS),(0,i*RH))
img.save(SP+'entregas/feed-4x5-labios-3-fotos-C7CDD3.png',icc_profile=P3)
