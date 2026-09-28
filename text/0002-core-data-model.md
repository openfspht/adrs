# ADR-0002 : Modèle de données fondamental

- Voie : Standards
- Statut : Brouillon
- Créée : 2026-08-17
- Dépend de : ADR-0001

## Résumé

Cette ADR spécifie les types primitifs à partir desquels toute ressource OpenFSP est
construite : montants monétaires, devises, numéros de téléphone, identifiants,
horodatages, métadonnées, et les conventions JSON qui les gouvernent tous.

Elle ne définit ni point d'accès ni ressource. Elle existe parce que chaque ADR ultérieure de
la voie Standards utilisera ces types, et que chacun doit signifier exactement la même chose
partout où il apparaît. Un montant qui est un entier à un endroit et une chaîne décimale à un
autre oblige chaque client à deviner lequel des deux il reçoit.

## Motivation

La plupart des échecs d'interopérabilité dans les systèmes de paiement ne sont pas des
échecs d'architecture. Ce sont des échecs de primitives : une différence d'arrondi, une
hypothèse de fuseau horaire, un numéro de téléphone au format local, un identifiant sur
lequel deux systèmes ne s'accordent pas.

Ces défauts partagent une forme : chacun est invisible dans le cas courant et coûteux dans
le cas rare. Un montant monétaire porté par un nombre à virgule flottante est correct pour
presque toutes les transactions et faux pour celle qui tombe sur une valeur que le format
ne peut pas représenter. Un horodatage sans décalage est sans ambiguïté jusqu'au changement
d'heure. Un numéro de téléphone écrit comme on le prononce va bien jusqu'à ce que deux pays
l'écrivent de la même façon.

Spécifier les primitives en premier, et les spécifier étroitement, élimine une classe
entière de défauts avant qu'aucun point d'accès n'existe. C'est aussi le moment le moins
coûteux pour le faire : changer la représentation de la monnaie après que trois ADR en
dépendent est une rupture de compatibilité pour les trois.

## Hors périmètre

- **Aucune ressource.** `Payment`, son cycle de vie et ses points d'accès relèvent d'ADR
  ultérieures. Cette ADR définit le vocabulaire dans lequel elles seront écrites.
- **Aucune conversion de devise.** Pas de taux de change, pas de conversion implicite, pas
  d'arithmétique multi-devises. Une ADR ultérieure pourra traiter le change ; celle-ci rend
  impossible de le faire par accident.
- **Aucun modèle d'identité au-delà du numéro de téléphone.** Savoir si OpenFSP modélise
  plus richement l'identité du payeur est une question ouverte de
  [ADR-0001](0001-architecture-and-scope.md#questions-non-résolues) et n'est pas tranchée
  ici.
- **Aucune sémantique d'idempotence.** La syntaxe du champ `Idempotency-Key` est
  contrainte ici par souci de cohérence ; ce qu'il *fait* est spécifié par sa propre ADR.
- **Aucune décision sur les devises qu'un déploiement prend en charge.** Cette ADR rend
  représentable n'importe quelle devise ISO 4217. Lesquelles une passerelle donnée accepte
  est une capacité, découverte à l'exécution, et non une propriété du modèle de données.

## Spécification

Les mots-clés MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
MAY et OPTIONAL sont à interpréter comme décrit dans les RFC 2119 et RFC 8174, lorsque, et
seulement lorsque, ils apparaissent en capitales.

Les types ci-dessous ne sont pas inventés de rien. Leur forme suit ISO 20022, qu'OpenFSP
traite comme un dictionnaire et non comme un transport
([ADR-0001, *Standards this builds on*](0001-architecture-and-scope.md)) : des montants
portant leur devise plutôt que la présupposant, des parties identifiées indépendamment de
l'institution qui les détient, et une référence choisie par le marchand qui parcourt toute
la chaîne sans altération, à la manière d'un identifiant de bout en bout. Le JSON ci-dessous
n'est pas de l'ISO 20022 et ne prétend pas l'être. La correspondance, et chaque endroit où
elle perd de l'information, relève de
[ADR-0010](0010-iso-20022-semantic-correspondence.md). En cas de désaccord entre les
deux, celle-ci gouverne le fil et celle-là gouverne la lecture qu'on en fait.

### 1. Synthèse des types

| Type | Forme JSON | Exemple |
|---|---|---|
| `Money` | objet | `{"amount": 125000, "currency": "HTG"}` |
| `Currency` | chaîne, ISO 4217 alpha-3 | `"HTG"` |
| `PhoneNumber` | chaîne, E.164 | `"+50934567890"` |
| `ResourceId` | chaîne opaque | `"pay_01J9ZK3QF8XN2M7VYB4C6D8E0G"` |
| `Reference` | chaîne choisie par le marchand | `"INV-2026-00184"` |
| `ProviderReference` | chaîne opaque | `"MC-8837291"` |
| `Timestamp` | chaîne, RFC 3339 UTC | `"2026-08-17T14:32:07.412Z"` |
| `Fee` | objet | `{"amount": {"amount": 1250, "currency": "HTG"}, "bearer": "merchant"}` |
| `Metadata` | objet de chaîne vers chaîne | `{"order_id": "184"}` |

### 2. Conventions JSON

**2.1.** Tous les corps de requête et de réponse sont en JSON (RFC 8259), encodés en UTF-8.
Aucun autre encodage n'est permis.

**2.2.** Les noms de champs utilisent `lower_snake_case` et sont stables : un champ n'est
jamais renommé à l'intérieur d'une version majeure.

**2.3. Champs inconnus dans les réponses.** Un client MUST ignorer les champs qu'il ne
reconnaît pas, et MUST NOT traiter leur présence comme une erreur. C'est ce qui permet à une
version mineure d'ajouter un champ sans casser les clients déployés.

**2.4. Champs inconnus dans les requêtes.** Un serveur MUST rejeter un corps de requête
contenant un champ qu'il ne reconnaît pas, avec un `400` et un problem detail identifiant le
champ.

L'asymétrie entre 2.3 et 2.4 est délibérée. La tolérance en sortie achète de la
compatibilité ascendante et ne coûte rien. La tolérance en entrée écarte silencieusement un
champ mal orthographié : et une requête où `amount` a été tapé `amout` n'est pas une requête
malformée, c'est une requête pour un autre montant d'argent. Dans ce domaine, l'échec doit
être bruyant.

**2.5. Absence et null.** Pour un champ OPTIONAL, l'absence et un `null` explicite sont
équivalents et signifient « pas de valeur ». Les implémentations SHOULD omettre le champ
plutôt qu'envoyer `null`. Un champ REQUIRED MUST NOT valoir `null`.

**2.6. Chaînes.** Toutes les chaînes sont Unicode. Les implémentations SHOULD normaliser en
forme de normalisation Unicode C (NFC) avant stockage et comparaison. Chaque limite de
longueur de cette spécification compte des **points de code Unicode**, jamais des octets et
jamais des unités UTF-16.

Le créole haïtien et le français utilisent tous deux des caractères hors ASCII, et une
référence marchande ou une valeur de métadonnée contenant `è` ou `ò` ne doit pas être tronquée
différemment par deux implémentations conformes.

**2.7. Booléens et nombres.** Les booléens sont des booléens JSON, jamais `"true"` ni `1`.
Les nombres sont des nombres JSON, jamais des chaînes, avec pour unique exception qu'il n'y
en a aucune : `Money.amount` est lui aussi un nombre, sous les contraintes du §3.

### 3. Money

**3.1.** Une valeur monétaire est un objet comportant exactement deux champs REQUIRED :

```json
{
  "amount": 125000,
  "currency": "HTG"
}
```

**3.2. `amount`** est un entier exprimé dans les **unités mineures** de sa devise.
L'exemple ci-dessus vaut 1 250,00 HTG.

**3.3.** `amount` MUST être un nombre JSON sans partie fractionnaire et sans exposant.
`1250.00`, `1.25e3` et `"125000"` sont tous invalides.

**3.4.** `amount` MUST se situer dans l'intervalle inclusif −(2⁵³ − 1) à 2⁵³ − 1.

Cette borne n'est pas arbitraire. Les nombres JSON sont couramment analysés en valeurs IEEE
754 double précision, qui ne représentent exactement les entiers que jusqu'à 2⁵³ − 1. Un
montant hors de cet intervalle serait silencieusement altéré par un analyseur JSON conforme
dans plusieurs langages très répandus. L'intervalle reste bien plus vaste que toute
transaction plausible : 2⁵³ − 1 unités mineures représentent environ 9 × 10¹³ gourdes.

**3.5.** Une implémentation MUST NOT représenter un montant en interne par une valeur à
virgule flottante binaire ou décimale à quelque moment que ce soit, y compris
transitoirement pendant l'analyse ou l'arithmétique.

**3.6. Signe.** `Money` MAY porter un montant négatif lorsqu'une ADR ultérieure le permet
explicitement : une ligne de remboursement dans un grand livre, par exemple. Sauf mention
contraire d'une telle ADR, un montant dans une requête MUST être strictement supérieur à
zéro. Un paiement de zéro MUST être rejeté plutôt qu'accepté comme opération neutre.

**3.7. Égalité.** Deux valeurs `Money` sont égales si et seulement si leurs `currency` sont
identiques et leurs `amount` égaux. La comparaison entre devises est indéfinie et MUST
échouer plutôt que renvoyer un résultat.

**3.8. Arithmétique.** L'addition et la soustraction ne sont définies qu'entre valeurs de
même devise. Une implémentation MUST NOT effectuer de conversion implicite de devise en
aucune circonstance. Il n'y a aucun arrondi dans cette spécification, parce que les unités
mineures entières rendent l'arrondi inutile : c'est la raison principale de leur choix.

### 4. Devise

**4.1.** Une devise est un code alphabétique ISO 4217 de trois lettres majuscules,
correspondant à `^[A-Z]{3}$`. Les minuscules MUST être rejetées plutôt que normalisées, afin
qu'un défaut du client soit visible par le client plutôt qu'absorbé par le serveur.

**4.2. Unités mineures.** Le nombre de décimales mineures est l'exposant ISO 4217 de la
devise. Une implémentation MUST NOT supposer qu'il vaut 2.

| Devise | Exposant | 1 unité majeure vaut |
|---|---|---|
| HTG, gourde haïtienne | 2 | 100 unités mineures |
| USD, dollar des États-Unis | 2 | 100 unités mineures |
| JPY, yen japonais | 0 | 1 unité mineure |
| KWD, dinar koweïtien | 3 | 1000 unités mineures |

Les deux dernières lignes ne sont dans le périmètre d'aucun déploiement OpenFSP envisagé.
Elles sont listées parce qu'une implémentation qui code en dur un exposant de 2 passera
chaque test écrit sur les deux premières lignes et sera fausse dès l'instant où ce n'est
plus le cas.

**4.3. Les numéros de devise ISO 4217** (`332` pour HTG) ne sont pas utilisés par ce
protocole. Codes alphabétiques uniquement.

**4.4. Devises prises en charge.** Cette ADR rend *représentable* toute devise ISO 4217.
Elle n'oblige aucune passerelle à en *accepter* une en particulier. Les devises qu'un
déploiement prend en charge sont annoncées par la découverte de capacités et MUST être
découvrables à l'exécution ; un client MUST NOT déduire cette prise en charge de la version
du protocole.

### 5. Numéros de téléphone

**5.1.** Un numéro de téléphone est une chaîne au format E.164 : un `+`, puis un indicatif
pays, puis le numéro d'abonné, sans aucun autre caractère. Le total des chiffres MUST NOT
dépasser 15. Il correspond à `^\+[1-9]\d{1,14}$`.

**5.2.** Valide : `"+50934567890"`. Invalides : `"34567890"` (pas d'indicatif pays),
`"+509 34 56 78 90"` (espaces), `"+509-3456-7890"` (séparateurs), `"050934567890"` (un
préfixe international au lieu du `+`).

**5.3.** Le protocole n'accepte que l'E.164. Une passerelle MUST NOT tenter de déduire un
indicatif pays d'un numéro au format national, et MUST rejeter toute valeur ne satisfaisant
pas le §5.1.

Les formats locaux sont ambigus par nature, et l'ambiguïté n'est pas toujours détectable :
un numéro national valide dans deux pays produit une requête bien formée qui débite la
mauvaise personne. Un SDK MAY offrir une fonction convertissant une saisie locale en E.164,
et c'est le bon endroit pour une telle commodité : dans le client, où le pays de
l'utilisateur est connu, et jamais sur le fil.

**5.4.** La validité structurelle n'implique rien sur la joignabilité, l'inscription chez un
fournisseur, ou l'existence d'un portefeuille. Une implémentation MUST NOT traiter un numéro
syntaxiquement valide comme un numéro vérifié.

**5.5.** Les numéros de téléphone sont des données personnelles. Voir *Considérations de
sécurité* et *Considérations réglementaires* ci-dessous.

### 6. Identifiants

OpenFSP distingue quatre sortes d'identifiants. Les confondre est une erreur fréquente et
coûteuse, aussi chacun est-il nommé séparément et contraint séparément.

#### 6.1. `ResourceId`, assigné par la passerelle

**6.1.1.** Une chaîne de 1 à 64 points de code correspondant à `^[A-Za-z0-9_-]+$`, assignée
par la passerelle à la création de la ressource, immuable ensuite.

**6.1.2.** Elle est **opaque**. Un client MUST NOT l'analyser, en déduire une structure, en
dériver un ordre, ni en construire une. Toute information dont un client a besoin est un
champ explicite.

**6.1.3.** Les implémentations SHOULD générer la portion identifiante comme un UUID version
7 (RFC 9562), dont l'ordonnancement temporel fait bien se comporter les index de base de
données à l'échelle. Tout générateur satisfaisant 6.1.1 et 6.1.4 est conforme ; un ULID, par
exemple, est tout aussi acceptable. La valeur étant opaque, ce choix relève de
l'implémentation et non de l'interopérabilité.

**6.1.4.** Un `ResourceId` MUST NOT être devinable. Les entiers séquentiels et les compteurs
monotones MUST NOT être utilisés, même là où l'identifiant seul n'accorde aucun accès.

**6.1.5.** Il est RECOMMENDED aux implémentations de préfixer l'identifiant par un court
marqueur de type suivi d'un tiret bas (`pay_`, `rfd_`), afin qu'un identifiant mal aiguillé
échoue immédiatement et lisiblement plutôt que d'adresser la mauvaise ressource sans rien
signaler. Le préfixe fait partie de la valeur opaque.

#### 6.2. `Reference`, choisie par le marchand

**6.2.1.** Une chaîne de 1 à 128 points de code correspondant à `^[A-Za-z0-9._:/-]+$`,
fournie par le marchand à la création de la ressource, immuable ensuite.

**6.2.2.** Une `Reference` MUST être unique parmi les ressources du même type appartenant au
même **propriétaire**, le propriétaire étant la partie pour le compte de laquelle la
ressource a été créée, normalement le marchand. Une passerelle MUST rejeter une requête de
création dont la référence est déjà utilisée par ce propriétaire, et MUST NOT créer une
seconde ressource sous cette référence.

**6.2.2.1.** L'unicité MUST NOT être imposée entre propriétaires. Une passerelle servant
plusieurs marchands MUST permettre à deux d'entre eux d'utiliser indépendamment la même
référence, et MUST NOT signaler de conflit entre eux.

**6.2.2.2.** La portée est le propriétaire plutôt que le déploiement parce qu'une contrainte
à l'échelle du déploiement serait observable entre des parties qui ne voient pas les
ressources l'une de l'autre. Un marchand créant `INV-1` s'entendrait dire que la référence
est prise, et apprendrait par là qu'un autre marchand de la même passerelle la détient. Les
références étant couramment séquentielles, cela transforme la création en oracle sur le
volume de transactions d'un concurrent. Restreindre la portée au propriétaire supprime le
canal au lieu de l'atténuer.

**6.2.3.** C'est la **clé de corrélation primaire**, et le §6.2.2 est ce qui la fait
fonctionner. Quand une requête de création expire, le marchand ne sait pas si le paiement
existe. Parce qu'il a choisi la référence et l'a stockée avant d'envoyer la requête, il peut
toujours interroger la passerelle sur cette référence et obtenir une réponse faisant
autorité. Un identifiant qui n'arrive jamais qu'en réponse ne peut pas répondre à la seule
question qui compte quand la réponse n'arrive pas.

**6.2.4.** Une `Reference` MAY être transmise au fournisseur de paiement, qui en a
couramment besoin pour son propre rapprochement. Elle MUST NOT contenir de données
personnelles, d'identifiants secrets, ni rien que le marchand ne divulguerait pas au
fournisseur. Utiliser `Metadata` (§9) pour ce qui doit rester dans les systèmes propres du
marchand.

**6.2.5.** L'interaction entre une référence en double et une requête rejouée portant un
`Idempotency-Key` est spécifiée par l'ADR d'idempotence, pas ici. Tant que cette ADR n'est
pas acceptée, les deux mécanismes MUST NOT être supposés interchangeables.

#### 6.3. `ProviderReference`, assignée par le fournisseur

**6.3.1.** Une chaîne opaque d'au plus 255 points de code, portant l'identifiant quelconque
assigné par le fournisseur. Aucune structure n'est imposée, parce qu'aucune ne peut l'être.

**6.3.2.** Elle est OPTIONAL et MAY être absente : avant que le fournisseur ait répondu, ou
définitivement, lorsqu'une requête a expiré et que le fournisseur n'a jamais rapporté
d'identifiant.

**6.3.3.** Un client MUST NOT l'utiliser comme clé de corrélation primaire, et MUST NOT
supposer qu'elle est unique entre fournisseurs. Elle existe pour le support, l'audit et le
règlement des litiges : c'est la valeur que le personnel du fournisseur demandera.

#### 6.4. `IdempotencyKey`

**6.4.1.** Une chaîne de 1 à 255 points de code correspondant à `^[A-Za-z0-9_-]+$`, portée
par l'en-tête HTTP `Idempotency-Key`. Les clients SHOULD la générer comme un UUID.

**6.4.2.** Sa syntaxe est fixée ici pour que toutes les ADR qui l'utilisent s'accordent. Sa
sémantique (portée, rétention, ce qui constitue un rejeu conflictuel) est spécifiée par la
ADR d'idempotence.

### 7. Horodatages

**7.1.** Un horodatage est une chaîne au format `date-time` de la RFC 3339, toujours en UTC,
toujours avec un `Z` littéral comme décalage : `"2026-08-17T14:32:07.412Z"`.

**7.2.** Un décalage numérique non nul tel que `-05:00` MUST être rejeté, tout comme le `z`
minuscule et une `date` seule sans heure.

**7.3.** La précision à la seconde est REQUIRED. Les fractions de seconde sont OPTIONAL,
jusqu'à la milliseconde, et un client MUST les accepter qu'il les utilise ou non. Un serveur
MUST NOT supposer qu'un client en envoie.

**7.4.** L'UTC est imposé et non recommandé. Haïti observe l'heure d'été, de sorte qu'un
horodatage local est ambigu pendant une heure chaque année et mal ordonné pendant une autre,
dans une piste d'audit d'événements financiers, dans une fenêtre qui revient chaque année, à
une heure que personne ne teste. Stocker en UTC et afficher l'heure locale dans une
interface utilisateur est le seul arrangement correct toute l'année.

**7.5. Ordonnancement.** Les horodatages MUST NOT servir d'ordre total sur les événements.
Les horloges dérivent, et deux événements peuvent partager une milliseconde. Là où l'ordre
importe, l'ADR qui définit ces événements spécifie un mécanisme de séquencement explicite ;
un client MUST NOT en inventer un à partir des horodatages.

### 8. Fee

**8.1.** Un `Fee` consigne ce que le fournisseur a facturé pour un paiement.

```json
{
  "amount": { "amount": 1250, "currency": "HTG" },
  "bearer": "merchant"
}
```

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `amount` | `Money` | REQUIRED | §3. Même devise que le paiement auquel il se rattache. |
| `bearer` | chaîne | REQUIRED | `merchant` ou `payer`. Voir §8.4. |

**8.2. Pourquoi ce type existe.** La section 8 de la circulaire 121 de la BRH impose un reçu
portant, entre autres, les frais. Sans ce type, un marchand ne peut pas produire ce reçu à
partir de ce que le protocole lui donne, et une spécification qui oblige un marchand à
obtenir ailleurs une donnée exigée lui a renvoyé une obligation réglementaire.

**8.3. L'absence signifie « non connu », jamais « aucun ».** C'est la distinction autour de
laquelle ce type est façonné, et s'y tromper est la manière dont un marchand sous-déclare
des frais sur un reçu. Des frais nuls sont un montant nul. Des frais que la passerelle
ignore sont le champ absent. Un client MUST NOT afficher des frais absents comme nuls, et
MUST NOT les dériver par soustraction.

**8.4. `bearer`** indique qui a supporté les frais. `merchant` est le cas ordinaire : le
fournisseur les déduit de ce qu'il verse. `payer` existe parce que certains fournisseurs
facturent le payeur, et non parce qu'un marchand pourrait ajouter une surcharge : la
circulaire 131 de la BRH interdit à une institution de permettre aux marchands d'imposer des
frais additionnels sur les paiements par carte ou autres paiements électroniques. Une
passerelle MUST NOT laisser un client fixer `bearer` ; elle rapporte ce que le fournisseur a
fait.

**8.5. Moment.** Les frais sont fréquemment inconnus à la création et connus seulement une
fois le paiement terminal. Une passerelle MUST NOT retarder une transition terminale en
attendant des frais, et MUST NOT les deviner. `updated_at` bouge quand des frais arrivent,
et [ADR-0003 §3.1](0003-payment-lifecycle.md) n'en est pas affectée : apprendre ce qu'un
paiement a coûté ne change pas ce qu'il a fait.

**8.6. Tous les fournisseurs n'en divulguent pas.** Là où un fournisseur ne rapporte jamais
de frais, le champ est définitivement absent, et la passerelle le dit en n'annonçant pas la
capacité `payments.fee` ([ADR-0007 §2.2](0007-capability-discovery.md)). C'est le modèle
de capacités appliqué à un champ plutôt qu'à une opération : un marchand qui intègre un tel
fournisseur apprend au moment de la découverte que cette ligne de reçu doit venir d'ailleurs,
au lieu de le découvrir lors d'un audit.

### 9. Métadonnées

**9.1.** `metadata` est un objet OPTIONAL associant des chaînes à des chaînes, posé par le
marchand et retourné inchangé partout où la ressource est retournée.

```json
{
  "metadata": {
    "order_id": "184",
    "channel": "web"
  }
}
```

**9.2.** Limites : au plus 20 clés ; des clés de 1 à 40 points de code correspondant à
`^[A-Za-z0-9_.-]+$` ; des valeurs d'au plus 500 points de code. Les valeurs MUST être des
chaînes : objets imbriqués, tableaux, nombres, booléens et `null` sont tous invalides.

**9.3.** Une passerelle MUST stocker et retourner les métadonnées sans altération. Elle MUST
NOT les interpréter, les indexer à des fins métier, ni agir en fonction d'elles.

**9.4.** Une passerelle MUST NOT transmettre les métadonnées à un fournisseur de paiement à
moins qu'une ADR ultérieure ne l'exige explicitement pour une opération nommée. Les
métadonnées sont l'annotation privée du marchand, et c'est ce qui les distingue de
`Reference` (§6.2.4).

**9.5.** Les marchands SHOULD NOT placer de données personnelles dans les métadonnées, et
MUST NOT y placer d'identifiants secrets, de jetons ou de matériel d'authentification. Les
métadonnées apparaissent dans les journaux, dans les échanges de support et dans les
exports.

## Compatibilité

Cette ADR introduit les premiers types normatifs d'OpenFSP. Il n'y a rien à casser.

Chaque type est porteur pour les ADR ultérieures, de sorte que modifier l'un d'eux après
acceptation est une rupture de compatibilité pour toute la spécification, régie par
[GOVERNANCE.md §5](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#5-garanties-de-stabilité).
C'est la raison de cette étroitesse : chaque contrainte ci-dessus serait pénible à ajouter
plus tard et est presque gratuite à imposer maintenant.

Deux dispositions sont délibérément extensibles sans rupture : le §4.4 permet à un
déploiement d'ajouter des devises sans toucher au protocole, et le §2.3 permet à une version
mineure d'ajouter des champs.

## Considérations de sécurité

**Traitement des montants.** Le §3.4 existe parce qu'un montant hors intervalle est
silencieusement altéré par les analyseurs JSON courants plutôt que rejeté, ce qui transforme
un échec de validation en transaction fausse. Les implémentations MUST valider l'intervalle
explicitement et MUST NOT s'en remettre à l'analyse numérique par défaut de leur langage.

**Confusion de signe.** L'exigence du §3.6 que les montants des requêtes soient strictement
positifs bloque une classe d'attaque où un montant négatif inverse le sens d'un transfert.
Le contrôle appartient à la frontière du protocole, pas à la logique métier.

**Énumération d'identifiants.** Le §6.1.4 interdit les identifiants de ressource devinables.
Même là où un identifiant seul n'accorde aucun accès, des identifiants séquentiels
divulguent un volume de transactions, et le volume est une information commercialement
sensible qu'un marchand n'a pas accepté de publier.

**Données personnelles sur le fil.** Les numéros de téléphone sont des données personnelles.
Ils MUST NOT apparaître dans les journaux à un niveau inférieur à celui de l'audit de
sécurité, MUST NOT apparaître dans les messages d'erreur retournés à un client, et MUST NOT
être inclus dans la télémétrie. Lorsqu'un numéro doit être affiché pour le support, seuls les
derniers chiffres devraient l'être.

**Les métadonnées comme vecteur de fuite.** Le §9.5 existe parce que les métadonnées sont
l'endroit où les valeurs sensibles s'accumulent en pratique. Une passerelle SHOULD documenter
que les métadonnées ne sont pas chiffrées au repos à moins que l'opérateur ne s'en charge.

**Divulgation par la référence.** Le §6.2.4 avertit qu'une référence peut atteindre le
fournisseur. Une référence séquentielle telle que `INV-2026-00184` divulgue un volume de
factures à ce fournisseur. Les marchands pour qui cela compte devraient utiliser une
référence opaque et garder l'identifiant lisible dans les métadonnées.

**L'unicité des références ne doit pas fuir entre marchands.** Le §6.2.2.1 interdit
d'imposer l'unicité entre propriétaires, et le §6.2.2.2 en donne la raison : un conflit
signalé entre deux parties qui ne voient pas les ressources l'une de l'autre est un canal
d'information, et avec des références séquentielles c'est un canal efficace. Une passerelle
MUST partitionner l'index d'unicité par propriétaire. L'imposer globalement, ce qui est la
chose naturelle à faire avec une colonne de base de données unique, est un défaut et pas
seulement une préférence de conception.

**Rejet plutôt que normalisation.** Les §4.1 et §5.3 exigent de rejeter une entrée malformée
plutôt que de la réparer. La réparation silencieuse masque les défauts du client jusqu'au cas
où la réparation devine mal, et dans ce domaine une mauvaise supposition est un mauvais
paiement.

## Considérations réglementaires

**Données personnelles.** La seule donnée personnelle de cette ADR est le numéro de
téléphone. Contraindre l'identité à l'E.164 et à rien d'autre maintient par construction
l'empreinte du protocole en données personnelles au minimum, ce qui simplifie toute analyse
de protection des données portant sur un déploiement.

**Auditabilité.** Des identifiants immuables (§6.1.1, §6.2.1) et des horodatages UTC
obligatoires (§7.1) sont ce qui rend possible une piste d'audit reconstructible. Un
superviseur examinant un déploiement peut ordonner les événements entre systèmes sans
réconcilier de fuseaux horaires ni résoudre de réutilisation d'identifiants.

**Intégrité des montants.** Les unités mineures entières éliminent entièrement l'écart
d'arrondi, de sorte que la somme des transactions enregistrées égale la somme de la valeur
transférée sans tolérance. Un reporting dérivé des enregistrements OpenFSP n'exige aucune
marge de réconciliation.

**Conservation.** Cette ADR ne spécifie aucune durée de conservation. La conservation est
juridictionnelle et appartient à l'opérateur, mais les types sont conçus pour qu'un
enregistrement puisse être conservé avec le numéro de téléphone caviardé tout en restant
cohérent en interne et auditable.

## Alternatives envisagées

**Chaînes décimales pour les montants**, `"1250.00"`. Utilisées par plusieurs API établies,
et évitent la question de l'exposant des unités mineures. Rejetées parce qu'elles déplacent
le problème au lieu de le résoudre : chaque implémentation doit alors analyser correctement
des décimaux dans un langage dont le type numérique par défaut est à virgule flottante
binaire, et l'échec est silencieux. Les unités mineures entières font de l'implémentation
correcte l'implémentation évidente.

**Montants à virgule flottante.** Rejetés sans réserve. `0.1 + 0.2` ne vaut pas `0.3` en
IEEE 754, et aucun soin au niveau applicatif ne répare une représentation choisie au niveau
du protocole.

**Une chaîne unique pour la monnaie**, `"HTG 1250.00"`. Compacte et lisible. Rejetée parce
qu'elle oblige chaque implémentation à écrire un analyseur, et que les analyseurs divergent.

**Devise implicite par la configuration du déploiement.** Une passerelle configurée pour
Haïti pourrait défaut à HTG et laisser les clients l'omettre. Rejeté : un montant sans devise
explicite est la condition préalable à la classe d'erreur la plus coûteuse que ce document
existe pour prévenir, et la réalité bimonétaire d'Haïti rend l'omission activement dangereuse
plutôt que simplement négligée.

**Formats téléphoniques nationaux acceptés et normalisés.** Meilleure expérience développeur
pour un déploiement purement domestique. Rejeté au titre du §5.3 : l'ambiguïté est
indétectable à l'endroit où elle compte, et la commodité appartient au SDK.

**ULID imposés au lieu d'UUIDv7.** Les deux sont ordonnés dans le temps et les deux sont en
production. Aucun n'est imposé : le §6.1.2 rend les identifiants opaques, ce qui fait du
choix un détail d'implémentation. Normaliser une représentation interne que nul ne peut
analyser contraindrait les implémenteurs sans gain d'interopérabilité.

**Entiers epoch Unix pour les horodatages.** Compacts, sans ambiguïté de fuseau, trivialement
ordonnés. Rejetés parce que l'unité n'est pas autodescriptive (les secondes et les
millisecondes sont toutes deux courantes, et la différence est un facteur mille qu'aucun
schéma n'attrape) et parce que les valeurs sont illisibles dans les journaux, là où elles
sont lues le plus souvent.

**Noms de champs en `camelCase`.** Un tirage à pile ou face avec `snake_case`. Choisi par
cohérence avec les API de paiement que les implémenteurs ont le plus de chances d'avoir déjà
intégrées, et parce que des conventions mélangées dans un même projet sont pires que l'une ou
l'autre convention.

## Questions non résolues

1. **Quelles devises une passerelle v1 doit accepter.** HTG est certaine. USD est réellement
   ouverte, et la réponse est une question de marché plutôt que de technique. Le §4.4 rend le
   modèle de données indifférent, de sorte que cela peut être tranché par l'ADR de capacités
   sans rouvrir celle-ci.
2. **Si l'unicité de `Reference` devrait être resserrée davantage, jusqu'au fournisseur.** Le
   §6.2.2 la porte au propriétaire, ce qui a fermé la divulgation entre marchands décrite au
   §6.2.2.2. Savoir si un même propriétaire devrait pouvoir réutiliser une référence auprès
   de deux fournisseurs est une autre question, toujours ouverte. La réutilisation
   permettrait à un marchand de retenter un paiement échoué chez un second fournisseur sous
   la même référence, ce qui est commode ; elle signifierait aussi qu'une référence
   n'identifie plus un paiement, propriété dont dépend le §6.2.3.
3. **Si le préfixe de type du §6.1.5 devrait être obligatoire.** En faire un MUST rendrait
   l'outillage et les messages d'erreur plus nets, au prix d'une contrainte sur les
   implémentations pour un bénéfice diagnostique plutôt que fonctionnel.
4. **Les limites des métadonnées.** Vingt clés et 500 points de code sont des chiffres
   conventionnels plutôt que mesurés. Ils peuvent être relevés sans rupture ; ils ne peuvent
   pas être abaissés. Viser bas est délibéré.
5. **Une convention de formatage monétaire.** Afficher `125000` comme `1 250,00 HTG`, avec le
   séparateur et la position du symbole en usage en Haïti, est une question de présentation,
   mais si chaque SDK invente la sienne, les utilisateurs voient des montants incohérents.
   Cela pourrait justifier une ADR Informational plutôt que normative.

## Références

Citations complètes dans [`references.md`](references.md).

**Normatives.** `RFC8785` pour la canonicalisation JSON, `RFC9562` pour l'UUID version 7,
`RFC3339` pour les horodatages, `ISO4217` pour les codes de devise et leurs exposants
d'unités mineures, `E164` pour les numéros de téléphone, `RFC2119` et `RFC8174` pour les
mots-clés d'exigence.

**Informatives.** `ISO20022` pour le modèle sémantique auquel ce modèle de données est
ancré, avec la correspondance et ses pertes dans
[ADR-0010](0010-iso-20022-semantic-correspondence.md). `IETF-IDEM` pour l'en-tête
`Idempotency-Key` du §6.4, examiné dans
[ADR-0004 §9](0004-idempotency-and-retries.md). `BRH-121` section 13.1 pour la
traçabilité que servent les identifiants du §6.

## Implémentation de référence

Aucune pour l'instant.

## Errata

Aucun.
