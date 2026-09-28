# ADR-0006 : API HTTP des paiements

- Statut : Proposée
- Date : 2026-08-17
- Règles : [spec/api-paiements.md](../spec/api-paiements.md)

## Contexte

Un marchand a besoin de créer un paiement et de savoir ce que le payeur doit faire, de le relire
par identifiant ou par sa propre référence (seule donnée dont il dispose après une coupure), et
de forcer une relecture chez l'opérateur quand un rappel se perd. Toute opération ajoutée au
socle devrait être implémentable par chaque opérateur.

## Décision

- Conventions : HTTPS, `/v1` dans le chemin, JSON, erreurs RFC 9457, `Request-Id` sur toute
  réponse, collections enveloppées dans `data`.
- Capacité de base `payments`, sans découverte préalable : créer, lire (par `id` ou par
  `reference`), synchroniser.
- Le client nomme l'opérateur ; aucun acheminement automatique.
- `next_action` fermé à trois types : `redirect`, `payer_approval`, `none`.
- Synchronisation en `POST` (non sûre : elle appelle l'opérateur), exemptée d'idempotence : une
  réponse rejouée renverrait un état périmé.
- Une référence inconnue donne `200` avec `data` vide.
- Le retour du payeur sur `return_url` ne prouve rien.
- `fee` est rapporté, jamais fourni par le client.

## Conséquences

- La ressource porte six des sept mentions du reçu de BRH-121 §8 ; la nature du service reste
  au marchand (`description` ou `metadata`).
- `provider` et `provider_reference` tracent chaque paiement jusqu'à l'opérateur.
- Ajouter un type de `next_action` est une rupture ; ajouter un champ facultatif ne l'est pas.
- Les conventions du §1 lient toutes les spécifications suivantes.

## Alternatives écartées

- **Choix de l'opérateur par la passerelle** : décision commerciale et réglementaire cachée.
- **`GET ?synchronize=true`** : rendrait `GET` non sûr.
- **`404` pour une référence inconnue** : ambigu entre absence de paiement et chemin inexistant.
- **Chemin `/by-reference/{reference}`** : seconde URL pour la même ressource.
- **`next_action` réduit à une URL** : n'exprime pas l'approbation sur l'appareil du payeur.
- **Point d'accès de liste** : différé ; pagination et filtrage à spécifier sur usage réel.

## Questions ouvertes

- `provider` facultatif quand la passerelle ne sert qu'un opérateur.
- Le nom `synchronize`.
- Garantir ou non l'affichage de `description` au payeur.
- Un type `next_action` pour code QR, à trancher avant 1.0.
- Paiement partiel ou excédentaire.
