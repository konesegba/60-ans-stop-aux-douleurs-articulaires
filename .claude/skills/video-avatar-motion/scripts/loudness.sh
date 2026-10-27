#!/usr/bin/env bash
# Règle le son d'une vidéo à ~ -14,5 LUFS (réseaux sociaux), pic < -1 dBTP, sans ré-encoder l'image.
# Le gain est calculé automatiquement à partir du volume mesuré.
# Usage : bash loudness.sh entree.mp4 sortie.mp4 [cible_LUFS=-14.5]
set -euo pipefail
IN="$1"; OUT="$2"; TARGET="${3:--14.5}"
I_IN=$(ffmpeg -v info -i "$IN" -af ebur128 -f null - 2>&1 | grep -A3 "Integrated loudness" | grep -oE "I: +-?[0-9.]+" | grep -oE "\-?[0-9.]+" | tail -1)
GAIN=$(python3 -c "print(round(($TARGET) - ($I_IN), 2))")
echo "Mesuré : $I_IN LUFS → gain $GAIN dB"
ffmpeg -v error -y -i "$IN" -c:v copy \
  -af "aresample=192000,volume=${GAIN}dB,alimiter=limit=0.72:level=false,aresample=48000" \
  -c:a aac -b:a 192k "$OUT"
ffmpeg -v info -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary | grep -E "I:|Peak:"
