# Automatisation WhatsApp — Coach KONE

But : les prospects qui écrivent sur le WhatsApp Business du Coach KONE sont accueillis, qualifiés, et relancés automatiquement par Claude, sans écrire une ligne de code. Tout tourne dans **Make** (make.com), déjà connecté au compte du coach.

## Comment ça marche, en une image

```
Un prospect écrit sur WhatsApp
        │
        ▼
Make reçoit le message (module "WhatsApp Business Cloud")
        │
        ▼
Make va chercher sa fiche dans le Data Store "Prospects WhatsApp"
(ou en crée une nouvelle s'il écrit pour la première fois)
        │
        ▼
Claude lit l'historique + le nouveau message,
qualifie le prospect et rédige la réponse
        │
        ▼
Make envoie la réponse sur WhatsApp
        │
        ▼
Make met à jour la fiche du prospect (statut, notes, dernier contact)
```

Un deuxième scénario, déclenché toutes les quelques heures, repère les prospects qui n'ont pas répondu et les relance.

## Ce qui est déjà en place

- **Data Store Make** `Prospects WhatsApp` (id `183853`) : la fiche de chaque prospect (téléphone, statut, historique, notes, dernier contact, nombre de relances).
- **Demande de connexion Make** : un lien pour autoriser en une fois le compte WhatsApp Business et la clé Claude. Ce lien reste valable, à ouvrir dès que vous avez les informations de la section suivante.
- **Le prompt de qualification** : voir [`prompt-qualification.md`](./prompt-qualification.md) — c'est le texte qui donne à Claude toutes les infos sur le programme et la façon de répondre. Vous pouvez le modifier ici, puis le recopier dans le module Claude de Make.

## Ce qu'il reste à faire côté Meta (WhatsApp)

Le WhatsApp Business "app gratuite" ne suffit pas pour être piloté automatiquement. Il faut activer la version professionnelle (le "WhatsApp Business Platform") chez Meta. Comptez de quelques heures à 2-3 jours pour la vérification.

1. **Compte Meta Business** — sur [business.facebook.com](https://business.facebook.com), créer ou utiliser votre compte entreprise, et le faire vérifier.
2. **Application développeur** — sur [developers.facebook.com](https://developers.facebook.com/apps), créer une appli de type "Entreprise", puis ajouter le produit **WhatsApp**.
3. **Numéro WhatsApp** — dans la configuration WhatsApp de l'appli, valider le numéro professionnel qui recevra les prospects (il doit être libre, pas déjà utilisé dans l'appli WhatsApp classique sur un téléphone).
4. **Jeton d'accès permanent** — dans les paramètres de l'entreprise Meta, créer un "Utilisateur système", lui donner un accès Admin sur l'appli WhatsApp, puis générer un jeton permanent avec les droits `whatsapp_business_messaging` et `whatsapp_business_management`. C'est ce jeton que Make vous demandera.
5. Notez le **Phone Number ID** et le **WhatsApp Business Account ID**, visibles dans l'appli, section WhatsApp > Démarrage.
6. **Clé Claude** — sur [console.anthropic.com](https://console.anthropic.com), section API Keys, générer une clé.
7. Ouvrir le lien de connexion Make fourni par Claude Code, et coller le jeton Meta d'un côté, la clé Anthropic de l'autre.

Une fois les deux connexions faites, dites-le pour que le scénario Make soit terminé et activé (déclencheur WhatsApp + module Claude + envoi de la réponse + mise à jour de la fiche prospect).

## Une règle importante à connaître : la fenêtre des 24h

WhatsApp interdit d'envoyer un message "libre" à quelqu'un qui n'a pas écrit depuis plus de 24h — il faut alors utiliser un **modèle de message pré-approuvé par Meta** (un "template"). Conséquence concrète :
- Une **réponse** à un prospect qui vient d'écrire → message libre, rédigé par Claude, aucun souci.
- Une **relance** à un prospect silencieux depuis plus de 24h → doit passer par un template WhatsApp validé à l'avance par Meta (ça prend quelques heures à être approuvé, une seule fois).

Exemple de template à soumettre pour les relances (catégorie "Marketing") :
> Bonjour {{1}}, c'est Coach KONE 👋 Je repense à notre échange sur vos douleurs articulaires. On regarde ensemble si le programme peut vous aider ?

## Statuts utilisés pour chaque prospect

`nouveau` · `qualifie_chaud` · `qualifie_tiede` · `qualifie_froid` · `proposition_envoyee` · `a_contacter_humain` · `converti` · `perdu`

`a_contacter_humain` signale un cas où mieux vaut que le coach reprenne la main lui-même (question sensible, situation médicale, forte envie d'acheter avec une question pointue...).

## Comment tester une fois branché

1. Écrire "Bonjour" depuis un téléphone vers le numéro WhatsApp Business.
2. Vérifier dans Make (onglet Historique du scénario) que l'exécution s'est bien déroulée.
3. Vérifier dans le Data Store qu'une fiche a été créée avec un statut cohérent.
4. Répondre en donnant une info (ex. "j'ai mal aux genoux depuis 2 ans") et vérifier que la réponse suivante en tient compte.
