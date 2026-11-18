from PIL import Image, ImageFilter
import numpy as np
src=Image.open('/home/user/claude/brand/antes-depois/referencias/10-historia-composicao-pb.webp').convert('L')
c=src.crop((600,1035,790,1135))
a=np.asarray(c).astype(float)
bg=np.asarray(c.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(6))).astype(float)
ink=45.0
alpha=np.clip((bg-a)/(bg-ink),0,1)
alpha[alpha<0.12]=0
al=Image.fromarray((alpha*255).astype('uint8'))
# upscale 4x then sharpen edges via contrast curve
S=4
al=al.resize((al.width*S,al.height*S),Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5))
arr=np.asarray(al).astype(float)/255
arr=np.clip((arr-0.35)/0.3,0,1)
al=Image.fromarray((arr*255).astype('uint8'))
bbox=al.getbbox(); al=al.crop(bbox)
al.save('logo_alpha.png'); print(al.size)
