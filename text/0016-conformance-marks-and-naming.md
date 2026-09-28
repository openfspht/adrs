# ADR-0016 : Marques de conformité et usage du nom

- Voie : Processus
- Statut : Brouillon
- Créée : 2026-09-07
- Dépend de : ADR-0015

## Résumé

[GOVERNANCE.md §8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité)
détient le nom OpenFSP et toute marque de conformité, et dit délibérément que les règles
d'usage ne sont pas encore définies, parce qu'elles ne pouvaient pas l'être honnêtement avant
qu'une suite de conformité n'existe. La suite est désormais spécifiée dans
[ADR-0015](0015-conformance-levels-and-suite.md), et cette ADR tranche les règles.

Elle est courte par conception. Il n'y a pas de programme de certification, pas de frais, pas
de candidature, et aucun organisme qui accorde quoi que ce soit. Une implémentation qui publie
un rapport de réussite reproductible peut énoncer exactement ce que ce rapport dit, sous une
forme fixe (§3), et ne peut pas en énoncer davantage (§4). Le rôle du projet est de publier la
suite et, là où une revendication publiée est fausse, de le dire.

La disposition qui a demandé le plus de réflexion est le §6. Le dépositaire construit des
produits commerciaux sur OpenFSP, ce que
[GOVERNANCE.md §2](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#2-intérêt-déclaré)
déclare, et un processus de marques que le dépositaire pourrait s'appliquer à lui-même plus
facilement qu'à autrui convertirait un intérêt déclaré en avantage opérationnel. Le §6 soumet
les revendications propres au dépositaire à la même publication que celles de tout le monde et
ne donne au dépositaire aucun pouvoir d'accorder ou de retenir.

## Motivation

Une marque de conformité vaut exactement la difficulté qu'il y a à faire une fausse
revendication, et les façons de se tromper sont bien documentées par l'expérience d'autrui.

Une marque accordée par un organisme devient une file d'attente, des frais, et finalement un
commerce. Le projet vendrait alors la permission d'interopérer avec une spécification sur
laquelle il est aussi en concurrence, ce que
[GOVERNANCE.md §2](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#2-intérêt-déclaré)
existe pour empêcher et à quoi aucune quantité de bonnes intentions ne survit.

Une marque sans aucune règle devient une décoration. Chaque fournisseur la revendique,
personne ne vérifie, et un marchand qui lit « conforme OpenFSP » n'apprend rien. C'est l'état
actuel de l'expression « conforme ISO 20022 », dont
[ADR-0010](0010-iso-20022-semantic-correspondence.md) ouvre en observant que c'est une
revendication faite constamment et vérifiée presque jamais.

Une marque dont la formulation est lâche devient un mensonge par omission. « Certifié OpenFSP »
laisse entendre que quelqu'un a certifié. « Pleinement conforme » laisse entendre une portée
que la suite n'a pas ([ADR-0015 §6.3](0015-conformance-levels-and-suite.md)). « Sûr et
conforme » emprunte une assurance que la suite décline explicitement
([ADR-0015 §5.6](0015-conformance-levels-and-suite.md)). Chacune de ces phrases sera écrite
de bonne foi par quelqu'un tant que les formes permises ne sont pas écrites.

La voie entre ces échecs est étroite et elle existe : faire de la revendication la reprise
d'un fait reproductible, fixer sa forme pour qu'elle ne puisse pas déborder, et laisser
quiconque la vérifier en réexécutant la suite. Cela ne fonctionne que parce que
[ADR-0015 §7.5](0015-conformance-levels-and-suite.md) a rendu les rapports reproductibles,
ce qui est pourquoi cette ADR ne pouvait pas être écrite en premier.

## Hors périmètre

- **Aucun programme de certification.** Le projet n'accorde rien, ne relit rien, et ne facture
  rien.
- **Aucune nouvelle exigence technique.** Ce qui doit être passé est entièrement la question
  de [ADR-0015](0015-conformance-levels-and-suite.md). Cette ADR n'ajoute jamais un
  comportement.
- **Aucun droit des marques.** Le nom est détenu par le dépositaire au titre de
  [GOVERNANCE.md §8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité).
  Cette ADR énonce la politique du projet pour l'utiliser ; elle ne reformule pas le droit et
  ne lie aucune juridiction.
- **Aucun programme de logo.** Le §3 régit des mots. Une marque visuelle pourra suivre, et
  elle suivrait ces règles plutôt que de les remplacer.
- **Aucune recommandation d'une implémentation.** Une revendication de conformité est une
  affirmation sur un résultat de test. Ce n'est pas une recommandation, et le projet n'en fait
  aucune.

## 1. Ce que cette ADR lie

**1.1.** C'est une ADR de la voie Process. Elle lie le projet et quiconque utilise le nom
OpenFSP. Elle n'impose aucune exigence sur le comportement d'une implémentation, et une
implémentation qui ne mentionne jamais OpenFSP n'en est pas affectée du tout.

**1.2.** Rien ici ne restreint la description factuelle. Dire « construit sur OpenFSP »,
« implémente OpenFSP 0.1.0 », ou « parle le protocole OpenFSP » décrit ce que le logiciel fait
et n'exige aucune permission, ce que
[GOVERNANCE.md §8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité)
disait déjà d'utiliser en attendant. Ces formes restent disponibles et ne sont pas des
revendications de conformité.

**1.3.** Ce que cette ADR régit est l'acte plus étroit de revendiquer la **conformité**, qui
affirme un résultat de test et doit donc être vrai d'une façon dont une description n'a pas
besoin.

## 2. Le fondement d'une revendication

**2.1.** Une revendication de conformité repose sur une seule chose : un rapport de réussite
de la suite de conformité, tel que spécifié en
[ADR-0015 §7](0015-conformance-levels-and-suite.md).

**2.2.** Le rapport doit être **publié**, avec la configuration nécessaire pour le reproduire
([ADR-0015 §7.5](0015-conformance-levels-and-suite.md)). Une revendication dont le rapport est
privé n'est pas recevable au titre de cette ADR, et le projet la traite comme non soutenue.

**2.3.** Le revendiquant exécute la suite lui-même. Il n'y a pas de soumission, pas de file
d'attente et pas d'approbation, et c'est la conception plutôt qu'une lacune : le rapport est
reproductible, de sorte que la vérification dont quiconque a besoin est de l'exécuter à
nouveau.

**2.4.** Le rapport doit être à jour pour la version revendiquée
([ADR-0015 §6.4](0015-conformance-levels-and-suite.md)). Une revendication citant un
rapport obtenu contre une version antérieure de l'implémentation est périmée, et republier la
revendication sans réexécuter la suite est une fausse revendication plutôt qu'une revendication
dépassée.

**2.5.** Il n'y a pas de palier probatoire, provisoire, ou autodéclaré. Soit un rapport de
réussite publié et reproductible existe, soit aucune conformité ne peut être revendiquée.

## 3. Formes permises

**3.1.** Une revendication de conformité énonce le triplet de
[ADR-0015 §1.1](0015-conformance-levels-and-suite.md) : cible, niveau, version de
protocole. La forme permise est :

```
OpenFSP conformant <target>, <level>, protocol <version>
```

suivie facultativement des profils passés :

```
OpenFSP conformant gateway, Core, protocol 0.1.0
OpenFSP conformant gateway, Core, protocol 0.1.0, profiles: payments.lookup, webhooks.emit
OpenFSP conformant client, Core, protocol 0.1.0
```

**3.2.** Partout où la revendication apparaît, le rapport doit être atteignable depuis elle.
Dans un document, une citation ; sur une page web, un lien ; dans une phrase marketing, au
minimum un énoncé de l'endroit où le rapport est publié.

**3.3.** Le mot est **conformant**. Ni certified, ni approved, ni validated, ni endorsed, ni
accredited, ni compliant. Les cinq premiers laissent entendre un acte par quelqu'un d'autre, et
aucun tel acte n'a lieu. Le sixième est le mot que cet écosystème a déjà usé.

**3.4.** Une revendication peut être abrégée dans un espace contraint, pourvu que rien en elle
ne soit inexact et que la forme complète soit atteignable.
« OpenFSP conformant (Core, 0.1.0) » est acceptable ; « OpenFSP conformant » seul ne l'est pas,
parce qu'il omet la portée qui le rend vérifiable.

## 4. Ce qui ne peut pas être revendiqué

**4.1.** Aucune revendication ne peut énoncer ni laisser entendre que le projet, le
dépositaire, ou une autre partie a certifié, approuvé, audité, testé ou recommandé
l'implémentation. Personne ne l'a fait.

**4.2.** Aucune revendication ne peut omettre la version du protocole, sans laquelle
[ADR-0015 §1.2](0015-conformance-levels-and-suite.md) la rend dénuée de sens.

**4.3.** Aucune revendication ne peut affirmer un profil que l'implémentation n'a pas passé,
ni une capacité qu'elle n'annonce pas
([ADR-0015 §3.3](0015-conformance-levels-and-suite.md)).

**4.4.** Aucune revendication ne peut présenter la conformité comme une assurance de sécurité.
La suite le décline explicitement
([ADR-0015 §5.6](0015-conformance-levels-and-suite.md)) et exige que chaque rapport porte
l'avertissement ([ADR-0015 §7.4](0015-conformance-levels-and-suite.md)). « Conforme
OpenFSP, donc sûr » est faux, et placer les deux mots ensemble d'une façon qui le suggère
l'est aussi.

**4.5.** Aucune revendication ne peut généraliser au-delà de la configuration testée
([ADR-0015 §6.3](0015-conformance-levels-and-suite.md)). Une passerelle testée contre la
simulation n'est pas pour autant éprouvée contre un vrai fournisseur, et le dire est le
débordement dont un fournisseur de solution est le plus tenté.

**4.6.** Aucune revendication ne peut utiliser le nom OpenFSP comme partie d'un nom de
produit, d'un nom d'entreprise, ou d'un domaine d'une façon suggérant que le produit est celui
du projet. « OpenFSP Gateway Pro » se lit comme un produit officiel ; « Acme Gateway, OpenFSP
conformant » non.

**4.7.** Un fournisseur dont un adaptateur existe dans une passerelle ne peut pas revendiquer
la conformité sur cette base. L'existence d'un adaptateur n'implique rien sur le fournisseur
([ADR-0001](0001-architecture-and-scope.md)), et la conformité fournisseur natif est une
cible avec ses propres tests
([ADR-0015 §2.4](0015-conformance-levels-and-suite.md)).

## 5. Quand une revendication est fausse

**5.1.** Le seul instrument d'application du projet est la publication. Là où une revendication
est fausse, l'Éditeur peut le dire publiquement, dans le dépôt de la spécification, avec le
raisonnement et les preuves.

**5.2.** Avant de le faire, l'Éditeur notifie le revendiquant et laisse un délai raisonnable
pour corriger ou retirer. La plupart des fausses revendications sont des erreurs : une version
qui a bougé, un profil mal retenu, une phrase écrite par quelqu'un qui n'a jamais lu cette ADR.

**5.3.** Là où une revendication est corrigée, rien n'est publié. Le but est l'exactitude, non
un relevé de qui s'est trompé.

**5.4.** Les recours de droit des marques sont ceux du dépositaire, détenus au titre de
[GOVERNANCE.md §8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité),
et cette ADR ne les accorde ni ne les limite. Elle énonce la politique du projet : la
publication d'abord, et les instruments juridiques seulement là où la publication a échoué et
où la fausse revendication cause un préjudice.

**5.5.** Il n'y a pas de révocation, parce qu'il n'y a pas d'octroi. Une revendication cesse
d'être vraie quand son rapport cesse d'être reproductible, et c'est un fait sur la revendication
plutôt qu'une décision de quelqu'un.

## 6. Les revendications propres au dépositaire

**6.1.**
[GOVERNANCE.md §2](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#2-intérêt-déclaré)
déclare que le dépositaire construit des produits commerciaux sur OpenFSP et que quiconque
évalue la spécification devrait supposer un intérêt commercial en elle. Un processus de marques
de conformité est là où cet intérêt pourrait le plus facilement devenir un avantage, et cette
section est ce qui l'empêche.

**6.2.** Les implémentations du dépositaire revendiquent la conformité au titre des §2 et §3
exactement comme quiconque : un rapport publié, reproductible par quiconque, sous la forme
permise. Il n'y a pas de voie alternative, pas d'accès anticipé, et pas d'autoattestation.

**6.3.** Les rapports du dépositaire sont publiés au même endroit et dans le même format que
tout autre, et sont soumis au même §5. Une fausse revendication du dépositaire reçoit une
réponse publique de l'Éditeur, de la même façon, et le fait que l'Éditeur soit le dépositaire
impose que le mécanisme soit la publication plutôt que la discrétion.

**6.4.** Le dépositaire ne peut pas accorder la marque, parce que personne ne le peut. Le §2.3
est ce qui fait fonctionner le §6 : là où il n'y a pas d'octroi, il n'y a rien à retenir d'un
concurrent, et rien à s'accorder à soi-même.

**6.5.** Là où le produit du dépositaire bénéficierait d'un changement à cette ADR, ce
changement passe par le processus ordinaire au titre de
[GOVERNANCE.md §2](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#2-intérêt-déclaré),
avec sa motivation déclarée. Une proposition d'assouplir le §3 ou le §4 d'une façon qui
convient à une phrase marketing est exactement le genre de disposition que les relecteurs sont
en droit de contester.

**6.6.** Cette section est écrite pour être citée par quelqu'un de sceptique sur l'arrangement.
Si elle cesse un jour d'être vraie, l'écart devrait être facile à montrer du doigt.

## 7. Rapport à la licence

**7.1.** La licence Apache-2.0 couvre le logiciel et le texte et n'accorde aucun droit de
marque, ce que
[GOVERNANCE.md §8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité)
énonce déjà. Forker la spécification, la passerelle ou la suite est permis par la licence ;
décrire le résultat comme OpenFSP conformant est régi par cette ADR.

**7.2.** Un fork qui change le comportement du protocole et garde le nom est le cas que cette
règle vise. Un tel fork peut dire ce qu'il est, honnêtement et sans permission, et ne peut pas
revendiquer la conformité à moins de passer la suite pour la version qu'il nomme. C'est toute
la protection qu'offre le nom, et c'est suffisant : c'est la suite qui décide, non une opinion
sur qui a forké qui.

**7.3.** Rien ici n'empêche quiconque d'exécuter la suite contre quoi que ce soit, de publier
le résultat, ou de dire ce qu'il a trouvé. Publier un rapport montrant que l'implémentation de
quelqu'un d'autre échoue est permis et utile.

## 8. Amender cette ADR

**8.1.** Cette ADR est amendée par une ADR Process qui la remplace, au titre du processus
ordinaire. Les formes permises du §3 et les interdictions du §4 sont les parties les plus
susceptibles d'avoir besoin d'ajustement une fois que quelqu'un aura essayé de les faire entrer
dans un vrai texte de produit.

**8.2.**
[GOVERNANCE.md §8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité)
a été mis à jour pour pointer vers cette ADR et la résumer, remplaçant la phrase disant que les
règles n'étaient pas encore définies. Il conserve l'instruction intérimaire, selon laquelle
tant que cette ADR n'est pas acceptée ce sont les descriptions factuelles du §1.2 qu'il faut
utiliser, de sorte que le résumé ne devienne pas une permission en avance sur le processus.
C'était un erratum contre GOVERNANCE.md plutôt qu'un changement de celui-ci.

## Compatibilité

Rien à casser. Aucun comportement d'implémentation ne change, et aucune revendication existante
n'est invalidée par cette ADR, parce que tant qu'elle n'est pas acceptée aucune revendication
de conformité n'était permise du tout
([GOVERNANCE.md §8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité)).

Les descriptions factuelles que cette ADR-là disait d'utiliser en attendant, « construit sur
OpenFSP » et « implémente OpenFSP `<version>` », restent permises et inchangées (§1.2).

## Considérations de sécurité

La défaillance que cette ADR existe pour prévenir est qu'un marchand choisisse une
implémentation sur la foi d'une revendication qui n'est pas vraie. C'est un enjeu de sécurité,
parce que l'implémentation en question traite des paiements et détient des identifiants de
fournisseur, et que le fondement de la confiance du marchand était une phrase que personne n'a
vérifiée.

Le mécanisme est la reproductibilité plutôt que l'autorité. Une revendication qui cite un
rapport publié et reproductible peut être vérifiée par quiconque se soucie assez d'exécuter la
suite, ce qui est une garantie plus faible qu'un audit et bien plus forte qu'une assertion.
L'exigence du §2.2 de publier la configuration est ce qui rend la vérification possible ; sans
elle, le rapport est une assertion avec un nom de fichier.

Le §4.4 mérite d'être nommé ici plutôt que seulement dans la liste. Une revendication de
conformité qui emprunte l'apparence d'une assurance de sécurité est le mésusage le plus
dommageable disponible, parce que [ADR-0015 §5.6](0015-conformance-levels-and-suite.md) est
explicite que les déclarations de capacité les plus pertinentes pour la sécurité sont celles
que la suite ne peut pas vérifier. Un marchand qui lit « conformant » comme « audité » a
inversé le sens de la seule section qui s'est le plus efforcée d'être honnête.

## Considérations réglementaires

La section 5 de la circulaire 121 de la BRH du 6 décembre 2021 exige que la conformité aux
exigences techniques, l'interopérabilité parmi elles, soit attestée par un audit externe au
moins tous les trois ans. Cette ADR ne positionne délibérément pas une revendication de
conformité comme une telle attestation, et un auditeur ne devrait pas en accepter une en
substitut de son propre travail. Ce qu'un rapport offre à un auditeur est un artefact
reproductible qu'il peut réexécuter
([ADR-0015](0015-conformance-levels-and-suite.md), *Considérations réglementaires*), ce qui
est une preuve qu'il peut vérifier plutôt qu'une conclusion qu'il doit accepter.

La distinction compte le plus là où une revendication est la plus forte. Un fournisseur de
solution qui dit à une institution supervisée qu'elle est « conforme OpenFSP, donc auditée » a
déformé à la fois cette ADR et la circulaire, et les §4.1 et §4.4 existent pour que la
déformation soit un manquement à une règle écrite plutôt qu'une affaire d'interprétation.

Si un régulateur devait un jour s'appuyer sur OpenFSP,
[GOVERNANCE.md §2](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#2-intérêt-déclaré)
dit que les contraintes sur l'intérêt du dépositaire deviennent le fondement sur lequel cet
appui est justifié. Le §6 est la forme propre aux marques de ces contraintes, et il est écrit
pour être lu sous cet éclairage.

**La règle haïtienne sur les conflits d'intérêts a la forme qu'a déjà le §6.** L'article 85 de
`HT-LAW-2012` oblige les banques, au titre des règles de conduite, à agir « loyalement et
équitablement au mieux des intérêts de leurs clients et de l'intégrité du marché », et à
« s'efforcer d'écarter les conflits d'intérêt et, lorsque ces derniers ne peuvent être évités,
à veiller à ce que leurs clients soient traités équitablement » [HT-LAW-2012, p. 30]. La règle
impose d'écarter le conflit là où il peut l'être et de le neutraliser là où il ne peut pas. Le
§6 écarte la part qui peut l'être, en s'assurant qu'il n'y a rien à accorder, et neutralise le
reste par la publication. Le projet n'est pas une banque et l'article 85 ne le lie pas. Il est
cité parce qu'un lecteur haïtien mesurera cet arrangement à l'aune du standard que son propre
droit fixe aux institutions réglementées, et il vaut la peine de savoir que l'arrangement
l'atteint.

## Alternatives envisagées

**Un programme de certification exploité par le projet.** Rejeté dans
[ADR-0015](0015-conformance-levels-and-suite.md) du côté technique et ici du côté de la
gouvernance. Cela mettrait le dépositaire en position d'accorder à un concurrent la permission
d'interopérer avec une spécification contre laquelle le dépositaire vend aussi, ce à quoi
aucune déclaration d'intérêt ne survit. Cela exige aussi une organisation avec du personnel, et
le projet est le travail d'une seule personne.

**Un certificateur tiers.** La bonne réponse à terme, et elle a besoin d'un organisme qui
n'existe pas. Rien ici ne l'exclut : une future ADR Process pourrait en reconnaître un, et le
mécanisme de publication du §5 continuerait de fonctionner à côté.

**Aucune règle, et s'en remettre à la bonne foi.** Le moins cher, et cela produit la marque
décorative décrite dans la *Motivation*. L'expression devient dénuée de sens en quelques
fournisseurs, et le marchand que tout cela devait protéger en revient à lire du texte marketing.

**Un registre des implémentations conformes, tenu par le projet.** Attrayant, et cela
réintroduit un gardien par la porte de derrière : quiconque décide de ce qui figure sur la
liste accorde quelque chose, et le dépositaire déciderait s'il inscrit un concurrent. Un
rapport publié que quiconque peut trouver est la même information sans le goulot
d'étranglement.

**Permettre le mot « certified » avec un avertissement.** Les fournisseurs de solution le
demandent, l'avertissement n'est lu par personne, et c'est le mot qui fait le travail. Le §3.3
est court pour cette raison.

**Exiger qu'un rapport soit contresigné par une seconde partie.** Cela élèverait
considérablement le coût d'une fausse revendication. Cela exigerait aussi de trouver une
seconde partie, ce qui pour une première implémentation sur un petit marché signifie trouver un
concurrent prêt à aider, et la barrière tomberait le plus durement sur exactement les petits
implémenteurs dont l'adoption dépend.

## Questions non résolues

**Où les rapports sont publiés.** Le §2.2 exige la publication et ne nomme aucun emplacement.
Un index hébergé par le projet serait commode et est le registre rejeté ci-dessus ; exiger de
chaque revendiquant qu'il héberge le sien est décentralisé et rend les rapports difficiles à
trouver. La distinction entre un index qui liste ce qui existe et un registre qui décide ce qui
est admis est réelle et mince, et s'y tromper recrée le gardien.

**Si une revendication portant seulement sur un profil devrait être permise.** Le §3.1 exige le
niveau, et une implémentation qui passe Core plus un profil doit le dire. Un fournisseur dont
l'intérêt est une capacité unique voudra ne nommer que celle-là, et savoir si c'est une
abréviation raisonnable au titre du §3.4 ou une omission au titre du §4.2 n'est actuellement
pas décidé.

**Ce qu'il advient d'une revendication quand la suite gagne des tests par un correctif.**
[ADR-0015 §6.5](0015-conformance-levels-and-suite.md) permet à un correctif d'ajouter des
tests, de sorte qu'une implémentation peut échouer à une suite qu'elle passait auparavant sans
avoir changé. Au titre du §2.4 la revendication devient périmée, ce qui est correct et abrupt,
et il y a peut-être matière à un délai de grâce.

**Si une marque visuelle vaut la peine d'être faite.** *Hors périmètre* la diffère. Un logo est
plus facile à mésuser qu'une phrase et plus facile à reconnaître, et l'équilibre n'est pas
évident avant que quiconque n'utilise les mots.

**Si le §6 est suffisant.** Il est écrit pour être vérifiable et il repose sur le fait que
l'Éditeur publie contre son propre employeur.
[GOVERNANCE.md §7](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#7-ouverture-de-la-gouvernance)
envisage d'ouvrir la gouvernance, et c'est un des endroits où le faire compterait le plus.

## Références

Citations complètes dans [`references.md`](references.md). Cette ADR est de la voie
Process, donc chaque référence est informative.

`HT-LAW-2012` article 85 pour le standard de conduite discuté ci-dessus. `BRH-121` section 5
pour l'audit triennal pour lequel une revendication au titre de cette ADR ne doit pas être
prise. `GSMA-MMAPI`, dont le service de conformité est le modèle de certification que les
*Alternatives envisagées* déclinent.
[ADR-0015](0015-conformance-levels-and-suite.md) fournit le rapport sur lequel repose
chaque revendication.

## Implémentation de référence

Sans objet. Cette ADR régit des mots.

## Errata

Aucun.
