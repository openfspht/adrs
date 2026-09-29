# ADR-0009 : Authentification et identifiants

- Statut : Proposée
- Date : 2026-09-06
- Règles : [spec/authentification.md](../spec/authentification.md)

## Contexte

Deux problèmes distincts. Vers l'extérieur, un client prouve son identité à la passerelle.
Vers l'intérieur, la passerelle détient les identifiants du marchand chez ses opérateurs,
l'actif le plus sensible du déploiement, et deux champs de relais (`provider_detail`,
`failure_detail`) transportent la sortie des opérateurs jusqu'au client. Sans règle commune,
chaque implémentation compare en temps variable, stocke en clair, accepte la clé en paramètre
d'URL, ou distingue clé inconnue et clé révoquée.

## Décision

- Clé d'API porteur `ofsp_<env>_<secret>`, 128 bits d'entropie, dans `Authorization: Bearer`
  uniquement. Préfixe fixe pour les scanners de secrets ; `live` et `test` distingués
  lexicalement et rejetés hors de leur environnement.
- Stockage en condensé SHA-256, comparaison en temps constant, condensé factice sur préfixe
  inconnu. Pas de hachage lent : l'entropie rend la devinette hors ligne sans objet.
- Une seule erreur `unauthenticated` pour tous les échecs ; le détail va dans les journaux.
- Le principal, pas la clé, porte l'idempotence : une rotation ne réinitialise
  aucune protection.
- Quatre portées sans implication ; `forbidden` si la portée manque.
- Plusieurs clés actives par principal, révocation effective en 60 secondes au plus, clé
  révoquée conservée sans secret pour l'audit.
- Identifiants d'opérateur : chargés depuis l'environnement ou un gestionnaire de secrets,
  jamais renvoyés, jamais journalisés, caviardés par comparaison de valeurs dans les relais.

## Conséquences

- Asymétrie assumée : jeton porteur sur TLS du client vers la passerelle, signature sur le
  message de la passerelle vers l'abonné.
- Une compromission se traite en quelques minutes : clés concurrentes, révocation immédiate,
  date de dernière utilisation.
- Les enregistrements d'audit répondent à BRH-126 §3 f) et §3 t) (audit triennal) et à la
  traçabilité de BRH-121 §13.1 ; le caviardage sert la minimisation de BRH-131 §6.10.2.
- Pas de comptes humains ni d'API d'émission de clés : l'administration relève du logiciel de
  déploiement.

## Alternatives écartées

- **OAuth 2.0 client credentials** : aucune seconde partie ; ajoute un aller-retour et un
  rafraîchissement. Possible en amont.
- **JWT autoémis** : la révocation exige une recherche de toute façon ; risques `alg`.
- **Signature HMAC des requêtes** : TLS couvre déjà cette direction.
- **TLS mutuel comme identifiant principal** : lie l'identité à la connexion.
- **Clé unique sans portée** : tout processus peut déplacer de l'argent.
- **Hachage lent** : coût par requête sans gain.
- **Portées par opérateur** : différées, avec les capacités par principal.

## Questions ouvertes

- Filtrer les capacités par principal.
- Expiration par défaut des clés.
- Une interface commune d'émission des clés.
- Tester le caviardage quand l'opérateur transforme l'identifiant avant de le renvoyer.
