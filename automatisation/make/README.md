# Automatisation Make — Réponse auto aux commentaires « boîte à outils »

Page Facebook : **IA POUR 40/50 ANS**
Lien envoyé : **https://la-boite-a-outils.netlify.app**
Objectif : quand quelqu'un commente `guide`, `prompt` ou `boite a outils` sous une
vidéo/publication de la Page, il reçoit **automatiquement une réponse publique**
sous son commentaire avec le lien vers le lead magnet.

> Choix validés : réponse **publique en commentaire** (pas de DM privé, donc
> **aucune App Review Meta nécessaire**), outil **Make** (pas ManyChat), et
> l'inscription **Brevo** est déjà gérée en aval quand la personne accède au lead
> magnet. Ce scénario ne touche donc **ni à Messenger, ni à Brevo**.

---

## 1. Vue d'ensemble du scénario (3 modules)

```
┌────────────────────────┐     ┌──────────────┐     ┌────────────────────────┐
│ Facebook Pages         │     │   FILTRE     │     │ Facebook Pages         │
│ Watch Comments         │────▶│ mots-clés ?  │────▶│ Create a Comment       │
│ (Page IA POUR 40/50)   │     │ guide/prompt │     │ (réponse sous le comm.)│
└────────────────────────┘     │ /boite/outils│     └────────────────────────┘
        déclencheur            └──────────────┘            action
```

C'est tout. Trois modules natifs Make, zéro code, zéro permission spéciale.

---

## 2. Montage pas à pas dans Make

### Module 1 — Facebook Pages > **Watch Comments** (déclencheur)
1. Nouveau scénario → ajoute le module **Facebook Pages → Watch Comments**.
2. **Create a connection** → autorise ton compte et **sélectionne la Page
   « IA POUR 40/50 ANS »**. (C'est la seule étape que toi seul peux faire :
   l'autorisation OAuth de la Page.)
3. Paramètre `Limit` : `2` à `5` (nombre de commentaires récupérés par exécution).
4. Au premier lancement, choisis **« From now on »** pour ne traiter que les
   nouveaux commentaires.

### Module 2 — **Filtre** (entre le module 1 et le module 3)
Clique sur le trait entre les deux modules → **Set up a filter**.

- **Label** : `Contient un mot-clé`
- **Condition** :
  - Champ gauche : `{{lower(1.message)}}`
  - Opérateur : **Text operators → Matches pattern (regex)**
  - Valeur : `(guide|prompt|bo[iî]te|outils)`

Ce regex attrape **toutes** les variantes utiles en une seule ligne :
`guide`, `Guide`, `PROMPT`, `boite`, `boîte`, `boite a outils`, `outils`, etc.
(le `lower(...)` met tout en minuscules → insensible à la casse).

### Module 3 — Facebook Pages > **Create a Comment** (action)
1. Ajoute **Facebook Pages → Create a Comment**.
2. **Post ID / Parent** : mappe l'**ID du commentaire** issu du module 1
   (`{{1.id}}`). Répondre à l'ID du commentaire crée une **réponse imbriquée**
   sous le commentaire de la personne (elle reçoit une notification).
3. **Message** : colle la formule de rotation ci-dessous (anti-spam).

---

## 3. Anti-spam : rotation automatique du texte de réponse

Poster **exactement le même texte** des dizaines de fois par jour est ce qui
déclenche le masquage automatique de Facebook. On fait donc tourner 5 variantes.
Colle **cette formule unique** dans le champ **Message** du module 3 :

```
{{get(split("Merci pour ton message 🙌 Voici ta boîte à outils IA juste ici 👉 https://la-boite-a-outils.netlify.app|Avec plaisir ! Ton accès à la boîte à outils est par ici 👉 https://la-boite-a-outils.netlify.app 🚀|C'est parti ✨ Récupère tes outils IA ici 👉 https://la-boite-a-outils.netlify.app|Super 🙌 Ton accès est juste là 👉 https://la-boite-a-outils.netlify.app 💡|Génial ! Profite de ta boîte à outils IA par ici 👉 https://la-boite-a-outils.netlify.app"; "|"); mod(formatDate(now; "X"); 5) + 1)}}
```

Comment ça marche : la liste de 5 messages est découpée sur le `|`, et
`mod(timestamp; 5) + 1` choisit un des 5 selon l'heure → le texte change à chaque
envoi. Tu peux éditer/ajouter des variantes (garde toujours le séparateur `|` et
n'utilise jamais `|` **dans** un message).

Les 5 variantes, en clair :
1. Merci pour ton message 🙌 Voici ta boîte à outils IA juste ici 👉 https://la-boite-a-outils.netlify.app
2. Avec plaisir ! Ton accès à la boîte à outils est par ici 👉 https://la-boite-a-outils.netlify.app 🚀
3. C'est parti ✨ Récupère tes outils IA ici 👉 https://la-boite-a-outils.netlify.app
4. Super 🙌 Ton accès est juste là 👉 https://la-boite-a-outils.netlify.app 💡
5. Génial ! Profite de ta boîte à outils IA par ici 👉 https://la-boite-a-outils.netlify.app

---

## 4. Réglages de fréquence et bonnes pratiques

- **Planification (Schedule)** du scénario : toutes les **5 à 15 minutes**.
  (Watch Comments fonctionne en interrogation périodique — inutile de descendre
  trop bas, ça consomme des opérations pour rien.)
- **Optionnel — délai naturel** : ajoute un module **Tools → Sleep** (5–15 s)
  avant le module 3 pour que les réponses n'aient pas l'air robotisées.
- **Volume** : garde `Limit = 2–5` sur Watch Comments pour lisser la charge sur
  les vidéos qui explosent (10k+ vues/24 h).
- **Activation** : bascule le scénario sur **ON** une fois testé.

---

## 5. Test avant mise en route

1. Laisse le scénario **désactivé**, clique **Run once**.
2. Va commenter `boite a outils` sous une de tes publications (depuis un autre
   compte ou demande à un proche).
3. Relance **Run once** → vérifie que la réponse publique apparaît bien sous le
   commentaire avec le bon lien.
4. Si OK → active le scénario (**ON**).

---

## 6. Point d'attention Facebook (à savoir)

- Facebook peut **masquer** des commentaires contenant des liens s'ils sont jugés
  répétitifs. La rotation des textes (section 3) réduit fortement ce risque, mais
  surveille les premiers jours que tes réponses restent visibles.
- Si tu veux réduire encore le risque, tu peux mettre le lien **sans `https://`**
  (ex. `la-boite-a-outils.netlify.app`) dans certaines variantes — Facebook le
  rend quand même cliquable la plupart du temps et c'est perçu comme moins « spam ».

---

## Statut de mise en place

- [x] Scénario spécifié et figé (ce document)
- [ ] Import / construction dans le compte Make `segbakone@gmail.com`
      *(à faire dès que le connecteur Make est de nouveau stable — il clignotait
      au moment de la rédaction)*
- [ ] Autorisation OAuth de la Page « IA POUR 40/50 ANS » (action utilisateur)
- [ ] Test « Run once » validé
- [ ] Scénario activé (ON)
