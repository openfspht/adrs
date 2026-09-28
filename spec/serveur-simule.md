# Serveur simulé

Informatif. Décision : [ADR-0014](../text/0014-mock-server-behaviour.md).

## 1. Rôle

**1.1.** Le serveur simulé se place là où sont les opérateurs. Une passerelle configurée contre
lui exécute ses adaptateurs, sa machine à états et son traitement des rappels ordinaires.

**1.2.** Il teste la passerelle et le client, pas la fidélité d'un adaptateur à un opérateur réel.

**1.3.** Il est l'implémentation de référence des capacités qu'aucun adaptateur ne peut
atteindre : [demandes de confirmation](demandes-de-confirmation.md) et [proximité](proximite.md).

## 2. Règle directrice

**2.1.** Le simulateur n'est jamais plus permissif qu'un opérateur réel : là où les opérateurs
diffèrent, il prend le comportement le plus strict.

**2.2.** Il n'invente pas de capacité, et chaque capacité facultative manque à au moins un
opérateur simulé.

## 3. Opérateurs simulés

**3.1.**

| Opérateur | Capacités | Cas exercé |
|---|---|---|
| `mock_alpha` | `payments`, `payments.lookup`, `webhooks.verify` | Rappels signés, consultation. |
| `mock_beta` | `payments` | Aucune source automatique : chaque paiement attend une attestation ; [idempotence §7.3](idempotence.md). |
| `mock_gamma` | `payments`, `payments.lookup`, `confirmation_requests`, `confirmation_requests.cancel`, `payments.proximity_cpm` | Flux de comptoir. |
| `mock_delta` | `payments`, `payments.lookup`, `confirmation_requests` | Confirmation sans retrait possible (§3.3). |
| `mock_epsilon` | `payments`, `webhooks.per_payment_url`, `payments.statement` | Ni signature ni consultation ; URL propre et relevé (§3.5). |

**3.2.** `mock_beta` exerce le chemin d'attestation ([cycle de vie §6.8](cycle-de-vie.md)) et
l'absence de renvoi automatique.

**3.3.** `mock_delta` exerce [demandes de confirmation §7.8](demandes-de-confirmation.md) :
`confirmation_requests` sans `confirmation_requests.cancel`.

**3.4.** Les identifiants des opérateurs simulés utilisent le préfixe `mock_`, réservé par le
[registre](https://github.com/openfspht/openfsp/blob/main/registries/providers.md). Aucun
opérateur réel n'y reçoit d'identifiant.

**3.5.** `mock_epsilon` isole les sources (c) et (d) du [cycle de vie §6.5](cycle-de-vie.md). Avec
`NO_CALLBACK`, la passerelle doit attendre le relevé ; un rappel sur URL au jeton erroné est
rejeté sans effet.

## 4. Défaillances

**4.1.** Chaque scénario est choisi de façon déterministe à la création du paiement ; aucun ne
survient sans avoir été demandé.

**4.2.** Sélecteur : une `reference` commençant par `MOCK-<SCENARIO>-`.

**4.3.** Scénarios :

| Scénario | Comportement | Règle exercée |
|---|---|---|
| `SUCCESS` | Dénouement rapide ; défaut sans préfixe. | Chemin nominal. |
| `DECLINE` | Échec, motif de refus. | [Cycle de vie §7.2](cycle-de-vie.md) |
| `INSUFFICIENT` | Échec, fonds insuffisants. | [ISO 20022](iso-20022.md) |
| `TIMEOUT` | Requête acceptée, aucune réponse. | [Idempotence §5.2, §7.1](idempotence.md) |
| `TIMEOUT_THEN_SUCCESS` | Aucune réponse, paiement réussi chez l'opérateur. | [Idempotence §7.1](idempotence.md) |
| `TIMEOUT_THEN_NOTHING` | Aucune réponse, rien ne s'est passé. | [Idempotence §7.1](idempotence.md) |
| `PENDING_FOREVER` | Reste en attente jusqu'à instruction (§5). | [Cycle de vie §1.1](cycle-de-vie.md) |
| `EXPIRE` | Expire à l'échéance. | [Cycle de vie §5](cycle-de-vie.md) |
| `NO_CALLBACK` | Dénouement sans rappel. | [Webhooks §10.2](webhooks.md) |
| `LATE_CALLBACK` | Rappel très tardif. | Ordre, abonnés inattentifs. |
| `DUPLICATE_CALLBACK` | Même rappel plusieurs fois. | [Webhooks §8.4](webhooks.md) |
| `UNKNOWN_STATUS` | Statut jamais vu. | [Adaptateurs §3.2](adaptateurs.md) |
| `PROVIDER_ERROR` | Erreur côté opérateur. | [Erreurs §9.6](erreurs.md) |
| `UNREACHABLE` | Connexion refusée. | [Erreurs §9.6.1](erreurs.md) |
| `CREDENTIAL_ECHO` | Renvoie les identifiants reçus dans l'erreur. | [Authentification §9.5](authentification.md) |
| `APPROVE_THEN_FAIL` | Approuve, puis la capture échoue. | [Demandes de confirmation §5.1](demandes-de-confirmation.md) |
| `CANCEL_RACE` | Approuve à l'arrivée d'une annulation. | [Demandes de confirmation §7.5](demandes-de-confirmation.md) |
| `TOKEN_EXPIRED` | Jeton de payeur expiré. | [Proximité §5.2](proximite.md) |
| `TOKEN_USED` | Jeton de payeur déjà résolu. | [Proximité §5.1.3](proximite.md) |

**4.4.** Un scénario n'est ajouté que si une spécification définit un comportement impossible à
provoquer autrement.

**4.5.** Une référence sans préfixe `MOCK-` se comporte comme `SUCCESS`.

**4.6.** Le simulateur répond après un court délai fixe, jamais instantanément.

## 5. Contrôle

**5.1.** Une surface de contrôle, distincte de l'interface vue par la passerelle, permet de
résoudre un paiement en attente, de livrer un rappel retenu et d'avancer l'horloge d'expiration.

**5.2.** Elle est pilotée par la suite de tests, jamais par la passerelle.

**5.3.** Avancer l'horloge n'affecte que l'expiration côté simulateur, pas l'horloge de la
passerelle.

**5.4.** Elle est liée à l'interface de bouclage ou placée derrière l'authentification de
l'environnement de test.

## 6. Déterminisme

**6.1.** Une même séquence de requêtes sur un simulateur fraîchement démarré produit la même
séquence de réponses.

**6.2.** L'état est propre à l'instance et n'est pas conservé entre redémarrages.

## 7. Séparation de la production

**7.1.** Tout paiement simulé porte un identifiant `mock_` (§3.4).

**7.2.** Le simulateur refuse toute configuration ressemblant à un identifiant d'opérateur réel ;
ses propres identifiants sont fixes et publiés.

**7.3.** Une passerelle configurée contre le simulateur l'indique dans son journal de démarrage.

**7.4.** Le simulateur ne rapporte jamais l'identifiant d'un opérateur réel et ne produit aucun
artefact assimilable à un règlement.

**7.5.** Le simulateur s'annonce comme des opérateurs distincts, jamais comme l'opérateur imité.

**7.6.** Un déploiement pointé vers le simulateur est en environnement `test` ; une clé `live`
y est refusée ([authentification §2.3](authentification.md)).

## 8. Limites

**8.1.** Le simulateur ne prouve pas qu'un adaptateur correspond à son opérateur.

**8.2.** Il ne prouve pas qu'un opérateur se comporte comme le dit sa documentation.

**8.3.** Il ne mesure pas la tenue en charge.

**8.4.** Ses scénarios viennent du raisonnement de la spécification, pas de l'observation
d'opérateurs réels.
