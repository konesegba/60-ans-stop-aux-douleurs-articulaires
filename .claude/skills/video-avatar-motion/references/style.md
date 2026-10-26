# Style visuel validé (inspiré de la vidéo de référence)

## Format
- 1080×1920, 30 i/s. Fond **blanc** `#FFFFFF` avec une grille très légère `#F3F3F3` (traits 2 px, pas de 72 px).
- Zones : rien d'important au-dessus de 168 px ; sous-titres à y = 200 ; contenu entre 330 et 1060 ; avatar en bas (≈ 1076–1937), décalé à gauche ou à droite pour laisser de la place à des étiquettes à côté de lui.

## Typographie
- **Montserrat** (incluse dans HyperFrames) : 900 en MAJUSCULES pour titres, étiquettes, sous-titres ; 600–800 pour le texte des maquettes.
- Taille mini lisible : 28 px. Sous-titres 60–70 px.

## Couleurs
| Rôle | Valeur |
| --- | --- |
| Accent (étiquettes, mots-clés) | `#E8532F` (orange-rouge) |
| Encre, bordures, ombres | `#111111` |
| Fond des cartes | `#FFFFFF` |
| Bulle ChatGPT | `#F1F1F1` |

## Composants
- **Étiquette** `.lbl` : fond orange, texte blanc 900, bordure noire 5 px, **ombre dure décalée** `9px 9px 0 #111`. Variantes : `.w` (fond blanc, texte noir), `.k` (fond noir, ombre orange), `.s` (petite), `.xl` (grande).
- **Carte** `.box` : fond blanc, bordure noire 5 px, rayon 12 px, ombre `14px 14px 0 #111`.
- **Badge** « NUMÉRO n » : carré orange 170×190, chiffre 120 px.
- **Fenêtre ChatGPT** : en-tête avec 3 points + « ChatGPT » + pastille « ÉTAPE n », bulle grise où le prompt s'écrit mot à mot (mots-clés en orange), barre « Envoyer » avec bouton rond noir.
- **Barre de commande** (comme la référence) : petit libellé « ChatGPT » au-dessus, barre blanche, texte tapé en orange.
- **Icônes** : SVG maison au trait noir de 6 px avec aplat orange (pas de logos de marques redessinés).

## Mouvement
- Entrées : `pop` (échelle 0,55 → 1, `back.out(2.2)`, 0,38 s), glissés latéraux (0,4 s `power3.out`), montée (0,5 s).
- Sorties : 0,25 s `power2.in`, juste avant le changement de scène.
- Avatar : respiration permanente (léger étirement + balancement), saut à chaque changement de scène, rebond à chaque changement de pose, tremblement sur « attention ».
- Rythme : un nouvel élément toutes les 2 à 4 s, calé sur le mot prononcé.

## Son
- Voix 1.0, musique 0.13, bruitages 0.3–0.6. Final normalisé à ≈ -14,5 LUFS.
