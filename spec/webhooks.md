# Webhooks

Décision : [ADR-0008](../text/0008-webhooks-and-event-delivery.md).

## 1. Événement

**1.1.** Un événement est une affirmation de la passerelle : une ressource a atteint un état
donné à un instant donné. Une livraison est une requête HTTP portant un événement. Un même
événement peut être livré plusieurs fois.

**1.2.** Une livraison dont la signature se vérifie (§5) provient de la passerelle détenant la
clé privée, et son corps est intact.

**1.3.** Un événement décrit la ressource à son émission, pas son état courant. En cas de
contradiction entre un événement et une lecture, la lecture l'emporte.

**1.4.** La passerelle NE DOIT PAS émettre d'événement pour un état que la ressource n'a pas
atteint.

## 2. Objet `event`

Le corps d'une livraison est un seul objet JSON, jamais un tableau ni un lot.

```json
{
  "id": "evt_01J9ZK4T2A0YHQ8F3W6N5R7B1C",
  "type": "payment.succeeded",
  "created_at": "2026-08-17T14:36:11.208Z",
  "sequence": 3,
  "resource_type": "payment",
  "resource_id": "pay_01J9ZK3QF8XN2M7VYB4C6D8E0G",
  "reference": "INV-2026-00184",
  "previous_status": "pending",
  "data": { "id": "pay_01J9ZK3QF8XN2M7VYB4C6D8E0G", "status": "succeeded", "...": "..." }
}
```

**2.1.** Champs :

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `id` | `ResourceId` | OBLIGATOIRE | Identifie l'événement ; identique à chaque livraison. |
| `type` | chaîne | OBLIGATOIRE | Registre du §3.2. |
| `created_at` | `Timestamp` | OBLIGATOIRE | Enregistrement de la transition, pas la tentative de livraison. |
| `sequence` | entier | OBLIGATOIRE | Ordinal par ressource (§8). |
| `resource_type` | chaîne | OBLIGATOIRE | `payment`. |
| `resource_id` | `ResourceId` | OBLIGATOIRE | Ressource concernée. |
| `reference` | `Reference` | OBLIGATOIRE | Référence du marchand. |
| `previous_status` | chaîne | conditionnel | OBLIGATOIRE pour un changement de statut. |
| `data` | objet | OBLIGATOIRE | Ressource complète à `created_at` ([API §3](api-paiements.md)). |

**2.2.** `id` suit les règles de `ResourceId` ([modèle de données §6.1](modele-de-donnees.md)) et
DOIT être identique sur toutes les livraisons d'un même événement.

**2.3.** `reference` est reprise au premier niveau en plus de `data`.

**2.4.** `data` est un instantané complet de la ressource, pas un différentiel.

**2.5.** Un abonné DOIT tolérer les membres inconnus de l'objet et de `data`. La passerelle NE
DOIT PAS retirer un membre de l'objet sans ADR.

**2.6.** Un client NE DOIT PAS rejeter un événement au seul motif que `previous_status` diffère
de l'état qu'il détient ; il DEVRAIT alors relire la ressource.

## 3. Types

**3.1.** `type` correspond à `^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$` : `resource_type` puis la
transition.

**3.2.** Registre :

| Type | Émis quand | `previous_status` |
|---|---|---|
| `payment.created` | Un paiement est créé en `pending`. | absent |
| `payment.succeeded` | Un paiement entre en `succeeded`. | OBLIGATOIRE |
| `payment.failed` | Un paiement entre en `failed`. | OBLIGATOIRE |
| `payment.expired` | Un paiement entre en `expired`. | OBLIGATOIRE |
| `payment.canceled` | Un paiement entre en `canceled`. | OBLIGATOIRE |

**3.3.** Un abonné DOIT ignorer un `type` inconnu et DOIT néanmoins répondre `2xx`.

**3.4.** Il n'y a pas de `payment.updated` : un changement de champ sans transition n'émet pas
d'événement.

**3.5.** Ajouter un type requiert une ADR ; ce n'est pas une rupture et n'exige pas de nouvelle
version majeure.

**3.6.** La passerelle NE DOIT PAS émettre vers un point d'accès un type qu'il n'a pas demandé
(§7.1).

## 4. Livraison

**4.1.** Une livraison est un `POST` vers l'URL configurée, en `Content-Type: application/json`,
signé selon le §5.

**4.2.** En-têtes :

| En-tête | Valeur |
|---|---|
| `Content-Digest` | SHA-256 du corps (RFC 9530). Couvert par la signature. |
| `OpenFSP-Event-Id` | `id` de l'événement. Couvert par la signature. |
| `OpenFSP-Event-Type` | `type` de l'événement. Couvert par la signature. |
| `OpenFSP-Delivery-Attempt` | Rang de la tentative, à partir de `1`. Non couvert. |

Un abonné NE DOIT PAS fonder une décision de confiance sur un en-tête non couvert. Les valeurs
qui font foi sont dans le corps.

**4.3.** Une livraison réussit sur un statut `2xx` reçu dans le délai du §4.5. La passerelle NE
DOIT PAS analyser le corps de la réponse, ni agir dessus, ni le journaliser en entier.

**4.4.** Tout autre statut, échec de connexion, échec TLS ou expiration est un échec, renvoyé
selon le §9. Exception : `410 Gone` est définitif ; la passerelle DOIT cesser de renvoyer cet
événement et DEVRAIT cesser de livrer à ce point d'accès, en le consignant (§9.6).

**4.5.** La passerelle DOIT borner connexion et réponse ; le total NE DOIT PAS dépasser
10 secondes.

**4.6.** Un `3xx` DOIT être traité comme un échec : les redirections ne sont pas suivies.

**4.7.** Le corps DOIT être identique à l'octet près d'une tentative à l'autre ; seule la
signature est recalculée.

**4.8.** La passerelle PEUT livrer en parallèle et dans le désordre, et NE DOIT PAS bloquer les
livraisons d'une ressource derrière celles d'une autre.

## 5. Signature

**5.1.** Toute livraison DOIT porter une signature HTTP (RFC 9421) dans `Signature-Input` et
`Signature`, y compris en mode de développement.

**5.2.** Composants couverts, exactement et dans cet ordre :

```
("@method" "@target-uri" "content-type" "content-digest" "openfsp-event-id"
 "openfsp-event-type")
```

**5.3.** Paramètres OBLIGATOIRES : `keyid`, `created`, `expires`, `nonce`, `alg`. `tag` DOIT
valoir `openfsp-webhook`.

```
Signature-Input: sig1=("@method" "@target-uri" "content-type" "content-digest" \
  "openfsp-event-id" "openfsp-event-type");created=1755441371;expires=1755441671;\
  keyid="gw-2026-08";nonce="Zk9tQ1p2WXhLbFEyNw";alg="ed25519";tag="openfsp-webhook"
Signature: sig1=:MEUCIQDf…:
```

**5.4.** La passerelle DOIT prendre en charge `ed25519` et l'utiliser par défaut. Elle PEUT
offrir `ecdsa-p256-sha256` et NE DOIT PAS offrir d'autre algorithme.

**5.5.** `Content-Digest` est OBLIGATOIRE, en `sha-256`. Le vérificateur DOIT recalculer le
condensé du corps reçu et le comparer à l'en-tête.

**5.6.** `created` DOIT être l'heure de la tentative et `expires` au plus `created` + 300
secondes. Le vérificateur DOIT rejeter une signature expirée ou dont `created` est à plus de
300 secondes dans le futur.

**5.7.** `nonce` DOIT contenir au moins 128 bits imprévisibles, en base64url, nouveaux à chaque
tentative. Le vérificateur DOIT conserver les nonces acceptés pendant au moins la fenêtre du
§5.6 et DOIT rejeter un nonce répété.

**5.8.** Le cache de nonces ne remplace pas la déduplication par `id` (§8.4) ; un abonné DOIT
appliquer les deux.

**5.9.** Un abonné DOIT vérifier avant d'agir, dans cet ordre : résoudre `keyid` et rejeter un
`keyid` inconnu, contrôler `alg` contre la clé, la fraîcheur, le nonce, le condensé, puis la
signature.

**5.10.** Le vérificateur NE DOIT PAS choisir l'algorithme d'après `alg` : la clé le détermine,
`alg` est seulement contrôlé.

**5.11.** Les comparaisons de condensés et de signatures DOIVENT être en temps constant.

**5.12.** En cas d'échec de vérification, l'abonné DOIT rejeter la livraison sans agir, NE DOIT
PAS répondre `2xx`, et DEVRAIT répondre `400`.

## 6. Clés

**6.1.** La passerelle DOIT publier ses clés de vérification en JWK Set à
`GET /v1/webhooks/keys`, dans l'enveloppe `data` ([API §1.12](api-paiements.md)).

```json
{
  "data": [
    {
      "kid": "gw-2026-08",
      "kty": "OKP",
      "crv": "Ed25519",
      "alg": "EdDSA",
      "use": "sig",
      "x": "11qYAYKxCrfVS_7TyWQHOg7hcvPapiMlrwIaaPcHURo",
      "openfsp_status": "active"
    }
  ]
}
```

**6.2.** `kid` DOIT être égal au `keyid` du §5.3. Le vérificateur DOIT accepter l'appariement du
nom JOSE `EdDSA` et du nom RFC 9421 `ed25519`.

**6.3.** `openfsp_status` vaut `active` (clé de signature) ou `retired` (vérification seulement).
Une clé retirée du service NE DOIT PAS être publiée.

**6.4.** Une nouvelle clé DOIT être publiée au moins 24 heures avant de signer, et une clé DOIT
rester publiée au moins 24 heures après sa dernière utilisation.

**6.5.** Un abonné DEVRAIT mettre l'ensemble de clés en cache et le rafraîchir sur un `keyid`
inconnu, avec limitation de débit. Il NE DOIT PAS le rafraîchir à chaque livraison.

**6.6.** Un abonné DOIT récupérer les clés uniquement depuis l'URL de base configurée, et NE
DOIT PAS prendre de clé, d'URL de clé ni de certificat dans une livraison.

**6.7.** Le point d'accès des clés n'est pas authentifié. La passerelle PEUT en limiter le débit.

**6.8.** Les clés privées sont détenues par l'exploitant. La passerelle NE DOIT PAS les
journaliser ni les exposer par un point d'accès.

## 7. Point d'accès de l'abonné

**7.1.** La passerelle DOIT permettre de configurer, par point d'accès : l'URL, les types
d'événement, l'activation.

**7.2.** La passerelle DOIT refuser une URL non `https`, hors mode de développement.

**7.3.** La passerelle DOIT valider le certificat TLS du point d'accès et NE DOIT PAS offrir
d'option pour désactiver cette validation.

**7.4.** Un abonné DEVRAIT vérifier, persister l'événement et répondre `2xx`, puis traiter de
façon asynchrone.

**7.5.** Un abonné NE DOIT PAS fonder une autorisation sur le seul fait qu'une requête atteint
son point d'accès.

**7.6.** Un abonné DOIT accepter tout type du §3.2 à tout moment, y compris pour une ressource
qu'il ne connaît pas.

## 8. Ordre et doublons

**8.1.** `sequence` commence à `1` pour le premier événement d'une ressource et croît de un à
chaque événement de cette ressource. Il n'ordonne pas les événements entre ressources.

**8.2.** La passerelle DOIT attribuer `sequence` à l'enregistrement de l'événement et NE DOIT
PAS réutiliser une valeur pour une ressource.

**8.3.** Un abonné DOIT ignorer un événement dont `sequence` est inférieur ou égal au plus grand
déjà traité pour ce `resource_id`.

**8.4.** `id` est la clé de déduplication : un abonné DOIT pouvoir traiter deux fois le même
`id` sans second effet.

**8.5.** Un abonné NE DOIT PAS faire sortir une ressource d'un état terminal sur la foi d'un
événement ; il DEVRAIT relire la ressource et lever une alerte.

**8.6.** Sur un trou dans `sequence`, un abonné DEVRAIT relire la ressource et NE DEVRAIT PAS
attendre l'événement manquant.

## 9. Renvois

**9.1.** Une livraison échouée DOIT être renvoyée avec un retrait exponentiel et une gigue.

**9.2.** Calendrier minimal, depuis la première tentative :

| Tentative | Délai |
|---|---|
| 1 | immédiat |
| 2 | 30 secondes |
| 3 | 2 minutes |
| 4 | 10 minutes |
| 5 | 1 heure |
| 6 | 6 heures |
| 7 | 24 heures |

**9.3.** Chaque délai DOIT porter une gigue d'au moins ±20 %. La passerelle PEUT espacer
davantage et NE DOIT PAS renvoyer plus tôt.

**9.4.** Après la dernière tentative, la passerelle DOIT s'arrêter, DOIT consigner l'abandon de
façon visible pour l'exploitant, NE DOIT PAS supprimer l'événement et NE DOIT PAS modifier la
ressource.

**9.5.** La passerelle DOIT honorer `Retry-After` sur `429` et `503`, jusqu'à une borne qu'elle
fixe.

**9.6.** La passerelle PEUT désactiver un point d'accès en échec prolongé ; elle DOIT alors
consigner la raison de façon visible pour l'exploitant.

**9.7.** La passerelle DOIT borner sa file de livraisons et délester en refusant de nouvelles
livraisons vers le point d'accès défaillant, sans supprimer d'événement.

## 10. Sondage

**10.1.** Les événements complètent le sondage sans le remplacer.

**10.2.** Un client DOIT disposer d'un accès à l'état courant qui ne dépend pas des événements :
lecture ou synchronisation ([API §5.2, §5.3](api-paiements.md)).

**10.3.** Un client DEVRAIT rapprocher tout paiement encore `pending` après un délai qu'il fixe.

## 11. Conformité

**11.1.** Passerelle conforme : émet chaque type du §3.2, signe selon le §5, publie les clés
selon le §6, renvoie selon le §9, n'émet jamais d'événement sans transition (§1.4).

**11.2.** Abonné conforme : vérifie selon le §5.9, rejette selon le §5.12, déduplique selon le
§8.4, séquence selon le §8.3, respecte le §8.5 et dispose du §10.2.

**11.3.** L'émission est annoncée par `webhooks.emit`, distincte de `webhooks.verify` qui
concerne l'opérateur. Une passerelle qui n'annonce pas `webhooks.emit` NE DOIT PAS émettre
d'événement.

## 12. Sécurité

**12.1.** La passerelle DOIT refuser une URL de point d'accès qui se résout vers une adresse de
bouclage, de lien local, privée ou de métadonnées d'hébergeur, hors mode de développement, et
DOIT refaire ce contrôle à chaque livraison.

**12.2.** Un TLS mutuel PEUT s'ajouter à la signature et NE DOIT PAS la remplacer.

**12.3.** En cas de compromission soupçonnée, la passerelle DEVRAIT pouvoir signer
immédiatement avec une nouvelle clé.

**12.4.** Un abonné DEVRAIT journaliser `id`, `type` et `sequence`, et NE DEVRAIT PAS
journaliser le corps. Valeurs de signature et nonces NE DEVRAIENT PAS être journalisés.

**12.5.** Une livraison réussie NE DOIT PAS tenir lieu de registre des opérations : la ressource
reste l'enregistrement.
