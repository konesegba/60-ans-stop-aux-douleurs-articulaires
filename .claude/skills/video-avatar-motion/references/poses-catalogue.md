# Catalogue des poses de l'avatar Koné (17 poses)

Fichiers prêts à l'emploi : `assets/poses/avatar_<nom>.png`. Toutes ont un fond transparent et le contour blanc. Elles partagent le même cadre (rapport 0,68) : même taille de personnage, pieds sur la même ligne. On passe donc de l'une à l'autre sans saut.
Originaux (fond gris) : `assets/poses-originales/`. Planche de départ fournie par Koné : `assets/planche-avatar-kone.png`.

Dans le modèle, on choisit une pose en ajoutant `(temps, "nom")` à la liste `sched`. Le retournement gauche/droite (`scaleX: -1` dans `moves`) marche avec toutes les poses.

## Comment choisir (selon ce que dit la voix)

| Nom | Ce qu'on voit | À utiliser quand la voix… |
| --- | --- | --- |
| `base` | Face, sourire, bras croisés, pouce levé | ouvre la vidéo, valide une idée, dit « atout », « c'est simple », conclut positivement |
| `face_pouce` | Variante de `base` (même attitude, rendu planche) | même usage que `base`, pour varier |
| `point` | Montre du doigt vers le haut/côté | présente une idée, une liste, un chiffre, « voici… », « par exemple… » (orienter le doigt vers le contenu) |
| `think` | Main au menton, regard vers le haut | pose une question, « et si… ? », « avant de… », réflexion |
| `pensif` | Main au menton, air sérieux, regard de côté | doute, mise en garde douce, « vérifiez », « posez-vous la question » |
| `pensif_souriant` | Main au menton, sourire | astuce, idée maligne, « voici l'astuce », « pensez à… » |
| `enjoue` | Deux mains levées, grand sourire | bonne nouvelle, résultat, « bravo », « c'est possible ! », énergie |
| `wave` | Salue d'une main, pointe le spectateur | salut d'ouverture, « contactez-moi », « abonnez-vous », fin de vidéo |
| `shock` | Mains sur la tête, bouche ouverte | « attention », erreur fréquente, piège, surprise négative |
| `triste` | Bras ballants, air déçu | problème, frustration, « vous pensez n'avoir rien à vendre », avant/après (avant) |
| `laptop` | Debout, ordinateur ouvert, tape dessus | « demandez à ChatGPT », prompt en train d'être écrit |
| `ordinateur_main` | Debout, présente un ordinateur ouvert d'une main | montre un outil, un résultat à l'écran, « regardez ce que ChatGPT propose » |
| `bureau_ordinateur` | Assis à un bureau, tape sur l'ordinateur | travail, méthode pas à pas, « installez-vous », formation, tutoriel |
| `trois_quarts` | De trois-quarts, tourné vers la droite, bras croisés | regarde le contenu affiché à côté de lui (placer le contenu du côté où il regarde) |
| `profil` | De profil, tourné vers la gauche | regarde/« écoute » un élément à gauche ; transition, marche |
| `dos_trois_quarts` | De dos, trois-quarts | se retourne vers un écran/un tableau, « regardons ensemble » |
| `dos` | De dos | entrée ou sortie de scène, regarde un grand titre ou un tableau derrière lui |

## Règles de mise en scène
- **Changer de pose à chaque nouvelle idée** (toutes les 3 à 8 s), jamais deux fois de suite la même sauf pendant un prompt.
- **Le regard ou le doigt va vers le contenu** : si le contenu est à droite de l'avatar, utiliser `point` / `trois_quarts` non retournés ; s'il est à gauche, les retourner (`scaleX: -1`).
- **Petite séquence de retournement** (effet « il se tourne vers l'écran ») : `trois_quarts` → `dos_trois_quarts` → `dos`, environ 0,15 s chacune.
- Ouverture : `base` ou `wave`. Problème : `triste` ou `think`. Solution : `point` / `enjoue`. Mise en garde : `shock` puis `pensif`. Appel à l'action : `wave`.
- `bureau_ordinateur` est plus large (il y a le bureau) : le placer au centre ou du côté opposé au contenu.

## Ajouter une pose
Voir `references/poses.md`, puis relancer `scripts/prepare_poses.py` sur **toutes** les poses (dossier `cut_*.png`) pour garder le cadre commun. Pour les objets fins que le détourage IA efface (pieds de table, chaise), compléter avec `scripts/colorkey_cut.py original.png cut.png cut.png 30`.
