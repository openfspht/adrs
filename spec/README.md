# Spécification OpenFSP

Règles normatives. Les raisons de chaque choix sont dans les [ADR](https://github.com/openfspht/adrs/tree/main/text).

## Mots-clés

DOIT, NE DOIT PAS, DEVRAIT, NE DEVRAIT PAS, PEUT, OBLIGATOIRE, RECOMMANDÉ et FACULTATIF
s'interprètent comme MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, REQUIRED, RECOMMENDED et
OPTIONAL au sens des RFC 2119 et RFC 8174, lorsqu'ils sont en capitales.

## Vocabulaire

| Terme | Sens |
|---|---|
| opérateur | Service de paiement vers lequel la passerelle traduit (MonCash, NatCash…). |
| passerelle | Implémentation d'OpenFSP qui reçoit les requêtes des clients. |
| exploitant | Qui déploie et administre une passerelle. |
| client | Application qui appelle la passerelle. |
| principal | Identité authentifiée d'un client. |

## Documents

| Document | Nature |
|---|---|
| [Modèle de données](modele-de-donnees.md) | Normatif |
| [Cycle de vie du paiement](cycle-de-vie.md) | Normatif |
| [Idempotence](idempotence.md) | Normatif |
| [Erreurs](erreurs.md) | Normatif |
| [API HTTP : paiements](api-paiements.md) | Normatif |
| [Découverte de capacités](capacites.md) | Normatif |
| [Webhooks](webhooks.md) | Normatif |
| [Authentification](authentification.md) | Normatif |
| [Demandes de confirmation](demandes-de-confirmation.md) | Normatif |
| [Paiement de proximité](proximite.md) | Normatif |
| [Relevés et rapprochement](releves.md) | Normatif |
| [Plafonds de montant](plafonds.md) | Normatif |
| [Conformité](conformite.md) | Normatif |
| [Revendications et usage du nom](marques.md) | Processus |
| [Architecture et périmètre](architecture.md) | Informatif |
| [Correspondance ISO 20022](iso-20022.md) | Informatif |
| [Adaptateurs d'opérateur](adaptateurs.md) | Informatif |
| [Serveur simulé](serveur-simule.md) | Informatif |
