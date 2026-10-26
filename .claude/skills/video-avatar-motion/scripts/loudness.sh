#!/usr/bin/env bash
# Remonte le son d'une vidéo à ~ -14,5 LUFS (réseaux sociaux), pic < -1 dBTP, sans ré-encoder l'image.
# Usage : bash loudness.sh entree.mp4 sortie.mp4 [gain_dB]
set -euo pipefail
IN="$1"; OUT="$2"; GAIN="${3:-5.5}"
ffmpeg -v error -y -i "$IN" -c:v copy \
  -af "aresample=192000,volume=${GAIN}dB,alimiter=limit=0.72:level=false,aresample=48000" \
  -c:a aac -b:a 192k "$OUT"
ffmpeg -v info -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary | grep -E "I:|Peak:"
echo "Viser I ≈ -14 à -15 LUFS et Peak < -1 dBFS ; sinon relancer avec un autre gain (3e argument)."
