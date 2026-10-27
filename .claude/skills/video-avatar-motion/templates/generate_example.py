# MODÈLE : vidéo "20 ans d expérience + ChatGPT" (1 min 53). Copier puis adapter scènes, textes et temps T(i).
# Usage : python3 generate.py <dossier_projet_video>   (lit assets/transcript.json, écrit index.html + compositions/)
import json, os, sys

P = sys.argv[1]  # project dir
os.makedirs(f"{P}/compositions", exist_ok=True)
W = json.load(open(f"{P}/assets/transcript.json"))
W = W if isinstance(W, list) else W["words"]
T = lambda i: round(W[i]["start"], 2)
TOTAL = 113.2
OR = "#E8532F"

# ---------------------------------------------------------------- icons
def svg(body, size=120):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" stroke="#111" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">{body}</svg>'

ICON = {
    "briefcase": '<rect x="10" y="30" width="80" height="55" rx="8" fill="#E8532F"/><path d="M36 30V20h28v10"/><path d="M10 52h80"/>',
    "coin": '<circle cx="50" cy="50" r="40" fill="#E8532F"/><path d="M62 34a18 18 0 1 0 0 32M30 45h26M30 56h26" stroke="#fff"/>',
    "sparkle": '<path d="M50 6c4 24 20 40 44 44-24 4-40 20-44 44-4-24-20-40-44-44 24-4 40-20 44-44z" fill="#E8532F"/>',
    "user": '<circle cx="50" cy="32" r="18" fill="#E8532F"/><path d="M16 90c0-20 15-32 34-32s34 12 34 32z"/>',
    "users": '<circle cx="36" cy="36" r="15" fill="#E8532F"/><circle cx="70" cy="40" r="12"/><path d="M8 88c0-18 12-28 28-28s28 10 28 28zM62 62c16 0 30 8 30 26H70"/>',
    "building": '<rect x="18" y="12" width="64" height="78" fill="#E8532F"/><path d="M32 28h10M58 28h10M32 46h10M58 46h10M32 64h10M58 64h10M44 90V76h12v14" stroke="#fff"/><rect x="18" y="12" width="64" height="78"/>',
    "folder": '<path d="M8 22h30l8 10h46v52H8z" fill="#E8532F"/><path d="M8 42h84"/>',
    "pen": '<path d="M20 10h44l16 16v64H20z"/><path d="M32 40h36M32 54h36M32 68h20"/><path d="M60 86l26-34 8 6-26 34-10 4z" fill="#E8532F"/>',
    "cap": '<path d="M4 38l46-20 46 20-46 20z" fill="#E8532F"/><path d="M24 48v22c0 8 52 8 52 0V48M88 42v24"/>',
    "route": '<circle cx="24" cy="78" r="10" fill="#E8532F"/><circle cx="76" cy="22" r="10" fill="#E8532F"/><path d="M34 78h30c14 0 14-22 0-22H36c-14 0-14-22 0-22h30" stroke-dasharray="2 10"/>',
    "bulb": '<path d="M50 8c-20 0-32 15-32 31 0 12 7 19 12 25 3 4 4 8 4 12h32c0-4 1-8 4-12 5-6 12-13 12-25 0-16-12-31-32-31z" fill="#E8532F"/><path d="M36 86h28M40 96h20"/>',
    "warning": '<path d="M50 8l44 80H6z" fill="#E8532F"/><path d="M50 36v24M50 74v1" stroke="#fff" stroke-width="9"/><path d="M50 8l44 80H6z"/>',
    "check": '<circle cx="50" cy="50" r="42" fill="#E8532F"/><path d="M30 52l14 14 28-30" stroke="#fff" stroke-width="10"/>',
    "hourglass": '<path d="M22 8h56M22 92h56M28 8c0 26 44 26 44 42s-44 16-44 42M72 8c0 26-44 26-44 42s44 16 44 42"/><path d="M36 84c4-10 24-10 28 0z" fill="#E8532F"/>',
    "magnifier": '<circle cx="42" cy="42" r="28" fill="#E8532F"/><circle cx="42" cy="42" r="28"/><path d="M62 62l28 28" stroke-width="10"/>',
    "trophy": '<path d="M28 10h44v26c0 14-10 24-22 24S28 50 28 36z" fill="#E8532F"/><path d="M28 18H12c0 16 8 24 18 24M72 18h16c0 16-8 24-18 24M50 60v16M32 90h36l-4-14H36z"/>',
    "chart": '<path d="M10 90h80M10 90V10"/><path d="M20 72l20-20 16 12 30-34" stroke="#E8532F" stroke-width="9"/><path d="M70 30h16v16"/>',
    "target": '<circle cx="50" cy="50" r="40"/><circle cx="50" cy="50" r="24" fill="#E8532F"/><circle cx="50" cy="50" r="8" fill="#fff"/>',
    "chat": '<path d="M10 16h80v52H44L24 86V68H10z" fill="#E8532F"/><path d="M28 36h44M28 50h30" stroke="#fff"/>',
    "send": '<circle cx="50" cy="50" r="46" fill="#111" stroke="none"/><path d="M50 72V30M32 46l18-18 18 18" stroke="#fff" stroke-width="9"/>',
    "plus": '<rect x="8" y="8" width="84" height="84" rx="12"/><path d="M50 28v44M28 50h44"/>',
}
def icon(name, size=120, cls="", idattr=""):
    return f'<div {idattr} class="ic {cls}">{svg(ICON[name], size)}</div>'

# ---------------------------------------------------------------- shared css / js
CSS = f"""
#root{{position:absolute;inset:0;font-family:'Montserrat',sans-serif;color:#111;}}
.abs{{position:absolute}}
.row{{position:absolute;left:0;width:1080px;display:flex;justify-content:center}}
.lbl{{display:inline-block;background:{OR};color:#fff;font-weight:900;text-transform:uppercase;font-size:50px;line-height:1.12;padding:14px 28px;border:5px solid #111;box-shadow:9px 9px 0 #111;white-space:nowrap;letter-spacing:.01em}}
.lbl.w{{background:#fff;color:#111}}
.lbl.k{{background:#111;color:#fff;box-shadow:9px 9px 0 {OR}}}
.lbl.s{{font-size:40px;padding:10px 22px}}
.lbl.xl{{font-size:76px;padding:16px 34px}}
.box{{background:#fff;border:5px solid #111;box-shadow:14px 14px 0 #111;border-radius:12px}}
.o{{color:{OR}}}
.ic{{display:flex;align-items:center;justify-content:center}}
svg{{flex:none}}
.badge{{width:170px;height:190px;background:{OR};border:5px solid #111;box-shadow:10px 10px 0 #111;color:#fff;text-align:center;font-weight:900}}
.badge small{{display:block;font-size:28px;margin-top:16px;letter-spacing:.06em}}
.badge b{{display:block;font-size:120px;line-height:1}}
.win-h{{height:78px;border-bottom:5px solid #111;display:flex;align-items:center;gap:12px;padding:0 26px;font-weight:900;font-size:32px}}
.win-h i{{width:20px;height:20px;border-radius:50%;border:4px solid #111;display:inline-block}}
.win-h i:first-child{{background:{OR}}}
.win-h .st{{margin-left:auto;background:#111;color:#fff;font-size:28px;padding:6px 14px;border-radius:6px;letter-spacing:.05em}}
.win-b{{padding:30px 30px 10px}}
.bubble{{margin-left:50px;background:#F1F1F1;border-radius:30px;padding:26px 32px;font-weight:600;font-size:34px;line-height:1.4}}
.bubble .tw{{opacity:0}}
.bubble .tw.o{{font-weight:800}}
.win-f{{margin:20px 30px 30px;border:4px solid #111;border-radius:50px;height:96px;display:flex;align-items:center;padding:0 14px 0 22px;gap:16px;font-size:30px;font-weight:600;color:#888}}
.win-f .sp{{margin-left:auto}}
.tile{{display:flex;align-items:center;gap:22px;padding:22px 26px;font-weight:900;font-size:36px;text-transform:uppercase;line-height:1.15}}
"""

JS = """
const tl = gsap.timeline({ paused: true });
const pop = (s, t, d) => tl.fromTo(s, { opacity: 0, scale: 0.55, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: d || 0.38, ease: "back.out(2.2)" }, t);
const slideL = (s, t) => tl.fromTo(s, { opacity: 0, x: -140 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, t);
const slideR = (s, t) => tl.fromTo(s, { opacity: 0, x: 140 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, t);
const rise = (s, t) => tl.fromTo(s, { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, t);
const out = (s, t) => tl.to(s, { opacity: 0, scale: 0.85, duration: 0.25, ease: "power2.in" }, t);
const typeAt = (sel, times) => { document.querySelectorAll(sel).forEach((el, i) => tl.set(el, { opacity: 1 }, times[i])); };
const typeChars = (sel, t0, t1) => { const el = document.querySelector(sel); const full = el.dataset.full; const o = { n: 0 };
  tl.fromTo(o, { n: 0 }, { n: full.length, duration: t1 - t0, ease: "none", onUpdate: () => { el.textContent = full.slice(0, Math.round(o.n)); } }, t0); };
const wiggle = (s, t, n) => tl.fromTo(s, { rotation: -4 }, { rotation: 4, duration: 0.1, yoyo: true, repeat: n || 5, ease: "sine.inOut" }, t).to(s, { rotation: 0, duration: 0.1 }, ">");
"""

def scene(cid, dur, css, html, js):
    return f"""<template>
  <style>{CSS}{css}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-layout-allow-overlap>
{html}
  </div>
  <script>
{JS}
{js}
    tl.set({{}}, {{}}, {dur});
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""

def lbl(id_, text, top, cls="", left=None):
    if left is None:
        return f'<div class="row" style="top:{top}px"><div id="{id_}" class="lbl {cls}">{text}</div></div>'
    return f'<div id="{id_}" class="lbl abs {cls}" style="top:{top}px;left:{left}px">{text}</div>'

ORANGE_WORDS = {"compétences", "connaissances", "problèmes", "entreprises", "personnes", "catégories", "services", "aide.", "proposer.", "résoudre.", "trois", "précisions.", "d’entreprises"}
def bubble_words(text, prefix):
    out = []
    for k, w in enumerate(text.split()):
        bare = w.strip(",.").lower()
        cls = "tw o" if (w.lower() in ORANGE_WORDS or bare in ORANGE_WORDS) else "tw"
        out.append(f'<span class="{cls} {prefix}-w">{w} </span>')
    return "".join(out)

def chat_window(p, step, text, top):
    return f"""<div id="{p}-win" class="box abs" style="left:70px;top:{top}px;width:940px">
  <div class="win-h"><i></i><i></i><i></i>&nbsp;ChatGPT<span class="st">ÉTAPE {step}</span></div>
  <div class="win-b"><div class="bubble">{bubble_words(text, p)}</div></div>
  <div class="win-f">{svg(ICON['plus'], 52)}<span>Envoyer</span><span id="{p}-dots" style="opacity:0;color:#111;font-weight:900">• • •</span><div id="{p}-send" class="sp">{svg(ICON['send'], 70)}</div></div>
</div>"""

def times(i0, n):
    return [T(i0 + k) for k in range(n)]

S = {}  # scene id -> (start, dur)
SFX = []  # (abs time, file, vol)

# ================================================================= HOOK 0–11.5
s0, d = 0.0, 11.5; S["hook"] = (s0, d)
html = f"""
<div id="h-card" class="box abs" style="left:150px;top:380px;width:780px;height:380px">
  <div class="abs" style="left:50px;top:30px;font-weight:900;font-size:250px;line-height:1;color:{OR};-webkit-text-stroke:5px #111">20</div>
  <div class="abs" style="left:395px;top:70px;font-weight:900;font-size:96px;line-height:1">ANS</div>
  <div class="abs" style="left:398px;top:180px;font-weight:900;font-size:40px">D'EXPÉRIENCE</div>
  <div class="abs" style="left:50px;top:300px;width:680px;height:28px;border:4px solid #111;border-radius:20px;overflow:hidden"><div id="h-bar" style="width:100%;height:100%;background:{OR};transform-origin:left center"></div></div>
</div>
{lbl("h-l1", "RIEN À VENDRE ?", 830)}
{lbl("h-l2", "EN DEHORS DE VOTRE EMPLOI", 960, "w s")}
<div id="h-q" class="abs" style="left:700px;top:1130px;font-weight:900;font-size:280px;line-height:1;color:{OR};-webkit-text-stroke:6px #111">?</div>
<div id="h-b1" class="box abs" style="left:90px;top:400px;width:390px;height:360px">{icon('briefcase',150).replace('class="ic ','class="ic abs ').replace('<div','<div style="left:120px;top:40px"',1)}<div class="abs" style="left:0;width:380px;top:220px;text-align:center;font-weight:900;font-size:40px;line-height:1.15">VOS<br>COMPÉTENCES</div></div>
<div id="h-plus" class="abs" style="left:498px;top:510px;font-weight:900;font-size:110px;line-height:1">+</div>
<div id="h-b2" class="box abs" style="left:600px;top:400px;width:390px;height:360px">{icon('coin',150).replace('<div','<div style="position:absolute;left:120px;top:40px"',1)}<div class="abs" style="left:0;width:380px;top:220px;text-align:center;font-weight:900;font-size:33px;line-height:1.2">ACTIVITÉ<br><span class="o">COMPLÉMENTAIRE</span></div></div>
<div class="row" style="top:850px"><div id="h-ia" class="lbl" style="display:flex;align-items:center;gap:18px">{svg(ICON['sparkle'],64)}GRÂCE À L'IA</div></div>
"""
js = f"""
tl.fromTo("#h-card", {{ scale: 0.94 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, 0);
tl.fromTo("#h-bar", {{ scaleX: 0.05 }}, {{ scaleX: 1, duration: 2.2, ease: "power2.out" }}, 0.1);
pop("#h-l1", {T(10)-0.1}); pop("#h-l2", {T(12)}); pop("#h-q", {T(10)+0.1});
tl.fromTo("#h-q", {{ rotation: -10 }}, {{ rotation: 10, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {T(10)+0.4});
out("#h-card", {T(18)-0.1}); out("#h-l1", {T(18)-0.1}); out("#h-l2", {T(18)-0.1}); out("#h-q", {T(18)-0.1});
slideL("#h-b1", {T(21)}); pop("#h-plus", {T(26)}); slideR("#h-b2", {T(28)});
pop("#h-ia", {T(30)}); tl.fromTo("#h-ia svg", {{ rotation: 0 }}, {{ rotation: 180, duration: 1.6, ease: "power1.inOut" }}, {T(30)+0.2});
out("#h-b1", {d-0.3}); out("#h-plus", {d-0.3}); out("#h-b2", {d-0.3}); out("#h-ia", {d-0.3});
"""
SFX += [(T(10)-0.1, "pop", .5), (T(12), "pop", .4), (T(21), "whoosh-short", .5), (T(28), "whoosh", .5), (T(30), "sparkle", .45)]
open(f"{P}/compositions/hook.html", "w").write(scene("hook", d, "", html, js))

# ================================================================= PLAN 11.5–15.7
s0, d = 11.5, 4.2; S["plan"] = (s0, d)
rows = [("1", "IDENTIFIEZ VOS COMPÉTENCES"), ("2", "TROUVEZ DES CLIENTS"), ("3", "CRÉEZ DES SERVICES")]
rh = "".join(f'<div id="p-r{n}" style="display:flex;align-items:center;gap:22px;margin:22px 0;font-weight:900;font-size:38px"><span style="background:{OR};color:#fff;border:4px solid #111;width:68px;height:68px;display:flex;align-items:center;justify-content:center;font-size:42px">{n}</span>{t}</div>' for n, t in rows)
html = f"""
{lbl("p-l", "VOICI COMMENT", 340)}
<div id="p-win" class="box abs" style="left:70px;top:480px;width:940px">
  <div class="win-h"><i></i><i></i><i></i>&nbsp;ChatGPT<span class="st">3 ÉTAPES</span></div>
  <div style="padding:20px 40px 26px">{rh}</div>
</div>
"""
js = f"""
pop("#p-l", 0.05); rise("#p-win", {T(37)-s0-0.2});
slideL("#p-r1", {T(38)-s0}); slideL("#p-r2", {T(39)-s0}); slideL("#p-r3", {T(40)-s0});
out("#p-l", {d-0.3}); out("#p-win", {d-0.3});
"""
SFX += [(s0, "whoosh", .55), (T(38), "pop", .35), (T(39), "pop", .35), (T(40), "pop", .35)]
open(f"{P}/compositions/plan.html", "w").write(scene("plan", d, "", html, js))

# ================================================================= generic step header
def header(p, n, l1, l2, top=360):
    return f"""<div id="{p}-badge" class="badge abs" style="left:90px;top:{top}px"><small>NUMÉRO</small><b>{n}</b></div>
{lbl(p+"-l1", l1, top+10, "w", 300)}
{lbl(p+"-l2", l2, top+110, "", 300)}"""

# ================================================================= STEP 1 15.7–34.9
s0, d = 15.7, 19.2; S["step1"] = (s0, d)
P1 = "Je possède 20 ans d’expérience dans mon métier. Aide-moi à identifier mes compétences, mes connaissances et les problèmes que je sais résoudre. Repère celles qui pourraient être utiles à d’autres personnes ou à des entreprises. Pose-moi des questions si tu as besoin de précisions."
assert len(P1.split()) == 44
chips = [("s1-c1", "COMPÉTENCES", "check", T(62)), ("s1-c2", "CONNAISSANCES", "check", T(64)), ("s1-c3", "PROBLÈMES RÉSOLUS", "check", T(67)),
         ("s1-c4", "PERSONNES", "users", T(80)), ("s1-c5", "ENTREPRISES", "building", T(84))]
ch = ""
ys = [1080, 1170, 1260, 1110, 1220]
for (cid, txt, ic, t), y in zip(chips, ys):
    ch += f'<div id="{cid}" class="lbl w s abs" style="left:560px;top:{y}px;display:flex;align-items:center;gap:14px;font-size:34px">{svg(ICON[ic],48)}{txt}</div>'
html = f"""
{header("s1", 1, "IDENTIFIEZ", "VOS COMPÉTENCES")}
{chat_window("s1", 1, P1, 330)}
{ch}
"""
tw = [round(t - s0, 2) for t in times(50, 44)]
js = f"""
pop("#s1-badge", 0.05); slideR("#s1-l1", {T(44)-s0}); slideR("#s1-l2", {T(45)-s0});
out("#s1-badge", {T(47)-s0-0.3}); out("#s1-l1", {T(47)-s0-0.3}); out("#s1-l2", {T(47)-s0-0.3});
rise("#s1-win", {T(47)-s0});
typeAt(".s1-w", {json.dumps(tw)});
""" + "".join(f'slideR("#{c[0]}", {round(c[3]-s0,2)});' for c in chips) + f"""
out("#s1-c1", {T(72)-s0-0.3}); out("#s1-c2", {T(72)-s0-0.3}); out("#s1-c3", {T(72)-s0-0.3});
tl.fromTo("#s1-send", {{ scale: 1 }}, {{ scale: 1.25, duration: 0.15, yoyo: true, repeat: 1 }}, {T(93)-s0+0.4});
tl.fromTo("#s1-dots", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {T(93)-s0+0.6});
out("#s1-win", {d-0.3}); out("#s1-c4", {d-0.3}); out("#s1-c5", {d-0.3});
"""
SFX += [(s0, "whoosh", .55), (T(44), "whoosh-short", .4), (T(47), "whoosh-short", .45), (T(50), "typing", .25), (T(58), "typing", .2), (T(72), "typing", .2), (T(85), "typing", .2)]
SFX += [(c[3], "pop", .35) for c in chips] + [(T(93)+0.4, "click-soft", .6)]
open(f"{P}/compositions/step1.html", "w").write(scene("step1", d, "", html, js))

# ================================================================= STEP 2 34.9–51.7
s0, d = 34.9, 16.8; S["step2"] = (s0, d)
P2 = "À partir de mes compétences, identifie trois catégories de personnes ou d’entreprises qui pourraient avoir besoin de mon aide."
assert len(P2.split()) == 19
cats = [("users", "PARTICULIERS", "Manque de temps", "Aide pratique"),
        ("building", "PETITES ENTREPRISES", "Tâches à déléguer", "Mission ponctuelle"),
        ("user", "INDÉPENDANTS", "Manque d’expertise", "Conseil sur mesure")]
ch = ""
for k, (ic, ttl, pb, sv) in enumerate(cats):
    ch += f"""<div id="s2-k{k}" class="box abs" style="left:70px;top:{350+k*235}px;width:940px;height:200px;display:flex;align-items:center;gap:26px;padding:0 30px">
  {svg(ICON[ic],120)}
  <div style="flex:1"><div style="font-weight:900;font-size:40px">{ttl}</div>
  <div id="s2-p{k}" style="font-size:30px;font-weight:700;margin-top:10px"><span class="o">PROBLÈME :</span> {pb}</div>
  <div id="s2-s{k}" style="font-size:30px;font-weight:700;margin-top:4px"><span class="o">SERVICE :</span> {sv}</div></div></div>"""
html = f"""
{header("s2", 2, "TROUVEZ", "DES CLIENTS POTENTIELS")}
{chat_window("s2", 2, P2, 350)}
{ch}
"""
tw = [round(t - s0, 2) for t in times(102, 19)]
js = f"""
pop("#s2-badge", 0.05); slideR("#s2-l1", {T(96)-s0}); slideR("#s2-l2", {T(98)-s0});
out("#s2-badge", {T(100)-s0-0.3}); out("#s2-l1", {T(100)-s0-0.3}); out("#s2-l2", {T(100)-s0-0.3});
rise("#s2-win", {T(100)-s0});
typeAt(".s2-w", {json.dumps(tw)});
out("#s2-win", {T(121)-s0-0.35});
slideL("#s2-k0", {T(121)-s0}); slideL("#s2-k1", {T(122)-s0}); slideL("#s2-k2", {T(123)-s0});
""" + "".join(f'pop("#s2-p{k}", {round(T(125)-s0+k*0.25,2)}); pop("#s2-s{k}", {round(T(132)-s0+k*0.25,2)});' for k in range(3)) + f"""
out("#s2-k0", {d-0.3}); out("#s2-k1", {d-0.3}); out("#s2-k2", {d-0.3});
"""
SFX += [(s0, "whoosh", .55), (T(96), "whoosh-short", .4), (T(100), "whoosh-short", .45), (T(102), "typing", .25), (T(109), "typing", .2), (T(115), "typing", .2),
        (T(121), "whoosh-short", .45), (T(122), "whoosh-short", .35), (T(123), "whoosh-short", .35), (T(125), "pop", .35), (T(132), "pop", .35)]
open(f"{P}/compositions/step2.html", "w").write(scene("step2", d, "", html, js))

# ================================================================= STEP 3 51.7–73.6
s0, d = 51.7, 21.9; S["step3"] = (s0, d)
tiles = [("folder", "<span style=\"font-size:29px\">AIDE<br>ADMINISTRATIVE</span>", T(153)), ("pen", "RÉDACTION", T(157)), ("cap", "FORMATION", T(160)),
         ("route", "ACCOMPA-<br>GNEMENT", T(162)), ("bulb", "CONSEIL", T(165))]
pos = [(70, 350), (560, 350), (70, 580), (560, 580), (315, 810)]
th = ""
for k, ((ic, txt, t), (x, y)) in enumerate(zip(tiles, pos)):
    th += f'<div id="s3-t{k}" class="box abs tile" style="left:{x}px;top:{y}px;width:450px;height:190px">{svg(ICON[ic],100)}<span>{txt}</span></div>'
offers = [("ATELIER", "Salariés en poste", "Monter en compétence"), ("RÉDACTION", "Petites entreprises", "Manque de temps"), ("CONSEIL", "Créateurs", "Éviter les erreurs")]
oh = ""
for k, (t1, cl, pb) in enumerate(offers):
    oh += f"""<div id="s3-o{k}" class="box abs" style="left:{60+k*330}px;top:520px;width:300px;height:500px;padding:22px">
  <div style="background:{OR};color:#fff;border:4px solid #111;font-weight:900;font-size:28px;padding:8px 12px;display:inline-block">SERVICE {k+1}</div>
  <div style="font-weight:900;font-size:34px;margin:18px 0 12px">{t1}</div>
  
  <div id="s3-oc{k}" style="margin-top:26px;display:flex;gap:10px;align-items:flex-start">{svg(ICON['user'],36)}<div style="font-size:28px;font-weight:700;line-height:1.2"><span class="o" style="font-weight:900">CLIENT IDÉAL</span><br>{cl}</div></div>
  <div id="s3-op{k}" style="margin-top:16px;display:flex;gap:10px;align-items:flex-start">{svg(ICON['target'],36)}<div style="font-size:28px;font-weight:700;line-height:1.2"><span class="o" style="font-weight:900">PROBLÈME RÉSOLU</span><br>{pb}</div></div>
</div>"""
html = f"""
{header("s3", 3, "TRANSFORMEZ", "EN IDÉES DE SERVICES")}
{th}
{lbl("s3-dom", "DANS VOTRE DOMAINE", 1150, "k s", 520)}
<div class="abs" style="left:70px;top:330px;width:940px"><div style="font-weight:900;font-size:30px;margin-left:6px" id="s3-bl">ChatGPT</div>
<div id="s3-bar" class="box" style="height:110px;display:flex;align-items:center;gap:18px;padding:0 16px 0 20px;box-shadow:10px 10px 0 #111">{svg(ICON['plus'],50)}<span id="s3-typed" data-full="Propose-moi 3 services concrets" style="color:{OR};font-weight:800;font-size:38px;flex:1"></span>{svg(ICON['send'],72)}</div></div>
{oh}
"""
js = f"""
pop("#s3-badge", 0.05); slideR("#s3-l1", {T(140)-s0}); slideR("#s3-l2", {T(144)-s0});
out("#s3-badge", {T(147)-s0-0.3}); out("#s3-l1", {T(147)-s0-0.3}); out("#s3-l2", {T(147)-s0-0.3});
""" + "".join(f'pop("#s3-t{k}", {round(t[2]-s0,2)});' for k, t in enumerate(tiles)) + f"""
slideR("#s3-dom", {T(167)-s0});
""" + "".join(f'out("#s3-t{k}", {T(170)-s0-0.3});' for k in range(5)) + f"""
out("#s3-dom", {T(170)-s0-0.3});
tl.fromTo("#s3-bl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {T(170)-s0}); rise("#s3-bar", {T(170)-s0});
typeChars("#s3-typed", {T(173)-s0}, {T(178)-s0+0.4});
pop("#s3-o0", {T(176)-s0}); pop("#s3-o1", {T(177)-s0}); pop("#s3-o2", {T(178)-s0});
""" + "".join(f'slideL("#s3-oc{k}", {round(T(184)-s0+k*0.2,2)}); slideL("#s3-op{k}", {round(T(187)-s0+k*0.2,2)});' for k in range(3)) + """
"""
SFX += [(s0, "whoosh", .55), (T(140), "whoosh-short", .4), (T(144), "whoosh-short", .4)] + [(t[2], "pop", .38) for t in tiles]
SFX += [(T(170), "whoosh-short", .45), (T(173), "typing", .3), (T(176), "pop", .35), (T(177), "pop", .35), (T(178), "pop", .35), (T(184), "click-soft", .5), (T(187), "click-soft", .5)]
open(f"{P}/compositions/step3.html", "w").write(scene("step3", d, "", html, js))

# ================================================================= WARN 73.6–90.65
s0, d = 73.6, 17.05; S["warn"] = (s0, d)
checks = [("DISCUTEZ AVEC DES CLIENTS", T(220), T(224)), ("IDENTIFIEZ LEURS BESOINS", T(225), T(227)), ("SONT-ILS PRÊTS À PAYER ?", T(229), T(234))]
ckh = ""
for k, (txt, ta, tc) in enumerate(checks):
    ckh += f'<div id="w-r{k}" style="display:flex;align-items:center;gap:24px;margin:26px 0;font-weight:900;font-size:36px"><div style="position:relative;width:76px;height:76px;border:5px solid #111;border-radius:12px;flex:none"><div id="w-c{k}" class="abs" style="left:-6px;top:-6px">{svg(ICON["check"],78)}</div></div>{txt}</div>'
html = f"""
<div class="row" style="top:350px"><div id="w-att" class="lbl xl" style="display:flex;align-items:center;gap:22px">{svg(ICON['warning'],90)}ATTENTION</div></div>
<div id="w-b1" class="box abs" style="left:70px;top:560px;width:380px;height:330px;text-align:center;padding-top:30px">{svg(ICON['bulb'],140)}<div style="font-weight:900;font-size:38px;margin-top:16px;line-height:1.1">IDÉE<br>DE L'IA</div></div>
<div id="w-ne" class="abs" style="left:478px;top:620px;font-weight:900;font-size:170px;line-height:1;color:{OR};-webkit-text-stroke:5px #111">≠</div>
<div id="w-b2" class="box abs" style="left:630px;top:560px;width:380px;height:330px;text-align:center;padding-top:30px">{svg(ICON['chart'],140)}<div style="font-weight:900;font-size:38px;margin-top:16px;line-height:1.1">BONNE<br>OPPORTUNITÉ</div></div>
{lbl("w-av", "AVANT D'INVESTIR", 350, "w")}
<div id="w-i1" class="box abs" style="left:150px;top:500px;width:360px;height:280px;text-align:center;padding-top:30px">{svg(ICON['hourglass'],130)}<div style="font-weight:900;font-size:40px;margin-top:12px">TEMPS</div></div>
<div id="w-i2" class="box abs" style="left:570px;top:500px;width:360px;height:280px;text-align:center;padding-top:30px">{svg(ICON['coin'],130)}<div style="font-weight:900;font-size:40px;margin-top:12px">ARGENT</div></div>
{lbl("w-ver", "VÉRIFIEZ LA DEMANDE", 860)}
<div id="w-list" class="box abs" style="left:70px;top:360px;width:940px;padding:20px 40px">
  <div style="font-weight:900;font-size:30px;letter-spacing:.06em;color:{OR}">✔ CHECK-LIST AVANT DE VOUS LANCER</div>{ckh}</div>
"""
js = f"""
pop("#w-att", 0.05); wiggle("#w-att svg", 0.4, 7);
slideL("#w-b1", {T(196)-s0}); pop("#w-ne", {T(200)-s0}); slideR("#w-b2", {T(204)-s0});
tl.fromTo("#w-ne", {{ rotation: -20 }}, {{ rotation: 0, duration: 0.4, ease: "back.out(3)" }}, {T(200)-s0});
out("#w-att", {T(207)-s0-0.3}); out("#w-b1", {T(207)-s0-0.3}); out("#w-ne", {T(207)-s0-0.3}); out("#w-b2", {T(207)-s0-0.3});
pop("#w-av", {T(207)-s0}); pop("#w-i1", {T(210)-s0}); pop("#w-i2", {T(213)-s0});
pop("#w-ver", {T(214)-s0}); wiggle("#w-ver", {T(218)-s0}, 3);
out("#w-av", {T(220)-s0-0.35}); out("#w-i1", {T(220)-s0-0.35}); out("#w-i2", {T(220)-s0-0.35}); out("#w-ver", {T(220)-s0-0.35});
rise("#w-list", {T(220)-s0-0.1});
""" + "".join(f'slideL("#w-r{k}", {round(c[1]-s0,2)}); pop("#w-c{k}", {round(c[2]-s0,2)});' for k, c in enumerate(checks)) + f"""
out("#w-list", {d-0.3});
"""
SFX += [(s0, "error", .35), (T(196), "whoosh-short", .4), (T(200), "pop", .4), (T(204), "whoosh-short", .4), (T(207), "whoosh", .45), (T(210), "pop", .35), (T(213), "pop", .35), (T(214), "pop", .45),
        (T(220), "whoosh-short", .4)] + [(c[2], "click-soft", .6) for c in checks]
open(f"{P}/compositions/warn.html", "w").write(scene("warn", d, "", html, js))

# ================================================================= ATOUT 90.65–101.3
s0, d = 90.65, 10.65; S["atout"] = (s0, d)
html = f"""
<div id="a-tro" class="abs" style="left:390px;top:330px">{svg(ICON['trophy'],300)}</div>
{lbl("a-l1", "VOTRE EXPÉRIENCE", 680, "w")}
{lbl("a-l2", "= UN VÉRITABLE ATOUT", 800)}
<div id="a-c1" class="box abs" style="left:60px;top:360px;width:450px;height:560px;padding:30px;text-align:center">
  <div style="background:{OR};color:#fff;border:4px solid #111;font-weight:900;font-size:44px;padding:8px 0">L'IA</div>
  <div style="margin:30px 0">{svg(ICON['magnifier'],150)}</div>
  <div style="font-weight:900;font-size:36px;line-height:1.2">REPÈRE DES<br><span class="o">POSSIBILITÉS</span></div></div>
<div id="a-c2" class="box abs" style="left:570px;top:360px;width:450px;height:560px;padding:30px;text-align:center">
  <div style="background:#111;color:#fff;border:4px solid #111;font-weight:900;font-size:44px;padding:8px 0">VOUS</div>
  <div style="margin:30px 0">{svg(ICON['check'],150)}</div>
  <div style="font-weight:900;font-size:36px;line-height:1.2">VÉRIFIEZ CE QUI<br>EST <span class="o">VIABLE</span></div></div>
<div id="a-st" class="abs" style="left:650px;top:860px;border:6px solid {OR};color:{OR};font-weight:900;font-size:50px;padding:6px 20px;border-radius:10px;background:#fff">VIABLE ✓</div>
"""
js = f"""
pop("#a-tro", {T(238)-s0}, 0.5); tl.fromTo("#a-tro", {{ rotation: -8 }}, {{ rotation: 8, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {T(238)-s0+0.5});
pop("#a-l1", {T(239)-s0}); pop("#a-l2", {T(243)-s0});
out("#a-tro", {T(246)-s0-0.3}); out("#a-l1", {T(246)-s0-0.3}); out("#a-l2", {T(246)-s0-0.3});
slideL("#a-c1", {T(246)-s0}); slideR("#a-c2", {T(259)-s0});
tl.fromTo("#a-st", {{ opacity: 0, scale: 2.4, rotation: -12 }}, {{ opacity: 1, scale: 1, rotation: -12, duration: 0.3, ease: "power4.in" }}, {T(267)-s0});
out("#a-c1", {d-0.3}); out("#a-c2", {d-0.3}); out("#a-st", {d-0.3});
"""
SFX += [(s0, "whoosh", .5), (T(238), "sparkle", .45), (T(243), "pop", .45), (T(246), "whoosh-short", .4), (T(259), "whoosh-short", .4), (T(267)+0.28, "pop", .55)]
open(f"{P}/compositions/atout.html", "w").write(scene("atout", d, "", html, js))

# ================================================================= CTA 101.3–113.2
s0, d = 101.3, TOTAL - 101.3; S["cta"] = (s0, d)
html = f"""
{lbl("c-l", "VOUS VOULEZ APPRENDRE ?", 350)}
{lbl("c-1", "✔ DÉVELOPPER VOS COMPÉTENCES", 500, "w s")}
{lbl("c-2", "✔ PRÉPARER UNE RECONVERSION", 610, "w s")}
{lbl("c-3", "✔ EXPLORER DE NOUVELLES PISTES", 720, "w s")}
<div class="row" style="top:850px"><div id="c-gpt" class="lbl k s" style="display:flex;align-items:center;gap:14px">{svg(ICON['sparkle'],48).replace('stroke="#111"','stroke="#fff"')}AVEC CHATGPT</div></div>
{lbl("c-big", "CONTACTEZ-MOI", 380, "xl")}
<div id="c-msg" class="box abs" style="left:70px;top:560px;width:940px;padding:26px">
  <div style="display:flex;align-items:center;gap:18px;font-weight:900;font-size:30px">{svg(ICON['chat'],60)}MESSAGE PRIVÉ </div>
  <div style="margin-top:20px;border:4px solid #111;border-radius:50px;height:100px;display:flex;align-items:center;padding:0 14px 0 30px">
    <span id="c-typed" data-full="Je veux en discuter !" style="color:{OR};font-weight:900;font-size:44px;flex:1"></span>{svg(ICON['send'],72)}</div>
</div>
{lbl("c-dis", "POUR EN DISCUTER", 860, "w")}
"""
js = f"""
pop("#c-l", {T(271)-s0-0.3}); slideL("#c-1", {T(276)-s0}); slideL("#c-2", {T(279)-s0}); slideL("#c-3", {T(283)-s0}); pop("#c-gpt", {T(274)-s0});
out("#c-l", {T(288)-s0-0.3}); out("#c-1", {T(288)-s0-0.3}); out("#c-2", {T(288)-s0-0.3}); out("#c-3", {T(288)-s0-0.3}); out("#c-gpt", {T(288)-s0-0.3});
pop("#c-big", {T(288)-s0}, 0.5); rise("#c-msg", {T(288)-s0+0.3});
typeChars("#c-typed", {T(288)-s0+0.7}, {T(288)-s0+2.0});
pop("#c-dis", {T(289)-s0+0.2});
tl.fromTo("#c-big", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {T(288)-s0+1.0});
"""
SFX += [(s0, "whoosh", .5), (T(276), "pop", .35), (T(279), "pop", .35), (T(283), "pop", .35), (T(288), "sparkle", .5), (T(288)+0.7, "typing", .3)]
open(f"{P}/compositions/cta.html", "w").write(scene("cta", d, "", html, js))

# ================================================================= AVATAR overlay
moves = [(3.3, -230, 1), (5.75, 0, 1), (11.5, 240, -1), (15.7, -240, 1), (34.9, 240, -1), (51.7, -240, 1), (73.6, 0, 1), (101.3, 0, 1)]
mjs = ""
for t, x, sx in moves:
    mjs += f'tl.to("#av-x", {{ x: {x}, scaleX: {sx}, duration: 0.5, ease: "power3.inOut" }}, {t});\n'
    mjs += f'tl.to("#av-hop", {{ y: -70, duration: 0.22, ease: "power2.out" }}, {t}).to("#av-hop", {{ y: 0, duration: 0.45, ease: "bounce.out" }}, {t+0.22});\n'
for t in [T(245)-0.3, T(288)]:
    mjs += f'tl.to("#av-hop", {{ y: -90, scale: 1.05, duration: 0.22, ease: "power2.out" }}, {t}).to("#av-hop", {{ y: 0, scale: 1, duration: 0.5, ease: "bounce.out" }}, {t+0.22});\n'
# Poses disponibles : voir references/poses-catalogue.md (17 poses). Seules celles de `sched` sont chargées.
sched = [(3.3, "think"), (5.75, "point"), (18.8, "laptop"), (34.9, "think"), (38.1, "laptop"), (46.2, "point"), (51.7, "think"),
         (55.9, "point"), (64.9, "laptop"), (73.6, "shock"), (79.2, "think"), (84.0, "point"), (90.65, "base"), (101.3, "point"), (109.4, "wave")]
POSES = ["base"] + sorted({n for _, n in sched} - {"base"})
imgs = "".join(f'<img id="av-{n}" class="av-img" src="assets/avatar_{n}.png" alt="avatar {n}">' for n in POSES)
cur = "base"
for t, n in sched:
    mjs += f'tl.set("#av-{cur}", {{ opacity: 0 }}, {t}); tl.set("#av-{n}", {{ opacity: 1 }}, {t});\n'
    mjs += f'tl.fromTo("#av-pop", {{ scaleX: 1.08, scaleY: 0.9 }}, {{ scaleX: 1, scaleY: 1, duration: 0.35, ease: "back.out(3)"{"" if cur == "base" and t == sched[0][0] else ", immediateRender: false"} }}, {t});\n'
    cur = n
avatar = f"""<template>
  <style>
    #root{{position:absolute;inset:0;pointer-events:none}}
    #av-x{{position:absolute;left:241px;top:1058px;width:598px;height:880px}}
    #av-hop,#av-bob,#av-pop{{position:relative;width:100%;height:100%;transform-origin:50% 100%}}
    .av-img{{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:contain;object-position:50% 100%;opacity:0}}
    #av-base{{opacity:1}}
  </style>
  <div id="root" data-composition-id="avatar" data-width="1080" data-height="1920" data-layout-allow-overflow data-layout-allow-overlap>
    <div id="av-x"><div id="av-hop"><div id="av-bob"><div id="av-pop">{imgs}</div></div></div></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#av-x", {{ y: 500 }}, {{ y: 0, duration: 0.5, ease: "back.out(1.4)" }}, 0);
    tl.fromTo("#av-bob", {{ scaleY: 1, rotation: -1.2 }}, {{ scaleY: 1.025, rotation: 1.2, duration: 0.9, yoyo: true, repeat: {int(TOTAL/0.9)}, ease: "sine.inOut" }}, 0);
{mjs}
    tl.fromTo("#av-hop", {{ rotation: -5 }}, {{ rotation: 5, duration: 0.09, yoyo: true, repeat: 7, ease: "sine.inOut" }}, 73.7).to("#av-hop", {{ rotation: 0, duration: 0.1 }}, 74.45);
    tl.set({{}}, {{}}, {TOTAL});
    window.__timelines["avatar"] = tl;
  </script>
</template>
"""
open(f"{P}/compositions/avatar.html", "w").write(avatar)

# ================================================================= CAPTIONS
FIX = {2: "20", 52: "20", 44: "identifiez", 96: "trouvez", 140: "transformez", 144: "idées", 146: "services.", 93: "précisions.",
       199: "l'IA", 246: "L'IA", 230: "s'ils", 231: "seraient", 232: "prêts", 49: "ChatGPT :", 101: "ensuite :"}
txt = [FIX.get(i, w["text"]) for i, w in enumerate(W)]
txt = [t[:-1] + " ?" if t.endswith("?") and not t.endswith(" ?") else t for t in txt]
KEY = {"20", "expérience", "vendre", "emploi", "compétences", "complémentaire", "l'intelligence", "chatgpt", "étape,", "compétences.", "clients",
       "services", "attention,", "demande.", "atout.", "contactez-moi", "payer", "besoins", "trois", "viables."}
groups, cur = [], []
for i, w in enumerate(W):
    cur.append(i)
    chars = sum(len(txt[j]) for j in cur) + len(cur) - 1
    nxt = i + 1 if i + 1 < len(W) else None
    brk = (txt[i][-1] in ".,?:!" or len(cur) >= 3 or nxt is None
           or chars + len(txt[nxt]) + 1 > 19 or W[nxt]["start"] - w["end"] > 0.15)
    if brk:
        groups.append(cur); cur = []
cap_html, cap_js = "", ""
for g, idx in enumerate(groups):
    st = max(0.12, W[idx[0]]["start"] - 0.04)
    en = W[groups[g + 1][0]]["start"] - 0.04 if g + 1 < len(groups) else TOTAL - 0.2
    en = min(en, W[idx[-1]]["end"] + 0.7)
    words = [txt[j] for j in idx]
    keyed = [k for k, t in enumerate(words) if t.lower().strip(",.") in KEY or t.lower() in KEY]
    hi = keyed[0] if keyed else max(range(len(words)), key=lambda k: len(words[k]))
    if len(words[hi]) < 4 and not keyed:
        hi = -1
    chars = len(" ".join(words))
    fs = min(70, int(940 / (chars * 0.78)))
    inner = " ".join(f'<span class="o">{t}</span>' if k == hi else t for k, t in enumerate(words))
    cap_html += f'    <div id="cg{g}" class="cg" style="font-size:{fs}px">{inner}</div>\n'
    cap_js += f'cap("#cg{g}", {st:.2f}, {en:.2f});\n'
captions = f"""<template>
  <style>
    #root{{position:absolute;inset:0;font-family:'Montserrat',sans-serif}}
    .cg{{position:absolute;left:0;top:200px;width:1080px;text-align:center;font-weight:900;text-transform:uppercase;color:#111;line-height:1.1;opacity:0;padding:0 70px;letter-spacing:.005em}}
    .cg .o{{color:{OR}}}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-layout-allow-overflow>
{cap_html}  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const cap = (s, a, b) => {{
      tl.fromTo(s, {{ opacity: 0, scale: 0.86, y: 10 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.12, ease: "power3.out" }}, a);
      tl.set(s, {{ opacity: 0, visibility: "hidden" }}, b);
    }};
{cap_js}
    tl.set({{}}, {{}}, {TOTAL});
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
open(f"{P}/compositions/captions.html", "w").write(captions)

# ================================================================= INDEX
SFXLEN = {"pop": .72, "whoosh": .57, "whoosh-short": .57, "typing": 1.54, "sparkle": 1.8, "click-soft": .36, "error": 1.62, "riser": 10.0}
hosts = ""
for k, (cid, (st, du)) in enumerate(S.items()):
    hosts += f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{st}" data-duration="{round(du,2)}" data-track-index="{1 + k % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{2+k}"></div>\n'
sfx_html = ""
SFX.sort()
for k, (t, f, v) in enumerate(SFX):
    sfx_html += f'      <audio id="sfx{k}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t:.2f}" data-duration="{SFXLEN[f]}" data-track-index="{30 + k % 3}" data-volume="{v}"></audio>\n'
index = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #ffffff; }}
      #root {{ width: 100%; height: 100%; position: relative; font-family: 'Montserrat', sans-serif;
        background-color: #ffffff;
        background-image: linear-gradient(#f3f3f3 2px, transparent 2px), linear-gradient(90deg, #f3f3f3 2px, transparent 2px);
        background-size: 72px 72px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{hosts}      <div id="avatar" data-composition-id="avatar" data-composition-src="compositions/avatar.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:20"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:30"></div>
      <audio id="vo" class="clip" src="assets/voice.mp3" data-start="0" data-duration="111.07" data-track-index="20" data-volume="1"></audio>
      <audio id="bgm" class="clip" src="assets/music.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="21" data-volume="0.13"></audio>
{sfx_html}    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(f"{P}/index.html", "w").write(index)
print("groups", len(groups), "sfx", len(SFX))
