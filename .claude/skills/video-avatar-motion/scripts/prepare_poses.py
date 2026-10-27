# Met plusieurs poses détourées à la même échelle (même hauteur de personnage), aligne les pieds,
# ajoute le contour blanc "sticker" et les recadre toutes dans un cadre commun : elles se remplacent sans saut.
# Usage : python3 prepare_poses.py <dossier_cut> <dossier_sortie> [ref=base] [noms...]
#   <dossier_cut> contient cut_<nom>.png (sortie de `npx hyperframes remove-background`).
#   Sans noms : toutes les cut_*.png du dossier. Sortie : avatar_<nom>.png
#   Les noms suffixés par ":h=0.9" gardent une hauteur relative (ex. bureau_ordinateur:h=0.9).
import glob, os, sys
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
ref = sys.argv[3] if len(sys.argv) > 3 else "base"
args = sys.argv[4:] or sorted(os.path.basename(p)[4:-4] for p in glob.glob(f"{src}/cut_*.png"))
rel = {}
names = []
for a in args:
    n, _, opt = a.partition(":h=")
    names.append(n)
    rel[n] = float(opt) if opt else 1.0

def load(n):
    im = Image.open(f"{src}/cut_{n}.png").convert("RGBA")
    bb = im.split()[3].point(lambda v: 255 if v > 100 else 0).getbbox()
    return im.crop(bb)

target_h = load(ref).size[1]
W, H, pad = 1100, int(target_h * 1.25) + 80, 40
frames = []
for n in names:
    im = load(n)
    s = target_h * rel[n] / im.size[1]
    im = im.resize((max(1, round(im.size[0] * s)), round(im.size[1] * s)), Image.LANCZOS)
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.paste(im, ((W - im.size[0]) // 2, H - pad - im.size[1]), im)  # centré, pieds sur la même ligne
    a = c.split()[3].point(lambda v: 255 if v > 100 else 0)
    ol = a.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(1.2))
    wht = Image.new("RGBA", c.size, (255, 255, 255, 255)); wht.putalpha(ol)
    sh = Image.new("RGBA", c.size, (0, 0, 0, 255)); sh.putalpha(ol.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .25)))
    o = Image.new("RGBA", c.size, (0, 0, 0, 0)); o.alpha_composite(sh); o.alpha_composite(wht); o.alpha_composite(c)
    frames.append((n, o))

box = None
for _, o in frames:
    b = o.getbbox()
    box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
os.makedirs(out, exist_ok=True)
for n, o in frames:
    o.crop(box).save(f"{out}/avatar_{n}.png")
print(f"{len(frames)} poses -> {out}  cadre commun {box[2]-box[0]}x{box[3]-box[1]} (rapport {round((box[2]-box[0])/(box[3]-box[1]),3)})")
