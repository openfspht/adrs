# ADR-0005 : Taxonomie des erreurs

- Voie : Standards
- Statut : Brouillon
- Créée : 2026-08-17
- Dépend de : ADR-0001, ADR-0002, ADR-0003, ADR-0004

## Résumé

Cette ADR spécifie comment une passerelle OpenFSP rapporte l'échec d'une requête : le format
de la réponse, le catalogue fermé des types d'erreur, et deux propriétés dont un client a
besoin pour réagir correctement, à savoir si la requête peut être rejouée et si elle a pu
prendre effet.

Elle s'appuie sur les Problem Details de la RFC 9457. Elle assigne aussi une représentation
aux conditions d'erreur nommées mais laissées sans représentation par
[ADR-0004](0004-idempotency-and-retries.md), achevant la couche fondamentale de la
spécification.

## Motivation

Un client qui reçoit une erreur doit répondre à deux questions avant de pouvoir faire quoi
que ce soit de sensé : *puis-je rejouer ?* et *est-ce que cela s'est produit quand même ?*

La plupart des API ne répondent ni à l'une ni à l'autre. Elles retournent un code de statut
et un message écrit pour un humain, et chaque client encode alors ses propres suppositions :
filtrage sur des bouts de message, traitement uniforme de tous les 5xx, reprises de choses
qui ne doivent pas être rejouées. Les suppositions sont généralement justes, ce qui rend les
mauvaises si coûteuses : elles sont découvertes en production, sur les chemins qui
surviennent rarement.

La seconde question est celle que les API de paiement laissent le plus souvent sans réponse,
et c'est celle qui coûte de l'argent. Un `503` signifie que la requête a été refusée et n'a
définitivement rien fait. Un `504` signifie que la passerelle a cessé d'attendre :
l'opération peut être achevée, peut avoir échoué, peut être encore en cours. Un client qui
traite ces deux cas de façon identique perdra des paiements ou en dupliquera, et aucun soin
du côté client ne répare une API qui ne les distingue pas.

Cette ADR rend les deux réponses explicites, lisibles par machine, et présentes dans chaque
réponse d'erreur. Elle trace aussi la ligne, de façon répétée parce que c'est la ligne la
plus souvent franchie dans les intégrations de paiement, entre une requête qui a échoué et un
paiement qui n'a pas abouti.

## Hors périmètre

- **Aucune erreur propre à un point d'accès.** Les conditions particulières à une opération
  sont nommées par l'ADR qui définit cette opération, avec le format et les règles établis
  ici.
- **Aucune raison d'échec de paiement.** Pourquoi un *paiement* a échoué relève de
  [ADR-0003 §7.2](0003-payment-lifecycle.md). Cette ADR couvre pourquoi une *requête* a
  échoué. La distinction est rappelée au §2 parce que tout le reste en dépend.
- **Aucun algorithme de reprise.** Le comportement de reprise du client relève de
  [ADR-0004 §8](0004-idempotency-and-retries.md). Cette ADR fournit les entrées dont ce
  comportement a besoin.
- **Aucune exigence de journalisation ou d'alerte.** Ce qu'un opérateur fait d'une erreur
  relève de sa politique de déploiement.

## Spécification

Les mots-clés MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
MAY et OPTIONAL sont à interpréter comme décrit dans les RFC 2119 et RFC 8174, lorsque, et
seulement lorsque, ils apparaissent en capitales.

### 1. Format

**1.1.** Toute réponse d'erreur MUST être un objet problem detail tel que défini par l'ADR
9457, envoyé avec le type de média `application/problem+json`.

**1.2.** Un exemple complet :

```json
{
  "type": "https://openfsp.org/problems/provider-timeout",
  "title": "The provider did not respond in time",
  "status": 504,
  "detail": "No response from the provider after 30s. The payment's outcome is unknown.",
  "instance": "/v1/payments",
  "retryable": true,
  "effect": "unknown",
  "request_id": "req_01J9ZK3QF8XN2M7VYB4C6D8E0G"
}
```

**1.3. Membres.**

| Membre | Type | Présence | Notes |
|---|---|---|---|
| `type` | URI | REQUIRED | L'identifiant stable lisible par machine. Voir §3. |
| `title` | chaîne | REQUIRED | Résumé court lisible par un humain. **Non stable.** |
| `status` | entier | REQUIRED | Le code de statut HTTP, dupliqué selon la RFC 9457. |
| `detail` | chaîne | OPTIONAL | Explication lisible de *cette* occurrence. **Non stable.** |
| `instance` | référence d'URI | OPTIONAL | Le chemin de la requête. |
| `retryable` | booléen | REQUIRED | Extension. Voir §5. |
| `effect` | chaîne | REQUIRED | Extension. `none` ou `unknown`. Voir §6. |
| `request_id` | chaîne | REQUIRED | Extension. Corrèle avec les journaux de la passerelle. |
| `errors` | tableau | OPTIONAL | Extension. Détail au niveau des champs. Voir §7. |
| `provider_detail` | objet | OPTIONAL | Extension. Relais du fournisseur. Voir §8. |

**1.4.** Un client MUST identifier une erreur par son seul `type`. `title` et `detail` sont
écrits pour des humains, MAY être reformulés dans n'importe quelle version, et MAY être
localisés. Filtrer sur eux est un défaut, et cette ADR n'offre aucune garantie de stabilité
qui le ferait fonctionner.

**1.5.** `status` MUST être égal au statut HTTP de la réponse.

**1.6.** `request_id` MUST être présent sur toute erreur, y compris un `500`. C'est ce qui
permet à un marchand de signaler un problème que l'opérateur de la passerelle peut ensuite
retrouver. Son absence est la raison la plus fréquente pour laquelle une conversation de
support à propos d'un paiement n'aboutit nulle part.

### 2. Une requête échouée n'est pas un paiement échoué

**2.1.** Une réponse relevant de cette ADR signifie que **la requête a échoué**. Elle ne
signifie pas qu'un paiement a échoué.

**2.2.** Un paiement refusé par le fournisseur est rapporté par une réponse de **succès** :
HTTP `200`, une ressource paiement, `"status": "failed"`, et un `failure_reason` au titre de
[ADR-0003 §7.2](0003-payment-lifecycle.md). L'API a fait son travail : on lui a demandé
de tenter un paiement, elle en a tenté un, et elle rapporte le dénouement.

**2.3.** Une passerelle MUST NOT rapporter un paiement refusé comme une réponse d'erreur, et
MUST NOT utiliser un statut 4xx ou 5xx pour transmettre le dénouement d'un paiement.

**2.4.** Un client MUST NOT traiter une réponse non-2xx comme un paiement échoué. C'est une
requête échouée, dont l'effet sur un éventuel paiement est donné par `effect` (§6) et est
fréquemment *unknown*.

**2.5.** Ceci est rappelé longuement parce que confondre les deux est le défaut sérieux le
plus fréquent dans les intégrations de paiement, et qu'il échoue dans les deux sens : un
client qui lit toute erreur comme un refus marquera comme échoués des paiements jamais
tentés, puis créera des doublons quand le client final réessaiera ; un client qui lit un
paiement refusé comme un échec de transport rejouera un refus qui ne réussira jamais.

### 3. URI de type

**3.1.** Les types d'erreur sont identifiés par un URI de la forme
`https://openfsp.org/problems/<code>`, où `<code>` est le code en minuscules séparé par des
tirets tiré du catalogue du §9.

**3.2.** Les URI de type sont d'abord des identifiants stables et seulement ensuite des
emplacements de documentation. Un client MUST les comparer comme des chaînes opaques et MUST
NOT en déréférencer un pour interpréter une réponse.

**3.3.** Les URI SHOULD pointer vers une documentation lisible du type d'erreur.

**3.4. L'autorité est permanente.** `openfsp.org` est l'autorité canonique de chaque URI de
type de cette spécification, et MUST NOT changer : ni pour un changement de marque, ni pour
un changement de dépositaire, ni pour une migration. Ces URI sont des identifiants que les
clients conformes comparent comme des chaînes littérales ; altérer l'autorité casserait
silencieusement le filtrage de tout client déployé alors que chaque réponse resterait bien
formée.

En conséquence, le projet traite l'enregistrement de ce domaine comme une obligation
permanente au titre de
[GOVERNANCE.md §5](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#5-garanties-de-stabilité),
au même rang que ne pas casser le format du fil.

**3.5.** Une passerelle MAY définir des types supplémentaires sous sa propre autorité pour
des conditions hors de cette spécification, et MUST NOT définir de nouveaux types sous
l'autorité OpenFSP.

**3.6.** Un client MUST traiter un `type` non reconnu en se rabattant sur la sémantique de
`status`, `retryable` et `effect`, tous présents sur chaque erreur. Par conséquent, ajouter
un type au catalogue n'est **pas** une rupture de compatibilité : un client plus ancien
dégrade vers un comportement correct mais grossier plutôt que d'échouer.

### 4. Usage des codes de statut

**4.1.** Le catalogue du §9 assigne un statut à chaque type. Une passerelle MUST utiliser le
statut assigné.

**4.2.** L'assignation suit la RFC 9110 : `400` pour une requête que la passerelle ne peut
pas analyser ou dont la forme est fausse ; `422` pour une requête bien formée dont le
contenu est sémantiquement invalide ; `409` là où la requête entre en conflit avec un état
que la passerelle détient déjà.

**4.3. Pourquoi `idempotency-key-reused` est en 422 et non en 409.** La distinction du §4.2
en décide, et cela mérite d'être dit parce que la réponse intuitive est l'autre. Une clé
réutilisée avec un corps différent n'entre pas en conflit avec un état que la passerelle
détient : la requête est bien formée, elle n'adresse aucune ressource existante, et rien dans
l'enregistrement stocké n'est contredit par elle. Ce qui ne va pas, c'est le contenu propre
de la requête, mesuré contre une règle que le client a acceptée en choisissant la clé. C'est
la définition de `422` au §4.2, et `409` est réservé au cas où la passerelle détient bien un
état conflictuel, qui est `idempotency-request-in-progress`.

Le draft IETF sur l'en-tête `Idempotency-Key` aboutit au même partage, avec `422` pour une
clé « reused across different payloads of this operation » et `409` pour une requête portant
la même clé « being processed or is outstanding » [IETF-IDEM, s. 2.7]. S'accorder avec lui ne
coûte rien ici et épargne une surprise à l'implémenteur.

**4.4.** Les échecs imputables au fournisseur sont distingués par le statut, et la
distinction porte un sens réel pour le client : `502` le fournisseur a répondu quelque chose
d'invalide ou une erreur qui lui est propre, `503` le fournisseur n'était pas joignable du
tout, `504` le fournisseur n'a pas répondu à temps.

### 5. Rejouabilité

**5.1.** `retryable` est REQUIRED sur toute erreur et indique si répéter la requête,
inchangée et avec le même `Idempotency-Key`, peut réussir.

**5.2.** `retryable: true` signifie que rejouer est **sans danger**, pas que cela marchera.
La sûreté est la garantie : parce que la même clé d'idempotence est présentée, une reprise ne
peut pas dupliquer une opération ayant déjà pris effet
([ADR-0004 §3](0004-idempotency-and-retries.md)).

**5.3.** Un client MUST NOT rejouer une erreur portant `retryable: false`. Une telle erreur
est causée par la requête elle-même et se reproduira à l'identique.

**5.4.** Un client qui rejoue MUST réutiliser la clé d'idempotence d'origine
([ADR-0004 §8.1](0004-idempotency-and-retries.md)) et MUST appliquer un retrait.
`retryable: true` n'est pas une permission de rejouer immédiatement ou indéfiniment.

**5.5.** Lorsque `Retry-After` est présent, un client MUST le respecter.

**5.6.** `retryable` MUST correspondre à la valeur assignée au type au §9. Il est porté dans
la réponse pour qu'un client générique se comporte correctement sans embarquer le catalogue,
ce qui est aussi ce qui garde du sens au repli du §3.6.

### 6. `effect`, le signal d'indétermination

**6.1.** `effect` est REQUIRED sur toute erreur et prend l'une de deux valeurs :

| Valeur | Signification |
|---|---|
| `none` | L'opération n'a définitivement pas pris effet. Rien n'a été créé ni modifié. |
| `unknown` | L'opération a pu prendre effet ou non. La passerelle ne peut pas le dire. |

**6.2.** Une passerelle MUST rapporter `none` seulement là où elle peut l'établir. Là où elle
ne le peut pas, elle MUST rapporter `unknown`. Rapporter `none` en supposant qu'un appel
échoué n'a rien fait est interdit : une requête qui a expiré en chemin vers un fournisseur a
couramment fait quelque chose.

**6.3.** Sur `effect: unknown`, un client MUST NOT conclure que l'opération a échoué. Il MUST
soit rejouer avec la clé d'idempotence d'origine, soit établir le dénouement en lisant la
ressource par sa `reference` ([ADR-0002 §6.2.3](0002-core-data-model.md)).

**6.4.** `effect: unknown` sur une création de paiement signifie qu'un paiement peut exister.
Un client qui abandonne l'opération ici a créé exactement le défaut que cette spécification
existe pour prévenir : un paiement que le payeur a peut-être fait et dont le marchand ignore
l'existence.

**6.5.** `effect` et `retryable` sont indépendants. `rate_limited` est rejouable sans effet ;
`internal_error` est rejouable avec effet inconnu ; `provider_unavailable` est rejouable sans
effet. Un client qui fond les deux en une seule notion de « transitoire » se trompera sur au
moins l'un d'eux.

**6.6.** Ce membre existe parce que l'information est disponible pour la passerelle et pour
personne d'autre. Il correspond exactement à la distinction de déterminité qui régit si un
enregistrement d'idempotence est écrit ([ADR-0004 §5](0004-idempotency-and-retries.md)) :
une erreur avec `effect: unknown` MUST NOT avoir été enregistrée, de sorte qu'une reprise est
une tentative neuve sous les protections du §7 de cette ADR.

### 7. Erreurs au niveau des champs

**7.1.** Lorsqu'une erreur concerne des champs précis, le tableau `errors` SHOULD être
présent. Chaque entrée comporte :

| Membre | Type | Présence | Notes |
|---|---|---|---|
| `field` | chaîne | REQUIRED | JSON Pointer (RFC 6901) dans le corps de la requête. |
| `code` | chaîne | REQUIRED | Code stable lisible par machine. |
| `detail` | chaîne | OPTIONAL | Lisible par un humain. Non stable. |

```json
{
  "type": "https://openfsp.org/problems/invalid-field",
  "title": "One or more fields are invalid",
  "status": 422,
  "retryable": false,
  "effect": "none",
  "request_id": "req_01J9ZK…",
  "errors": [
    { "field": "/amount/currency", "code": "unsupported_currency",
      "detail": "This gateway accepts HTG." },
    { "field": "/payer/phone_number", "code": "malformed",
      "detail": "Must be E.164, e.g. +50934567890." }
  ]
}
```

**7.2.** JSON Pointer est spécifié plutôt qu'un chemin pointé afin que les emplacements
imbriqués et de tableau soient sans ambiguïté, et que les clients puissent relier une erreur
à une saisie sans analyseur à eux.

**7.3.** Une passerelle SHOULD rapporter tous les champs invalides dans une seule réponse
plutôt que le premier trouvé. Les retourner un à un transforme une correction unique en
plusieurs allers-retours, et dans un formulaire de paiement l'utilisateur paie chacun d'eux.

**7.4.** `field` MUST référencer la requête telle que le client l'a envoyée, pas une
représentation interne.

### 8. Relais du fournisseur

**8.1.** Lorsqu'une erreur provient d'un fournisseur, `provider_detail` SHOULD porter le
rapport propre du fournisseur :

```json
"provider_detail": { "code": "E4021", "message": "Subscriber not registered" }
```

**8.2.** Son contenu est **non fiable et non interprété**. Une passerelle MUST NOT l'analyser,
MUST NOT en dériver `type`, `retryable` ou `effect`, et MUST le relayer sans altération.

**8.3.** Un client MUST NOT brancher sur `provider_detail`. Il existe pour le support et
l'audit : c'est la valeur que le personnel du fournisseur demandera. Les décisions
programmatiques se prennent sur `type`, `retryable` et `effect`.

**8.4.** `provider_detail` MUST NOT contenir d'identifiants secrets, de jetons, ni aucun
matériel d'authentification. Lorsqu'un fournisseur inclut un tel matériel dans sa sortie
d'erreur, la passerelle MUST le caviarder avant de le relayer.

**8.5.** Ceci reflète `failure_detail` sur un paiement échoué
([ADR-0003 §7.4](0003-payment-lifecycle.md)). L'appariement est le même dans les deux cas
et pour la même raison : un code neutre seul est introuvable quand un marchand appelle le
support du fournisseur, et un relais seul est non programmable.

### 9. Le catalogue

Cette énumération est fermée. Y ajouter exige une ADR ; le §3.6 rend un tel ajout non
cassant.

Chaque code de ce catalogue est un nom normalisé pour une condition que chaque fournisseur
rapporte aujourd'hui différemment. Là où un code de motif ISO 20022 correspond à l'un d'eux,
[ADR-0010](0010-iso-20022-semantic-correspondence.md) consigne la correspondance. Elle y
est consignée plutôt qu'ici afin que ce catalogue reste gouverné par le seul comportement du
protocole : les codes ci-dessous font autorité, et la correspondance est une vue sur eux,
jamais l'inverse. L'essentiel de ce catalogue n'a aucun homologue ISO 20022, portant sur la
requête plutôt que sur le paiement. Les codes de motif qu'un superviseur reconnaît se
rattachent à `failure_reason` ([ADR-0003 §7.2](0003-payment-lifecycle.md)), pas à
ceux-ci.

#### 9.1. Erreurs de requête

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `malformed-request` | 400 | false | `none` | Le corps n'est pas du JSON valide, ou n'est pas un objet. |
| `unknown-field` | 400 | false | `none` | Un champ non reconnu a été envoyé ([ADR-0002 §2.4](0002-core-data-model.md)). |
| `missing-field` | 400 | false | `none` | Un champ obligatoire est absent. |
| `idempotency-key-required` | 400 | false | `none` | Pas d'`Idempotency-Key` sur une requête mutante ([ADR-0004 §1.3](0004-idempotency-and-retries.md)). |
| `invalid-field` | 422 | false | `none` | Bien formé mais sémantiquement invalide. Porte `errors`. |
| `unsupported-currency` | 422 | false | `none` | La devise est un ISO 4217 valide mais n'est pas acceptée ici ([ADR-0002 §4.4](0002-core-data-model.md)). |
| `capability-not-supported` | 422 | false | `none` | L'opération exige une capacité que cette passerelle n'annonce pas. |
| `idempotency-key-reused` | 422 | false | `none` | Même clé, corps différent ([ADR-0004 §3.4](0004-idempotency-and-retries.md)). Voir §4.3. |

#### 9.2. Authentification et autorisation

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `unauthenticated` | 401 | false | `none` | Identifiants absents, malformés ou invalides. |
| `forbidden` | 403 | false | `none` | Authentifié, mais non autorisé à effectuer cette opération. |

#### 9.3. Ressource introuvable

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `not-found` | 404 | false | `none` | Pas de telle ressource, ou non visible pour ce principal. |

**9.3.1.** Une passerelle MUST retourner `not-found` plutôt que `forbidden` là où divulguer
l'existence d'une ressource fuiterait en soi de l'information. Distinguer les deux indique à
un appelant non autorisé quels identifiants sont réels.

#### 9.4. Conflits

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `reference-conflict` | 409 | false | `none` | La `reference` est déjà utilisée ([ADR-0002 §6.2.2](0002-core-data-model.md)). |
| `idempotency-request-in-progress` | 409 | **true** | `unknown` | Une requête portant cette clé est encore en cours ([ADR-0004 §3.5](0004-idempotency-and-retries.md)). |
| `state-conflict` | 409 | false | `none` | L'opération n'est pas permise depuis l'état courant de la ressource ([ADR-0003 §2.1](0003-payment-lifecycle.md)). |

**9.4.1.** `reference-conflict` porte `retryable: false` et `effect: none` (la requête n'a
rien fait), mais ce n'est **pas** un échec que le client devrait traiter comme terminal. Il
signifie qu'une ressource portant cette référence existe déjà, et la réponse correcte est de
la lire. C'est la protection permanente contre les doublons décrite en
[ADR-0004 §6.3](0004-idempotency-and-retries.md), et la recevoir après une reprise est le
mécanisme qui fonctionne, pas qui casse.

**9.4.2.** `idempotency-request-in-progress` est le seul 409 rejouable, et il porte
`effect: unknown` parce que la requête concurrente peut aboutir. Il SHOULD être envoyé avec
`Retry-After`.

#### 9.5. Limitation de débit

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `rate-limited` | 429 | true | `none` | Trop de requêtes. MUST porter `Retry-After`. |

#### 9.6. Défaillances de la passerelle et du fournisseur

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `internal-error` | 500 | true | **`unknown`** | Une défaillance inattendue de la passerelle. |
| `provider-error` | 502 | true | **`unknown`** | Le fournisseur a retourné une erreur ou une réponse inexploitable. |
| `provider-unavailable` | 503 | true | `none` | Le fournisseur n'a pas pu être joint du tout. |
| `provider-timeout` | 504 | true | **`unknown`** | Le fournisseur n'a pas répondu à temps. |

**9.6.1.** `provider-unavailable` porte `effect: none` parce qu'une connexion jamais établie
ne peut pas avoir eu d'effet. Une passerelle MUST ne l'utiliser que là où cela est établi :
une connexion refusée ou un échec DNS. Là où une requête a été envoyée et où le dénouement
est incertain, `provider-timeout` est correct.

**9.6.2.** Choisir `provider-unavailable` quand `provider-timeout` est la vérité est le
rapport erroné le plus dommageable dont dispose une implémentation : il affirme
`effect: none` pour une opération qui a pu déplacer de l'argent, et un client conforme le
croira.

**9.6.3.** `internal-error` MUST porter `effect: unknown` à moins que la passerelle ne puisse
établir qu'aucun appel au fournisseur n'a été fait. L'optimisme n'est pas de mise ici ; la
passerelle a échoué de façon inattendue, et son propre récit de ce qu'elle a fait est la
chose la moins digne de confiance.

**9.6.4.** `internal-error` MUST NOT inclure de diagnostics internes (traces de pile,
requêtes, noms d'hôtes) dans `detail`. `request_id` (§1.6) est la façon dont l'opérateur les
retrouve.

### 10. Langue

**10.1.** `title` et `detail` SHOULD être en anglais par défaut.

**10.2.** Une passerelle MAY les localiser, et SHOULD honorer `Accept-Language` lorsqu'elle
le fait. Le français et le créole haïtien sont les langues dont les déploiements propres à
cette spécification auront le plus vraisemblablement besoin.

**10.3.** La localisation MUST NOT altérer `type`, `retryable`, `effect`, ni aucun `code`.
L'interdiction du §1.4 de filtrer sur du texte lisible existe en partie pour que la
localisation ne puisse pas casser un client.

## Compatibilité

Nouvelle spécification. Rien à casser.

Les conditions nommées par [ADR-0004](0004-idempotency-and-retries.md) reçoivent ici leur
représentation : `idempotency_key_reused` devient `idempotency-key-reused` (422) et
`idempotency_request_in_progress` devient `idempotency-request-in-progress` (409). Aucun
changement à cette ADR n'est requis ; le §9.4 est la représentation qu'elle avait différée.

Ajouter une entrée au catalogue est non cassant au titre du §3.6. Changer le `status`, le
`retryable` ou l'`effect` d'une entrée existante est cassant, puisque les clients conformes
agissent sur les trois.

## Considérations de sécurité

**Les erreurs divulguent.** Une erreur est un canal de la passerelle vers quiconque a envoyé
la requête, y compris quelqu'un qui la sonde. Chaque disposition ci-dessous en découle.

**Pas de données personnelles dans les erreurs.** `detail`, `title` et `errors[].detail` MUST
NOT contenir de numéros de téléphone, d'identifiants de payeur, ni de montants. Renvoyer un
numéro de téléphone invalide pour expliquer pourquoi il a été rejeté est naturel, courant, et
interdit : cela transforme le point d'accès en oracle de confirmation pour qui a fourni le
numéro.

**Pas de détail interne.** Le §9.6.4 interdit les traces de pile, le texte des requêtes et
les noms d'hôtes dans les réponses. C'est la matière première d'une attaque ciblée, et cela
parvient au client sans lui apporter aucun bénéfice.

**Pas de divulgation d'existence.** Le §9.3.1 exige `not-found` de préférence à `forbidden`
là où la distinction confirmerait qu'un identifiant est réel.

**Relais non fiable.** `provider_detail` est du contenu que la passerelle n'a pas rédigé. Un
tableau de bord marchand qui l'affiche sans échappement a un vecteur de script intersites
provenant de l'extérieur des deux parties. Cette obligation incombe au client, et les SDK
SHOULD la documenter.

**Fuite d'identifiants par le relais.** Le §8.4 exige un caviardage, parce que la sortie
d'erreur d'un fournisseur a été observée en train de réémettre le contenu de la requête, y
compris du matériel d'authentification.

**Échecs d'authentification uniformes.** `unauthenticated` MUST NOT distinguer un principal
inconnu d'un principal valide avec un mauvais identifiant : la distinction énumère les
principaux valides.

**La limitation de débit est un contrôle de sécurité.** `rate-limited` borne le sondage de
tous les autres types d'erreur, y compris les erreurs au niveau des champs du §7 qui
permettraient autrement une énumération efficace.

**`effect` n'est pas exploitable, et son absence l'est.** Rapporter honnêtement `unknown` ne
divulgue rien qu'un attaquant puisse utiliser, tandis qu'une passerelle qui rapporte `none`
pour paraître assurée fait abandonner aux clients des opérations qui ont réussi : un défaut
d'intégrité des données atteignable par quiconque peut provoquer une expiration.

## Considérations réglementaires

**Traçabilité.** `request_id` sur chaque erreur (§1.6), combiné au relais du fournisseur
(§8), permet de tracer tout échec signalé depuis les enregistrements du marchand, à travers
les journaux de la passerelle, jusqu'à la référence propre du fournisseur. C'est la chaîne
que suit un examinateur.

**Rapport honnête de l'incertitude.** Le §6.2 interdit d'affirmer qu'une opération n'a eu
aucun effet là où cela n'est pas établi. Les enregistrements d'un déploiement distinguent
donc « ne s'est pas produit » de « non connu », au lieu de présenter le second comme le
premier, ce qui est la différence entre un enregistrement reconstructible et un
enregistrement trompeur.

**Conséquences pour le consommateur.** Les §6.4 et §9.4.1 existent pour garantir qu'un
paiement achevé par un payeur n'est pas perdu parce que le client du marchand a mal traité une
erreur. Combinée à [ADR-0004](0004-idempotency-and-retries.md), un client conforme ne peut pas
écarter sans trace un paiement qui a pu réussir.

**Minimisation des données.** L'interdiction des données personnelles dans les réponses
d'erreur limite jusqu'où l'information du payeur voyage, y compris dans les journaux et les
canaux de support où la rétention est la moins maîtrisée.

**Le régulateur exige désormais ce que ce catalogue rend possible.** `BRH-131` interdit à une
institution financière de « négliger de signaler et de compenser toute perte du consommateur
liée à une défaillance du système » [BRH-131, p. 8, s. 6.1 s)]. Signaler et compenser une
perte causée par le système suppose de pouvoir dire qu'une défaillance a eu lieu, laquelle, et
si l'opération a pris effet. Cette dernière question est `effect` (§6), et c'est le champ de
cette ADR dont l'homologue réglementaire est le plus direct : `none` signifie que le
consommateur n'a rien perdu parce que rien ne s'est produit, `unknown` signifie que
l'institution ne le sait pas encore et doit le découvrir avant de pouvoir répondre.

La même circulaire exige que les dispositifs de protection « définir clairement les
responsabilités respectives des parties en cas de pertes financières » [BRH-131, p. 17,
s. 6.9 c)]. Deux parties ne peuvent pas répartir clairement la responsabilité d'une
défaillance qu'elles nomment différemment.

**Le rapport agrégé des plaintes exige des catégories comparables.** `BRH-131` exige un
rapport consolidé des plaintes, couvrant « nature, fréquence, causes, mesures correctives et
taux de résolution », à soumettre trimestriellement à la BRH sous forme agrégée [BRH-131,
p. 21, s. 6.11.5 c)], et exige des institutions qu'elles « analyser régulièrement les plaintes
afin d'identifier les causes récurrentes et les faiblesses systémiques » [BRH-131, p. 21,
s. 6.11.4 a)]. L'agrégation entre institutions est une arithmétique sur des catégories. Là où
les catégories sont privées, l'arithmétique est dépourvue de sens, et le superviseur reçoit
des sommes de choses qui ne sont pas la même chose.

**Un vocabulaire partagé des défaillances.** Un superviseur qui compare aujourd'hui deux
institutions compare deux vocabulaires privés. Le catalogue fermé du §9, avec l'énumération
fermée de `failure_reason` de [ADR-0003 §7.2](0003-payment-lifecycle.md) et sa
correspondance vers les codes de motif ISO 20022, fait qu'une défaillance signifie la même
chose d'un déploiement à l'autre. C'est une condition préalable à toute comparaison que
l'autorité pourrait souhaiter faire, et cela ne coûte rien aux institutions au-delà de
l'adoption des noms.

## Alternatives envisagées

**Un objet d'erreur nu**, `{"error": {"code": ..., "message": ...}}`, comme la plupart des
API. Rejeté au profit de la RFC 9457 : une norme publiée, avec un type de média enregistré,
de l'outillage existant et un mécanisme d'extension défini. Le principal argument pour une
forme sur mesure est la familiarité, qui vaut moins que l'interopérabilité pour une
spécification destinée à être implémentée par des parties qui n'ont pas été consultées.

**Un membre `code` séparé doublant `type`.** Courant et ergonomique : des chaînes courtes
sont plus agréables à comparer que des URI. Rejeté parce que deux identifiants pour une même
chose finissent par diverger, et que la RFC 9457 désigne déjà `type` comme l'identifiant. Les
codes du catalogue n'apparaissent que comme le dernier segment de l'URI.

**Déduire la rejouabilité du code de statut.** Cela marche presque : 5xx rejouable, 4xx non.
Cela casse sur `429`, qui est rejouable, et sur `409 idempotency-request-in-progress`, qui
est rejouable et qui est le cas qui compte le plus. Encoder la propriété explicitement coûte
un booléen et supprime une classe de suppositions côté client.

**Omettre `effect`, en laissant l'indétermination implicite dans le code de statut.**
L'approche habituelle, et la source de la défaillance décrite dans la Motivation. `502`,
`503` et `504` ne distinguent pas de façon fiable « n'a rien fait » de « a pu faire quelque
chose » : les implémentations choisissent entre eux au jugé. Rendre la propriété explicite
force l'implémenteur à décider, et le §9.6.2 nomme la conséquence d'une mauvaise décision.

**Rapporter les paiements refusés en 4xx.** Superficiellement net : le paiement n'a pas
abouti, donc la réponse n'est pas un succès. Rejeté au titre du §2 : cela détruit la
distinction entre un paiement tenté et refusé et une requête qui n'a jamais atteint le
fournisseur, et cette distinction détermine si rejouer est correct ou catastrophique.

**Localiser par défaut depuis `Accept-Language`.** Séduisant sur un marché bilingue. Rejeté
comme défaut au titre du §10.1 parce que le texte d'erreur finit dans les journaux et les
tickets de support, où un mélange de langues déterminé par le client qui a appelé rend le
dépouillement illisible pour l'exploitant. La localisation reste disponible là où un
déploiement la souhaite.

## Questions non résolues

1. **Si `errors` devrait être REQUIRED pour `invalid-field`.** C'est un SHOULD au §7.1. Un
   MUST serait testable par la suite de conformité et empêcherait une passerelle de rapporter
   « quelque chose est invalide » sans dire quoi.
2. **Un vocabulaire de codes lisibles par machine pour `errors[].code`.** Le §7.1 exige que
   les codes soient stables mais ne les énumère pas. Un vocabulaire fermé permettrait aux
   clients de traiter génériquement les erreurs au niveau des champs ; un vocabulaire ouvert
   est plus facile à étendre. Cette question est différée jusqu'à ce que les ADR des points
   d'accès montrent quels codes reviennent réellement.
3. **Si `effect` devrait avoir une troisième valeur** pour « partiellement appliqué ». Aucune
   opération de la spécification actuelle ne peut s'appliquer partiellement, et ajouter la
   valeur par anticipation obligerait chaque client à traiter un cas qui ne peut pas survenir.
   C'est noté pour qu'une future opération composée ne surcharge pas `unknown` à l'insu des
   clients.
4. **En-têtes de limitation de débit.** `Retry-After` est exigé sur `rate-limited`, mais
   savoir si les champs d'en-tête `RateLimit` devraient aussi être spécifiés est une question
   ouverte, et dépend du modèle d'authentification que l'ADR de l'API tranchera.

## Références

Citations complètes dans [`references.md`](references.md).

**Normatives.** `RFC9457` pour le format des problem details, `RFC9110` pour la sémantique
des codes de statut, `RFC6901` pour le JSON Pointer d'`errors`, `RFC2119` et `RFC8174` pour
les mots-clés d'exigence.

**Informatives.** `BRH-131` pour les homologues réglementaires des *Considérations
réglementaires*. `IETF-IDEM` pour le partage des codes de statut adopté au §4.3. `ADR-0010`
consigne où un code du §9 correspond à un code de motif ISO 20022, et où il n'en a aucun.

## Implémentation de référence

Aucune pour l'instant.

## Errata

Aucun.
