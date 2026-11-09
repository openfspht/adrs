# ADR-0006 : API HTTP des paiements

- Date : 2026-08-17
- Règles : [spec/api-paiements.md](../spec/api-paiements.md), [spec/idempotence.md](../spec/idempotence.md)

## Contexte

Je pars des besoins du marchand : créer un paiement et connaître l'action attendue du payeur ; le
relire par identifiant ou par sa propre référence (seule donnée dont il dispose après une
coupure) ; forcer une relecture chez l'opérateur quand un rappel se perd. Toute opération
ajoutée à la capacité de base `payments` devrait être implémentable par chaque opérateur.

## Décision

Je propose :

- Conventions : HTTPS, `/v1` dans le chemin, JSON, erreurs RFC 9457, `Request-Id` sur toute
  réponse, collections enveloppées dans `data`.
- Capacité de base `payments`, sans découverte préalable : créer, lire (par `id` ou par
  `reference`), synchroniser.
- Le client nomme l'opérateur ; aucun acheminement automatique.
- `next_action` fermé à trois types : `redirect`, `payer_approval`, `none`.
- Synchronisation en `POST` (non sûre : elle appelle l'opérateur), exemptée d'idempotence : une
  réponse rejouée renverrait un état périmé.
- Une référence inconnue donne `200` avec `data` vide.
- Le retour du payeur sur `return_url` ne prouve pas le paiement. Si l'opérateur ne prend qu'une URL de
  retour fixe (MonCash), la passerelle la relaie vers la `return_url` du paiement.
- Langue de la page du payeur (`locale` : `fr`, `ht`, `en`), transmise si l'opérateur
  l'accepte.
- `fee` est rapporté, jamais fourni par le client.
- Un `405` porte le code `method-not-allowed`, ajouté au catalogue fermé des erreurs.
- Erreurs (reprend l'ADR-0005) : format RFC 9457 sous l'autorité `openfsp.org`, avec deux
  extensions obligatoires, `retryable` et `effect` (`none` ou `unknown`), et `request_id`.
  Catalogue fermé de 19 types ; un paiement refusé est un `200` avec `status: failed`, jamais une
  erreur.
- Idempotence (reprend l'ADR-0004) : `Idempotency-Key` obligatoire sur toute opération
  idempotente (idempotence 1), la synchronisation exceptée ; exécution au plus une fois par
  (principal, opération, clé), réponse rejouée, seuls les dénouements déterminés enregistrés. L'unicité permanente de la `reference` protège le
  paiement au-delà de la rétention, et aucun renvoi automatique ne part vers un opérateur sans
  idempotence ni recherche. L'identifiant de commande transmis à l'opérateur est un HMAC de la
  `reference`, stocké et visible du marchand (`provider_order_id`).

## Conséquences

- La ressource porte six des sept mentions du reçu de BRH-121 8 ; la nature du service reste
  au marchand (`description` ou `metadata`).
- `provider` et `provider_reference` tracent chaque paiement jusqu'à l'opérateur.
- Ajouter un type de `next_action` hors d'une capacité est une rupture ; une capacité peut en
  introduire un, produit seulement pour les opérateurs qui l'annoncent. Ajouter un champ
  facultatif n'est pas une rupture.
- Les conventions de l'API 1 s'appliquent à tout point d'accès OpenFSP.
- Un client traite un type d'erreur inconnu par `status`, `retryable` et `effect`
  (API 10.3.6).
- Un renvoi avec la même clé n'exécute pas l'opération deux fois ; la passerelle conserve des
  réponses contenant des données personnelles 24 heures au moins.

## Ce que je n'ai pas retenu

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
- Rétention minimale des enregistrements d'idempotence : 24 heures ou 7 jours.
- Une troisième valeur d'`effect` pour une opération partiellement appliquée.
