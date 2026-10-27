# Lit un texte avec la voix clonée de Koné (Chatterbox multilingue, licence MIT, tourne sur CPU).
# Usage : <venv>/bin/python voice_clone.py texte.txt sortie.mp3 [reference.wav]
#           [--tempo 1.1] [--exaggeration 0.5] [--cfg 0.5] [--pause 0.3] [--retries 3] [--redo 5,7]
#   texte.txt : le texte de la voix off. Découpé en phrases (une génération par phrase).
#   reference.wav : extrait propre de la voix (10-20 s). Par défaut : assets/voix/kone_reference.wav du skill.
# Contrôle qualité automatique : une phrase anormalement longue (répétition) ou courte (coupée) est régénérée
# avec une autre graine, jusqu'à --retries fois. Les phrases réussies sont gardées en cache (<sortie>.parts/),
# donc relancer la commande ne recalcule que ce qui manque ; --redo 5,7 force la régénération des phrases 5 et 7.
# Vitesse constatée : ~5-7 s de calcul par seconde de voix sur 4 CPU.
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, time
import torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("text"); ap.add_argument("out")
ap.add_argument("ref", nargs="?", default=os.path.join(SKILL, "assets/voix/kone_reference.wav"))
ap.add_argument("--exaggeration", type=float, default=0.5, help="expressivité (0.3 calme – 0.8 très expressif)")
ap.add_argument("--cfg", type=float, default=0.5, help="fidélité au rythme de la référence (0.3 plus lent – 0.7)")
ap.add_argument("--pause", type=float, default=0.3, help="silence entre phrases, en secondes")
ap.add_argument("--tempo", type=float, default=1.0, help="accélère sans changer le timbre (1.1 = +10 %%)")
ap.add_argument("--retries", type=int, default=3)
ap.add_argument("--redo", default="", help="numéros de phrases à régénérer, ex. 5,7")
a = ap.parse_args()

text = open(a.text, encoding="utf-8").read()
text = text.replace("’", "'").replace("«", "").replace("»", "").replace(" ", " ")
text = re.sub(r"\s+", " ", text).strip()
sents = []
for s in re.split(r"(?<=[.!?…])\s+", text):
    while len(s) > 220:  # phrases trop longues : recoupées aux virgules
        cut = s.rfind(",", 0, 220)
        cut = cut if cut > 60 else 220
        sents.append(s[: cut + 1].strip()); s = s[cut + 1 :].strip()
    if s:
        sents.append(s)

cache = a.out + ".parts"
os.makedirs(cache, exist_ok=True)
redo = {int(x) for x in a.redo.split(",") if x.strip()}
m = None

def trim(wav, sr, thr=0.01, keep=0.06):
    """Retire le silence au début et à la fin d'une phrase."""
    env = wav.abs().squeeze(0)
    idx = (env > thr).nonzero()
    if len(idx) == 0:
        return wav
    k = int(sr * keep)
    return wav[:, max(0, idx[0].item() - k): min(wav.shape[-1], idx[-1].item() + k)]

def ok_length(s, dur):
    expected = len(s) / 15.0  # ≈ 15 caractères par seconde en français
    return 0.55 * expected - 0.3 <= dur <= 1.6 * expected + 0.7, expected

t0 = time.time()
parts, sr, report = [], None, []
for i, s in enumerate(sents, 1):
    key = hashlib.md5(json.dumps([s, os.path.abspath(a.ref), a.exaggeration, a.cfg]).encode()).hexdigest()[:12]
    path = os.path.join(cache, f"{i:02d}_{key}.wav")
    if os.path.exists(path) and i not in redo:
        wav, sr = torchaudio.load(path)
        status = "cache"
    else:
        if m is None:
            m = ChatterboxMultilingualTTS.from_pretrained(device="cuda" if torch.cuda.is_available() else "cpu")
        sr, best, status = m.sr, None, "?"
        start_seed = 100 if i in redo else 0
        for attempt in range(a.retries):
            torch.manual_seed(start_seed + attempt)
            w = trim(m.generate(s, language_id="fr", audio_prompt_path=a.ref, exaggeration=a.exaggeration, cfg_weight=a.cfg), sr)
            good, exp = ok_length(s, w.shape[-1] / sr)
            if best is None or abs(w.shape[-1] / sr - exp) < abs(best.shape[-1] / sr - exp):
                best = w
            status = f"ok (essai {attempt+1})" if good else f"suspect (essai {attempt+1})"
            if good:
                break
        wav = best
        torchaudio.save(path, wav, sr)
    report.append((i, round(wav.shape[-1] / sr, 2), status, s))
    print(f"[{i}/{len(sents)}] {round(time.time()-t0)} s  {wav.shape[-1]/sr:.1f}s {status}  {s[:60]}", flush=True)
    parts += [wav, torch.zeros(1, int(sr * a.pause))]

full = torch.cat(parts, dim=-1)
with tempfile.TemporaryDirectory() as d:
    wav_path = os.path.join(d, "voix.wav")
    torchaudio.save(wav_path, full, sr)
    af = (f"atempo={a.tempo}," if a.tempo != 1.0 else "") + "loudnorm=I=-16:TP=-1.5:LRA=11"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav_path, "-af", af, "-ar", "44100", "-b:a", "192k", a.out], check=True)
sus = [r for r in report if r[2].startswith("suspect")]
print(f"OK {a.out} : {full.shape[-1]/sr/a.tempo:.1f} s de voix en {round(time.time()-t0)} s")
if sus:
    print("À vérifier (longueur anormale) :", ", ".join(str(r[0]) for r in sus))
print("Conseil : retranscrire le MP3 (npx hyperframes transcribe … --language fr) et relancer avec --redo n pour une phrase fautive.")
