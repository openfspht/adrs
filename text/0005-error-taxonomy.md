# ADR-0005 : Erreurs

- Statut : Proposée
- Date : 2026-08-17
- Règles : [spec/erreurs.md](../spec/erreurs.md)

## Contexte

Face à une erreur, un client doit savoir s'il peut renvoyer et si l'opération a pu avoir lieu.
Un code de statut ne répond pas à la seconde question : un `503` et un `504` ne disent pas de
façon fiable si un débit a eu lieu. Les clients encodent leurs propres suppositions, qui
échouent sur les chemins rares.

## Décision

- Format RFC 9457 (`application/problem+json`), identifié par `type` sous l'autorité
  permanente `openfsp.org`.
- Deux extensions obligatoires : `retryable` (renvoi sans danger) et `effect` (`none` ou
  `unknown`), indépendantes l'une de l'autre.
- `request_id` sur toute erreur.
- Catalogue fermé, avec statut, `retryable` et `effect` fixés par type : 19 types de base et 3
  propres au paiement de proximité.
- Un paiement refusé est une réponse `200` avec `status: failed`, jamais une erreur.
- `provider_detail` relaie l'erreur brute de l'opérateur, sans interprétation, caviardée.
- `idempotency-key-reused` en `422`, `idempotency-request-in-progress` en `409`, comme le
  brouillon IETF.

## Conséquences

- Un client générique réagit correctement sans embarquer le catalogue ; un type inconnu se
  replie sur `status`, `retryable` et `effect`, et l'ajout d'un type ne casse rien.
- Changer le statut, `retryable` ou `effect` d'un type existant est une rupture.
- `effect` rend rapportable la question de BRH-131 §6.1 s) : l'opération défaillante a-t-elle
  pris effet. Le catalogue fermé donne des catégories comparables entre institutions pour le
  rapport trimestriel des plaintes (BRH-131 §6.11.5).
- Le domaine `openfsp.org` doit rester enregistré en permanence.

## Alternatives écartées

- **Objet d'erreur maison** : pas de type de média, pas d'outillage, pas d'extension définie.
- **Membre `code` doublant `type`** : deux identifiants pour une chose finissent par diverger.
- **Rejouabilité déduite du statut** : faux pour `429` et pour le `409` rejouable.
- **Indétermination implicite dans le statut** : les implémentations choisissent entre `502`,
  `503` et `504` au jugé.
- **Paiement refusé en `4xx`** : confond un paiement refusé et une requête qui n'a jamais
  atteint l'opérateur.
- **Localisation par défaut** : mélange de langues dans les journaux.

## Questions ouvertes

- `errors` obligatoire pour `invalid-field`.
- Un vocabulaire fermé pour `errors[].code`.
- Une troisième valeur d'`effect` pour une opération partiellement appliquée.
- Les en-têtes `RateLimit`.
