# Vidéo « 5 raccourcis ChatGPT » — construite avec le skill video-avatar-motion.
# Usage : python3 gen2.py <template_generate_example.py> <dossier_projet_video>
import json, os, sys, unicodedata

TEMPLATE, P = sys.argv[1], sys.argv[2]
src = open(TEMPLATE, encoding="utf-8").read()
prefix = src.split("# ================================================================= HOOK")[0]
sys.argv = [TEMPLATE, P]
exec(prefix)  # ICON, CSS, JS, svg, icon, scene, lbl, W, T, S, SFX, OR, TOTAL…

VOICE_LEN = float(os.environ.get("VOICE_LEN", "0")) or W[-1]["end"]
TOTAL = round(VOICE_LEN + 1.6, 2)

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if c.isalnum())

def I(word, after=0.0):
    k = norm(word)
    for i, x in enumerate(W):
        if x["start"] >= after - 0.05 and norm(x["text"]).startswith(k):
            return i
    raise SystemExit(f"repère introuvable : {word!r} après {after}")

def A(word, after=0.0, end=False):
    for w in word.split("|"):  # alternatives : "écris|décrits"
        try:
            x = W[I(w, after)]; break
        except SystemExit:
            continue
    else:
        raise SystemExit(f"repère introuvable : {word!r} après {after}")
    return round(x["end"] if end else x["start"], 2)

ICON.update({
    "lines": '<rect x="10" y="12" width="80" height="76" rx="8"/><path d="M24 32h52M24 46h52M24 60h52M24 74h30"/>',
    "proscons": '<rect x="8" y="12" width="84" height="76" rx="8"/><path d="M50 12v76"/><path d="M20 38l7 7 12-14" stroke="#E8532F" stroke-width="8"/><path d="M62 30l16 16M78 30L62 46"/>',
    "bullets": '<circle cx="20" cy="26" r="7" fill="#E8532F"/><circle cx="20" cy="50" r="7" fill="#E8532F"/><circle cx="20" cy="74" r="7" fill="#E8532F"/><path d="M38 26h50M38 50h50M38 74h40"/>',
    "table": '<rect x="8" y="14" width="84" height="72" rx="6"/><path d="M8 36h84M8 60h84M38 14v72M66 14v72"/><rect x="8" y="14" width="84" height="22" fill="#E8532F"/>',
    "plan": '<circle cx="22" cy="20" r="10" fill="#E8532F"/><circle cx="22" cy="50" r="10" fill="#E8532F"/><circle cx="22" cy="80" r="10" fill="#E8532F"/><path d="M22 30v10M22 60v10M42 20h46M42 50h40M42 80h46"/>',
    "cursor": '<path d="M20 8l60 44-26 6 14 30-12 6-14-30-22 18z" fill="#fff"/>',
    "eye": '<path d="M6 50c20-30 68-30 88 0-20 30-68 30-88 0z" fill="#fff"/><circle cx="50" cy="50" r="16" fill="#E8532F"/><circle cx="50" cy="50" r="6" fill="#111"/>',
    "doc": '<path d="M18 6h46l18 18v70H18z" fill="#fff"/><path d="M64 6v18h18"/><path d="M30 44h40M30 58h40M30 72h26"/>',
    "lock": '<rect x="18" y="44" width="64" height="48" rx="8" fill="#E8532F"/><path d="M32 44V30a18 18 0 0 1 36 0v14"/>',
    "star": '<path d="M50 6l13 28 31 4-23 21 6 31-27-15-27 15 6-31L6 38l31-4z" fill="#E8532F"/>',
    "arrow": '<path d="M8 50h74M60 28l24 22-24 22" stroke-width="10"/>',
})

EXTRA_CSS = f"""
.bar{{height:110px;display:flex;align-items:center;gap:16px;padding:0 14px 0 18px;box-shadow:10px 10px 0 #111}}
.bar .typed{{color:{OR};font-weight:800;font-size:31px;flex:1;white-space:nowrap;overflow:hidden}}
.card-t{{font-weight:900;font-size:34px;text-transform:uppercase}}
.gpt{{display:flex;align-items:center;gap:12px;font-weight:900;font-size:28px;margin-bottom:16px}}
.gpt i{{width:40px;height:40px;border-radius:50%;background:#111;display:inline-block}}
"""

def badge_bar(p, n, cmd):
    return f"""<div id="{p}-badge" class="badge abs" style="left:70px;top:330px"><small>NUMÉRO</small><b>{n}</b></div>
<div class="abs" style="left:280px;top:340px;width:730px"><div style="font-weight:900;font-size:28px;margin:0 0 6px 6px">ChatGPT</div>
<div id="{p}-bar" class="box bar">{svg(ICON['plus'],48)}<span id="{p}-typed" class="typed" data-full="{cmd}"></span>{svg(ICON['send'],70)}</div></div>"""

def side_chip(id_, text, ic, left):
    return f'<div id="{id_}" class="lbl w s abs" style="left:{left}px;top:1150px;display:flex;align-items:center;gap:14px;font-size:34px">{svg(ICON[ic],48)}{text}</div>'

# ------------------------------------------------------------------ repères (sur la voix réelle)
n1 = A("numéro"); n2 = A("numéro", n1 + 1); n3 = A("numéro", n2 + 1); n4 = A("numéro", n3 + 1)
i_last = I("dernier", n4 + 1); n5 = round(W[i_last - 2]["start"], 2)  # « Et le dernier »
n5num = A("numéro", n5)
ast = A("petite", n5num); cta = A("tu", A("tableau", ast) + 0.1)
starts = {"hook": 0.0, "n1": n1, "n2": n2, "n3": n3, "n4": n4, "n5": n5, "astuce": ast, "cta": cta}
names = list(starts)
for k, nm in enumerate(names):
    st = starts[nm]; en = starts[names[k + 1]] if k + 1 < len(names) else TOTAL
    S[nm] = (round(st, 2), round(en - st, 2))
print("scènes", S)

def L(t, nm):  # temps absolu -> local à la scène
    return round(t - S[nm][0], 2)

# ================================================================= HOOK
nm = "hook"; d = S[nm][1]
mini = [("lines", "DÉVELOPPE"), ("proscons", "POUR / CONTRE"), ("bullets", "LISTE"), ("table", "TABLEAU"), ("plan", "PLAN")]
mh = "".join(f'<div id="h-m{k}" class="box abs" style="left:{60+k*196}px;top:540px;width:176px;height:230px;text-align:center;padding-top:16px"><div style="font-weight:900;font-size:30px;color:{OR}">{k+1}</div>{svg(ICON[ic],96)}<div style="font-weight:900;font-size:22px;margin-top:8px" data-layout-ignore>{t}</div></div>' for k, (ic, t) in enumerate(mini))
html = f"""
<div class="abs" style="left:70px;top:330px;width:940px"><div style="font-weight:900;font-size:28px;margin:0 0 6px 6px">ChatGPT</div>
<div id="h-bar" class="box bar">{svg(ICON['plus'],48)}<span id="h-typed" class="typed" data-full="Comment trouver mes premiers clients ?"></span><div id="h-send">{svg(ICON['send'],70)}</div></div></div>
<div id="h-cur" class="abs" style="left:960px;top:470px">{svg(ICON['cursor'],80)}</div>
{mh}
{lbl("h-clic", "UN SEUL CLIC SUFFIT", 830)}
{lbl("h-fin", "RESTE JUSQU'À LA FIN", 830, "w")}
<div id="h-star" class="abs" style="left:880px;top:470px">{svg(ICON['star'],110)}</div>
{lbl("h-top", "LE PLUS PUISSANT", 930, "k")}
"""
c5, cd, seul, clic, reste, puis = A("cinq"), A("différent", end=True), A("seul"), A("clic"), A("reste"), A("puissant")
js = f"""
tl.fromTo("#h-bar", {{ scale: 0.95 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, 0);
typeChars("#h-typed", 0.1, 1.1);
""" + "".join(f'pop("#h-m{k}", {round(c5 + k*(cd-c5)/5, 2)});' for k in range(5)) + f"""
pop("#h-clic", {seul});
tl.fromTo("#h-cur", {{ x: 0, y: 300, opacity: 0 }}, {{ x: -10, y: 0, opacity: 1, duration: 0.45, ease: "power2.out" }}, {clic-0.5});
tl.fromTo("#h-cur", {{ scale: 1 }}, {{ scale: 0.8, duration: 0.1, yoyo: true, repeat: 1 }}, {clic});
tl.fromTo("#h-send", {{ scale: 1 }}, {{ scale: 1.25, duration: 0.12, yoyo: true, repeat: 1 }}, {clic});
out("#h-clic", {reste-0.3}); out("#h-cur", {reste-0.3}); pop("#h-fin", {reste});
""" + "".join(f'tl.to("#h-m{k}", {{ opacity: 0.35, duration: 0.3 }}, {puis-0.2});' for k in range(4)) + f"""
tl.to("#h-m4", {{ scale: 1.18, y: -20, duration: 0.4, ease: "back.out(3)" }}, {puis-0.2});
pop("#h-star", {puis}); tl.fromTo("#h-star", {{ rotation: 0 }}, {{ rotation: 90, duration: 1.2 }}, {puis+0.3});
out("#h-fin", {puis-0.25}); pop("#h-top", {puis});
"""
SFX += [(0.1, "typing", .3), (seul, "pop", .4), (clic, "click-soft", .7), (reste, "whoosh-short", .4), (puis, "sparkle", .5)] + [(round(c5 + k*(cd-c5)/5, 2), "pop", .3) for k in range(5)]
open(f"{P}/compositions/hook.html", "w").write(scene(nm, d, EXTRA_CSS, html, js))

# ================================================================= N1 développe
nm = "n1"; s0, d = S[nm]
ta, dev, ex = A("ta", n1), A("phrase", n1), A("vrai", n1)
html = f"""
{badge_bar("a", 1, "Développe et ajoute des détails")}
<div id="a-card" class="box abs" style="left:70px;top:560px;width:940px;height:470px;padding:26px 30px">
  <div class="gpt"><i></i>Réponse de ChatGPT</div>
  <div id="a-short" class="abs" style="left:30px;top:96px;font-size:36px;font-weight:700;background:#F1F1F1;border-radius:24px;padding:18px 26px">Publie sur LinkedIn.</div>
  <div id="a-long" class="abs" style="left:30px;top:96px;width:870px;font-size:30px;font-weight:600;line-height:1.38;background:#F1F1F1;border-radius:24px;padding:20px 26px">Publie <b class="o">3 fois par semaine</b> sur LinkedIn : raconte le problème d'un client, ta solution et le résultat obtenu. Commente aussi les posts de tes futurs clients pour te faire remarquer.</div>
  <div id="a-e1" class="abs" style="left:30px;top:330px;font-size:28px;font-weight:700"><span class="lbl s" style="font-size:28px;padding:6px 12px;box-shadow:5px 5px 0 #111">EXEMPLE</span>&nbsp; Coach : l'avant / après d'un client</div>
  <div id="a-e2" class="abs" style="left:30px;top:395px;font-size:28px;font-weight:700"><span class="lbl s" style="font-size:28px;padding:6px 12px;box-shadow:5px 5px 0 #111">EXEMPLE</span>&nbsp; Comptable : 3 erreurs fréquentes</div>
</div>
{side_chip("a-chip", "+ DE DÉTAILS", "lines", 600)}
"""
js = f"""
pop("#a-badge", 0.05); rise("#a-bar", 0.2); typeChars("#a-typed", 0.5, {L(A('détails', n1, True), nm)});
rise("#a-card", {L(ta, nm)-0.2}); pop("#a-short", {L(ta, nm)});
out("#a-short", {L(dev, nm)}); tl.fromTo("#a-long", {{ opacity: 0, scaleY: 0.3, transformOrigin: "50% 0%" }}, {{ opacity: 1, scaleY: 1, duration: 0.45, ease: "power3.out" }}, {L(dev, nm)+0.1});
slideL("#a-e1", {L(ex, nm)}); slideL("#a-e2", {L(ex, nm)+0.5}); slideR("#a-chip", {L(dev, nm)+0.4});
out("#a-card", {d-0.3}); out("#a-chip", {d-0.3}); out("#a-badge", {d-0.3}); out("#a-bar", {d-0.3});
"""
SFX += [(s0, "whoosh", .5), (s0+0.5, "typing", .3), (ta, "pop", .35), (dev, "whoosh-short", .4), (ex, "pop", .35)]
open(f"{P}/compositions/n1.html", "w").write(scene(nm, d, EXTRA_CSS, html, js))

# ================================================================= N2 pour / contre
nm = "n2"; s0, d = S[nm]
vois, deux, decide = A("vois", n2), A("deux", n2 + 1), A("décides", n2)
pros = ["Lancement rapide", "Peu d'investissement", "Horaires flexibles"]
cons = ["Revenus irréguliers", "Prospection à faire", "Moins de temps libre"]
col = lambda items, p, mark: "".join(f'<div id="{p}{k}" style="display:flex;gap:12px;align-items:center;margin:20px 0;font-size:30px;font-weight:700">{mark}{t}</div>' for k, t in enumerate(items))
okm = f'<span style="color:{OR};font-weight:900;font-size:36px">✓</span>'
nom = '<span style="font-weight:900;font-size:36px">✕</span>'
html = f"""
{badge_bar("b", 2, "Compare le pour et le contre")}
<div id="b-card" class="box abs" style="left:70px;top:560px;width:940px;height:470px;padding:24px 30px">
  <div class="card-t" style="font-size:28px;margin-bottom:14px">Lancer une activité en plus de mon emploi</div>
  <div style="display:flex;gap:30px">
    <div style="flex:1"><div style="background:{OR};color:#fff;font-weight:900;font-size:32px;padding:8px 16px;border:4px solid #111">POUR</div>{col(pros, "b-p", okm)}</div>
    <div style="flex:1"><div style="background:#111;color:#fff;font-weight:900;font-size:32px;padding:8px 16px;border:4px solid #111">CONTRE</div>{col(cons, "b-c", nom)}</div>
  </div>
</div>
<div id="b-st" class="abs" style="left:560px;top:975px;border:6px solid {OR};color:{OR};font-weight:900;font-size:46px;padding:6px 18px;border-radius:10px;background:#fff">TU DÉCIDES ✓</div>
"""
js = f"""
pop("#b-badge", 0.05); rise("#b-bar", 0.2); typeChars("#b-typed", 0.5, {L(A('contre', n2, True), nm)});
rise("#b-card", 0.9);
""" + "".join(f'slideL("#b-p{k}", {round(L(vois, nm) + k*0.35, 2)}); slideR("#b-c{k}", {round(L(deux, nm) + k*0.35, 2)});' for k in range(3)) + f"""
tl.fromTo("#b-st", {{ opacity: 0, scale: 2.2, rotation: -10 }}, {{ opacity: 1, scale: 1, rotation: -10, duration: 0.3, ease: "power4.in" }}, {L(decide, nm)});
out("#b-card", {d-0.3}); out("#b-st", {d-0.3}); out("#b-badge", {d-0.3}); out("#b-bar", {d-0.3});
"""
SFX += [(s0, "whoosh", .5), (s0+0.5, "typing", .3), (vois, "pop", .3), (deux, "pop", .3), (decide+0.28, "pop", .55)]
open(f"{P}/compositions/n2.html", "w").write(scene(nm, d, EXTRA_CSS, html, js))

# ================================================================= N3 liste à puces
nm = "n3"; s0, d = S[nm]
tout, oeil = A("tout", n3), A("coup", n3)
items = ["Définis ton client idéal", "Choisis un seul réseau social", "Publie 3 fois par semaine", "Contacte 5 personnes par jour"]
ih = "".join(f'<div id="c-i{k}" style="display:flex;gap:18px;align-items:center;margin:22px 0;font-size:34px;font-weight:700"><span style="width:22px;height:22px;border-radius:50%;background:{OR};border:3px solid #111;flex:none"></span>{t}</div>' for k, t in enumerate(items))
html = f"""
{badge_bar("c", 3, "Fais une liste à puces")}
<div id="c-card" class="box abs" style="left:70px;top:560px;width:940px;height:470px;padding:26px 36px">
  <div class="card-t">Trouver des clients : l'essentiel</div>{ih}</div>
{side_chip("c-chip", "EN UN COUP D'ŒIL", "eye", 520)}
"""
js = f"""
pop("#c-badge", 0.05); rise("#c-bar", 0.2); typeChars("#c-typed", 0.5, {L(A('puce', n3, True), nm)});
rise("#c-card", 1.0);
""" + "".join(f'slideL("#c-i{k}", {round(1.3 + k*0.45, 2)});' for k in range(4)) + f"""
slideR("#c-chip", {L(A("lisible", n3), nm)});
out("#c-card", {d-0.3}); out("#c-chip", {d-0.3}); out("#c-badge", {d-0.3}); out("#c-bar", {d-0.3});
"""
SFX += [(s0, "whoosh", .5), (s0+0.5, "typing", .3)] + [(round(s0 + 1.3 + k*0.45, 2), "pop", .3) for k in range(4)] + [(A("lisible", n3), "sparkle", .4)]
open(f"{P}/compositions/n3.html", "w").write(scene(nm, d, EXTRA_CSS, html, js))

# ================================================================= N4 tableau
nm = "n4"; s0, d = S[nm]
comp, lig_end = A("tu", n4), A("ligne", A("par", n4), True)
rows = [("CANAL", "COÛT", "DÉLAI"), ("LinkedIn", "Gratuit", "1 mois"), ("Bouche-à-oreille", "Gratuit", "2 mois"), ("Publicité", "50 €/mois", "1 semaine"), ("Partenariats", "Gratuit", "3 mois")]
rh = ""
for k, r in enumerate(rows):
    head = k == 0
    cells = "".join(f'<div style="flex:{1.6 if j==0 else 1};padding:14px 18px;border-left:{0 if j==0 else 4}px solid #111">{c}</div>' for j, c in enumerate(r))
    rh += f'<div id="d-r{k}" style="display:flex;border-bottom:4px solid #111;font-size:{30 if head else 30}px;font-weight:{900 if head else 700};{"background:"+OR+";color:#fff;" if head else ""}">{cells}</div>'
html = f"""
{badge_bar("d", 4, "Convertis en tableau")}
<div id="d-card" class="box abs" style="left:70px;top:580px;width:940px;overflow:hidden;padding:0">{rh}</div>
{side_chip("d-chip", "LIGNE PAR LIGNE", "table", 70)}
"""
js = f"""
pop("#d-badge", 0.05); rise("#d-bar", 0.2); typeChars("#d-typed", 0.5, {L(A('tableau', n4, True), nm)});
rise("#d-card", 1.0); tl.fromTo("#d-r0", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 1.1);
""" + "".join(f'slideL("#d-r{k}", {round(L(comp, nm) + (k-1)*(lig_end-comp)/4, 2)});' for k in range(1, 5)) + f"""
slideL("#d-chip", {L(A('ligne', n4), nm)});
out("#d-card", {d-0.3}); out("#d-chip", {d-0.3}); out("#d-badge", {d-0.3}); out("#d-bar", {d-0.3});
"""
SFX += [(s0, "whoosh", .5), (s0+0.5, "typing", .3)] + [(round(comp + (k-1)*(lig_end-comp)/4, 2), "click-soft", .5) for k in range(1, 5)]
open(f"{P}/compositions/n4.html", "w").write(scene(nm, d, EXTRA_CSS, html, js))

# ================================================================= N5 plan
nm = "n5"; s0, d = S[nm]
march, etp_end = A("réponse", n5), A("suivre", n5, True)
steps = ["Définis ton offre", "Liste 10 prospects", "Propose un appel découverte", "Signe ton premier client"]
sh = "".join(f'<div id="e-s{k}" style="display:flex;gap:22px;align-items:center;margin:0 0 26px;position:relative"><div style="width:70px;height:70px;border-radius:50%;background:{OR};border:4px solid #111;color:#fff;font-weight:900;font-size:36px;display:flex;align-items:center;justify-content:center;flex:none">{k+1}</div><div><div style="font-weight:900;font-size:28px;color:{OR}">ÉTAPE {k+1}</div><div style="font-weight:800;font-size:32px">{t}</div></div></div>' for k, t in enumerate(steps))
html = f"""
<div class="row" style="top:420px"><div id="e-last" class="lbl xl" style="display:flex;align-items:center;gap:20px">{svg(ICON['star'],80)}LE DERNIER</div></div>
{badge_bar("e", 5, "Crée un plan étape par étape")}
<div id="e-card" class="box abs" style="left:70px;top:560px;width:940px;height:470px;padding:30px 40px">
  <div id="e-line" class="abs" style="left:73px;top:66px;width:6px;height:340px;background:#111;transform-origin:50% 0%"></div>{sh}</div>
"""
num = L(n5num, nm)
js = f"""
pop("#e-last", 0.05); wiggle("#e-last svg", 0.4, 5); out("#e-last", {num-0.3});
pop("#e-badge", {num}); rise("#e-bar", {num+0.1}); typeChars("#e-typed", {num+0.4}, {L(A('structure', n5, True), nm)});
rise("#e-card", {L(A('structure', n5, True), nm)});
tl.fromTo("#e-line", {{ scaleY: 0 }}, {{ scaleY: 1, duration: {round(etp_end-march, 2)}, ease: "none" }}, {L(march, nm)});
""" + "".join(f'slideL("#e-s{k}", {round(L(march, nm) + k*(etp_end-march)/4, 2)});' for k in range(4)) + f"""
out("#e-card", {d-0.3}); out("#e-badge", {d-0.3}); out("#e-bar", {d-0.3});
"""
SFX += [(s0, "whoosh", .5), (s0+0.05, "sparkle", .45), (n5num, "pop", .4), (n5num+0.4, "typing", .3)] + [(round(march + k*(etp_end-march)/4, 2), "pop", .3) for k in range(4)]
open(f"{P}/compositions/n5.html", "w").write(scene(nm, d, EXTRA_CSS, html, js))

# ================================================================= ASTUCE
nm = "astuce"; s0, d = S[nm]
dab, ens, tab_end = A("d'abord", ast), A("ensuite", ast), A("tableau", ast, True)
html = f"""
<div class="row" style="top:350px"><div id="f-l" class="lbl" style="display:flex;align-items:center;gap:16px">{svg(ICON['bulb'],62)}PETITE ASTUCE</div></div>
{lbl("f-l2", "TU PEUX LES ENCHAÎNER", 470, "w")}
<div id="f-a" class="box abs tile" style="left:70px;top:640px;width:380px;height:200px">{svg(ICON['lines'],90)}<span style="font-size:31px"><span class="o">1</span> DÉVELOPPE</span></div>
<div id="f-ar" class="abs" style="left:470px;top:690px">{svg(ICON['arrow'],110)}</div>
<div id="f-b" class="box abs tile" style="left:630px;top:640px;width:380px;height:200px">{svg(ICON['table'],90)}<span style="font-size:31px"><span class="o">4</span> TABLEAU</span></div>
{lbl("f-res", "= RÉPONSE COMPLÈTE ET CLAIRE", 900, "k")}
"""
js = f"""
pop("#f-l", 0.05); pop("#f-l2", {L(A('peux', ast), nm)});
slideL("#f-a", {L(dab, nm)}); tl.fromTo("#f-ar", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35 }}, {L(ens, nm)-0.3}); slideR("#f-b", {L(ens, nm)});
pop("#f-res", {L(tab_end, nm)});
out("#f-l", {d-0.3}); out("#f-l2", {d-0.3}); out("#f-a", {d-0.3}); out("#f-ar", {d-0.3}); out("#f-b", {d-0.3}); out("#f-res", {d-0.3});
"""
SFX += [(s0, "whoosh", .5), (A('peux', ast), "pop", .35), (dab, "whoosh-short", .4), (ens, "whoosh-short", .4), (tab_end, "pop", .45)]
open(f"{P}/compositions/astuce.html", "w").write(scene(nm, d, EXTRA_CSS, html, js))

# ================================================================= CTA
nm = "cta"; s0, d = S[nm]
ecris, com, envoie = A("écris|décrit", cta), A("commentaire", cta), A("l'envoie|envoie", cta)
html = f"""
{lbl("g-l", "TU VEUX LA LISTE ?", 340)}
<div id="g-doc" class="box abs" style="left:250px;top:470px;width:580px;height:520px;padding:30px;text-align:center">
  <div style="font-weight:900;font-size:150px;line-height:1;color:{OR};text-shadow:6px 6px 0 #111">25</div>
  <div style="font-weight:900;font-size:40px;line-height:1.15;margin-top:10px">RACCOURCIS<br>CHATGPT</div>
  <div style="margin:26px auto 0;width:80%;height:14px;background:#E6E6E6;border-radius:8px"></div>
  <div style="margin:12px auto 0;width:65%;height:14px;background:#E6E6E6;border-radius:8px"></div>
  <div style="margin:12px auto 0;width:72%;height:14px;background:#E6E6E6;border-radius:8px"></div>
</div>
{lbl("g-ec", "ÉCRIS EN COMMENTAIRE", 340, "w")}
<div id="g-com" class="box abs" style="left:70px;top:480px;width:940px;padding:26px">
  <div style="display:flex;align-items:center;gap:16px;font-weight:900;font-size:30px">{svg(ICON['chat'],56)}COMMENTAIRES</div>
  <div style="margin-top:20px;border:4px solid #111;border-radius:50px;height:120px;display:flex;align-items:center;padding:0 14px 0 34px">
    <span id="g-typed" data-full="ACADÉMIE" style="color:{OR};font-weight:900;font-size:62px;flex:1;letter-spacing:.02em"></span>{svg(ICON['send'],84)}</div>
</div>
<div id="g-rep" class="abs" style="left:300px;top:800px;background:#111;color:#fff;font-weight:800;font-size:36px;padding:20px 30px;border-radius:30px 30px 6px 30px;box-shadow:8px 8px 0 {OR}">Je te l'envoie ! ✓</div>
"""
js = f"""
pop("#g-l", 0.05); rise("#g-doc", {L(A('liste', cta), nm)-0.2}); tl.fromTo("#g-doc", {{ rotation: -3 }}, {{ rotation: 3, duration: 0.8, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {L(A('liste', cta), nm)+0.4});
out("#g-l", {L(ecris, nm)-0.3}); out("#g-doc", {L(ecris, nm)-0.3});
pop("#g-ec", {L(ecris, nm)}); rise("#g-com", {L(ecris, nm)+0.1}); typeChars("#g-typed", {L(A('académi', cta), nm)}, {L(A('académi', cta, True), nm)+0.2});
pop("#g-rep", {L(envoie, nm)-0.4});
tl.fromTo("#g-com", {{ scale: 1 }}, {{ scale: 1.03, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {L(com, nm)});
"""
SFX += [(s0, "whoosh", .5), (A('liste', cta), "pop", .4), (ecris, "whoosh-short", .4), (A('académi', cta), "typing", .35), (envoie-0.4, "sparkle", .5)]
open(f"{P}/compositions/cta.html", "w").write(scene(nm, d, EXTRA_CSS, html, js))

# ================================================================= AVATAR
moves = [(n1, -230, 1), (n2, 230, -1), (n3, -230, 1), (n4, 230, -1), (n5, 0, 1), (ast, -230, 1), (cta, 0, 1)]
sched = [(A("cinq"), "point"), (A("seul"), "face_pouce"), (A("reste"), "think"), (A("puissant"), "enjoue"),
         (n1 + 0.1, "point"), (A("ta", n1), "ordinateur_main"), (A("exemples", n1), "pensif_souriant"),
         (n2 + 0.1, "think"), (A("vois", n2), "pensif"), (A("décides", n2), "base"),
         (n3 + 0.1, "laptop"), (A("coup", n3), "point"),
         (n4 + 0.1, "bureau_ordinateur"),
         (n5 + 0.1, "enjoue"), (n5num, "point"), (A("marche", n5), "trois_quarts"),
         (ast + 0.1, "pensif_souriant"), (A("d'abord", ast), "point"), (A("tableau", ast), "face_pouce"),
         (cta + 0.1, "think"), (A("écris|décrit", cta), "laptop"), (A("l'envoie|envoie", cta) - 0.4, "wave")]
mjs = ""
for t, x, sx in moves:
    mjs += f'tl.to("#av-x", {{ x: {x}, scaleX: {sx}, duration: 0.5, ease: "power3.inOut" }}, {t});\n'
    mjs += f'tl.to("#av-hop", {{ y: -70, duration: 0.22, ease: "power2.out" }}, {t}).to("#av-hop", {{ y: 0, duration: 0.45, ease: "bounce.out" }}, {t+0.22});\n'
POSES = ["wave"] + sorted({n for _, n in sched} - {"wave"})
imgs = "".join(f'<img id="av-{n}" class="av-img" src="assets/avatar_{n}.png" alt="avatar {n}"{" style=\"opacity:1\"" if n == "wave" else ""}>' for n in POSES)
cur = "wave"
for k, (t, n) in enumerate(sched):
    mjs += f'tl.set("#av-{cur}", {{ opacity: 0 }}, {t}); tl.set("#av-{n}", {{ opacity: 1 }}, {t});\n'
    mjs += f'tl.fromTo("#av-pop", {{ scaleX: 1.08, scaleY: 0.9 }}, {{ scaleX: 1, scaleY: 1, duration: 0.35, ease: "back.out(3)"{"" if k == 0 else ", immediateRender: false"} }}, {t});\n'
    cur = n
avatar = f"""<template>
  <style>
    #root{{position:absolute;inset:0;pointer-events:none}}
    #av-x{{position:absolute;left:241px;top:1058px;width:598px;height:880px}}
    #av-hop,#av-bob,#av-pop{{position:relative;width:100%;height:100%;transform-origin:50% 100%}}
    .av-img{{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:contain;object-position:50% 100%;opacity:0}}
  </style>
  <div id="root" data-composition-id="avatar" data-width="1080" data-height="1920" data-layout-allow-overflow data-layout-allow-overlap>
    <div id="av-x"><div id="av-hop"><div id="av-bob"><div id="av-pop">{imgs}</div></div></div></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#av-x", {{ y: 500 }}, {{ y: 0, duration: 0.5, ease: "back.out(1.4)" }}, 0);
    tl.fromTo("#av-bob", {{ scaleY: 1, rotation: -1.2 }}, {{ scaleY: 1.025, rotation: 1.2, duration: 0.9, yoyo: true, repeat: {int(TOTAL/0.9)}, ease: "sine.inOut" }}, 0);
{mjs}
    tl.set({{}}, {{}}, {TOTAL});
    window.__timelines["avatar"] = tl;
  </script>
</template>
"""
open(f"{P}/compositions/avatar.html", "w").write(avatar)

# ================================================================= CAPTIONS
FIXT = {"compars": "compares", "1": "un", "2": "deux", "3": "trois", "4": "quatre", "5": "cinq", "25": "25"}
def fix(t):
    core = t.rstrip(",.?!:")
    tail = t[len(core):]
    return FIXT.get(core.lower(), core) + tail
txt = [fix(w["text"]) for w in W]
txt = [t[:-1] + " ?" if t.endswith("?") and not t.endswith(" ?") else t for t in txt]
KEY = {"cinq", "clic", "fin", "puissant", "développe", "détails", "paragraphe", "exemples", "compare", "contre", "décides", "liste", "puces",
       "œil", "d'œil", "tableau", "ligne", "plan", "structure", "étape", "astuce", "enchaîner", "académie", "commentaire", "un", "deux", "trois", "quatre", "dernier"}
groups, curg = [], []
for i, w in enumerate(W):
    curg.append(i)
    chars = sum(len(txt[j]) for j in curg) + len(curg) - 1
    nxt = i + 1 if i + 1 < len(W) else None
    if (txt[i][-1] in ".,?:!" or len(curg) >= 3 or nxt is None or chars + len(txt[nxt]) + 1 > 19 or W[nxt]["start"] - w["end"] > 0.15):
        groups.append(curg); curg = []
cap_html, cap_js = "", ""
for g, idx in enumerate(groups):
    st = max(0.12, W[idx[0]]["start"] - 0.04)
    en = W[groups[g + 1][0]]["start"] - 0.04 if g + 1 < len(groups) else TOTAL - 0.2
    en = min(en, W[idx[-1]]["end"] + 0.7)
    words = [txt[j] for j in idx]
    keyed = [k for k, t in enumerate(words) if t.lower().strip(",.? ") in KEY]
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
    .cg{{position:absolute;left:0;top:200px;width:1080px;text-align:center;font-weight:900;text-transform:uppercase;color:#111;line-height:1.1;opacity:0;padding:0 70px}}
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
SFXLEN = {"pop": .72, "whoosh": .57, "whoosh-short": .57, "typing": 1.54, "sparkle": 1.8, "click-soft": .36, "error": 1.62}
hosts = ""
for k, (cid, (st, du)) in enumerate(S.items()):
    hosts += f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{st}" data-duration="{du}" data-track-index="{1 + k % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{2+k}"></div>\n'
sfx_html = ""
for k, (t, f, v) in enumerate(sorted(SFX)):
    sfx_html += f'      <audio id="sfx{k}" class="clip" src="assets/sfx/{f}.mp3" data-start="{max(0,t):.2f}" data-duration="{SFXLEN[f]}" data-track-index="{30 + k % 3}" data-volume="{v}"></audio>\n'
index = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #ffffff; }}
      #root {{ width: 100%; height: 100%; position: relative; font-family: 'Montserrat', sans-serif; background-color: #ffffff;
        background-image: linear-gradient(#f3f3f3 2px, transparent 2px), linear-gradient(90deg, #f3f3f3 2px, transparent 2px); background-size: 72px 72px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{hosts}      <div id="avatar" data-composition-id="avatar" data-composition-src="compositions/avatar.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:20"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:30"></div>
      <audio id="vo" class="clip" src="assets/voice.mp3" data-start="0" data-duration="{VOICE_LEN}" data-track-index="20" data-volume="1"></audio>
      <audio id="bgm" class="clip" src="assets/music.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="21" data-volume="0.13"></audio>
{sfx_html}    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(f"{P}/index.html", "w").write(index)
print("TOTAL", TOTAL, "groupes", len(groups), "sfx", len(SFX))
