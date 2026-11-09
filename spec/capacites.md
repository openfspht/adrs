# Découverte de capacités

Je justifie ces choix dans l'[ADR-0007](../text/0007-capability-discovery.md).

## 1. Capacité

**1.1.** Une capacité est une fonctionnalité nommée, prise en charge ou non pour un opérateur
donné.

**1.2.** Les capacités sont rapportées par opérateur, jamais pour la passerelle entière.

**1.3.** Une passerelle DOIT n'annoncer une capacité que si l'opérateur exécute l'opération
lui-même. Elle NE DOIT PAS annoncer une capacité obtenue par émulation,
approximation ou composition d'autres opérations.

**1.4.** Capacité `payments` : [API 2.1](api-paiements.md).

## 2. Noms et registre

**2.1.** Un nom de capacité correspond à `^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$` : domaine,
puis opération.

**2.2.** Registre. Un nom *réservé* n'a pas encore de spécification et NE DOIT PAS être
annoncé.

| Nom | Statut | Sens |
|---|---|---|
| `payments` | spécifié, obligatoire | Créer, lire, synchroniser un paiement ([API](api-paiements.md)). |
| `payments.lookup` | spécifié | Consultation faisant foi de l'état chez l'opérateur (5). |
| `payments.statement` | spécifié | Relevé des transactions par canal authentifié ([cycle de vie 6.7](cycle-de-vie.md)), lisible par le client ([relevés](cycle-de-vie.md#10-relevés-et-rapprochement)). |
| `payments.fee` | spécifié | L'opérateur rapporte les frais ([modèle de données 8](modele-de-donnees.md)). |
| `payments.refund` | réservé | Remboursement d'un paiement capturé. |
| `payments.capture` | réservé | Autorisation et capture séparées. |
| `payments.cancel` | réservé | Annulation avant achèvement. |
| `payments.proximity_cpm` | réservé | Résolution native de jetons présentés par le payeur. |
| `confirmation_requests` | réservé | Confirmation minutée par le payeur. |
| `confirmation_requests.cancel` | réservé | Retrait d'une demande avant réponse du payeur. |
| `transfers` | réservé | Envoi de fonds à un bénéficiaire. |
| `webhooks.emit` | spécifié | Événements signés vers le client ([webhooks](webhooks.md)). |
| `webhooks.verify` | spécifié | Rappels signés par l'opérateur ([cycle de vie 6.5](cycle-de-vie.md) a). |
| `webhooks.per_payment_url` | spécifié | URL de rappel propre à chaque paiement ([cycle de vie 6.6](cycle-de-vie.md)). |

**2.3.** Ajouter un nom requiert une ADR. Un ajout n'est pas une rupture (4.3).

**2.4.** Une passerelle PEUT annoncer des noms hors registre, préfixés d'un nom DNS inversé
qu'elle contrôle (`com.example.payments.instalments`), et NE DOIT PAS inventer de noms non
préfixés.

**2.5.** Les capacités ne sont pas versionnées : un changement de sens exige un nouveau nom.

**2.6.** La passerelle DOIT utiliser l'identifiant enregistré de chaque opérateur
([registre](https://github.com/openfspht/openfsp/blob/main/registries/providers.md)).

**2.7.** Un identifiant d'opérateur s'enregistre par pull request sur le registre, sans ADR.

**2.8.** Les identifiants sont permanents ; un opérateur renommé reçoit un nouvel identifiant
et l'ancien est marqué remplacé.

## 3. Découverte

### 3.1. Descripteur de service

```
GET /.well-known/openfsp
```

Non authentifié (RFC 8615).

```json
{
  "protocol_version": "0.1.0",
  "api_base": "https://gateway.example/v1",
  "capabilities_url": "https://gateway.example/v1/capabilities"
}
```

**3.1.1.** Le descripteur NE DOIT PAS révéler les opérateurs utilisés, ni d'information sur le
marchand, ni la version du logiciel de la passerelle.

**3.1.2.** `protocol_version` est la version de spécification visée. Un client NE DOIT PAS en
déduire de capacité.

### 3.2. Capacités

```
GET /v1/capabilities
```

Authentifié.

```json
{
  "protocol_version": "0.1.0",
  "providers": [
    {
      "id": "moncash",
      "display_name": "MonCash",
      "capabilities": ["payments", "payments.lookup"],
      "payments": {
        "next_actions": ["redirect"],
        "payer_required": false,
        "return_url_required": true,
        "expiry_guaranteed": false,
        "locales": []
      }
    }
  ]
}
```

**3.2.1.** Champs d'un opérateur :

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `id` | chaîne | OBLIGATOIRE | Identifiant enregistré ; égal à `provider` d'un paiement. |
| `display_name` | chaîne | OBLIGATOIRE | Affichage, pas un identifiant. |
| `capabilities` | tableau de chaînes | OBLIGATOIRE | Contient toujours `payments`. |
| `payments` | objet | OBLIGATOIRE | 3.2.2. |

**3.2.2.** Objet `payments` :

| Champ | Type | Sens |
|---|---|---|
| `next_actions` | tableau de chaînes | Types de `next_action` produits ([API 4.2](api-paiements.md)). |
| `payer_required` | booléen | `payer` exigé à la création. |
| `return_url_required` | booléen | `return_url` exigée à la création. |
| `expiry_guaranteed` | booléen | Garantie du [cycle de vie 5.3](cycle-de-vie.md) c. |
| `limits` | objet | FACULTATIF. Bornes de montant (6.4). |
| `locales` | tableau de chaînes | Valeurs de `locale` transmises à l'opérateur ([API 5.1.7](api-paiements.md)). |

**3.2.3.** `expiry_guaranteed` DOIT valoir `false` sauf si la condition du
[cycle de vie 5.3](cycle-de-vie.md) (c) est remplie.

**3.2.4.** La réponse DEVRAIT porter `Cache-Control` avec un `max-age` d'une heure au plus.

## 4. Obligations

**4.1.** Un client NE DOIT PAS invoquer une opération dont la capacité n'est pas annoncée pour
l'opérateur choisi.

**4.2.** Un client DOIT traiter `capability-not-supported` à tout moment, et DEVRAIT alors
relire les capacités.

**4.3.** Un client DOIT ignorer un nom de capacité inconnu.

**4.4.** La passerelle DOIT rejeter avec `capability-not-supported` toute opération dont elle
n'annonce pas la capacité, même si elle peut l'exécuter.

**4.5.** La passerelle DOIT tenir l'ensemble annoncé à jour et NE DOIT PAS annoncer une
capacité suspendue par l'opérateur.

## 5. `payments.lookup`

**5.1.** `payments.lookup` annonce une consultation faisant foi de l'état courant chez
l'opérateur.

**5.2.** Si elle est annoncée, la synchronisation ([API 5.3](api-paiements.md)) DOIT lire
l'état chez l'opérateur.

**5.3.** Sinon, la synchronisation DOIT renvoyer `capability-not-supported` et NE DOIT PAS
renvoyer l'état stocké comme s'il avait été relu.

**5.3.1.** Exception : un paiement terminal est renvoyé inchangé en `200`
([API 5.3.3](api-paiements.md)).

**5.4.** Sans `payments.lookup`, le rapprochement s'appuie sur les autres sources du
[cycle de vie 6.5](cycle-de-vie.md).

## 6. Plafonds de montant

**6.1.** Les bornes d'un opérateur sont le montant minimal et le montant maximal d'une
transaction sur le compte marchand, fixés par l'opérateur pour ce marchand.

**6.2.** L'exploitant déclare les bornes dans l'administration de la passerelle, par opérateur.

**6.3.** La passerelle NE DOIT PAS inventer une borne, ni en déduire une des échecs passés.

**6.4.** L'objet `payments` d'un opérateur (3.2.2) porte un membre FACULTATIF `limits` :

```json
"limits": {
  "min_amount": { "amount": 1000, "currency": "HTG" },
  "max_amount": { "amount": 7500000, "currency": "HTG" },
  "amount_step": { "amount": 100, "currency": "HTG" }
}
```

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `min_amount` | `Money` | FACULTATIF | 6.5. |
| `max_amount` | `Money` | FACULTATIF | 6.5. |
| `amount_step` | `Money` | FACULTATIF | Le montant DOIT en être un multiple. `100` : gourdes entières. |

**6.5.** Une borne absente signifie « non connue », pas « illimitée ». Un client NE DOIT PAS
l'afficher comme une absence de plafond.

**6.6.** Si `min_amount` et `max_amount` sont présents, `min_amount` DOIT être inférieur ou égal
à `max_amount`.

**6.7.** À la création ([API 5.1](api-paiements.md)), la passerelle DOIT rejeter un montant
inférieur à `min_amount`, supérieur à `max_amount` ou non multiple de `amount_step`, avec
`amount-out-of-range`, avant tout appel à l'opérateur. La réponse porte les bornes en membres
d'extension :

```json
{
  "type": "https://openfsp.org/problems/amount-out-of-range",
  "title": "Amount out of range",
  "status": 422,
  "retryable": false,
  "effect": "none",
  "request_id": "req_01J9ZR2T4V6X8Z0B2D4F6H8K0M",
  "min_amount": { "amount": 1000, "currency": "HTG" },
  "max_amount": { "amount": 7500000, "currency": "HTG" },
  "amount_step": { "amount": 100, "currency": "HTG" }
}
```

**6.8.** `amount-out-of-range` est une erreur causée par la requête : sa réponse est enregistrée au titre de
l'[idempotence 5.1](idempotence.md). Après un changement de bornes, un client qui soumet de
nouveau la création DOIT utiliser une nouvelle `Idempotency-Key`.

**6.9.** Un paiement refusé par l'opérateur pour un plafond du payeur, ou pour une borne que la
passerelle ne connaissait pas, prend `failed` avec `limit_exceeded`
([cycle de vie 7.2](cycle-de-vie.md)). La passerelle NE DOIT PAS le convertir en
`amount-out-of-range`.

## 7. Conformité

**7.1.** Une passerelle conforme DOIT servir les deux points d'accès du 3.

**7.2.** La suite de conformité vérifie le 2.2.

**7.3.** La suite teste le 6.7 aux deux bornes (borne acceptée, borne dépassée d'un centime)
et vérifie qu'aucun appel n'atteint l'opérateur simulé.

## 8. Sécurité

**8.1.** Le descripteur public DEVRAIT être limité en débit.

**8.2.** L'annonce d'une capacité ne confère aucune autorisation : la passerelle DOIT contrôler
la portée de la clé indépendamment ([authentification 6](authentification.md)).

**8.3.** Les bornes ne sont servies que par le point d'accès authentifié du 3.2,
jamais par le descripteur public (3.1.1).
