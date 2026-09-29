# Plafonds de montant

Décision : [ADR-0018](../text/0018-amount-limits.md).

## 1. Bornes

**1.1.** Les bornes d'un opérateur sont le montant minimal et le montant maximal d'une
transaction sur le compte marchand, fixés par l'opérateur pour ce marchand.

**1.2.** L'exploitant déclare les bornes dans l'administration de la passerelle, par opérateur.

**1.3.** La passerelle NE DOIT PAS inventer une borne, ni en déduire une des échecs passés.

## 2. Annonce

**2.1.** L'objet `payments` d'un opérateur ([capacités §3.2.2](capacites.md)) porte un membre
FACULTATIF `limits` :

```json
"limits": {
  "min_amount": { "amount": 1000, "currency": "HTG" },
  "max_amount": { "amount": 7500000, "currency": "HTG" },
  "amount_step": { "amount": 100, "currency": "HTG" }
}
```

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `min_amount` | `Money` | FACULTATIF | Absent signifie non connu. |
| `max_amount` | `Money` | FACULTATIF | Absent signifie non connu. |
| `amount_step` | `Money` | FACULTATIF | Le montant DOIT en être un multiple. `100` : gourdes entières. |

**2.2.** Une borne absente signifie « non connue », pas « illimitée ». Un client NE DOIT PAS
l'afficher comme une absence de plafond.

**2.3.** Si `min_amount` et `max_amount` sont présents, `min_amount` DOIT être inférieur ou égal
à `max_amount`.

## 3. Contrôle

**3.1.** À la création ([API §5.1](api-paiements.md)), la passerelle DOIT rejeter un montant
inférieur à `min_amount`, supérieur à `max_amount` ou non multiple de `amount_step`, avec
`amount-out-of-range`, avant tout appel à l'opérateur.

**3.2.** La réponse porte les bornes en membres d'extension :

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

**3.3.** C'est une erreur causée par la requête : la réponse est enregistrée au titre de
l'[idempotence §5.1](idempotence.md). Après un changement de bornes, le client DOIT réessayer
avec une nouvelle clé.

**3.4.** Un paiement refusé par l'opérateur pour un plafond du payeur, ou pour une borne que la
passerelle ne connaissait pas, prend `failed` avec `limit_exceeded`
([cycle de vie §7.2](cycle-de-vie.md)). La passerelle NE DOIT PAS le convertir en
`amount-out-of-range`.

## 4. Conformité

**4.1.** La suite teste le §3.1 aux deux bornes (borne acceptée, borne dépassée d'un centime)
et vérifie qu'aucun appel n'atteint l'opérateur simulé.

## 5. Sécurité

**5.1.** Les bornes révèlent une partie du contrat du marchand. Elles ne sont servies que par le
point d'accès authentifié des capacités, jamais par le descripteur public
([capacités §3.1.1](capacites.md)).
