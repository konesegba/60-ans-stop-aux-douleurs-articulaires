"""Affiche les phrases minutées puis chaque mot avec son index (pour caler les animations).
Usage : python3 print_transcript.py assets/transcript.json"""
import json, sys
w = json.load(open(sys.argv[1]))
w = w if isinstance(w, list) else w["words"]
line, st = [], None
for x in w:
    st = x["start"] if st is None else st
    line.append(x["text"])
    if x["text"][-1] in ".?:!»":
        print(f"{st:6.2f}-{x['end']:6.2f} {' '.join(line)}"); line, st = [], None
if line:
    print(f"{st:6.2f}- {' '.join(line)}")
print(f"\n{len(w)} mots :")
print(" ".join(f"{i}:{x['text']}@{x['start']:.1f}" for i, x in enumerate(w)))
