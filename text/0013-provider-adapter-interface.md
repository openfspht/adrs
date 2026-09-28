# ADR-0013 : Interface des adaptateurs de fournisseur

- Voie : Informative
- Statut : Brouillon
- Créée : 2026-09-07
- Dépend de : ADR-0001, ADR-0003, ADR-0004, ADR-0005, ADR-0006, ADR-0007, ADR-0009

## Résumé

Un adaptateur est la pièce de la passerelle qui parle le dialecte d'un fournisseur. Cette
ADR décrit la jointure sur laquelle il repose : les opérations qu'on lui demande
d'effectuer, les faits sur lesquels il doit être honnête, les correspondances qu'il doit
rendre totales, et le document qu'il doit publier afin que quiconque le déploie sache ce
qu'il obtient.

Elle est Informational parce qu'elle lie la passerelle et non le protocole. Deux passerelles
de formes internes complètement différentes peuvent toutes deux être conformes, et rien ici
ne change ce qu'un client voit. Ce qui change, en revanche, c'est la possibilité de
raisonner sur un déploiement : une passerelle dont les adaptateurs ne sont pas documentés est
une passerelle dont le comportement en cas de défaillance est inconnu, et
[ADR-0004 §7.5](0004-idempotency-and-retries.md) exige déjà une partie de ce document sans
dire ce que contient le reste.

Les trois règles qui comptent sont au §3, et ce sont toutes des refus. Un adaptateur
n'invente jamais une capacité, n'invente jamais une terminalité, et ne renvoie jamais une
opération qu'il ne peut pas vérifier.

## Motivation

[ADR-0001](0001-architecture-and-scope.md) fonde toute la cause du projet sur une
affirmation arithmétique : le coût d'intégration passe de `P × L` à `P + L`, parce qu'un
adaptateur par fournisseur est écrit une fois au lieu d'une fois par langage. L'affirmation
ne tient que si un adaptateur est une chose petite et bien bornée, que quelqu'un d'autre que
son auteur d'origine peut écrire, relire et croire.

Rien jusqu'ici ne décrit ce qu'est cette chose. Les ADR de la voie Standards disent ce
qu'une passerelle doit faire, ce qui est correct et délibéré, et laissent ouverte toute
question sur son organisation interne, ce qui est également correct. Mais certaines de ces
questions ne sont pas internes. Savoir si un adaptateur renvoie un débit indéterminé n'est
pas un détail d'implémentation : c'est la différence entre un marchand qui débite
occasionnellement deux fois et un marchand qui ne le fait pas, et un déployeur ne peut pas le
voir de l'extérieur.

Les défaillances précises contre lesquelles ce document est écrit sont toutes des
défaillances d'honnêteté plutôt que de code :

Un adaptateur qui projette un statut de fournisseur inconnu sur l'état OpenFSP le plus proche
parce que le laisser sans correspondance semblait négligé. La passerelle rapporte alors
`failed` pour un paiement encore en vol, et l'invariant de terminalité de
[ADR-0003](0003-payment-lifecycle.md) est brisé à la seule couche que personne
n'inspecte.

Un adaptateur qui annonce `payments.lookup` parce qu'il peut retourner le paiement qu'il
détient déjà. [ADR-0007 §5.3](0007-capability-discovery.md) l'interdit dans le protocole ;
c'est interdit ici dans le composant qui le ferait réellement.

Un adaptateur qui rejoue un débit expiré parce que c'est ce qu'on fait des expirations.
[ADR-0004 §7.4](0004-idempotency-and-retries.md) est explicite, et un auteur
d'adaptateur qui ne l'a pas lue réinventera le double débit en une après-midi.

Chacune de ces défaillances est bon marché à prévenir en écrivant ce qu'un adaptateur doit, et
coûteuse à découvrir en production.

## Hors périmètre

- **Aucune forme d'API.** Ce document ne définit pas d'interface dans un langage quelconque.
  Une interface Kotlin, un protocole d'extension et un ensemble de fonctions internes sont
  tous raisonnables, et choisir entre eux est l'affaire de l'implémentation de la passerelle.
- **Aucune exigence normative.** Informational, donc aucun mot-clé RFC 2119, selon
  [le processus ADR](https://github.com/openfspht/adrs/blob/main/README.md#voies).
  Là où une obligation est citée ici, elle appartient à une ADR de la voie Standards et est
  référencée.
- **Aucune correspondance propre à un fournisseur.** Ce que MonCash appelle un paiement en
  attente est documenté dans l'adaptateur MonCash, pas ici.
- **Aucun acheminement.** Choisir vers quel fournisseur un paiement part est hors périmètre
  dans [ADR-0006](0006-gateway-http-api-payments.md) et le reste ici.
- **Aucune décision sur le dedans ou le dehors de l'arbre.**
  [ADR-0001](0001-architecture-and-scope.md) laisse cela ouvert ; le §8 dit ce que la
  réponse change et ne choisit pas.

## 1. Ce qu'est un adaptateur

**1.1.** Un adaptateur est un traducteur sans mémoire de rien. Il reçoit une opération
exprimée en termes OpenFSP, l'exprime dans les termes d'un fournisseur, et retraduit la
réponse. La passerelle possède l'enregistrement de paiement, le magasin d'idempotence, les
transitions d'état et la piste d'audit ; l'adaptateur ne possède rien de tout cela.

**1.2.** Tout ce qu'un adaptateur rapporte est soit quelque chose que le fournisseur a dit,
soit son incapacité honnête à le dire. Il n'y a pas de troisième catégorie, et l'essentiel du
§3 consiste à défendre cette phrase.

**1.3.** Un adaptateur est le seul composant qui détient un identifiant de fournisseur
([ADR-0009 §9](0009-authentication-and-credentials.md)), ce qui en fait le composant qui
mérite le plus d'être relu soigneusement et celui dont la journalisation mérite le plus de
méfiance.

**1.4.** Un adaptateur est une déclaration statique autant qu'il est du code. Son ensemble de
capacités, sa correspondance de statuts et sa stratégie d'idempotence sont des propriétés du
fournisseur qu'il enveloppe, sont connues avant son exécution, et sont ce que le §7 lui
demande de publier.

## 2. Les opérations

On demande à un adaptateur d'effectuer un sous-ensemble de celles-ci. Quel sous-ensemble il
implémente est ce que dit sa déclaration de capacités (§4).

| Opération | Correspond à | Obligatoire |
|---|---|---|
| Créer un paiement | [ADR-0006 §5.1](0006-gateway-http-api-payments.md) | oui |
| Lire un paiement chez le fournisseur | [ADR-0006 §5.3](0006-gateway-http-api-payments.md), `payments.lookup` | non |
| Ingérer un rappel de fournisseur | [ADR-0003 §6.3](0003-payment-lifecycle.md), [§6.6](0003-payment-lifecycle.md) pour `webhooks.per_payment_url` | non |
| Lire un relevé du fournisseur | [ADR-0003 §6.7](0003-payment-lifecycle.md), `payments.statement` | non |
| Résoudre un jeton de payeur | [ADR-0012 §3](0012-proximity-payments-cpm.md), `payments.proximity_cpm` | non |
| Retirer une demande de confirmation | [ADR-0011 §7](0011-confirmation-requests.md), `confirmation_requests.cancel` | non |

**2.1.** La création est la seule opération obligatoire, parce que c'est la seule que chaque
fournisseur offre. C'est le même raisonnement qui rend la capacité de base de
[ADR-0006 §2](0006-gateway-http-api-payments.md) aussi réduite qu'elle l'est.

**2.2.** Relire un paiement depuis le magasin propre à la passerelle n'est pas une opération
d'adaptateur. Cela ne touche jamais le fournisseur, donc aucun adaptateur n'est impliqué, ce
qui est exactement pourquoi
[ADR-0006 §5.2.4](0006-gateway-http-api-payments.md) peut promettre que cela fonctionne
pour chaque fournisseur.

**2.3.** L'ingestion de rappels est listée comme une opération bien qu'elle soit entrante,
parce que c'est un travail d'adaptateur : analyser une forme que seul ce fournisseur produit,
vérifier une signature que seul ce fournisseur utilise, et décider ce qu'on peut, s'il y a
lieu, en conclure.

**2.4.** Un adaptateur qui ne peut pas effectuer une opération ne l'implémente pas et ne la
déclare pas. Il n'y a pas d'implémentation partielle qui retourne une erreur : un client peut
planifier autour d'une absence et ne peut pas planifier autour d'une opération qui n'échoue
que parfois.

## 3. Les trois refus

**3.1. Un adaptateur n'invente jamais une capacité.** Il déclare ce que le fournisseur fait,
non ce que la passerelle pourrait simuler.
[ADR-0007 §1.3](0007-capability-discovery.md) le rend normatif et
[ADR-0007 §5.3](0007-capability-discovery.md) nomme le cas tentant : répondre à une
recherche depuis l'enregistrement propre à la passerelle. L'enregistrement peut être périmé,
de sorte que la réponse serait une fausse affirmation dans le seul endroit où un client a
explicitement demandé une vérité faisant autorité.

La raison pour laquelle cette règle vit chez l'adaptateur est que l'adaptateur est là où se
trouve la tentation. L'auteur de la passerelle qui écrit le point d'accès de recherche n'a
aucun moyen de simuler ; l'auteur de l'adaptateur en a un, et cela prend trois lignes.

**3.2. Un adaptateur n'invente jamais une terminalité.** Un statut de fournisseur qu'il ne
reconnaît pas ne correspond à rien, et le paiement reste `pending`, que [ADR-0003
§1.1](0003-payment-lifecycle.md) définit comme *pas encore connu comme terminal* pour ce cas.
L'instinct d'attraper l'état le plus proche est le mauvais, et le caractère négligé d'un
statut sans correspondance est le signal correct qu'une correspondance manque.

Il en va de même pour `failure_reason` :
[ADR-0003 §7.3](0003-payment-lifecycle.md) interdit de deviner une valeur précise depuis
un code de fournisseur inconnu, et `unspecified` existe pour que la réponse honnête soit
disponible.

**3.3. Un adaptateur ne renvoie jamais ce qu'il ne peut pas vérifier.** Après un dénouement
indéterminé, une expiration ou une connexion perdue en pleine requête, l'adaptateur tente
d'abord d'établir ce qui s'est passé
([ADR-0004 §7.2](0004-idempotency-and-retries.md)). Là où le fournisseur offre une
idempotence ou une recherche, il l'utilise
([ADR-0004 §7.3](0004-idempotency-and-retries.md)). Là où il n'offre ni l'une ni l'autre,
l'opération n'est pas renvoyée, le paiement reste `pending`, et un opérateur est averti
([ADR-0004 §7.4](0004-idempotency-and-retries.md)).

Ce dernier cas ressemble à un abandon, et c'est le comportement correct. Une reprise contre
un fournisseur qui ne sait ni dédupliquer ni être interrogé est un double débit avec des
étapes en plus, selon les termes de l'ADR qui l'exige.

**3.4.** Les trois refus partagent une forme : quand l'adaptateur ne sait pas quelque chose,
la réponse est qu'il ne sait pas, exprimée dans le vocabulaire que le protocole possède déjà
pour ne pas savoir. Le protocole a été conçu avec ce vocabulaire parce que la couche des
adaptateurs allait forcément en avoir besoin.

## 4. Déclaration de capacités

**4.1.** Un adaptateur déclare les noms de capacité qu'il prend en charge, tirés du registre
de [ADR-0007 §2.2](0007-capability-discovery.md), et la passerelle les annonce au titre de
[ADR-0007 §3.2](0007-capability-discovery.md).

**4.2.** La déclaration est statique par fournisseur, non par paiement et non par marchand.
Un fournisseur qui active les remboursements pour certains marchands et pas pour d'autres est
la question ouverte de [ADR-0007](0007-capability-discovery.md), et un adaptateur déclare
aujourd'hui la position générale du fournisseur.

**4.3.** La déclaration porte aussi ce que
[ADR-0007 §3.2](0007-capability-discovery.md) appelle le profil de paiement : quels types
de `next_action` le fournisseur produit, si un identifiant de payeur est requis à la
création, si une URL de retour est requise, et si le fournisseur garantit l'expiration. Ce
sont des faits sur le fournisseur dont un client a besoin avant de construire un tunnel
d'achat, et ils sont connus de l'auteur de l'adaptateur et de personne d'autre.

**4.4.** Un adaptateur qui déclare une capacité qu'il n'a pas est la défaillance que
[ADR-0007 §6.2](0007-capability-discovery.md) teste. Il vaut la peine de dire que le test
ne peut l'attraper que là où le mensonge est observable : un adaptateur qui prétend
`webhooks.verify` et n'effectue aucune vérification passe chaque test fonctionnel et n'échoue
que face à un adversaire. C'est la relecture, non le test, qui attrape celui-là.

## 5. Correspondances

**5.1. La correspondance de statuts est totale, ou elle est documentée comme partielle.**
Chaque statut de fournisseur que l'adaptateur a vu correspond à un état OpenFSP ou à rien, et
les deux sont consignés. Une correspondance avec des trous silencieux est une correspondance
où un statut inattendu produit ce que le cas par défaut du code fait au hasard.

**5.2.** La correspondance est directionnelle. Les statuts de fournisseur se projettent sur
les états OpenFSP, et jamais l'inverse, parce que l'inverse n'est pas une fonction : plusieurs
statuts de fournisseur s'effondrent sur `pending`, et reconstituer lequel n'est pas possible
ni nécessaire.

**5.3.** La correspondance est aussi là où l'ambiguïté d'un fournisseur devient visible.
Plusieurs fournisseurs utilisent un même statut pour « le payeur n'a pas encore agi » et « on
ne sait pas ce qui s'est passé », ce que [ADR-0003](0003-payment-lifecycle.md) anticipe en
faisant couvrir les deux par `pending`. Un adaptateur dont la correspondance a une ligne
comme celle-là a fait son travail ; un adaptateur qui a résolu l'ambiguïté en choisissant ne
l'a pas fait.

**5.4. La correspondance des raisons, pour `failure_reason`, suit les mêmes règles** et a une
tolérance moindre à l'optimisme. [ADR-0003 §7.3](0003-payment-lifecycle.md) interdit de
deviner parce que la réponse automatisée d'un marchand à `insufficient_funds` diffère de sa
réponse à `provider_error`, et qu'une mauvaise supposition produit une mauvaise action
automatisée plutôt qu'une mauvaise étiquette.

**5.5. `failure_detail` porte le code et le message propres du fournisseur sans
altération** ([ADR-0003 §7.4](0003-payment-lifecycle.md)), ce qui est ce qui rend un
statut sans correspondance récupérable : un marchand qui appelle le support du fournisseur
peut citer quelque chose que le fournisseur reconnaît. C'est soumis au devoir de caviardage de
[ADR-0009 §9.5](0009-authentication-and-credentials.md), et l'adaptateur est le composant
qui sait quelles chaînes sont des identifiants.

**5.6. La correspondance des erreurs** vise le catalogue de
[ADR-0005 §9](0005-error-taxonomy.md), et les deux lignes le plus souvent ratées sont
`provider-unavailable` et `provider-timeout`. Elles diffèrent par `effect` : indisponible
signifie que la requête n'est jamais arrivée, donc rien ne s'est passé ; expiration signifie
que la passerelle ne sait pas, donc `effect` vaut `unknown`. Un adaptateur qui rapporte une
expiration comme une indisponibilité a dit à un client que rien ne s'était passé alors que
quelque chose a pu se passer.

## 6. Rappels

**6.1.** Un rappel entrant de fournisseur est un indice, jamais un fait
([ADR-0003 §6.3](0003-payment-lifecycle.md)). Là où le fournisseur signe, la vérification
est obligatoire et un rappel invérifiable est rejeté plutôt que journalisé. Là où il ne signe
pas, le rappel est une invitation à relire l'état faisant autorité.

**6.2.** Un adaptateur pour un fournisseur qui ne signe pas effectue donc son travail le plus
important en ignorant le contenu du rappel. Le rappel dit un identifiant de paiement ;
l'adaptateur relit ce paiement ; la relecture est ce qui change quoi que ce soit. Un corps de
rappel qui arrive signé et un corps qui arrive d'un attaquant sont alors indiscernables dans
leurs effets, ce qui est la propriété achetée.

**6.3.** Là où le fournisseur n'offre pas non plus de recherche, l'adaptateur a une
affirmation non signée et aucun moyen de la corroborer par consultation. Le rappel reste un
indice, et l'adaptateur déclare les sources qui lui restent au titre d'[ADR-0003
§6.5](0003-payment-lifecycle.md) : une URL propre au paiement si le fournisseur en accepte
une, un relevé s'il en fournit un. S'il n'en a aucune, la déclaration correcte est qu'aucune
capacité de finalité n'est prise en charge, et chaque paiement de ce fournisseur attendra une
attestation de l'exploitant, ce qu'[ADR-0007 §5.5](0007-capability-discovery.md) rend visible.

**6.4.** La protection contre le rejeu est exigée que le rappel soit signé ou non
([ADR-0001](0001-architecture-and-scope.md), *Security considerations*). Une relecture
déclenchée par un rappel rejoué est inoffensive mais pas gratuite, et un point d'accès qu'on
peut faire relire au rythme d'un attaquant est une façon d'épuiser une limite de débit chez le
fournisseur.

## 7. Ce qu'un adaptateur publie

Un adaptateur est déployable par quelqu'un qui ne l'a pas écrit, et voici le document qui rend
cela possible. [ADR-0004 §7.5](0004-idempotency-and-retries.md) en exige normativement la
troisième ligne ; le reste est ce qu'un déployeur devra sinon découvrir dans le code source.

| Élément | Pourquoi un déployeur en a besoin |
|---|---|
| Ensemble de capacités et profil de paiement | Ce contre quoi un client peut être écrit ([ADR-0007 §3.2](0007-capability-discovery.md)). |
| Correspondance de statuts, y compris les statuts sans correspondance | Ce que la passerelle fera d'un statut que personne n'a anticipé. |
| Correspondance de `failure_reason` | Quelles réponses marchandes automatisées se déclencheront correctement. |
| Stratégie d'idempotence : [ADR-0004 §7.3](0004-idempotency-and-retries.md) ou [§7.4](0004-idempotency-and-retries.md) | Si un débit indéterminé est résolu automatiquement ou attend une personne. Exigé. |
| Prise en charge des rappels : signés, non signés, ou aucun | Si les changements d'état arrivent promptement ou seulement par sondage. |
| Pertes connues | Champs que le fournisseur ne retourne pas, distinctions qu'il ne fait pas. |
| Identifiants requis, et comment ils sont fournis | [ADR-0009 §9.1](0009-authentication-and-credentials.md). |
| Identifiant du fournisseur | La valeur enregistrée ([`registries/providers.md`](https://github.com/openfspht/openfsp/blob/main/registries/providers.md)). |

**7.1.** La ligne la plus précieuse est *pertes connues*, et c'est celle qui a le plus de
chances d'être omise. Un fournisseur qui ne retourne jamais de `ProviderReference`, ou qui ne
rapporte aucune distinction entre un refus et une erreur, impose une limitation permanente à
chaque marchand qui l'utilise, et la limitation est invisible jusqu'à ce que quelqu'un ait
besoin du champ.

**7.2.** Le document est écrit par adaptateur et non par passerelle, parce que les faits sont
ceux du fournisseur. Une seconde passerelle enveloppant le même fournisseur écrira presque le
même document, ce qui est un argument modéré pour que les adaptateurs vivent quelque part de
partageable (§8).

## 8. Où vivent les adaptateurs

[ADR-0001](0001-architecture-and-scope.md) laisse ouverte la question du dedans ou du
dehors de l'arbre. Ce document ne la tranche pas non plus, et consigne ce que le choix décide
réellement, parce que le cadrage de cette ADR porte sur la disposition des dépôts et que les
conséquences n'y sont pas.

**8.1.** Dans l'arbre signifie que le projet relit chaque adaptateur, ce qui est le seul
mécanisme qui attrape le mensonge infalsifiable du §4.4. Cela signifie aussi que le projet se
porte implicitement garant d'adaptateurs qu'il n'a pas écrits contre des fournisseurs qu'il ne
peut pas tester, ce dont [ADR-0001](0001-architecture-and-scope.md) ne veut explicitement
pas : l'existence d'un adaptateur n'implique rien sur la solidité du fournisseur, et un dépôt
peut saper cette phrase par association.

**8.2.** Hors de l'arbre signifie qu'un fournisseur peut livrer son propre adaptateur sans
demander, ce qui est le chemin d'adoption que le projet veut, et cela signifie que personne ne
relit le §3.

**8.3.** La réponse vraisemblable n'est ni l'une ni l'autre purement : un petit ensemble dans
l'arbre contre lequel la suite de conformité s'exécute, et un point d'extension documenté pour
le reste, avec la marque de conformité
([ADR-0016](0016-conformance-marks-and-naming.md)) plutôt que le dépôt qui se porte garante.
C'est une conjecture, et c'est consigné comme telle.

## 9. Tester un adaptateur

**9.1.** Un adaptateur ne peut pas être testé contre un vrai fournisseur à la demande.
L'accès aux bacs à sable va de l'inscription libre à une démarche auprès de l'opérateur,
et aucun d'eux ne rend une défaillance reproductible, ce qui est la raison que
[ADR-0001](0001-architecture-and-scope.md) donne à l'existence même de la simulation.

**9.2.** Ce qui peut être testé sans fournisseur est tout ce qui est aux §3 et §5 : la
correspondance de statuts est de la donnée, et lui donner chaque valeur que le fournisseur
documente plus une qu'il ne documente pas est un test unitaire. Les refus sont comportementaux
et sont testables contre des réponses de fournisseur enregistrées.

**9.3.** Ce qui ne peut pas être testé ainsi est de savoir si les réponses enregistrées sont
ce que le fournisseur envoie réellement. Un adaptateur n'est honnête qu'autant que la lecture
que son auteur a faite de la documentation d'un fournisseur, et la documentation des
fournisseurs se trompe fréquemment sur les cas de défaillance, qui sont ceux qui comptent ici.

**9.4.** [ADR-0014](0014-mock-server-behaviour.md) spécifie une simulation dont la valeur
dépend de ceci : une simulation qui imite un fournisseur plus poliment que le fournisseur ne
se comporte produit des adaptateurs qui marchent en test et échouent sur un marché.

## Compatibilité

Rien à casser. Ce document décrit une jointure qui existe déjà implicitement dans chaque
passerelle conforme aux ADR de la voie Standards, et n'ajoute aucune exigence à aucune d'elles.

Une passerelle existante se met en conformité avec le §7 en écrivant un document, ce qui est
le seul travail que cette ADR crée.

## Considérations de sécurité

L'adaptateur est là où se trouvent les identifiants de fournisseur
([ADR-0009 §9](0009-authentication-and-credentials.md)), ce qui en fait le code de plus
grande valeur de la passerelle et l'endroit où une commodité de journalisation devient une
divulgation d'identifiant. Le devoir de caviardage du §5.5 échoit ici parce qu'aucun autre
composant ne sait quelles chaînes sont secrètes.

Un adaptateur est aussi le seul composant qui analyse à grande échelle des entrées influencées
par un attaquant : les réponses de fournisseur et les corps de rappel. Une réponse de
fournisseur n'est pas une entrée de confiance du seul fait qu'elle vient d'un fournisseur,
puisqu'un point d'accès de rappel est atteignable par quiconque (§6.1) et que les systèmes
propres d'un fournisseur peuvent être compromis. L'hygiène ordinaire d'analyse s'applique, et
un adaptateur qui fait correspondre un statut de fournisseur par filtrage de motifs sur du
texte libre accepte des instructions de ce texte.

La déclaration infalsifiable du §4.4 mérite d'être répétée comme propriété de sécurité plutôt
que de correction. Un adaptateur qui prétend `webhooks.verify` sans rien vérifier fait faire
confiance à des rappels non vérifiés à chaque client de ce déploiement, et aucun test
fonctionnel ne le détecte. C'est un argument pour relire les adaptateurs qui réclament des
capacités pertinentes pour la sécurité, et c'est l'argument le plus fort du §8 en faveur de la
position dans l'arbre.

## Considérations réglementaires

La section 13.1 de la circulaire 121 de la BRH du 6 décembre 2021 exige que chaque transaction
soit traçable. L'adaptateur est là où une transaction acquiert son identité côté fournisseur,
et l'exigence du §5.5 de porter le code et le message propres du fournisseur mot pour mot est
ce qui rend un enregistrement de passerelle résoluble contre un enregistrement de fournisseur
pendant un audit ou un litige.

La section 15 régit la protection des données en stockage et en transmission, et
[ADR-0009 §9](0009-authentication-and-credentials.md) place les exigences opérantes à cette
couche.

Rien dans ce document ne crée d'obligation pour le projet. Un adaptateur est un logiciel qu'un
marchand déploie sur sa propre infrastructure pour parler à un fournisseur avec lequel il a
déjà une relation, et le publieur de l'adaptateur n'est pas partie à cette relation.

## Alternatives envisagées

**Spécifier normativement une interface d'adaptateur, dans une ADR de la voie Standards.**
Cela rendrait les adaptateurs portables entre passerelles, ce qui semble précieux et ne l'est
pour l'essentiel pas : il y a une passerelle, et une interface interne normative figerait une
décision de conception avant que quiconque n'ait implémenté deux fournisseurs. La position
honnête est que ceci est une recommandation jusqu'à ce qu'il y ait des preuves de ce dont un
adaptateur a réellement besoin.

**La spécifier comme une interface au niveau du langage.** Concret, testable, et cela lierait
la passerelle à un langage. [ADR-0001](0001-architecture-and-scope.md) nomme Kotlin pour la
passerelle, et une spécification qui le suppose barre une seconde implémentation sans gain à ce
stade.

**Ne rien documenter du tout.** Le statu quo, et défendable : les ADR de la voie Standards
interdisent déjà chaque comportement que le §3 interdit, de sorte qu'un auteur d'adaptateur qui
les lit ne se trompera pas. Rejeté parce qu'il les lit dispersées sur quatre documents, et que les trois refus sont exactement les règles qu'un auteur rencontrera sous pression en
regardant une API de fournisseur qui rend chacune d'elles commode.

**Exiger que les adaptateurs soient générés depuis une description de fournisseur.**
Attrayant, et cela échoue sur la même chose que tout le reste ici : la documentation des
fournisseurs n'est pas fiable sur les cas de défaillance, de sorte qu'un adaptateur généré
serait correct sur le chemin heureux et faux exactement là où la correction est coûteuse.

## Questions non résolues

**Dans l'arbre ou hors de l'arbre.** §8, hérité de
[ADR-0001](0001-architecture-and-scope.md), et maintenant avec le raisonnement attaché.

**Si le document d'adaptateur devrait être lisible par machine.** Le tableau du §7 est en prose
aujourd'hui. Une forme structurée permettrait à la suite de conformité de vérifier que les
capacités annoncées d'une passerelle correspondent à la déclaration de son adaptateur, ce qui
est un vrai test d'une vraie défaillance. C'est aussi un schéma à maintenir, et cela peut être
ajouté plus tard sans rien changer d'autre.

**Si un adaptateur devrait pouvoir refuser un paiement avant d'appeler le fournisseur.** Un
fournisseur avec un montant minimum documenté pourrait être vérifié localement, épargnant un
aller-retour et donnant une meilleure erreur. Cela met aussi la politique du fournisseur dans
la passerelle, où elle se périme silencieusement, et une règle locale périmée rejette des
paiements valides que le fournisseur aurait acceptés.

**Comment un adaptateur rapporte qu'un fournisseur a changé.** Un fournisseur qui ajoute un
statut, ou qui commence à retourner un champ qu'il ne retournait jamais, est le cas normal sur
plusieurs années. Aujourd'hui la réponse est que la correspondance de l'adaptateur a un trou et
que les paiements restent `pending`, ce qui est sûr et peu informatif. Savoir si mieux est
possible sans inventer de terminalité est une question ouverte.

## Références

Citations complètes dans [`references.md`](references.md). Cette ADR est Informational,
donc chaque référence est informative.

`BRH-126` section 2 pour la règle selon laquelle, là où un tiers traite des données pour le
compte d'une institution, le contrôle reste à l'institution, qui est le cadre dans lequel le §8
se placerait ; et `BRH-126` sections 3 f) et 3 p) pour le contrôle d'accès et la documentation.
`BRH-121` section 13.1 pour la traçabilité que sert le relais mot pour mot du §5.5. Les codes
de motif `ISO20022` apparaissent dans
[ADR-0010 §6](0010-iso-20022-semantic-correspondence.md), qui est où un auteur d'adaptateur
devrait regarder avant d'inventer une correspondance.

## Implémentation de référence

Aucune pour l'instant.

## Errata

Aucun.
