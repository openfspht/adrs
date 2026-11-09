# Idempotence

Je justifie ces choix dans [ADR-0006](../text/0006-gateway-http-api-payments.md).

## 1. Opérations concernées

**1.1.** Toute requête `POST`, `PATCH` ou `DELETE` de l'API client est une opération
soumise à idempotence, sauf exemption (1.4). Les points appelés par l'opérateur ou le payeur
(rappels, retour) ne sont pas concernés.

**1.2.** `GET` et `HEAD` ne sont pas concernées. Un client PEUT les renvoyer librement.

**1.3.** Un client DOIT envoyer `Idempotency-Key` sur toute opération soumise à idempotence. La
passerelle DOIT rejeter sans l'exécuter une telle requête qui n'en porte pas, avec
`idempotency-key-required`.

**1.4.** Une ADR PEUT exempter une opération nommée si les deux conditions sont réunies :
l'exécuter deux fois est sans effet, et une réponse enregistrée servie à sa place rapporterait
un état antérieur à l'exécution. Pour une opération exemptée, la passerelle NE DOIT PAS exiger la clé, NE DOIT PAS
enregistrer de réponse, et DOIT ignorer l'en-tête s'il est présent.

## 2. Clé

**2.1.** La valeur est un `IdempotencyKey` : 1 à 255 caractères parmi `A-Za-z0-9_-`. La
passerelle DOIT rejeter sans l'exécuter une requête dont la clé n'est pas conforme, avec
`invalid-field` ([API 10.9.1](api-paiements.md)) sans `errors` : `field` ne désigne qu'un
emplacement du corps ([API 10.7.1](api-paiements.md)).

**2.2.** Un client DEVRAIT générer la clé comme un UUID (RFC 9562) ou à partir d'au moins
128 bits d'aléa cryptographique, et NE DEVRAIT PAS la dériver de données métier.

**2.3.** Un enregistrement est identifié par le triplet (principal, opération, clé). La
passerelle NE DOIT PAS servir une réponse enregistrée à un autre principal que celui qui l'a
créée.

## 3. Traitement

Je note *P* le principal, *O* l'opération, *K* la clé et *F* l'empreinte du 4.

**3.1. Première requête.** Sans enregistrement pour (*P*, *O*, *K*), la passerelle exécute
l'opération puis, le dénouement déterminé (5), enregistre *F*, le statut et le corps de la
réponse.

**3.2. Rejeu.** Si l'enregistrement existe avec la même empreinte, la passerelle NE DOIT PAS
exécuter l'opération. Elle DOIT renvoyer le statut et le corps enregistrés, identiques à
l'octet près, avec `Idempotent-Replay: true`.

**3.3. Conflit.** Si l'empreinte diffère, la passerelle DOIT rejeter la requête sans
l'exécuter, avec `idempotency-key-reused` (`422`).

**3.4. En cours.** Si la première requête n'a pas encore de dénouement déterminé, la
passerelle NE DOIT PAS exécuter la seconde en parallèle. Elle DOIT soit la faire attendre,
soit la rejeter avec `idempotency-request-in-progress` (`409`) et `Retry-After`.

**3.5.** La création de l'enregistrement et l'exécution DOIVENT être mutuellement exclusives
(insertion conditionnelle, verrou ou équivalent). Un contrôle lecture puis écriture NE DOIT
PAS être utilisé.

## 4. Empreinte

**4.1.** *F* est le condensé SHA-256 du corps de la requête canonicalisé selon la RFC 8785.
Un corps vide a l'empreinte de `{}`.

**4.2.** Seul le corps entre dans l'empreinte. Le chemin, les paramètres et les en-têtes en
sont exclus.

## 5. Enregistrement

**5.1.** La passerelle DOIT enregistrer la réponse seulement si le dénouement est déterminé :

- un succès, y compris un paiement `failed` ;
- une erreur causée par la requête elle-même : validation, champ inconnu,
  `reference-conflict`.

**5.2.** La passerelle NE DOIT PAS enregistrer :

- une erreur interne dont l'effet est inconnu ;
- une expiration ou un échec de transport vers l'opérateur ;
- un arrêt avant la persistance du dénouement ;
- une réponse `idempotency-request-in-progress`.

**5.3.** La passerelle NE DOIT PAS modifier une réponse enregistrée.

## 6. Rétention et référence

**6.1.** La passerelle DOIT conserver les enregistrements au moins 24 heures, DEVRAIT les
conserver 7 jours, et DOIT publier sa durée de rétention.

**6.2.** Passé ce délai, la même clé est traitée comme une première requête. La passerelle
DOIT faire respecter l'unicité de la `reference` indépendamment des enregistrements
d'idempotence.

**6.3.** Création de paiement :

| Clé | Corps | Référence | Résultat |
|---|---|---|---|
| identique, non expirée | identique | identique | rejeu (3.2) |
| identique | différent | quelconque | `idempotency-key-reused` (3.3) |
| expirée | identique | identique | `reference-conflict` |
| différente | quelconque | identique | `reference-conflict` |
| différente | quelconque | différente | nouveau paiement |

## 7. Opérateur

**7.1.** Avant de renvoyer à l'opérateur une opération au dénouement indéterminé, la
passerelle DOIT tenter de l'établir par une source faisant foi
([cycle de vie 6.5](cycle-de-vie.md)).

**7.2.** La passerelle DOIT transmettre à l'opérateur un identifiant de commande :

- dérivé de la `reference` par HMAC-SHA256, sous une clé de dérivation propre à la passerelle ;
- encodé dans l'alphabet de l'opérateur, au moins 128 bits : 26 caractères en base32
  minuscule, ou 39 chiffres si l'opérateur n'accepte que des chiffres ;
- DOIT être stocké et indexé avec le paiement ([API 7.4](api-paiements.md),
  [cycle de vie 10.4.1](cycle-de-vie.md)) ;
- valide après un changement de clé de dérivation ; la nouvelle clé de dérivation sert aux
  nouveaux paiements ;
- dérivé de la même façon pour les opérateurs `mock_*`.

Si l'opérateur limite l'identifiant à moins de 128 bits, l'adaptateur DOIT le documenter comme
perte connue. Si l'opérateur offre une idempotence ou une recherche par identifiant de commande,
la passerelle DOIT s'en servir pour établir le dénouement (7.1).

**7.2.1.** Un identifiant de requête exigé par l'opérateur à chaque appel (`requestId`) est
distinct de l'identifiant de commande : un opérateur qui rejette un `requestId` en double
n'offre pas pour autant une idempotence au sens du 7.2.

**7.3.** Si l'opérateur n'offre ni idempotence ni recherche par identifiant de
commande, la passerelle NE DOIT PAS renvoyer automatiquement une opération indéterminée. Le
paiement reste `pending` ; la passerelle DOIT signaler l'opération indéterminée à l'exploitant.

**7.4.** La passerelle DOIT documenter, par adaptateur, lequel du 7.2 ou du 7.3 s'applique.

## 8. Client

**8.1.** Un client DOIT utiliser une clé par opération logique et la même clé pour chaque
renvoi de cette opération.

**8.2.** Un client NE DOIT PAS renvoyer une requête ayant reçu une réponse `4xx`, hormis
`idempotency-request-in-progress` et `rate-limited`.

**8.3.** Après des renvois, un client DOIT lire la ressource pour connaître le dénouement, et
NE DOIT PAS le déduire de la dernière réponse reçue.

**8.4.** Un client DOIT espacer ses renvois et respecter `Retry-After`. Il DEVRAIT utiliser
une temporisation exponentielle avec gigue.

**8.5.** Un client DEVRAIT persister la clé avant d'envoyer la requête.

## 9. Sécurité

**9.1.** La clé seule NE DOIT PAS servir d'identifiant de recherche : les enregistrements
sont cloisonnés par principal (2.3). La clé n'est pas un secret et NE DOIT conférer aucune
autorisation.

**9.2.** La passerelle DOIT limiter le débit de création par principal et DEVRAIT plafonner le
nombre d'enregistrements par principal, en rejetant les requêtes en excès plutôt qu'en
supprimant des enregistrements.

**9.3.** Les réponses enregistrées PEUVENT contenir des données personnelles et DOIVENT être
protégées comme les ressources dont elles sont issues.
