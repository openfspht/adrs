# ADR-0003 : Cycle de vie du paiement

- Statut : Proposée
- Date : 2026-08-17
- Règles : [spec/cycle-de-vie.md](../spec/cycle-de-vie.md)

## Contexte

La question du marchand est « puis-je livrer ». Un statut qui change après avoir paru définitif
conduit à livrer contre un paiement qui n'aboutit pas, ou à relancer un paiement déjà débité.
Les vocabulaires de statut des opérateurs diffèrent, et plusieurs confondent « le payeur n'a
pas agi » et « état inconnu ».

## Décision

- Cinq états : `pending`, seul non terminal, et quatre terminaux (`succeeded`, `failed`,
  `expired`, `canceled`).
- Un état terminal n'est atteint que sur information autoritative et n'est jamais quitté.
- `pending` signifie « non encore connu comme terminal » : il couvre aussi l'absence de
  réponse de l'opérateur. Pas d'état `unknown`.
- Aucune expiration par horloge : `expired` exige une confirmation (spec §5.3).
- Cinq sources autoritatives, de la plus immédiate à la plus lente : rappel signé,
  consultation, URL de rappel propre au paiement, relevé, attestation de l'exploitant. Les
  sources disponibles par opérateur sont annoncées dans la découverte de capacités.
- Un rappel signé ne vaut que si la signature couvre le paiement et son dénouement ; sinon il
  déclenche une consultation. Un montant contradictoire est un conflit, jamais un succès.
- L'attestation passe par l'administration de la passerelle, jamais par l'API : une clé
  `payments:write` ne peut pas déclarer ses propres paiements réussis.
- `failure_reason` est une énumération fermée de huit valeurs, accompagnée de l'erreur brute
  de l'opérateur (`failure_detail`).
- Les capacités étendent la machine sans toucher aux états de base ni à la terminalité. Un
  remboursement est une ressource distincte.

## Conséquences

- Un paiement peut rester `pending` longtemps ; le rapprochement est une obligation de la
  passerelle, pas du marchand.
- Un conflit avec un état terminal est enregistré et remonté, jamais résolu automatiquement.
- Chez un opérateur sans source automatique, chaque paiement attend une attestation.
- Pour `succeeded`, l'invariant s'aligne sur l'irrévocabilité de l'ordre de paiement
  (BRH-121 §13.5). Pour les états d'échec, il protège contre le double débit après un échec
  apparent.
- L'état terminal immuable empêche la réécriture rétroactive des données de transaction
  (BRH-131 §6.1 v).
- Ajouter un état de base est une rupture de compatibilité ; ajouter une valeur de
  `failure_reason` n'en est pas une.

## Alternatives écartées

- **Terminal révisable** : rend tout état terminal consultatif et renvoie le rapprochement au
  marchand.
- **État `unknown`** : même réponse que `pending` à « puis-je livrer ».
- **État `processing`** : ne change aucune décision ; une capacité pourra l'introduire.
- **Machine calquée sur les opérateurs** (`authorized`, `settling`…) : la plupart des
  opérateurs ne peuvent pas la renseigner.
- **Expiration par horloge** : produit un échec terminal pour un paiement réussi juste avant
  la fermeture.
- **État `refunded`** : impose la modélisation du remboursement partout et efface la
  distinction entre jamais réussi et réussi puis remboursé.
- **État unique `closed` avec un champ d'issue** : déplace la machine à états dans un autre
  champ.

## Questions ouvertes

- Rendre `expires_at` obligatoire.
- Une cadence minimale de rapprochement, pour rendre le §6.2 testable.
- La représentation des conflits dans l'API.
- Capture et remboursement partiels.
- Exposer, par paiement, la source qui a fondé l'état terminal.
