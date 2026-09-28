# Découverte de capacités

Décision : [ADR-0007](../text/0007-capability-discovery.md).

## 1. Capacité

**1.1.** Une capacité est une fonctionnalité nommée qu'une passerelle prend en charge ou non,
pour un opérateur donné.

**1.2.** Les capacités sont rapportées par opérateur, jamais pour la passerelle entière.

**1.3.** Une passerelle DOIT n'annoncer une capacité que si l'opérateur prend réellement en
charge l'opération. Elle NE DOIT PAS annoncer une capacité obtenue par émulation,
approximation ou composition d'autres opérations.

**1.4.** La capacité `payments` ([API §2](api-paiements.md)) est présente pour tout opérateur ;
un client NE DOIT PAS être tenu d'interroger la découverte avant de l'utiliser.

## 2. Noms et registre

**2.1.** Un nom de capacité correspond à `^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$` : domaine,
puis opération.

**2.2.** Registre. Un nom *enregistré* n'a pas encore de spécification et NE DOIT PAS être
annoncé.

| Nom | Statut | Sens |
|---|---|---|
| `payments` | spécifié, obligatoire | Créer, lire, synchroniser un paiement ([API](api-paiements.md)). |
| `payments.lookup` | spécifié | Consultation autoritative de l'état chez l'opérateur (§5). |
| `payments.statement` | spécifié | Relevé des transactions par canal authentifié ([cycle de vie §6.7](cycle-de-vie.md)). |
| `payments.fee` | spécifié | L'opérateur rapporte les frais ([modèle de données §8](modele-de-donnees.md)). |
| `payments.refund` | enregistré | Remboursement d'un paiement capturé. |
| `payments.capture` | enregistré | Autorisation et capture séparées. |
| `payments.cancel` | enregistré | Annulation avant achèvement. |
| `payments.proximity_cpm` | enregistré | Résolution native de jetons présentés par le payeur ([proximité](proximite.md)). |
| `confirmation_requests` | enregistré | Confirmation minutée par le payeur ([demandes de confirmation](demandes-de-confirmation.md)). |
| `confirmation_requests.cancel` | enregistré | Retrait d'une demande avant réponse du payeur. |
| `transfers` | enregistré | Envoi de fonds à un bénéficiaire. |
| `webhooks.emit` | enregistré | Événements signés vers le client ([webhooks](webhooks.md)). |
| `webhooks.verify` | spécifié | Rappels signés par l'opérateur ([cycle de vie §6.5](cycle-de-vie.md) a). |
| `webhooks.per_payment_url` | spécifié | URL de rappel propre à chaque paiement ([cycle de vie §6.6](cycle-de-vie.md)). |

**2.3.** Ajouter un nom requiert une ADR. Un ajout n'est pas une rupture (§4.3).

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
        "expiry_guaranteed": true
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
| `payments` | objet | OBLIGATOIRE | §3.2.2. |

**3.2.2.** Objet `payments` :

| Champ | Type | Sens |
|---|---|---|
| `next_actions` | tableau de chaînes | Types de `next_action` produits ([API §4.2](api-paiements.md)). |
| `payer_required` | booléen | `payer` exigé à la création. |
| `return_url_required` | booléen | `return_url` exigée à la création. |
| `expiry_guaranteed` | booléen | Garantie du [cycle de vie §5.3](cycle-de-vie.md) c. |

**3.2.3.** En cas de doute, `expiry_guaranteed` DOIT valoir `false`.

**3.2.4.** La réponse DEVRAIT porter `Cache-Control` avec un `max-age` d'une heure au plus.

## 4. Obligations

**4.1.** Un client NE DOIT PAS invoquer une opération dont la capacité n'est pas annoncée pour
l'opérateur choisi.

**4.2.** Un client DOIT traiter `capability-not-supported` à tout moment, et DEVRAIT alors
relire les capacités.

**4.3.** Un client DOIT ignorer un nom de capacité inconnu.

**4.4.** La passerelle DOIT rejeter avec `capability-not-supported` toute opération dont elle
n'annonce pas la capacité, même si elle pourrait l'exécuter.

**4.5.** La passerelle DOIT tenir l'ensemble annoncé à jour et NE DOIT PAS annoncer une
capacité suspendue par l'opérateur.

## 5. `payments.lookup`

**5.1.** `payments.lookup` annonce une consultation autoritative de l'état courant chez
l'opérateur.

**5.2.** Si elle est annoncée, la synchronisation ([API §5.3](api-paiements.md)) lit l'état
chez l'opérateur.

**5.3.** Sinon, la synchronisation DOIT renvoyer `capability-not-supported` et NE DOIT PAS
renvoyer l'état stocké comme s'il avait été relu.

**5.3.1.** Exception : un paiement terminal est renvoyé inchangé en `200`
([API §5.3.3](api-paiements.md)).

**5.4.** Sans `payments.lookup`, le rapprochement s'appuie sur les autres sources du
[cycle de vie §6.5](cycle-de-vie.md).

## 6. Conformité

**6.1.** Une passerelle conforme DOIT servir les deux points d'accès du §3.

**6.2.** Une passerelle qui annonce un nom *enregistré* n'est pas conforme.

## 7. Sécurité

**7.1.** Le descripteur public DEVRAIT être limité en débit.

**7.2.** Une capacité annoncée ne vaut pas autorisation : la passerelle DOIT contrôler
l'autorisation indépendamment.
