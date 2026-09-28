# ADR-0009 : Authentification et identifiants

- Voie : Standards
- Statut : Brouillon
- Créée : 2026-09-06
- Dépend de : ADR-0001, ADR-0002, ADR-0004, ADR-0005, ADR-0006, ADR-0007

## Résumé

Cette ADR spécifie les deux problèmes d'identifiants qu'a une passerelle, qui ne sont pas le
même problème et sont souvent confondus.

**Vers l'extérieur**, un client prouve qui il est à la passerelle avec une clé d'API porteur
dans un en-tête `Authorization`. Le §2 fixe le format, le §3 la présentation, le §4 la façon
dont la passerelle la stocke et la compare, le §6 les portées qui décident de ce que le
principal résultant peut faire, et le §7 la rotation et la révocation.

**Vers l'intérieur**, la passerelle détient les identifiants du marchand chez ses
fournisseurs, que [ADR-0001](0001-architecture-and-scope.md) identifie déjà comme l'actif
de plus grande valeur de la conception. Le §9 transforme cet énoncé d'architecture en
exigences qu'une suite de conformité peut tester, et ferme les chemins de fuite que le reste
de la spécification a ouverts : le relais du fournisseur dans les erreurs, le relais du
fournisseur dans les paiements, et les journaux.

Cette ADR tranche aussi une question que [ADR-0004 §2.3](0004-idempotency-and-retries.md)
laisse en suspens, en définissant ce qu'est un **principal** (§5).

## Motivation

Chaque ADR jusqu'ici a supposé un principal authentifié et est passée à autre chose.
[ADR-0006](0006-gateway-http-api-payments.md) déclare l'authentification hors périmètre
et y renvoie. [ADR-0004 §2.3](0004-idempotency-and-retries.md) cloisonne les
enregistrements d'idempotence au principal, ce qui est sa disposition de sécurité la plus
importante, et le terme n'est défini nulle part.
[ADR-0007 §3.2](0007-capability-discovery.md) marque la découverte de capacités
« authentifiée » sans dire par quoi. La spécification tire des chèques sur cette ADR depuis
un certain temps.

Le coût de la laisser non écrite n'est pas que les implémenteurs n'auront pas
d'authentification. C'est qu'ils en auront chacun une différente, et que les différences
atterriront exactement aux endroits difficiles à voir. Une passerelle compare les clés d'API
par égalité de chaînes et fuite leur longueur par le temps. Une autre les stocke en clair
parce que ce ne sont « que des clés d'API ». Une troisième accepte la clé dans un paramètre
de requête par commodité, et met l'identifiant de chaque marchand dans un journal d'accès de
serveur web, un historique de navigateur, et un en-tête `Referer`. Une quatrième retourne
une erreur différente pour une clé inconnue et pour une clé révoquée, et transforme son 401
en oracle.

Aucune de ces défaillances n'est exotique. Les quatre sont en production quelque part
aujourd'hui, et chacune est bon marché à éliminer par spécification avant que quiconque
n'écrive le code.

La moitié intérieure a une motivation plus aiguë. Cette spécification a, sans le vouloir,
construit deux canaux qui portent la sortie du fournisseur droit au marchand :
`provider_detail` dans une erreur ([ADR-0005 §8](0005-error-taxonomy.md)) et
`failure_detail` sur un paiement ([ADR-0006 §3.1](0006-gateway-http-api-payments.md)).
Les deux existent pour de bonnes raisons, et les deux sont des tuyaux d'un système qui
détient des identifiants vers un système qui ne doit jamais les voir. Un fournisseur qui
réémet un en-tête de requête dans un corps d'erreur, ce que plusieurs font, transforme une
aide au débogage en divulgation d'identifiant. Le §9.5 existe à cause de cela.

## Hors périmètre

- **Aucune authentification d'humain.** Il n'y a pas de comptes utilisateurs, pas de mots de
  passe, pas de sessions et pas de connexion. Les clients d'une passerelle sont les
  applications propres du marchand, et une personne qui administre le déploiement le fait par
  sa configuration, non par cette API.
- **Aucun serveur d'autorisation.** OAuth 2.0 n'est pas exigé, et le §11 dit pourquoi. Un
  déploiement qui en veut un peut en placer un devant ; rien ici ne l'interdit.
- **Aucun format d'identifiant de fournisseur.** Ce que veut MonCash et ce que veut NatCash
  diffèrent, et chaque adaptateur définit sa propre configuration. Le §9 régit la façon dont
  chacun d'eux est traité, jamais ce qu'ils contiennent.
- **Aucune API d'émission de clés.** Les clés sont émises par l'opérateur du déploiement via
  la surface d'administration propre à la passerelle, qui est du logiciel de déploiement, pas
  du protocole sur le fil. Le §7 spécifie les propriétés que cette surface doit avoir sans
  spécifier la surface.
- **Aucune multilocation.** Une passerelle sert un marchand
  ([ADR-0001](0001-architecture-and-scope.md)). Les principaux distinguent les
  applications de ce marchand les unes des autres, non un marchand d'un autre. Le §5.6 dit ce
  qui change si cette hypothèse est un jour abandonnée.
- **Aucun filtrage des capacités par principal.** Savoir si la découverte de capacités
  devrait différer par principal est laissé ouvert dans
  [ADR-0007](0007-capability-discovery.md) et reste ouvert ici.

## Spécification

Les mots-clés MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED,
MAY et OPTIONAL sont à interpréter comme décrit dans les RFC 2119 et RFC 8174, lorsque, et
seulement lorsque, ils apparaissent en capitales.

### 1. Schéma

**1.1.** Un client s'authentifie auprès d'une passerelle avec une **clé d'API porteur**.
Chaque point d'accès défini par cette spécification est authentifié, avec exactement deux
exceptions : le descripteur de service de
[ADR-0007 §3.1](0007-capability-discovery.md) et l'ensemble de clés de webhook de
[ADR-0008 §6.1](0008-webhooks-and-event-delivery.md).

**1.2.** Une passerelle MUST NOT offrir de mode non authentifié pour tout autre point
d'accès, y compris en mode de développement. Un chemin d'authentification qu'on coupe en
développement est un chemin que personne ne teste.

**1.3.** Une passerelle MAY en outre exiger un TLS mutuel, une liste d'adresses autorisées,
ou un serveur d'autorisation devant l'API. Ce sont des choix de déploiement et ils MUST NOT
remplacer le §3.

### 2. Format de clé

**2.1.** Une clé d'API est une chaîne de la forme :

```
ofsp_<env>_<secret>
```

où `<env>` vaut `live` ou `test`, et `<secret>` fait au moins 32 caractères correspondant à
`^[A-Za-z0-9]+$`.

```
ofsp_live_7Kq2NfPzR4wYb9LdHt3XvA6mSjE0uCgB
```

**2.2.** `<secret>` MUST être généré par un générateur de nombres aléatoires
cryptographiquement sûr et MUST porter au moins **128 bits** d'entropie. Une passerelle MUST
NOT le dériver d'un nom de marchand, d'un horodatage, d'un compteur, ou d'un condensé de
quoi que ce soit de prévisible.

**2.3. Le préfixe `ofsp_` n'est pas une décoration.** Les scanners de secrets travaillent sur
des formes reconnaissables. Une clé qui ressemble à n'importe quelle autre chaîne opaque est
une clé qu'un scanner de dépôt, un pipeline de journaux et une règle de protection de push ne
peuvent pas signaler, et les clés atteignent les dépôts quoi qu'en dise une spécification. Un
préfixe fixe distinctif est le contrôle le moins cher de ce document.

**2.4. Le segment d'environnement.** Une passerelle MUST être configurée avec exactement un
environnement, `live` ou `test`, et MUST rejeter une clé dont l'`<env>` ne correspond pas,
avec `unauthenticated` ([ADR-0005 §9](0005-error-taxonomy.md)).

**2.5.** Le §2.4 existe pour prévenir l'accident d'identifiant le plus fréquent et le plus
coûteux en paiement, qui n'est pas le vol mais la confusion : une clé de test en production,
dont les échecs sont mystérieux, ou une clé réelle dans une suite de tests, dont les succès
déplacent de l'argent réel. Rendre les deux lexicalement distinguables signifie qu'un humain
qui lit un fichier de configuration peut voir l'erreur, et que la passerelle peut la refuser
avant que quoi que ce soit ne se produise.

**2.6.** Une clé MUST NOT encoder un principal, une portée, une expiration, ni aucune autre
structure qu'un client pourrait analyser. Elle est opaque au sens de
[ADR-0002 §6.1.2](0002-core-data-model.md). Une clé autodescriptive est une clé dont le
sens peut être altéré, et elle rend la révocation plus difficile qu'elle n'a besoin de
l'être.

**2.7.** Une passerelle MAY utiliser un `<secret>` plus long et MAY y ajouter une somme de
contrôle, pourvu que le résultat corresponde encore au §2.1. Une somme de contrôle permet à
l'outillage de rejeter une clé mal tapée sans appel réseau, et cela ne coûte rien ici.

### 3. Présentation

**3.1.** Un client MUST envoyer la clé dans l'en-tête `Authorization`, en utilisant le schéma
`Bearer` de la RFC 9110 :

```
Authorization: Bearer ofsp_live_7Kq2NfPzR4wYb9LdHt3XvA6mSjE0uCgB
```

**3.2.** Une passerelle MUST NOT accepter une clé présentée dans un paramètre de requête,
dans un corps de requête, dans un cookie, ou dans tout en-tête autre qu'`Authorization`.

**3.3.** Le §3.2 est une interdiction dure plutôt qu'une recommandation parce que chacun de
ces emplacements fuite par défaut plutôt que par accident. Un paramètre de requête atteint
les journaux d'accès des serveurs web, les journaux de mandataires, l'historique du
navigateur et l'en-tête `Referer` de toute requête ultérieure. Un corps est journalisé par
chaque intergiciel de journalisation de requêtes jamais écrit. Un cookie est envoyé par un
navigateur que le client n'avait pas l'intention d'impliquer. Aucune de ces fuites n'exige
que quiconque commette une erreur.

**3.4.** Une passerelle MUST rejeter une requête sans en-tête `Authorization`, avec un
en-tête inanalysable, ou utilisant un schéma autre que `Bearer`, avec `unauthenticated`. La
réponse MUST porter `WWW-Authenticate: Bearer`.

**3.5.** La correspondance du schéma est insensible à la casse, selon la RFC 9110. La clé
elle-même est sensible à la casse.

**3.6.** Une passerelle MUST NOT accepter plus d'un identifiant dans une même requête, et MUST
rejeter une requête qui en porte plusieurs avec `unauthenticated`. Aucune règle de priorité
entre deux identifiants n'est définie, parce que toute règle de ce type laisse un appelant
choisir sous quelle identité il agit.

### 4. Stockage et comparaison

**4.1.** Une passerelle MUST NOT stocker une clé d'API sous une forme d'où la clé peut être
retrouvée. Elle stocke un condensé.

**4.2.** Le condensé MUST être calculé avec SHA-256 ou plus fort, sur la clé entière y
compris son préfixe.

**4.3. Un hachage de mot de passe lent n'est pas exigé ici, et SHOULD NOT être utilisé.**
Argon2id, scrypt et bcrypt existent parce que les secrets choisis par des humains ont trop
peu d'entropie pour survivre à une attaque par devinette hors ligne, et ils achètent cette
résistance avec un coût par vérification. Une clé générée selon le §2.2 a 128 bits
d'entropie, il n'y a donc rien à deviner, et le coût serait payé sur chaque requête que la
passerelle sert. C'est dit explicitement parce que le conseil habituel, correct pour des mots
de passe, est faux pour ce cas, et qu'un implémenteur qui le suivrait ralentirait la
passerelle sans gain de sécurité.

**4.4. Recherche.** Une passerelle a besoin de trouver l'enregistrement d'une clé présentée
sans parcourir tous les enregistrements. Elle MAY stocker un **préfixe de recherche**, les 12
premiers caractères de `<secret>`, en clair à côté du condensé, et indexer dessus. Un préfixe
de cette longueur n'est pas un identifiant secret : il porte moins de 72 bits, le reste du
secret n'est pas affecté, et il est assez court pour être montré dans une interface
d'administration afin qu'un opérateur puisse distinguer deux clés.

**4.5.** Après avoir localisé un enregistrement candidat, une passerelle MUST comparer le
condensé de la clé présentée au condensé stocké en **temps constant**. Elle MUST NOT utiliser
d'égalité de chaînes ordinaire, et MUST NOT court-circuiter au premier octet divergent.

**4.6.** Une passerelle SHOULD faire en sorte qu'une requête portant une clé inconnue et une
requête portant une clé connue mais révoquée prennent un temps indiscernable. Lorsque la
recherche du §4.4 ne trouve aucun enregistrement candidat, la passerelle MUST calculer malgré
tout un condensé de la clé présentée et le comparer en temps constant à une valeur factice,
afin que l'absence de préfixe ne se lise pas dans le temps de réponse. Là où la différence ne
peut pas être supprimée, elle MUST NOT être aggravée par un travail conditionnel tel que
journaliser un cas et pas l'autre.

**4.7. Une seule erreur pour chaque échec.** Un identifiant absent, malformé, inconnu,
révoqué, expiré, ou du mauvais environnement produit tous `unauthenticated` avec le même
`title` et aucun `detail` qui les distingue. Une passerelle MUST NOT dire à un appelant lequel
de ces cas s'applique.

**4.8.** Le §4.7 coûte un peu de commodité à l'opérateur et supprime un oracle. L'opérateur
obtient la distinction là où elle appartient, dans les journaux propres de la passerelle,
corrélée par le `request_id` de [ADR-0005 §1.6](0005-error-taxonomy.md), que l'appelant
peut citer sans rien en apprendre.

**4.9.** Une passerelle MUST NOT journaliser une clé présentée, en entier ou tronquée au-delà
de son préfixe de recherche, à aucun niveau, y compris en cas d'échec. Une tentative
d'authentification échouée est journalisée avec le préfixe de recherche et le `request_id`,
jamais avec le secret.

### 5. Principaux

**5.1.** Un **principal** est l'identité à laquelle une authentification réussie se résout.
C'est le sujet de chaque décision d'autorisation, et c'est le *P* de
[ADR-0004 §2.3](0004-idempotency-and-retries.md).

**5.2.** Chaque clé appartient à exactement un principal. Un principal MAY détenir plusieurs
clés, et le §7 dépend de ce qu'il en détienne au moins deux pendant une rotation.

**5.3. Deux clés du même principal sont le même principal.** Elles partagent les
enregistrements d'idempotence, elles voient les mêmes ressources, et une requête rejouée avec
la seconde clé après révocation de la première se résout au même enregistrement. Une
passerelle MUST NOT cloisonner quoi que ce soit à la clé là où cette spécification dit
principal.

**5.4.** Le §5.3 est tout l'intérêt de la distinction. Si les enregistrements d'idempotence
étaient cloisonnés à la clé, faire tourner une clé réinitialiserait silencieusement toute
protection contre les doublons en cours, et une reprise à cheval sur une rotation créerait un
second paiement. Tout l'objet de [ADR-0004](0004-idempotency-and-retries.md) tomberait au
moment où un opérateur fait la chose responsable.

**5.5.** Un principal a un identifiant stable et opaque assigné par la passerelle, obéissant
à [ADR-0002 §6.1](0002-core-data-model.md). Il apparaît dans les journaux de la passerelle
et dans l'enregistrement d'audit du §10. Il n'est exposé sur le fil par aucun point d'accès de
cette spécification.

**5.6.** Tous les principaux d'une passerelle voient les mêmes ressources. Cela découle du
modèle de déploiement à marchand unique et est énoncé pour que nul n'infère une isolation qui
n'est pas spécifiée : une passerelle n'est pas un mécanisme pour empêcher une des applications
d'un marchand de lire les paiements d'une autre. Les portées (§6) restreignent ce qu'un
principal peut *faire*, jamais ce qu'il peut *voir*. Si un déploiement multimarchand entrait
un jour dans le périmètre, l'isolation au niveau des ressources serait une nouvelle ADR et non
une option de configuration.

### 6. Portées

**6.1.** Une clé est émise avec un ensemble de **portées**. Une portée est une chaîne en
minuscules nommant une classe d'opérations.

**6.2. Le registre.** Cette ADR définit ces portées et aucune autre.

| Portée | Permet |
|---|---|
| `capabilities:read` | La découverte de capacités ([ADR-0007 §3.2](0007-capability-discovery.md)). |
| `payments:read` | Lire un paiement, rechercher par référence ([ADR-0006 §5.2](0006-gateway-http-api-payments.md)). |
| `payments:write` | Créer un paiement, synchroniser un paiement ([ADR-0006 §5.1](0006-gateway-http-api-payments.md), [§5.3](0006-gateway-http-api-payments.md)). |

**6.3.** `payments:write` n'implique pas `payments:read`. Une clé est émise avec chaque portée
dont elle a besoin, listée. Les chaînes d'implication sont commodes une fois et déroutantes
pour toujours, et un implémenteur qui doit raisonner sur ce qu'une portée accorde
implicitement finira par se tromper dans le sens permissif.

**6.4.** Une passerelle MUST rejeter une requête dont le principal n'a pas la portée requise
avec `forbidden` ([ADR-0005 §9](0005-error-taxonomy.md)), et MUST NOT y substituer
`unauthenticated` ni `not-found`.

**6.5.** Le §6.4 est le seul endroit où cette ADR dit délibérément quelque chose à
l'appelant. La distinction entre « je ne sais pas qui vous êtes » et « je sais qui vous êtes
et vous n'avez pas le droit de faire cela » est actionnable : la première est un problème
d'identifiant, la seconde un problème d'attribution de droits, et les confondre envoie un
opérateur chercher au mauvais endroit. L'information divulguée ne l'est qu'à un appelant déjà
authentifié.

**6.6. Synchroniser est une écriture.**
[ADR-0006 §5.3](0006-gateway-http-api-payments.md) appelle le fournisseur et peut changer
l'état stocké, ce qui est pourquoi c'est un `POST` là-bas et `payments:write` ici, nonobstant
qu'un marchand y pense comme à une consultation.

**6.7.** Ajouter une portée exige une ADR. Une portée est ajoutée à côté des opérations
qu'elle régit, de sorte qu'une ADR qui ajoute une opération ajoute sa portée dans le même
document.

**6.8.** Une passerelle MUST NOT émettre une clé sans portée et la traiter comme non
restreinte. Un ensemble de portées vide ne permet rien.

**6.9. Le moindre privilège est le défaut que l'outillage devrait rendre facile.** Un tunnel
d'achat a besoin de `payments:write` et `payments:read`. Une tâche de rapprochement a besoin
de `payments:read` seule, et lui émettre une portée d'écriture est la façon dont un rapport en
lecture seule finit par créer un paiement pendant un incident.

### 7. Rotation, révocation et expiration

**7.1.** Une passerelle MUST prendre en charge plusieurs clés simultanément valides pour un
principal, afin qu'une clé puisse être remplacée sans interruption.

**7.2. La rotation** consiste à : émettre une seconde clé, la déployer, confirmer qu'elle est
en usage, révoquer la première. Une passerelle MUST NOT exiger l'ordre inverse, et MUST NOT
invalider les autres clés d'un principal quand une clé est émise.

**7.3. La révocation prend effet immédiatement.** Une passerelle MUST NOT servir une requête
avec une clé révoquée, et MUST NOT mettre en cache une décision d'authentification plus de
**60 secondes** après révocation. Là où un déploiement met les recherches en cache pour la
performance, le cache MUST être invalidé à la révocation plutôt que laissé expirer.

**7.4.** Une clé révoquée MUST NOT être rétablie, et son secret MUST NOT être réémis. Une clé
est révoquée parce qu'elle peut être connue de quelqu'un d'autre ; la raison n'expire pas.

**7.5.** Une passerelle MUST conserver l'enregistrement d'une clé révoquée, sans son secret,
afin que la piste d'audit du §10 puisse encore résoudre le principal d'une requête passée.
Supprimer l'enregistrement rendrait une vieille entrée de journal non attribuable, ce qui est
le contraire de l'objet de la révocation.

**7.6.** Une clé MAY porter une expiration. Une passerelle MUST rejeter une clé expirée avec
`unauthenticated` au titre du §4.7, et SHOULD prévenir son opérateur avant l'expiration plutôt
qu'après. Une expiration non annoncée casse le tunnel d'achat d'un marchand à minuit, sans que
rien n'indique pourquoi.

**7.7.** Une passerelle MUST montrer le secret de la clé exactement une fois, à l'émission, et
MUST être incapable de le montrer à nouveau. Cela découle du §4.1 et est énoncé séparément
parce que c'est une propriété de la surface d'administration, que le §4.1 n'atteint pas de
façon évidente.

**7.8.** Une passerelle SHOULD enregistrer et exposer, par clé, la date de sa dernière
utilisation. C'est le seul élément d'information qui fait de la révocation d'une clé inconnue
une décision plutôt qu'un pari.

### 8. Interaction avec le reste de la spécification

**8.1. Idempotence.** [ADR-0004 §2.3](0004-idempotency-and-retries.md) cloisonne un
enregistrement au principal, à l'opération et à la clé. Le **principal** de cette ADR-là est
le §5.1 d'ici, et la **clé** de là-bas est l'en-tête `Idempotency-Key`, non une clé d'API. Les
deux sens de « clé » sont fâcheux et la lecture est tranchée ici : un enregistrement
d'idempotence survit à une rotation de clé d'API (§5.4), et n'est jamais visible d'un autre
principal.

**8.2. Limitation de débit.** [ADR-0004](0004-idempotency-and-retries.md) exige une
limitation de débit par principal. Le principal est le §5.1, de sorte qu'un client ne peut pas
obtenir davantage de la passerelle en détenant davantage de clés.

**8.3. Erreurs.** `unauthenticated` et `forbidden` sont définies par
[ADR-0005 §9](0005-error-taxonomy.md) et ne sont pas redéfinies ici. Les deux sont
`retryable: false` et `effect: none`, ce qui est correct : une requête rejetée n'a rien fait,
et la répéter avec le même identifiant échouera à l'identique.

**8.4. Découverte de capacités.** Le descripteur de service
([ADR-0007 §3.1](0007-capability-discovery.md)) est non authentifié par conception et ne
divulgue aucun fournisseur. Le point d'accès des capacités exige `capabilities:read`. Les
fournisseurs avec lesquels un marchand travaille sont commercialement sensibles, et c'est ce
que la séparation protège.

**8.5. Webhooks.** [ADR-0008](0008-webhooks-and-event-delivery.md) authentifie dans
l'autre direction et n'utilise pas de clé d'API. Une passerelle MUST NOT envoyer de clé d'API
à un point d'accès de webhook, dans un en-tête ou ailleurs, et un abonné MUST NOT authentifier
une livraison par un autre moyen que la signature de
[ADR-0008 §5](0008-webhooks-and-event-delivery.md). Un jeton porteur partagé dans un
en-tête de webhook est un identifiant posté à une URL publique à chaque changement d'état.

**8.6.** L'ensemble de clés de webhook
([ADR-0008 §6.1](0008-webhooks-and-event-delivery.md)) est non authentifié, selon son §6.7.
Cette ADR ne change pas cela.

### 9. Identifiants de fournisseur

Le sujet change ici. Les §1 à §8 régissent l'identifiant qu'un client présente à la
passerelle. Cette section régit les identifiants que la passerelle présente à un fournisseur,
qui sont ceux du marchand, et que le projet ne détient jamais
([ADR-0001](0001-architecture-and-scope.md)).

**9.1. Source.** Une passerelle MUST pouvoir charger les identifiants de fournisseur depuis
des variables d'environnement ou depuis un gestionnaire de secrets. Elle MUST NOT exiger
qu'ils soient écrits dans un fichier de configuration, et sa documentation MUST NOT présenter
cela comme la méthode principale. Ce qui apparaît dans un guide de démarrage est ce qui
apparaît dans un dépôt.

**9.2.** Une passerelle SHOULD prendre en charge le rechargement des identifiants de
fournisseur sans redémarrage. Une rotation qui exige une interruption est une rotation qu'on
reporte.

**9.3. Aucune sortie.** Une passerelle MUST NOT retourner un identifiant de fournisseur, en
tout ou partie, depuis un quelconque point d'accès, dans un quelconque champ, sous une
quelconque condition. Il n'y a pas de point d'accès de débogage, pas de point d'accès de
configuration et pas de contrôle de santé qui en inclue un. Un contrôle de santé MAY rapporter
qu'un fournisseur est joignable ; il MUST NOT rapporter avec quoi.

**9.4. Aucun journal.** Une passerelle MUST NOT écrire un identifiant de fournisseur dans un
journal, une trace, une étiquette de métrique, un rapport d'erreur ou un vidage de plantage, à
aucun niveau. Là où une requête vers un fournisseur est journalisée pour diagnostic, l'en-tête
`Authorization` et tout champ portant un identifiant MUST être caviardés avant que la ligne de
journal ne soit construite, non filtrés ensuite.

**9.5. Le relais est un chemin de fuite, et MUST être caviardé.** `provider_detail`
([ADR-0005 §8](0005-error-taxonomy.md)) et `failure_detail`
([ADR-0006 §3.1](0006-gateway-http-api-payments.md)) portent la sortie du fournisseur au
client. Une passerelle MUST caviarder des deux toute valeur qu'elle détient comme identifiant
de fournisseur, et MUST le faire en comparant aux identifiants qu'elle détient plutôt que par
filtrage de motifs ressemblant à des secrets.

**9.6.** Le §9.5 n'est pas hypothétique. Des fournisseurs réémettent les paramètres de requête
dans les corps d'erreur, plusieurs incluent l'identité authentifiée dans un champ de
diagnostic, et au moins un retourne l'ensemble des en-têtes reçus en cas d'échec de
validation. La passerelle est le seul composant qui sait quelles chaînes sont des
identifiants, c'est donc le seul composant qui peut les retirer, et un client ne peut pas
compenser une passerelle qui ne le fait pas.

**9.7.** Le caviardage MUST NOT taire le fait qu'il a eu lieu. Là où une valeur est retirée, le
membre est remplacé par la chaîne `[redacted]` plutôt que supprimé, afin qu'un marchand qui
débogue une intégration puisse distinguer un champ que le fournisseur n'a pas envoyé d'un
champ que la passerelle a retiré.

**9.8. Rayon d'action.** Une compromission de la passerelle expose les identifiants de
fournisseur et l'historique de paiement d'un marchand. [ADR-0001](0001-architecture-and-scope.md)
accepte cela comme la conséquence directe de l'auto-hébergement, et c'est la raison pour
laquelle les exigences de cette section sont absolues plutôt que graduées : le marchand n'a
pas de seconde ligne de défense, parce qu'il n'y a pas d'opérateur derrière lui.

### 10. Audit

**10.1.** Une passerelle MUST enregistrer, pour chaque requête authentifiée, le principal, le
préfixe de recherche de la clé, l'opération, le `request_id` et le dénouement.

**10.2.** Elle MUST enregistrer les tentatives d'authentification échouées avec les mêmes
champs, moins le principal, qui est inconnu.

**10.3.** Elle MUST enregistrer chaque émission et chaque révocation de clé, avec l'heure et
les portées résultantes.

**10.4.** Aucun de ces enregistrements ne peut contenir un secret de clé (§4.9) ni un
identifiant de fournisseur (§9.4).

### 11. Conformité

**11.1.** Une passerelle est conforme si elle n'accepte que la présentation du §3, stocke et
compare selon le §4, se résout à un principal selon le §5, fait respecter les portées selon le
§6, prend en charge des clés qui se recouvrent et une révocation immédiate selon le §7, et
satisfait le §9 pour chaque fournisseur qu'elle prend en charge.

**11.2.** La suite de conformité teste le §4.7 en présentant une clé inconnue, une clé
révoquée et une clé du mauvais environnement, et en exigeant trois réponses indiscernables.
Elle teste le §9.5 en configurant un fournisseur simulé qui réémet les identifiants reçus dans
un corps d'erreur et en exigeant `[redacted]` dans `provider_detail`.

**11.3.** L'authentification n'est pas une capacité et n'est jamais annoncée. Il n'existe
aucun déploiement qui s'en passe (§1.2), il n'y a donc rien à découvrir.

## Compatibilité

Rien ne casse, parce que rien n'était spécifié avant. Chaque ADR à ce jour renvoyait à un
principal authentifié sans en définir un, et cette ADR fournit la définition que ces renvois
supposaient déjà.

Deux lectures sont tranchées plutôt que changées.
[ADR-0004 §2.3](0004-idempotency-and-retries.md) cloisonne les enregistrements à un
principal, que le §5.1 définit désormais et que le §5.3 fait survivre à une rotation de clé.
[ADR-0007 §3.2](0007-capability-discovery.md) est marquée authentifiée, et le §6.2 nomme
désormais la portée qu'elle exige. Une implémentation qui aurait deviné autrement sur l'un ou
l'autre point change ; une qui ne les avait pas implémentés n'a rien à changer.

Il n'y a aucune détection à l'exécution à spécifier. Un client sans identifiant valide reçoit
`unauthenticated`, que [ADR-0005](0005-error-taxonomy.md) définit déjà.

## Considérations de sécurité

Cette ADR est pour l'essentiel des considérations de sécurité, et le texte normatif porte son
propre raisonnement. Quatre choses ont leur place ici plutôt que là.

**Le modèle de menace n'est pas symétrique.** Un client s'authentifie auprès de la passerelle
par TLS avec un jeton porteur, et la passerelle s'authentifie auprès du client par une
signature à clé publique ([ADR-0008 §5](0008-webhooks-and-event-delivery.md)). Cette
asymétrie est délibérée et mérite d'être défendue. Le client initie sa requête et peut donc
vérifier la passerelle par TLS, de sorte qu'un jeton porteur sur un canal authentifié suffit
dans cette direction. L'abonné n'initie pas un webhook et ne peut vérifier son origine par
aucune propriété de transport, il lui faut donc une signature sur le message. Exiger que les
deux directions signent chargerait chaque SDK client, dans chaque langage, d'une
implémentation de signature pour résoudre un problème que TLS a déjà résolu.

**Un jeton porteur ne vaut que ce que vaut le canal.** Tout le §3 suppose du TLS avec
validation de certificat, selon [ADR-0006 §1.1](0006-gateway-http-api-payments.md). Une
passerelle joignable en clair remet ses clés au réseau, et aucune hygiène de stockage ne
compense.

**Énumération et force brute.** Une clé a 128 bits d'entropie, la deviner n'est donc pas la
menace. Deviner en volume comme déni de service en est une, et une passerelle SHOULD limiter
en débit les authentifications échouées par source, indépendamment des limites par principal
du §8.2, qui ne peuvent pas s'appliquer à une requête qui ne s'est résolue à aucun principal.

**Le régulateur exige l'audit que ces enregistrements servent.** `BRH-126` rend obligatoire un
audit de sécurité informatique au moins tous les trois ans, assorti d'une pénalité de
200 000 gourdes puis 100 000 gourdes par jour [BRH-126, p. 4]. Une piste d'audit incapable
d'attribuer une requête passée à un principal, parce que l'enregistrement de la clé a été
supprimé à la révocation, échoue à cet audit. Le §7.5 est écrit pour cela.

**La récupération après compromission est la propriété à tester.** La mesure de cette
conception n'est pas qu'elle prévient une fuite mais qu'un marchand qui en découvre une à neuf
heures du matin peut être en sûreté à neuf heures cinq. Des clés qui se recouvrent (§7.1), une
révocation immédiate (§7.3), des horodatages de dernière utilisation (§7.8) et un préfixe
distinctif qu'un scanner peut trouver (§2.3) existent ensemble pour cela. Un déploiement qui
ne peut pas faire tourner une clé sans interruption a tout le mécanisme et aucun du résultat.

## Considérations réglementaires

La circulaire 121 de la BRH du 6 décembre 2021 porte sur cette ADR en deux endroits, et il y a
un troisième point à faire sur ce qu'elle n'atteint pas.

Sa section 13.1 exige que chaque client soit identifié de façon unique et chaque transaction
traçable. Le §10 est l'enregistrement qui y répond du côté de la passerelle : chaque requête
se résout à un principal, chaque principal est stable à travers une rotation de clés (§5.3),
et l'enregistrement d'une clé révoquée est conservé (§7.5) de sorte qu'une requête passée reste
attribuable. Une conception qui supprimerait les identifiants à la révocation satisferait une
intuition d'hygiène et casserait la traçabilité.

Sa section 15 régit la protection des données en transmission et en stockage. Le §4.1 couvre
les clés d'API au repos, les §9.1 et §9.4 couvrent les identifiants de fournisseur, et
[ADR-0006 §1.1](0006-gateway-http-api-payments.md) couvre la transmission. Le §9.5 couvre
le cas que la section n'anticipe pas, qui est celui de données qui sortent par un champ conçu
pour autre chose.

**`BRH-126` est la circulaire à laquelle cette ADR répond le plus directement, et elle dérive
de l'article 83(10) de `HT-LAW-2012`, le pouvoir d'édicter des règles sur « les mécanismes de
contrôle et de sécurité dans le domaine de l'informatique » [HT-LAW-2012, p. 29].** Quatre de
ses exigences atterrissent ici.

Sa section 2 exige la disponibilité, l'intégrité, la confidentialité et la traçabilité de
toutes les données traitées par le système d'information [BRH-126, p. 1]. La confidentialité,
ce sont les §4 et §9 ; la traçabilité, c'est le §10.

Sa section 3 f) exige d'une institution qu'elle mette en place « un système de gestion
sécurisé de l'accès pour les données nécessaires à l'application et à l'exécution de ses
opérations » [BRH-126, p. 2]. Ce sont les §3, §4 et §6 ensemble : une présentation unique, un
condensé stocké, et des portées.

Sa section 2 prévoit également que là où un tiers traite des données pour le compte d'une
institution, les normes minimales de sécurité doivent être « contrôlée par l'institution qui
confie les travaux à ces tiers » [BRH-126, p. 1]. Le modèle auto-hébergé n'a pas de tel tiers,
ce qui est la façon la plus simple de satisfaire une obligation de contrôle. C'est aussi le
cadre qui s'appliquerait au déploiement hébergé que
[ADR-0001](0001-architecture-and-scope.md) laisse ouvert : la circulaire n'interdit pas un
tiers, elle place le contrôle sur l'institution.

Sa section 3 t) exige un audit de sécurité informatique au moins tous les trois ans
[BRH-126, p. 4], et ce sont les enregistrements du §10 qu'un auditeur lirait.

**`BRH-131` atteint les règles sur les identifiants par la protection des données.** Elle
exige le principe de minimisation, « seules les données strictement nécessaires doivent être
recueillies » [BRH-131, p. 18, s. 6.10.2 c)], et un registre des traitements consignant, par
catégorie, la nature des données, la finalité, la base légale et la durée de conservation
[BRH-131, p. 19, s. 6.10.5 c)]. Le devoir de caviardage du §9.5 sert le premier : un
identifiant de fournisseur réémis dans un champ tourné vers le marchand est une donnée qui sort
sans aucune finalité. Elle exige aussi la notification d'un incident de sécurité aux
consommateurs touchés et à la BRH « sans délai », avec les faits et les mesures correctives
documentés [BRH-131, p. 19, s. 6.10.7], et l'article 84 de `HT-LAW-2012` impose déjà la
notification de « tout incident significatif » au niveau légal [HT-LAW-2012, p. 30]. La
révocation immédiate du §7.3 et l'horodatage de dernière utilisation du §7.8 sont ce qui rend
une réponse rapide et documentée possible plutôt qu'aspirationnelle.

Le troisième point est de périmètre, et c'est le même que fait
[ADR-0001](0001-architecture-and-scope.md). Les identifiants que cette ADR protège sont
ceux du marchand, détenus sur l'infrastructure propre du marchand. Le projet n'en détient
aucun, n'en émet aucun, et n'exploite rien qui le pourrait. Rien ici ne crée une partie que la
circulaire aurait besoin d'agréer, et un marchand qui déploie la passerelle reste le client
d'un fournisseur agréé exactement comme avant.

## Alternatives envisagées

**OAuth 2.0 en client credentials.** La réponse institutionnelle évidente, et rejetée comme
exigence. Sa machinerie mérite son coût quand un serveur de ressources doit faire confiance à
des jetons frappés par une partie qu'il n'exploite pas, ce qui est précisément l'inverse de la
situation ici : la passerelle émet l'identifiant, le détient, et le valide, de sorte que le
point d'accès de jeton ajoute un aller-retour, une expiration à traiter dans chaque SDK, et un
chemin de rafraîchissement à rater, en échange d'une indirection sans seconde partie dedans.
[ADR-0001](0001-architecture-and-scope.md) le cadre déjà comme justifié seulement là où il
y a un serveur d'autorisation, et le §1.3 laisse la place d'en mettre un devant un déploiement
qui a d'autres raisons d'en vouloir un.

**Des JWT autoémis comme identifiants porteurs.** Attrayants parce que la passerelle pourrait
valider sans recherche. Rejetés parce que la révocation exige alors la recherche de toute
façon, ce qui supprime le seul avantage, et qu'un JWT invite la portée et l'expiration à
voyager dans une charge utile analysable et altérable, contre le §2.6. Les modes de défaillance
de la validation JWT, l'`alg` à `none` en tête, sont un prix élevé pour économiser une lecture
en base.

**Une signature de requête HMAC du client vers la passerelle.** Symétrique avec
[ADR-0008](0008-webhooks-and-event-delivery.md), et rejetée pour la raison donnée sous
*Considérations de sécurité* : elle résout l'authentification d'origine, que TLS résout déjà
dans cette direction, et elle met une implémentation de canonicalisation dans chaque SDK
client. Là où un déploiement a réellement besoin d'une signature de requête, la RFC 9421 est
déjà dans la spécification et peut être superposée au titre du §1.3.

**Le TLS mutuel comme identifiant client principal.** Solide, et rejeté comme exigence pour la
même raison que [ADR-0008](0008-webhooks-and-event-delivery.md) le rejette là-bas : il
authentifie la connexion plutôt que la requête, de sorte qu'il ne survit pas à un mandataire
terminant, et il fait de l'identifiant un problème de cycle de vie de certificat pour des
marchands qui intègrent un tunnel d'achat. Il reste disponible au titre du §1.3 pour les
déploiements équipés pour cela.

**Une clé unique sans portées.** Plus simple, et ce que livrent la plupart des petites API de
paiement. Rejetée parce que la tâche de rapprochement du §6.9 est un cas réel : une intégration
qui n'a qu'un identifiant donne à chaque processus la capacité de déplacer de l'argent, et le
coût de l'alternative est une comparaison de chaîne par requête.

**Stocker un condensé lent de la clé.** Rejeté au §4.3, contre le conseil habituel, et le
raisonnement y est consigné parce qu'il sera sinon soulevé à nouveau par chaque relecteur qui
sait comment stocker un mot de passe.

**Des portées par fournisseur**, telles que `payments:write:moncash`. Réellement utiles pour
un marchand qui exploite plusieurs fournisseurs, et différées plutôt que rejetées. Elles
multiplient l'espace des portées par le registre des fournisseurs, et elles interagissent avec
la question ouverte de [ADR-0007](0007-capability-discovery.md) sur les capacités par
principal. Les deux devraient être tranchées ensemble ou pas du tout.

## Questions non résolues

**Si les capacités devraient être filtrées par principal.**
[ADR-0007](0007-capability-discovery.md) laisse cela ouvert, et le §6 ne le ferme pas. Un
principal sans `payments:write` ne devrait sans doute pas s'entendre dire que la passerelle
peut créer des paiements. Le contre-argument est que la découverte de capacités décrit le
déploiement plutôt que l'appelant, et que la filtrer ferait diverger deux clients sur ce que la
même passerelle sait faire.

**Si une clé devrait pouvoir expirer par défaut.** Le §7.6 rend l'expiration optionnelle parce
qu'un identifiant qui cesse de fonctionner sans surveillance est une panne. Une expiration par
défaut avec des avertissements bruyants est peut-être le meilleur compromis, et rien ici ne le
décide.

**Comment un opérateur émet une clé.** Le §7 spécifie les propriétés, *Hors périmètre* exclut
la surface, et l'écart est réel : deux passerelles auront deux interfaces d'administration, et
un marchand qui passe de l'une à l'autre ne trouvera rien de familier. Savoir si cette surface
mérite une ADR Informational est une question ouverte.

**Si le caviardage du §9.5 peut être rendu testable en général.** Le §11.2 le teste contre une
simulation qui réémet des identifiants. Un fournisseur qui transforme un identifiant avant de
le réémettre, en le tronquant ou en le hachant, défait la comparaison de valeurs, et le
filtrage de motifs est explicitement rejeté au §9.5. Il n'y a peut-être aucune réponse
complète, et le dire vaut mieux que laisser entendre qu'il y en a une.

## Références

Citations complètes dans [`references.md`](references.md).

**Normatives.** `RFC9110` pour le schéma `Bearer` et `WWW-Authenticate`, `RFC2119` et
`RFC8174` pour les mots-clés d'exigence.

**Informatives.** `HT-LAW-2012` articles 83, 84 et 161 pour la base légale ; `BRH-126` pour
les exigences de sécurité de l'information auxquelles cette ADR répond ; `BRH-131` pour la
minimisation des données, le registre des traitements et la notification d'incident ;
`BRH-121` pour la traçabilité. `RFC9421` pour la signature utilisée dans l'autre direction,
discutée sous *Considérations de sécurité*.

## Implémentation de référence

Aucune pour l'instant.

## Errata

Aucun.
