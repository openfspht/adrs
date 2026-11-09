# ADR-0003 : Cycle de vie du paiement

- Date : 2026-08-17
- Règles : [spec/cycle-de-vie.md](../spec/cycle-de-vie.md)

## Contexte

Côté marchand, la livraison dépend de l'état et exige un état qui ne varie plus une fois
rapporté terminal. Un statut qui change après avoir paru définitif
conduit à livrer contre un paiement qui n'aboutit pas, ou à relancer un paiement déjà débité.
Les vocabulaires de statut des opérateurs diffèrent, et certains ne distinguent pas « le payeur
n'a pas agi » de « état inconnu » (architecture 8.3).

## Décision

Je propose :

- Cinq états : `pending`, seul non terminal, et quatre terminaux (`succeeded`,
  `failed`, `expired`, `canceled`).
- Un état terminal n'est atteint que sur information faisant foi et n'est jamais quitté.
- `pending` signifie « non encore connu comme terminal » : il couvre aussi l'absence de
  réponse de l'opérateur. Pas d'état `unknown`.
- Aucune expiration par horloge : `expired` exige une confirmation (spec 5.3).
- Cinq sources faisant foi, dans l'ordre de préférence de la spec 6.5 : rappel signé,
  consultation, URL de rappel propre au paiement, relevé, attestation de l'exploitant. La
  découverte de capacités annonce les sources disponibles par opérateur.
- Un rappel signé ne vaut que si la signature couvre le paiement et son dénouement ; sinon il
  déclenche une consultation. Un montant contradictoire est un conflit, jamais un succès.
- L'attestation passe par l'administration de la passerelle, jamais par l'API : le détenteur
  d'une clé `payments:write` ne peut pas enregistrer un état terminal.
- `failure_reason` est une énumération fermée de huit valeurs, accompagnée de l'erreur brute
  de l'opérateur (`failure_detail`).
- Les capacités étendent la machine sans toucher aux états de base ni à la terminalité. Un
  remboursement est une ressource distincte.
- Relevés (reprend l'ADR-0017) : lisibles par le client, par opérateur et journée comptable à
  l'heure de Port-au-Prince ; chaque ligne porte brut, frais et net tels que rapportés, et est
  rapprochée d'un paiement ; une ligne `unmatched` ne crée jamais de paiement. Les lignes viennent
  de l'opérateur ou de l'export de son portail, qu'un exploitant peut attester complet.

## Conséquences

- Un paiement peut rester `pending` longtemps ; le rapprochement incombe à la passerelle
  (spec 6.1, 6.2), pas au marchand ; sa cadence reste ouverte.
- Un conflit avec un état terminal est enregistré et remonté, jamais résolu automatiquement.
- Chez un opérateur sans source automatique, chaque paiement attend une attestation.
- Pour `succeeded`, l'invariant s'aligne sur l'irrévocabilité de l'ordre de paiement
  (BRH-121 13.5). Pour les états d'échec, il protège contre le double débit après un échec
  apparent.
- L'état terminal immuable empêche la réécriture rétroactive des données de transaction
  (BRH-131 6.1 v).
- Ajouter un état de base est une rupture de compatibilité ; ajouter une valeur de
  `failure_reason` n'en est pas une.
- Les fonds reçus hors passerelle apparaissent au rapprochement (lignes `unmatched`).

## Ce que je n'ai pas retenu

- **Terminal révisable** : un état terminal pourrait changer, et le marchand devrait
  rapprocher lui-même chaque paiement.
- **État `unknown`** : même effet que `pending` sur la décision de livraison.
- **État `processing`** : ne change aucune décision ; une capacité pourra l'introduire.
- **Machine calquée sur les opérateurs** (`authorized`, `settling`…) : ni MonCash ni
  NatCash ne documentent ces états (architecture 8.3).
- **Expiration par horloge** : produit un échec terminal pour un paiement réussi juste avant
  la fermeture.
- **État `refunded`** : impose la modélisation du remboursement partout et efface la
  distinction entre jamais réussi et réussi puis remboursé.
- **État unique `closed` avec un champ d'issue** : déplace la machine à états dans un autre
  champ.

## Questions ouvertes

- Rendre `expires_at` obligatoire.
- Une cadence minimale de rapprochement, pour rendre le 6.2 testable.
- La représentation des conflits dans l'API.
- Capture et remboursement partiels.
- Exposer, par paiement, la source qui a fondé l'état terminal.
- Soldes d'ouverture et de clôture d'un relevé, et correction d'un relevé déjà clos.
