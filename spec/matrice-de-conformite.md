# Matrice de conformité

Je rattache chaque règle numérotée des documents normatifs au test de [conformité 5](conformite.md)
qui la vérifie, ou j'indique pourquoi aucun test ne la vérifie. `check-rules.py` vérifie en intégration continue
que la matrice couvre toutes les règles, et seulement elles. Une règle qui oblige plusieurs parties
a une ligne par partie.

| Sujet | Partie obligée |
|---|---|
| passerelle | La passerelle. |
| opérateur natif | Un opérateur qui expose lui-même le protocole OpenFSP. |
| client | Le client, une bibliothèque cliente, un abonné ou un vérificateur. |
| serveur simulé | Le serveur simulé. |
| suite | La suite de conformité ou son rapport. |
| exploitant | L'exploitant de la passerelle. |
| déclarant | Qui publie une affirmation de conformité ou un rapport. |
| spécification | La spécification elle-même : définition, exemple, évolution, numéro réservé. |

| Vérification | Sens | Détail |
|---|---|---|
| test | Un test de conformité 5 couvre la règle. | Le test. |
| à écrire | Vérifiable en boîte noire, aucun test défini. | Le test à écrire. |
| non testable | Aucune observation extérieure ne l'établit. | La raison. |
| sans objet | Aucun comportement à vérifier. | |

## Modèle de données

| Règle | Sujet | Vérification | Détail |
|---|---|---|---|
| [1](modele-de-donnees.md) | spécification | sans objet | Table de types, règles détaillées aux 3 à 9 |
| [2.1](modele-de-donnees.md) | passerelle | test | conformité 5.1, types de média |
| [2.2](modele-de-donnees.md) | passerelle | à écrire | Vérifier que tout nom de champ de réponse est en `lower_snake_case` |
| [2.3](modele-de-donnees.md) | client | test | conformité 5.8, tolérance aux membres inconnus |
| [2.4](modele-de-donnees.md) | passerelle | test | conformité 5.1, requêtes strictes |
| [2.5](modele-de-donnees.md) | passerelle | à écrire | Champ facultatif à `null` traité comme absent ; obligatoire à `null` rejeté |
| [2.6](modele-de-donnees.md) | passerelle | à écrire | `reference` décomposée relue en NFC, valeur de `metadata` relue à l'identique |
| [2.7](modele-de-donnees.md) | passerelle | à écrire | `amount` envoyé en chaîne, attendre `invalid-field` |
| [3.1](modele-de-donnees.md) | passerelle | à écrire | `Money` sans `currency` ou sans `amount`, attendre `invalid-field` |
| [3.2](modele-de-donnees.md) | passerelle | test | conformité 5.1, `Money` entier |
| [3.3](modele-de-donnees.md) | passerelle | test | conformité 5.1, `Money` entier |
| [3.4](modele-de-donnees.md) | passerelle | à écrire | `amount` à 2⁵³ - 1 accepté, 2⁵³ et -2⁵³ rejetés |
| [3.5](modele-de-donnees.md) | passerelle | non testable | Représentation interne des montants invisible en boîte noire |
| [3.6](modele-de-donnees.md) | passerelle | à écrire | `POST` avec montant nul puis négatif, attendre `invalid-field` |
| [3.7](modele-de-donnees.md) | spécification | sans objet | Définition de l'égalité |
| [3.8](modele-de-donnees.md) | passerelle | à écrire | Opérateur simulé rapportant un montant non exact au centime, aucun arrondi |
| [3.9](modele-de-donnees.md) | passerelle | à écrire | Montant opérateur `1250.005`, attendre `provider-error` ; scénario manquant |
| [4.1](modele-de-donnees.md) | passerelle | à écrire | `POST` avec `currency` `USD`, attendre `invalid-field` |
| [4.2](modele-de-donnees.md) | spécification | sans objet | Requiert une ADR |
| [5.1](modele-de-donnees.md) | passerelle | à écrire | Tout numéro renvoyé vérifié contre la regex E.164 |
| [5.2](modele-de-donnees.md) | spécification | sans objet | Exemples |
| [5.3](modele-de-donnees.md) | passerelle | à écrire | `POST` avec chaque numéro invalide du 5.2, attendre rejet |
| [5.4](modele-de-donnees.md) | passerelle | non testable | « Vérifié » non défini, aucun effet observable désigné |
| [5.5](modele-de-donnees.md) | passerelle | à écrire | Opérateur simulé rapporte `50937007294`, attendre `+50937007294` ; scénario manquant |
| [6.1.1](modele-de-donnees.md) | passerelle | à écrire | Vérifier alphabet, longueur et stabilité de `id` entre lectures |
| [6.1.2](modele-de-donnees.md) | client | non testable | Absence d'analyse de l'identifiant invisible en boîte noire |
| [6.1.3](modele-de-donnees.md) | passerelle | non testable | Encodage de l'UUID dans l'identifiant non spécifié |
| [6.1.4](modele-de-donnees.md) | passerelle | à écrire | Créer plusieurs paiements, rejeter identifiants séquentiels ou à compteur |
| [6.1.5](modele-de-donnees.md) | passerelle | à écrire | Vérifier préfixe `pay_` ou `rfd_`, sinon avertissement |
| [6.2.1](modele-de-donnees.md) | passerelle | à écrire | `reference` de 129 caractères ou caractère interdit, attendre `invalid-field` |
| [6.2.2](modele-de-donnees.md) | passerelle | test | conformité 5.3, `reference` en double rejetée |
| [6.2.3](modele-de-donnees.md) | client | test | conformité 5.8, récupération par référence |
| [6.2.4](modele-de-donnees.md) | passerelle | à écrire | Journal du simulé (9.5.5) : identifiant de commande transmis, jamais la `reference` |
| [6.2.5](modele-de-donnees.md) | spécification | sans objet | Renvoi |
| [6.3.1](modele-de-donnees.md) | passerelle | à écrire | `provider_reference` renvoyée égale à celle du serveur simulé |
| [6.3.2](modele-de-donnees.md) | passerelle | à écrire | Scénario `TIMEOUT`, vérifier `provider_reference` absente |
| [6.3.3](modele-de-donnees.md) | client | non testable | Choix interne de la clé de corrélation non observable |
| [6.4.1](modele-de-donnees.md) | passerelle | à écrire | Clé de 256 caractères ou caractère interdit, attendre rejet |
| [7.1](modele-de-donnees.md) | passerelle | test | conformité 5.1, horodatages UTC |
| [7.2](modele-de-donnees.md) | passerelle | à écrire | Horodatage avec `+00:00`, `z` ou sans heure, attendre `invalid-field` |
| [7.3](modele-de-donnees.md) | passerelle | à écrire | Horodatage sans fraction de seconde accepté en requête |
| [7.4](modele-de-donnees.md) | client | non testable | Usage interne des horodatages par le client non observable |
| [7.5](modele-de-donnees.md) | passerelle | à écrire | Opérateur simulé envoie heure locale sans décalage, vérifier UTC ; scénario manquant |
| [8.1](modele-de-donnees.md) | passerelle | à écrire | `fee` présent porte `amount` en HTG et `bearer` valide |
| [8.2](modele-de-donnees.md) | client | non testable | Affichage des frais côté client hors boîte noire |
| [8.3](modele-de-donnees.md) | passerelle | à écrire | `POST` portant `bearer` ou `fee`, attendre rejet `400` |
| [8.4](modele-de-donnees.md) | passerelle | à écrire | Succès sans frais rapportés, transition terminale immédiate sans `fee` |
| [8.5](modele-de-donnees.md) | passerelle | à écrire | Opérateur sans frais, vérifier `payments.fee` non annoncée |
| [9.1](modele-de-donnees.md) | passerelle | à écrire | Créer avec `metadata`, vérifier sa présence dans chaque représentation |
| [9.2](modele-de-donnees.md) | passerelle | à écrire | 21 clés, clé de 41 caractères, valeur non chaîne : attendre rejet |
| [9.3](modele-de-donnees.md) | passerelle | à écrire | Métadonnées Unicode renvoyées identiques à l'octet près |
| [9.4](modele-de-donnees.md) | passerelle | à écrire | Créer avec `metadata` : aucune valeur dans les requêtes au journal (9.5.5) |
| [9.5](modele-de-donnees.md) | client | non testable | Contenu choisi par le marchand, devoir organisationnel |
| [10.1](modele-de-donnees.md) | passerelle | à écrire | Numéro invalide envoyé, absent du `detail` du problème renvoyé |
| [10.2](modele-de-donnees.md) | passerelle | non testable | Obligation documentaire hors API |

## Cycle de vie et relevés

| Règle | Sujet | Vérification | Détail |
|---|---|---|---|
| [1](cycle-de-vie.md) | passerelle | à écrire | `status` toujours l'une des cinq valeurs, sur chaque scénario |
| [1.1](cycle-de-vie.md) | passerelle | test | conformité 5.4, Statut d'opérateur inconnu |
| [1.2](cycle-de-vie.md) | client | à écrire | bibliothèque cliente recevant un `status` inconnu signale une erreur |
| [2](cycle-de-vie.md) | spécification | sans objet | diagramme, règle portée par le 2.1 |
| [2.1](cycle-de-vie.md) | passerelle | test | conformité 5.2 |
| [2.2](cycle-de-vie.md) | passerelle | test | conformité 5.2 |
| [3.1](cycle-de-vie.md) | passerelle | test | conformité 5.2 |
| [3.2](cycle-de-vie.md) | passerelle | test | conformité 5.10, Création sans réponse, aucun paiement chez l'opérateur |
| [3.3](cycle-de-vie.md) | passerelle | à écrire | `UNREACHABLE` sur `mock_beta` : paiement reste `pending` |
| [3.4](cycle-de-vie.md) | passerelle | sans objet | permission sans contrainte propre |
| [4](cycle-de-vie.md) | passerelle | test | conformité 5.10, Échéance atteinte chez l'opérateur |
| [4.1](cycle-de-vie.md) | passerelle | à écrire | horodatage opérateur décalé : `completed_at` reste l'instant d'enregistrement |
| [4.2](cycle-de-vie.md) | passerelle | à écrire | `updated_at` change à chaque transition observée |
| [4.2](cycle-de-vie.md) | client | à écrire | `updated_at` changé sans transition : la bibliothèque ne signale aucune transition |
| [4.3](cycle-de-vie.md) | passerelle | test | conformité 5.10, Même rappel signé reçu plusieurs fois |
| [5.1](cycle-de-vie.md) | spécification | sans objet | définition |
| [5.2](cycle-de-vie.md) | passerelle | à écrire | `expires_at` écoulé sans source : paiement reste `pending` |
| [5.3](cycle-de-vie.md) | passerelle | test | conformité 5.4, Relevé sans le paiement, `expires_at` non écoulé |
| [5.4](cycle-de-vie.md) | passerelle | à écrire | `EXPIRE` sur `mock_beta` sans attestation : reste `pending` |
| [6.1](cycle-de-vie.md) | passerelle | à écrire | capacités annoncées égales aux sources de chaque opérateur simulé |
| [6.2](cycle-de-vie.md) | passerelle | à écrire | `NO_CALLBACK` sur `mock_alpha` : dénouement relu sans synchronisation demandée |
| [6.3](cycle-de-vie.md) | passerelle | test | conformité 5.4, Rappel non signé, hors URL propre, annonçant un succès |
| [6.3.1](cycle-de-vie.md) | passerelle | à écrire | rappel signé sans le dénouement dans la signature : aucune transition |
| [6.3.2](cycle-de-vie.md) | passerelle | test | conformité 5.5, `AMOUNT_MISMATCH` |
| [6.4](cycle-de-vie.md) | passerelle | test | conformité 5.2, `CONTRADICT` |
| [6.5](cycle-de-vie.md) | passerelle | test | conformité 5.10, Dénouement sans rappel, relevé seul |
| [6.6](cycle-de-vie.md) | passerelle | test | conformité 5.4, Rappel sur URL propre avec jeton erroné |
| [6.7](cycle-de-vie.md) | passerelle | test | conformité 5.4, Relevé sans le paiement, `expires_at` non écoulé |
| [6.8](cycle-de-vie.md) | passerelle | test | conformité 5.4, Requête de l'API tentant de fixer l'état |
| [7.1](cycle-de-vie.md) | passerelle | à écrire | `DECLINE` : lecture en `200` portant un paiement `failed` |
| [7.2](cycle-de-vie.md) | passerelle | test | conformité 5.10, Refus de l'opérateur |
| [7.3](cycle-de-vie.md) | passerelle | à écrire | échec sans motif chez l'opérateur simulé donne `unspecified` |
| [7.4](cycle-de-vie.md) | passerelle | test | conformité 5.10, Refus de l'opérateur |
| [7.5](cycle-de-vie.md) | client | à écrire | bibliothèque cliente traite un `failure_reason` inconnu comme `unspecified` |
| [7.5](cycle-de-vie.md) | spécification | sans objet | évolution de la spécification |
| [8.1](cycle-de-vie.md) | spécification | sans objet | évolution de la spécification |
| [8.2](cycle-de-vie.md) | spécification | sans objet | évolution de la spécification |
| [8.3](cycle-de-vie.md) | passerelle | non testable | aucune capacité spécifiée n'introduit d'état supplémentaire |
| [8.4](cycle-de-vie.md) | spécification | sans objet | évolution de la spécification |
| [8.5](cycle-de-vie.md) | spécification | sans objet | `payments.refund` réservé |
| [9.1](cycle-de-vie.md) | client | non testable | affichage par l'application, hors API |
| [9.1](cycle-de-vie.md) | passerelle | non testable | affichage par la passerelle hors API, sans interface normalisée |
| [9.2](cycle-de-vie.md) | passerelle | à écrire | rafale de créations limitée, seuil non spécifié |
| [9.3](cycle-de-vie.md) | client | non testable | porte sur le contenu d'une documentation |
| [9.4](cycle-de-vie.md) | exploitant | non testable | seuil et seconde validation organisationnels, propres au déploiement |
| [9.5](cycle-de-vie.md) | passerelle | non testable | porte sur le contenu du guide de durcissement |
| [10.1.1](cycle-de-vie.md) | spécification | sans objet | renvoi au modèle de données |
| [10.1.2](cycle-de-vie.md) | passerelle | test | conformité 5.11, Ligne sans date de l'opérateur |
| [10.1.3](cycle-de-vie.md) | passerelle | test | conformité 5.11, Ligne sans date de l'opérateur |
| [10.2.1](cycle-de-vie.md) | spécification | sans objet | définition |
| [10.2.2](cycle-de-vie.md) | passerelle | à écrire | relevé de `mock_epsilon` complet, `missing_payments` vide si non clos |
| [10.2.3](cycle-de-vie.md) | passerelle | à écrire | `GET /v1/statements` renvoie au plus un relevé par journée |
| [10.2.4](cycle-de-vie.md) | passerelle | à écrire | ligne publiée après clôture absente du relevé clos |
| [10.3.1](cycle-de-vie.md) | passerelle | à écrire | lignes portent les champs obligatoires, `payment` si `matched` ou `conflict` |
| [10.3.2](cycle-de-vie.md) | client | à écrire | bibliothèque cliente traite un `type` inconnu comme `adjustment` |
| [10.3.3](cycle-de-vie.md) | passerelle | à écrire | ligne `reversal` négative publiée par `mock_epsilon` servie telle quelle |
| [10.3.4](cycle-de-vie.md) | passerelle | à écrire | ligne sans frais rapportés : `fee_amount` et `net_amount` absents |
| [10.4.1](cycle-de-vie.md) | passerelle | test | conformité 5.11, Ligne d'un paiement de la passerelle |
| [10.4.2](cycle-de-vie.md) | passerelle | test | conformité 5.11, Ligne d'un paiement de la passerelle |
| [10.4.3](cycle-de-vie.md) | passerelle | test | conformité 5.11, Ligne sans paiement correspondant |
| [10.4.4](cycle-de-vie.md) | passerelle | test | conformité 5.11, Paiement `succeeded` absent d'un relevé clos |
| [10.4.5](cycle-de-vie.md) | passerelle | à écrire | ligne contredisant un paiement terminal : paiement inchangé, ligne `conflict` |
| [10.5.1](cycle-de-vie.md) | passerelle | non testable | format d'export propre au portail de chaque opérateur réel |
| [10.5.2](cycle-de-vie.md) | passerelle | à écrire | assisté : import attesté complet sans le paiement, échéance passée, donne `expired` |
| [10.5.3](cycle-de-vie.md) | passerelle | à écrire | assisté : import non attesté reste `complete` à `false` |
| [10.6.1](cycle-de-vie.md) | passerelle | à écrire | paramètre manquant rejeté, journée sans relevé donne `200` et `data` vide |
| [10.6.2](cycle-de-vie.md) | passerelle | test | conformité 5.11, Ligne sans paiement correspondant |
| [10.6.3](cycle-de-vie.md) | passerelle | à écrire | clé sans `statements:read` refusée sur les deux points d'accès |
| [10.6.4](cycle-de-vie.md) | passerelle | à écrire | relevés servis pour `mock_alpha`, qui n'annonce pas `payments.statement` |
| [10.7.1](cycle-de-vie.md) | suite | test | conformité 5.11 |
| [10.8.1](cycle-de-vie.md) | exploitant | non testable | choix des portées accordées par l'exploitant |

## Idempotence

| Règle | Sujet | Vérification | Détail |
|---|---|---|---|
| [1.1](idempotence.md) | passerelle | à écrire | `PATCH` et `DELETE` sans clé, attendre `idempotency-key-required` |
| [1.2](idempotence.md) | passerelle | à écrire | `GET` sans clé, attendre succès |
| [1.3](idempotence.md) | passerelle | test | conformité 5.4, `POST` sans `Idempotency-Key` |
| [1.4](idempotence.md) | passerelle | à écrire | Synchroniser avec et sans clé : jamais exigée, jamais de rejeu |
| [2.1](idempotence.md) | passerelle | à écrire | Clé de 256 caractères ou interdite : `invalid-field` sans `errors`, rien exécuté |
| [2.2](idempotence.md) | client | à écrire | Clés émises par la bibliothèque client au format UUID |
| [2.3](idempotence.md) | passerelle | test | conformité 5.3, cloisonnement par principal |
| [3](idempotence.md) | spécification | sans objet | Notations |
| [3.1](idempotence.md) | passerelle | test | conformité 5.3, rejeu |
| [3.2](idempotence.md) | passerelle | test | conformité 5.3, rejeu |
| [3.3](idempotence.md) | passerelle | test | conformité 5.3, même clé, autre corps |
| [3.4](idempotence.md) | passerelle | test | conformité 5.3, doublon concurrent |
| [3.5](idempotence.md) | passerelle | non testable | Mécanisme d'exclusion interne ; l'effet relève du doublon concurrent |
| [4.1](idempotence.md) | passerelle | à écrire | Même clé, corps réordonné ou réespacé, attendre rejeu |
| [4.2](idempotence.md) | passerelle | à écrire | Même clé et corps, en-têtes ou paramètres différents, attendre rejeu |
| [5.1](idempotence.md) | passerelle | à écrire | Requête invalide renvoyée avec même clé, attendre `Idempotent-Replay: true` |
| [5.2](idempotence.md) | passerelle | à écrire | Scénario `TIMEOUT`, renvoi même clé non servi en rejeu |
| [5.3](idempotence.md) | passerelle | à écrire | Rejeu après transition du paiement, attendre corps initial inchangé |
| [6.1](idempotence.md) | passerelle | non testable | Attente de 24 heures ; lieu de publication non précisé |
| [6.2](idempotence.md) | passerelle | test | conformité 5.3, `reference` en double rejetée de façon permanente |
| [6.3](idempotence.md) | passerelle | test | conformité 5.3 |
| [7.1](idempotence.md) | passerelle | test | conformité 5.10, Création sans réponse, aucun paiement chez l'opérateur |
| [7.2](idempotence.md) | passerelle | test | conformité 5.12, Identifiant de commande |
| [7.2.1](idempotence.md) | spécification | sans objet | Précision de définition |
| [7.3](idempotence.md) | passerelle | test | conformité 5.4, Dénouement indéterminé, opérateur sans idempotence ni recherche |
| [7.4](idempotence.md) | passerelle | non testable | Obligation documentaire par adaptateur |
| [8.1](idempotence.md) | client | test | conformité 5.8, réutilisation de la clé |
| [8.2](idempotence.md) | client | test | conformité 5.8, pas de renvoi d'un `4xx` non rejouable |
| [8.3](idempotence.md) | client | à écrire | Après renvois, la bibliothèque lit la ressource avant de conclure |
| [8.4](idempotence.md) | client | à écrire | Répondre `409` avec `Retry-After`, mesurer le délai avant renvoi |
| [8.5](idempotence.md) | client | non testable | Persistance locale avant envoi invisible côté serveur |
| [9.1](idempotence.md) | passerelle | test | conformité 5.3, cloisonnement par principal |
| [9.2](idempotence.md) | passerelle | à écrire | Rafale de créations par un principal, attendre `rate-limited` |
| [9.3](idempotence.md) | passerelle | non testable | Protection du stockage interne des réponses |

## API et erreurs

| Règle | Sujet | Vérification | Détail |
|---|---|---|---|
| [1](api-paiements.md) | spécification | sans objet |  |
| [1.1](api-paiements.md) | passerelle | à écrire | requête en HTTP clair refusée ; journal de démarrage hors portée |
| [1.2](api-paiements.md) | passerelle | à écrire | tous les points d'accès servis sous `/v1` |
| [1.3](api-paiements.md) | spécification | sans objet |  |
| [1.4](api-paiements.md) | passerelle | test | conformité 5.1 |
| [1.5](api-paiements.md) | passerelle | à écrire | corps en `text/plain` rejeté en `malformed-request` |
| [1.6](api-paiements.md) | passerelle | à écrire | `DELETE /v1/payments/{id}` donne `405` avec `Allow` |
| [1.7](api-paiements.md) | passerelle | test | conformité 5.4, `POST` sans `Idempotency-Key` |
| [1.8](api-paiements.md) | passerelle | test | conformité 5.1 |
| [1.9](api-paiements.md) | passerelle | test | conformité 5.1 |
| [1.10](api-paiements.md) | passerelle | à écrire | `/v1/payments/` traité comme `/v1/payments` |
| [1.11](api-paiements.md) | passerelle | test | conformité 5.1 |
| [1.12](api-paiements.md) | passerelle | test | conformité 5.1 |
| [2.1](api-paiements.md) | passerelle | à écrire | créer, lire, synchroniser pour chaque opérateur simulé annoncé |
| [2.2](api-paiements.md) | passerelle | à écrire | création acceptée sans interrogation préalable de la découverte |
| [3](api-paiements.md) | spécification | sans objet |  |
| [3.1](api-paiements.md) | passerelle | à écrire | champs obligatoires présents, `completed_at` présent si terminal |
| [3.2](api-paiements.md) | passerelle | à écrire | `provider` conforme au motif et égal au `mock_*` demandé |
| [3.3](api-paiements.md) | passerelle | à écrire | `payer` avec un champ autre que `phone_number` rejeté |
| [3.4](api-paiements.md) | client | non testable | contenu choisi par le client, données personnelles indétectables |
| [3.5](api-paiements.md) | passerelle | à écrire | création contenant `fee` rejetée ; arrivée de `fee` sans changer `status` |
| [3.5](api-paiements.md) | client | non testable | affichage propre à l'application cliente |
| [4.1](api-paiements.md) | passerelle | à écrire | `next_action` présent si `pending`, absent une fois terminal |
| [4.2](api-paiements.md) | passerelle | à écrire | `type` dans l'énumération, champs de `redirect` présents |
| [4.3](api-paiements.md) | passerelle | à écrire | type de `next_action` égal à celui exigé par le simulé |
| [4.4](api-paiements.md) | client | à écrire | bibliothèque transmet `redirect_url` sans réécriture |
| [4.5](api-paiements.md) | passerelle | à écrire | `next_action` échue, paiement non échu reste `pending` |
| [4.6](api-paiements.md) | client | à écrire | bibliothèque ne traite pas un type inconnu comme `none` |
| [5.1](api-paiements.md) | passerelle | à écrire | champ obligatoire absent ou montant non positif rejeté |
| [5.1.1](api-paiements.md) | passerelle | à écrire | `provider` absent rejeté, `provider` renvoyé égal au demandé |
| [5.1.2](api-paiements.md) | passerelle | à écrire | `payer` absent pour un opérateur qui l'exige : `missing-field` |
| [5.1.3](api-paiements.md) | passerelle | à écrire | `return_url` en `http` ou relative rejetée |
| [5.1.4](api-paiements.md) | passerelle | à écrire | `expires_at` de la réponse égal à la garantie du simulé |
| [5.1.4](api-paiements.md) | client | à écrire | `expires_at` différent de la demande : la bibliothèque expose la valeur renvoyée |
| [5.1.5](api-paiements.md) | client | à écrire | bibliothèque lit le paiement existant sur `reference-conflict` |
| [5.1.6](api-paiements.md) | passerelle | test | conformité 5.10, Création sans réponse, paiement réussi chez l'opérateur |
| [5.1.7](api-paiements.md) | passerelle | à écrire | `locale` au journal (9.5.5) si annoncée, absente sinon ; autre valeur rejetée |
| [5.2](api-paiements.md) | spécification | sans objet |  |
| [5.2.1](api-paiements.md) | passerelle | à écrire | identifiant inconnu donne `404 not-found` |
| [5.2.2](api-paiements.md) | passerelle | à écrire | référence connue : un élément ; inconnue : `200`, `data` vide |
| [5.2.3](api-paiements.md) | client | test | conformité 5.8, récupération par référence |
| [5.2.4](api-paiements.md) | passerelle | à écrire | `GET` d'un paiement `pending` : aucune requête au journal (9.5.5) |
| [5.3](api-paiements.md) | spécification | sans objet |  |
| [5.3.1](api-paiements.md) | passerelle | à écrire | `PENDING_FOREVER` résolu sur le simulé, synchronisation renvoie l'état final |
| [5.3.2](api-paiements.md) | passerelle | à écrire | `NO_CALLBACK` : paiement dénoué sans synchronisation ni rappel |
| [5.3.3](api-paiements.md) | passerelle | test | conformité 5.4, synchroniser un paiement terminal sans `payments.lookup` |
| [5.3.3.1](api-paiements.md) | passerelle | test | conformité 5.4, synchroniser un paiement terminal sans `payments.lookup` |
| [5.3.4](api-paiements.md) | passerelle | à écrire | opérateur injoignable à la synchronisation : `503` ou `504`, paiement `pending` |
| [5.3.5](api-paiements.md) | passerelle | à écrire | rafale de synchronisations : `429 rate-limited` avec `Retry-After` |
| [5.3.6](api-paiements.md) | passerelle | à écrire | synchronisation sans `Idempotency-Key` acceptée |
| [6.1](api-paiements.md) | spécification | sans objet |  |
| [6.2](api-paiements.md) | client | à écrire | bibliothèque espace ses sondages et cesse à l'état terminal |
| [6.3](api-paiements.md) | spécification | sans objet |  |
| [7.1](api-paiements.md) | client | test | conformité 5.8, URL de retour non probante |
| [7.2](api-paiements.md) | spécification | sans objet |  |
| [7.3](api-paiements.md) | client | test | conformité 5.8, URL de retour non probante |
| [7.4](api-paiements.md) | passerelle | à écrire | point de retour : `303` vers `return_url` enregistrée, `404` si inconnu |
| [7.5](api-paiements.md) | passerelle | à écrire | rafale sur le point de retour limitée en débit |
| [8](api-paiements.md) | spécification | sans objet |  |
| [9.1](api-paiements.md) | passerelle | à écrire | paiement créé par une clé trouvé par référence avec une autre |
| [9.2](api-paiements.md) | passerelle | à écrire | clé sans la portée requise reçoit `403 forbidden` |
| [9.3](api-paiements.md) | client | non testable | obligation documentaire, aucun comportement observable |
| [10.1.1](api-paiements.md) | passerelle | test | conformité 5.1 |
| [10.1.2](api-paiements.md) | spécification | sans objet |  |
| [10.1.3](api-paiements.md) | passerelle | test | conformité 5.1 |
| [10.1.4](api-paiements.md) | client | à écrire | bibliothèque insensible aux variations de `title` et `detail` |
| [10.1.5](api-paiements.md) | passerelle | test | conformité 5.1 |
| [10.1.6](api-paiements.md) | passerelle | test | conformité 5.1 |
| [10.2.1](api-paiements.md) | spécification | sans objet |  |
| [10.2.2](api-paiements.md) | passerelle | test | conformité 5.10, Refus de l'opérateur |
| [10.2.3](api-paiements.md) | passerelle | à écrire | scénarios `DECLINE`, `INSUFFICIENT` : aucune réponse `4xx` ou `5xx` |
| [10.2.4](api-paiements.md) | client | à écrire | bibliothèque face à `504` ne marque pas le paiement échoué |
| [10.3.1](api-paiements.md) | passerelle | à écrire | chaque `type` reçu de forme `https://openfsp.org/problems/<code>` catalogué |
| [10.3.2](api-paiements.md) | client | à écrire | bibliothèque interprète l'erreur sans requête vers `openfsp.org` |
| [10.3.3](api-paiements.md) | spécification | non testable | documentation publiée sur `openfsp.org`, hors implémentation, suite hors ligne |
| [10.3.4](api-paiements.md) | spécification | sans objet |  |
| [10.3.5](api-paiements.md) | passerelle | à écrire | tout `type` sous `openfsp.org` appartient au catalogue |
| [10.3.6](api-paiements.md) | client | à écrire | bibliothèque face à un `type` inconnu suit `retryable` et `effect` |
| [10.4.1](api-paiements.md) | passerelle | à écrire | statut de chaque erreur provoquée égal au catalogue |
| [10.4.2](api-paiements.md) | spécification | sans objet |  |
| [10.4.3](api-paiements.md) | spécification | sans objet |  |
| [10.4.4](api-paiements.md) | passerelle | à écrire | `PROVIDER_ERROR` en `502`, `UNREACHABLE` en `503`, `TIMEOUT` en `504` |
| [10.5.1](api-paiements.md) | spécification | sans objet |  |
| [10.5.2](api-paiements.md) | passerelle | à écrire | renvoi même clé après erreur rejouable : un seul paiement |
| [10.5.3](api-paiements.md) | client | test | conformité 5.8, pas de renvoi d'un `4xx` non rejouable |
| [10.5.4](api-paiements.md) | client | test | conformité 5.8, réutilisation de la clé |
| [10.5.5](api-paiements.md) | client | à écrire | bibliothèque attend la durée `Retry-After` avant de renvoyer |
| [10.5.6](api-paiements.md) | passerelle | à écrire | `retryable` de chaque erreur provoquée égal au catalogue |
| [10.6.1](api-paiements.md) | spécification | sans objet |  |
| [10.6.2](api-paiements.md) | passerelle | à écrire | `UNREACHABLE` donne `none`, `TIMEOUT` donne `unknown` |
| [10.6.3](api-paiements.md) | client | à écrire | bibliothèque sur `effect` `unknown` renvoie même clé ou lit par référence |
| [10.6.4](api-paiements.md) | spécification | sans objet |  |
| [10.6.5](api-paiements.md) | passerelle | test | conformité 5.10, Erreur de l'opérateur à la création |
| [10.7.1](api-paiements.md) | passerelle | à écrire | `invalid-field` porte `errors` avec `field` et `code` |
| [10.7.2](api-paiements.md) | passerelle | à écrire | deux champs invalides rapportés dans une seule réponse |
| [10.7.3](api-paiements.md) | passerelle | à écrire | `field` est un JSON Pointer résolu dans le corps envoyé |
| [10.8.1](api-paiements.md) | passerelle | à écrire | `PROVIDER_ERROR` : `provider_detail` porte le code et le message |
| [10.8.2](api-paiements.md) | passerelle | test | conformité 5.10, Erreur de l'opérateur à la création |
| [10.8.3](api-paiements.md) | client | à écrire | bibliothèque insensible aux variations de `provider_detail` |
| [10.8.4](api-paiements.md) | passerelle | test | conformité 5.4, opérateur renvoyant des identifiants dans une erreur |
| [10.9](api-paiements.md) | spécification | sans objet |  |
| [10.9.1](api-paiements.md) | passerelle | à écrire | provoquer chaque code de requête, vérifier statut, `retryable`, `effect` |
| [10.9.2](api-paiements.md) | passerelle | à écrire | `unauthenticated` et `forbidden` : statut, `retryable`, `effect` du catalogue |
| [10.9.3](api-paiements.md) | passerelle | à écrire | `not-found` en `404`, `retryable` faux, `effect` `none` |
| [10.9.3.1](api-paiements.md) | passerelle | à écrire | clé sans la portée : `forbidden` sur identifiant existant comme inexistant |
| [10.9.4](api-paiements.md) | passerelle | à écrire | `reference-conflict`, `idempotency-request-in-progress` : valeurs du catalogue |
| [10.9.4.1](api-paiements.md) | spécification | sans objet |  |
| [10.9.4.2](api-paiements.md) | passerelle | test | conformité 5.3, doublon concurrent |
| [10.9.5](api-paiements.md) | passerelle | à écrire | `429 rate-limited` porte `Retry-After` |
| [10.9.6](api-paiements.md) | passerelle | test | conformité 5.10, Erreur de l'opérateur à la création |
| [10.9.6.1](api-paiements.md) | passerelle | test | conformité 5.10, Connexion refusée à la création |
| [10.9.6.2](api-paiements.md) | passerelle | non testable | `internal-error` impossible à provoquer sans instrumentation |
| [10.9.6.3](api-paiements.md) | passerelle | non testable | `internal-error` impossible à provoquer sans instrumentation |
| [10.10.1](api-paiements.md) | passerelle | à écrire | `title` en anglais sans `Accept-Language` |
| [10.10.2](api-paiements.md) | passerelle | à écrire | passerelle localisée : `Accept-Language: fr` honoré |
| [10.10.3](api-paiements.md) | passerelle | à écrire | `type`, `retryable`, `effect`, `code` identiques selon `Accept-Language` |
| [10.11.1](api-paiements.md) | passerelle | à écrire | téléphone et montant de la requête absents de `title`, `detail` |
| [10.11.2](api-paiements.md) | passerelle | test | conformité 5.4, clé inconnue, révoquée, d'un autre environnement |
| [10.11.3](api-paiements.md) | client | non testable | obligation documentaire, aucun comportement observable |

## Capacités et plafonds

| Règle | Sujet | Vérification | Détail |
|---|---|---|---|
| [1.1](capacites.md) | spécification | sans objet | définition |
| [1.2](capacites.md) | passerelle | à écrire | `/v1/capabilities` rapporte les capacités opérateur par opérateur |
| [1.3](capacites.md) | passerelle | test | conformité 5.12, Capacités annoncées pour chaque opérateur simulé |
| [1.4](capacites.md) | spécification | sans objet | renvoi à l'API |
| [2.1](capacites.md) | passerelle | à écrire | chaque nom annoncé conforme à l'expression régulière |
| [2.2](capacites.md) | passerelle | test | conformité 5.12, Capacités annoncées pour chaque opérateur simulé |
| [2.3](capacites.md) | spécification | sans objet | évolution de la spécification |
| [2.4](capacites.md) | passerelle | à écrire | tout nom hors registre préfixé d'un nom DNS inversé |
| [2.5](capacites.md) | spécification | sans objet | évolution de la spécification |
| [2.6](capacites.md) | passerelle | à écrire | `id` des opérateurs égaux aux identifiants `mock_` enregistrés |
| [2.7](capacites.md) | spécification | sans objet | procédure du registre |
| [2.8](capacites.md) | spécification | sans objet | procédure du registre |
| [3.1](capacites.md) | passerelle | à écrire | descripteur servi sans authentification avec ses trois membres |
| [3.1.1](capacites.md) | passerelle | à écrire | descripteur sans opérateur, marchand ni version logicielle |
| [3.1.2](capacites.md) | client | non testable | déduction interne au client, sans effet observable |
| [3.2](capacites.md) | passerelle | à écrire | sans clé `unauthenticated`, avec clé `protocol_version` et `providers` |
| [3.2.1](capacites.md) | passerelle | à écrire | champs obligatoires présents, `capabilities` contient `payments` |
| [3.2.2](capacites.md) | passerelle | à écrire | objet `payments` complet, `next_actions` cohérent avec les paiements créés |
| [3.2.3](capacites.md) | passerelle | à écrire | `expiry_guaranteed` vaut `false` pour chaque opérateur simulé |
| [3.2.4](capacites.md) | passerelle | à écrire | `Cache-Control` avec `max-age` d'au plus 3600 |
| [4.1](capacites.md) | client | à écrire | bibliothèque cliente ne synchronise pas sans `payments.lookup` annoncée |
| [4.2](capacites.md) | client | à écrire | client recevant `capability-not-supported` relit les capacités |
| [4.3](capacites.md) | client | à écrire | bibliothèque cliente ignore un nom de capacité inconnu |
| [4.4](capacites.md) | passerelle | test | conformité 5.4, Opération d'une capacité non annoncée |
| [4.5](capacites.md) | passerelle | non testable | le serveur simulé ne sait pas suspendre une capacité |
| [5.1](capacites.md) | spécification | sans objet | définition |
| [5.2](capacites.md) | passerelle | test | conformité 5.10, Dénouement sans rappel, opérateur avec consultation |
| [5.3](capacites.md) | passerelle | test | conformité 5.4, Synchroniser sans `payments.lookup` |
| [5.3.1](capacites.md) | passerelle | test | conformité 5.4, Synchroniser un paiement terminal sans `payments.lookup` |
| [5.4](capacites.md) | spécification | sans objet | renvoi au cycle de vie 6.5 |
| [6.1](capacites.md) | spécification | sans objet | définition |
| [6.2](capacites.md) | passerelle | à écrire | assisté : bornes déclarées par l'exploitant servies dans `limits` |
| [6.3](capacites.md) | passerelle | à écrire | sans bornes déclarées, `limits` absent, même après des échecs |
| [6.4](capacites.md) | passerelle | à écrire | assisté : `limits` servi en `Money` conformes aux bornes déclarées |
| [6.5](capacites.md) | client | non testable | affichage propre à l'application cliente |
| [6.6](capacites.md) | passerelle | à écrire | assisté : déclaration avec `min_amount` supérieur à `max_amount` refusée |
| [6.7](capacites.md) | passerelle | test | conformité 5.12, Montant inférieur d'un centime à `min_amount` |
| [6.8](capacites.md) | passerelle | à écrire | même clé après `amount-out-of-range` rejoue l'erreur enregistrée |
| [6.8](capacites.md) | client | à écrire | bornes changées après `amount-out-of-range` : nouvelle création sous nouvelle clé |
| [6.9](capacites.md) | passerelle | à écrire | refus opérateur pour plafond donne `failed` et `limit_exceeded` |
| [7.1](capacites.md) | passerelle | à écrire | les deux points d'accès du 3 répondent |
| [7.2](capacites.md) | suite | test | conformité 5.12 |
| [7.3](capacites.md) | suite | test | conformité 5.12 |
| [8.1](capacites.md) | passerelle | à écrire | rafale sur le descripteur public limitée, seuil non spécifié |
| [8.2](capacites.md) | passerelle | à écrire | clé sans la portée requise refusée malgré la capacité annoncée |
| [8.3](capacites.md) | passerelle | à écrire | `limits` absent du descripteur, servi seulement par `/v1/capabilities` |

## Webhooks

| Règle | Sujet | Vérification | Détail |
|---|---|---|---|
| [1.1](webhooks.md) | spécification | sans objet | définition d'événement et de livraison |
| [1.2](webhooks.md) | spécification | sans objet | portée de la signature, définie au 5 |
| [1.3](webhooks.md) | client | à écrire | événement contredit par la lecture : l'abonné retient la lecture |
| [1.4](webhooks.md) | passerelle | à écrire | `PENDING_FOREVER` puis `CONTRADICT` : aucun événement d'état non atteint |
| [2](webhooks.md) | passerelle | à écrire | chaque livraison porte un seul objet JSON, jamais un tableau |
| [2.1](webhooks.md) | passerelle | à écrire | valider chaque événement reçu contre la table des champs |
| [2.2](webhooks.md) | passerelle | à écrire | répondre `500` puis comparer `id` entre tentatives |
| [2.3](webhooks.md) | passerelle | à écrire | `reference` au premier niveau égale à `data.reference` |
| [2.4](webhooks.md) | passerelle | à écrire | comparer `data` à la lecture du paiement au même état |
| [2.5](webhooks.md) | client | à écrire | événement avec membres inconnus accepté par l'abonné, réponse `2xx` |
| [2.5](webhooks.md) | passerelle | à écrire | aucun membre de la table du 2.1 absent d'un événement reçu |
| [2.6](webhooks.md) | client | à écrire | `previous_status` discordant : abonné accepte et relit la ressource |
| [3.1](webhooks.md) | passerelle | à écrire | `type` de chaque événement reçu conforme à l'expression |
| [3.2](webhooks.md) | passerelle | à écrire | chaque transition émet son type, `previous_status` selon la table |
| [3.3](webhooks.md) | client | à écrire | livrer un `type` inconnu : abonné ignore et répond `2xx` |
| [3.4](webhooks.md) | passerelle | à écrire | synchronisation sans transition : aucun événement reçu |
| [3.5](webhooks.md) | spécification | sans objet | évolution de la spécification |
| [3.6](webhooks.md) | passerelle | à écrire | point d'accès limité à un type, aucun autre reçu (assisté) |
| [4.1](webhooks.md) | passerelle | à écrire | méthode `POST`, `Content-Type: application/json`, signature présente |
| [4.2](webhooks.md) | passerelle | à écrire | en-têtes présents, valeurs égales au corps, condensé exact |
| [4.2](webhooks.md) | client | à écrire | `OpenFSP-Delivery-Attempt` altéré : décision de l'abonné inchangée |
| [4.3](webhooks.md) | passerelle | à écrire | `2xx` avec corps d'erreur : aucun renvoi attendu |
| [4.4](webhooks.md) | passerelle | à écrire | `500`, coupure, TLS invalide renvoyés ; `410` arrête les renvois |
| [4.5](webhooks.md) | passerelle | à écrire | réponse retardée de 11 secondes traitée comme échec et renvoyée |
| [4.6](webhooks.md) | passerelle | à écrire | répondre `302` : cible non appelée, livraison renvoyée |
| [4.7](webhooks.md) | passerelle | à écrire | comparer les corps de deux tentatives octet par octet |
| [4.8](webhooks.md) | passerelle | à écrire | livraisons d'un paiement en échec, celles d'un autre arrivent |
| [5.1](webhooks.md) | passerelle | à écrire | `Signature-Input` et `Signature` présents sur chaque tentative |
| [5.2](webhooks.md) | passerelle | à écrire | liste des composants couverts exacte et ordonnée |
| [5.3](webhooks.md) | passerelle | à écrire | paramètres obligatoires présents, `tag` égal à `openfsp-webhook` |
| [5.4](webhooks.md) | passerelle | à écrire | `alg` par défaut `ed25519`, aucun algorithme hors liste publié |
| [5.5](webhooks.md) | passerelle | à écrire | `Content-Digest` `sha-256` égal au condensé du corps reçu |
| [5.5](webhooks.md) | client | à écrire | corps altéré sous signature valide : le vérificateur rejette |
| [5.6](webhooks.md) | passerelle | à écrire | `created` proche de la réception, `expires` au plus `created` + 300 |
| [5.6](webhooks.md) | client | à écrire | signature expirée ou `created` 301 secondes dans le futur : rejet |
| [5.7](webhooks.md) | passerelle | à écrire | nonces de 128 bits au moins, distincts entre tentatives |
| [5.7](webhooks.md) | client | à écrire | nonce répété dans la fenêtre du 5.6 : le vérificateur rejette |
| [5.8](webhooks.md) | client | à écrire | même `id` avec nonce neuf : aucun second effet chez l'abonné |
| [5.9](webhooks.md) | client | test | conformité 5.8, vérification avant action des abonnés |
| [5.10](webhooks.md) | client | à écrire | `alg` falsifié contredisant la clé : vérificateur rejette |
| [5.11](webhooks.md) | client | non testable | temps constant non mesurable de façon probante en boîte noire |
| [5.12](webhooks.md) | client | à écrire | signature invalide : pas de `2xx`, avertissement si autre que `400` |
| [6.1](webhooks.md) | passerelle | à écrire | `GET /v1/webhooks/keys` renvoie un JWK Set sous `keys` |
| [6.2](webhooks.md) | passerelle | à écrire | `keyid` de chaque signature présent comme `kid` publié |
| [6.2](webhooks.md) | client | à écrire | `kid` sous `EdDSA`, signature `ed25519` : le vérificateur accepte |
| [6.3](webhooks.md) | passerelle | à écrire | `openfsp_status` vaut `active` ou `retired` ; clé retirée absente (assisté) |
| [6.4](webhooks.md) | passerelle | à écrire | rotation assistée, suivre l'ensemble publié pendant 48 heures |
| [6.5](webhooks.md) | client | à écrire | compter les lectures de l'ensemble de clés par livraison |
| [6.6](webhooks.md) | client | à écrire | livraison signée par une clé hors ensemble publié : rejet |
| [6.7](webhooks.md) | passerelle | à écrire | `GET /v1/webhooks/keys` sans `Authorization` répond `200` |
| [6.8](webhooks.md) | passerelle | à écrire | aucun membre privé `d` dans l'ensemble publié |
| [7.1](webhooks.md) | passerelle | à écrire | configurer URL, types, activation ; désactivé ne reçoit rien (assisté) |
| [7.2](webhooks.md) | passerelle | à écrire | configurer une URL `http` hors développement : refus (assisté) |
| [7.3](webhooks.md) | passerelle | à écrire | certificat autosigné sur le point d'accès : livraison échouée |
| [7.4](webhooks.md) | client | non testable | persistance et asynchronisme internes à l'abonné |
| [7.5](webhooks.md) | client | à écrire | requête non signée sur le point d'accès : aucun effet |
| [7.6](webhooks.md) | client | à écrire | événement d'une ressource inconnue de l'abonné accepté, `2xx` |
| [8.1](webhooks.md) | passerelle | à écrire | `sequence` vaut 1, 2, 3 sur les événements d'un paiement |
| [8.2](webhooks.md) | passerelle | à écrire | aucune valeur de `sequence` répétée entre événements d'un paiement |
| [8.3](webhooks.md) | client | à écrire | livrer `sequence` inférieur au maximum traité : ignoré |
| [8.4](webhooks.md) | client | à écrire | livrer deux fois le même `id` : un seul effet |
| [8.5](webhooks.md) | client | à écrire | `payment.failed` après `succeeded` : état conservé, relecture |
| [8.6](webhooks.md) | client | à écrire | trou dans `sequence` : l'abonné relit sans attendre |
| [9.1](webhooks.md) | passerelle | à écrire | échecs répétés : délais croissants et non constants |
| [9.2](webhooks.md) | passerelle | à écrire | mesurer les délais entre tentatives contre le calendrier |
| [9.3](webhooks.md) | passerelle | à écrire | aucun délai sous le calendrier, dispersion au-dessus d'au moins 20 % |
| [9.4](webhooks.md) | passerelle | à écrire | après la septième tentative : aucun renvoi, paiement inchangé |
| [9.5](webhooks.md) | passerelle | à écrire | `429` avec `Retry-After` : tentative suivante pas plus tôt |
| [9.6](webhooks.md) | passerelle | à écrire | si désactivation, l'exploitant constate la raison consignée (assisté) |
| [9.7](webhooks.md) | passerelle | non testable | borne de file fixée par l'implémentation, inconnue de la suite |
| [10.1](webhooks.md) | spécification | sans objet | énoncé de principe, détaillé au 10.2 |
| [10.2](webhooks.md) | client | test | conformité 5.8, sondage fonctionnel quand tout événement est retenu |
| [10.3](webhooks.md) | client | test | conformité 5.8, paiement durablement `pending` |
| [11.1](webhooks.md) | spécification | sans objet | récapitulatif des règles citées |
| [11.2](webhooks.md) | spécification | sans objet | récapitulatif des règles citées |
| [11.3](webhooks.md) | passerelle | à écrire | sans `webhooks.emit` annoncé : aucune livraison reçue |
| [12.1](webhooks.md) | passerelle | à écrire | URL résolue vers bouclage ou privée refusée ; rebinding DNS refusé |
| [12.2](webhooks.md) | passerelle | à écrire | TLS mutuel configuré : signature toujours présente (assisté) |
| [12.3](webhooks.md) | passerelle | à écrire | compromission déclarée : nouvelle clé signe, ancienne retirée (assisté) |
| [12.4](webhooks.md) | client | non testable | journaux internes de l'abonné |
| [12.5](webhooks.md) | spécification | sans objet | énoncé de principe renvoyant au 1.3 |

## Authentification

| Règle | Sujet | Vérification | Détail |
|---|---|---|---|
| [1.1](authentification.md) | passerelle | à écrire | chaque point d'accès sans clé : `unauthenticated`, sauf exceptions listées |
| [1.2](authentification.md) | passerelle | à écrire | en mode de développement, requête sans clé rejetée |
| [1.3](authentification.md) | passerelle | à écrire | mesure amont configurée : requête sans `Bearer` rejetée (assisté) |
| [2.1](authentification.md) | passerelle | à écrire | vérifier la forme des clés de test émises (assisté) |
| [2.2](authentification.md) | passerelle | non testable | entropie de génération non établissable par quelques échantillons |
| [2.3](authentification.md) | passerelle | test | conformité 5.4, Clé inconnue, révoquée, d'un autre environnement |
| [2.4](authentification.md) | passerelle | non testable | absence d'encodage interne non démontrable en boîte noire |
| [2.5](authentification.md) | passerelle | sans objet | option bornée par le 2.1 |
| [3.1](authentification.md) | client | à écrire | bibliothèque cliente envoie `Authorization: Bearer` et rien d'autre |
| [3.2](authentification.md) | passerelle | à écrire | clé valide en paramètre, corps, cookie, autre en-tête : rejet |
| [3.3](authentification.md) | passerelle | test | conformité 5.13, Clé absente, mal formée, inconnue, révoquée, expirée, d'un autre environnement |
| [3.4](authentification.md) | passerelle | à écrire | `bearer` minuscule accepté ; clé en casse modifiée rejetée |
| [3.5](authentification.md) | passerelle | à écrire | deux en-têtes `Authorization` valides : `unauthenticated` |
| [4.1](authentification.md) | passerelle | non testable | stockage interne |
| [4.2](authentification.md) | passerelle | non testable | stockage interne |
| [4.3](authentification.md) | passerelle | non testable | choix interne, latence non probante |
| [4.4](authentification.md) | passerelle | sans objet | option de stockage interne |
| [4.5](authentification.md) | passerelle | non testable | temps constant non mesurable de façon probante en boîte noire |
| [4.6](authentification.md) | passerelle | à écrire | comparer statistiquement les temps clé inconnue et révoquée (assisté) |
| [4.7](authentification.md) | passerelle | test | conformité 5.4, Clé inconnue, révoquée, d'un autre environnement |
| [4.8](authentification.md) | passerelle | non testable | journaux internes de la passerelle |
| [5.1](authentification.md) | spécification | sans objet | définition du principal |
| [5.2](authentification.md) | spécification | sans objet | définition du rattachement clé-principal |
| [5.3](authentification.md) | passerelle | à écrire | deux clés d'un principal : rejeu idempotent croisé (assisté) |
| [5.4](authentification.md) | passerelle | à écrire | identifiant fourni par l'exploitant absent de toute réponse (assisté) |
| [5.5](authentification.md) | passerelle | à écrire | second principal lit le paiement créé par le premier (assisté) |
| [6.1](authentification.md) | spécification | sans objet | définition |
| [6.2](authentification.md) | passerelle | à écrire | chaque opération avec et sans sa portée (assisté) |
| [6.3](authentification.md) | passerelle | à écrire | clé `payments:write` seule : lecture refusée en `forbidden` |
| [6.4](authentification.md) | passerelle | à écrire | portée manquante : `forbidden`, ni `unauthenticated` ni `not-found` |
| [6.5](authentification.md) | spécification | sans objet | Réservé. |
| [6.6](authentification.md) | spécification | sans objet | évolution de la spécification |
| [6.7](authentification.md) | passerelle | à écrire | clé sans portée : chaque opération en `forbidden` (assisté) |
| [6.8](authentification.md) | passerelle | non testable | outillage d'émission hors de l'API |
| [7.1](authentification.md) | passerelle | à écrire | deux clés valides du même principal acceptées (assisté) |
| [7.2](authentification.md) | passerelle | à écrire | émettre une seconde clé : la première reste acceptée (assisté) |
| [7.3](authentification.md) | passerelle | à écrire | révoquer puis appeler après 60 secondes : rejet (assisté) |
| [7.4](authentification.md) | passerelle | non testable | absence de fonction d'administration non observable |
| [7.5](authentification.md) | passerelle | non testable | conservation interne de l'enregistrement |
| [7.6](authentification.md) | passerelle | test | conformité 5.13, Clé absente, mal formée, inconnue, révoquée, expirée, d'un autre environnement |
| [7.7](authentification.md) | passerelle | non testable | interface d'émission hors de l'API |
| [7.8](authentification.md) | passerelle | non testable | administration hors de l'API |
| [8.1](authentification.md) | passerelle | à écrire | rotation puis rejeu avec la nouvelle clé : réponse enregistrée (assisté) |
| [8.2](authentification.md) | passerelle | à écrire | deux clés d'un principal partagent le quota (assisté) |
| [8.3](authentification.md) | spécification | sans objet | renvoi aux définitions de l'API |
| [8.4](authentification.md) | spécification | sans objet | Réservé. |
| [8.5](authentification.md) | passerelle | à écrire | aucune livraison ne porte `Authorization` ni la clé d'API |
| [9.1](authentification.md) | passerelle | à écrire | démarrer avec secrets d'opérateur en variables d'environnement seules |
| [9.2](authentification.md) | passerelle | non testable | identifiants simulés fixes, rechargement non observable |
| [9.3](authentification.md) | passerelle | à écrire | rechercher les secrets simulés dans toutes les réponses |
| [9.4](authentification.md) | passerelle | non testable | journaux, traces et vidages internes |
| [9.5](authentification.md) | passerelle | test | conformité 5.4, Opérateur renvoyant des identifiants dans une erreur |
| [9.6](authentification.md) | passerelle | test | conformité 5.4, Opérateur renvoyant des identifiants dans une erreur |
| [10.1](authentification.md) | passerelle | non testable | registre d'audit interne, sans interface normalisée |
| [10.2](authentification.md) | passerelle | non testable | registre d'audit interne, sans interface normalisée |
| [10.3](authentification.md) | passerelle | non testable | registre d'audit interne, sans interface normalisée |
| [10.4](authentification.md) | passerelle | non testable | registre d'audit interne, sans interface normalisée |
| [11.1](authentification.md) | spécification | sans objet | récapitulatif des règles citées |
| [11.2](authentification.md) | suite | test | conformité 5.4, lignes clé et `CREDENTIAL_ECHO` |
| [11.3](authentification.md) | passerelle | à écrire | descripteur de capacités sans entrée d'authentification |
| [12.1](authentification.md) | passerelle | à écrire | rafale de clés invalides : `429` attendu, sinon avertissement |

## Conformité et serveur simulé

| Règle | Sujet | Vérification | Détail |
|---|---|---|---|
| [1.1](conformite.md) | déclarant | non testable | honnêteté d'une affirmation publiée, hors de la boîte noire |
| [1.2](conformite.md) | spécification | sans objet |  |
| [1.3](conformite.md) | spécification | sans objet |  |
| [1.4](conformite.md) | suite | à écrire | rejouer la suite deux fois, même configuration, comparer les rapports |
| [2.1](conformite.md) | spécification | sans objet |  |
| [2.2](conformite.md) | client | test | conformité 5.8 |
| [2.3](conformite.md) | spécification | sans objet |  |
| [2.4](conformite.md) | spécification | sans objet |  |
| [2.5](conformite.md) | suite | à écrire | vérifier qu'un rapport ne nomme qu'une seule cible |
| [3.1](conformite.md) | spécification | sans objet |  |
| [3.2](conformite.md) | spécification | sans objet |  |
| [3.3](conformite.md) | passerelle | à écrire | comparer profils revendiqués et capacités annoncées par la découverte |
| [3.4](conformite.md) | spécification | sans objet |  |
| [3.5](conformite.md) | suite | à écrire | faire échouer un test Core, vérifier Core échoué, sans taux |
| [3.6](conformite.md) | spécification | sans objet |  |
| [4.1](conformite.md) | suite | à écrire | exécuter la suite contre une implémentation tierce, valider le rapport |
| [4.2](conformite.md) | suite | sans objet |  |
| [4.3](conformite.md) | suite | à écrire | exécuter contre une passerelle de référence publiée, sans modification |
| [4.4](conformite.md) | suite | à écrire | vérifier que la suite n'exige que les trois entrées de configuration |
| [4.5](conformite.md) | suite | à écrire | journaliser la surface de contrôle, vérifier qu'elle est pilotée par la suite |
| [4.6](conformite.md) | suite | à écrire | exécuter la suite en intégration continue, sans réseau ni compte |
| [4.7](conformite.md) | suite | à écrire | vérifier que les tests assistés sont signalés comme tels au rapport |
| [5.1](conformite.md) | passerelle | test | conformité 5.1 |
| [5.2](conformite.md) | passerelle | test | conformité 5.2 |
| [5.3](conformite.md) | passerelle | test | conformité 5.3 |
| [5.4](conformite.md) | passerelle | test | conformité 5.4 |
| [5.4.1](conformite.md) | suite | test | conformité 5.4 |
| [5.5](conformite.md) | suite | à écrire | croiser les scénarios du 9.4.3 avec les tests de la suite |
| [5.6](conformite.md) | suite | à écrire | vérifier l'avertissement `webhooks.verify` dans chaque rapport |
| [5.7](conformite.md) | opérateur natif | test | conformité 5.7 |
| [5.8](conformite.md) | client | test | conformité 5.8 |
| [5.9](conformite.md) | suite | à écrire | comparer la correspondance test-exigence du rapport à la matrice |
| [5.10](conformite.md) | passerelle | test | conformité 5.10 |
| [5.11](conformite.md) | passerelle | test | conformité 5.11 |
| [5.12](conformite.md) | passerelle | test | conformité 5.12 |
| [5.13](conformite.md) | passerelle | test | conformité 5.13 |
| [5.14](conformite.md) | suite | test | conformité 5.11 |
| [6.1](conformite.md) | suite | à écrire | lancer contre une version majeure inconnue, attendre un refus |
| [6.2](conformite.md) | suite | à écrire | vérifier dans le résultat les sept éléments exigés |
| [6.3](conformite.md) | spécification | sans objet |  |
| [6.4](conformite.md) | déclarant | non testable | citation de la version testée, pratique de publication |
| [6.5](conformite.md) | suite | non testable | contenu des notes de version, pratique de publication |
| [7.1](conformite.md) | suite | à écrire | analyser le rapport avec un parseur standard |
| [7.2](conformite.md) | suite | à écrire | vérifier la présence de chaque champ requis dans le rapport |
| [7.3](conformite.md) | suite | à écrire | faire échouer un test, vérifier attendu et observé au rapport |
| [7.4](conformite.md) | suite | à écrire | vérifier la mention des limites dans un rapport réussi |
| [7.5](conformite.md) | déclarant | non testable | publication de la configuration, pratique hors protocole |
| [7.6](conformite.md) | spécification | sans objet |  |
| [8.1](conformite.md) | spécification | sans objet |  |
| [8.2](conformite.md) | suite | à écrire | exécuter la suite avec les seuls identifiants de test publiés |
| [9](conformite.md) | spécification | sans objet |  |
| [9.1.1](conformite.md) | serveur simulé | sans objet |  |
| [9.1.2](conformite.md) | serveur simulé | sans objet |  |
| [9.1.3](conformite.md) | serveur simulé | à écrire | comparer les capacités des opérateurs simulés à celles spécifiées |
| [9.2.1](conformite.md) | serveur simulé | non testable | choix de conception, comparaison aux opérateurs réels hors portée |
| [9.2.2](conformite.md) | serveur simulé | à écrire | vérifier que chaque capacité facultative manque à un opérateur simulé |
| [9.3.1](conformite.md) | serveur simulé | à écrire | comparer les capacités découvertes de chaque opérateur simulé au tableau |
| [9.3.2](conformite.md) | serveur simulé | à écrire | vérifier que `mock_beta` n'émet ni rappel ni consultation |
| [9.3.3](conformite.md) | serveur simulé | à écrire | vérifier qu'aucun opérateur simulé n'annonce de capacité de comptoir |
| [9.3.4](conformite.md) | serveur simulé | à écrire | vérifier le préfixe `mock_` de chaque opérateur simulé |
| [9.3.5](conformite.md) | serveur simulé | à écrire | `mock_epsilon` en `NO_CALLBACK` : aucun rappel, paiement présent au relevé |
| [9.4.1](conformite.md) | serveur simulé | à écrire | rejouer un même scénario deux fois, comparer les dénouements |
| [9.4.2](conformite.md) | serveur simulé | à écrire | déclarer un scénario par identifiant dérivé, vérifier son application |
| [9.4.2](conformite.md) | passerelle | non testable | absence de chemin de code propre, invisible en boîte noire |
| [9.4.3](conformite.md) | serveur simulé | à écrire | provoquer chaque scénario, comparer au comportement décrit |
| [9.4.4](conformite.md) | spécification | sans objet |  |
| [9.4.5](conformite.md) | serveur simulé | à écrire | paiement sans scénario déclaré, vérifier un dénouement `SUCCESS` |
| [9.4.6](conformite.md) | serveur simulé | à écrire | mesurer les délais de réponse, vérifier constance et non-nullité |
| [9.5.1](conformite.md) | serveur simulé | à écrire | exercer les quatre opérations de contrôle hors interface opérateur |
| [9.5.2](conformite.md) | serveur simulé | à écrire | journaliser les appels de contrôle, vérifier qu'ils viennent de la suite |
| [9.5.3](conformite.md) | serveur simulé | à écrire | avancer l'horloge, vérifier horodatages de la passerelle inchangés |
| [9.5.4](conformite.md) | serveur simulé | à écrire | appeler le contrôle hors bouclage sans authentification, attendre un refus |
| [9.5.5](conformite.md) | serveur simulé | à écrire | créer un paiement, retrouver méthode, chemin et corps au journal |
| [9.6.1](conformite.md) | serveur simulé | à écrire | rejouer une séquence sur deux instances fraîches, comparer les réponses |
| [9.6.2](conformite.md) | serveur simulé | à écrire | redémarrer, vérifier qu'un paiement antérieur est inconnu |
| [9.7.1](conformite.md) | serveur simulé | à écrire | vérifier le préfixe `mock_` des identifiants de paiements simulés |
| [9.7.2](conformite.md) | serveur simulé | à écrire | fournir un secret au format réel, attendre un refus |
| [9.7.3](conformite.md) | passerelle | non testable | journal de démarrage interne, hors de la boîte noire |
| [9.7.4](conformite.md) | serveur simulé | à écrire | inspecter les réponses : aucun identifiant réel ni artefact de règlement |
| [9.7.5](conformite.md) | serveur simulé | à écrire | vérifier que les opérateurs annoncés diffèrent des opérateurs réels |
| [9.7.6](conformite.md) | passerelle | à écrire | présenter une clé `live` au déploiement simulé, attendre un refus |
| [9.8.1](conformite.md) | spécification | sans objet |  |
| [9.8.2](conformite.md) | spécification | sans objet |  |
| [9.8.3](conformite.md) | spécification | sans objet |  |
| [9.8.4](conformite.md) | spécification | sans objet |  |
