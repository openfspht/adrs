# Revendications de conformité et usage du nom

Processus. Décision : [ADR-0016](../text/0016-conformance-marks-and-naming.md).

## 1. Portée

**1.1.** Ces règles lient le projet et quiconque utilise le nom OpenFSP. Elles n'imposent rien au
comportement d'une implémentation.

**1.2.** La description factuelle reste libre : « construit sur OpenFSP », « implémente OpenFSP
0.1.0 », « parle le protocole OpenFSP ». Ce ne sont pas des revendications de conformité.

**1.3.** Ces règles régissent la revendication de conformité, qui affirme un résultat de test.

## 2. Fondement

**2.1.** Une revendication repose sur un rapport de réussite de la suite
([conformité §7](conformite.md)).

**2.2.** Le rapport DOIT être publié avec la configuration permettant de le reproduire ; sinon
la revendication n'est pas recevable.

**2.3.** Le revendiquant exécute la suite lui-même : ni soumission, ni file d'attente, ni
approbation.

**2.4.** Le rapport DOIT correspondre à la version revendiquée de l'implémentation.

**2.5.** Aucun palier provisoire ou autodéclaré.

## 3. Formes permises

**3.1.** Forme : `OpenFSP conformant <target>, <level>, protocol <version>`, suivie
éventuellement des profils :

```
OpenFSP conformant gateway, Core, protocol 0.1.0
OpenFSP conformant gateway, Core, protocol 0.1.0, profiles: payments.lookup, webhooks.emit
OpenFSP conformant client, Core, protocol 0.1.0
```

**3.2.** Le rapport DOIT être accessible depuis la revendication (citation, lien, ou indication
de l'endroit où il est publié).

**3.3.** Le mot est **conformant**, jamais certified, approved, validated, endorsed, accredited
ni compliant.

**3.4.** Une forme abrégée est admise si elle reste exacte et renvoie à la forme complète :
« OpenFSP conformant (Core, 0.1.0) », jamais « OpenFSP conformant » seul.

## 4. Interdictions

**4.1.** Aucune revendication NE DOIT laisser entendre qu'une partie a certifié, approuvé,
audité, testé ou recommandé l'implémentation.

**4.2.** Aucune revendication NE DOIT omettre la version du protocole.

**4.3.** Aucune revendication NE DOIT affirmer un profil non réussi ni une capacité non annoncée.

**4.4.** Aucune revendication NE DOIT présenter la conformité comme une assurance de sécurité.

**4.5.** Aucune revendication NE DOIT s'étendre au-delà de la configuration testée.

**4.6.** Le nom OpenFSP NE DOIT PAS entrer dans un nom de produit, d'entreprise ou de domaine
d'une façon qui le fait passer pour un produit du projet.

**4.7.** Un opérateur NE DOIT PAS revendiquer la conformité du seul fait qu'un adaptateur existe
pour lui.

## 5. Revendication fausse

**5.1.** Le seul instrument du projet est la publication : l'éditeur PEUT signaler publiquement
une revendication fausse, avec les preuves.

**5.2.** Il notifie d'abord le revendiquant et laisse un délai raisonnable pour corriger.

**5.3.** Une revendication corrigée n'est pas publiée.

**5.4.** Les recours de droit des marques restent ceux du dépositaire
([GOVERNANCE §8](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#8-nom-et-marques-de-conformité)).

**5.5.** Il n'y a ni octroi ni révocation : une revendication cesse d'être vraie quand son rapport
cesse d'être reproductible.

## 6. Revendications du dépositaire

**6.1.** Les implémentations du dépositaire revendiquent la conformité selon les §2 et §3, comme
toute autre : ni voie parallèle, ni accès anticipé.

**6.2.** Leurs rapports sont publiés au même endroit, au même format, et soumis au §5.

**6.3.** Le dépositaire ne peut pas accorder la marque : personne ne le peut.

**6.4.** Toute modification de ces règles qui profiterait à un produit du dépositaire suit le
processus ordinaire, motivation déclarée
([GOVERNANCE §2](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md#2-intérêt-déclaré)).

## 7. Licence

**7.1.** Apache-2.0 couvre le code et le texte, pas le nom. Forker est permis ; se dire
« OpenFSP conformant » relève de ces règles.

**7.2.** Un fork qui modifie le protocole et garde le nom ne peut revendiquer la conformité qu'en
réussissant la suite pour la version qu'il nomme.

**7.3.** Chacun peut exécuter la suite contre toute implémentation et publier le résultat.
