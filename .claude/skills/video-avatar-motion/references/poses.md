# Créer de nouvelles poses de l'avatar (FLORA)

Les 17 poses actuelles (voir `poses-catalogue.md`) sont dans `assets/poses/` (prêtes) et `assets/poses-originales/` (fond gris, 1024×1024).
Pour une nouvelle pose ou un autre avatar :

## 1. Envoyer l'image de départ sur FLORA
- `flora_create_asset` avec `source: "signed-url"`, `file_name`, `content_type: image/jpeg|png`, `workspace_id`, `project_id`.
- Envoyer le fichier avec `curl -X POST <upload.url>` en recopiant **tous** les `form_fields` (`-F champ=valeur`) puis `-F "file=@image.jpg;type=image/jpeg"` en dernier (réponse 204 = OK).
- `flora_complete_asset` → récupérer l'`url` publique.

## 2. Générer les poses (Nano Banana 2.1, ≈ 0,05 $ l'image)
`flora_create_generations`, `model: "i2i-elote-gateway"`, `params: { image_url: <url>, aspect_ratio: "1:1" }`, plusieurs poses dans un seul appel.

Début de prompt commun (garde le personnage identique) :
> Same exact 3D cartoon character (same face, blue cap, navy sweater, blue jeans, same style and lighting), full body, standing, …  Plain flat light grey background, full body visible with feet, centered, no text.

Fins de prompt utilisées :
| Pose | Fin de prompt |
| --- | --- |
| point | smiling, pointing up and to the side with his right index finger as if presenting something above him |
| think | thoughtful expression looking up, one hand on his chin thinking, other arm crossed |
| shock | shocked worried expression, mouth open, both hands on the sides of his head |
| laptop | smiling, holding an open grey laptop in his arms and typing on it (+ no logo) |
| wave | big friendly smile, waving hello with his right hand raised, other hand pointing at the viewer |

Idées d'autres poses : assis à un bureau, bras levés de joie, tenant un téléphone, montrant un tableau, haussant les épaules.

Suivre avec `flora_list_generations` (run_ids), télécharger les PNG.

## 3. Détourer et aligner
```bash
cd video
for n in point think shock laptop wave; do
  npx hyperframes remove-background ../poses/$n.png -o ../poses/cut_$n.png
done
npx hyperframes remove-background ../poses/base.jpg -o ../poses/cut_base.png
python3 $SKILL/scripts/prepare_poses.py ../poses assets
```
`prepare_poses.py` aligne les pieds sur la pose `base`, ajoute le contour blanc et recadre toutes les poses dans le **même cadre**, pour qu'elles se remplacent sans saut. Pour ajouter une pose, ajouter son nom à la liste `names` du script et à `POSES` dans le modèle.

Vérifier : composer les PNG sur fond magenta (`ffmpeg ... overlay`) et regarder le détourage.
