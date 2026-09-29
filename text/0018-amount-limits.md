# ADR-0018 : Plafonds de montant

- Statut : Proposée
- Date : 2026-09-28
- Règles : [spec/plafonds.md](../spec/plafonds.md)

## Contexte

Chaque compte marchand chez un opérateur a un montant minimal et maximal par transaction,
fixés par contrat ou par niveau de compte. Aujourd'hui, un paiement hors de ces bornes est
créé, part chez l'opérateur, puis finit `failed` avec `limit_exceeded`. Le client ne peut ni
masquer à l'avance un opérateur inutilisable pour un montant, ni distinguer un plafond du
marchand d'un plafond du payeur.

## Décision

- Les bornes par transaction du compte marchand sont annoncées par opérateur dans les
  capacités (`payments.limits`).
- Elles sont déclarées par l'exploitant d'après son contrat. Une borne inconnue est absente,
  jamais devinée.
- Une granularité (`amount_step`) couvre les opérateurs qui n'acceptent que des gourdes
  entières.
- Une création hors bornes est rejetée avant tout appel à l'opérateur, avec une nouvelle erreur
  `amount-out-of-range` (422) qui rappelle les bornes.
- Les plafonds du payeur (niveau de portefeuille, cumul journalier, seuils réglementaires)
  restent inconnus à l'avance et continuent de produire `failed` avec `limit_exceeded`.

## Conséquences

- Un client peut proposer seulement les opérateurs utilisables pour un montant donné.
- Aucun paiement `failed` n'est créé pour une erreur que la passerelle pouvait prévoir.
- Des bornes déclarées fausses bloquent des paiements valides ou en laissent passer : la
  passerelle ne peut pas les vérifier.
- `limit_exceeded` ne désigne plus que des plafonds que la passerelle ignorait.

## Alternatives écartées

- **Bornes codées dans l'adaptateur** : elles dépendent du contrat de chaque marchand, pas de
  l'opérateur.
- **Bornes lues chez l'opérateur** : aucun opérateur visé ne les expose par API.
- **Réutiliser `invalid-field`** : ne permet pas au client de distinguer un montant mal formé
  d'un montant hors bornes, ni de lire les bornes.
- **Plafonds cumulés du marchand** (réception journalière, solde maximal du portefeuille) :
  la passerelle ne connaît pas le solde ; ils restent des échecs chez l'opérateur.

## Questions ouvertes

- Annonce d'un plafond de solde du compte marchand : MonCash le signale
  (`Maximum Account Balance`) sans l'exposer.
- Bornes différentes selon le type de `next_action`.
