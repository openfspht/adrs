# ADR-0007 : Découverte de capacités

- Statut : Proposée
- Date : 2026-08-17
- Règles : [spec/capacites.md](../spec/capacites.md)

## Contexte

Les opérateurs diffèrent : remboursement ou non, rappels signés ou non, redirection ou
approbation sur l'appareil, consultation d'état possible ou non. Une interface uniforme comble
ces écarts par émulation, et l'appelant découvre la différence au moment où elle coûte de
l'argent.

## Décision

- L'interface reste incomplète et ses manques sont découvrables : une capacité est annoncée
  par opérateur, seulement si l'opérateur la prend réellement en charge.
- Registre de noms de capacité, étendu par ADR ; extensions propriétaires sous nom DNS inversé.
- Deux points d'accès : `/.well-known/openfsp` public et minimal, `/v1/capabilities`
  authentifié et détaillé par opérateur.
- Les comportements propres à un opérateur (types de `next_action`, champs exigés, garantie
  d'expiration) sont des champs lisibles par machine, pas de la documentation.
- Ensemble annoncé = ensemble permis : une opération non annoncée est refusée.
- Sans `payments.lookup`, la synchronisation renvoie `capability-not-supported`, sauf pour un
  paiement terminal.
- Identifiants d'opérateur enregistrés dans un registre partagé, par pull request.

## Conséquences

- Un client s'écrit contre un déploiement qu'il n'a jamais vu.
- La suite de conformité teste les capacités annoncées et le refus des autres.
- Un superviseur lit ce qu'un déploiement fait sans s'en remettre à sa documentation.
- Les relations commerciales avec les opérateurs restent derrière l'authentification.
- Retirer une capacité d'un déploiement n'est pas un changement de spécification, mais une
  rupture pour les marchands qui s'en servent.

## Alternatives écartées

- **Capacités fixes par version** : fausses dès que les opérateurs diffèrent.
- **`OPTIONS` HTTP** : n'exprime ni garantie d'expiration ni types de `next_action`.
- **Essayer et traiter l'erreur** : apprendre en tentant, dans une API où une tentative peut
  déplacer de l'argent.
- **Capacités versionnées** : multiplie les combinaisons.
- **Capacités dans chaque réponse de paiement** : surcharge le chemin critique, inutile avant la
  création.
- **Capacités globales à la passerelle** : fausses pour toute passerelle multi-opérateurs.

## Questions ouvertes

- Capacités différenciées par principal.
- Découverte d'un `next_action` QR.
- Place de `display_name` dans le protocole.
