import sys
from PIL import Image, ImageFilter
names = ['base','point','think','shock','laptop','wave']
src, out = sys.argv[1], sys.argv[2]
ims = {}
for n in names:
    im = Image.open(f'{src}/cut_{n}.png').convert('RGBA')
    a = im.split()[3].point(lambda v: 255 if v > 100 else 0)
    bb = a.getbbox()
    ims[n] = (im, bb)
base_bottom = ims['base'][1][3]
pad = 40
canvas = []
for n in names:
    im, bb = ims[n]
    dy = base_bottom - bb[3]          # align feet on the base pose
    c = Image.new('RGBA', (1024 + 2*pad, 1024 + 2*pad), (0,0,0,0))
    c.paste(im, (pad, pad + dy), im)
    a = c.split()[3].point(lambda v: 255 if v > 100 else 0)
    ol = a.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(1.2))
    w = Image.new('RGBA', c.size, (255,255,255,255)); w.putalpha(ol)
    sh = Image.new('RGBA', c.size, (0,0,0,255)); sh.putalpha(ol.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v*.25)))
    o = Image.new('RGBA', c.size, (0,0,0,0)); o.alpha_composite(sh); o.alpha_composite(w); o.alpha_composite(c)
    canvas.append((n, o))
box = None
for n, o in canvas:
    b = o.getbbox()
    box = b if box is None else (min(box[0],b[0]), min(box[1],b[1]), max(box[2],b[2]), max(box[3],b[3]))
for n, o in canvas:
    o.crop(box).save(f'{out}/avatar_{n}.png')
print(box, box[2]-box[0], box[3]-box[1])
