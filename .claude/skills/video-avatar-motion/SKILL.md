---
name: video-avatar-motion
description: Crée une vidéo verticale (Reels/TikTok/Shorts) en motion design à partir d'un texte, avec l'avatar 3D de Koné animé en plusieurs poses, une voix off ElevenLabs (voix « Tony - Podcast Narrator », repli via FLORA), des sous-titres mot à mot, des mockups ChatGPT et des illustrations, sur fond blanc dans le style « étiquettes orange + cadres noirs ». Utilise HyperFrames (installé par le skill). À utiliser quand on demande une vidéo motion design / explainer / reel avec l'avatar, une voix off ou à partir d'un script texte.
---

# Vidéo motion design avec l'avatar Koné

Méthode complète validée le 26/10/2026 (vidéo « 20 ans d'expérience + ChatGPT », 1 min 53).
Le résultat de référence est dans `download/avatar-kone/` du dépôt.

Entrées attendues : **le texte de la voix off**, l'image de l'avatar (par défaut : `assets/poses/avatar_base.png` de ce skill), éventuellement une vidéo de référence de style.
Sortie : un MP4 1080×1920 + un dossier livrable (vidéo, poses, audio, sources).

Tout ce qui suit se lance depuis un dossier de travail (le scratchpad de la session de préférence). `$SKILL` = le dossier de ce skill.

---

## Étape 0 — Installer HyperFrames (une fois par session)

```bash
bash $SKILL/scripts/setup.sh <dossier_de_travail>
```

Le script : installe les skills HyperFrames (`npx skills add heygen-com/hyperframes -y`), crée le projet `<dossier>/video` (`npx hyperframes init video`), copie les 6 poses de l'avatar et les bruitages dans `video/assets/`.
Puis **lire** `<dossier>/.agents/skills/hyperframes/SKILL.md` et `references/format.md`, `types/vertical.md`, `captions.md` : ce sont les règles du format (contrat `class="clip"`, `data-start`, timelines GSAP en pause, `<template>` par scène…).

Prérequis : Node 22+, FFmpeg, Python 3 + Pillow (déjà présents dans l'environnement cloud).

## Étape 1 — Analyser la vidéo de référence (si fournie)

```bash
ffmpeg -i ref.mp4 -vf "fps=1/3,scale=360:-1" ref/f_%03d.jpg
ffmpeg -pattern_type glob -i 'ref/f_*.jpg' -vf tile=8x2 -frames:v 1 ref_sheet.jpg
```
Regarder la planche (Read) et noter : police, couleurs, composants, position de l'avatar. Sans référence, appliquer `references/style.md` (le style validé).

## Étape 2 — La voix off

1. **ElevenLabs d'abord** : `creative_list_voices` (search « Tony ») → voix **« Tony - Podcast Narrator », id `M4ZqLOXSFqxSkn9RDxFO`** (voix française, léger accent africain). `creative_generate_speech` avec `eleven_multilingual_v2`, puis `creative_get_flow_run_status`.
2. **Si ElevenLabs refuse** (ex. « Free Tier access has been disabled ») → **FLORA** :
   - modèle `t2a-elevenlabs-v4-t2a` avec `params.voice_id = "M4ZqLOXSFqxSkn9RDxFO"` (il accepte n'importe quelle voix ElevenLabs) ;
   - d'abord `quote: true` pour annoncer le prix (≈ 0,24 $ pour 2 000 caractères), puis la vraie génération ;
   - projet FLORA : si « Project limit reached », réutiliser un projet existant (`flora_list_projects`) — ex. « Vidéo Académie Réussir avec l'IA – audio » `prj_ns7bvejg7hdftcp3wnfqz8xt718gw0mw`, workspace `ws_qd72aawtpaetyzznf65pc03e457v8rbs`.
3. Télécharger le MP3 dans `video/assets/voice.mp3`.

## Étape 3 — Minutage mot à mot

```bash
cd video && npx hyperframes transcribe assets/voice.mp3 --model small --language fr --json
python3 $SKILL/scripts/print_transcript.py assets/transcript.json
```
Le script affiche les phrases avec leurs temps **et** la liste `index:mot@temps`. On cale chaque animation sur l'index du mot prononcé (`T(i)` dans le modèle).
Whisper écrit « vingt », « LIA », « identifier »… : on corrige l'affichage par index dans le dictionnaire `FIX` du modèle (le minutage reste bon).

## Étape 4 — Musique de fond (optionnelle, ≈ 0,10 $)

FLORA `t2a-lyria-3-5-t2a`, prompt utilisé :
« Light upbeat instrumental background music for a social media explainer video, modern lo-fi pop with soft plucked synths, gentle claps and warm bass, positive and motivating, steady 110 bpm, no vocals, no big drops, loopable ».
Puis couper à la durée de la vidéo avec un fondu :
```bash
ffmpeg -i music_src.mp3 -t <DUREE> -af "afade=t=in:d=0.5,afade=t=out:st=<DUREE-3>:d=3" assets/music.mp3
```
Volume dans la vidéo : `data-volume="0.13"` sous la voix.

## Étape 5 — L'avatar et ses poses

Les 6 poses prêtes à l'emploi (fond transparent, contour blanc, pieds alignés, même cadre 676×957) sont dans `$SKILL/assets/poses/` :
`base` (pouce levé), `point` (montre du doigt), `think` (réfléchit), `shock` (mains sur la tête), `laptop` (ordinateur), `wave` (salue). `setup.sh` les copie déjà.

**Nouvel avatar ou nouvelles poses** → `references/poses.md` (envoi de l'image sur FLORA, prompts Nano Banana 2.1 à 0,05 $ l'image, détourage, alignement).

## Étape 6 — Écrire la vidéo

Partir du modèle : `cp $SKILL/templates/generate_example.py generate.py`, puis l'adapter au nouveau texte. Il génère `index.html` + une scène par fichier dans `compositions/` :

- **Scènes** : une par grande partie du texte (accroche, plan, étape 1/2/3, attention, atout, appel à l'action). Pour chaque scène : `S["id"] = (début, durée)`, du HTML et des appels JS (`pop`, `slideL`, `slideR`, `rise`, `out`, `wiggle`, `typeAt` pour taper un prompt mot à mot au rythme de la voix, `typeChars`).
- **Composants prêts** : `lbl()` (étiquette orange / blanche / noire), `header()` (badge « NUMÉRO n » + 2 étiquettes), `chat_window()` (fenêtre ChatGPT avec bulle tapée mot à mot), cartes `.box`, icônes SVG maison (`ICON` : briefcase, coin, sparkle, user, users, building, folder, pen, cap, route, bulb, warning, check, hourglass, magnifier, trophy, chart, target, chat, send, plus).
- **Avatar** : `moves` (déplacements gauche/centre/droite + retournement) et `sched` (changement de pose au bon moment, avec petit rebond). Règle : réfléchit sur une question, montre du doigt sur une idée, ordinateur pendant un prompt, choqué sur « attention », salue sur « contactez-moi ».
- **Sous-titres** : générés automatiquement (3 mots max, ≤ 19 caractères, mot-clé en orange via `KEY`), en haut à y = 200 px.
- **Bruitages** (`SFX`) : whoosh aux changements de scène, pop sur les étiquettes, frappe clavier sur les prompts, sparkle sur l'IA et l'appel final.
- **Mise en page 1080×1920** : légendes 180–300 px, contenu 330–1060 px, avatar en bas (y ≈ 1076–1937). Texte lisible ≥ 28 px.

Ne jamais inventer d'exemples présentés comme réels ; les exemples des cartes sont des illustrations, le signaler à l'utilisateur.

```bash
python3 generate.py video
```

## Étape 7 — Contrôler

```bash
cd video
npx hyperframes lint
npx hyperframes check --json      # 0 erreur ; traiter text_below_floor, line_unread
npx hyperframes snapshot --at 0.5,5,10,...   # un instant par scène, puis LIRE les planches
```
Corriger tout débordement de texte (cadres trop petits) et les avertissements `gsap_repeated_fromto_without_baseline` (`immediateRender: false`).

## Étape 8 — Rendu et son

```bash
HYPERFRAMES_RENDER_DETACHED=1 npx hyperframes render --quality delivery --output renders/video.mp4 > render.log 2>&1 &
# attendre : until grep -qE 'Render (complete|failed)' render.log; do sleep 5; done   (≈ 5 min pour 2 min de vidéo)
bash $SKILL/scripts/loudness.sh renders/video.mp4 renders/video_final.mp4
```
`loudness.sh` remonte le son à ≈ -14,5 LUFS (norme réseaux sociaux) avec un pic sous -1 dB, sans recalculer l'image.
Vérifier quelques images décodées du MP4 final avant de livrer.

## Étape 9 — Livrer

Créer `download/<nom>/` avec : la vidéo, `poses-avatar/` (détourées + originales), `audio/` (voix + musique), `source/` (index.html, compositions, assets, generate.py) et un `LISEZ-MOI.md`. Envoyer la vidéo avec `SendUserFile`, committer et pousser.

## Coûts constatés (FLORA)
Voix 2 000 caractères ≈ 0,24 $ · musique ≈ 0,10 $ · une pose d'avatar ≈ 0,05 $. Annoncer le coût avant une série de générations.
