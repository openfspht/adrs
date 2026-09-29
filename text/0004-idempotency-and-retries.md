# ADR-0004 : Idempotence des requêtes

- Statut : Proposée
- Date : 2026-08-17
- Règles : [spec/idempotence.md](../spec/idempotence.md)

## Contexte

Une coupure réseau après l'arrivée d'une requête et avant sa réponse laisse le client sans
moyen de savoir si l'opération a eu lieu. Renvoyer peut débiter deux fois ; ne pas renvoyer
peut perdre le paiement. L'information manquante est côté serveur.

## Décision

- `Idempotency-Key` est OBLIGATOIRE sur toute requête qui modifie un état.
- La passerelle exécute au plus une fois par (principal, opération, clé) et rejoue la réponse
  enregistrée ; une clé réutilisée avec un autre corps est rejetée.
- Seuls les dénouements déterminés sont enregistrés.
- La clé protège la requête pendant la rétention ; l'unicité permanente de la `reference`
  protège le paiement au-delà.
- Aucun renvoi automatique vers un opérateur sans idempotence ni recherche.
- L'identifiant de commande transmis à l'opérateur est un HMAC de la `reference` sous une clé
  de la passerelle : il tient dans les limites de l'opérateur (50 caractères chez NatCash),
  n'est pas devinable, et la passerelle retrouve un paiement chez l'opérateur sans rien avoir
  stocké.

Le mécanisme suit le brouillon IETF `Idempotency-Key` et ajoute trois contraintes : le
cloisonnement par principal, la double protection clé et référence, et le refus de renvoyer
vers un opérateur qui ne déduplique pas.

## Conséquences

- Renvoi sans risque côté client.
- Une requête sans clé échoue en `400` dès le premier appel.
- La passerelle stocke des réponses contenant des données personnelles, 24 heures au moins.
- Les rejeux sont identifiables dans les journaux par `Idempotent-Replay`.
- Chez un opérateur sans idempotence ni recherche, les opérations indéterminées demandent
  une intervention de l'exploitant.

## Alternatives écartées

- **Clé facultative** : absente chez les clients qui en ont le plus besoin.
- **Déduplication sur le contenu** : fusionne deux achats identiques légitimes.
- **`reference` comme clé** : un renvoi reçoit un conflit au lieu de la réponse d'origine, et
  les opérations sans paiement restent sans protection.
- **Fenêtre de temps fixe** : arbitraire.
- **Empreinte sur les octets bruts** : une resérialisation du JSON provoque un faux conflit.

## Questions ouvertes

- Rétention minimale : 24 heures ou 7 jours.
- Le test d'exemption (§1.4) n'a été éprouvé que sur une opération.
- Renvoi concurrent : attendre ou rejeter ; autoriser les deux affaiblit la conformité.
- `Date` et en-têtes voisins d'une réponse rejouée : valeur d'origine ou du rejeu.
