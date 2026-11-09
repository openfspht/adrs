# ADR-0008 : Webhooks

- Date : 2026-09-06
- Règles : [spec/webhooks.md](../spec/webhooks.md)

## Contexte

Le sondage impose une latence au moins égale à l'intervalle de sondage et une charge
proportionnelle au nombre de paiements `pending`. Les schémas de notification des opérateurs
diffèrent (architecture 8.1) ; chaque schéma exige une vérification propre, et une
vérification défaillante admet un `succeeded` forgé.

## Décision

Je propose :

- Livraison au moins une fois, non ordonnée : `sequence` par ressource et `id` de
  déduplication.
- Signature HTTP RFC 9421 sur Ed25519, clé publiée par la passerelle, composants couvrant la
  cible, le condensé du corps, l'identifiant et le type de l'événement.
- Fraîcheur de 300 secondes et nonce contre le rejeu réseau.
- Corps = instantané complet de la ressource.
- Cinq types d'événement, registre fermé ; pas de `payment.updated`.
- Renvoi en sept tentatives sur 31 heures ; un événement abandonné n'est jamais
  supprimé.
- Le sondage reste le chemin de récupération : un client sans sondage n'est pas conforme.
- Tout webhook émis par la passerelle est signé, quoi qu'ait fourni l'opérateur.

## Conséquences

- Un abonné rejette une contrefaçon par vérification de signature.
- Un événement signé par clé publique prouve à un tiers ce que la passerelle a affirmé, utile
  pour l'audit triennal de BRH-121 5 ; un HMAC ne le permet pas.
- Les événements portent le numéro du payeur : TLS avec validation obligatoire, journalisation
  restreinte côté abonné (webhooks 12.4, BRH-131 6.10.4).
- L'interdiction de supprimer un événement abandonné ou de désactiver un point d'accès sans
  trace conserve l'historique qu'exige l'analyse d'un incident.
- L'émission est une capacité (`webhooks.emit`), hors capacité de base.

## Ce que je n'ai pas retenu

- **HMAC à secret partagé** : pas de valeur probante, chaîne à signer différente à chaque
  intégration.
- **En-tête de signature maison** : impose à chaque abonné un vérificateur spécifique au
  lieu d'une bibliothèque RFC 9421.
- **TLS mutuel seul** : authentifie la connexion, pas le message.
- **Exactement une fois** : impossible sur un réseau non fiable.
- **Événements minces (identifiant seul)** : transforme chaque livraison en lecture obligatoire.
- **Lots d'événements** : succès partiel inexprimable.
- **Ordre garanti par ressource** : bloque la file sur une livraison lente.
- **Point d'accès de rejeu** : différé.

## Questions ouvertes

- Durée de conservation d'un événement abandonné.
- Acquittement par `sequence`.
