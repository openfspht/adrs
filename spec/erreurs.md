# Erreurs

Décision : [ADR-0005](../text/0005-error-taxonomy.md).

## 1. Format

**1.1.** Toute réponse d'erreur DOIT être un problem detail (RFC 9457) de type de média
`application/problem+json`.

**1.2.** Exemple :

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

**1.3.** Membres :

| Membre | Type | Présence | Notes |
|---|---|---|---|
| `type` | URI | OBLIGATOIRE | Identifiant stable (§3). |
| `title` | chaîne | OBLIGATOIRE | Lisible, non stable. |
| `status` | entier | OBLIGATOIRE | Statut HTTP. |
| `detail` | chaîne | FACULTATIF | Lisible, propre à l'occurrence, non stable. |
| `instance` | référence d'URI | FACULTATIF | Chemin de la requête. |
| `retryable` | booléen | OBLIGATOIRE | §5. |
| `effect` | chaîne | OBLIGATOIRE | `none` ou `unknown` (§6). |
| `request_id` | chaîne | OBLIGATOIRE | Corrélation avec les journaux de la passerelle. |
| `errors` | tableau | FACULTATIF | Détail par champ (§7). |
| `provider_detail` | objet | FACULTATIF | Relais de l'opérateur (§8). |

**1.4.** Un client DOIT identifier une erreur par son seul `type`. `title` et `detail` PEUVENT
changer ou être localisés.

**1.5.** `status` DOIT être égal au statut HTTP de la réponse.

**1.6.** `request_id` DOIT être présent sur toute erreur, y compris `500`.

## 2. Requête échouée et paiement échoué

**2.1.** Une réponse d'erreur signifie que la requête a échoué, pas qu'un paiement a échoué.

**2.2.** Un paiement refusé est rapporté en `200`, avec `"status": "failed"` et un
`failure_reason` ([cycle de vie §7.2](cycle-de-vie.md)).

**2.3.** La passerelle NE DOIT PAS rapporter un paiement refusé par une réponse d'erreur, ni
utiliser un statut `4xx` ou `5xx` pour le dénouement d'un paiement.

**2.4.** Un client NE DOIT PAS traiter une réponse non `2xx` comme un paiement échoué. Son
effet est donné par `effect`.

## 3. URI de type

**3.1.** Forme : `https://openfsp.org/problems/<code>`, `<code>` venant du catalogue du §9.

**3.2.** Un client DOIT comparer ces URI comme des chaînes opaques et NE DOIT PAS les
déréférencer pour interpréter une réponse.

**3.3.** Les URI DEVRAIENT pointer vers une documentation du type.

**3.4.** L'autorité `openfsp.org` NE DOIT PAS changer. Le projet maintient l'enregistrement
du domaine comme une obligation permanente.

**3.5.** Une passerelle PEUT définir des types sous sa propre autorité et NE DOIT PAS en
définir sous l'autorité OpenFSP.

**3.6.** Face à un `type` inconnu, un client DOIT se fonder sur `status`, `retryable` et
`effect`. Ajouter un type au catalogue n'est donc pas une rupture de compatibilité.

## 4. Statuts

**4.1.** La passerelle DOIT utiliser le statut assigné par le catalogue.

**4.2.** Les statuts suivent la RFC 9110 : `400` requête illisible ou mal formée, `422`
contenu invalide, `409` conflit avec un état détenu par la passerelle.

**4.3.** `idempotency-key-reused` est en `422` : aucun état détenu n'est contredit, le contenu
de la requête viole la règle de la clé. `409` est réservé à `idempotency-request-in-progress`.
Ce partage est celui du brouillon IETF `Idempotency-Key`.

**4.4.** Côté opérateur : `502` réponse invalide ou erreur de l'opérateur, `503` opérateur
injoignable, `504` pas de réponse à temps.

## 5. `retryable`

**5.1.** `retryable` indique si répéter la requête inchangée, avec la même `Idempotency-Key`,
peut réussir.

**5.2.** `true` signifie que le renvoi est sans danger, pas qu'il réussira.

**5.3.** Un client NE DOIT PAS renvoyer une requête dont l'erreur porte `retryable: false`.

**5.4.** Un client qui renvoie DOIT réutiliser la clé d'origine
([idempotence §8.1](idempotence.md)) et DOIT appliquer un retrait.

**5.5.** Un client DOIT respecter `Retry-After`.

**5.6.** `retryable` DOIT correspondre à la valeur du catalogue.

## 6. `effect`

**6.1.** Valeurs :

| Valeur | Sens |
|---|---|
| `none` | L'opération n'a pas pris effet. |
| `unknown` | L'opération a pu prendre effet. |

**6.2.** La passerelle DOIT rapporter `none` seulement si elle peut l'établir, `unknown`
sinon.

**6.3.** Sur `unknown`, un client NE DOIT PAS conclure à l'échec. Il DOIT renvoyer avec la clé
d'origine ou lire la ressource par sa `reference`
([modèle de données §6.2.3](modele-de-donnees.md)).

**6.4.** `effect` et `retryable` sont indépendants.

**6.5.** Une erreur `unknown` NE DOIT PAS avoir été enregistrée au titre de
l'[idempotence](idempotence.md) ; un renvoi est traité selon idempotence §7.

## 7. Erreurs par champ

**7.1.** Si l'erreur concerne des champs précis, `errors` DEVRAIT être présent :

| Membre | Type | Présence | Notes |
|---|---|---|---|
| `field` | chaîne | OBLIGATOIRE | JSON Pointer (RFC 6901) dans le corps de la requête. |
| `code` | chaîne | OBLIGATOIRE | Code stable. |
| `detail` | chaîne | FACULTATIF | Lisible, non stable. |

```json
{
  "type": "https://openfsp.org/problems/invalid-field",
  "title": "One or more fields are invalid",
  "status": 422,
  "retryable": false,
  "effect": "none",
  "request_id": "req_01J9ZK…",
  "errors": [
    { "field": "/amount/amount", "code": "not_positive" },
    { "field": "/payer/phone_number", "code": "malformed" }
  ]
}
```

**7.2.** La passerelle DEVRAIT rapporter tous les champs invalides dans une seule réponse.

**7.3.** `field` DOIT désigner la requête telle qu'envoyée par le client.

## 8. Relais de l'opérateur

**8.1.** Pour une erreur venant de l'opérateur, `provider_detail` DEVRAIT porter son code et
son message :

```json
"provider_detail": { "code": "E4021", "message": "Subscriber not registered" }
```

**8.2.** La passerelle NE DOIT PAS l'analyser ni en dériver `type`, `retryable` ou `effect`,
et DOIT le relayer sans altération.

**8.3.** Un client NE DOIT PAS s'appuyer sur `provider_detail` pour une décision
programmatique.

**8.4.** `provider_detail` NE DOIT contenir aucun identifiant secret, jeton ou matériel
d'authentification ; la passerelle DOIT caviarder un tel contenu.

## 9. Catalogue

Fermé ; l'étendre requiert une ADR. La correspondance avec ISO 20022 est dans
[ISO 20022](iso-20022.md).

### 9.1. Requête

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `malformed-request` | 400 | false | `none` | Corps non JSON ou non objet. |
| `unknown-field` | 400 | false | `none` | Champ inconnu ([modèle de données §2.4](modele-de-donnees.md)). |
| `missing-field` | 400 | false | `none` | Champ obligatoire absent. |
| `idempotency-key-required` | 400 | false | `none` | `Idempotency-Key` absente ([idempotence §1.3](idempotence.md)). |
| `invalid-field` | 422 | false | `none` | Contenu invalide. Porte `errors`. |
| `capability-not-supported` | 422 | false | `none` | Capacité non annoncée. |
| `amount-out-of-range` | 422 | false | `none` | Montant hors des bornes annoncées ([plafonds §3](plafonds.md)). |
| `idempotency-key-reused` | 422 | false | `none` | Même clé, corps différent ([idempotence §3.3](idempotence.md)). |

### 9.2. Authentification

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `unauthenticated` | 401 | false | `none` | Identifiant absent, mal formé ou invalide. |
| `forbidden` | 403 | false | `none` | Authentifié, non autorisé. |

### 9.3. Ressource

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `not-found` | 404 | false | `none` | Ressource inexistante. |

**9.3.1.** La passerelle DOIT renvoyer `not-found` plutôt que `forbidden` lorsque la
distinction révélerait l'existence de la ressource.

### 9.4. Conflits

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `reference-conflict` | 409 | false | `none` | `reference` déjà utilisée ([modèle de données §6.2.2](modele-de-donnees.md)). |
| `idempotency-request-in-progress` | 409 | true | `unknown` | Requête de même clé en cours ([idempotence §3.4](idempotence.md)). |
| `state-conflict` | 409 | false | `none` | Opération interdite depuis l'état courant ([cycle de vie §2.1](cycle-de-vie.md)). |

**9.4.1.** Sur `reference-conflict`, le client DEVRAIT lire la ressource existante.

**9.4.2.** `idempotency-request-in-progress` DEVRAIT porter `Retry-After`.

### 9.5. Débit

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `rate-limited` | 429 | true | `none` | Trop de requêtes. DOIT porter `Retry-After`. |

### 9.6. Passerelle et opérateur

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `internal-error` | 500 | true | `unknown` | Défaillance inattendue de la passerelle. |
| `provider-error` | 502 | true | `unknown` | Erreur ou réponse inexploitable de l'opérateur. |
| `provider-unavailable` | 503 | true | `none` | Opérateur injoignable. |
| `provider-timeout` | 504 | true | `unknown` | Pas de réponse de l'opérateur à temps. |

**9.6.1.** `provider-unavailable` NE DOIT être utilisé que si aucune requête n'a atteint
l'opérateur (connexion refusée, échec DNS). Si une requête a été envoyée sans dénouement
connu, `provider-timeout` s'applique.

**9.6.2.** `internal-error` DOIT porter `unknown`, sauf si la passerelle établit qu'aucun appel
à l'opérateur n'a eu lieu.

**9.6.3.** `internal-error` NE DOIT PAS inclure de diagnostic interne (trace, requête, nom
d'hôte).

### 9.7. Paiement de proximité

| Code | Statut | `retryable` | `effect` | Condition |
|---|---|---|---|---|
| `payer-token-invalid` | 422 | false | `none` | Jeton non reconnu par l'opérateur ([proximité §6](proximite.md)). |
| `payer-token-expired` | 422 | false | `none` | Jeton reconnu, durée de vie dépassée. |
| `payer-token-used` | 409 | false | `none` | Jeton reconnu, déjà résolu. |

## 10. Langue

**10.1.** `title` et `detail` DEVRAIENT être en anglais par défaut.

**10.2.** Une passerelle PEUT les localiser et DEVRAIT alors honorer `Accept-Language`.

**10.3.** La localisation NE DOIT PAS modifier `type`, `retryable`, `effect` ni aucun `code`.

## 11. Sécurité

**11.1.** `title`, `detail` et `errors[].detail` NE DOIVENT PAS contenir de numéro de
téléphone, d'identifiant de payeur ni de montant.

**11.2.** `unauthenticated` NE DOIT PAS distinguer un principal inconnu d'un identifiant
invalide.

**11.3.** Les SDK DEVRAIENT documenter que `provider_detail` doit être échappé à l'affichage.
