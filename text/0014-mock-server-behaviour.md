# ADR-0014 : Comportement du serveur simulé

- Voie : Informative
- Statut : Brouillon
- Créée : 2026-09-07
- Dépend de : ADR-0001, ADR-0003, ADR-0004, ADR-0005, ADR-0006, ADR-0007, ADR-0011, ADR-0012, ADR-0013

## Résumé

Le serveur simulé imite les fournisseurs de paiement afin qu'une intégration puisse être
construite et une passerelle testée sans compte marchand nulle part. Ce document dit ce
qu'il garantit, afin qu'un test qui passe contre lui signifie quelque chose.

Trois choses en font davantage qu'un bouchon. Il présente **plusieurs fournisseurs aux
capacités délibérément inégales** (§3), parce qu'une passerelle qui n'a jamais parlé qu'à un
fournisseur n'a pas exercé le modèle de capacités du tout. Il rend **chaque défaillance
reproductible à la demande** (§4), ce qu'aucun bac à sable de fournisseur ne fait et qui est
la raison d'être de la simulation. Et il est **impossible à prendre pour de la production**
(§7), ce qui en paiement est une propriété de sûreté plutôt qu'une coquetterie.

Sa règle directrice est le §2.1 : la simulation n'est jamais plus indulgente qu'un vrai
fournisseur. Une simulation plus facile à satisfaire que la chose qu'elle imite produit des
intégrations qui marchent en test et échouent sur un marché, où l'écart se découvre sur de
l'argent réel.

## Motivation

[ADR-0001](0001-architecture-and-scope.md) dit que les preuves de ces ADR viennent d'une
simulation plutôt que d'une intégration en production, parce que l'accès aux bacs à sable
va de l'inscription libre à une démarche auprès de l'opérateur, et qu'aucun d'eux ne rend
une défaillance reproductible à la demande. C'est une affirmation forte sur laquelle faire reposer une
spécification, et elle ne vaut que ce que vaut la simulation.

La chose testée est principalement la défaillance. Presque chaque règle des ADR de la voie
Standards porte sur quelque chose qui tourne mal : une expiration dont le dénouement est
inconnu, un rappel qui ne peut pas être vérifié, un paiement qui reste en attente une heure,
un doublon soumis sous pression réseau, un fournisseur qui rapporte un statut que personne
n'a jamais vu. Un vrai bac à sable vous donnera un paiement réussi de façon fiable et aucune
de ces choses sur demande. Vous les attendez, ou vous ne les voyez jamais.

La conséquence est visible dans chaque intégration de paiement jamais écrite : le chemin
heureux est bien testé et les chemins de récupération ne le sont pas du tout, parce qu'ils ne
pouvaient pas l'être. [ADR-0006 §7.4](0006-gateway-http-api-payments.md) fait ce point à
propos de l'URL de retour, et il se généralise. La vulnérabilité la plus fréquente des
intégrations de paiement est invisible en test, parce que le chemin heureux fonctionne
parfaitement que le contrôle soit effectué ou non.

Une simulation à qui l'on peut dire d'expirer, de perdre un rappel, de répondre à une
recherche par un statut que l'adaptateur n'a jamais vu, et d'approuver une demande de
confirmation dans la seconde même où le marchand l'annule, convertit chacun de ces cas en test
ordinaire. C'est l'argument pour en construire une.

Il y a un second argument, plus modeste et néanmoins réel. Un marchand qui évalue OpenFSP
devrait pouvoir exécuter un tunnel d'achat de bout en bout en dix minutes sans contacter de
fournisseur. L'adoption dépend de ce que cela soit vrai.

## Hors périmètre

- **Aucune exigence normative.** Informational, donc aucun mot-clé RFC 2119, selon
  [le processus ADR](https://github.com/openfspht/adrs/blob/main/README.md#voies).
- **Aucune imitation du format de fil d'un fournisseur précis.** La simulation imite les
  fournisseurs tels que la passerelle les éprouve, à travers des adaptateurs. Qu'un
  adaptateur simulé lui parle par une API en forme de MonCash ou par une API commode est un
  choix d'implémentation, et le §3.5 dit pourquoi la distinction compte moins qu'il n'y
  paraît.
- **Aucune simulation de performance.** La simulation n'est pas un générateur de charge et
  ses temps ne sont pas représentatifs. Le §4.6 couvre le seul comportement temporel qui est
  délibéré.
- **Aucun règlement, grand livre ni solde.** L'argent dans la simulation est un nombre qui
  change d'état, non un compte qui est débité.
- **Aucun usage en production.** Le §7 vise à rendre cela structurellement difficile plutôt
  qu'à le déconseiller simplement.

## 1. Ce qu'est la simulation

**1.1.** La simulation est un serveur qui se tient là où se tiennent les fournisseurs. Une
passerelle configurée contre elle exécute ses adaptateurs ordinaires, sa machine à états
ordinaire et son traitement de rappels ordinaire, et la seule chose qui diffère est ce qui se
trouve à l'autre bout.

**1.2.** C'est donc un test de la passerelle et du client, et non un test de la fidélité d'un
adaptateur à un vrai fournisseur. Le §5 de
[ADR-0013](0013-provider-adapter-interface.md) est où cette limite est posée : un
adaptateur n'est honnête qu'autant que la lecture que son auteur a faite de la documentation
d'un fournisseur, et aucune simulation ne peut vérifier cette lecture.

**1.3.** La simulation est aussi la cible d'implémentation de référence pour les deux
capacités qu'aucun adaptateur ne peut atteindre : les demandes de confirmation
([ADR-0011 §9.3](0011-confirmation-requests.md)) et les paiements de proximité
([ADR-0012 §8.4](0012-proximity-payments-cpm.md)). Pour celles-là, elle n'est pas un
substitut à un fournisseur qui existe ; elle est la seule implémentation qui soit.

## 2. La règle directrice

**2.1. La simulation n'est jamais plus permissive qu'un vrai fournisseur.** Là où les
fournisseurs diffèrent, elle prend le comportement le plus strict. Là où un vrai fournisseur
rejetterait une requête, la simulation la rejette. Là où un vrai fournisseur est lent, la
simulation ne répond pas instantanément par défaut (§4.6).

**2.2.** La règle compte parce que la défaillance qu'elle prévient est silencieuse. Une
simulation qui accepte un numéro de téléphone malformé, ou qui tolère un champ manquant qu'un
fournisseur exige, produit une intégration qui passe ses tests et échoue au premier contact
avec un marché. Personne ne le découvre avant qu'un client ne se tienne à une caisse.

**2.3.** Le corollaire est que la simulation a le droit d'être agaçante. Une suite de tests
qu'il faut corriger parce que la simulation a refusé quelque chose de négligé vient de faire
son travail.

**2.4. La simulation n'invente pas de capacités non plus.** Tout ce que
[ADR-0013 §3](0013-provider-adapter-interface.md) interdit à un adaptateur de faire, la
simulation ne le fait pas non plus, et les fournisseurs simulés du §3 sont configurés de sorte
qu'au moins l'un d'eux manque de chaque capacité optionnelle. Une passerelle qui ne voit
jamais qu'un fournisseur pleinement capable n'a jamais exécuté son propre chemin
`capability-not-supported`.

## 3. La flotte de fournisseurs

**3.1.** La simulation présente plusieurs fournisseurs, pas un seul. Leurs capacités sont
délibérément inégales, afin qu'une passerelle et un client rencontrent le modèle de capacités
plutôt que de supposer un monde uniforme.

| Fournisseur simulé | Capacités | Existe pour exercer |
|---|---|---|
| `mock_alpha` | `payments`, `payments.lookup`, `webhooks.verify` | Le cas confortable. Rappels signés, recherche faisant autorité. |
| `mock_beta` | `payments` seulement | Le cas le plus dur. Aucune source automatique d'[ADR-0003 §6.5](0003-payment-lifecycle.md) : chaque paiement attend une attestation de l'exploitant, et [ADR-0004 §7.4](0004-idempotency-and-retries.md) s'applique aux opérations indéterminées. |
| `mock_gamma` | `payments`, `payments.lookup`, `confirmation_requests`, `confirmation_requests.cancel`, `payments.proximity_cpm` | Le flux de comptoir, qu'aucun vrai fournisseur n'offre aujourd'hui. |
| `mock_delta` | `payments`, `payments.lookup`, `confirmation_requests` | Une confirmation qui ne peut pas être retirée. §3.3. |
| `mock_epsilon` | `payments`, `webhooks.per_payment_url`, `payments.statement` | Le cas intermédiaire. Ni signature ni recherche, mais une URL de rappel par paiement et un relevé. §3.6. |

**3.2.** `mock_beta` est l'important. C'est le fournisseur dont personne ne veut et auquel
plusieurs vrais ressemblent : aucun moyen de demander ce qui s'est passé, aucun moyen de
vérifier ce qui est arrivé. L'essentiel du raisonnement soigneux de
[ADR-0003](0003-payment-lifecycle.md) et de [ADR-0004](0004-idempotency-and-retries.md) existe
pour des fournisseurs comme lui, et une suite de tests qui ne le configure jamais n'a jamais
testé ce raisonnement. Il exerce aussi le chemin d'attestation d'[ADR-0003
§6.8](0003-payment-lifecycle.md), le seul qui lui reste.

**3.3.** `mock_delta` existe pour une ligne de la spécification.
[ADR-0011 §7.8](0011-confirmation-requests.md) exige d'une passerelle servant un
fournisseur sans opération de retrait qu'elle retourne `capability-not-supported` plutôt que
d'accepter une annulation qu'elle n'effectuera silencieusement pas, et tester cela demande un
fournisseur offrant `confirmation_requests` et pas `confirmation_requests.cancel`.
`mock_gamma` a les deux et `mock_alpha` n'a ni l'une ni l'autre, donc aucun des deux ne peut
produire le cas. Une paire de capacités qui peut se dissocier exige un fournisseur où elle
s'est dissociée.

**3.4.** Les identifiants de fournisseur utilisés par la simulation sont réservés par préfixe.
Le [registre des fournisseurs](https://github.com/openfspht/openfsp/blob/main/registries/providers.md)
réserve `mock_`, et aucun vrai fournisseur ne se voit assigner un identifiant dans cet espace.
C'est ce qui rend le §7 applicable : un enregistrement de paiement portant `mock_beta` est
sans ambiguïté pour toujours, y compris dans une base de données restaurée d'une sauvegarde
cinq ans plus tard.

**3.5.** Savoir si chaque fournisseur simulé parle une API distincte en forme de fournisseur
ou une API commune est laissé ouvert. L'argument pour des formes distinctes est que les
adaptateurs sont alors de vrais adaptateurs ; l'argument contre est que les formes seraient
inventées plutôt qu'observées, ce qui ne teste rien sur les vrais fournisseurs et double la
surface de la simulation. Les *Questions non résolues* le consignent.

**3.6.** `mock_epsilon` isole les deux sources intermédiaires d'[ADR-0003
§6.5](0003-payment-lifecycle.md). Il n'a ni signature ni recherche, de sorte qu'une passerelle
ne peut finaliser ses paiements que par l'URL propre au paiement (§6.6) ou par le relevé
(§6.7). Le scénario `NO_CALLBACK` du §4.3 y oblige la passerelle à attendre le relevé, et un
rappel reçu sur une URL au jeton erroné y MUST être rejeté sans effet.

## 4. Provoquer les défaillances

**4.1.** Chaque comportement du §4.3 est sélectionné de façon déterministe par le marchand, à
la création du paiement, et aucun scénario ne survient jamais sans avoir été demandé. Une
simulation qui échoue au hasard produit des tests instables, et une suite de tests instable
est une suite dont les échecs cessent d'être lus.

**4.2. Le sélecteur est un préfixe réservé sur `reference`.** Un paiement dont la référence
commence par `MOCK-<SCENARIO>-` déclenche ce scénario. La référence a été choisie comme
sélecteur parce que le marchand la choisit déjà avant d'envoyer la requête
([ADR-0002 §6.2](0002-core-data-model.md)), qu'elle apparaît dans chaque journal et chaque
réponse, et qu'elle survit aux défaillances réseau testées. Un sélecteur fondé sur le montant
était l'alternative et est discuté dans *Alternatives envisagées*.

**4.3. Les scénarios.** Cet ensemble couvre les défaillances sur lesquelles raisonnent les
ADR de la voie Standards.

| Scénario | La simulation fait | Teste |
|---|---|---|
| `SUCCESS` | Se dénoue promptement. | Le chemin heureux. Aussi le défaut quand aucun préfixe n'est présent. |
| `DECLINE` | Échoue avec une raison de refus. | [ADR-0003 §7.2](0003-payment-lifecycle.md). |
| `INSUFFICIENT` | Échoue pour fonds insuffisants. | La seule correspondance de motif exacte de [ADR-0010 §6](0010-iso-20022-semantic-correspondence.md). |
| `TIMEOUT` | Accepte la requête et ne répond jamais. | [ADR-0004 §5.3](0004-idempotency-and-retries.md) et §7.2, le dénouement indéterminé. |
| `TIMEOUT_THEN_SUCCESS` | Ne répond jamais, mais le paiement a réussi du côté du fournisseur. | Le cas pour lequel [ADR-0004 §7.2](0004-idempotency-and-retries.md) existe : la relecture trouve un paiement dont le client n'a jamais entendu parler. |
| `TIMEOUT_THEN_NOTHING` | Ne répond jamais, et rien ne s'est passé. | Le même chemin de récupération aboutissant à la conclusion opposée. |
| `PENDING_FOREVER` | Reste en attente jusqu'à instruction contraire (§5). | [ADR-0003 §1.1](0003-payment-lifecycle.md), et chaque client qui suppose que les paiements se résolvent. |
| `EXPIRE` | Expire à son échéance. | [ADR-0003 §5](0003-payment-lifecycle.md). |
| `NO_CALLBACK` | Se dénoue, et n'envoie aucun rappel. | Si le chemin de sondage du client fonctionne ([ADR-0008 §10.2](0008-webhooks-and-event-delivery.md)). |
| `LATE_CALLBACK` | Se dénoue, et envoie le rappel longtemps après. | L'ordre, et les clients qui ont cessé d'écouter. |
| `DUPLICATE_CALLBACK` | Envoie le même rappel plusieurs fois. | La déduplication ([ADR-0008 §8.4](0008-webhooks-and-event-delivery.md)). |
| `UNKNOWN_STATUS` | Rapporte un statut que l'adaptateur n'a jamais vu. | [ADR-0013 §3.2](0013-provider-adapter-interface.md) : le paiement reste en attente, rien n'est inventé. |
| `PROVIDER_ERROR` | Retourne une erreur côté fournisseur. | La correspondance de [ADR-0005 §9](0005-error-taxonomy.md), et un `effect` d'`unknown`. |
| `UNREACHABLE` | Refuse la connexion. | `provider-unavailable`, et qu'il n'est pas confondu avec une expiration ([ADR-0013 §5.6](0013-provider-adapter-interface.md)). |
| `CREDENTIAL_ECHO` | Retourne les identifiants reçus dans son corps d'erreur. | Le caviardage de [ADR-0009 §9.5](0009-authentication-and-credentials.md), et c'est le test que nomme [ADR-0009 §11.2](0009-authentication-and-credentials.md). |
| `APPROVE_THEN_FAIL` | Approuve une demande de confirmation, puis fait échouer la capture. | [ADR-0011 §5.1](0011-confirmation-requests.md) : une approbation n'est pas un reçu. Le scénario le plus précieux d'ici. |
| `CANCEL_RACE` | Approuve à l'instant même où une annulation arrive. | [ADR-0011 §7.5](0011-confirmation-requests.md). |
| `TOKEN_EXPIRED` | Rejette un jeton de payeur comme expiré. | [ADR-0012 §5.2](0012-proximity-payments-cpm.md). |
| `TOKEN_USED` | Rejette un jeton de payeur comme déjà résolu. | [ADR-0012 §5.1.3](0012-proximity-payments-cpm.md). |

**4.4.** L'ensemble est appelé à grandir, et un scénario est ajouté quand une ADR spécifie un
comportement qui ne peut pas être provoqué autrement. Un scénario qui existe parce qu'il était
facile à implémenter, plutôt que parce qu'un comportement spécifié en a besoin, est du poids
mort dans une suite que tout le monde exécute.

**4.5.** Une référence sans préfixe `MOCK-` se comporte comme `SUCCESS`. Le cas courant est
donc celui qui n'exige aucun cérémonial, et un développeur qui n'a jamais lu ce document
obtient un paiement fonctionnel.

**4.6. Temps.** La simulation introduit un petit délai fixe avant de répondre, plutôt que de
répondre instantanément. Les réponses instantanées cachent les courses : un client dont le
gestionnaire de rappel et la réponse de création arrivent dans un ordre qui ne survient jamais
en production passera ses tests et échouera sur un marché. Le délai est fixe plutôt
qu'aléatoire, afin que les tests restent déterministes.

## 5. Contrôler le temps et l'état

**5.1.** Plusieurs scénarios doivent être avancés délibérément. `PENDING_FOREVER` doit bien
devenir quelque chose un jour, un test d'expiration ne peut pas attendre quinze minutes, et
l'expiration d'une demande de confirmation prend soixante secondes qu'une suite de tests ne
devrait pas dépenser.

**5.2.** La simulation expose donc une surface de contrôle, séparée de sa surface tournée vers
les fournisseurs, qui peut résoudre un paiement en attente vers un dénouement choisi, livrer
un rappel qui avait été retenu, et avancer l'horloge aux fins d'expiration.

**5.3.** La surface de contrôle ne fait partie de l'API d'aucun fournisseur et aucun
adaptateur ne l'utilise. Elle est pilotée par le test, non par la passerelle, ce qui garde la
vue que la passerelle a de la simulation identique à celle qu'elle a d'un vrai fournisseur.

**5.4.** Avancer l'horloge n'affecte que la notion d'expiration propre à la simulation. Cela
ne change pas et ne peut pas changer l'horloge de la passerelle, ce qui signifie qu'un test
d'expiration exerce le traitement par la passerelle d'un fournisseur qui rapporte une
expiration, et non le minuteur propre à la passerelle. C'est la bonne chose à tester, puisque
[ADR-0003 §5](0003-payment-lifecycle.md) et
[ADR-0011 §3.4](0011-confirmation-requests.md) placent tous deux l'autorité du côté du
fournisseur.

## 6. Déterminisme

**6.1.** La même séquence de requêtes contre une simulation fraîchement démarrée produit la
même séquence de réponses. Il n'y a aucun aléa dans la sélection des dénouements, dans
l'assignation des identifiants là où un test peut avoir besoin de les prédire, ni dans les
temps au-delà du délai fixe du §4.6.

**6.2.** L'état est par instance et ne persiste pas entre redémarrages. Une suite de tests
démarre une simulation, s'exécute, et la jette, et aucun test ne dépend du résidu d'un autre.

**6.3.** Le déterminisme est ce qui rend la simulation utilisable en intégration continue, et
c'est la propriété qui la distingue d'un bac à sable de fournisseur. Un bac à sable qui échoue
une exécution sur cinquante pour des raisons que personne ne peut reproduire entraîne une
équipe à relancer le pipeline, et une équipe qui relance des pipelines finira par en relancer
un qui disait la vérité.

## 7. Impossible à prendre pour de la production

**7.1.** Chaque paiement fait à travers la simulation porte un identifiant de fournisseur
simulé (§3.4), qui est réservé et donc sans ambiguïté dans tout enregistrement, pour toujours.

**7.2.** La simulation refuse d'être configurée avec quoi que ce soit ressemblant à un vrai
identifiant de fournisseur, et ses propres identifiants sont des valeurs fixes et publiées
sans prétention de secret.

**7.3.** Une passerelle configurée contre la simulation le dit, en évidence, dans son journal
de démarrage. C'est le même principe que le drapeau de mode de développement de
[ADR-0006 §1.1](0006-gateway-http-api-payments.md) : un mode aux garanties plus faibles
s'annonce plutôt que d'attendre d'être remarqué.

**7.4.** La simulation ne prétend jamais à une devise pour laquelle elle n'est pas
configurée, ne rapporte jamais l'identifiant d'un vrai fournisseur, et ne produit aucun
artefact qu'un marchand pourrait prendre pour un enregistrement de règlement.

**7.5.** [ADR-0007](0007-capability-discovery.md) laisse ouverte la question de savoir si
une simulation devrait s'annoncer comme un fournisseur distinct. Ce document prend la position
qu'elle le devrait, pour la raison que cette ADR anticipe : la distinction rend impossible de
prendre une simulation pour de la production, et dans une infrastructure de paiement cela vaut
plus que la symétrie perdue.

**7.6.** Le segment d'environnement d'une clé d'API
([ADR-0009 §2.4](0009-authentication-and-credentials.md)) est une seconde protection
indépendante. Un déploiement pointé vers la simulation est un environnement `test`, et une clé
`live` qui lui est présentée est refusée avant toute autre chose.

## 8. Ce que la simulation ne prouve pas

**8.1.** Qu'un adaptateur correspond à son fournisseur. §1.2, et
[ADR-0013 §9.3](0013-provider-adapter-interface.md).

**8.2.** Qu'un fournisseur se comporte comme sa documentation le dit. C'est la plus grande
inconnue du projet, et aucune quantité de simulation ne la réduit.

**8.3.** Que le système tient la charge. *Hors périmètre*.

**8.4.** Que les modes de défaillance d'un vrai fournisseur sont ceux du §4.3. La liste a été
assemblée depuis le raisonnement propre à la spécification, qui est une bonne source et n'est
pas la même chose qu'une observation. Une défaillance que personne n'a anticipée n'est pas dans
le tableau, par construction.

**8.5.** Ces limites méritent d'être énoncées parce qu'une suite de tests au vert est
persuasive, et celle-ci est persuasive sur quelque chose de plus étroit qu'il n'y paraît : que
la passerelle et le client se comportent correctement étant donné les comportements de
fournisseur que quelqu'un a pensé à écrire.

## Compatibilité

Rien à casser. La simulation est un composant, non une surface de protocole, et aucune
implémentation conforme ne change à cause de ce document.

La réservation du préfixe `mock_` dans le registre des fournisseurs est le seul changement en
dehors de la simulation elle-même, et il ne contraint que les futures entrées du registre.

## Considérations de sécurité

**La simulation est une machine qui approuve des paiements.** Tout ce qui est au §7 existe
pour qu'elle ne puisse pas être atteinte par quelqu'un qui croit en faire un vrai. La
défaillance à prévenir n'est pas une attaque : c'est une mauvaise configuration de déploiement
où un tunnel d'achat de production est pointé vers une simulation et où chaque paiement semble
réussir alors qu'aucun argent ne bouge. Les §7.1, §7.3 et §7.6 sont trois signaux
indépendants, sur le principe qu'une seule protection ne suffit pas ici.

**La surface de contrôle (§5) est une autorité pour fabriquer des dénouements.** Elle ne fait
pas partie de l'API des fournisseurs et n'est pas exposée à la passerelle, et un déploiement
de simulation qui la rendrait atteignable depuis un réseau où se trouve quelqu'un d'autre a
publié un bouton qui marque des paiements comme réussis. Elle doit être liée à une interface
de bouclage ou derrière la même authentification que le reste de l'environnement de test.

**La simulation ne détient aucun identifiant réel** (§7.2) et n'en émet aucun. Ses
identifiants publiés le sont délibérément, et les traiter comme des secrets créerait
l'habitude que ce document cherche à éviter.

**`CREDENTIAL_ECHO` se comporte délibérément mal** (§4.3), en retournant ce qu'on lui a donné.
Il existe pour tester que la passerelle caviarde
([ADR-0009 §9.5](0009-authentication-and-credentials.md)), et il n'est sûr que parce que
les identifiants impliqués sont ceux, publiés, de la simulation. C'est le seul scénario qui
serait dangereux contre de vraies entrées, et une simulation qu'on pourrait configurer avec un
identifiant réel (§7.2) le rendrait tel.

## Considérations réglementaires

La simulation ne produit aucun paiement, ne détient aucun fonds, et ne règle rien, de sorte
que rien dans la circulaire 121 de la BRH du 6 décembre 2021 ne l'atteint directement. Le §7
est ce qui maintient cela vrai : une simulation prise pour un fournisseur produirait des
enregistrements affirmant des règlements qui n'ont pas eu lieu, et le registre exigé par la
section 13.4 de la circulaire contiendrait alors de la fiction.

La simulation a un rôle réglementaire positif. La section 5 de la circulaire exige que
l'interopérabilité soit attestée par un audit externe au moins tous les trois ans, et ne
prescrit aucune norme selon laquelle elle est jugée. Une suite de conformité est une réponse
auditable, et la suite n'est exécutable que parce que la simulation rend les défaillances
reproductibles. La simulation fait donc partie de ce qui fait de l'affirmation de
[ADR-0001](0001-architecture-and-scope.md) sur l'interopérabilité auditable davantage
qu'une assertion.

## Alternatives envisagées

**Sélectionner les scénarios par le montant.** L'approche courante de l'industrie : débiter
42,00 et obtenir un refus. Rejetée parce que les montants ont du sens. Une suite de tests qui
doit utiliser des montants particuliers ne peut pas aussi tester le traitement des montants, la
conversion de devises ou les limites, et un montant magique qui fuite dans une vraie intégration
débite un vrai client d'un nombre choisi pour un test. La référence est inerte par comparaison
et, contrairement au montant, est déjà la clé de récupération
([ADR-0006 §5.2.3](0006-gateway-http-api-payments.md)).

**Sélectionner les scénarios par un champ de requête dédié.** Le plus propre isolément, et
cela signifie que le schéma de requête de la passerelle porte un membre qui n'existe que pour
le test, ce que [ADR-0006 §1.9](0006-gateway-http-api-payments.md) devrait alors tolérer en
production. Un champ qui doit être ignoré en production est un champ que quelqu'un finira par
ne pas ignorer.

**Sélectionner par `metadata`.** Plausible, et rejeté parce que `metadata`
([ADR-0002 §9](0002-core-data-model.md)) appartient au marchand. Réserver une clé à
l'intérieur reprend quelque chose que la spécification avait cédé.

**Injection aléatoire de défaillances.** Le chaos testing a une vraie place, et ce n'est pas
ici. La valeur de la simulation est qu'une défaillance peut être exigée, examinée, corrigée et
exigée à nouveau. L'aléa rend la première et la dernière de ces actions impossibles, et une
suite qui échoue de façon imprévisible est relancée plutôt que lue. Un mode chaos séparé est un
ajout ultérieur raisonnable et ne devrait pas être le défaut.

**Enregistrer et rejouer du trafic réel de fournisseur.** L'approche la plus fidèle
disponible, et elle échoue sur la disponibilité : enregistrer exige des comptes que personne
n'a, et les cas de défaillance sont exactement ceux qui ne peuvent pas être provoqués pour être
enregistrés. Cela intégrerait aussi le trafic réel d'un marchand dans un dépôt public.

**Aucune simulation, et tester contre des bacs à sable.** Le statu quo de la plupart des
intégrations, et la chose que [ADR-0001](0001-architecture-and-scope.md) rejette.
L'accès aux bacs à sable est inégal, et chaque bac à sable est non déterministe et
incapable de produire une défaillance à la demande, c'est-à-dire qu'ils ne peuvent pas
tester les parties d'une intégration de paiement qui tournent mal.

## Questions non résolues

**Si les fournisseurs simulés devraient parler des API distinctes en forme de fournisseur.**
§3.5. Des formes distinctes font des adaptateurs testés de vrais adaptateurs ; une forme
commune divise la surface par deux et teste moins. Les formes seraient inventées dans les deux
cas, ce qui est l'argument qui l'a emporté jusqu'ici.

**Comment l'ensemble de scénarios reste honnête.** Le §8.4 admet que la liste vient du
raisonnement propre à la spécification plutôt que d'une observation. La première intégration
d'un vrai fournisseur trouvera des comportements que personne n'a écrits, et il n'y a pas
encore de mécanisme pour les réinjecter dans le §4.3.

**Si la simulation devrait modéliser un fournisseur qui ment.** Plusieurs règles existent
parce qu'un fournisseur pourrait rapporter une transition impossible, et
[ADR-0003 §2.1](0003-payment-lifecycle.md) exige d'une passerelle qu'elle traite cela comme
une erreur du fournisseur plutôt que de l'appliquer. Rien ne le provoque actuellement. Un
scénario `LIES` rapportant une transition hors d'un état terminal testerait le seul invariant
dont tout le reste dépend.

**Si la surface de contrôle devrait pouvoir revenir en arrière.** Avancer le temps est
spécifié ; défaire une transition ne l'est pas, et cela permettrait à un seul test d'exercer
plusieurs dénouements depuis un même paiement. Cela permettrait aussi à une simulation de
quitter un état terminal, qui est le comportement que toute la spécification interdit, et le
construire enseignerait peut-être la mauvaise chose.

## Références

Citations complètes dans [`references.md`](references.md). Cette ADR est Informational,
donc chaque référence est informative.

`BRH-121` section 5 et `BRH-126` section 3 t), les deux audits triennaux que
[ADR-0015](0015-conformance-levels-and-suite.md) sert et que cette simulation rend
exécutables. `RFC9421` pour la signature que le fournisseur `mock_alpha` produit et que
`mock_beta` ne produit pas. `CPMI-PAFI-2020` p. 54, encadré R, pour les ensembles de capacités
inégaux entre déploiements africains réels sur lesquels la flotte de fournisseurs du §3 est
modelée.

## Implémentation de référence

Aucune pour l'instant. [ADR-0001](0001-architecture-and-scope.md) planifie la simulation à
côté de la passerelle.

## Errata

Aucun.
