# Demandes de confirmation

Décision : [ADR-0011](../text/0011-confirmation-requests.md).

## 1. Ressource

**1.1.** Une demande de confirmation est une décision soumise au payeur au sujet d'un paiement,
avec une échéance.

```json
{
  "id": "cnf_01J9ZM8W4B7XKQ2R5T3N6P0V9D",
  "payment_id": "pay_01J9ZK3QF8XN2M7VYB4C6D8E0G",
  "reference": "POS-2026-09-06-0042",
  "status": "awaiting",
  "amount": { "amount": 45000, "currency": "HTG" },
  "provider": "moncash",
  "created_at": "2026-09-06T13:04:19.882Z",
  "updated_at": "2026-09-06T13:04:19.882Z",
  "expires_at": "2026-09-06T13:05:19.882Z",
  "resolved_at": null,
  "outcome_reason": null,
  "outcome_detail": null
}
```

**1.2.** Champs :

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `id` | `ResourceId` | OBLIGATOIRE | |
| `payment_id` | `ResourceId` | OBLIGATOIRE | Paiement concerné. Immuable. |
| `reference` | `Reference` | OBLIGATOIRE | Copie de celle du paiement (§1.4). |
| `status` | chaîne | OBLIGATOIRE | §2. |
| `amount` | `Money` | OBLIGATOIRE | Montant soumis au payeur (§1.5). |
| `provider` | chaîne | OBLIGATOIRE | Comme sur un paiement. |
| `created_at` | `Timestamp` | OBLIGATOIRE | Soumission au payeur. |
| `updated_at` | `Timestamp` | OBLIGATOIRE | |
| `expires_at` | `Timestamp` | OBLIGATOIRE | §3. |
| `resolved_at` | `Timestamp` | conditionnel | OBLIGATOIRE une fois terminal. |
| `outcome_reason` | chaîne | conditionnel | OBLIGATOIRE si `declined` (§6). |
| `outcome_detail` | objet | FACULTATIF | Erreur brute de l'opérateur. |

**1.3.** Un paiement a au plus une demande de confirmation. La passerelle DOIT rejeter une
seconde demande avec `state-conflict`, quel que soit l'état de la première.

**1.4.** `reference` est celle du paiement : la recherche par référence atteint les deux
objets.

**1.5.** La passerelle NE DOIT PAS créer une demande dont le montant diffère de celui du
paiement.

**1.6.** Un client ne crée jamais directement une demande : elle naît avec un paiement dans un
flux qui l'exige ([proximité](proximite.md)).

## 2. États

| État | Terminal | Sens |
|---|---|---|
| `awaiting` | non | Soumise, sans réponse connue. |
| `approved` | oui | Le payeur a approuvé. Les fonds n'ont pas nécessairement bougé (§5). |
| `declined` | oui | Refus du payeur, ou de l'opérateur en son nom. |
| `expired` | oui | Échéance passée sans réponse, confirmée (§3.4). |
| `canceled` | oui | Retirée avant réponse, confirmé par l'opérateur (§7). |

**2.1.** `awaiting` est le seul état non terminal.

**2.2.** La terminalité du [cycle de vie §3.1](cycle-de-vie.md) s'applique. Un client DOIT
rejeter un `status` inconnu.

**2.3.** Un client NE DOIT PAS déduire l'état du paiement de celui de la demande, ni
l'inverse, hors du §4.

## 3. Échéance

**3.1.** `expires_at` est OBLIGATOIRE et fixé à la création.

**3.2.** La valeur est celle de l'opérateur. S'il n'en déclare pas, la passerelle DOIT appliquer
la sienne, sans dépasser ce que l'opérateur honore.

**3.3.** La fenêtre DEVRAIT être de 60 secondes et NE DOIT PAS dépasser 300 secondes.

**3.4.** La passerelle NE DOIT PAS passer une demande à `expired` sur sa seule horloge :
l'expiration est confirmée par l'opérateur, ou établie par une relecture postérieure à
l'échéance sans approbation.

**3.5.** Un client PEUT afficher le temps restant et DEVRAIT arrêter le décompte à zéro sans
afficher de dénouement tant que le §3.4 n'est pas satisfait.

## 4. Rapport au paiement

**4.1.** Tant que la demande est `awaiting`, le paiement porte un `next_action` de type
`confirmation_request`, ajouté à l'[API §4.2](api-paiements.md) :

| `type` | Sens | Champs |
|---|---|---|
| `confirmation_request` | Le payeur doit approuver une demande déjà poussée, dans le délai affiché. | `confirmation_request_id`, `expires_at` |

**4.2.** `next_action.expires_at` est égal à l'`expires_at` de la demande.

**4.3.** Le paiement reste `pending` tant que la demande est `awaiting`.

**4.4.** Projection obligatoire des dénouements :

| Demande | Paiement |
|---|---|
| `approved` | reste `pending` jusqu'à confirmation de la capture, puis `succeeded` |
| `declined` | `failed`, `failure_reason` `payer_canceled` (ou valeur du §6.2) |
| `expired` | `expired` |
| `canceled` | `canceled` |

**4.5.** La passerelle NE DOIT PAS passer le paiement à un état terminal sur un dénouement de
demande qu'elle n'a pas elle-même enregistré comme terminal.

## 5. Approbation et capture

**5.1.** `approved` signifie consentement, pas mouvement de fonds. Un client NE DOIT PAS remettre
de marchandise, imprimer de reçu ni rapporter de succès sur la foi d'`approved`, et DOIT se
fonder sur le `status` du paiement.

**5.2.** Entre `approved` et `succeeded`, un client DEVRAIT afficher que le paiement est en cours
d'achèvement.

**5.3.** Un client NE DOIT PAS faire de la remise anticipée sur `approved` son comportement par
défaut ; ce choix appartient au marchand.

## 6. `outcome_reason`

**6.1.** Si `status` vaut `declined`, `outcome_reason` DOIT prendre l'une de ces valeurs :

| Valeur | Sens |
|---|---|
| `payer_declined` | Le payeur a refusé. |
| `insufficient_funds` | Solde insuffisant. |
| `limit_exceeded` | Plafond de l'opérateur ou réglementaire. |
| `rejected_by_provider` | Refus propre à l'opérateur (risque, conformité). |
| `unspecified` | Refus sans motif exploitable. |

**6.2.** La passerelle DEVRAIT reporter la valeur correspondante sur le `failure_reason` du
paiement ; `payer_declined` correspond à `payer_canceled`.

**6.3.** L'énumération est fermée. Un client DOIT traiter une valeur inconnue comme
`unspecified`.

**6.4.** `outcome_detail` porte le code et le message de l'opérateur, caviardés selon
l'[authentification §9.5](authentification.md).

**6.5.** Une demande expirée est dans l'état `expired`, jamais `declined`.

## 7. Annulation

**7.1.** Requête :

```
POST /v1/confirmation_requests/{id}/cancel
```

Portée `payments:write`.

**7.2.** L'opération porte `Idempotency-Key` ([idempotence](idempotence.md)).

**7.3.** La passerelle demande le retrait à l'opérateur. La demande n'atteint `canceled` que sur
confirmation de l'opérateur qu'elle a été retirée sans approbation.

**7.4.** La passerelle NE DOIT PAS rapporter `canceled` sur le seul envoi de l'annulation. Sans
réponse de l'opérateur, la demande reste `awaiting`.

**7.5.** L'annulation PEUT perdre contre une approbation simultanée. Un client DOIT traiter ce
cas et NE DOIT PAS traiter la réponse `202` comme une preuve du résultat.

**7.6.** Réponse : `202 Accepted` avec la demande dans son état courant.

**7.7.** Annuler une demande terminale renvoie `state-conflict` sans effet.

**7.8.** Sans opération de retrait chez l'opérateur, la passerelle NE DOIT PAS annoncer
`confirmation_requests.cancel` et DOIT renvoyer `capability-not-supported`.

## 8. Lecture et événements

**8.1.** `GET /v1/confirmation_requests/{id}`, portée `payments:read`.

**8.2.** Tant qu'elle est `awaiting`, la demande est atteignable par le `next_action` du paiement ;
ensuite par son identifiant ou la référence du paiement.

**8.3.** Une application de comptoir DEVRAIT sonder à intervalle court fixe.

**8.4.** Types d'événement ajoutés aux [webhooks](webhooks.md) : `confirmation_request.approved`,
`confirmation_request.declined`, `confirmation_request.expired`,
`confirmation_request.canceled`, avec `resource_type` `confirmation_request`.

**8.5.** Pas d'événement `confirmation_request.created`.

**8.6.** Une application de comptoir NE DEVRAIT PAS dépendre d'un événement pour la décision.

## 9. Capacité et conformité

**9.1.** Capacité `confirmation_requests`. La passerelle NE DOIT l'annoncer que si l'opérateur
offre réellement une confirmation minutée, jamais sur la foi d'une simulation.

**9.2.** L'annulation est annoncée séparément : `confirmation_requests.cancel`.

**9.3.** Cette capacité ne s'obtient pas par adaptation ; sa cible de conformité est une
implémentation native de l'opérateur ou le simulateur.

**9.4.** La suite exerce au minimum : approbation, refus, expiration, annulation gagnante,
annulation perdante contre une approbation simultanée, approbation suivie d'un échec de
capture.
