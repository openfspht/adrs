# ADR-0015 : Conformité

- Statut : Proposée
- Date : 2026-09-07
- Règles : [spec/conformite.md](../spec/conformite.md)

## Contexte

La promesse centrale, une opération absente est déclarée absente et jamais émulée, n'est pas
inspectable : une passerelle qui répond depuis son état périmé ressemble à une passerelle qui a
interrogé l'opérateur. Seul un test peut la vérifier. Par ailleurs, BRH-121 §5 et BRH-126 §3 t)
imposent deux audits triennaux sans prescrire d'étalon.

## Décision

- Conformité = triplet cible (client, passerelle, opérateur natif), niveau, version du
  protocole.
- Niveau Core obligatoire, puis un profil par capacité annoncée ; pas de réussite partielle,
  pas de classement.
- Les tests de refus comptent le plus : Core s'obtient aussi en refusant correctement.
- Suite exécutable par quiconque, hors ligne, sans modifier l'implémentation ; le serveur
  simulé joue les opérateurs.
- Rapport lisible par machine, daté, reproductible, qui porte toujours ses limites.
- La suite produit des preuves ; les revendications relèvent de l'ADR-0016.

## Conséquences

- Une implémentation qui émule une capacité échoue à Core.
- Un rapport fournit à l'auditeur d'un FSP qui implémente OpenFSP un étalon pour la part
  applicative de l'audit d'interopérabilité (BRH-121 §5), et une pièce pour l'audit de sécurité
  (BRH-126 §3 t)).
- La suite versionnée tient lieu de registre de documentation pour la surface de conformité
  (BRH-126 §3 p)).
- Un résultat obtenu contre le simulateur ne vaut pas preuve contre un opérateur réel.
- La vérification effective des signatures entrantes reste hors de portée des tests.

## Alternatives écartées

- **Certification par le projet, payante** : fait du projet un gardien sur un marché où son
  porteur vend.
- **Niveaux bronze, argent, or** : mesurent l'opérateur, incitent à annoncer à tort.
- **Score en pourcentage** : ne dit pas si la part manquante est un double débit.
- **Tests contre les bacs à sable des opérateurs** : aucun ne provoque de défaillance à la
  demande.
- **Instrumentation de l'implémentation** : ce n'est plus l'implémentation déployée.
- **Marques dans la même ADR** : un résultat est un fait, une permission est une politique.

## Questions ouvertes

- Tester la vérification des signatures (signature invalide envoyée par le simulateur).
- Tester un client sans sa coopération.
- Barre suffisante pour un opérateur natif.
- Tests de correspondance ISO 20022 si un exportateur existe.
- Format de publication de la configuration d'un rapport.
