# ADR-0000 : Le titre de cette ADR

- Voie : Standards | Informative | Processus
- Statut : Brouillon
- Créée : AAAA-MM-JJ
- Dépend de : ADR-NNNN

## Résumé

Un paragraphe. Ce qui change, et ce qu'un implémenteur doit faire différemment. On doit
pouvoir lire ceci seul et savoir si la suite le concerne.

## Motivation

Le problème, énoncé avant toute solution. Ce qui casse aujourd'hui, pour qui, et ce que
cela leur coûte. Prenez une situation concrète plutôt qu'une abstraction : « un marchand
qui rapproche les paiements de la journée ne peut pas distinguer une expiration d'un
refus » vaut mieux que « le traitement des erreurs est incohérent ».

Si cette ADR est motivée par un besoin commercial du dépositaire du projet, dites-le ici.
Voir [GOVERNANCE.md §2](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#2-intérêt-déclaré).

## Hors périmètre

Ce que cette ADR ne traite délibérément pas, pour que l'examen n'y dérive pas et que le
lecteur suivant sache que l'omission est une décision et non un oubli.

## Spécification

*(Voie Standards uniquement. Une ADR informative ou de processus remplace cette section
par la structure qui lui convient.)*

Le contenu normatif. Les mots-clés d'exigence MUST, MUST NOT, SHOULD, SHOULD NOT et MAY
sont à interpréter comme décrit dans les RFC 2119 et RFC 8174, et n'apparaissent en
capitales que lorsqu'ils sont employés normativement.

Soyez exact sur le format transmis : noms de champs, types, unités, caractère
optionnel, et ce que fait une implémentation quand un champ est absent, nul ou non
reconnu. Donnez au moins un exemple complet de requête et de réponse, et au moins un
exemple d'échec : c'est là que l'interopérabilité casse réellement.

## Compatibilité

S'il s'agit d'une rupture de compatibilité, et contre quelle version. Ce que les
implémentations existantes doivent faire, si un délai de dépréciation s'applique, et
comment un client détecte la prise en charge à l'exécution. Si rien ne casse, dites-le
explicitement : un relecteur ne devrait pas avoir à le déduire.

## Considérations de sécurité

Obligatoire, et jamais « aucune ». Ce qu'un attaquant gagne si ceci est mal implémenté,
ce qui doit être validé, ce qui ne doit jamais être journalisé, et ce qui est supposé du
transport et du déploiement. Si vous pensez sincèrement qu'il n'y a aucun impact,
argumentez-le : dans une infrastructure de paiement, cette affirmation demande à être
démontrée.

## Considérations réglementaires

Tout ce qui touche à la tenue de registres, à la traçabilité, à l'auditabilité, à la
localisation des données ou au traitement des données personnelles. N'omettez la section
que lorsqu'il n'y a véritablement rien.

## Alternatives envisagées

Chaque alternative réaliste, et pourquoi elle n'a pas été retenue. Ce n'est pas une
formalité : c'est ce qui empêche la même proposition de revenir chaque année, et c'est ce
qu'un lecteur voudra le plus dans cinq ans.

## Questions non résolues

Ce qui est délibérément laissé ouvert, et ce qui permettrait de le trancher. Une liste
honnête ici vaut mieux qu'une apparence de complétude.

## Références

Les clés de [`references.md`](text/references.md), qui porte la citation complète de
chacune. Une ADR de la voie Standards sépare les deux listes ; une ADR informative ou de
processus n'a que la seconde, puisqu'elle n'impose rien.

**Normatives.** Ce qu'un implémenteur doit lire pour implémenter ceci correctement.

**Informatives.** D'où vient une affirmation, et pourquoi une décision a été prise.

Ne citez une source que si elle a été lue, et représentez-la fidèlement, y compris là où
elle joue contre la proposition. Une citation qui reprend la moitié favorable d'une source
et omet le reste est un défaut.

## Implémentation de référence

Un lien, ou « aucune pour l'instant ». Une ADR de la voie Standards peut être acceptée
sans, mais n'atteint pas le statut `Implémentée` tant qu'une implémentation ne passe pas
la suite de conformité.

## Errata

Les corrections appliquées après acceptation qui ne changent pas le sens. Datées. Vide
jusqu'à ce qu'il y en ait.
