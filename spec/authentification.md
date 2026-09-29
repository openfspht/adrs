# Authentification

Décision : [ADR-0009](../text/0009-authentication-and-credentials.md).

## 1. Schéma

**1.1.** Un client s'authentifie par une clé d'API porteur. Tous les points d'accès sont
authentifiés, sauf le descripteur de service ([capacités §3.1](capacites.md)) et l'ensemble de
clés de webhook ([webhooks §6.1](webhooks.md)).

**1.2.** La passerelle NE DOIT PAS offrir de mode non authentifié pour un autre point d'accès,
y compris en développement.

**1.3.** Un déploiement PEUT exiger en plus un TLS mutuel, une liste d'adresses ou un serveur
d'autorisation en amont. Ces mesures NE DOIVENT PAS remplacer le §3.

## 2. Format de clé

**2.1.** Forme `ofsp_<env>_<secret>`, où `<env>` vaut `live` ou `test` et `<secret>` compte au
moins 32 caractères parmi `A-Za-z0-9` :

```
ofsp_live_7Kq2NfPzR4wYb9LdHt3XvA6mSjE0uCgB
```

**2.2.** `<secret>` DOIT venir d'un générateur cryptographique et porter au moins 128 bits
d'entropie. Il NE DOIT PAS être dérivé d'une donnée prévisible.

**2.3.** Une passerelle est configurée pour un seul environnement et DOIT rejeter une clé d'un
autre environnement avec `unauthenticated`.

**2.4.** Une clé NE DOIT encoder ni principal, ni portée, ni expiration : elle est opaque.

**2.5.** Une passerelle PEUT allonger `<secret>` ou y ajouter une somme de contrôle, dans le
respect du §2.1.

## 3. Présentation

**3.1.** Un client DOIT envoyer la clé dans `Authorization`, schéma `Bearer` (RFC 9110) :

```
Authorization: Bearer ofsp_live_7Kq2NfPzR4wYb9LdHt3XvA6mSjE0uCgB
```

**3.2.** La passerelle NE DOIT PAS accepter une clé dans un paramètre de requête, un corps, un
cookie ou un autre en-tête.

**3.3.** Absence d'`Authorization`, en-tête illisible ou schéma autre que `Bearer` : la
passerelle DOIT répondre `unauthenticated` avec `WWW-Authenticate: Bearer`.

**3.4.** Le nom du schéma est insensible à la casse ; la clé y est sensible.

**3.5.** La passerelle DOIT rejeter avec `unauthenticated` une requête portant plus d'un
identifiant.

## 4. Stockage et comparaison

**4.1.** La passerelle NE DOIT PAS stocker une clé sous une forme réversible ; elle stocke un
condensé.

**4.2.** Le condensé DOIT être SHA-256 ou plus fort, calculé sur la clé entière.

**4.3.** Un hachage lent de mot de passe (Argon2id, scrypt, bcrypt) NE DEVRAIT PAS être
utilisé.

**4.4.** La passerelle PEUT stocker en clair un préfixe de recherche, les 12 premiers
caractères de `<secret>`, et l'indexer.

**4.5.** Le condensé présenté DOIT être comparé au condensé stocké en temps constant.

**4.6.** Une clé inconnue et une clé révoquée DEVRAIENT prendre un temps de traitement
indiscernable. Si le préfixe ne correspond à aucun enregistrement, la passerelle DOIT tout de
même calculer un condensé et le comparer en temps constant à une valeur factice. Aucun
traitement conditionnel, comme journaliser un seul des deux cas, NE DOIT creuser l'écart.

**4.7.** Identifiant absent, mal formé, inconnu, révoqué, expiré ou d'un autre environnement :
tous produisent `unauthenticated` avec le même `title` et aucun `detail` distinctif.

**4.8.** La passerelle NE DOIT PAS journaliser une clé présentée au-delà de son préfixe de
recherche, à aucun niveau. Un échec est journalisé avec le préfixe et le `request_id`.

## 5. Principal

**5.1.** Le principal est l'identité à laquelle se résout une authentification réussie. C'est le
*P* de l'[idempotence §2.3](idempotence.md).

**5.2.** Chaque clé appartient à un seul principal ; un principal PEUT détenir plusieurs clés.

**5.3.** Deux clés d'un même principal sont le même principal : mêmes enregistrements
d'idempotence, mêmes ressources. La passerelle NE DOIT PAS cloisonner par clé ce que la
spécification cloisonne par principal.

**5.4.** Un principal a un identifiant opaque et stable ([modèle de données §6.1](modele-de-donnees.md)),
présent dans les journaux et l'audit, jamais exposé par l'API.

**5.5.** Tous les principaux d'une passerelle voient les mêmes ressources. Les portées
restreignent les actions, pas la visibilité.

## 6. Portées

**6.1.** Une clé porte un ensemble de portées.

**6.2.** Registre :

| Portée | Permet |
|---|---|
| `capabilities:read` | Découverte de capacités ([capacités §3.2](capacites.md)). |
| `payments:read` | Lire un paiement, rechercher par référence ([API §5.2](api-paiements.md)). |
| `payments:write` | Créer et synchroniser un paiement ([API §5.1, §5.3](api-paiements.md)). |
| `statements:read` | Lire les relevés et leurs lignes ([relevés §6](releves.md)). |

**6.3.** Aucune portée n'en implique une autre.

**6.4.** Sans la portée requise, la passerelle DOIT répondre `forbidden`, jamais
`unauthenticated` ni `not-found`.

**6.5.** La synchronisation exige `payments:write`.

**6.6.** Ajouter une portée requiert une ADR, en même temps que l'opération qu'elle régit.

**6.7.** Une clé sans portée ne permet rien ; la passerelle NE DOIT PAS la traiter comme non
restreinte.

**6.8.** L'outillage d'émission DEVRAIT proposer le moindre privilège par défaut.

## 7. Rotation, révocation, expiration

**7.1.** La passerelle DOIT accepter plusieurs clés valides simultanément pour un principal.

**7.2.** Rotation : émettre une seconde clé, la déployer, vérifier son usage, révoquer la
première. L'émission d'une clé NE DOIT PAS invalider les autres clés du principal.

**7.3.** La révocation est immédiate. La passerelle NE DOIT PAS servir une clé révoquée ni
conserver en cache une décision d'authentification plus de 60 secondes après révocation ; un
cache DOIT être invalidé à la révocation.

**7.4.** Une clé révoquée NE DOIT PAS être rétablie ni son secret réémis.

**7.5.** L'enregistrement d'une clé révoquée DOIT être conservé, sans secret, pour l'audit.

**7.6.** Une clé PEUT expirer. Une clé expirée DOIT être rejetée avec `unauthenticated` ;
l'exploitant DEVRAIT être prévenu avant l'expiration.

**7.7.** Le secret DOIT être affiché une seule fois, à l'émission, et ne plus jamais pouvoir
l'être.

**7.8.** La passerelle DEVRAIT enregistrer et afficher la date de dernière utilisation de chaque
clé.

## 8. Articulation

**8.1.** L'enregistrement d'idempotence survit à la rotation d'une clé d'API et n'est jamais
visible d'un autre principal.

**8.2.** La limitation de débit s'applique par principal, pas par clé.

**8.3.** `unauthenticated` et `forbidden` sont définis dans les [erreurs §9.2](erreurs.md).

**8.4.** Le point d'accès des capacités exige `capabilities:read`.

**8.5.** La passerelle NE DOIT PAS envoyer de clé d'API à un point d'accès de webhook, et un
abonné NE DOIT PAS authentifier une livraison autrement que par sa signature
([webhooks §5](webhooks.md)).

## 9. Identifiants d'opérateur

**9.1.** La passerelle DOIT pouvoir charger les identifiants d'opérateur depuis des variables
d'environnement ou un gestionnaire de secrets. Elle NE DOIT PAS exiger un fichier de
configuration, et sa documentation NE DOIT PAS présenter le fichier comme méthode principale.

**9.2.** La passerelle DEVRAIT recharger les identifiants d'opérateur sans redémarrage.

**9.3.** La passerelle NE DOIT renvoyer aucun identifiant d'opérateur, même partiel, par aucun
point d'accès. Un contrôle de santé PEUT indiquer qu'un opérateur est joignable.

**9.4.** La passerelle NE DOIT écrire aucun identifiant d'opérateur dans un journal, une trace,
une métrique, un rapport d'erreur ou un vidage mémoire. `Authorization` et tout champ portant un
identifiant DOIVENT être caviardés avant la construction de la ligne de journal.

**9.5.** La passerelle DOIT caviarder de `provider_detail` et `failure_detail` toute valeur
qu'elle détient comme identifiant d'opérateur, par comparaison avec les valeurs détenues et non
par motifs.

**9.6.** Une valeur caviardée est remplacée par la chaîne `[redacted]`, pas supprimée.

## 10. Audit

**10.1.** Pour chaque requête authentifiée, la passerelle DOIT enregistrer le principal, le
préfixe de recherche, l'opération, le `request_id` et le résultat.

**10.2.** Les échecs d'authentification DOIVENT être enregistrés avec les mêmes champs, sans
principal.

**10.3.** Toute émission et révocation de clé DOIT être enregistrée, avec l'heure et les portées.

**10.4.** Ces enregistrements NE DOIVENT contenir ni secret de clé ni identifiant d'opérateur.

## 11. Conformité

**11.1.** Passerelle conforme : présentation du §3, stockage et comparaison du §4, principal du
§5, portées du §6, rotation et révocation du §7, §9 pour chaque opérateur.

**11.2.** La suite teste le §4.7 avec une clé inconnue, une clé révoquée et une clé d'un autre
environnement (trois réponses indiscernables), et le §9.5 avec un opérateur simulé qui renvoie
les identifiants reçus (`[redacted]` attendu dans `provider_detail`).

**11.3.** L'authentification n'est pas une capacité et n'est pas annoncée.

## 12. Sécurité

**12.1.** La passerelle DEVRAIT limiter le débit des authentifications échouées par source.
