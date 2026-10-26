# Contour blanc "sticker" + ombre douce autour d une image détourée.
# Usage : python3 outline_avatar.py avatar_cut.png avatar.png
import sys
from PIL import Image, ImageFilter
im = Image.open(sys.argv[1]).convert("RGBA")
im = im.crop(im.getbbox())
pad = 40
W,H = im.size
canvas = Image.new("RGBA",(W+2*pad,H+2*pad),(0,0,0,0))
canvas.paste(im,(pad,pad),im)
a = canvas.split()[3].point(lambda v: 255 if v>100 else 0)
outline = a.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(1.2))
white = Image.new("RGBA",canvas.size,(255,255,255,255)); white.putalpha(outline)
# soft drop shadow
sh = outline.filter(ImageFilter.GaussianBlur(10)).point(lambda v:int(v*0.25))
shadow = Image.new("RGBA",canvas.size,(0,0,0,255)); shadow.putalpha(sh)
out = Image.new("RGBA",canvas.size,(0,0,0,0))
out.alpha_composite(shadow,(0,6)) if False else out.alpha_composite(shadow)
out.alpha_composite(white); out.alpha_composite(canvas)
out.save(sys.argv[2]); print(out.size)
