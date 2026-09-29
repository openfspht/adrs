# ADR-0001 : Architecture et périmètre

- Statut : Proposée
- Date : 2026-08-16
- Guide : [spec/architecture.md](../spec/architecture.md) (informatif)

## Contexte

Haïti a des services de paiement numérique qui fonctionnent et aucune interopérabilité entre
eux. 14 % des micro, petites et moyennes entreprises sont bancarisées (BRH, d'après FinScope
2023) ; ce sont elles qui intègrent les interfaces de paiement. Chaque opérateur a sa propre
API, ses statuts, ses erreurs : un marchand qui accepte deux opérateurs écrit deux intégrations,
et chaque langage refait le travail. Les bacs à sable des opérateurs permettent de tester un
paiement réussi, pas de provoquer une défaillance à la demande. Le coût croît comme
`opérateurs × applications`.

Le secteur le constate : la Circulaire 121 « pose le principe mais ne définit ni les standards
techniques, ni les protocoles d'échange » (Ekosistèm Fintèk Ayiti). Le CPMI et la Banque
mondiale font le même diagnostic, et avertissent qu'une passerelle peut vivre de la
fragmentation qu'elle prétend réduire.

## Décision

- Une spécification ouverte, une passerelle auto-hébergée par le marchand, un serveur simulé
  et des bibliothèques clientes minces. Coût ramené à `opérateurs + applications`.
- Aucune détention de fonds, aucun service hébergé, aucun agrément, aucune compensation.
- Capacités annoncées par opérateur ; rien n'est émulé.
- Passerelle et simulateur en Kotlin et Spring Boot.
- Devise unique : HTG.
- Spécification en français, qui fait foi ; mots-clés normatifs en français ; champs et
  valeurs en anglais.
- Trois cibles de conformité : client, passerelle, opérateur natif. Un opérateur qui implémente
  OpenFSP nativement est l'objectif.
- La passerelle a un état durable (base de données) : idempotence, conflits, attestations,
  audit, événements et relevés l'exigent.

## Conséquences

- Réponse à l'avertissement du CPMI : la passerelle est déployée par le marchand, le protocole
  est public, et un opérateur natif rend son adaptateur inutile.
- Hors du champ de la loi de 2012 (art. 2, 3 et 7) et de BRH-121 §2, sous réserve de
  l'article 6, qui permet à la BRH d'étendre la loi.
- La spécification versionnée sert de modèle au devoir de documentation de BRH-126 §3 p). La
  suite de conformité fournit un étalon à l'auditeur d'un FSP qui implémente OpenFSP (BRH-121
  §5), sans démontrer à elle seule l'interopérabilité entre FSP.
- Le marchand exploite un service sensible : l'exploitabilité est une exigence de sécurité.
- OpenFSP ne résout pas le paiement d'un opérateur vers un autre : c'est le rôle d'un
  commutateur (PRONAP).

## Alternatives écartées

- **Bibliothèques par langage sans serveur** : `opérateurs × langages` adaptateurs, identifiants
  dispersés, aucun chemin vers un opérateur natif.
- **Spécification sans implémentation de référence** : citée, pas adoptée.
- **Service hébergé multi-locataire** : place le projet sur le chemin des fonds et agrège les
  identifiants.
- **GSMA Mobile Money API telle quelle** : surface disproportionnée.
- **Mojaloop** : autre couche, suppose des participants déjà d'accord pour interopérer.

## Questions ouvertes

- Préférence d'acheminement exprimée par le client quand plusieurs opérateurs sont configurés.
- Modélisation de l'identité du payeur au-delà du numéro de téléphone.
- Adaptateurs dans le dépôt de la passerelle ou en greffons.
- Documentation en créole : question de registre, sans vocabulaire de supervision arrêté.
