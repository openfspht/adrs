# ADR-0009 : Authentification et identifiants

- Date : 2026-09-06
- Règles : [spec/authentification.md](../spec/authentification.md)

## Contexte

Je distingue deux surfaces. Vers l'extérieur, un client prouve son identité à la passerelle. Vers
l'intérieur, la passerelle détient les secrets d'opérateur du marchand, et deux champs de relais
(`provider_detail`, `failure_detail`) transportent la sortie des opérateurs jusqu'au client.
Sans règle commune, une implémentation peut comparer en temps variable, stocker en clair,
accepter la clé en paramètre d'URL, ou distinguer clé inconnue et clé révoquée.

## Décision

Je propose :

- Clé d'API porteur `ofsp_<env>_<secret>`, 128 bits d'entropie, dans `Authorization: Bearer`
  uniquement. Préfixe fixe pour les outils de détection de secrets ; `live` et `test` distingués
  lexicalement et rejetés hors de leur environnement.
- Stockage en condensé SHA-256, comparaison en temps constant, condensé factice sur préfixe
  inconnu. Pas de hachage lent : 128 bits d'entropie rendent une recherche exhaustive hors ligne
  impraticable.
- Une seule erreur `unauthenticated` pour tous les échecs ; le détail va dans les journaux.
- Les enregistrements d'idempotence sont rattachés au principal ; une rotation de clé les
  conserve.
- Quatre portées sans implication ; `forbidden` si la portée manque.
- Plusieurs clés actives par principal, révocation effective en 60 secondes au plus, clé
  révoquée conservée sans secret pour l'audit.
- Secrets d'opérateur : chargés depuis l'environnement ou un gestionnaire de secrets,
  jamais renvoyés, jamais journalisés, caviardés par comparaison de valeurs dans les relais.

## Conséquences

- Asymétrie : jeton porteur sur TLS du client vers la passerelle, signature sur le
  message de la passerelle vers l'abonné.
- Neutralisation d'une clé compromise : clés concurrentes, révocation effective en
  60 secondes au plus (authentification 7.3), date de dernière utilisation.
- Les clés à portées répondent à la gestion sécurisée de l'accès de BRH-126 3 f) ; les
  enregistrements d'audit, à BRH-126 3 t) (audit triennal) et à la traçabilité de
  BRH-121 13.1 ; le caviardage sert la minimisation de BRH-131 6.10.2.
- Pas de comptes humains ni d'API d'émission de clés : l'administration relève du logiciel de
  déploiement.

## Ce que je n'ai pas retenu

- **OAuth 2.0 client credentials** : aucun serveur d'autorisation tiers requis ; ajoute un
  aller-retour et un rafraîchissement. Possible en amont.
- **JWT autoémis** : la révocation exige une recherche de toute façon ; expose à la
  confusion d'algorithme (`alg`).
- **Signature HMAC des requêtes** : TLS couvre déjà cette direction.
- **TLS mutuel comme identifiant principal** : lie l'identité à la connexion.
- **Clé unique sans portée** : tout processus détenteur de la clé peut créer des
  paiements.
- **Hachage lent** : coût de calcul à chaque requête, sans gain de sécurité à 128 bits
  d'entropie.
- **Portées par opérateur** : différées, avec les capacités par principal.

## Questions ouvertes

- Filtrer les capacités par principal.
- Expiration par défaut des clés.
- Une interface commune d'émission des clés.
- Tester le caviardage quand l'opérateur transforme le secret d'opérateur avant de le
  renvoyer.
