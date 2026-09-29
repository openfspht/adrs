# Modèle de données

Décision : [ADR-0002](../text/0002-core-data-model.md).

## 1. Types

| Type | Forme JSON | Exemple |
|---|---|---|
| `Money` | objet | `{"amount": 125000, "currency": "HTG"}` |
| `Currency` | chaîne, valeur unique `HTG` | `"HTG"` |
| `PhoneNumber` | chaîne, E.164 | `"+50934567890"` |
| `ResourceId` | chaîne opaque | `"pay_01J9ZK3QF8XN2M7VYB4C6D8E0G"` |
| `Reference` | chaîne choisie par le marchand | `"INV-2026-00184"` |
| `ProviderReference` | chaîne opaque | `"MC-8837291"` |
| `Timestamp` | chaîne, RFC 3339 UTC | `"2026-08-17T14:32:07.412Z"` |
| `Date` | chaîne, `full-date` RFC 3339 | `"2026-09-28"` ([relevés §1](releves.md)) |
| `Fee` | objet | `{"amount": {"amount": 1250, "currency": "HTG"}, "bearer": "merchant"}` |
| `Metadata` | objet de chaînes | `{"order_id": "184"}` |

## 2. Conventions JSON

**2.1.** Les corps de requête et de réponse sont en JSON (RFC 8259), encodés en UTF-8.

**2.2.** Les noms de champs sont en `lower_snake_case` et ne changent pas à l'intérieur d'une
version majeure.

**2.3.** Un client DOIT ignorer un champ de réponse inconnu.

**2.4.** Un serveur DOIT rejeter en `400` un corps de requête contenant un champ inconnu, en
nommant le champ.

**2.5.** Pour un champ FACULTATIF, l'absence et `null` sont équivalents. Les implémentations
DEVRAIENT omettre le champ plutôt qu'envoyer `null`. Un champ OBLIGATOIRE NE DOIT PAS valoir
`null`.

**2.6.** Les chaînes DEVRAIENT être normalisées en NFC avant stockage et comparaison. Toute
limite de longueur compte des points de code Unicode.

**2.7.** Les booléens et les nombres sont des types JSON natifs, jamais des chaînes.

## 3. `Money`

**3.1.** Un objet à deux champs OBLIGATOIRES, `amount` et `currency`.

**3.2.** `amount` est un entier en centimes de gourde : `125000` vaut 1 250,00 HTG.

**3.3.** `amount` DOIT être un nombre JSON sans partie fractionnaire ni exposant.

**3.4.** `amount` DOIT être compris entre -(2⁵³ - 1) et 2⁵³ - 1 inclus. Les implémentations
DOIVENT valider cet intervalle explicitement.

**3.5.** Une implémentation NE DOIT PAS représenter un montant par une valeur à virgule
flottante, même transitoirement.

**3.6.** Sauf disposition contraire d'une autre spécification, un montant de requête
DOIT être strictement positif. Un montant nul DOIT être rejeté.

**3.7.** Deux `Money` sont égaux si leurs `amount` sont égaux.

**3.8.** Aucun arrondi.

**3.9.** Un montant reçu de l'opérateur DOIT être converti depuis sa forme décimale textuelle,
sans passer par un flottant. Un montant qui n'est pas exact au centime rend la réponse
inexploitable (`provider-error`).

## 4. Devise

**4.1.** La seule devise est la gourde : `currency` DOIT valoir `"HTG"` (ISO 4217, exposant
2). Toute autre valeur DOIT être rejetée avec `invalid-field`.

**4.2.** Ajouter une devise requiert une ADR.

## 5. Numéro de téléphone

**5.1.** Format E.164, `^\+[1-9]\d{1,14}$`.

**5.2.** Valide : `"+50934567890"`. Invalides : `"34567890"`, `"+509 34 56 78 90"`,
`"+509-3456-7890"`, `"050934567890"`.

**5.3.** Une passerelle NE DOIT PAS déduire un indicatif pays d'un numéro national et DOIT
rejeter toute valeur non conforme au §5.1. Un SDK PEUT convertir une saisie locale en E.164.

**5.4.** Un numéro syntaxiquement valide NE DOIT PAS être traité comme vérifié.

**5.5.** Un numéro reçu de l'opérateur DOIT être converti en E.164 selon le format documenté de
cet opérateur (`50937007294` devient `"+50937007294"`). Un numéro dont la conversion n'est pas
certaine est omis.

## 6. Identifiants

### 6.1. `ResourceId`

**6.1.1.** 1 à 64 caractères parmi `A-Za-z0-9_-`, attribué par la passerelle à la création,
immuable.

**6.1.2.** Opaque : un client NE DOIT PAS l'analyser, en déduire un ordre, ni en construire
un.

**6.1.3.** Les implémentations DEVRAIENT le générer comme un UUID version 7 (RFC 9562). Tout
générateur conforme aux §6.1.1 et §6.1.4 est admis.

**6.1.4.** Il NE DOIT PAS être devinable. Entiers séquentiels et compteurs sont interdits.

**6.1.5.** Un préfixe de type suivi d'un souligné (`pay_`, `rfd_`) est RECOMMANDÉ. Il fait
partie de la valeur opaque.

### 6.2. `Reference`

**6.2.1.** 1 à 128 caractères parmi `A-Za-z0-9._:/-`, fournie par le marchand à la création,
immuable.

**6.2.2.** Une `Reference` DOIT être unique parmi les ressources de même type d'une même
passerelle, quel que soit le principal qui l'a créée. La passerelle DOIT rejeter une création
dont la référence est déjà utilisée.

**6.2.3.** La `Reference` est la clé de corrélation primaire : elle permet de retrouver un
paiement dont la création n'a pas reçu de réponse.

**6.2.4.** La `Reference` n'est pas transmise à l'opérateur : il reçoit l'identifiant de commande
qui en est dérivé ([idempotence §7.2](idempotence.md)). Elle NE DOIT PAS contenir de données
personnelles ni d'identifiant secret.

**6.2.5.** L'articulation avec `Idempotency-Key` est dans [idempotence §6](idempotence.md).

### 6.3. `ProviderReference`

**6.3.1.** Chaîne opaque d'au plus 255 caractères, attribuée par l'opérateur.

**6.3.2.** FACULTATIVE : absente avant la réponse de l'opérateur, ou définitivement s'il n'en
a jamais fourni.

**6.3.3.** Un client NE DOIT PAS l'utiliser comme clé de corrélation primaire ni la supposer
unique entre opérateurs.

### 6.4. `IdempotencyKey`

**6.4.1.** 1 à 255 caractères parmi `A-Za-z0-9_-`, portée par l'en-tête `Idempotency-Key`.
Sémantique : [idempotence](idempotence.md).

## 7. Horodatage

**7.1.** Format `date-time` RFC 3339, en UTC, avec un `Z` majuscule :
`"2026-08-17T14:32:07.412Z"`.

**7.2.** Un décalage numérique, un `z` minuscule ou une date sans heure DOIVENT être rejetés.

**7.3.** La seconde est OBLIGATOIRE ; les fractions, jusqu'à la milliseconde, sont
FACULTATIVES. Un client DOIT les accepter ; un serveur NE DOIT PAS les exiger.

**7.4.** Les horodatages NE DOIVENT PAS servir d'ordre total entre événements. Un client NE
DOIT PAS en dériver un séquencement.

**7.5.** Un horodatage reçu de l'opérateur sans décalage est interprété dans le fuseau
`America/Port-au-Prince`. Une heure ambiguë (retour à l'heure d'hiver) prend l'instant le plus
tardif. Une durée relative (`expiredAt: 300`) court à partir de la réception de la réponse.

## 8. `Fee`

**8.1.** Frais facturés par l'opérateur pour un paiement.

| Champ | Type | Présence | Notes |
|---|---|---|---|
| `amount` | `Money` | OBLIGATOIRE | En HTG. |
| `bearer` | chaîne | OBLIGATOIRE | `merchant` ou `payer`. |

**8.2.** Un `Fee` absent signifie « non connu » ; des frais nuls sont un montant nul. Un
client NE DOIT PAS afficher des frais absents comme nuls ni les dériver par soustraction.

**8.3.** `bearer` rapporte qui a supporté les frais selon l'opérateur. La passerelle NE DOIT
PAS laisser un client le fixer.

**8.4.** La passerelle NE DOIT PAS retarder une transition terminale dans l'attente des frais,
ni les deviner.

**8.5.** Une passerelle dont l'opérateur ne rapporte jamais les frais NE DOIT PAS annoncer
`payments.fee`.

## 9. `Metadata`

**9.1.** Objet FACULTATIF de chaînes vers chaînes, fourni par le marchand, renvoyé inchangé
partout où la ressource est renvoyée.

**9.2.** Au plus 20 clés ; clés de 1 à 40 caractères parmi `A-Za-z0-9_.-` ; valeurs d'au plus
500 caractères. Toute valeur autre qu'une chaîne est invalide.

**9.3.** La passerelle DOIT stocker et renvoyer les métadonnées sans altération, et NE DOIT
PAS les interpréter.

**9.4.** La passerelle NE DOIT PAS transmettre les métadonnées à l'opérateur, sauf exigence
explicite d'une spécification pour une opération nommée.

**9.5.** Les marchands NE DEVRAIENT PAS y placer de données personnelles et NE DOIVENT PAS y
placer d'identifiants secrets.

## 10. Sécurité

**10.1.** Les numéros de téléphone NE DOIVENT PAS apparaître dans les journaux sous le niveau
d'audit de sécurité, dans les messages d'erreur ni dans la télémétrie.

**10.2.** La passerelle DEVRAIT documenter que les métadonnées ne sont pas chiffrées au repos,
sauf si l'exploitant les chiffre.
