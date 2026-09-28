# ADR-0010 : Correspondance ISO 20022

- Statut : Proposée
- Date : 2026-09-06
- Guide : [spec/iso-20022.md](../spec/iso-20022.md) (informatif)

## Contexte

L'ADR-0001 affirme qu'OpenFSP emprunte le modèle conceptuel d'ISO 20022 comme dictionnaire, pas
comme transport. Sans tableau de correspondance, l'affirmation n'est pas vérifiable. Une
institution haïtienne devra aussi, tôt ou tard, produire du XML ISO 20022 pour la BRH ou une
banque.

## Décision

- Document informatif : correspondance élément par élément, statuts, codes de motif, pertes,
  éléments ISO non repris, annexe réglementaire.
- Aucune obligation, aucun test de conformité ; le modèle de données gouverne en cas de
  divergence.
- JSON sur le fil ; le XML doit pouvoir être produit mécaniquement.

## Conséquences

- Deux défauts de la spécification ont été trouvés et corrigés : le flux est un `pain.013`
  (demande d'activation du créancier), pas un `pain.001` ; le reçu de BRH-121 §8 exigeait des
  frais, d'où le champ `fee`.
- Une seule valeur de `failure_reason` sur huit a un code ISO exact ; trois se confondent en
  `MS03`.
- OpenFSP est plus strict qu'ISO sur la terminalité : pas de contre-passation.
- L'annexe met en regard BRH-121, BRH-126 et BRH-131 et les champs qui y répondent.

## Alternatives écartées

- **XML ISO 20022 sur le fil** : hiérarchie de compensation interbancaire vide pour ce marché.
- **Variantes JSON enregistrées par l'ISO** : même hiérarchie, même cadence de versions.
- **Noms de champs ISO** : promettraient une sémantique que les champs n'ont pas.
- **`failure_reason` étendu aux codes ISO** : des centaines de valeurs jamais rapportées.
- **Correspondance normative** : chaque publication de codes ISO deviendrait une rupture.

## Questions ouvertes

- Écart réel entre `pain.013` et `pain.001` sous le niveau transaction.
- Scinder `limit_exceeded` entre plafond d'opérateur et plafond réglementaire.
- Vocabulaire des frais plus fin.
- Publication des External Code Sets à fixer.
- Un exportateur dans le projet.
