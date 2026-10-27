# Lit un texte avec la voix clonée de Koné (Chatterbox multilingue, licence MIT, tourne sur CPU).
# Usage : <venv>/bin/python voice_clone.py texte.txt sortie.mp3 [reference.wav] [--exaggeration 0.5] [--cfg 0.5]
#   texte.txt : le texte de la voix off (paragraphes libres). Découpé en phrases, une génération par phrase.
#   reference.wav : extrait propre de la voix (10-20 s). Par défaut : assets/voix/kone_reference.wav du skill.
# Vitesse constatée : ~7 s de calcul par seconde de voix sur 4 CPU (2 min de voix ≈ 15 min).
import argparse, os, re, subprocess, sys, tempfile, time
import torch, torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("text"); ap.add_argument("out")
ap.add_argument("ref", nargs="?", default=os.path.join(SKILL, "assets/voix/kone_reference.wav"))
ap.add_argument("--exaggeration", type=float, default=0.5, help="expressivité (0.3 calme – 0.8 très expressif)")
ap.add_argument("--cfg", type=float, default=0.5, help="fidélité au rythme de la référence (0.3 plus lent – 0.7)")
ap.add_argument("--pause", type=float, default=0.35, help="silence entre phrases, en secondes")
a = ap.parse_args()

text = open(a.text, encoding="utf-8").read()
text = text.replace("’", "'").replace("«", "").replace("»", "").replace(" ", " ")
text = re.sub(r"\s+", " ", text).strip()
# phrases ; les phrases trop longues (> 220 caractères) sont recoupées aux virgules
sents = []
for s in re.split(r"(?<=[.!?…])\s+", text):
    while len(s) > 220:
        cut = s.rfind(",", 0, 220)
        cut = cut if cut > 60 else 220
        sents.append(s[: cut + 1].strip()); s = s[cut + 1 :].strip()
    if s:
        sents.append(s)

t0 = time.time()
m = ChatterboxMultilingualTTS.from_pretrained(device="cuda" if torch.cuda.is_available() else "cpu")
parts = []
gap = torch.zeros(1, int(m.sr * a.pause))
for i, s in enumerate(sents, 1):
    wav = m.generate(s, language_id="fr", audio_prompt_path=a.ref, exaggeration=a.exaggeration, cfg_weight=a.cfg)
    parts += [wav, gap]
    print(f"[{i}/{len(sents)}] {round(time.time()-t0)} s  {s[:70]}", flush=True)
full = torch.cat(parts, dim=-1)
with tempfile.TemporaryDirectory() as d:
    wav_path = os.path.join(d, "voix.wav")
    torchaudio.save(wav_path, full, m.sr)
    # volume homogène (≈ -16 LUFS), puis MP3
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav_path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", "44100", "-b:a", "192k", a.out], check=True)
print(f"OK {a.out} : {full.shape[-1]/m.sr:.1f} s de voix en {round(time.time()-t0)} s")
