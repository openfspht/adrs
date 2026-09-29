# Conformité

Décision : [ADR-0015](../text/0015-conformance-levels-and-suite.md).

## 1. Définition

**1.1.** Une affirmation de conformité est un triplet : cible, niveau, version du protocole. Une
affirmation incomplète n'est pas reconnue, et une implémentation NE DOIT PAS la présenter comme
telle.

**1.2.** La conformité vaut pour une version de la spécification ; un résultat obtenu sur une
version majeure ne dit rien d'une autre.

**1.3.** La conformité est une propriété d'une configuration de déploiement, pas d'un code
source.

**1.4.** Un résultat est daté et reproductible : même implémentation, même version de suite et
même configuration DOIVENT donner le même résultat ([serveur simulé §6](serveur-simule.md)).

## 2. Cibles

**2.1.**

| Cible | Testé | Remplacé par |
|---|---|---|
| Client | Application ou SDK qui appelle une passerelle. | Une passerelle de référence conforme. |
| Passerelle | Serveur implémentant le protocole. | Le [serveur simulé](serveur-simule.md) comme opérateur. |
| Opérateur natif | Opérateur implémentant OpenFSP directement. | Rien. |

**2.2.** La conformité client porte sur l'usage des réponses : récupération par référence,
URL de retour non probante, réutilisation de la clé d'idempotence, paiement durablement
`pending`.

**2.3.** La conformité passerelle est le cas principal (§5).

**2.4.** La conformité opérateur natif reprend les tests passerelle, moins ceux qui supposent un
opérateur derrière l'implémentation (§5.7).

**2.5.** Une exécution vise une seule cible.

## 3. Niveaux

**3.1.** **Core** : la capacité de base ([API §2](api-paiements.md)) et tout ce qui est
obligatoire quelle que soit la capacité : modèle de données, cycle de vie, idempotence, erreurs,
authentification, découverte de capacités, plafonds lorsqu'ils sont déclarés, tests de refus
du §5.4 hors ceux du §5.4.1.

**3.2.** Core est obligatoire : sans lui, une implémentation n'est pas conforme.

**3.3.** Un profil porte le nom de la capacité testée. Un profil NE DOIT PAS être revendiqué pour
une capacité non annoncée.

| Profil | Capacité | Spécification |
|---|---|---|
| `payments.lookup` | Consultation autoritative | [capacités §5](capacites.md) |
| `payments.statement` | Relevé de l'opérateur | [cycle de vie §6.7](cycle-de-vie.md), [relevés](releves.md) |
| `webhooks.per_payment_url` | URL de rappel propre au paiement | [cycle de vie §6.6](cycle-de-vie.md) |
| `webhooks.emit` | Événements signés | [webhooks](webhooks.md) |
| `confirmation_requests` | Décision minutée du payeur | [demandes de confirmation](demandes-de-confirmation.md) |
| `confirmation_requests.cancel` | Retrait avant réponse | [demandes de confirmation §7](demandes-de-confirmation.md) |
| `payments.proximity_cpm` | Paiement au comptoir | [proximité](proximite.md) |

**3.4.** La spécification d'une capacité DOIT définir les tests de son profil.

**3.5.** Pas de réussite partielle : un test Core échoué fait échouer Core. La suite NE DOIT PAS
produire de résultat suggérant le contraire.

**3.6.** Réussir tous les profils ne constitue pas un niveau supplémentaire.

## 4. Exécution

**4.1.** La suite est un programme, exécuté par qui veut le résultat, contre l'implémentation
qu'il désigne ; elle produit le rapport du §7.

**4.2.** Pour une passerelle, la suite joue le client et le serveur simulé joue les opérateurs.

**4.3.** La suite NE DOIT PAS exiger de modification, d'instrumentation ou de mode de test de
l'implémentation.

**4.4.** Seule la configuration est permise : pointer la passerelle vers le simulateur, fournir
des identifiants de test et la clé de dérivation des identifiants de commande
([idempotence §7.2](idempotence.md)).

**4.5.** La suite pilote directement la surface de contrôle du simulateur
([serveur simulé §5](serveur-simule.md)).

**4.6.** La suite DOIT être exécutable hors ligne, en intégration continue, sans compte.

**4.7.** Un test qui exige une action d'administration de la passerelle (attestation,
révocation de clé, déclaration de bornes) est marqué assisté : la suite décrit l'action, un
opérateur l'exécute par l'administration de la passerelle, et le rapport signale le test comme
assisté. Ce n'est pas une modification de l'implémentation au sens du §4.3.

## 5. Contenu

**5.1. Forme.** Types de média ([API §1.4](api-paiements.md)), enveloppe de collection
([API §1.12](api-paiements.md)), `Request-Id` ([API §1.8](api-paiements.md)), problem details
([erreurs §1](erreurs.md)), `Money` entier ([modèle de données §3](modele-de-donnees.md)),
horodatages UTC ([modèle de données §7](modele-de-donnees.md)), requêtes strictes et réponses
tolérantes ([modèle de données §2.3, §2.4](modele-de-donnees.md)).

**5.2. Cycle de vie.** Chaque transition du [cycle de vie §2](cycle-de-vie.md) est atteignable ;
aucun état terminal n'est quitté ; un rapport contradictoire du simulateur produit un conflit, pas
une transition ([cycle de vie §2.2](cycle-de-vie.md)) ; `failure_reason` est présent si et
seulement si `status` vaut `failed`.

**5.3. Idempotence.** Rejeu de la réponse enregistrée ([idempotence §3.2](idempotence.md)) ; même
clé, autre corps rejeté ([idempotence §3.3](idempotence.md)) ; doublon concurrent en
`idempotency-request-in-progress` ; cloisonnement par principal ([idempotence §2.3](idempotence.md)) ;
`reference` en double rejetée de façon permanente.

**5.4. Refus.** Chaque test ne réussit que si l'implémentation refuse :

| Test | Attendu | Règle | Simulateur |
|---|---|---|---|
| Synchroniser sans `payments.lookup` | `capability-not-supported`, pas d'état stocké présenté comme relu | [capacités §5.3](capacites.md) | `mock_epsilon`, `PENDING_FOREVER` |
| Synchroniser un paiement terminal sans `payments.lookup` | paiement inchangé, `200` | [capacités §5.3.1](capacites.md) | `mock_epsilon`, `SUCCESS` |
| Opération d'une capacité non annoncée | `capability-not-supported` | [capacités §4.4](capacites.md) | `mock_beta`, `SUCCESS` |
| `POST` sans `Idempotency-Key` | `idempotency-key-required` | [idempotence §1.3](idempotence.md) | aucun |
| Dénouement indéterminé, opérateur sans idempotence ni recherche | paiement `pending`, aucun renvoi | [idempotence §7.3](idempotence.md) | `mock_beta`, `TIMEOUT` |
| Statut d'opérateur inconnu | paiement `pending` | [cycle de vie §1.1](cycle-de-vie.md) | `mock_alpha`, `UNKNOWN_STATUS` |
| Rappel non signé, hors URL propre, annonçant un succès | aucune transition | [cycle de vie §6.3](cycle-de-vie.md) | `mock_alpha`, `PENDING_FOREVER`, rappel forgé par la suite |
| Rappel sur URL propre avec jeton erroné | rejet sans effet | [cycle de vie §6.6](cycle-de-vie.md) | `mock_epsilon`, `PENDING_FOREVER`, rappel forgé par la suite |
| Relevé sans le paiement, `expires_at` non écoulé | paiement `pending`, pas d'`expired` | [cycle de vie §5.3, §6.7](cycle-de-vie.md) | `mock_epsilon`, `PENDING_FOREVER` |
| Requête de l'API tentant de fixer l'état d'un paiement | état inchangé | [cycle de vie §6.8](cycle-de-vie.md) | `mock_beta`, `PENDING_FOREVER` |
| Opérateur renvoyant des identifiants dans une erreur | `[redacted]` dans `provider_detail` | [authentification §9.5, §9.6](authentification.md) | `mock_alpha`, `CREDENTIAL_ECHO` |
| Clé inconnue, révoquée, d'un autre environnement | trois `unauthenticated` indiscernables | [authentification §4.7](authentification.md) | aucun ; assisté (§4.7) |
| `payer_token` et `payer` ensemble | `invalid-field` | [proximité §3.2](proximite.md) | `mock_gamma` |

**5.4.1.** Les tests « Rappel sur URL propre avec jeton erroné » et « `payer_token` et `payer`
ensemble » relèvent des profils `webhooks.per_payment_url` et `payments.proximity_cpm`. Une passerelle qui n'annonce
pas ces capacités n'y est pas soumise ; pour elle, `payer_token` est un champ inconnu
([modèle de données §2.4](modele-de-donnees.md)).

**5.5.** Chaque test qui dépend d'un comportement d'opérateur nomme le scénario du simulateur
qu'il utilise ([serveur simulé §4.3](serveur-simule.md)). Un scénario sans test, ou un tel test
sans scénario, est un défaut. Le rapport contradictoire du §5.2 utilise `CONTRADICT`, l'écart
de montant du [cycle de vie §6.3.2](cycle-de-vie.md) utilise `AMOUNT_MISMATCH`.

**5.6.** Limite : une passerelle qui annonce `webhooks.verify` sans vérifier passe tous les tests
fonctionnels. La suite DOIT signaler cette limite (§7.4).

**5.7.** Opérateur natif : tests passerelle moins les lignes du §5.4 portant sur le comportement
de l'opérateur ; les refus sur ses propres capacités s'appliquent.

**5.8.** Tests client : réutilisation de la clé ([idempotence §8.1](idempotence.md)), pas de renvoi
d'un `4xx` non rejouable ([idempotence §8.2](idempotence.md)), récupération par référence
([API §5.2.3](api-paiements.md)), URL de retour non probante ([API §7.3](api-paiements.md)),
tolérance aux membres inconnus, paiement durablement `pending`, et pour les abonnés, vérification
avant action ([webhooks §5.9](webhooks.md)) avec sondage fonctionnel quand tout événement est
retenu ([webhooks §10.2](webhooks.md)).

**5.9.** La suite DOIT couvrir chaque exigence observable par au moins un test, et le rapport DOIT
expliciter la correspondance test-exigence.

## 6. Versions

**6.1.** La suite teste une seule version mineure du protocole et DOIT refuser une version
majeure qu'elle ne connaît pas.

**6.2.** Un résultat nomme la version de la suite, la version du protocole, la cible, le niveau,
les profils, la date et la configuration.

**6.3.** Un résultat ne vaut que pour la configuration qui l'a produit : obtenu contre le
simulateur, il ne prouve rien sur un opérateur réel.

**6.4.** Un résultat devient périmé quand l'implémentation ou la version du protocole change.
Une implémentation qui cite un résultat DOIT citer sa propre version.

**6.5.** Une version corrective PEUT ajouter des tests ; les notes de version de la suite DOIVENT
le signaler.

## 7. Rapport

**7.1.** Le rapport est lisible par machine ; seul son contenu est spécifié.

**7.2.** Il porte le triplet du §1.1, la version de la suite, la date, la configuration, un
résultat par test et l'exigence correspondante.

**7.3.** Un test échoué indique l'attendu et l'observé.

**7.4.** Le rapport DOIT mentionner les limites du §5.6 à chaque exécution, même réussie.

**7.5.** Une implémentation qui publie un rapport DEVRAIT publier la configuration permettant de le
reproduire.

**7.6.** Les revendications fondées sur un rapport relèvent de l'[ADR-0016](../text/0016-conformance-marks-and-naming.md).

## 8. Sécurité

**8.1.** Un rapport de conformité n'est pas un audit de sécurité (§5.6, §7.4).

**8.2.** La suite NE DOIT PAS exiger d'identifiant d'opérateur réel ; elle s'exécute contre le
[serveur simulé](serveur-simule.md) avec des identifiants de test.
