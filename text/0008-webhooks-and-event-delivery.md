# ADR-0008 : Webhooks

- Statut : Proposée
- Date : 2026-09-06
- Règles : [spec/webhooks.md](../spec/webhooks.md)

## Contexte

Le sondage a un plancher de latence et un coût de charge. Chaque opérateur invente sa propre
notification (secret en paramètre, HMAC sur une concaténation non documentée, ou rien), et un
marchand qui en intègre trois écrit trois vérifications, dont une fausse, jusqu'à ce qu'un
`succeeded` fabriqué soit posté sur son point d'accès public.

## Décision

- Livraison au moins une fois, non ordonnée : `sequence` par ressource et `id` de
  déduplication.
- Signature HTTP RFC 9421 sur Ed25519, clé publiée par la passerelle, composants couvrant la
  cible, le condensé du corps, l'identifiant et le type de l'événement.
- Fraîcheur de 300 secondes et nonce contre le rejeu réseau.
- Corps = instantané complet de la ressource.
- Cinq types de transition, registre fermé ; pas de `payment.updated`.
- Calendrier de renvoi de sept tentatives sur 31 heures ; un événement abandonné n'est jamais
  supprimé.
- Le sondage reste le chemin de récupération : un client sans sondage n'est pas conforme.
- Ce qui sort de la passerelle est signé, quel que soit ce qu'a fourni l'opérateur.

## Conséquences

- Un abonné rejette une contrefaçon au lieu de la soupçonner.
- Un événement signé par clé publique prouve à un tiers ce que la passerelle a affirmé, utile
  pour l'audit triennal de BRH-121 §5 ; un HMAC ne le permet pas.
- Les événements portent le numéro du payeur : TLS avec validation obligatoire, et discipline
  de journalisation côté abonné (BRH-131 §6.10.4).
- L'interdiction de supprimer un événement abandonné ou de désactiver un point d'accès sans
  trace conserve l'historique qu'exige l'analyse d'un incident.
- L'émission est une capacité (`webhooks.emit`), hors socle.

## Alternatives écartées

- **HMAC à secret partagé** : pas de valeur probante, chaîne à signer différente à chaque
  intégration.
- **En-tête de signature maison** : reporte la complexité sur chaque abonné.
- **TLS mutuel seul** : authentifie la connexion, pas le message.
- **Exactement une fois** : impossible sur un réseau non fiable.
- **Événements minces (identifiant seul)** : transforme chaque livraison en lecture obligatoire.
- **Lots d'événements** : succès partiel inexprimable.
- **Ordre garanti par ressource** : bloque la file sur une livraison lente.
- **Point d'accès de rejeu** : différé.

## Questions ouvertes

- Durée de conservation d'un événement abandonné.
- Acquittement par `sequence`.
- Profil de livraison rapide pour les demandes de confirmation.
