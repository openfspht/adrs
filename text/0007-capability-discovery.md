# ADR-0007 : Découverte de capacités

- Date : 2026-08-17
- Règles : [spec/capacites.md](../spec/capacites.md)

## Contexte

Les opérateurs diffèrent : remboursement ou non, rappels signés ou non, redirection ou
approbation sur l'appareil, consultation d'état possible ou non. Une interface uniforme comble
ces écarts par émulation ; l'écart n'est alors observable qu'à l'exécution d'un paiement
réel.

## Décision

Je propose :

- Une capacité d'opérateur n'est annoncée que s'il la prend en charge ; aucune émulation des
  manques.
- Registre de noms de capacité, étendu par ADR ; extensions propriétaires sous nom DNS inversé.
- Deux points d'accès : `/.well-known/openfsp` public et minimal, `/v1/capabilities`
  authentifié et détaillé par opérateur.
- Les comportements propres à un opérateur (types de `next_action`, champs exigés, garantie
  d'expiration) sont des champs lisibles par machine, pas de la documentation.
- Ensemble annoncé = ensemble permis : une opération non annoncée est refusée.
- Sans `payments.lookup`, la synchronisation renvoie `capability-not-supported`, sauf pour un
  paiement terminal.
- Identifiants d'opérateur enregistrés dans un registre partagé, par pull request.
- Plafonds de montant (reprend l'ADR-0018) : bornes et granularité (`amount_step`) du compte
  marchand, déclarées par l'exploitant et annoncées dans `limits` ; une création hors bornes est
  refusée avant l'opérateur avec `amount-out-of-range`. Les plafonds du payeur restent des
  échecs `limit_exceeded`.

## Conséquences

- Un client peut être implémenté sans connaissance préalable du déploiement ; il lit
  `/v1/capabilities`.
- La suite de conformité teste les capacités annoncées et le refus des autres.
- Un tiers muni d'une clé `capabilities:read` lit les capacités d'un déploiement sans recourir
  à sa documentation.
- La liste des opérateurs d'un marchand n'est servie qu'au point d'accès authentifié
  (capacités 3.1.1).
- Retirer une capacité d'un déploiement ne modifie pas la spécification et rompt les clients
  qui l'utilisent.
- Des bornes déclarées fausses bloquent des paiements valides ou en laissent passer : la
  passerelle ne peut pas les vérifier.

## Ce que je n'ai pas retenu

- **Capacités fixes par version** : fausses dès que les opérateurs diffèrent.
- **`OPTIONS` HTTP** : n'exprime ni garantie d'expiration ni types de `next_action`.
- **Essayer et traiter l'erreur** : détecter un manque exige une tentative, et une création
  peut débiter le payeur.
- **Capacités versionnées** : multiplie les combinaisons.
- **Capacités dans chaque réponse de paiement** : surcharge le chemin critique, inutile avant la
  création.
- **Capacités globales à la passerelle** : fausses pour toute passerelle multi-opérateurs.
- **Bornes codées dans l'adaptateur ou lues chez l'opérateur** : elles dépendent du contrat de
  chaque marchand, et aucun opérateur visé ne les expose par API.

## Questions ouvertes

- Capacités différenciées par principal.
- Découverte d'un `next_action` QR.
- Place de `display_name` dans le protocole.
- Annonce d'un plafond de solde du compte marchand.
