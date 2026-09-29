# ADR-0016 : Revendications de conformité et usage du nom

- Statut : Proposée
- Date : 2026-09-07
- Règles : [spec/marques.md](../spec/marques.md)

## Contexte

Une marque de conformité vaut ce que coûte une fausse déclaration. Trois échecs connus : la
marque accordée par un organisme devient une file d'attente, des frais, puis un commerce ; la
marque sans règle devient un ornement ; la marque au vocabulaire lâche ment par omission. Le
porteur construit des produits commerciaux sur OpenFSP : un processus d'octroi qu'il
s'appliquerait plus aisément qu'aux autres transformerait un intérêt déclaré en avantage.

## Décision

- Aucun programme de certification, aucun frais, aucun octroi.
- Une revendication repose sur un rapport de la suite, publié et reproductible, exécuté par le
  revendiquant.
- Forme fixe : `OpenFSP conformant <cible>, <niveau>, protocol <version>`, avec lien vers le
  rapport. Le mot est « conformant ».
- Interdictions : laisser entendre une certification, omettre la version, présenter la
  conformité comme une garantie de sécurité, généraliser au-delà de la configuration testée,
  utiliser le nom comme nom de produit.
- Seul recours : la publication, après notification.
- Le dépositaire suit exactement les mêmes règles.

## Conséquences

- Aucun octroi, donc rien à refuser à un concurrent ni à s'accorder à soi-même.
- La loi de 2012 (art. 85), qui lie les banques et non le projet, sert d'étalon : écarter le
  conflit d'intérêts quand c'est possible, le neutraliser sinon ; l'absence d'octroi l'écarte, la publication le neutralise.
- Un fork peut revendiquer la conformité s'il réussit la suite.
- Le nom reste détenu par Karako Systems en dépositaire, avec les engagements de GOVERNANCE §8.

## Alternatives écartées

- **Certification par le projet** : le dépositaire accorderait à un concurrent le droit
  d'interopérer ; exige aussi une organisation, alors que le projet repose sur une personne.
- **Certificateur tiers** : la bonne réponse à terme, mais l'organisme n'existe pas ; une ADR
  future pourra en reconnaître un.
- **Aucune règle** : la marque devient décorative.
- **Registre des implémentations conformes tenu par le projet** : réintroduit un gardien.
- **« certified » avec avertissement** : l'avertissement n'est pas lu.
- **Rapport contresigné par une seconde partie** : bloquerait les premiers et plus petits
  implémenteurs.

## Questions ouvertes

- Où publier les rapports sans recréer un registre.
- Une revendication portant sur un seul profil.
- Un délai de grâce quand un correctif ajoute des tests à la suite.
- Une marque visuelle.
- Le §6 de la spécification suffit-il, tant que l'éditeur publie contre son propre employeur.
