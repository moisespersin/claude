# Abre a foto mantendo a cor exata: tudo é levado para o perfil Display P3
# (o mais amplo entre as fotos), sem perda. Fotos sem perfil são tratadas como sRGB.
import io
from PIL import Image, ImageCms
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
P3=Image.open(IMG+'18.jpg').info['icc_profile']
_p3=ImageCms.ImageCmsProfile(io.BytesIO(P3)); _srgb=ImageCms.createProfile('sRGB')
def abrir(f):
    im=Image.open(IMG+f); p=im.info.get('icc_profile'); im=im.convert('RGB')
    src=ImageCms.ImageCmsProfile(io.BytesIO(p)) if p else _srgb
    if p and ImageCms.getProfileDescription(src).strip()=='Display P3': return im
    return ImageCms.profileToProfile(im,src,_p3,renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,outputMode='RGB')
