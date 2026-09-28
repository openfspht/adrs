# ADR-0011 : Demandes de confirmation

- Statut : Proposée
- Date : 2026-09-06
- Règles : [spec/demandes-de-confirmation.md](../spec/demandes-de-confirmation.md)

## Contexte

`payer_approval` suffit pour un achat en ligne. À un comptoir, le vendeur doit savoir combien
de temps attendre, distinguer un refus d'une invite non reçue, abandonner pour servir le client
suivant, et gérer un jeton scanné deux fois ou un réseau tombé après soumission. Ces besoins
forment un objet : une échéance, des états terminaux distincts, une annulation, un
comportement déterministe en cas de répétition.

## Décision

- Ressource distincte, `confirmation_request`, avec sa propre machine à états (`awaiting`,
  `approved`, `declined`, `expired`, `canceled`) ; aucun état de paiement ajouté.
- Échéance obligatoire, 60 secondes par défaut, 300 au plus ; expiration confirmée, jamais par
  horloge.
- Une approbation n'est pas un reçu : la remise se fonde sur `succeeded` du paiement.
- Annulation asynchrone (`202`), confirmée par l'opérateur, pouvant perdre contre une
  approbation.
- Nouveau `next_action` `confirmation_request` ; quatre types d'événement.
- Capacités `confirmation_requests` et `confirmation_requests.cancel`, non émulables.

## Conséquences

- Le comptoir affiche un compte à rebours et un dénouement distinct pour chaque cas.
- Le reçu exigé par BRH-121 §8 n'est produit qu'après capture.
- L'annulation porte sur une demande non approuvée, qui n'est pas encore un ordre : elle ne
  contredit pas l'irrévocabilité de BRH-121 §13.5.
- La décision du payeur est enregistrée et horodatée séparément du paiement (traçabilité,
  BRH-121 §13.1).
- Ajouts non cassants : un type de `next_action`, quatre types d'événement.

## Alternatives écartées

- **`expires_at` ajouté à `payer_approval`** : ne distingue pas refus et expiration, pas
  d'annulation.
- **État de paiement `awaiting_confirmation`** : rupture de la machine de base.
- **`approved` signifiant capturé** : cache l'écart où se produisent les pertes.
- **Expiration par horloge** : « expiré » affiché pour un payeur débité.
- **Annulation synchrone** : l'opérateur possède la décision.
- **Intégration dans la spec de proximité** : l'objet sert tout flux à décision minutée.

## Questions ouvertes

- Contre-proposition du payeur (pourboire, arrondi).
- Prolongation de l'échéance.
- Plusieurs demandes successives pour un même paiement.
- Fonctionnement sans connectivité.
