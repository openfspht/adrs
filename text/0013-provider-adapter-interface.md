# ADR-0013 : Adaptateurs d'opérateur

- Statut : Proposée
- Date : 2026-09-07
- Guide : [spec/adaptateurs.md](../spec/adaptateurs.md) (informatif)

## Contexte

Le gain `O + L` suppose qu'un adaptateur soit petit, borné, et relisible par un autre que son
auteur. Ses erreurs typiques sont des fautes d'honnêteté invisibles de l'extérieur : projeter un
statut inconnu sur l'état le plus proche, annoncer `payments.lookup` en relisant son propre
stockage, renvoyer un débit expiré.

## Décision

- Document informatif : aucune obligation nouvelle, les règles citées viennent des
  spécifications normatives.
- Aucune interface de langage imposée.
- Trois refus : pas de capacité inventée, pas de terminalité inventée, pas de renvoi
  invérifiable.
- Correspondance des statuts totale ou documentée comme partielle, de l'opérateur vers OpenFSP.
- Chaque adaptateur publie un document : capacités, correspondances, stratégie d'idempotence,
  rappels, pertes connues, identifiants requis.

## Conséquences

- Un exploitant sait, avant déploiement, si un débit indéterminé se résout seul ou attend une
  personne.
- La déclaration mensongère de `webhooks.verify` n'est détectable que par relecture.
- L'adaptateur est le code le plus sensible : identifiants d'opérateur, analyse d'entrées
  influencées par un attaquant.

## Alternatives écartées

- **Interface d'adaptateur normative** : figerait une conception avant deux opérateurs
  implémentés.
- **Interface au niveau du langage** : lierait la spécification à Kotlin.
- **Ne rien documenter** : les règles restent dispersées dans quatre spécifications.
- **Adaptateurs générés depuis la documentation des opérateurs** : cette documentation est peu
  fiable sur les défaillances.

## Questions ouvertes

- Adaptateurs dans le dépôt de la passerelle ou à l'extérieur : relecture par le projet contre
  adoption libre par les opérateurs ; piste probable, un petit ensemble interne et un point
  d'extension documenté.
- Document d'adaptateur lisible par machine.
- Refus local d'un paiement (montant minimum) avant appel à l'opérateur.
- Signalement d'un changement de comportement de l'opérateur.
