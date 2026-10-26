#!/usr/bin/env bash
# Installe HyperFrames et prépare un projet vidéo vertical avec l'avatar Koné.
# Usage : bash setup.sh <dossier_de_travail>
set -euo pipefail
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${1:?Usage: setup.sh <dossier_de_travail>}"
mkdir -p "$WORK" && cd "$WORK"

command -v node >/dev/null || { echo "Node.js 22+ requis"; exit 1; }
command -v ffmpeg >/dev/null || { echo "FFmpeg requis"; exit 1; }
python3 -c "import PIL" 2>/dev/null || pip install --quiet pillow

# 1) Skills HyperFrames (hyperframes, hyperframes-cli, hyperframes-registry, media-use…)
if [ ! -d .agents/skills/hyperframes ]; then
  npx -y skills add heygen-com/hyperframes -y
fi

# 2) Projet vidéo
if [ ! -f video/index.html ]; then
  npx -y hyperframes init video
fi

# 3) Avatar (6 poses) + bruitages
mkdir -p video/assets/sfx
cp "$SKILL"/assets/poses/avatar_*.png video/assets/
cp "$SKILL"/assets/sfx/*.mp3 video/assets/sfx/

# 4) Navigateur de rendu
(cd video && npx hyperframes browser ensure >/dev/null 2>&1 || true)

echo "OK : projet prêt dans $WORK/video"
echo "Lire ensuite : $WORK/.agents/skills/hyperframes/SKILL.md"
