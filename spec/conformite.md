# Conformité

Je justifie ces choix dans l'[ADR-0015](../text/0015-conformance-levels-and-suite.md) et rattache
chaque règle à son test dans la [matrice de conformité](matrice-de-conformite.md).

## 1. Définition

**1.1.** Une affirmation de conformité est un triplet : cible, niveau, version du protocole. Une
affirmation incomplète n'est pas reconnue ; la partie qui la publie NE DOIT PAS la présenter
comme telle.

**1.2.** La conformité vaut pour une version de la spécification ; un résultat sur une version
majeure ne vaut pas pour une autre.

**1.3.** La conformité est une propriété d'une configuration de déploiement, pas d'un code
source.

**1.4.** Un résultat est daté et reproductible : même implémentation, même version de suite et
même configuration DOIVENT donner le même résultat (9.6).

## 2. Cibles

**2.1.**

| Cible | Testé | Remplacé par |
|---|---|---|
| Client | Application ou SDK qui appelle une passerelle. | Une passerelle de référence conforme. |
| Passerelle | Serveur implémentant le protocole. | Le serveur simulé (9) comme opérateur. |
| Opérateur natif | Opérateur implémentant OpenFSP directement. | Rien. |

**2.2.** La conformité client porte sur l'usage des réponses : récupération par référence,
URL de retour non probante, réutilisation de la clé d'idempotence, paiement durablement
`pending`.

**2.3.** Le 5 définit les tests de la cible passerelle.

**2.4.** Tests de la cible opérateur natif : 5.7.

**2.5.** Une exécution vise une seule cible.

## 3. Niveaux

**3.1.** **Core** : la capacité de base ([API 2](api-paiements.md)) et tout ce qui est
obligatoire quelle que soit la capacité : modèle de données, cycle de vie, idempotence, erreurs,
authentification, découverte de capacités, plafonds lorsqu'ils sont déclarés, tests de refus
du 5.4 hors ceux du 5.4.1.

**3.2.** Une implémentation qui ne satisfait pas Core n'est pas conforme.

**3.3.** Un profil porte le nom de la capacité testée. Un profil NE DOIT PAS être revendiqué pour
une capacité non annoncée.

| Profil | Capacité | Spécification |
|---|---|---|
| `payments.lookup` | Consultation faisant foi | [capacités 5](capacites.md) |
| `payments.statement` | Relevé de l'opérateur | [cycle de vie 6.7](cycle-de-vie.md), [relevés](cycle-de-vie.md#10-relevés-et-rapprochement) |
| `payments.fee` | Frais rapportés par l'opérateur | [modèle de données 8](modele-de-donnees.md) |
| `webhooks.verify` | Rappels signés par l'opérateur | [cycle de vie 6.5](cycle-de-vie.md) (a) |
| `webhooks.per_payment_url` | URL de rappel propre au paiement | [cycle de vie 6.6](cycle-de-vie.md) |
| `webhooks.emit` | Événements signés | [webhooks](webhooks.md) |

**3.4.** La spécification d'une capacité DOIT définir les tests de son profil.

**3.5.** Un test Core échoué fait échouer Core. La suite NE DOIT PAS
rapporter Core comme réussi lorsqu'un test Core a échoué, ni rapporter un taux de réussite de Core.

**3.6.** Réussir tous les profils ne constitue pas un niveau supplémentaire.

## 4. Exécution

**4.1.** La suite est exécutable par toute partie, contre l'implémentation de son choix ; elle
produit le rapport du 7.

**4.2.** Pour une passerelle, la suite joue le client et le serveur simulé joue les opérateurs.

**4.3.** La suite NE DOIT PAS exiger de modification, d'instrumentation ou de mode de test de
l'implémentation.

**4.4.** Seule la configuration est permise : pointer la passerelle vers le serveur simulé, fournir
des identifiants de test et la clé de dérivation des identifiants de commande
([idempotence 7.2](idempotence.md)).

**4.5.** La suite pilote directement la surface de contrôle du serveur simulé (9.5).

**4.6.** La suite DOIT être exécutable hors ligne, en intégration continue, sans compte.

**4.7.** Un test qui exige une action d'administration de la passerelle (attestation,
révocation de clé, déclaration de bornes) est marqué assisté : la suite décrit l'action, un
exploitant l'exécute par l'administration de la passerelle, le rapport signale le test comme
assisté. Ce n'est pas une modification au sens du 4.3.

## 5. Contenu

**5.1. Forme.** Types de média ([API 1.4](api-paiements.md)), enveloppe de collection
([API 1.12](api-paiements.md)), `Request-Id` ([API 1.8](api-paiements.md)), problem details
([API 10.1](api-paiements.md)), `Money` entier ([modèle de données 3](modele-de-donnees.md)),
horodatages UTC ([modèle de données 7](modele-de-donnees.md)), requêtes strictes et réponses
tolérantes ([modèle de données 2.3, 2.4](modele-de-donnees.md)).

**5.2. Cycle de vie.** Chaque transition du [cycle de vie 2](cycle-de-vie.md) est atteignable ;
aucun état terminal n'est quitté ; un rapport contradictoire du serveur simulé produit un conflit, pas
une transition ([cycle de vie 2.2](cycle-de-vie.md)) ; `failure_reason` est présent si et
seulement si `status` vaut `failed`.

**5.3. Idempotence.** Rejeu de la réponse enregistrée ([idempotence 3.2](idempotence.md)) ; même
clé, autre corps rejeté ([idempotence 3.3](idempotence.md)) ; doublon concurrent jamais
exécuté en parallèle, mis en attente ou rejeté en `idempotency-request-in-progress` avec
`Retry-After` ([idempotence 3.4](idempotence.md)) ; cloisonnement par principal ([idempotence 2.3](idempotence.md)) ;
`reference` en double rejetée de façon permanente.

**5.4. Refus.** Chaque test vérifie un refus ou une absence d'effet :

| Test | Attendu | Règle | Serveur simulé |
|---|---|---|---|
| Synchroniser sans `payments.lookup` | `capability-not-supported`, pas d'état stocké présenté comme relu | [capacités 5.3](capacites.md) | `mock_epsilon`, `PENDING_FOREVER` |
| Synchroniser un paiement terminal sans `payments.lookup` | paiement inchangé, `200` | [capacités 5.3.1](capacites.md) | `mock_epsilon`, `SUCCESS` |
| Opération d'une capacité non annoncée | `capability-not-supported` | [capacités 4.4](capacites.md) | `mock_beta`, `SUCCESS` |
| `POST` sans `Idempotency-Key` | `idempotency-key-required` | [idempotence 1.3](idempotence.md) | aucun |
| Dénouement indéterminé, opérateur sans idempotence ni recherche | paiement `pending`, aucun renvoi | [idempotence 7.3](idempotence.md) | `mock_beta`, `TIMEOUT` |
| Statut d'opérateur inconnu | paiement `pending` | [cycle de vie 1.1](cycle-de-vie.md) | `mock_alpha`, `UNKNOWN_STATUS` |
| Rappel non signé, hors URL propre, annonçant un succès | aucune transition | [cycle de vie 6.3](cycle-de-vie.md) | `mock_alpha`, `PENDING_FOREVER`, rappel forgé par la suite |
| Rappel sur URL propre avec jeton erroné | rejet sans effet | [cycle de vie 6.6](cycle-de-vie.md) | `mock_epsilon`, `PENDING_FOREVER`, rappel forgé par la suite |
| Relevé sans le paiement, `expires_at` non écoulé | paiement `pending`, pas d'`expired` | [cycle de vie 5.3, 6.7](cycle-de-vie.md) | `mock_epsilon`, `PENDING_FOREVER` |
| Requête de l'API tentant de fixer l'état d'un paiement | état inchangé | [cycle de vie 6.8](cycle-de-vie.md) | `mock_beta`, `PENDING_FOREVER` |
| Opérateur renvoyant des identifiants dans une erreur | `[redacted]` dans `provider_detail` | [authentification 9.5, 9.6](authentification.md) | `mock_alpha`, `CREDENTIAL_ECHO` |
| Clé inconnue, révoquée, d'un autre environnement | trois `unauthenticated` indiscernables | [authentification 4.7](authentification.md) | aucun ; assisté (4.7) |

**5.4.1.** Le test « Rappel sur URL propre avec jeton erroné » relève du profil
`webhooks.per_payment_url` ; une passerelle qui n'annonce pas cette capacité n'y est pas soumise.

**5.5.** Chaque test qui dépend d'un comportement d'opérateur nomme son scénario du serveur simulé
(9.4.3) ; tout scénario a au moins un test. Le rapport contradictoire du 5.2 utilise `CONTRADICT`, l'écart de montant du [cycle de vie 6.3.2](cycle-de-vie.md) utilise `AMOUNT_MISMATCH`.

**5.6.** Limite : une passerelle qui annonce `webhooks.verify` sans vérifier passe tous les tests
fonctionnels. La suite DOIT le signaler (7.4).

**5.7.** Opérateur natif : tests passerelle moins les lignes du 5.4 portant sur le comportement
de l'opérateur ; les refus sur ses propres capacités s'appliquent.

**5.8.** Tests client : réutilisation de la clé ([idempotence 8.1](idempotence.md)), pas de renvoi
d'un `4xx` non rejouable ([idempotence 8.2](idempotence.md)), récupération par référence
([API 5.2.3](api-paiements.md)), URL de retour non probante ([API 7.3](api-paiements.md)),
tolérance aux membres inconnus, paiement durablement `pending`, et pour les abonnés, vérification
avant action ([webhooks 5.9](webhooks.md)) avec sondage fonctionnel quand tout événement est
retenu ([webhooks 10.2](webhooks.md)).

**5.9.** La suite DOIT couvrir chaque exigence observable par au moins un test, et le rapport DOIT
expliciter la correspondance test-exigence.

**5.10. Défaillances d'opérateur.** Chaque test exerce un scénario du 9.4.3 ; le journal est
celui du 9.5.5 :

| Test | Attendu | Règle | Serveur simulé |
|---|---|---|---|
| Refus de l'opérateur | synchronisation `200`, `failed`, `failure_reason` `declined`, `failure_detail` portant le code et le message de l'opérateur inaltérés | [cycle de vie 7.2, 7.4](cycle-de-vie.md), [API 10.2.2](api-paiements.md) | `mock_alpha`, `DECLINE` |
| Fonds insuffisants | synchronisation `200`, `failed`, `failure_reason` `insufficient_funds` | [cycle de vie 7.2](cycle-de-vie.md) | `mock_alpha`, `INSUFFICIENT` |
| Création sans réponse, paiement réussi chez l'opérateur, renvoi de même clé | `504 provider-timeout`, `effect` `unknown` ; une seule création au journal ; `succeeded` après synchronisation | [API 5.1.6](api-paiements.md), [idempotence 7.1, 7.2](idempotence.md) | `mock_alpha`, `TIMEOUT_THEN_SUCCESS` |
| Création sans réponse, aucun paiement chez l'opérateur, renvoi de même clé | `504 provider-timeout`, `effect` `unknown` ; au journal, une consultation précède toute seconde création ; aucun état terminal sans source faisant foi | [idempotence 7.1](idempotence.md), [cycle de vie 3.2](cycle-de-vie.md) | `mock_alpha`, `TIMEOUT_THEN_NOTHING` |
| Échéance atteinte chez l'opérateur | `expired` après synchronisation, `completed_at` présent | [cycle de vie 4, 5.3](cycle-de-vie.md) (a) | `mock_alpha`, `EXPIRE`, horloge avancée (9.5.1) |
| Dénouement sans rappel, opérateur avec consultation | état rapporté par la consultation, après synchronisation | [capacités 5.2](capacites.md) | `mock_alpha`, `NO_CALLBACK` |
| Dénouement sans rappel, relevé seul | état terminal correspondant à la mention du relevé | [cycle de vie 6.5, 6.7](cycle-de-vie.md) | `mock_epsilon`, `NO_CALLBACK` |
| Rappel tardif sur un paiement terminal | paiement inchangé ; aucun événement si `webhooks.emit` est annoncée | [cycle de vie 3.1](cycle-de-vie.md), [webhooks 11.1](webhooks.md) | `mock_alpha`, `LATE_CALLBACK`, terminal par synchronisation puis rappel livré (9.5.1) |
| Même rappel signé reçu plusieurs fois | une seule transition, `completed_at` inchangé ; un seul événement de transition si `webhooks.emit` est annoncée | [cycle de vie 3.1, 4.3](cycle-de-vie.md), [webhooks 11.1](webhooks.md) | `mock_alpha`, `DUPLICATE_CALLBACK` |
| Erreur de l'opérateur à la création | `502 provider-error`, `retryable` `true`, `effect` `unknown` ; `provider_detail`, s'il est présent, égal au code et au message de l'opérateur ; renvoi de même clé sans `Idempotent-Replay` | [API 10.6.5, 10.8.2, 10.9.6](api-paiements.md) | `mock_alpha`, `PROVIDER_ERROR` |
| Connexion refusée à la création | `503 provider-unavailable`, `retryable` `true`, `effect` `none` | [API 10.9.6, 10.9.6.1](api-paiements.md) | `mock_alpha`, `UNREACHABLE` |
| Succès rapporté pour un autre montant | paiement `pending`, jamais `succeeded` ; conflit signalé à l'exploitant | [cycle de vie 6.3.2, 6.4](cycle-de-vie.md) | `mock_alpha`, `AMOUNT_MISMATCH` |

**5.11. Relevés.** Tests du [cycle de vie 10.7.1](cycle-de-vie.md) :

| Test | Attendu | Règle | Serveur simulé |
|---|---|---|---|
| Ligne d'un paiement de la passerelle | `match` `matched`, `payment` égal à l'`id` du paiement | [cycle de vie 10.4.1, 10.4.2](cycle-de-vie.md) | `mock_epsilon`, `SUCCESS` |
| Ligne sans paiement correspondant | `match` `unmatched`, ligne listée par `GET /v1/statement_entries?match=unmatched`, aucun paiement créé | [cycle de vie 10.4.3, 10.6.2](cycle-de-vie.md) | `mock_epsilon` |
| Paiement `succeeded` absent d'un relevé clos | paiement listé dans `missing_payments` | [cycle de vie 10.4.4](cycle-de-vie.md) | `mock_epsilon`, `PENDING_FOREVER`, `succeeded` attesté ; assisté (4.7) |
| Ligne sans date de l'opérateur, comptabilisée le jour d'un changement d'heure | `business_date` égale à la date de `booked_at` dans `America/Port-au-Prince` | [cycle de vie 10.1.2, 10.1.3](cycle-de-vie.md) | `mock_epsilon`, `SUCCESS` |

**5.12. Capacités et identifiant de commande.**

| Test | Attendu | Règle | Serveur simulé |
|---|---|---|---|
| Capacités annoncées pour chaque opérateur simulé | aucun nom réservé ; aucune capacité hors de celles du 9.3.1 | [capacités 1.3, 2.2, 7.2](capacites.md) | `mock_alpha`, `mock_beta`, `mock_epsilon` |
| Montant égal à `min_amount`, puis à `max_amount` | paiement créé (`201`) | [capacités 6.7, 7.3](capacites.md) | `mock_alpha`, `SUCCESS` ; bornes déclarées, assisté (4.7) |
| Montant inférieur d'un centime à `min_amount`, supérieur d'un centime à `max_amount`, non multiple de `amount_step` | `amount-out-of-range` portant les bornes déclarées ; aucune requête au journal (9.5.5) | [capacités 6.7, 7.3](capacites.md) | `mock_alpha`, `SUCCESS` ; bornes déclarées, assisté (4.7) |
| Identifiant de commande | `provider_order_id` égal à l'identifiant calculé par la suite avec la clé de dérivation et à celui reçu au journal (9.5.5) ; le scénario déclaré sous cet identifiant s'applique | [idempotence 7.2](idempotence.md) | `mock_alpha`, `DECLINE` |

**5.13. Authentification.**

| Test | Attendu | Règle | Serveur simulé |
|---|---|---|---|
| Clé absente, mal formée, inconnue, révoquée, expirée, d'un autre environnement | six `unauthenticated` au même `title`, sans `detail` distinctif ; `WWW-Authenticate: Bearer` sur la clé absente | [authentification 3.3, 4.7, 7.6](authentification.md) | aucun ; assisté (4.7) |
| Opérateur renvoyant des identifiants dans le motif d'un échec | `[redacted]` dans `failure_detail` | [authentification 9.5, 9.6](authentification.md) | `mock_alpha`, `CREDENTIAL_ECHO` |

**5.14.** Les tests du 5.11 et le test « Dénouement sans rappel, relevé seul » du 5.10 relèvent
du profil `payments.statement` ; une passerelle qui n'annonce pas cette capacité n'y est pas
soumise.

## 6. Versions

**6.1.** La suite teste une seule version mineure du protocole et DOIT refuser une version
majeure qu'elle ne connaît pas.

**6.2.** Un résultat nomme la version de la suite, la version du protocole, la cible, le niveau,
les profils, la date et la configuration.

**6.3.** Un résultat ne vaut que pour la configuration qui l'a produit : obtenu avec le
serveur simulé, il ne vaut pas pour un opérateur réel (9.8).

**6.4.** Un résultat devient périmé quand l'implémentation ou la version du protocole change.
La partie qui cite un résultat DOIT citer la version de l'implémentation testée.

**6.5.** Une version corrective PEUT ajouter des tests ; les notes de version de la suite DOIVENT
le signaler.

## 7. Rapport

**7.1.** Le rapport est lisible par machine ; seul son contenu est spécifié.

**7.2.** Il porte le triplet du 1.1, la version de la suite, la date, la configuration, un
résultat par test et l'exigence correspondante.

**7.3.** Un test échoué indique l'attendu et l'observé.

**7.4.** Le rapport DOIT mentionner les limites du 5.6 à chaque exécution, même réussie.

**7.5.** La partie qui publie un rapport DEVRAIT publier la configuration permettant de le
reproduire.

**7.6.** Les revendications fondées sur un rapport relèvent de la
[gouvernance 8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité).

## 8. Sécurité

**8.1.** Un rapport de conformité n'est pas un audit de sécurité (5.6, 7.4).

**8.2.** La suite NE DOIT PAS exiger de secret d'opérateur réel ; elle s'exécute contre le
serveur simulé (9) avec des identifiants de test.

## 9. Serveur simulé

Les règles du 9 obligent le serveur simulé. La dernière phrase du 9.4.2, le 9.7.3 et le
9.7.6 obligent aussi la passerelle.

### 9.1. Rôle

**9.1.1.** Le serveur simulé remplace les opérateurs. Une passerelle configurée contre lui exécute
ses adaptateurs, sa machine à états et son traitement des rappels ordinaires.

**9.1.2.** Il teste la passerelle et le client (limites : 9.8).

**9.1.3.** Il ne simule que les capacités spécifiées ([capacités 2.2](capacites.md)).

### 9.2. Règle directrice

**9.2.1.** Pour chaque comportement où les opérateurs documentés diffèrent
([architecture 8](architecture.md#8-profils-observés)), le serveur simulé reproduit celui qui impose le
plus de contraintes à la passerelle.

**9.2.2.** Il n'invente pas de capacité, et chaque capacité facultative manque à au moins un
opérateur simulé.

### 9.3. Opérateurs simulés

**9.3.1.**

| Opérateur | Capacités | Cas exercé |
|---|---|---|
| `mock_alpha` | `payments`, `payments.lookup`, `webhooks.verify` | Rappels signés, consultation. |
| `mock_beta` | `payments` | Aucune source automatique : chaque paiement attend une attestation ; [idempotence 7.3](idempotence.md). |
| `mock_epsilon` | `payments`, `webhooks.per_payment_url`, `payments.statement` | Ni signature ni consultation ; URL propre et relevé (9.3.5). |

**9.3.2.** `mock_beta` exerce le chemin d'attestation ([cycle de vie 6.8](cycle-de-vie.md)) et
l'absence de renvoi automatique.

**9.3.3.** Le paiement au comptoir est reporté : aucun opérateur simulé n'en annonce les
capacités.

**9.3.4.** Les identifiants des opérateurs simulés utilisent le préfixe `mock_`, réservé par le
[registre](https://github.com/openfspht/openfsp/blob/main/registries/providers.md). Aucun
opérateur réel n'y reçoit d'identifiant.

**9.3.5.** `mock_epsilon` isole les sources (c) et (d) du [cycle de vie 6.5](cycle-de-vie.md). Avec
`NO_CALLBACK`, la passerelle ne dispose que du relevé ; un rappel sur URL au jeton erroné est
rejeté sans effet.

### 9.4. Défaillances

**9.4.1.** Chaque scénario est choisi de façon déterministe à la création du paiement ; aucun ne
survient sans avoir été demandé.

**9.4.2.** Sélecteur : avant la création, la suite déclare le scénario d'un paiement sur la
surface de contrôle (9.5), sous l'identifiant de commande qu'elle calcule avec la clé de
dérivation fournie en configuration ([idempotence 7.2](idempotence.md),
4.4). La passerelle n'a aucun chemin de code propre au serveur simulé.

**9.4.3.** Scénarios :

| Scénario | Comportement | Règle exercée |
|---|---|---|
| `SUCCESS` | Succès sans délai ajouté ; scénario par défaut (9.4.5). | Chemin nominal. |
| `DECLINE` | Échec, motif de refus. | [Cycle de vie 7.2](cycle-de-vie.md) |
| `INSUFFICIENT` | Échec, fonds insuffisants. | [Cycle de vie 7.2](cycle-de-vie.md) |
| `TIMEOUT` | Requête acceptée, aucune réponse. | [Idempotence 5.2, 7.1](idempotence.md) |
| `TIMEOUT_THEN_SUCCESS` | Aucune réponse, paiement réussi chez l'opérateur. | [Idempotence 7.1](idempotence.md) |
| `TIMEOUT_THEN_NOTHING` | Aucune réponse ; aucun paiement créé chez l'opérateur. | [Idempotence 7.1](idempotence.md) |
| `PENDING_FOREVER` | Reste en attente jusqu'à instruction (9.5). | [Cycle de vie 1.1](cycle-de-vie.md) |
| `EXPIRE` | Expire à l'échéance. | [Cycle de vie 5](cycle-de-vie.md) |
| `NO_CALLBACK` | Dénouement sans rappel. | [Cycle de vie 6.2, 6.5](cycle-de-vie.md) |
| `LATE_CALLBACK` | Rappel très tardif. | Ordre, abonnés inattentifs. |
| `DUPLICATE_CALLBACK` | Même rappel plusieurs fois. | [Cycle de vie 3.1](cycle-de-vie.md) |
| `UNKNOWN_STATUS` | Statut jamais vu. | [Cycle de vie 1.1](cycle-de-vie.md) |
| `PROVIDER_ERROR` | Erreur côté opérateur. | [API 10.9.6](api-paiements.md) |
| `UNREACHABLE` | Connexion refusée. | [API 10.9.6.1](api-paiements.md) |
| `CREDENTIAL_ECHO` | Renvoie les identifiants reçus dans l'erreur. | [Authentification 9.5](authentification.md) |
| `CONTRADICT` | Rapporte un succès, puis un échec à la consultation suivante. | [Cycle de vie 6.4](cycle-de-vie.md) |
| `AMOUNT_MISMATCH` | Rapporte le succès d'un montant différent. | [Cycle de vie 6.3.2](cycle-de-vie.md) |

**9.4.4.** Un scénario n'est ajouté que si une spécification définit un comportement impossible à
provoquer autrement.

**9.4.5.** Un paiement sans scénario déclaré se comporte comme `SUCCESS`.

**9.4.6.** Le serveur simulé répond après un court délai fixe, jamais instantanément.

### 9.5. Contrôle

**9.5.1.** Une surface de contrôle, distincte de l'interface vue par la passerelle, permet de
déclarer le scénario d'un paiement à venir, de résoudre un paiement en attente, de livrer un
rappel retenu et d'avancer l'horloge d'expiration.

**9.5.2.** Elle est pilotée par la suite de tests, jamais par la passerelle.

**9.5.3.** Avancer l'horloge n'affecte que l'expiration côté serveur simulé, pas l'horloge de la
passerelle.

**9.5.4.** Elle est liée à l'interface de bouclage ou placée derrière l'authentification de
l'environnement de test.

**9.5.5.** La surface de contrôle DOIT exposer à la suite le journal des requêtes reçues de la
passerelle, par opérateur simulé : méthode, chemin et corps tels que reçus. La suite y vérifie
un appel à l'opérateur ou son absence sans instrumenter la passerelle (4.3).

### 9.6. Déterminisme

**9.6.1.** Une même séquence de requêtes sur un serveur simulé fraîchement démarré produit la même
séquence de réponses.

**9.6.2.** L'état est propre à l'instance et n'est pas conservé entre redémarrages.

### 9.7. Séparation de la production

**9.7.1.** Tout paiement simulé porte un identifiant `mock_` (9.3.4).

**9.7.2.** Le serveur simulé refuse toute configuration ressemblant à un secret d'opérateur réel ;
ses propres identifiants sont fixes et publiés.

**9.7.3.** Une passerelle configurée contre le serveur simulé l'indique dans son journal de démarrage.

**9.7.4.** Le serveur simulé ne rapporte jamais l'identifiant d'un opérateur réel et ne produit aucun
artefact assimilable à un règlement.

**9.7.5.** Le serveur simulé s'annonce comme des opérateurs distincts, jamais comme l'opérateur imité.

**9.7.6.** Un déploiement pointé vers le serveur simulé est en environnement `test` ; une clé `live`
y est refusée ([authentification 2.3](authentification.md)).

### 9.8. Limites

**9.8.1.** Le serveur simulé ne prouve pas qu'un adaptateur correspond à son opérateur.

**9.8.2.** Il ne prouve pas qu'un opérateur se comporte comme le dit sa documentation.

**9.8.3.** Il ne mesure pas la tenue en charge.

**9.8.4.** Ses scénarios sont dérivés des règles de la spécification ; aucun n'est issu d'une
observation d'opérateur réel.
