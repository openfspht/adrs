# ADR-0015 : Conformité

- Date : 2026-09-07
- Règles : [spec/conformite.md](../spec/conformite.md)

## Contexte

Le principe de non-émulation (architecture, Principes de conception) n'est vérifiable que par
un test en boîte noire : à l'inspection, une passerelle qui répond depuis son état périmé
ressemble à une passerelle qui a interrogé l'opérateur. BRH-121 5 et BRH-126 3 t) imposent
deux audits triennaux sans prescrire d'étalon.

## Décision

Je propose :

- Conformité = triplet cible (client, passerelle, opérateur natif), niveau, version du
  protocole.
- Niveau Core obligatoire, puis un profil par capacité annoncée ; pas de réussite partielle,
  pas de classement.
- Core inclut les tests de refus de conformité 5.4, hors ceux du 5.4.1 : une implémentation
  n'obtient Core que si chacun réussit.
- Suite exécutable par quiconque, hors ligne, sans modifier l'implémentation ; le serveur
  simulé joue les opérateurs.
- Rapport lisible par machine, daté, reproductible, qui porte toujours ses limites.
- La suite produit des preuves ; les revendications relèvent de la gouvernance (8), qui reprend
  l'ADR-0016.
- Serveur simulé (reprend l'ADR-0014) : trois opérateurs aux capacités inégales, dont un sans
  source automatique d'état terminal ; jamais plus permissif qu'un opérateur réel ; dix-sept
  scénarios, dont seize de défaillance, déclarés sur une surface de contrôle ; déterministe et
  impossible à confondre avec la production (identifiants `mock_`, environnement `test`).
- Le serveur simulé expose le journal des requêtes reçues, pour vérifier sans instrumenter la
  passerelle.

## Conséquences

- Émuler une capacité est une non-conformité à Core ; la suite ne la détecte pas toujours
  ([conformité 5.6](../spec/conformite.md)).
- Un rapport fournit à l'auditeur d'un FSP qui implémente OpenFSP un étalon pour la part
  applicative de l'audit d'interopérabilité (BRH-121 5), et une pièce pour l'audit de sécurité
  (BRH-126 3 t)).
- La suite versionnée tient lieu de registre de documentation pour la surface de conformité
  (BRH-126 3 p)).
- Un résultat contre le simulateur ne vaut pas preuve contre un opérateur réel.
- La vérification effective des signatures entrantes reste hors de portée des tests.

## Ce que je n'ai pas retenu

- **Certification par le projet, payante** : placerait le projet en position de contrôle
  d'accès à un marché sur lequel j'exerce une activité commerciale.
- **Niveaux bronze, argent, or** : mesurent l'opérateur, incitent à annoncer à tort.
- **Score en pourcentage** : n'indique pas quelles exigences échouent, en
  particulier celles dont l'échec permet un double débit.
- **Tests contre les bacs à sable des opérateurs** : aucun ne provoque de défaillance à la
  demande.
- **Scénario choisi par le montant** : interdit de tester les montants ; un montant déclencheur de
  scénario, envoyé en production, débite un payeur réel.
- **Défaillances aléatoires** : résultats non reproductibles (conformité 1.4).
- **Instrumentation de l'implémentation** : teste autre chose que l'implémentation déployée.
- **Marques dans la même ADR** : le rapport relève de la suite, l'usage des
  marques relève de la gouvernance ; les deux évoluent selon des processus distincts.

## Questions ouvertes

- Tester la vérification des signatures (signature invalide envoyée par le simulateur).
- Tester un client sans sa coopération.
- Barre suffisante pour un opérateur natif.
- Format de publication de la configuration d'un rapport.
- Opérateurs simulés avec des API calquées sur les opérateurs réels, ou une API commune.
