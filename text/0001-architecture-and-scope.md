# ADR-0001 : Architecture et périmètre

- Date : 2026-08-16
- Règles : [spec/architecture.md](../spec/architecture.md) (informatif)

## Contexte

Les services de paiement mobile haïtiens n'exposent aucune interface commune aux marchands.
14 % des micro, petites et moyennes entreprises sont bancarisées (`FINSCOPE-2023`, cité par
`BRH-PILOT-2026`). Chaque opérateur a sa propre API, ses statuts, ses erreurs : un marchand qui
accepte deux opérateurs écrit deux intégrations, et l'intégration est réimplémentée dans chaque
langage. Les bacs à sable documentés de MonCash et NatCash n'offrent pas de déclenchement de
défaillance à la demande. Le nombre d'intégrations croît comme `opérateurs × applications`.

La Circulaire 121 « pose le principe mais ne définit ni les standards
techniques, ni les protocoles d'échange » (`EF-AYITI-121`, p. 11). `CPMI-PAFI-2020` (146,
p. 53) établit le même constat et relève qu'une passerelle peut tirer avantage de la
fragmentation qu'elle vise à réduire.

## Décision

Je propose :

- Une spécification ouverte, une passerelle auto-hébergée par le marchand, un serveur simulé
  et des bibliothèques clientes minces. Nombre d'intégrations ramené à
  `opérateurs + applications`.
- Aucune détention de fonds, aucun service hébergé, aucun agrément, aucune compensation.
- Capacités annoncées par opérateur ; rien n'est émulé.
- Passerelle et simulateur en Kotlin et Spring Boot.
- Devise unique : HTG.
- Spécification en français, qui fait foi ; mots-clés normatifs en français ; champs et
  valeurs en anglais.
- Trois cibles de conformité : client, passerelle, opérateur natif. Je vise à terme
  l'opérateur natif.
- La passerelle a un état durable (base de données) : idempotence, conflits, attestations,
  audit, événements et relevés l'exigent.
- Adaptateurs (reprend l'ADR-0013) : un adaptateur traduit sans rien inventer, ni capacité, ni
  terminalité, ni renvoi invérifiable ; chacun publie son profil (capacités, statuts,
  idempotence, rappels, pertes connues).

## Conséquences

- Réponse à l'avertissement du CPMI : la passerelle est déployée par le marchand, le protocole
  est public, et un opérateur natif rend son adaptateur inutile.
- Hors du champ de la loi de 2012 (art. 2, 3 et 7) et de BRH-121 2, sous réserve de
  l'article 6, qui permet à la BRH d'étendre la loi.
- La spécification versionnée sert de modèle au devoir de documentation de BRH-126 3 p). La
  suite de conformité fournit un étalon à l'auditeur d'un FSP qui implémente OpenFSP (BRH-121
  5), sans démontrer à elle seule l'interopérabilité entre FSP.
- La passerelle détient les secrets d'opérateur du marchand qui l'exploite ; je traite la
  facilité d'exploitation comme une exigence de sécurité (binaire unique et sa base de
  données, réglages sûrs par défaut).
- L'adaptateur détient les secrets d'opérateur et traite des entrées qu'un attaquant peut
  influencer.
- Le paiement d'un opérateur vers un autre relève d'un commutateur (PRONAP), hors du champ
  d'OpenFSP.

## Ce que je n'ai pas retenu

- **Bibliothèques par langage sans serveur** : `opérateurs × langages` adaptateurs, identifiants
  dispersés, aucun chemin vers un opérateur natif.
- **Spécification sans implémentation de référence** : rien ne démontre que la
  spécification est implémentable ni qu'elle se comporte comme spécifié.
- **Service hébergé multi-locataire** : place le projet sur le chemin des fonds et agrège les
  identifiants.
- **GSMA Mobile Money API telle quelle** : surface disproportionnée.
- **Mojaloop** : autre couche, suppose des participants déjà d'accord pour interopérer.

## Questions ouvertes

- Préférence d'acheminement exprimée par le client quand plusieurs opérateurs sont configurés.
- Modélisation de l'identité du payeur au-delà du numéro de téléphone.
- Adaptateurs dans le dépôt de la passerelle ou en greffons, et profil d'adaptateur lisible par
  machine.
- Documentation en créole : registre de langue à fixer, en l'absence de terminologie
  réglementaire établie en créole.
