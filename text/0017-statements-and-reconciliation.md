# ADR-0017 : Relevés et rapprochement

- Statut : Proposée
- Date : 2026-09-28
- Règles : [spec/releves.md](../spec/releves.md)

## Contexte

Un marchand rapproche chaque jour ce qu'il a vendu avec ce qu'il a reçu. `payments.statement`
fait du relevé de l'opérateur une source de finalité
([cycle de vie §6.7](../spec/cycle-de-vie.md)), mais le relevé reste interne à la passerelle :
le client n'en voit ni les lignes, ni les écarts.

Trois écarts coûtent de l'argent : des fonds reçus sans paiement connu (paiement hors
passerelle, création sans réponse), un paiement `succeeded` absent du relevé, un montant
différent. Le montant net reçu n'est rapporté nulle part.

Les opérateurs arrêtent leurs relevés par journée, à l'heure de Port-au-Prince ; la
spécification ne connaît que l'UTC.

## Décision

- Le relevé devient une ressource lisible par le client, par opérateur et **journée
  comptable**.
- Une journée comptable est une date locale : celle de l'opérateur s'il la fournit, sinon la
  date dans le fuseau `America/Port-au-Prince`. Nouveau type `Date` (`AAAA-MM-JJ`).
- Chaque ligne porte le montant brut, les frais et le **montant net** tels que l'opérateur les
  rapporte, jamais recalculés.
- La passerelle rapproche chaque ligne d'un paiement et publie le résultat : rapprochée, sans
  paiement, en conflit. Elle publie aussi les paiements `succeeded` absents d'un relevé clos.
- Une ligne sans paiement ne crée jamais de paiement.
- La ressource est offerte là où `payments.statement` est annoncée. Nouvelle portée
  `statements:read`.

## Conséquences

- Le rapprochement quotidien se fait contre l'API, sans export manuel du portail de
  l'opérateur.
- Les fonds reçus hors passerelle deviennent visibles au lieu d'être ignorés.
- Les montants de ligne peuvent être négatifs (reversement, frais) : c'est l'exception prévue au
  [modèle de données §3.6](../spec/modele-de-donnees.md).
- Un relevé importé à la main reste une attestation de l'exploitant
  ([cycle de vie §6.8](../spec/cycle-de-vie.md)) : ses lignes sont marquées comme telles.
- Un opérateur sans relevé authentifié n'offre pas de relevé : le marchand garde son outil
  actuel.

## Alternatives écartées

- **Montant net dans `Payment`** : le net n'est connu qu'au relevé, et un paiement n'a pas de
  ligne de frais ni de reversement.
- **Net calculé par la passerelle** : `amount - fee` est faux dès que l'opérateur arrondit,
  regroupe ou prélève plus tard.
- **Journée en UTC** : ne correspond à aucun relevé d'opérateur et coupe la journée de vente
  à 19 h ou 20 h.
- **Créer un paiement depuis une ligne orpheline** : invente une `Reference` et un
  consentement du marchand.
- **Export CSV** : un format par implémentation, pas de rapprochement.

## Questions ouvertes

- Événement à la clôture d'un relevé.
- Soldes d'ouverture et de clôture.
- Correction par l'opérateur d'un relevé déjà clos.
