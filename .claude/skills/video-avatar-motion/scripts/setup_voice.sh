#!/usr/bin/env bash
# Installe le clonage de voix (Chatterbox multilingue, licence MIT) dans un environnement Python séparé.
# Usage : bash setup_voice.sh <dossier_de_travail>     (≈ 10-15 min la première fois, ~3 Go)
# Ensuite : <dossier>/tts-venv/bin/python $SKILL/scripts/voice_clone.py texte.txt voice.mp3
set -euo pipefail
WORK="${1:?Usage: setup_voice.sh <dossier_de_travail>}"
mkdir -p "$WORK" && cd "$WORK"
if [ ! -x tts-venv/bin/python ] || ! tts-venv/bin/python -c "import chatterbox" 2>/dev/null; then
  python3 -m venv tts-venv
  tts-venv/bin/pip install -q --upgrade pip
  tts-venv/bin/pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu
  tts-venv/bin/pip install -q chatterbox-tts
fi
tts-venv/bin/python -c "import chatterbox, torch; print('Chatterbox OK, torch', torch.__version__)"
