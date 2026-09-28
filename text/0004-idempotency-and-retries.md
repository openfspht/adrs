# ADR-0004 : Idempotence et sémantique des reprises

- Voie : Standards
- Statut : Brouillon
- Créée : 2026-08-17
- Dépend de : ADR-0001, ADR-0002, ADR-0003

## Résumé

Cette ADR spécifie comment un client peut rejouer sans danger une requête qui a peut-être
déjà été exécutée, et ce qu'une passerelle doit faire lorsqu'elle en reçoit une.

Elle rend `Idempotency-Key` obligatoire sur toute requête modifiant l'état, définit
exactement quand une requête répétée est un rejeu et quand elle est un conflit, et résout
l'interaction entre la clé d'idempotence et la référence marchande laissée ouverte par
[ADR-0002 §6.2.5](0002-core-data-model.md). Les deux mécanismes protègent des choses
différentes sur des échelles de temps différentes, et une implémentation correcte a besoin
des deux.

## Motivation

Un client envoie une requête de création de paiement. La connexion tombe avant qu'une
réponse n'arrive.

Le client ne peut pas savoir ce qui s'est passé. La requête n'a peut-être jamais atteint la
passerelle. Elle l'a peut-être atteinte, a été exécutée, et la réponse s'est perdue au
retour. Du point de vue du client ces cas sont indiscernables, et les deux actions
disponibles sont toutes deux fausses :

- **Rejouer**, et si la première tentative a réussi, débiter le payeur deux fois.
- **Ne pas rejouer**, et si la première tentative n'est jamais arrivée, perdre le paiement
  sans trace.

Il n'existe pas de troisième option accessible au client seul, parce que l'information
manquante est sur le serveur. Ce n'est pas un cas limite à traiter défensivement : c'est le
comportement normal des réseaux, et cela survient sur une fraction du trafic de toute
intégration réelle.

L'idempotence déplace la décision vers la partie qui détient l'information. Le client
attache une clé identifiant *l'opération qu'il entend faire*, plutôt que la requête qu'il
envoie, et peut ensuite rejouer librement : la passerelle exécute l'opération au plus une
fois et retourne la même réponse à chaque fois. L'incertitude du client cesse d'être un
problème de correction.

C'est pourquoi le mécanisme est spécifié avant tout point d'accès. Une API dont les points
d'accès auraient été conçus d'abord et rendus idempotents ensuite a une décision fine à
prendre pour chacun, et en ratera certains.

## Hors périmètre

- **Aucune définition de point d'accès.** Quelles opérations existent relève de l'ADR sur
  l'API HTTP. Cette ADR spécifie ce que l'idempotence signifie pour toutes.
- **Aucun format d'erreur.** La structure des problem details et les URI de type relèvent
  de l'ADR sur la taxonomie des erreurs. Les *conditions* d'erreur sont nommées ici ; leur
  représentation ne l'est pas.
- **Aucune transaction distribuée.** L'idempotence garantit une exécution au plus une fois
  d'une opération unique. Elle ne coordonne pas plusieurs opérations et n'offre aucun
  retour arrière.
- **Aucune livraison exactement-une-fois des événements.** La sémantique de livraison des
  webhooks est spécifiée dans [ADR-0008](0008-webhooks-and-event-delivery.md). Cette ADR
  concerne les requêtes qu'un client émet, pas les événements qu'une passerelle envoie.

## Spécification

Les mots-clés MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
MAY et OPTIONAL sont à interpréter comme décrit dans les RFC 2119 et RFC 8174, lorsque, et
seulement lorsque, ils apparaissent en capitales.

### 1. Périmètre

**1.1.** Toute requête qui crée ou modifie un état (tout `POST`, `PATCH` et `DELETE` de
cette spécification) est une **opération idempotente** et relève de cette ADR, sauf si une
ADR de la voie Standards exempte une opération nommée au titre du §1.5.

**1.2.** `GET` et `HEAD` sont sûrs, ne changent rien, et sont hors de cette ADR. Un client
MAY les rejouer librement.

**1.3.** Un client MUST envoyer un en-tête `Idempotency-Key` sur toute requête relevant du
§1.1. Une passerelle MUST rejeter une requête relevant du §1.1 qui ne porte pas de clé, et
MUST NOT l'exécuter.

**1.4.** La clé est REQUIRED plutôt qu'OPTIONAL, et c'est un écart délibéré à la pratique
courante. Un mécanisme de sûreté optionnel est absent quand le client est le moins soigneux,
c'est-à-dire quand il en avait le plus besoin. Le rendre obligatoire convertit un péril
silencieux de correction en un `400` dès le premier essai du client.

**1.5. Exemptions.** Une ADR de la voie Standards MAY exempter une opération nommée du
§1.3. Elle MUST justifier l'exemption sur **les deux** motifs suivants ; une opération ne
satisfaisant qu'un seul n'est pas exemptée :

- **(a)** L'opération est naturellement répétable : l'exécuter deux fois est inoffensif.
- **(b)** Retourner une réponse enregistrée au lieu de l'exécuter serait *incorrect*, et
  non simplement inutile.

Le motif (b) est ce qui garde l'exemption étroite, et c'est celui qu'on oublie facilement.
L'idempotence fonctionne en remplaçant l'exécution par une réponse enregistrée antérieurement.
Là où l'objet même de l'appelant est d'obtenir une réponse *fraîche*, cette substitution ne le
protège pas, elle défait sa requête. Une telle opération ne gagne rien à une clé, et une clé
qui doit être différente à chaque appel n'apporte aucune garantie tout en en ayant
l'apparence.

**1.6.** Une opération exemptée MUST NOT exiger `Idempotency-Key`. Une passerelle MUST NOT
enregistrer de réponse pour une telle opération, et MUST ignorer l'en-tête si un client
l'envoie tout de même.

### 2. La clé

**2.1.** `Idempotency-Key` porte un `IdempotencyKey` tel que défini en
[ADR-0002 §6.4](0002-core-data-model.md) : 1 à 255 points de code correspondant à
`^[A-Za-z0-9_-]+$`.

**2.2.** Les clients SHOULD la générer comme un UUID (RFC 9562) ou à partir d'au moins 128
bits d'aléa cryptographique. Une clé dérivée de données métier (un numéro de facture, un
horodatage) risque de collisionner entre opérations sans rapport, et le §3.4 transforme une
collision en échec dur.

**2.3. Portée.** Un enregistrement d'idempotence a pour portée le triplet du **principal
authentifié** ([ADR-0009 §5.1](0009-authentication-and-credentials.md)), de
l'**opération d'API** et de la **clé**. Deux requêtes partagent un enregistrement seulement
si les trois correspondent.

**2.4.** Restreindre la portée au principal authentifié est une exigence de sécurité, pas
une commodité d'organisation. Sans cela, un appelant présentant la clé d'une autre partie
recevrait la réponse enregistrée de cette partie, transformant l'idempotence en oracle de
divulgation. Une passerelle MUST NOT servir une réponse enregistrée à un principal autre que
celui qui a créé l'enregistrement. Voir *Considérations de sécurité* ci-dessous.

**2.5.** Une clé réutilisée entre deux opérations différentes MUST être rejetée au titre du
§3.4. Les clés ne sont pas cloisonnées par nom de domaine côté client, c'est donc la
passerelle qui fait respecter la distinction.

### 3. Sémantique

Soit *K* la clé, *P* le principal authentifié, *O* l'opération, et *F* l'empreinte de
requête définie au §4.

**3.1. Première requête.** Lorsqu'aucun enregistrement n'existe pour (*P*, *O*, *K*), la
passerelle exécute l'opération normalement et, en atteignant un dénouement déterminé (§5),
enregistre *F* avec le statut et le corps de la réponse.

**3.2. Rejeu.** Lorsqu'un enregistrement existe et que l'empreinte entrante égale le *F*
enregistré, la passerelle MUST NOT exécuter l'opération à nouveau. Elle MUST retourner le
statut et le corps enregistrés, et MUST inclure l'en-tête `Idempotent-Replay: true`.

**3.3.** La réponse rejouée MUST être identique octet pour octet au corps enregistré. En
particulier, une création de paiement rejouée retourne le paiement tel qu'il était à
l'enregistrement, ce qui peut montrer un état depuis dépassé. C'est correct : la réponse
répond à *ce que cette requête a fait*, non à *ce qui est vrai maintenant*. Un client ayant
besoin de l'état courant émet un `GET`, et le §8.3 l'y oblige.

**3.4. Conflit.** Lorsqu'un enregistrement existe et que l'empreinte entrante diffère du *F*
enregistré, la passerelle MUST rejeter la requête et MUST NOT l'exécuter. La condition est
`idempotency_key_reused`, portée en `422`
([ADR-0005 §4.3](0005-error-taxonomy.md) donne le raisonnement sur le statut).

C'est presque toujours un défaut du client : une clé réutilisée entre opérations distinctes,
ou une boucle de reprise qui a muté la charge utile entre deux tentatives. La rejeter
bruyamment est la seule réponse sûre : les alternatives sont d'exécuter une seconde opération,
différente, sous une clé dont le client croit qu'elle le protège, ou de retourner le résultat
de la première opération à une requête qui demandait autre chose. Les deux font la mauvaise
chose avec de l'argent, et sans le dire.

**3.5. En cours.** Lorsqu'un enregistrement existe pour (*P*, *O*, *K*) mais que la première
requête n'a pas encore atteint de dénouement déterminé, la passerelle MUST NOT exécuter
l'opération concurremment. Elle MUST soit retenir la seconde requête jusqu'à la résolution
de la première, soit la rejeter avec la condition rejouable
`idempotency_request_in_progress` et un en-tête `Retry-After`.

**3.6.** Le §3.5 est une exigence de correction, pas de performance. Un client dont la
première tentative a semblé se figer rejouera couramment pendant que l'originale tourne
encore ; une passerelle qui admet les deux concurremment n'a fourni aucune protection,
exactement dans le scénario pour lequel le mécanisme existe. Les implémentations MUST rendre
mutuellement exclusives la création de l'enregistrement et l'exécution de l'opération
(insertion conditionnelle, verrou consultatif, ou équivalent) et MUST NOT s'appuyer sur un
contrôle lecture-puis-écriture, qui comporte une course.

### 4. Empreinte de requête

**4.1.** L'empreinte *F* est le condensé SHA-256 du corps de la requête canonicalisé selon
la RFC 8785, le JSON Canonicalization Scheme.

**4.2.** La canonicalisation est spécifiée plutôt que le hachage des octets bruts afin qu'un
client qui resérialise sa charge utile entre deux tentatives (ordre de clés différent,
espaces différents, autre bibliothèque JSON) ne soit pas puni d'un conflit fallacieux pour
avoir envoyé une requête sémantiquement identique.

**4.3.** L'empreinte couvre le corps de la requête seulement. Les en-têtes, les paramètres
de requête et le chemin sont exclus : le chemin et l'opération font déjà partie de la portée
de l'enregistrement au titre du §2.3, et les en-têtes varient légitimement entre reprises.

**4.4.** Une requête au corps vide a pour empreinte celle de l'objet JSON vide.

### 5. Ce qui est enregistré

**5.1.** Une passerelle MUST enregistrer une réponse seulement lorsque l'opération a atteint
un **dénouement déterminé**, c'est-à-dire un dénouement où la passerelle sait ce qui s'est
passé ou non.

**5.2.** Déterminé, donc enregistré :

- Une réponse de succès, y compris une réponse rapportant un paiement `failed` (voir
  [ADR-0003 §7.1](0003-payment-lifecycle.md)).
- Une erreur client causée par la requête elle-même : échec de validation, champ inconnu,
  conflit de référence. Rejouer une telle requête inchangée échouera toujours de la même
  façon, et l'enregistrer le rend explicite.

**5.3.** Indéterminé, donc MUST NOT être enregistré :

- Toute erreur interne où la passerelle ne peut établir si l'opération a pris effet.
- Une expiration ou un échec de transport côté fournisseur laissant l'état du fournisseur
  inconnu.
- Un plantage avant que le dénouement n'ait été persisté.
- Une réponse `409 idempotency-request-in-progress` au titre du §3.5.

**5.3.1.** Le dernier cas est facile à rater, parce qu'un `409` est une erreur client par sa
classe de statut et que le §5.2 enregistre les erreurs client. Il n'est pourtant pas causé
par la requête : il rapporte qu'une tentative *concurrente* est encore en cours.
L'enregistrer rejouerait le conflit pendant toute la vie de l'enregistrement, bloquant
définitivement l'opération même que la clé protégeait, et contredisant
[ADR-0005 §9.4.2](0005-error-taxonomy.md), qui en fait le seul conflit rejouable.

**5.4.** Le §5.3 existe parce qu'enregistrer un échec indéterminé priverait définitivement
le client de la reprise qui est son seul moyen de lever l'ambiguïté. Là où aucun
enregistrement n'est écrit, une reprise est une première requête au titre du §3.1, et le §7
régit ce que la passerelle doit faire avant de toucher à nouveau au fournisseur.

**5.5.** Une réponse enregistrée est immuable. Elle n'est jamais mise à jour pour refléter un
état ultérieur.

### 6. Rétention, et son interaction avec `Reference`

**6.1.** Une passerelle MUST conserver les enregistrements d'idempotence au moins
**24 heures** à compter de leur création, MUST documenter sa durée de rétention réelle, et
SHOULD les conserver **7 jours**.

**6.2.** Après expiration d'un enregistrement, une requête portant la même clé est une
première requête au titre du §3.1. La rétention borne donc la durée de la protection contre
le rejeu, et c'est exactement la brèche que
[ADR-0002 §6.2.5](0002-core-data-model.md) avait laissée ouverte.

**6.3.** La brèche est fermée par la référence marchande, qui n'expire jamais. Les deux
mécanismes sont complémentaires :

| Mécanisme | Protège | Durée de vie | En cas de répétition |
|---|---|---|---|
| `Idempotency-Key` | la **requête** | la fenêtre de rétention | rejoue la réponse d'origine |
| `Reference` | le **paiement** | permanente | rejette avec un conflit de référence |

**6.4.** Concrètement, pour une création de paiement :

| Situation | Dénouement |
|---|---|
| Même clé, même corps, dans la rétention | Rejeu de la réponse enregistrée (§3.2). |
| Même clé, corps différent | `idempotency_key_reused` (§3.4). |
| Clé expirée, même corps, même référence | Conflit de référence. **Pas de paiement en double.** |
| Clé différente, même référence | Conflit de référence. **Pas de paiement en double.** |
| Clé différente, référence différente | Un nouveau paiement, distinct. Correct : deux achats identiques sont deux paiements. |

**6.5.** La dernière ligne est la raison pour laquelle la déduplication ne peut pas reposer
sur la seule charge utile. Un client qui achète deux fois le même article au même prix envoie
deux requêtes identiques octet pour octet, et toutes deux doivent réussir. Seules une clé
explicite ou une référence explicite peuvent distinguer une répétition intentionnelle d'une
répétition accidentelle, parce que la différence n'existe que dans l'intention du client.

**6.6.** Une passerelle MUST NOT s'appuyer sur les enregistrements d'idempotence pour une
prévention permanente des doublons, et MUST faire respecter l'unicité de la référence
([ADR-0002 §6.2.2](0002-core-data-model.md)) indépendamment d'eux.

### 7. Idempotence vis-à-vis du fournisseur

**7.1.** Les garanties de cette ADR couvrent la passerelle. Elles ne s'étendent pas
automatiquement au fournisseur situé derrière elle, et une passerelle qui rejoue sans danger
vers son client tout en renvoyant aveuglément vers son fournisseur a déplacé le double débit
d'une couche plus bas au lieu de l'empêcher.

**7.2.** Avant de retenter une opération fournisseur dont la tentative précédente s'est
terminée de façon indéterminée (§5.3), une passerelle MUST d'abord tenter d'établir le
dénouement de cette tentative en relisant l'état faisant autorité chez le fournisseur, comme
l'exige [ADR-0003 §6.1](0003-payment-lifecycle.md).

**7.3.** Là où le fournisseur offre son propre mécanisme d'idempotence ou de déduplication,
la passerelle MUST l'utiliser, indexé sur une valeur dérivée de façon déterministe de la
`reference` du paiement, afin que le même paiement logique présente toujours la même valeur.

**7.4.** Là où le fournisseur n'offre ni mécanisme d'idempotence ni recherche par référence
marchande, la passerelle MUST NOT renvoyer automatiquement une opération indéterminée. Elle
MUST laisser le paiement `pending` et faire remonter la situation à l'exploitant, jusqu'à ce
qu'une source d'[ADR-0003 §6.5](0003-payment-lifecycle.md) établisse le dénouement,
l'attestation de l'exploitant comprise. Une reprise automatique contre un fournisseur qui ne
sait ni dédupliquer ni être interrogé est un double débit avec des étapes en plus.

**7.5.** Une passerelle MUST documenter, par adaptateur de fournisseur, lequel du §7.3 ou du
§7.4 s'applique. C'est une information matérielle pour qui la déploie.

### 8. Obligations du client

**8.1.** Un client MUST générer une clé par opération logique et MUST réutiliser cette même
clé pour chaque reprise de cette opération. Générer une clé neuve à la reprise défait
entièrement le mécanisme, et c'est la façon la plus courante dont les intégrations se
trompent.

**8.2.** Un client MUST NOT rejouer une réponse `4xx` autre que les conditions rejouables
nommées au §3.5 et la limitation de débit. Un échec de validation ne deviendra pas valide.

**8.3.** Après toute séquence de reprises, un client MUST établir le dénouement de
l'opération en lisant la ressource, et MUST NOT le déduire de la dernière réponse reçue. Le
§3.3 implique qu'une réponse rejouée peut être périmée.

**8.4.** Les clients SHOULD rejouer avec un retrait exponentiel et une gigue aléatoire, et
MUST respecter `Retry-After` lorsqu'il est présent. Des reprises synchronisées après une
panne de fournisseur sont la façon dont un système en cours de rétablissement est mis à terre
une seconde fois.

**8.5.** Un client SHOULD persister la clé à côté de l'opération qu'elle identifie **avant**
d'émettre la requête. Une clé gardée seulement en mémoire est perdue précisément quand le
processus plante en pleine requête, qui est le cas auquel l'idempotence existe pour survivre.

### 9. Rapport aux travaux en cours à l'IETF

**9.1.** Le mécanisme spécifié ici n'est pas inventé. Le groupe de travail HTTPAPI de l'IETF
normalise le même en-tête, et cette ADR le suit partout où il a pris position [IETF-IDEM].

**9.2.** Les points d'accord sont la substance du mécanisme, et ils sont listés pour qu'un
implémenteur puisse constater l'alignement plutôt que le croire sur parole.

| Cette ADR | `IETF-IDEM` |
|---|---|
| La clé est générée par le client et identifie une reprise de la même requête (§1) | « An idempotency key is a unique value generated by the client which the resource uses to recognize subsequent retries of the same request » (s. 2) |
| Elle voyage dans un en-tête HTTP, pas dans le corps ([ADR-0002 §6.4.1](0002-core-data-model.md)) | `Idempotency-Key` est un champ Structured Header dont la valeur est une String (s. 2.1) |
| Un UUID est RECOMMENDED ([ADR-0002 §6.4.1](0002-core-data-model.md)) | Les UUID sont cités comme l'exemple d'une clé forte, et les clés faibles sont un risque de sécurité (s. 5) |
| Un doublon achevé est rejoué, succès ou échec (§3.2) | « The resource SHOULD respond with the result of the previously completed operation, success or an error » (s. 2.6) |
| Un doublon concurrent est rejeté comme conflit (§3.5) | « The resource SHOULD respond with a resource conflict error » (s. 2.6), `409` (s. 2.7) |
| Une clé réutilisée avec un corps différent est rejetée en `422` (§3.4) | `422`, « Idempotency Key MUST not be reused across different payloads of this operation » (s. 2.7) |
| La fenêtre de rétention est bornée et publiée (§6.1) | « The resource SHOULD define such expiration policy and publish it in the documentation » (s. 2.3) |

**9.3.** Là où cette ADR va plus loin, c'est parce que le paiement n'est pas un problème
d'API générale. Le draft ne dit rien sur le cloisonnement des enregistrements par principal
authentifié, dont le §2.4 fait une exigence de sécurité ; rien sur la protection à deux
couches où la `Reference` du marchand survit à la clé
([ADR-0002 §6.2](0002-core-data-model.md)) ; et rien sur ce qu'une passerelle peut faire
quand le fournisseur derrière elle n'offre ni idempotence ni recherche, ce à quoi le §7.4
répond en refusant de renvoyer.

**9.4.** Un Internet-Draft n'est pas une norme publiée et peut changer. Une version ultérieure
qui contredirait cette ADR est une raison d'ouvrir une ADR ici, pas une raison de diverger
sans le dire. Les divergences qui existent aujourd'hui sont les ajouts du §9.3, et il n'y a
aucune contradiction.

## Compatibilité

Nouvelle spécification. Rien à casser.

Le §1.3 rend l'en-tête obligatoire dès la première version. Introduire cette exigence plus
tard casserait tout client déployé, elle est donc imposée maintenant, avant qu'il n'y en ait.

Les conditions d'erreur nommées aux §3.4 et §3.5 sont des marque-places pour l'ADR sur la
taxonomie des erreurs, qui leur assignera des URI de type et des codes de statut. Leurs
*conditions* sont normatives ici ; leur représentation ne l'est pas.

## Considérations de sécurité

**Les enregistrements sont cloisonnés par appelant.** Le §2.4 est la disposition de sécurité
la plus importante de cette ADR. Un magasin d'idempotence non partitionné par principal
authentifié permet à tout appelant qui devine ou obtient une clé de récupérer la réponse
enregistrée d'une autre partie, numéros de téléphone du payeur et montants compris. Les
implémentations MUST partitionner le magasin, et MUST NOT traiter la clé seule comme
identifiant de recherche.

**Les clés ne sont pas des secrets, et MUST NOT être traitées comme des capacités.** Le §2.4
les rend inutilisables par un principal différent ; rien d'autre dans une clé ne confère
d'autorité. Une clé apparaissant dans un journal n'est pas une compromission d'identifiant
secret.

**Les corps enregistrés contiennent des données personnelles.** Une réponse stockée contient
ce que contenait l'originale : numéros de téléphone, références, métadonnées. Le magasin
d'idempotence hérite donc des exigences de confidentialité des ressources elles-mêmes, et sa
rétention (§6.1) prolonge la durée de vie de ces données. Une rétention courte est un
contrôle de protection de la vie privée autant qu'un contrôle de stockage.

**Épuisement du stockage.** Un attaquant envoyant beaucoup de requêtes avec des clés neuves
fait croître le magasin sans borne. Les passerelles MUST limiter le débit de création de
requêtes par principal et SHOULD plafonner les enregistrements stockés par principal, en
rejetant les requêtes supplémentaires plutôt qu'en évinçant des enregistrements : l'éviction
retirerait la protection contre le rejeu au trafic légitime sans que rien ne l'indique.

**Collisions d'empreintes.** SHA-256 rend une collision accidentelle négligeable, et une
collision délibérée exigerait une attaque en préimage contre une valeur que l'attaquant ne
peut pas exploiter utilement au titre du §2.4.

**Divulgation temporelle.** La condition `idempotency_request_in_progress` révèle qu'une clé
est en usage. Le cloisonnement par principal (§2.3) fait qu'elle ne le révèle qu'à la partie
qui l'a créée.

**Les échecs indéterminés ne sont pas enregistrés.** Le §5.3 est aussi une propriété de
sécurité : enregistrer un échec que la passerelle ne comprend pas laisserait une panne
passagère bloquer définitivement une opération légitime, ce qui est un déni de service
déclenchable par quiconque peut induire une erreur.

## Considérations réglementaires

**Les débits en double sont une affaire de protection du consommateur**, pas seulement un
défaut d'ingénierie. Un payeur débité deux fois pour un achat a subi une perte causée par la
conception du système. L'idempotence obligatoire (§1.3), combinée à l'unicité permanente de
la référence (§6.6), fait qu'un déploiement conforme ne peut pas produire de doublon par la
voie ordinaire des reprises.

**Auditabilité des rejeux.** L'en-tête `Idempotent-Replay: true` (§3.2) rend les rejeux
distinguables des exécutions originales dans les journaux, de sorte qu'un examinateur peut
établir combien de fois une opération a été demandée et confirmer qu'elle a été exécutée une
fois.

**Honnêteté au niveau du fournisseur.** L'exigence du §7.4 qu'une opération non résoluble
soit laissée `pending` et escaladée, plutôt que rejouée aveuglément, fait que les
enregistrements du déploiement reflètent une incertitude réelle au lieu de la dissimuler
derrière une reprise automatique.

**Conservation.** Le §6.1 pose un plancher, pas un plafond, et les corps enregistrés peuvent
contenir des données personnelles. Les opérateurs soumis à des règles de protection des
données ou de tenue de registres devraient fixer la rétention pour satisfaire la plus stricte
des deux ; le plancher de la spécification est un minimum de correction et n'est pas offert
comme guide de conformité.

## Alternatives envisagées

**Une clé d'idempotence optionnelle.** L'approche courante parmi les API de paiement
établies, et plus douce pour un client qui débute. Rejetée au titre du §1.4 : une protection
optionnelle est omise exactement par les clients qui en ont le plus besoin, et le défaut qui
en résulte apparaît en production plutôt qu'en développement.

**Déduplication sur la seule charge utile**, sans clé. D'une simplicité séduisante : hacher le
corps, rejeter une répétition dans une certaine fenêtre. Rejetée au titre du §6.5 : deux
requêtes légitimes identiques sont indiscernables d'une requête dupliquée par leur contenu, ce
qui fusionne sans alerte le second achat d'un client dans le premier. L'intention du client
n'est pas dans la charge utile.

**Utiliser `Reference` comme clé d'idempotence**, pour éviter un second mécanisme. Réellement
tentant, et cela apporte bien la sûreté essentielle : l'unicité de la référence suffit à
empêcher un paiement en double. Rejeté pour deux raisons. Premièrement, une reprise recevrait
un conflit de référence plutôt que la réponse d'origine, de sorte que tout client aurait
encore besoin d'une logique de récupération : le mécanisme préviendrait le dommage sans
supprimer la complexité. Deuxièmement, `Reference` est une propriété d'un paiement, et
l'idempotence doit protéger des opérations qui ne créent aucun paiement et ne portent aucune
référence. Garder les mécanismes séparés est ce qui permet la protection à deux couches du
§6.3, avec des durées de vie différentes.

**Une déduplication à fenêtre temporelle fixe**, rejeter les répétitions dans les *n*
minutes. Rejetée comme arbitraire : toute fenêtre est trop courte pour un client qui rejoue
après une panne et trop longue pour une répétition rapide légitime, et elle hérite à nouveau
du problème d'intention ci-dessus.

**Hacher les octets bruts de la requête** au lieu de la forme canonique RFC 8785. Plus
simple, sans dépendance à une canonicalisation. Rejeté au titre du §4.2 : un client qui
resérialise sa charge utile entre deux tentatives recevrait un conflit pour une requête
sémantiquement identique, ce qui entraîne les implémenteurs à contourner le mécanisme.

**Retenir plutôt que rejeter les rejeux concurrents.** Le §3.5 permet les deux. Aucun n'est
imposé parce que le bon choix dépend du déploiement : retenir donne aux clients une
expérience plus simple, rejeter protège une passerelle sous charge de l'accumulation de
connexions retenues.

## Questions non résolues

1. **Le plancher de rétention.** Vingt-quatre heures est défendable et court. Sept jours
   couvriraient une panne de week-end, au prix proportionnel en données personnelles
   stockées. Le bon chiffre dépend d'une réalité opérationnelle que personne n'a encore.
2. **Si le test d'exemption du §1.5 est assez serré.** La règle uniforme du §1.1 était à
   l'origine absolue ; le test en deux parties a été ajouté une fois que le premier ensemble
   de points d'accès a montré un cas réel où une clé produit des résultats périmés plutôt que
   de la sûreté. Deux motifs sont délibérément exigeants, mais le test n'a été appliqué
   qu'une fois, et un point de donnée n'est pas une preuve qu'il trace la ligne au bon
   endroit.
3. **Retenir ou rejeter en cas de rejeu concurrent.** Laisser le §3.5 ouvert est une
   couverture. La suite de conformité devra accepter les deux comportements, ce qui affaiblit
   ce que la conformité démontre.
4. **Adaptateurs de fournisseurs sans idempotence ni recherche.** Le §7.4 exige une
   résolution manuelle, ce qui pourrait s'avérer impraticable si un fournisseur réellement
   utilisé tombe dans cette catégorie. Si c'est le cas, la réponse honnête est de documenter
   la limitation plutôt que de l'automatiser, mais la charge opérationnelle devrait être
   mesurée avant d'être imposée.
5. **Si les réponses rejouées devraient porter la date d'origine.** Le §3.3 exige un corps
   identique octet pour octet ; savoir si `Date` et les en-têtes similaires devraient
   refléter l'exécution d'origine ou le rejeu n'est pas spécifié, et importe aux clients qui
   les journalisent.

## Références

Citations complètes dans [`references.md`](references.md).

**Normatives.** `RFC9110` pour la sémantique HTTP, `RFC9562` pour l'UUID recommandé comme
clé, `RFC8785` pour la canonicalisation utilisée dans l'empreinte, `RFC2119` et `RFC8174`
pour les mots-clés d'exigence.

**Informatives.** `IETF-IDEM`, les travaux en cours à l'IETF sur le même en-tête, examinés au
§9. Ils sont informatifs et non normatifs parce qu'il s'agit d'un draft : c'est à cette ADR
qu'un implémenteur se conforme, et le §9 consigne que les deux s'accordent.

## Implémentation de référence

Aucune pour l'instant.

## Errata

Aucun.
