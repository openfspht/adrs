# ADR-0014 : Serveur simulé

- Statut : Proposée
- Date : 2026-09-07
- Guide : [spec/serveur-simule.md](../spec/serveur-simule.md) (informatif)

## Contexte

Presque chaque règle de la spécification porte sur une défaillance : expiration au dénouement
inconnu, rappel invérifiable, paiement en attente prolongée, doublon sous coupure réseau,
statut inconnu. Les bacs à sable des opérateurs, d'accès inégal, permettent de tester un
paiement réussi mais aucune de ces défaillances à la demande.

## Décision

- Un serveur qui remplace les opérateurs, avec cinq opérateurs simulés aux capacités inégales ;
  `mock_beta` n'a aucune source automatique de finalité.
- Jamais plus permissif qu'un opérateur réel.
- Vingt et un scénarios de défaillance déclenchés par un préfixe réservé sur `reference`.
- Surface de contrôle séparée pour avancer le temps et résoudre les attentes.
- Déterministe, sans état persistant.
- Impossible à confondre avec la production : identifiants `mock_`, annonce au démarrage,
  environnement `test` obligatoire.

## Conséquences

- La suite de conformité devient exécutable et reproductible en intégration continue.
- Un marchand peut exécuter un parcours de bout en bout sans compte chez un opérateur.
- Le simulateur est l'implémentation de référence des demandes de confirmation et du paiement
  de proximité.
- Un test réussi ne prouve rien sur le comportement d'un opérateur réel.

## Alternatives écartées

- **Scénario choisi par le montant** : interdit de tester les montants ; un montant magique en
  production débite un vrai client.
- **Champ de requête dédié au test** : un champ à ignorer en production finit par ne plus l'être.
- **Clé réservée dans `metadata`** : `metadata` appartient au marchand.
- **Défaillances aléatoires** : tests instables, donc relancés plutôt que lus.
- **Enregistrement et rejeu de trafic réel** : les défaillances ne peuvent pas être provoquées
  pour être enregistrées.
- **Tests contre les bacs à sable** : non déterministes, sans défaillance à la demande.

## Questions ouvertes

- Opérateurs simulés avec des API distinctes calquées sur les opérateurs réels, ou une API
  commune.
- Réinjecter dans les scénarios les comportements observés chez de vrais opérateurs.
- Un scénario `LIES` rapportant une transition hors d'un état terminal.
- Retour en arrière de la surface de contrôle.
