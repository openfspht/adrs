# ADR-0015 : Niveaux et suite de conformité

- Voie : Standards
- Statut : Brouillon
- Créée : 2026-09-07
- Dépend de : ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006, ADR-0007, ADR-0008, ADR-0009, ADR-0011, ADR-0012, ADR-0014

## Résumé

Cette ADR définit ce que signifie se conformer à OpenFSP, et spécifie la suite exécutable
qui en décide.

La conformité s'énonce comme un triplet : une **cible** (§2), un **niveau** (§3), et une
**version de protocole**. « Cette passerelle est conforme » ne dit ni à quoi ni à quel niveau,
et cette ADR ne la reconnaît pas. « Cette passerelle passe Core au protocole 0.1.0, avec les
profils `payments.lookup` et `webhooks.emit` » en est une, parce que chacune de ses parties
est vérifiable.

Les tests les plus importants de la suite sont les tests négatifs (§5.4). Une passerelle
gagne un profil de capacité en l'implémentant ; elle gagne Core en partie en **refusant,
correctement et visiblement, de faire ce qu'elle ne peut pas faire**. Une implémentation qui
émule une capacité manquante échoue à Core, ce qui est le seul mécanisme qui rend la promesse
centrale de [ADR-0001](0001-architecture-and-scope.md#principes-de-conception) applicable plutôt
qu'aspirationnelle.

Les résultats sont un rapport lisible par machine (§7) que quiconque peut régénérer. La suite
produit des preuves, non une permission : qui peut utiliser le nom OpenFSP sur la foi d'un tel
rapport est la question de [ADR-0016](0016-conformance-marks-and-naming.md) et non de
celle-ci.

## Motivation

Chaque ADR jusqu'ici s'est terminée par une section sur ce qu'une suite de conformité
testerait, et aucune ne pouvait dire ce qu'est la conformité.
[ADR-0007 §6.2](0007-capability-discovery.md) dit qu'une fausse déclaration de capacité
est ce que la suite attrape. [ADR-0009 §11.2](0009-authentication-and-credentials.md)
nomme deux tests précis. [ADR-0011 §9.4](0011-confirmation-requests.md) et
[ADR-0012 §8.5](0012-proximity-payments-cpm.md) énumèrent chacune des cas. Ce sont des
engagements envers un document qui n'existe pas, et le voici.

Tout l'argument d'OpenFSP repose sur une promesse comportementale qui ne peut pas être
inspectée. La promesse est qu'une opération qu'un fournisseur ne peut pas effectuer est
**absente et découvrable comme absente, jamais émulée**. Un client s'y fie pour décider s'il
construit un flux de remboursement. Un superviseur s'y fierait pour comparer deux
institutions. Et elle est invisible : une passerelle qui répond à une recherche depuis son
propre enregistrement périmé ressemble exactement à une passerelle qui a interrogé le
fournisseur, jusqu'au moment où un marchand expédie des marchandises contre un paiement qui
avait déjà échoué.

Rien d'autre qu'un test ne détecte cela. La documentation ne le fait pas, parce que la
documentation de la passerelle est écrite par qui a écrit la passerelle. La relecture de code
ne le fait pas, à l'échelle d'un marché comptant plusieurs déploiements. Une suite exécutable
qui demande à une passerelle de faire quelque chose qu'elle devrait refuser, et la fait
échouer si elle obtempère, est le seul mécanisme disponible.

Il y a une seconde motivation, qui est celle dont une institution se souciera en premier, et
ce sont deux audits plutôt qu'un. La section 5 de `BRH-121` exige que l'interopérabilité soit
attestée par un audit externe au moins tous les trois ans et ne prescrit aucune norme selon
laquelle elle est jugée. La section 3 t) de `BRH-126` exige séparément un audit de la sécurité
du système d'information à la même cadence triennale, et ne prescrit aucune norme non plus. Ce
second audit a des dents que le premier n'a pas : ne pas le réaliser expose l'institution à une
pénalité de 200 000 gourdes, puis 100 000 gourdes par jour d'infraction à compter de la
notification [BRH-126, p. 4]. Un auditeur confronté à cela aujourd'hui doit inventer une
méthode. Une suite qui s'exécute, produit un rapport daté, et nomme exactement quels
comportements ont été exercés est une réponse à une question qui n'en a actuellement aucune, et
[ADR-0001](0001-architecture-and-scope.md) l'affirme depuis avant que la suite ne soit
spécifiée.

## Hors périmètre

- **Aucune marque de conformité, et aucune permission d'utiliser le nom.** Cette ADR produit
  des preuves. [ADR-0016](0016-conformance-marks-and-naming.md) décide de ce qui peut être
  revendiqué sur leur foi, et la séparation est délibérée : un résultat de test est un fait,
  et une permission de marque est une politique.
- **Aucun service de certification.** Le projet n'exploite rien, n'audite personne, et ne
  facture rien. Quiconque peut exécuter la suite contre sa propre implémentation, et le §7.5
  est ce qui donne de la valeur à un rapport autoproduit.
- **Aucun test de performance ni de charge.** La conformité porte sur le comportement. Une
  implémentation correcte et lente est conforme et lente.
- **Aucun audit de sécurité.** La suite teste le comportement spécifié, y compris le
  comportement pertinent pour la sécurité qui est observable. Le §5.6 est explicite sur ce
  qu'elle ne peut pas atteindre.
- **Aucun test de fidélité d'adaptateur.** Savoir si un adaptateur correspond au fournisseur
  qu'il enveloppe est hors de portée de toute suite
  ([ADR-0013 §9.3](0013-provider-adapter-interface.md)).
- **Aucun droit acquis.** Il n'y a pas de passage partiel et pas de dérogation. §3.5.

## Spécification

Les mots-clés MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
MAY et OPTIONAL sont à interpréter comme décrit dans les RFC 2119 et RFC 8174, lorsque, et
seulement lorsque, ils apparaissent en capitales.

### 1. Ce qu'est la conformité

**1.1.** Une affirmation de conformité est un triplet : une cible, un niveau, et une version
de protocole. Une affirmation à laquelle manque l'un des trois n'est pas reconnue par cette
ADR, et une implémentation MUST NOT en présenter une comme si elle l'était.

**1.2.** La conformité est à une **version** de la spécification, non à OpenFSP en général.
La spécification est versionnée au titre de
[GOVERNANCE.md §5](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#5-garanties-de-stabilité),
et un résultat obtenu contre une version MAJEURE ne dit rien d'une autre.

**1.3.** La conformité est une propriété d'une **configuration de déploiement**, non d'un
dépôt de code source. La même passerelle configurée contre un ensemble de fournisseurs
différent peut passer des profils différents, et le §6.3 régit ce à quoi un résultat peut être
généralisé.

**1.4.** Un résultat est daté et reproductible. Quiconque détient la même implémentation, la
même version de suite et la même configuration MUST pouvoir obtenir le même résultat, ce que
[ADR-0014 §6](0014-mock-server-behaviour.md) rend possible.

### 2. Cibles

**2.1.** La suite teste trois sortes de choses, et elles ne sont pas interchangeables.

| Cible | Ce qui est testé | Ce qui tient lieu du reste |
|---|---|---|
| **Client** | Une application ou un SDK qui appelle une passerelle. | Une passerelle de référence conforme. |
| **Passerelle** | Un serveur implémentant le protocole. | Le serveur simulé ([ADR-0014](0014-mock-server-behaviour.md)) comme fournisseur. |
| **Fournisseur natif** | Un fournisseur implémentant OpenFSP directement, sans passerelle entre les deux. | Rien. Le fournisseur est l'implémentation. |

**2.2. La conformité client** porte sur ce qu'un client fait de ce qu'il reçoit :
récupère-t-il par référence après une expiration, refuse-t-il de traiter une URL de retour
comme un reçu, réutilise-t-il une clé d'idempotence à la reprise, traite-t-il un paiement qui
reste `pending`. Ce sont les comportements que
[ADR-0006 §7](0006-gateway-http-api-payments.md) et
[ADR-0004 §8](0004-idempotency-and-retries.md) exigent des clients et que rien n'a vérifiés
jusqu'ici.

**2.3. La conformité passerelle** est le cas principal et l'essentiel du §5.

**2.4. La conformité fournisseur natif** est l'échelle que décrit
[ADR-0001](0001-architecture-and-scope.md) : un fournisseur qui implémente lui-même le
protocole, auquel point l'adaptateur pour lui devient inutile. Ses tests sont ceux de la
passerelle, moins ceux qui n'ont de sens qu'avec un fournisseur derrière l'implémentation.
§5.7.

**2.5.** Une exécution de test vise exactement une cible. Une passerelle et son client sont
testés séparément, parce qu'un défaut qui s'annule entre les deux reste deux défauts, et que
le client suivant rencontrera le premier.

### 3. Niveaux

**3.1. Core** est la capacité de base de
[ADR-0006 §2](0006-gateway-http-api-payments.md) plus tout ce qui est obligatoire quelle
que soit la capacité : le modèle de données, le cycle de vie, l'idempotence, la taxonomie des
erreurs, l'authentification, la découverte de capacités, et les tests négatifs du §5.4.

**3.2.** Core n'est pas optionnel et n'est pas un niveau qu'une implémentation choisit. Une
implémentation le passe ou n'est pas conforme du tout.

**3.3. Les profils** portent le nom de la capacité qu'ils testent, et une implémentation gagne
chacun de ceux qu'elle annonce. Un profil MUST NOT être revendiqué pour une capacité que
l'implémentation n'annonce pas au titre de [ADR-0007](0007-capability-discovery.md).

| Profil | Capacité | Spécifié dans |
|---|---|---|
| `payments.lookup` | Lecture autoritaire chez le fournisseur | [ADR-0007 §5](0007-capability-discovery.md) |
| `webhooks.emit` | Livraison d'événements signés | [ADR-0008](0008-webhooks-and-event-delivery.md) |
| `confirmation_requests` | Décision minutée du payeur | [ADR-0011](0011-confirmation-requests.md) |
| `confirmation_requests.cancel` | Retrait avant réponse | [ADR-0011 §7](0011-confirmation-requests.md) |
| `payments.proximity_cpm` | Paiement de comptoir | [ADR-0012](0012-proximity-payments-cpm.md) |

**3.4.** Un profil est ajouté par l'ADR qui ajoute la capacité, et cette ADR spécifie ses
tests. Une ADR qui introduit une capacité sans spécifier comment la tester est incomplète.

**3.5. Il n'y a pas de passage partiel.** Un niveau est passé ou ne l'est pas. Une
implémentation qui échoue à un test Core échoue à Core, quoi qu'elle passe par ailleurs, et la
suite MUST NOT émettre un résultat suggérant le contraire. Un crédit partiel dans une suite de
conformité de paiement est une invitation à livrer la partie qui échoue.

**3.6.** Passer chaque profil n'est pas un niveau distinct et ne reçoit aucun nom
supplémentaire. Une passerelle servant un fournisseur qui ne peut réellement pas faire de
remboursements n'est pas moins conforme qu'une passerelle dont le fournisseur le peut ; elle
est conforme contre un fournisseur différent. Classer les implémentations par nombre de
capacités punirait l'honnêteté, qui est le contraire de ce que cette spécification récompense.

### 4. Comment la suite s'exécute

**4.1.** La suite est un programme. Elle est exécutée par qui veut le résultat, contre une
implémentation vers laquelle il la pointe, et elle produit le rapport du §7.

**4.2.** Pour une cible passerelle, la suite agit comme un client, et le serveur simulé
([ADR-0014](0014-mock-server-behaviour.md)) tient lieu de fournisseurs. La passerelle
testée est configurée contre la simulation et est par ailleurs non modifiée.

**4.3.** La suite MUST NOT exiger que l'implémentation testée soit modifiée, instrumentée, ou
dotée d'un mode réservé au test. Tout ce dont la suite a besoin, elle l'obtient par le
protocole. Une suite qui exige un point d'accroche a cessé de tester la chose qui sera
déployée.

**4.4.** L'unique exception est la configuration : pointer une passerelle vers la simulation,
et fournir des identifiants que la suite peut utiliser. Les deux sont des opérations de
déploiement ordinaires.

**4.5.** La suite pilote directement la surface de contrôle de la simulation
([ADR-0014 §5](0014-mock-server-behaviour.md)), non à travers la passerelle. C'est ce qui
lui permet de résoudre un paiement `PENDING_FOREVER` ou de faire arriver un rappel en retard.

**4.6.** La suite MUST être exécutable hors ligne, en intégration continue, sans compte nulle
part. Un mécanisme de conformité qui exigerait d'atteindre un service exploité par le projet
ferait du projet un gardien, ce que [ADR-0001](0001-architecture-and-scope.md) exclut.

### 5. Ce que la suite teste

**5.1. Forme.** Que les requêtes et les réponses correspondent à la spécification : les types
de média ([ADR-0006 §1.4](0006-gateway-http-api-payments.md)), l'enveloppe de collection
([ADR-0006 §1.12](0006-gateway-http-api-payments.md)), `Request-Id` sur chaque réponse
([ADR-0006 §1.8](0006-gateway-http-api-payments.md)), des problem details sur chaque erreur
([ADR-0005 §1](0005-error-taxonomy.md)), `Money` en unités mineures entières
([ADR-0002 §3](0002-core-data-model.md)), des horodatages RFC 3339 UTC
([ADR-0002 §7](0002-core-data-model.md)), et un traitement strict des requêtes avec un
traitement tolérant des réponses ([ADR-0002 §2.3](0002-core-data-model.md)).

**5.2. Cycle de vie.** Que chaque transition de
[ADR-0003 §2](0003-payment-lifecycle.md) est atteignable, qu'aucun état terminal n'est
jamais quitté, qu'un paiement rapporté terminal par la simulation puis rapporté différemment
produit une erreur de fournisseur plutôt qu'une transition
([ADR-0003 §2.1](0003-payment-lifecycle.md)), et que `failure_reason` est présent
exactement quand `status` vaut `failed`.

**5.3. Idempotence.** Qu'une clé rejouée retourne la réponse enregistrée
([ADR-0004 §3.2](0004-idempotency-and-retries.md)), que la même clé avec un corps différent
est rejetée ([ADR-0004 §3.4](0004-idempotency-and-retries.md)), qu'un doublon concurrent
obtient `idempotency-request-in-progress`, que les enregistrements sont cloisonnés au
principal ([ADR-0004 §2.3](0004-idempotency-and-retries.md), et qu'un second principal
présentant la même clé MUST NOT recevoir la réponse du premier), et qu'une `reference` en
double est rejetée avec `reference-conflict` de façon permanente plutôt que pour une fenêtre.

**5.4. Refus.** Ce sont les tests qui comptent le plus, et chacun d'eux ne passe que lorsque
l'implémentation décline de faire quelque chose.

| Test | L'implémentation doit | Spécifié dans |
|---|---|---|
| Synchroniser sans `payments.lookup` | retourner `capability-not-supported`, et MUST NOT retourner son état stocké comme s'il avait été relu | [ADR-0007 §5.3](0007-capability-discovery.md) |
| Synchroniser un paiement terminal sans `payments.lookup` | le retourner inchangé avec un `200`, qui est l'unique exception permise | [ADR-0007 §5.3.1](0007-capability-discovery.md) |
| Toute opération de capacité non annoncée | retourner `capability-not-supported` | [ADR-0007 §1.3](0007-capability-discovery.md) |
| POST mutant sans `Idempotency-Key` | retourner `idempotency-key-required` | [ADR-0004 §1.3](0004-idempotency-and-retries.md) |
| Dénouement fournisseur indéterminé, fournisseur sans idempotence ni recherche | laisser le paiement `pending` et MUST NOT renvoyer | [ADR-0004 §7.4](0004-idempotency-and-retries.md) |
| Statut de fournisseur inconnu venant de la simulation | laisser le paiement `pending`, MUST NOT le projeter sur un état terminal | [ADR-0003 §1.1](0003-payment-lifecycle.md) |
| Rappel de fournisseur non signé, hors URL propre au paiement, affirmant un succès | MUST NOT transitionner sur le seul rappel | [ADR-0003 §6.3](0003-payment-lifecycle.md) |
| Rappel sur une URL propre au paiement portant un jeton erroné | le rejeter sans effet sur aucun paiement | [ADR-0003 §6.6](0003-payment-lifecycle.md) |
| Relevé ne mentionnant pas un paiement dont `expires_at` n'est pas écoulé | laisser le paiement `pending`, MUST NOT enregistrer `expired` | [ADR-0003 §5.3](0003-payment-lifecycle.md), [§6.7](0003-payment-lifecycle.md) |
| Requête de l'API marchande tentant de fixer l'état d'un paiement | MUST NOT modifier l'état : l'attestation n'est pas exposée par cette API | [ADR-0003 §6.8](0003-payment-lifecycle.md) |
| Le fournisseur réémet des identifiants dans un corps d'erreur | les caviarder de `provider_detail`, en émettant `[redacted]` | [ADR-0009 §9.5](0009-authentication-and-credentials.md), [§9.7](0009-authentication-and-credentials.md) |
| Clés d'API inconnue, révoquée, et du mauvais environnement | produire trois réponses `unauthenticated` indiscernables | [ADR-0009 §4.7](0009-authentication-and-credentials.md) |
| `payer_token` et `payer` tous deux présents | retourner `invalid-field` | [ADR-0012 §3.2](0012-proximity-payments-cpm.md) |

**5.5.** Les scénarios de simulation de
[ADR-0014 §4.3](0014-mock-server-behaviour.md) existent pour rendre le §5.4 exécutable, et
chaque ligne ci-dessus nomme le scénario qu'elle utilise. Un scénario sans test et un test sans
scénario sont tous deux des défauts.

**5.6. Ce que la suite ne peut pas tester.** Une passerelle qui annonce `webhooks.verify` et
n'effectue aucune vérification passe chaque test fonctionnel, parce que la signature de la
simulation est valide et que la vérifier ou non produit le même dénouement observable. C'est
la limite de [ADR-0007 §6.2](0007-capability-discovery.md) et celle de
[ADR-0013 §4.4](0013-provider-adapter-interface.md), et la suite MUST le rapporter comme
limitation connue plutôt que laisser un résultat positif laisser entendre le contraire. §7.4.

**5.7. Fournisseur natif.** Les tests sont ceux de la passerelle, moins les lignes du §5.4
portant sur le comportement du fournisseur, qui n'ont aucun sens quand l'implémentation est le
fournisseur. Une implémentation fournisseur natif reste soumise à chaque refus concernant ses
propres capacités : elle déclare ce qu'elle fait, et la suite vérifie qu'elle décline le reste.

**5.8. Les tests client** exercent les obligations client que la spécification énonce déjà :
réutilisation d'une clé d'idempotence à la reprise
([ADR-0004 §8.1](0004-idempotency-and-retries.md)), aucune reprise d'un `4xx` non rejouable
([ADR-0004 §8.2](0004-idempotency-and-retries.md)), récupération par référence après une
réponse perdue ([ADR-0006 §5.2.3](0006-gateway-http-api-payments.md)), refus de traiter une
URL de retour comme preuve ([ADR-0006 §7.3](0006-gateway-http-api-payments.md)), tolérance
aux membres de réponse inconnus, traitement correct d'un paiement qui ne quitte jamais
`pending`, et, là où le client reçoit des événements, vérification avant d'agir
([ADR-0008 §5.9](0008-webhooks-and-event-delivery.md)) avec un chemin de sondage qui
fonctionne quand chaque événement est retenu
([ADR-0008 §10.4](0008-webhooks-and-event-delivery.md)).

**5.9.** La suite MUST inclure au moins un test par exigence normative qu'elle est capable
d'observer, et le rapport MUST rendre explicite la correspondance du test à l'exigence. Une
suite de tests dont la relation à la spécification n'est pas documentée est une seconde
spécification.

### 6. Versionnement et validité

**6.1.** La suite est versionnée avec la spécification. Une version de suite teste exactement
une version MINEURE du protocole et MUST refuser de s'exécuter contre une implémentation
annonçant une version MAJEURE qu'elle ne connaît pas.

**6.2.** Un résultat nomme la version de la suite, la version du protocole, la cible, le
niveau, les profils, la date, et la configuration sous laquelle il a été obtenu. Un résultat
auquel il manque l'un de ces éléments ne peut pas être reproduit.

**6.3. Un résultat se généralise à la configuration sous laquelle il a été obtenu, et pas
plus loin.** Une passerelle testée contre la simulation a été montrée se comporter
correctement étant donné les comportements de fournisseur que la simulation produit. Il n'a pas
été montré qu'elle fonctionne avec un vrai fournisseur, et affirmer le contraire est faux. Les
*Considérations de sécurité* y reviennent.

**6.4.** Un résultat n'expire pas au calendrier, et il devient périmé quand l'implémentation
change ou que la version du protocole change. Une implémentation qui cite un résultat MUST
citer la version d'elle-même qui l'a produit.

**6.5.** Un incrément CORRECTIF de la spécification peut ajouter des tests, puisqu'un correctif
clarifie une formulation qui était déjà normative
([GOVERNANCE.md §5](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#5-garanties-de-stabilité)).
Une implémentation qui passait avant et échoue après s'est révélée non conforme depuis le
début, et les notes de version de la suite MUST dire quand un correctif ajoute des tests.

### 7. Le rapport

**7.1.** Une exécution produit un rapport lisible par machine. C'est son contenu, non son
encodage, que cette section spécifie.

**7.2.** Il porte : le triplet du §1.1, la version de la suite, la date, la configuration, un
résultat par test, et l'exigence à laquelle chaque test correspond.

**7.3.** Un test en échec apparaît dans le rapport avec ce qui était attendu et ce qui a été
observé. Un rapport qui dit seulement que quelque chose a échoué renvoie le lecteur au code
source.

**7.4.** Le rapport MUST porter les limitations du §5.6 explicitement, à chaque exécution, y
compris une exécution réussie. Un lecteur qui prend un rapport au vert pour une assurance de
sécurité a été induit en erreur par une omission, et l'omission est corrigeable.

**7.5. Les rapports sont reproductibles, ce qui est ce qui rend l'autoexécution crédible.** Le
projet n'audite personne (*Hors périmètre*), de sorte que la valeur d'un rapport repose sur la
possibilité pour quiconque d'obtenir le même depuis les mêmes entrées. Une implémentation qui
publie un rapport SHOULD publier la configuration nécessaire pour le reproduire, et une
implémentation qui ne le fait pas a publié une assertion plutôt qu'une preuve.

**7.6.** Le rapport est l'entrée de
[ADR-0016](0016-conformance-marks-and-naming.md). Cette ADR dit ce qu'il contient ; celle-là
dit ce qui peut être revendiqué sur sa foi.

## Compatibilité

Rien ne casse. Cette ADR n'ajoute aucun comportement sur le fil, ne change aucun champ, et
n'impose aucune exigence à une implémentation qui ne lui était pas déjà imposée par l'ADR
testée. Chaque exigence que la suite vérifie est référencée à l'ADR qui l'a posée.

Le changement visible est que des comportements auparavant inapplicables deviennent
applicables. Une implémentation qui émulait une capacité manquante était déjà non conforme à
[ADR-0007 §1.3](0007-capability-discovery.md) ; elle l'est maintenant de façon détectable.

De nouveaux tests peuvent être ajoutés par toute ADR qui ajoute une exigence, et par un
correctif au titre du §6.5. Ni l'un ni l'autre n'est une rupture de compatibilité du protocole,
et les deux peuvent changer le résultat d'une implémentation.

## Considérations de sécurité

**Un résultat positif n'est pas une assurance de sécurité, et le mésusage le plus probable de
cette ADR est de le traiter comme tel.** Le §5.6 nomme la lacune précise : les capacités dont
l'implémentation honnête est inobservable ne peuvent pas être testées, et `webhooks.verify` est
le cas le plus net. Le §7.4 exige que chaque rapport le dise, parce que l'alternative est un
badge vert tenant lieu d'une relecture que personne n'a faite.

**La portée d'un résultat est étroite, et la tentation de l'élargir est commerciale.** Le §6.3
confine un résultat à la configuration qui l'a produit. Une passerelle testée contre la
simulation et commercialisée comme éprouvée contre de vrais fournisseurs a fait une affirmation
que la suite ne soutient pas, et c'est l'affirmation qu'un fournisseur de solution veut le plus
faire.

**La suite détient des identifiants pour l'implémentation testée.** Ce sont des identifiants de
test dans un environnement `test`
([ADR-0009 §2.4](0009-authentication-and-credentials.md)), et une exécution de la suite
contre un déploiement `live` avec des identifiants `live` créerait de vrais paiements. Le
segment d'environnement refuse cette combinaison avant que quoi que ce soit ne se produise, ce
qui est une des raisons de son existence.

**La suite est adverse par conception.** Elle présente des requêtes malformées, des rappels
contrefaits, et des identifiants qu'elle ne devrait pas avoir, ce qui est pourquoi le §4.6
exige qu'elle soit exécutable hors ligne et pourquoi la pointer vers le déploiement de
production de quelqu'un d'autre est une attaque et non un test.

## Considérations réglementaires

La section 5 de `BRH-121` liste l'interopérabilité parmi les exigences techniques qu'un
fournisseur doit satisfaire, et exige que la conformité à ces exigences soit attestée par un
audit externe au moins une fois tous les trois ans. Elle ne prescrit aucune norme. La
section 3 t) de `BRH-126` exige un second audit triennal, de la sécurité du système
d'information, avec une copie annexée au rapport annuel de contrôle interne, et ne prescrit
aucune norme non plus [BRH-126, p. 4].

Cette ADR est la part de la réponse d'OpenFSP qui est vérifiable. Un rapport daté nommant la
version du protocole, le niveau, les profils et la configuration est un artefact qu'un auditeur
peut lire, et une suite que quiconque peut réexécuter est un artefact qu'il peut vérifier
plutôt qu'accepter. C'est une chose différente d'une déclaration d'intention, et la différence
est toute la raison pour laquelle [ADR-0001](0001-architecture-and-scope.md) affirme qu'une
spécification ouverte avec une suite exécutable par machine est une réponse auditable.

Deux limites appartiennent au même souffle. La suite teste la conformité à OpenFSP, non la
conformité à la circulaire, et aucun résultat n'est une preuve de la seconde. Et la limite de
portée du §6.3 s'applique à un auditeur autant qu'à un fournisseur de solution : un résultat
obtenu contre la simulation atteste d'un comportement étant donné des fournisseurs simulés.

La section 13.4 de `BRH-121` exige un registre des opérations, et les tests de cycle de vie du
§5.2 sont ce qui établit que le registre d'un déploiement ne peut pas contenir un paiement qui
a quitté un état terminal.

**De quoi un rapport est une preuve, et pour quel audit.** Pour l'audit d'interopérabilité de
la section 5 de `BRH-121`, un rapport nommant la cible, le niveau, les profils et la version du
protocole est une preuve directe : il dit avec quoi le déploiement interopère et comment cela a
été établi. Pour l'audit de sécurité de la section 3 t) de `BRH-126`, c'est au mieux une preuve
partielle. La suite teste le comportement spécifié, y compris le comportement pertinent pour la
sécurité qui est observable, et le §5.6 nomme ce qu'elle ne peut pas atteindre. Un auditeur qui
accepterait un rapport de conformité à la place d'un audit de sécurité aurait été induit en
erreur par un document qui dit, à chaque exécution, qu'il n'en est pas un.

La section 3 p) de `BRH-126` exige séparément d'une institution qu'elle tienne à jour la
documentation de ses systèmes en consignant les changements et les corrections
[BRH-126, p. 4]. Une suite versionnée avec la spécification (§6.1), dont les notes de version
disent quand un correctif a ajouté des tests (§6.5), et dont les rapports sont datés et
reproductibles (§7.5), est ce registre pour la surface de conformité.

## Alternatives envisagées

**Une certification par le projet, avec une relecture et des frais.** Le modèle traditionnel,
et il attraperait les défaillances inobservables du §5.6, ce que l'autotest ne peut pas.
Rejetée sur trois plans. Cela fait du projet un gardien sur un marché où il vend aussi, ce que
[GOVERNANCE.md §2](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#2-intérêt-déclaré)
existe pour empêcher. Cela exige une organisation dont personne n'a la capacité. Et des frais
excluent exactement les petits implémenteurs dont l'adoption dépend.

**Des niveaux en échelle : bronze, argent, or.** Familier et lisible, et cela échoue sur le
§3.6. Une passerelle servant un fournisseur sans capacité de remboursement se classerait
au-dessous d'une passerelle dont le fournisseur l'a, ce qui mesure le fournisseur plutôt que
l'implémentation et donne à un implémenteur une raison d'annoncer une capacité qu'il devrait
décliner. Les profils disent ce qui est pris en charge sans impliquer un classement.

**Des passages partiels avec un pourcentage.** Rejeté au §3.5. Un score de 94 pour cent sur une
suite de conformité de paiement ne dit rien à un marchand sur le fait que les 6 pour cent
manquants soient ou non un chemin de double débit.

**Tester contre de vrais bacs à sable de fournisseurs.** La chose la plus fidèle disponible, et
impossible pour la raison que donne [ADR-0001](0001-architecture-and-scope.md) :
l'accès aux bacs à sable est inégal et aucun bac à sable ne peut produire une défaillance
à la demande, de sorte que les tests qui comptent ne pourraient pas être écrits.
[ADR-0014](0014-mock-server-behaviour.md) existe à cause de cela.

**Exiger l'instrumentation de l'implémentation testée.** Cela permettrait à la suite d'observer
les comportements inobservables du §5.6, tels que la vérification effective d'une signature.
Rejeté au §4.3 : une implémentation avec un point d'accroche de test n'est pas l'implémentation
qui est déployée, et le point d'accroche lui-même devient une surface d'attaque en production.

**Fondre les marques dans cette ADR.** Elles ne faisaient qu'un document au départ. Séparées
parce qu'un résultat de test et une permission de marque répondent à des choses différentes :
l'un est reproductible par quiconque, l'autre est une politique que le dépositaire fixe, et les
mélanger laisserait un changement de politique ressembler à un changement technique.

## Questions non résolues

**Comment la lacune du §5.6 est comblée, si elle peut l'être.** L'honnêteté inobservable est
une limite réelle, et les candidats ont tous des coûts : l'instrumentation (rejetée au §4.3),
la relecture du code source (qui ne passe pas à l'échelle et n'est pas reproductible), ou une
simulation qui envoie délibérément une signature invalide et vérifie que la passerelle la
rejette. Ce dernier candidat est prometteur et ne couvre pas tous les cas, puisqu'une passerelle
pourrait vérifier les signatures et ignorer quand même le résultat.

**Si la conformité client peut être testée sans coopération.** Le §5.8 suppose un client qu'on
peut pointer vers une passerelle de référence et conduire à travers des scénarios. Un SDK le
peut ; le tunnel d'achat d'un marchand largement pas, et les obligations client de
[ADR-0004 §8](0004-idempotency-and-retries.md) sont celles qui sont le plus souvent violées.

**Ce qu'une implémentation fournisseur natif fait de la simulation.** Le §5.7 retire les tests
tournés vers le fournisseur, et il n'est pas évident que ce qui reste soit une barre
suffisante. La question devient concrète la première fois qu'un fournisseur la pose.

**Si la suite devrait tester la correspondance ISO 20022.**
[ADR-0010](0010-iso-20022-semantic-correspondence.md) est Informational et ne lie rien, il
n'y a donc rien à tester. Si un exportateur est un jour construit, la correspondance devient
testable à travers lui, et c'est ici que ces tests vivraient.

**Comment un déploiement prouve sous quelle configuration un rapport a été obtenu.** Le §7.5
demande que la configuration soit publiée et ne spécifie aucun format, de sorte que deux
rapports ne sont actuellement comparables d'aucune façon mécanique.

## Références

Citations complètes dans [`references.md`](references.md).

**Normatives.** `RFC2119` et `RFC8174` pour les mots-clés d'exigence. Chaque ADR OpenFSP que
cette suite teste, chacune référencée au §5 à l'exigence qu'elle vérifie.

**Informatives.** `BRH-121` section 5 et `BRH-126` section 3 t), les deux audits triennaux que
cette suite est censée servir, et `BRH-126` section 3 p) pour le devoir de documentation auquel
le §6 répond. `GSMA-MMAPI` exploite un service de conformité pour sa propre spécification, qui
est le modèle que [ADR-0016](0016-conformance-marks-and-naming.md) examine et décline.

## Implémentation de référence

Aucune pour l'instant. La suite dépend du serveur simulé, que
[ADR-0014](0014-mock-server-behaviour.md) spécifie et qui n'existe pas non plus.

## Errata

Aucun.
