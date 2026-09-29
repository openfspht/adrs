# ADR-0012 : Paiement de proximité, mode présenté par le client

- Statut : Proposée
- Date : 2026-09-06
- Règles : [spec/proximite.md](../spec/proximite.md)

## Contexte

Au comptoir, le marchand ne connaît pas le payeur et ne doit pas lui demander son numéro.
L'interaction existe déjà : un code lu à voix haute ou un QR affiché par l'application du payeur.
Aucun opérateur haïtien ne l'expose aujourd'hui dans une API, donc aucune passerelle ne peut la
traduire : cette spécification s'adresse aux opérateurs, et sa cible de conformité est une
implémentation native.

## Décision

- Le payeur affiche un jeton opaque, à usage unique, de courte durée (180 secondes au plus
  recommandées),
  d'au moins 64 bits, ne révélant pas son identité. Seule la chaîne est spécifiée, pas le
  support.
- Le marchand soumet `payer_token` avec le montant sur `POST /v1/payments` ; le jeton est résolu
  à la création ; la décision du payeur est une demande de confirmation.
- `payer` reste nul : le marchand n'apprend jamais l'identité du payeur.
- La passerelle ne conserve, ne journalise ni ne renvoie le jeton.
- Comportement fixé pour quatre défaillances : double scan, jeton expiré, payeur parti, réseau
  perdu.
- Trois codes d'erreur ; capacité `payments.proximity_cpm`, qui exige `confirmation_requests`.

## Conséquences

- La protection contre le double débit repose sur trois couches : clé d'idempotence,
  `reference`, jeton à usage unique.
- 64 bits est un compromis d'ergonomie (lecture à voix haute) compensé par l'usage unique et la
  durée de vie.
- L'attaque réaliste est la photo de l'écran ; la défense est l'écran de confirmation du payeur,
  qui montre montant et marchand.
- Minimisation des données conforme à BRH-131 §6.10.2 et §6.10.3 ; l'identification du payeur
  reste chez l'opérateur (BRH-121 §13.1).
- Aucun repli pour un téléphone sans application : la capacité est simplement absente.

## Alternatives écartées

- **Mode présenté par le marchand (QR fixe)** : le montant est saisi par le payeur ; fera l'objet
  d'une ADR distincte.
- **Jeton contenant le numéro chiffré** : chaîne stable, donc traçable.
- **Format de charge utile QR (type EMVCo)** : exclurait le code lu à voix haute.
- **Montant saisi par le payeur** : pas de rapprochement ni de preuve en cas de litige.
- **Paiement créé avant résolution du jeton** : transforme une erreur de scan en paiement échoué.
- **Point d'accès dédié** : même ressource, surface doublée.

## Questions ouvertes

- Un reçu sans identifiant du payeur satisfait-il BRH-121 §8.
- Un identifiant de payeur masqué pour le marchand.
- Limite de demandes par payeur chez l'opérateur.
- 64 ou 128 bits d'entropie.
- Payeurs sans smartphone : variante USSD ou ADR distincte.
