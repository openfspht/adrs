# Adaptateurs d'opérateur

Informatif. Décision : [ADR-0013](../text/0013-provider-adapter-interface.md). Ce document ne crée
aucune obligation ; il rassemble celles des autres spécifications qui s'appliquent à un
adaptateur.

## 1. Rôle

**1.1.** Un adaptateur traduit une opération OpenFSP vers l'API d'un opérateur et retraduit la
réponse. Il ne détient ni l'enregistrement de paiement, ni le magasin d'idempotence, ni les
transitions d'état, ni l'audit.

**1.2.** Un adaptateur rapporte ce que l'opérateur a dit, ou son incapacité à le savoir.

**1.3.** L'adaptateur est le seul composant qui détient un identifiant d'opérateur
([authentification §9](authentification.md)).

## 2. Opérations

| Opération | Règle | Obligatoire |
|---|---|---|
| Créer un paiement | [API §5.1](api-paiements.md) | oui |
| Lire un paiement chez l'opérateur | [API §5.3](api-paiements.md), `payments.lookup` | non |
| Ingérer un rappel | [cycle de vie §6.3, §6.6](cycle-de-vie.md) | non |
| Lire un relevé | [cycle de vie §6.7](cycle-de-vie.md), `payments.statement` | non |
| Convertir un export de portail | [relevés §5](releves.md) | non |
| Résoudre un jeton de payeur | [proximité §3](proximite.md), `payments.proximity_cpm` | non |
| Retirer une demande de confirmation | [demandes de confirmation §7](demandes-de-confirmation.md), `confirmation_requests.cancel` | non |

**2.1.** Lire un paiement dans le magasin de la passerelle n'est pas une opération d'adaptateur.

**2.2.** Une opération que l'opérateur ne sait pas faire n'est ni implémentée ni déclarée ; pas
d'implémentation partielle qui renvoie une erreur.

## 3. Refus

**3.1.** Aucune capacité inventée : l'adaptateur déclare ce que fait l'opérateur, jamais ce que
la passerelle pourrait simuler ([capacités §1.3, §5.3](capacites.md)).

**3.2.** Aucune terminalité inventée : un statut inconnu ne correspond à rien et le paiement reste
`pending` ([cycle de vie §1.1](cycle-de-vie.md)) ; un motif incertain donne `unspecified`
([cycle de vie §7.3](cycle-de-vie.md)).

**3.3.** Aucun renvoi invérifiable : après un dénouement indéterminé, établir d'abord l'état ;
utiliser l'idempotence ou la recherche de l'opérateur ; à défaut, ne pas renvoyer
([idempotence §7](idempotence.md)).

## 4. Déclaration

**4.1.** L'adaptateur déclare les capacités du [registre](capacites.md) qu'il prend en charge.

**4.2.** La déclaration est statique par opérateur.

**4.3.** Elle inclut le profil de paiement : types de `next_action`, `payer` exigé, `return_url`
exigée, expiration garantie ([capacités §3.2.2](capacites.md)).

## 5. Correspondances

**5.1.** La correspondance des statuts de l'opérateur est totale, ou documentée comme partielle ;
chaque statut observé correspond à un état OpenFSP ou à rien.

**5.2.** Elle va de l'opérateur vers OpenFSP, jamais l'inverse.

**5.3.** Un statut ambigu de l'opérateur (« pas encore agi » ou « inconnu ») correspond à
`pending`.

**5.4.** `failure_detail` porte le code et le message de l'opérateur, caviardés
([authentification §9.5](authentification.md)).

**5.5.** `provider-unavailable` seulement si la requête n'a jamais atteint l'opérateur ; sinon
`provider-timeout` ([erreurs §9.6.1](erreurs.md)).

## 6. Rappels

**6.1.** Rappel signé : vérifier ; un rappel invérifiable est rejeté.

**6.2.** Rappel non signé : signal pour consulter une source autoritative, contenu ignoré.

**6.3.** Sans consultation, l'adaptateur déclare les sources restantes (URL propre au paiement,
relevé) ; sans aucune, chaque paiement attend une attestation ([cycle de vie §6.5](cycle-de-vie.md)).

**6.4.** La protection contre le rejeu s'applique aux rappels signés comme non signés.

## 7. Document publié par adaptateur

| Élément | Usage |
|---|---|
| Capacités et profil de paiement | Base d'écriture d'un client. |
| Correspondance des statuts, y compris sans correspondance | Comportement face à un statut imprévu. |
| Correspondance de `failure_reason` | Réactions automatiques du marchand. |
| Stratégie d'idempotence : [idempotence §7.2 ou §7.3](idempotence.md) | Exigé ([idempotence §7.4](idempotence.md)). |
| Rappels : signés, non signés, absents | Délai de connaissance des changements d'état. |
| Pertes connues | Champs ou distinctions que l'opérateur ne fournit pas. |
| Identifiants requis et mode de fourniture | [Authentification §9.1](authentification.md). |
| Identifiant d'opérateur | [Registre](https://github.com/openfspht/openfsp/blob/main/registries/providers.md). |

## 8. Profils observés

D'après la documentation des opérateurs (MonCash REST API, NatCash Merchant Online Integration
2.0). À confirmer contre les environnements de test : les deux documents contiennent des
erreurs.

### 8.1. Correspondance

| | MonCash | NatCash |
|---|---|---|
| Authentification | OAuth 2 `client_credentials`, jeton de 59 s | Identifiant, mot de passe et HMAC-SHA256 à chaque requête |
| Création | `amount`, `orderId` | `amount`, `orderNumber`, `callbackUrl`, `msisdn`, `language` |
| `next_action` | `redirect` | `redirect` |
| Expiration | Date absolue sans fuseau | Durée relative (`expiredAt`, secondes) |
| URL de retour | Fixe, déclarée au portail : relais [API §7.4](api-paiements.md) | Aucune ; le rappel suffit |
| Rappel | Non documenté | Par paiement, signé sur `orderNumber` et `code` |
| Consultation | `RetrieveOrderPayment` | `checkTransaction` |
| Relevé par API | Non | Non |
| Frais rapportés | Non | Non |
| Langue | Non | `fr`, `ht`, `en` |
| Annulation après succès | Non | Dans les 30 minutes (futur `payments.refund`) |
| Transferts | `Transfert`, statut et solde prépayé (futur `transfers`) | Non |

### 8.2. Capacités annonçables

| | MonCash | NatCash |
|---|---|---|
| `payments` | oui | oui |
| `payments.lookup` | oui | oui |
| `webhooks.verify` | non | oui ([cycle de vie §6.3.1](cycle-de-vie.md)) |
| `webhooks.per_payment_url` | non | oui |
| `payments.statement` | non : relevé par import ([relevés §5](releves.md)) | non : relevé par import |
| `payments.fee` | non | non |

Stratégie d'idempotence : recherche par identifiant de commande
([idempotence §7.2](idempotence.md)) pour les deux.

### 8.3. Statuts

| Opérateur | Valeur | OpenFSP |
|---|---|---|
| MonCash | `message: "successful"` | `succeeded` |
| MonCash | `404` sur la consultation | aucune ; `expired` au titre du [cycle de vie §5.3](cycle-de-vie.md) (b) après `expires_at` |
| NatCash | `1` | `succeeded` |
| NatCash | `-1` | `failed`, `unspecified` |
| NatCash | `-3` | aucune : `pending`, nouvelle consultation |
| NatCash | `ERR_TRANSACTION_EXPIRED` | `expired` au titre du [cycle de vie §5.3](cycle-de-vie.md) (a) |
| NatCash | `ERR_DUPLICATE_REQUEST_ID` | aucune : doublon de requête, pas un dénouement ([idempotence §7.2.1](idempotence.md)) |

### 8.4. Pertes connues

- Aucun motif d'échec : `failure_reason` vaut `unspecified`.
- Aucuns frais : `fee` reste absent.
- Montants en décimal ou en chaîne, numéros sans `+`, dates sans fuseau : conversions du
  [modèle de données §3.9, §5.5, §7.5](modele-de-donnees.md).
- Gourdes entières probables : `amount_step` à `100` tant que les centimes ne sont pas
  confirmés ([plafonds §2](plafonds.md)).

## 9. Tests

**9.1.** Sans opérateur, on teste la correspondance (données) et les refus (réponses enregistrées).

**9.2.** La fidélité des réponses enregistrées à l'opérateur réel n'est pas testable ainsi.
