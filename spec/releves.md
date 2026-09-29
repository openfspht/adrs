# Relevés et rapprochement

Décision : [ADR-0017](../text/0017-statements-and-reconciliation.md).

## 1. Journée comptable

**1.1.** Le type `Date` est une chaîne `full-date` RFC 3339 : `"2026-09-28"`.

**1.2.** La journée comptable d'une ligne est la date que lui attribue l'opérateur. S'il n'en
attribue pas, c'est la date de `booked_at` dans le fuseau IANA `America/Port-au-Prince`.

**1.3.** La passerelle NE DOIT PAS dériver une journée comptable d'un décalage horaire fixe :
Haïti applique l'heure d'été.

## 2. Relevé

**2.1.** Un relevé regroupe les mouvements du compte marchand chez un opérateur pour une
journée comptable.

```json
{
  "id": "stm_01J9ZQ0R8V2K4M6N8P0Q2R4S6T",
  "provider": "moncash",
  "business_date": "2026-09-28",
  "complete": true,
  "entries": [
    {
      "provider_reference": "MC-8837291",
      "type": "payment",
      "amount": { "amount": 125000, "currency": "HTG" },
      "fee": { "amount": 1250, "currency": "HTG" },
      "net_amount": { "amount": 123750, "currency": "HTG" },
      "booked_at": "2026-09-28T14:33:02Z",
      "payment": "pay_01J9ZK3QF8XN2M7VYB4C6D8E0G",
      "match": "matched",
      "source": "provider"
    }
  ],
  "missing_payments": []
}
```

**2.2.** Champs du relevé :

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `id` | `ResourceId` | OBLIGATOIRE | |
| `provider` | chaîne | OBLIGATOIRE | Identifiant enregistré. |
| `business_date` | `Date` | OBLIGATOIRE | §1. |
| `complete` | booléen | OBLIGATOIRE | §2.4. |
| `entries` | tableau | OBLIGATOIRE | §3. |
| `missing_payments` | tableau de `ResourceId` | OBLIGATOIRE | §4.4. Vide tant que `complete` vaut `false`. |

**2.3.** Il y a au plus un relevé par (opérateur, journée comptable).

**2.4.** `complete` vaut `true` quand l'opérateur a clos la journée. Un relevé non clos PEUT
recevoir de nouvelles lignes ; un relevé clos NE DOIT PAS en recevoir par la source
`provider`.

## 3. Ligne

**3.1.** Champs :

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `provider_reference` | `ProviderReference` | OBLIGATOIRE | |
| `type` | chaîne | OBLIGATOIRE | §3.2. |
| `amount` | `Money` | OBLIGATOIRE | Brut, signé : positif au crédit du marchand. |
| `fee` | `Money` | FACULTATIF | Tel que rapporté. Absent signifie non connu. |
| `net_amount` | `Money` | FACULTATIF | Tel que rapporté. Absent signifie non connu. |
| `booked_at` | `Timestamp` | OBLIGATOIRE | Heure de comptabilisation chez l'opérateur. |
| `payment` | `ResourceId` | conditionnel | Présent si `match` vaut `matched` ou `conflict`. |
| `match` | chaîne | OBLIGATOIRE | §4. |
| `source` | chaîne | OBLIGATOIRE | `provider` ou `import` (§5). |

**3.2.** `type` prend l'une des valeurs `payment`, `reversal`, `fee`, `adjustment`.
L'énumération est fermée ; l'étendre requiert une ADR. Un client DOIT traiter une valeur
inconnue comme `adjustment`.

**3.3.** Par exception au [modèle de données §3.6](modele-de-donnees.md), `amount`, `fee` et
`net_amount` d'une ligne PEUVENT être négatifs ou nuls.

**3.4.** La passerelle NE DOIT PAS calculer `fee` ni `net_amount`, ni les compléter par
soustraction.

## 4. Rapprochement

**4.1.** La passerelle rapproche une ligne d'un paiement par `provider_reference`, puis, si
l'opérateur la transmet, par `Reference`. Elle NE DOIT PAS rapprocher par montant ou par heure.

**4.2.** `match` prend l'une des valeurs :

| Valeur | Sens |
|---|---|
| `matched` | Un paiement correspond ; montant et état concordent. |
| `unmatched` | Aucun paiement ne correspond. |
| `conflict` | Un paiement correspond, mais son montant ou son état contredit la ligne. |

**4.3.** Une ligne `unmatched` NE DOIT PAS créer de paiement. La passerelle DOIT la signaler à
l'exploitant.

**4.4.** Un relevé clos DOIT lister dans `missing_payments` les paiements `succeeded` chez cet
opérateur dont `completed_at` tombe dans la journée comptable et qu'aucune ligne ne rapproche.

**4.5.** Un `conflict` sur un paiement terminal relève du [cycle de vie §6.4](cycle-de-vie.md).
Sur un paiement `pending`, une ligne `payment` de source `provider` fonde `succeeded` au titre
du [cycle de vie §6.7](cycle-de-vie.md).

## 5. Import

**5.1.** L'exploitant PEUT importer un relevé par l'administration de la passerelle. Ses lignes
portent `source: "import"`. L'import DEVRAIT accepter tel quel l'export du portail de
l'opérateur ; sa conversion relève de l'adaptateur.

**5.2.** Une ligne `import` relève de l'attestation ([cycle de vie §6.8](cycle-de-vie.md)) et
NE DOIT PAS fonder seule une transition au titre du §6.7.

**5.3.** Un relevé contenant une ligne `import` NE DOIT PAS avoir `complete` à `true` sur la
seule foi de l'import.

## 6. Points d'accès

**6.1.** Lire un relevé :

```
GET /v1/statements?provider=moncash&business_date=2026-09-28
```

`provider` et `business_date` sont OBLIGATOIRES. Réponse `200` avec le relevé, ou `not-found`
s'il n'existe pas encore.

**6.2.** Lister les lignes non rapprochées :

```
GET /v1/statement-entries?match=unmatched&provider=moncash
```

`match` PEUT valoir `unmatched` ou `conflict`. La réponse est une collection
([API §1.12](api-paiements.md)) triée par
`booked_at` croissant, d'au plus `limit` éléments (1 à 100, 50 par défaut). S'il en reste,
elle porte `next_cursor`, chaîne opaque à renvoyer dans le paramètre `cursor`.

**6.3.** Les deux points d'accès exigent la portée `statements:read`
([authentification §6](authentification.md)).

**6.4.** Ils sont servis pour tout opérateur. Les lignes viennent de l'opérateur, s'il annonce
`payments.statement`, ou d'un import (§5).


## 7. Conformité

**7.1.** La suite teste, avec un opérateur simulé qui publie un relevé : une ligne rapprochée,
une ligne orpheline (aucun paiement créé), un paiement `succeeded` absent d'un relevé clos, et
une journée comptable à cheval sur le changement d'heure.

## 8. Sécurité

**8.1.** Un relevé révèle le chiffre d'affaires du marchand. `statements:read` NE DEVRAIT PAS
être accordée à une clé qui ne sert qu'à encaisser.
