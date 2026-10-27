# Complète un détourage IA avec un détourage par couleur de fond (objets fins : pieds de table…).
# Usage : python3 colorkey.py original.png cut_ia.png sortie.png [seuil=38]
import sys
from PIL import Image, ImageChops, ImageFilter
orig = Image.open(sys.argv[1]).convert("RGB")
cut = Image.open(sys.argv[2]).convert("RGBA")
thr = int(sys.argv[4]) if len(sys.argv) > 4 else 38
w, h = orig.size
corners = [orig.getpixel(p) for p in [(5, 5), (w - 6, 5), (5, h - 6), (w - 6, h - 6), (w // 2, 5)]]
bg = tuple(sorted(c[i] for c in corners)[2] for i in range(3))
diff = ImageChops.difference(orig, Image.new("RGB", orig.size, bg)).convert("L")
key = diff.point(lambda v: 255 if v > thr else 0).filter(ImageFilter.MedianFilter(5))
alpha = ImageChops.lighter(cut.split()[3], key)
out = orig.convert("RGBA"); out.putalpha(alpha)
out.save(sys.argv[3]); print("fond", bg)
