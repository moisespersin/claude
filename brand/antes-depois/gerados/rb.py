import sys
from rembg import new_session, remove
from PIL import Image
IMG='/tmp/claude-0/-home-user-claude/2fe0263b-8b87-5d83-9885-629a1898bc55/images/'
s=new_session(sys.argv[1])
for f in sys.argv[2:]:
    m=remove(Image.open(IMG+f).convert('RGB'),session=s,only_mask=True)
    m.save(f'm_{sys.argv[1]}_{f[:2]}.png'); print(f,m.size,m.mode)
