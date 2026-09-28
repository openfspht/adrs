<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://cdn.openfsp.org/logo/openfsp-logo-inverse.svg">
  <img src="https://cdn.openfsp.org/logo/openfsp-logo.svg" alt="OpenFSP" width="320">
</picture>

</div>

# Spécification et décisions OpenFSP

- [`spec/`](spec/README.md) : les règles. Ce qu'une implémentation doit faire.
- [`text/`](https://github.com/openfspht/adrs/tree/main/text) : les ADR (Architecture Decision Records). Pourquoi chaque règle existe :
  contexte, décision, conséquences, alternatives écartées, questions ouvertes.

Chaque document de spécification renvoie à l'ADR qui le fonde, et chaque ADR à sa
spécification.

## Nature des documents

| Nature | Portée |
|---|---|
| Normatif | Lie toute implémentation conforme. Mots-clés DOIT, NE DOIT PAS, DEVRAIT, PEUT. |
| Informatif | Explique ou guide, n'exige rien. |
| Processus | Lie le projet et l'usage du nom, pas les implémentations. |

## Statuts d'une ADR

| Statut | Sens |
|---|---|
| Proposée | Ouverte à la discussion ; examen de 14 jours au moins, puis dernier appel de 7 jours. |
| Acceptée | Décidée. La changer exige une nouvelle ADR. |
| Rejetée | Examinée et déclinée, raisons consignées. Conservée. |
| Remplacée | Remplacée par une ADR nommée. Conservée. |

L'éditeur peut allonger un délai, jamais le raccourcir.

## Écrire une ADR

1. Ouvrir une issue qui décrit le problème.
2. Copier [`0000-template.md`](https://github.com/openfspht/adrs/blob/main/0000-template.md) en `text/NNNN-titre-court.md`, avec le prochain
   numéro libre ; les numéros ne sont jamais réutilisés.
3. Mettre les règles dans `spec/`, dans le document concerné ou un nouveau.
4. Ouvrir une pull request au statut Proposée.
5. L'éditeur accepte ou rejette publiquement, avec ses raisons. Un rejet est fusionné, pas
   fermé.

Ce qui exige une ADR est défini dans
[GOVERNANCE §4](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#4-comment-les-décisions-sont-prises).

## Amender

- Erratum (coquille, lien, formulation qui trahit la décision) : corrigé sur place.
- Changement de fond : nouvelle ADR, qui remplace l'ancienne.

## Références et registres

Sources citées : [`text/references.md`](text/references.md). Identifiants d'opérateur :
[registre](https://github.com/openfspht/openfsp/blob/main/registries/providers.md).

## Index

| ADR | Spécification | Nature |
|---|---|---|
| [0001](text/0001-architecture-and-scope.md) Architecture et périmètre | [architecture](spec/architecture.md) | Informatif |
| [0002](text/0002-core-data-model.md) Modèle de données | [modele-de-donnees](spec/modele-de-donnees.md) | Normatif |
| [0003](text/0003-payment-lifecycle.md) Cycle de vie du paiement | [cycle-de-vie](spec/cycle-de-vie.md) | Normatif |
| [0004](text/0004-idempotency-and-retries.md) Idempotence | [idempotence](spec/idempotence.md) | Normatif |
| [0005](text/0005-error-taxonomy.md) Erreurs | [erreurs](spec/erreurs.md) | Normatif |
| [0006](text/0006-gateway-http-api-payments.md) API HTTP des paiements | [api-paiements](spec/api-paiements.md) | Normatif |
| [0007](text/0007-capability-discovery.md) Découverte de capacités | [capacites](spec/capacites.md) | Normatif |
| [0008](text/0008-webhooks-and-event-delivery.md) Webhooks | [webhooks](spec/webhooks.md) | Normatif |
| [0009](text/0009-authentication-and-credentials.md) Authentification | [authentification](spec/authentification.md) | Normatif |
| [0010](text/0010-iso-20022-semantic-correspondence.md) Correspondance ISO 20022 | [iso-20022](spec/iso-20022.md) | Informatif |
| [0011](text/0011-confirmation-requests.md) Demandes de confirmation | [demandes-de-confirmation](spec/demandes-de-confirmation.md) | Normatif |
| [0012](text/0012-proximity-payments-cpm.md) Paiement de proximité | [proximite](spec/proximite.md) | Normatif |
| [0013](text/0013-provider-adapter-interface.md) Adaptateurs d'opérateur | [adaptateurs](spec/adaptateurs.md) | Informatif |
| [0014](text/0014-mock-server-behaviour.md) Serveur simulé | [serveur-simule](spec/serveur-simule.md) | Informatif |
| [0015](text/0015-conformance-levels-and-suite.md) Conformité | [conformite](spec/conformite.md) | Normatif |
| [0016](text/0016-conformance-marks-and-naming.md) Revendications et usage du nom | [marques](spec/marques.md) | Processus |

Aucune ADR n'est encore acceptée et rien n'est implémenté. Suivront : transferts,
remboursement, capture et annulation, acheminement multi-opérateur, reporting de rapprochement.
