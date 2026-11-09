<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://cdn.openfsp.org/logo/openfsp-logo-inverse.svg">
  <img src="https://cdn.openfsp.org/logo/openfsp-logo.svg" alt="OpenFSP" width="320">
</picture>

</div>

# Spécification et décisions OpenFSP

Je propose ici la norme OpenFSP, dans le cadre de mon master MBDS : les règles normatives
dans [`spec/`](spec/README.md), les décisions qui les fondent dans
[`text/`](https://github.com/openfspht/adrs/tree/main/text), les sources dans
[`text/references.md`](text/references.md) et les identifiants d'opérateur dans le
[registre](https://github.com/openfspht/openfsp/blob/main/registries/providers.md).
Quand je reviens sur une décision, une nouvelle ADR la remplace ; un numéro n'est jamais
réutilisé.

## Index

| ADR | Spécification | Nature |
|---|---|---|
| [0001](text/0001-architecture-and-scope.md) Architecture et périmètre | [architecture](spec/architecture.md) | Informatif |
| [0002](text/0002-core-data-model.md) Modèle de données | [modele-de-donnees](spec/modele-de-donnees.md) | Normatif |
| [0003](text/0003-payment-lifecycle.md) Cycle de vie et relevés | [cycle-de-vie](spec/cycle-de-vie.md) | Normatif |
| [0006](text/0006-gateway-http-api-payments.md) API, erreurs et idempotence | [api-paiements](spec/api-paiements.md), [idempotence](spec/idempotence.md) | Normatif |
| [0007](text/0007-capability-discovery.md) Capacités et plafonds | [capacites](spec/capacites.md) | Normatif |
| [0008](text/0008-webhooks-and-event-delivery.md) Webhooks | [webhooks](spec/webhooks.md) | Normatif |
| [0009](text/0009-authentication-and-credentials.md) Authentification | [authentification](spec/authentification.md) | Normatif |
| [0015](text/0015-conformance-levels-and-suite.md) Conformité et serveur simulé | [conformite](spec/conformite.md) | Normatif |

J'ai fusionné 0004, 0005, 0013, 0014, 0016, 0017 et 0018 dans les ADR ci-dessus ou
dans la [gouvernance 8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité) ;
je garde 0010 (ISO 20022), 0011 et 0012 (paiement au comptoir) pour une version ultérieure,
avec les transferts, le remboursement, la capture, l'annulation et l'acheminement
multi-opérateur.

## Aperçu local

```
docker build -t openfsp-adrs . && docker run -p 8080:8080 openfsp-adrs
```
