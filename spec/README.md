# Spécification OpenFSP

Je propose ici les règles normatives d'OpenFSP ; je justifie chacun de mes choix dans les [ADR](https://github.com/openfspht/adrs/tree/main/text).

## Mots-clés

DOIT, NE DOIT PAS, DEVRAIT, NE DEVRAIT PAS, PEUT, OBLIGATOIRE, RECOMMANDÉ et FACULTATIF
s'interprètent comme MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, REQUIRED, RECOMMENDED et
OPTIONAL au sens des RFC 2119 et RFC 8174, lorsqu'ils sont en capitales. Leurs formes
accordées (DOIVENT, DEVRAIENT, PEUVENT, OBLIGATOIRES, FACULTATIVE) ont le même sens.

## Vocabulaire

| Terme | Sens |
|---|---|
| opérateur | Service de paiement vers lequel la passerelle traduit (MonCash, NatCash…) ; désigné « FSP » dans les circulaires BRH. |
| passerelle | Implémentation d'OpenFSP qui reçoit les requêtes des clients. Elle sert un seul marchand, à qui appartiennent toutes ses ressources. |
| exploitant | Qui déploie et administre une passerelle. |
| client | Application qui appelle la passerelle. |
| abonné | Point d'accès qui reçoit les webhooks d'une passerelle. |
| vérificateur | Partie qui vérifie la signature d'un événement : abonné, auditeur ou bibliothèque. |
| principal | Identité authentifiée d'un client. |

## Documents

| Document | Nature |
|---|---|
| [Modèle de données](modele-de-donnees.md) | Normatif |
| [Cycle de vie du paiement](cycle-de-vie.md) | Normatif |
| [Idempotence](idempotence.md) | Normatif |
| [API HTTP : paiements](api-paiements.md) | Normatif |
| [Découverte de capacités](capacites.md) | Normatif |
| [Webhooks](webhooks.md) | Normatif |
| [Authentification](authentification.md) | Normatif |
| [Conformité](conformite.md) | Normatif |
| [Matrice de conformité](matrice-de-conformite.md) | Informatif |
| [Architecture et périmètre](architecture.md) | Informatif |
