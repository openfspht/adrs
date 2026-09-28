# ADR-0010 : Correspondance sémantique ISO 20022

- Voie : Informative
- Statut : Brouillon
- Créée : 2026-09-06
- Dépend de : ADR-0001, ADR-0002, ADR-0003, ADR-0005, ADR-0006

## Résumé

[ADR-0001](0001-architecture-and-scope.md) énonce qu'OpenFSP ancre son modèle de données
dans ISO 20022 comme dictionnaire plutôt que comme transport, et promet un document rendant
cet ancrage vérifiable. C'est ce document.

Il donne la correspondance élément par élément entre le paiement OpenFSP et les messages ISO
20022 des domaines Payments Initiation et Cash Management (§4), la correspondance des statuts
(§5), la correspondance des codes de motif de `failure_reason` à laquelle
[ADR-0003 §7.4.1](0003-payment-lifecycle.md) et [ADR-0005 §9](0005-error-taxonomy.md)
renvoient toutes deux (§6), un inventaire de tout ce que la correspondance perd (§7), un
inventaire de ce qu'ISO 20022 offre et qu'OpenFSP décline (§8), et l'annexe faisant
correspondre la Circulaire 121 de la BRH au champ ou à l'invariant qui y répond, promise par
[ADR-0001](0001-architecture-and-scope.md) (§9).

Il ne lie rien. Aucune implémentation ne change à cause de cette ADR, et aucun test de
conformité n'en dérive. Là où ce document et [ADR-0002](0002-core-data-model.md) divergent,
ADR-0002 gouverne le fil et ce document a tort.

Deux trouvailles y étaient inconfortables, et toutes deux ont depuis modifié la spécification
plutôt que d'être lissées. Le flux d'encaissement que spécifie OpenFSP correspond à une
CreditorPaymentActivationRequest et non à la CustomerCreditTransferInitiation que ADR-0001
nommait initialement, ce que cette ADR dit désormais (§3.4). Et le reçu exigé par la section 8
de la Circulaire 121 comporte les frais, pour lesquels la ressource paiement n'avait aucun
champ ; elle en a un maintenant, et la §9.3 consigne la séquence.

## Motivation

« Conforme à ISO 20022 » est une affirmation faite constamment et vérifiée presque jamais.
Elle signifie d'ordinaire que quelqu'un a lu la norme, emprunté un peu de vocabulaire et
s'est arrêté là. L'affirmation est attirante parce qu'elle est coûteuse à réfuter : il
faudrait qu'une institution s'assoie avec les définitions de messages et le modèle de données
de l'implémenteur et procède élément par élément, ce que personne ne fait pour une phrase
commerciale.

ADR-0001 fait une affirmation plus étroite et plus vérifiable, à savoir que le modèle de
données d'OpenFSP emprunte le modèle conceptuel d'ISO 20022, et elle promet ce document pour
que l'affirmation puisse être vérifiée. Une correspondance qui n'est jamais écrite est
indiscernable d'une correspondance qui n'existe pas, et un projet qui se dit « sémantiquement
aligné sur ISO 20022 » sans produire le tableau fait exactement ce que décrit le paragraphe
précédent.

Il existe une seconde motivation, plus pratique. Une institution haïtienne qui doit rapporter
à la BRH, se rapprocher d'une banque ou échanger des données avec une contrepartie opérant sur
des rails institutionnels aura besoin, à un moment, de XML ISO 20022. OpenFSP ne met pas de
XML sur le fil et ne le fera pas. La façon dont ces deux affirmations restent vraies
simultanément est que le JSON porte assez, et le porte dans la bonne forme, pour que le XML
puisse en être produit mécaniquement. Savoir s'il en est ainsi est une question qui a une
réponse, et les §4 et §7 sont cette réponse.

La troisième motivation est celle qui a rendu ce document digne d'être écrit plutôt que
simplement digne d'être promis. Faire la correspondance honnêtement a fait apparaître deux
défauts dans la spécification elle-même : un flux nommé d'après le mauvais message, et une
exigence réglementaire de reçu sans champ pour la satisfaire. Ni l'un ni l'autre n'était
visible depuis l'intérieur des ADR de paiement, qui étaient cohérentes sans eux. Les deux ont
depuis été corrigés. Un document de correspondance qui ne produirait aucune trouvaille de ce
genre serait un document que personne n'aurait réellement fait.

## Hors périmètre

- **Aucun changement de format de transport.** OpenFSP reste en JSON. Rien ici ne propose du
  XML sur le fil, et la §2.2 explique pourquoi l'ancrage est sémantique plutôt que syntaxique.
- **Aucune exigence normative.** Ceci est une ADR informative, elle n'emploie donc aucun
  mot-clé RFC 2119, conformément au [processus ADR](https://github.com/openfspht/adrs/blob/main/README.md#voies). Une implémentation
  ne peut pas échouer à se conformer à ce document, puisqu'il n'y a rien ici à quoi se
  conformer.
- **Aucune implémentation d'export ISO 20022.** La correspondance est ce à partir de quoi un
  exportateur serait bâti ; l'exportateur lui-même est un logiciel, et s'il est un jour
  spécifié, ce sera dans sa propre ADR.
- **Aucun enregistrement auprès de l'ISO.** OpenFSP ne soumet aucune définition de message, ne
  recherche aucune variante enregistrée, et ne prétend pas être un message ISO 20022.
- **Aucune correspondance pour ce qu'OpenFSP n'a pas spécifié.** Remboursements, transferts,
  capture et paiement de proximité n'ont pas encore de définition OpenFSP, ils n'ont donc rien
  à quoi correspondre. La §8 recense les éléments ISO qu'ils toucheraient.
- **Aucune prétention d'exhaustivité face à chaque variante ISO.** La §2.4 fixe les variantes
  contre lesquelles cette correspondance a été établie et dit ce qui se passe lorsqu'elles
  évoluent.

## 1. Statut de ce document

**1.1.** Ce document est descriptif. Il consigne la manière dont le modèle OpenFSP se rapporte
à ISO 20022 à la date figurant dans son en-tête. Il n'accorde aucune permission et n'impose
aucune obligation.

**1.2.** Là où ce document et une ADR de la voie Standards divergent, c'est l'ADR de la voie
Standards qui a raison. C'est la règle que [ADR-0002](0002-core-data-model.md) énonce déjà :
cette ADR gouverne le fil, et celle-ci en gouverne la lecture. Une divergence découverte ici
est un erratum contre ce document, non un défaut du protocole.

**1.3.** L'unique exception est une divergence qui se révèle être une véritable erreur de
modélisation, comme en §3.4. Dans ce cas, la trouvaille est consignée ici et la correction est
faite là où se trouve l'erreur, par erratum ou par ADR remplaçante. Ce document n'est pas
l'endroit où la corriger.

**1.4.** La correspondance est énoncée au niveau des **éléments métier** d'ISO 20022, non
d'une version particulière de schéma XML. Les noms d'éléments sont donnés dans la notation
propre à la norme (`CdtTrfTx/PmtId/EndToEndId`), parce que c'est ce qu'un lecteur cherchera.

## 2. Ce qui est emprunté, et ce qui ne l'est pas

**2.1. Emprunté : quatre idées.** [ADR-0001](0001-architecture-and-scope.md) les nomme, et
ce sont elles que le reste de ce document met à l'épreuve.

| Idée | Où elle se traduit dans OpenFSP |
|---|---|
| Une instruction et son statut sont des objets différents | [ADR-0003](0003-payment-lifecycle.md) : le paiement porte `status`, et le cycle de vie est spécifié à part de la ressource. |
| Les parties sont identifiées indépendamment de l'institution qui les détient | [ADR-0002 §5](0002-core-data-model.md) : un payeur est un numéro E.164, non un compte chez un opérateur nommé. |
| Un identifiant de bout en bout traverse toute la chaîne inchangé | [ADR-0002 §6.2](0002-core-data-model.md) : `Reference`, choisie par le marchand, est la clé de corrélation primaire. |
| Les montants sont typés par leur devise, jamais nus | [ADR-0002 §3](0002-core-data-model.md) : `Money` porte `amount` et `currency` ensemble. |

**2.2. Non emprunté : la syntaxe.** Les messages ISO 20022 sont en XML, et de plus en plus
aussi en JSON dans les variantes enregistrées par l'ISO. OpenFSP n'emploie ni l'un ni l'autre :
il emploie son propre JSON, parce que les définitions de messages portent une hiérarchie
dimensionnée pour la compensation interbancaire, et qu'un marchand intégrant un parcours de
paiement ne devrait pas avoir à construire un `GrpHdr` pour encaisser 1 250 gourdes.
L'argument de bande passante d'ADR-0001 est réel sur ce marché, et l'argument d'expérience
développeur est plus grand encore.

**2.3. Non emprunté : le processus.** ISO 20022 est également une autorité d'enregistrement,
un référentiel et une procédure de gouvernance des définitions de messages. OpenFSP ne
participe à rien de tout cela (*Hors périmètre*).

**2.4. Fixation des versions.** La correspondance ci-dessous a été établie contre les
définitions de messages des domaines Payments Initiation et Cash Management dans la forme
qu'elles ont prise depuis le cycle de maintenance de 2019, avec `pain.001`, `pain.002`,
`pain.013`, `pain.014` et `camt.053` comme messages d'intérêt, et contre les External Code
Sets tels que publiés par l'ISO dans son tableur trimestriel. Les éléments métier au niveau
employé ici sont stables d'une variante récente à l'autre. Les jeux de codes ne le sont pas :
ils gagnent des entrées chaque trimestre, et une entrée que ce document dit absente peut
exister au moment où il est lu. La §6.6 dit comment cela est traité, et la question non
résolue relative à la fixation d'une publication précise est réelle.

## 3. Quels messages correspondent

**3.1. Les trois que ADR-0001 nommait.**

| Message ISO | Sens métier | Contrepartie OpenFSP |
|---|---|---|
| `pain.013` CreditorPaymentActivationRequest | Un créancier demande à un débiteur d'autoriser un paiement à son profit. | Création de paiement, [ADR-0006 §5.1](0006-gateway-http-api-payments.md). Voir §3.4. |
| `pain.014` CreditorPaymentActivationRequestStatusReport | Le statut d'une telle demande. | Statut du paiement, [ADR-0003](0003-payment-lifecycle.md), livré par lecture ou par événement. |
| `pain.001` CustomerCreditTransferInitiation | Une partie initiatrice donne instruction à son institution de déplacer des fonds. | **Ce n'est pas la forme d'OpenFSP**, et c'est l'erreur que corrige la §3.4. Nommé ici parce que c'est le message auquel la plupart des lecteurs penseront, et la §4.1 dit comment lire ses lignes contre lui. |
| `pain.002` CustomerPaymentStatusReport | L'institution rend compte d'une instruction précédemment reçue. | Le rapport de statut appartenant à `pain.001`. Nommé pour la même raison, et la §4.2 dit comment ses lignes se lisent contre lui. |
| `camt.053` BankToCustomerStatement | Un relevé de compte, écriture par écriture, sur une période. | Rapprochement. OpenFSP ne définit aucun point d'accès de relevé ; la §4.3 fait correspondre le paiement à une écriture. |

**3.2.** La correspondance n'est pas d'un message par appel HTTP. Un `pain.013` porte un
en-tête de groupe, un ou plusieurs blocs d'information de paiement, et une ou plusieurs
transactions dans chacun ; une création de paiement OpenFSP porte exactement une transaction.
La correspondance de la §4.1 remplit donc les niveaux supérieurs avec le cas dégénéré :
`NbOfTxs` valant 1, `CtrlSum` égal au montant, un `PmtInf`, un `CdtTrfTx`. C'est une perte
d'expressivité et non d'information, et elle est consignée en §7.6.

**3.3.** `pain.002` correspond aux *deux* manières dont un client apprend un statut, la
lecture ([ADR-0006 §5.2](0006-gateway-http-api-payments.md)) et la réception d'un événement
([ADR-0008](0008-webhooks-and-event-delivery.md)). ISO 20022 ne distingue pas la poussée de
la traction, préoccupation de transport qu'elle laisse de côté, de sorte que les deux
produisent le même rapport de statut.

**3.4. Une trouvaille : le flux est `pain.013`, non `pain.001`.** Cela mérite d'être énoncé
clairement plutôt qu'enfoui dans un tableau, parce que ADR-0001 nommait le mauvais message et
que c'est ce document qui l'a trouvé.

`pain.001` modélise **un payeur donnant instruction à sa propre institution** de pousser des
fonds. Le paiement OpenFSP modélise **un marchand demandant à un payeur d'approuver un
encaissement** : le marchand crée le paiement, le payeur l'approuve sur son téléphone ou sur
une page de redirection, et les fonds bougent. ISO 20022 possède un message pour exactement
cette forme, et ce n'est pas `pain.001`. C'est `pain.013` CreditorPaymentActivationRequest,
avec `pain.014` comme rapport de statut. C'est le motif de la demande de paiement, et
l'approbation du payeur en est l'activation.

La distinction importe parce qu'elle est la différence entre « le payeur a dit à sa banque de
payer » et « le marchand a demandé, et le payeur a accepté ». La terminalité
([ADR-0003 §3.1](0003-payment-lifecycle.md)), `next_action`
([ADR-0006 §4](0006-gateway-http-api-payments.md)) et toute la notion d'un paiement en
attente du payeur découlent de la seconde forme, non de la première.

Deux choses en découlent :

- [ADR-0001](0001-architecture-and-scope.md) a été corrigée pour nommer `pain.013` et
  `pain.014`. Elle était à l'état `Draft`, où tout peut changer
  ([le processus ADR](https://github.com/openfspht/adrs/blob/main/README.md#cycle-de-vie)), de sorte que la correction a été faite en
  place plutôt que par la machinerie d'errata qui gouverne une ADR acceptée. Si elle avait été
  acceptée, la §1.3 se serait appliquée et le choix entre un erratum et une ADR remplaçante
  aurait appartenu à l'éditeur.
- Les tableaux des §4.1 et §4.2 sont énoncés contre `pain.013` et `pain.014`, ce qui est la
  conclusion de modélisation ci-dessus. Une version antérieure les énonçait contre `pain.001`
  et `pain.002` au motif que davantage de lecteurs connaissent ces messages, et signalait ce
  choix comme présentationnel. C'était une erreur : une ADR de correspondance dont les
  tableaux nomment le mauvais message sape la trouvaille qu'elle vient de faire, si clairement
  le choix soit-il signalé. Les lecteurs que ce choix devait servir le sont désormais par la
  note ouvrant chaque tableau, qui donne l'unique substitution transformant un chemin
  `pain.013` en un chemin `pain.001`.

**3.5. `camt.052` et `camt.054` ne sont pas mis en correspondance.** Le reporting intermédiaire
et la notification de débit ou de crédit sont les contreparties naturelles, respectivement,
d'une consultation de solde en cours de journée et d'un événement de notification. OpenFSP n'a
aucune notion de solde, et la §3.3 fait déjà correspondre l'événement. Les ajouter serait
faire de la correspondance pour allonger un tableau.

## 4. Correspondance des éléments

Lire `→` comme « est porté par ». Une cellule ISO vide signifie qu'OpenFSP détient une donnée
qu'ISO n'a nulle part où mettre naturellement ; une cellule OpenFSP vide signifie l'inverse,
et chaque ligne de ce type est reprise en §7 ou en §8.

**4.1. Création de paiement, contre `pain.013`.** Les chemins d'éléments ci-dessous sont ceux
de `CreditorPaymentActivationRequest`. Un lecteur qui connaît mieux `pain.001` peut lire
chaque ligne inchangée moyennant une substitution : le bloc de transaction s'y nomme
`CdtTrfTxInf` et se nomme `CdtTrfTx` ici. Rien d'autre ne diffère à ce niveau de détail, ce
qui est ce que veut dire la §3.4 lorsqu'elle affirme que la correspondance au niveau de la
transaction est presque identique entre les deux messages.

| OpenFSP | Élément ISO 20022 | Notes |
|---|---|---|
| (aucun) | `GrpHdr/MsgId` | Dégénéré, §3.2. Un exportateur le génère. Ce n'est pas la `Reference` : `MsgId` identifie un message, et OpenFSP n'envoie aucun message. |
| `created_at` | `GrpHdr/CreDtTm` | Exact. RFC 3339 vers ISO 8601 est sans perte. |
| (aucun) | `GrpHdr/NbOfTxs` | Toujours `1`. |
| `amount.amount` | `GrpHdr/CtrlSum` | Toujours égal au montant unique. |
| (aucun) | `GrpHdr/InitgPty` | Le marchand. Connu du déploiement, absent de la ressource paiement, parce que la passerelle sert un seul marchand ([ADR-0001](0001-architecture-and-scope.md)). |
| `id` | `PmtInf/PmtInfId` | Le `ResourceId` de la passerelle. |
| (aucun) | `PmtInf/PmtMtd` | `TRF`. |
| (aucun) | `PmtInf/ReqdExctnDt` | OpenFSP n'a aucune date d'exécution demandée. §8.2. |
| `payer.phone_number` | `PmtInf/Dbtr/Id/PrvtId/Othr/Id`, avec `SchmeNm/Prtry` valant `MSISDN` | La perte centrale. §7.1. |
| (aucun) | `PmtInf/DbtrAcct` | Il n'existe aucun identifiant de compte qui ne soit le numéro de téléphone. §7.1. |
| `provider` | `PmtInf/DbtrAgt/FinInstnId/Othr/Id` | Un identifiant de registre ([`registries/providers.md`](https://github.com/openfspht/openfsp/blob/main/registries/providers.md)), jamais un BIC. §7.2. |
| `reference` | `CdtTrfTx/PmtId/EndToEndId` | Le cœur de la correspondance. §4.4. |
| `id` | `CdtTrfTx/PmtId/InstrId` | L'identifiant attribué par la passerelle, correspondant au sens que donne l'ISO à un identifiant attribué par la partie donneuse d'instruction. |
| `amount` | `CdtTrfTx/Amt/InstdAmt` avec attribut `Ccy` | Requiert la conversion d'unités mineures de la §4.5. |
| `fee.bearer` | `CdtTrfTx/ChrgBr` | Ajouté par [ADR-0002 §8](0002-core-data-model.md). Les valeurs diffèrent : l'ISO distingue davantage de cas que `merchant` et `payer`. §7.4. |
| (aucun) | `CdtTrfTx/Cdtr`, `CdtrAcct`, `CdtrAgt` | Le marchand, de nouveau connu du déploiement plutôt que de la ressource. |
| `description` | `CdtTrfTx/RmtInf/Ustrd` | Risque de troncature, §7.7. |
| `metadata` | (aucun) | Aucune contrepartie ISO. §7.8. |
| `expires_at` | (aucun) | L'ISO n'a aucune expiration sur une instruction. §7.9. |
| `next_action` | (aucun) | Ce n'est pas du tout une notion du domaine des paiements. §7.10. |

**4.2. Statut du paiement, contre `pain.014`.** Le rapport de statut appartenant à une
`CreditorPaymentActivationRequest`. Les noms d'éléments ci-dessous sont partagés avec
`pain.002`, de sorte qu'un lecteur qui connaît ce message lit les lignes inchangées.

| OpenFSP | Élément ISO 20022 | Notes |
|---|---|---|
| (aucun) | `OrgnlGrpInfAndSts/OrgnlMsgId` | Dégénéré, comme en §4.1. |
| (aucun) | `OrgnlGrpInfAndSts/OrgnlMsgNmId` | La variante de la demande faisant l'objet du rapport, `pain.013.001.xx`. |
| `reference` | `TxInfAndSts/OrgnlEndToEndId` | Le champ sur lequel un rapport de statut est rattaché à son instruction, ce qui est exactement le rôle que joue `Reference` dans [ADR-0002 §6.2.3](0002-core-data-model.md). |
| `id` | `TxInfAndSts/OrgnlInstrId` | |
| `provider_reference` | `TxInfAndSts/AcctSvcrRef` | Exact quant au sens : un identifiant attribué par l'institution gestionnaire. Optionnel dans les deux, et possiblement absent à jamais dans les deux ([ADR-0002 §6.3](0002-core-data-model.md)). |
| `status` | `TxInfAndSts/TxSts` | §5. |
| `failure_reason` | `TxInfAndSts/StsRsnInf/Rsn/Cd` | §6. |
| `failure_detail` | `TxInfAndSts/StsRsnInf/AddtlInf` | Texte libre dans l'ISO, objet de report structuré dans OpenFSP. Perte à l'export, §7.11. |
| `updated_at` | `GrpHdr/CreDtTm` | Le moment du rapport, ce qui est le sens d'`updated_at` pour un changement de statut. |
| `completed_at` | (aucun) | L'ISO ne porte aucun horodatage d'achèvement sur un rapport de statut. Il apparaît dans `camt.053` sous `BookgDt`. §7.12. |

**4.3. Rapprochement, contre `camt.053`.** Un paiement terminal correspond à une écriture de
relevé. OpenFSP n'a pas de relevé, la correspondance va donc du paiement vers `Ntry`.

| OpenFSP | Élément ISO 20022 | Notes |
|---|---|---|
| `id` | `Ntry/NtryRef` | |
| `amount` | `Ntry/Amt` avec `Ccy` | |
| (implicite) | `Ntry/CdtDbtInd` | `CRDT` du point de vue du marchand. Un encaissement crédite le marchand. |
| `status` | `Ntry/Sts` | Seul `succeeded` produit une écriture, donc `BOOK`. Un paiement en attente n'est pas une écriture. §7.13. |
| `completed_at` | `Ntry/BookgDt` | |
| (aucun) | `Ntry/ValDt` | OpenFSP ne distingue pas la date de valeur de la date de comptabilisation. §7.12. |
| `provider_reference` | `Ntry/AcctSvcrRef` | |
| (aucun) | `Ntry/BkTxCd` | Un code de transaction bancaire, structuré par domaine, famille et sous-famille. OpenFSP n'a aucune classification équivalente. §8.4. |
| `reference` | `Ntry/NtryDtls/TxDtls/Refs/EndToEndId` | La même valeur qu'en §4.1, ce qui est l'objet même d'un identifiant de bout en bout. |
| `description` | `Ntry/NtryDtls/TxDtls/RmtInf/Ustrd` | |
| (aucun) | `Stmt/Bal` | OpenFSP n'a aucune notion de solde ni de période de relevé. §7.14. |

**4.4. `Reference` et `EndToEndId` sont la même idée, et c'est la ligne la plus forte de ce
document.** L'ISO définit `EndToEndId` comme un identifiant attribué par la partie initiatrice
et transmis inchangé à travers toute la chaîne. [ADR-0002 §6.2](0002-core-data-model.md)
définit `Reference` comme choisie par le marchand, unique, et clé de corrélation primaire,
précisément pour qu'un marchand ayant perdu la réponse à une création détienne encore la clé
du paiement. Les deux définitions ont été atteintes pour la même raison et se comportent de
manière identique.

C'est également là que la formulation du whitepaper, et toute présentation du modèle, doit
être soignée : l'identifiant de bout en bout est la `Reference` du marchand, non le
`ResourceId` de la passerelle. `ResourceId` est opaque et attribué par la passerelle
([ADR-0002 §6.1](0002-core-data-model.md)), ce qui correspond à `InstrId`, un élément ISO
différent doté d'un propriétaire différent.

**4.5. Les montants.** L'ISO porte un décimal assorti d'un attribut `Ccy`, par exemple
`<InstdAmt Ccy="HTG">1250.00</InstdAmt>`. OpenFSP porte un entier en unités mineures,
`{"amount": 125000, "currency": "HTG"}` ([ADR-0002 §3](0002-core-data-model.md)). La
conversion est une division par dix à la puissance de l'exposant d'unité mineure de la devise,
tiré d'ISO 4217, que [ADR-0002 §4](0002-core-data-model.md) exige déjà des implémentations de
connaître. Elle est sans perte dans les deux sens pour toutes les devises du périmètre. Elle
ne préserve pas la forme, et un exportateur qui oublie l'exposant se trompe d'un facteur cent
dans le sens du trop-perçu, sans qu'aucune validation ne l'arrête.

## 5. Correspondance des statuts

**5.1.** OpenFSP a cinq états ([ADR-0003 §1](0003-payment-lifecycle.md)). Le jeu de codes
de statut de transaction de paiement externe de l'ISO en compte considérablement plus.

| `status` OpenFSP | `TxSts` ISO | Fidélité |
|---|---|---|
| `pending` | `PDNG` | Perte dans un sens. §5.2. |
| `succeeded` | `ACSC`, ou `ACCC` lorsque le compte du créancier est connu comme crédité | §5.3. |
| `failed` | `RJCT` | Avec un code de motif de la §6. |
| `expired` | `RJCT` | Aucun statut ISO distinct. §5.4. |
| `canceled` | `CANC` | Exact. |

**5.2. `pending` est délibérément grossier, et l'ISO délibérément fin.** L'ISO distingue
l'acceptation après validation technique, l'acceptation après contrôles du profil client, et
l'acceptation avec règlement en cours. [ADR-0003 §1.1](0003-payment-lifecycle.md) les
rassemble tous, plus le cas où la passerelle a émis une requête sans recevoir de réponse, dans
un seul état signifiant *pas encore connu comme terminal*.

Ce rassemblement est une décision de conception, non un oubli, et la correspondance avec l'ISO
ne le défait pas. Un exportateur peut émettre `PDNG` honnêtement. Il ne peut pas récupérer
`ACTC` depuis un paiement OpenFSP, parce que l'information n'a jamais été détenue. Un opérateur
qui rapporte la distinction plus fine la donne à `failure_detail` ou à rien.

**5.3. `succeeded` se situe entre deux codes ISO.** `ACSC` signifie règlement achevé du côté
du débiteur ; `ACCC` signifie que le compte du créancier a été crédité. Le `succeeded`
d'OpenFSP signifie que l'opérateur a confirmé de manière autoritative que les fonds sont
capturés, ce qui est plus proche d'`ACCC` par l'intention et plus proche d'`ACSC` par ce qu'un
opérateur de monnaie mobile dit réellement à la passerelle. Un exportateur en choisit un et
documente lequel. Ce document ne choisit pas, parce que choisir reviendrait à inventer un fait
au sujet de l'opérateur.

**5.4. `expired` et `failed` entrent en collision.** Les deux deviennent `RJCT`, distingués
seulement par le code de motif, et l'ISO n'a pas de meilleure réponse : une instruction qui a
manqué de temps n'a pas été acceptée, elle a donc été rejetée. La distinction OpenFSP ne
survit à l'aller-retour que si le code de motif y survit.

**5.5. La correspondance n'est injective dans aucun des deux sens**, ce qui est le résumé
honnête de cette section. Cinq états OpenFSP correspondent à quatre codes ISO ; plus d'une
douzaine de codes ISO correspondent à un seul état OpenFSP. Un aller-retour par ISO 20022 ne
restitue pas le paiement de départ, et la §7 est la liste de ce qu'il laisse tomber.

## 6. Correspondance des codes de motif

**6.1.** [ADR-0003 §7.2](0003-payment-lifecycle.md) ferme `failure_reason` à huit valeurs.
Le jeu de codes de motif de statut externe de l'ISO en compte plusieurs centaines. La
correspondance ci-dessous est celle que [ADR-0003 §7.4.1](0003-payment-lifecycle.md)
promet.

| `failure_reason` | Code de motif ISO | Fidélité |
|---|---|---|
| `insufficient_funds` | `AM04` InsufficientFunds | **Exact.** L'unique ligne nette. |
| `payer_canceled` | `CUST` RequestedByCustomer | Partielle. §6.3. |
| `limit_exceeded` | `AM21` LimitExceeded, ou `RR04` RegulatoryReason lorsque le plafond est réglementaire | Ambiguë. §6.4. |
| `rejected_by_provider` | `AG01` TransactionForbidden | Partielle. §6.5. |
| `payer_unreachable` | aucun code unique | §6.6. |
| `declined` | `MS03` NotSpecifiedReasonAgentGenerated | Collision. §6.7. |
| `provider_error` | `MS03`, ou `ED05` SettlementFailed lorsque le règlement a été tenté | Collision. §6.7. |
| `unspecified` | `MS03` | La seule valeur pour laquelle `MS03` convienne. |

**6.2.** Une ligne sur huit est exacte. Ce nombre est la chose la plus utile de cette section,
et toute présentation d'OpenFSP comme aligné sur ISO 20022 devrait pouvoir survivre à ce qu'on
le lui oppose.

**6.3. `payer_canceled` couvre deux conditions que l'ISO sépare.** Un payeur qui refuse dans
l'application de l'opérateur a demandé l'annulation, ce qui est `CUST`. Un payeur qui s'en va
et laisse la demande se périmer n'a rien demandé, et appeler cela `CUST` lui attribue un acte
qu'il n'a pas accompli. [ADR-0003 §7.2](0003-payment-lifecycle.md) fusionne les deux parce
que la réponse d'un marchand est identique. La lecture plus fine de l'ISO est disponible et
inutilisée.

**6.4. `limit_exceeded` est réellement ambiguë.** La définition OpenFSP couvre « un plafond de
l'opérateur ou réglementaire », une seule valeur pour deux conditions aux conséquences
différentes : un plafond d'opérateur est un paramètre commercial qu'un marchand pourrait
négocier, un plafond réglementaire ne l'est pas. L'ISO les sépare, et la fusion est du côté
d'OpenFSP. C'est sans doute un défaut de [ADR-0003 §7.2](0003-payment-lifecycle.md) plutôt
que de la correspondance, et la question est soulevée dans *Questions non résolues* plutôt que
corrigée ici.

**6.5. `rejected_by_provider` est la ligne de la conformité, et l'imprécision est peut-être
une qualité.** Sa définition OpenFSP est « refusé pour un motif propre à l'opérateur, tel que
le risque ou la conformité ». `AG01` TransactionForbidden est le code le plus proche. Une
correspondance précise exigerait parfois de divulguer qu'un refus est motivé par la
conformité, ce qui, dans plusieurs juridictions, est exactement ce qu'une institution ne peut
pas divulguer. Une valeur unique et peu informative est le comportement le plus sûr, et il
vaut la peine de remarquer que la fusion protège au lieu de dégrader.

**6.6. `payer_unreachable` n'a aucune contrepartie, et le manque est instructif.** La condition
fusionne « ce compte n'existe pas », que l'ISO code `AC01` IncorrectAccountNumber, « le compte
est fermé », `AC04`, et « le téléphone du payeur n'a pas répondu », que l'ISO ne code pas du
tout parce que la messagerie interbancaire n'a aucune notion de partie devant être jointe en
temps réel. L'absence n'est pas un oubli de l'ISO. C'est une différence de domaine : la monnaie
mobile requiert la participation du payeur en direct, le modèle des paiements institutionnels
non.

Si une publication future des External Code Sets ajoute un code pour cette condition, c'est
dans cette ligne qu'il atterrira, et le changement sera un erratum contre ce document.

**6.7. Trois valeurs OpenFSP s'effondrent sur `MS03`.** `declined`, `provider_error` et
`unspecified` deviennent toutes « motif non spécifié, généré par l'agent ». Quiconque ne lit
que l'export ISO ne peut pas distinguer un refus d'une défaillance de l'opérateur du côté de
la passerelle. Cette distinction étant de celles sur lesquelles un marchand agit
différemment, c'est la perte unique la plus lourde de conséquences de ce document, et un
exportateur soucieux devrait porter `failure_reason` tel quel dans `AddtlInf` à côté du code.

**6.8.** Rien de ce qui précède ne change `failure_reason`.
[ADR-0003 §7.4.1](0003-payment-lifecycle.md) est explicite : une valeur est ajoutée parce
qu'un marchand agirait dessus, jamais parce que l'ISO dispose d'un code inutilisé, et le rôle
de cette section est de consigner la distance plutôt que de la combler.

## 7. Ce que la correspondance perd

La promesse de [ADR-0001](0001-architecture-and-scope.md) est que les pertes soient
documentées comme des pertes. Voici cette liste.

**7.1. Un numéro de téléphone n'est pas un compte.** Le modèle de partie de l'ISO suppose un
compte dans une institution identifiée : `Dbtr` nomme la partie, `DbtrAcct` le compte,
`DbtrAgt` l'institution. OpenFSP identifie un payeur par un numéro E.164
([ADR-0002 §5](0002-core-data-model.md)) et n'a rien à mettre dans les deux autres. La
correspondance place le numéro dans un `Othr/Id` propriétaire sous un nom de schéma `MSISDN`,
ce qui est syntaxiquement valide et sémantiquement mince : cela dit « voici une chaîne qui
identifie quelqu'un » et rien sur l'endroit où se trouve son argent.

Aucune discipline de nommage n'améliore cela, et la position honnête est que le modèle de
partie de l'ISO ne convient pas à un marché où le compte *est* le numéro de téléphone. Il vaut
la peine d'être précis sur celle des quatre idées empruntées qui survit : les parties sont
toujours identifiées indépendamment de l'institution qui les détient, ce qui est l'idée. Ce
qui est perdu est l'identification institutionnelle que l'ISO attend à côté.

**7.2. Il n'y a pas de BIC.** `DbtrAgt` et `CdtrAgt` attendent un identifiant d'institution
financière, canoniquement un BIC. Les opérateurs haïtiens de monnaie mobile n'en ont pas, au
sens que le champ donne à ce terme. La correspondance emploie un identifiant propriétaire tiré
du registre d'opérateurs d'OpenFSP, stable et unique au sein d'OpenFSP et dénué de sens en
dehors. Un export franchissant la frontière vers un système qui résout les BIC ne résoudra pas
ceux-ci.

**7.3. Les montants survivent ; leur forme non.** §4.5. Sans perte, et piégeux.

**7.4. Le frais correspond, sa granularité non.** L'ISO porte `ChrgBr` pour dire qui supporte
les frais et `ChrgsInf` pour dire ce qu'ils étaient. OpenFSP porte désormais un `Fee`
([ADR-0002 §8](0002-core-data-model.md)), ajouté après que cette annexe eut identifié
l'omission, de sorte que le montant et celui qui le supporte correspondent. Ce qui ne
correspond pas est le vocabulaire plus fin de l'ISO sur la charge des frais, qui distingue
davantage de cas que `merchant` et `payer`, et sa capacité à détailler plusieurs frais. La
perte porte sur la granularité plutôt que sur le chiffre lui-même.

**7.5. Il n'y a ni date de règlement ni date d'exécution.** `ReqdExctnDt` dans `pain.001` et
`ValDt` dans `camt.053` expriment tous deux une date distincte du moment de l'instruction.
OpenFSP a `created_at`, `updated_at` et `completed_at`, tous trois des horodatages
d'événements. Un marché où le règlement est en temps réel
([Circulaire 121, sa section 13.5](0001-architecture-and-scope.md)) rend la distinction
presque vide, ce qui est la raison pour laquelle personne ne l'a regrettée. C'est néanmoins
une perte réelle face à l'ISO, et elle mordrait dès qu'un paiement différé ou programmé serait
spécifié.

**7.6. Le traitement par lot est inexprimable.** §3.2. Un paiement, une transaction, toujours.
Un `pain.001` portant une paie de quatre cents virements n'a aucune contrepartie OpenFSP, et
il faudrait la construire plutôt que la faire correspondre.

**7.7. L'information de remise peut être tronquée.** `description` autorise 255 points de code
([ADR-0006 §3.1](0006-gateway-http-api-payments.md)) ; `RmtInf/Ustrd` est
conventionnellement limité à 140 caractères par occurrence. Un exportateur répartit sur
plusieurs occurrences ou tronque, et la troncature est une perte silencieuse dans un champ que
les marchands emploient pour leur propre comptabilité.

**7.8. `metadata` n'a aucune contrepartie.** [ADR-0002 §9](0002-core-data-model.md) existe
pour qu'un marchand puisse attacher ses propres paires clé-valeur à un paiement. L'ISO n'a
aucun point d'extension général de ce type dans ces messages, données supplémentaires mises à
part, et un export le laisse entièrement tomber.

**7.9. L'expiration est inexprimable.** `expires_at`
([ADR-0003 §5](0003-payment-lifecycle.md)) n'a aucun élément ISO. Une instruction, dans
l'ISO, ne se périme pas ; elle est exécutée, rejetée ou annulée. C'est la même différence de
domaine que la §6.6, vue de l'autre côté.

**7.10. `next_action` n'est pas une notion du domaine des paiements.** Il dit à un client ce
que le payeur doit maintenant faire : suivre une redirection, ou approuver sur son téléphone
([ADR-0006 §4](0006-gateway-http-api-payments.md)). ISO 20022 modélise des messages entre
institutions et n'a aucun vocabulaire pour donner des instructions à l'interface d'un
intégrateur, parce que ce n'est pas à cela que sert la norme. L'élément est abandonné à
l'export et rien n'est anormal.

**7.11. `failure_detail` se dégrade en texte libre.**
[ADR-0003 §7.4](0003-payment-lifecycle.md) exige le code et le message propres de
l'opérateur tels quels, sous forme structurée. `AddtlInf` est une chaîne. L'information
survit ; son exploitabilité par machine non.

**7.12. Les dates de comptabilisation et de valeur s'effondrent en un seul horodatage.** §7.5,
en termes de `camt.053`.

**7.13. Les paiements non terminaux n'ont pas d'écriture.** Une écriture de `camt.053` est
quelque chose qui est arrivé à un compte. Un paiement en attente n'est pas arrivé. Quiconque
se rapproche à partir d'un export ne voit que les paiements réussis, ce qui est correct et
mérite d'être dit, parce qu'un marchand comparant un export à `GET /v1/payments` trouvera
moins de lignes et ne devrait pas en conclure que quelque chose manque.

**7.14. Il n'y a ni solde ni période de relevé.** `camt.053` est bâti autour d'un compte sur
un intervalle, avec soldes d'ouverture et de clôture. OpenFSP n'a aucun objet compte. La
correspondance de la §4.3 atteint le niveau de l'écriture et s'arrête, et toute enveloppe de
relevé est synthétisée par l'exportateur à partir de données qu'OpenFSP ne détient pas.

**7.15. La terminalité est plus stricte dans OpenFSP, et c'est aussi une discordance.**
[ADR-0003 §3.1](0003-payment-lifecycle.md) interdit de quitter un état terminal, jamais.
L'ISO permet à un rapport de statut ultérieur d'en remplacer un antérieur, et comporte des
messages entiers, `camt.056` et `pain.007`, pour contre-passer ce qui a été fait. Un flux
parfaitement conforme à ISO 20022 peut donc produire une séquence qu'OpenFSP refuserait
d'appliquer. La perte va ici dans l'autre sens : OpenFSP décline une information que l'ISO est
disposée à porter, délibérément, et [ADR-0003](0003-payment-lifecycle.md) explique
longuement pourquoi.

## 8. Ce qu'ISO 20022 a et qu'OpenFSP n'a pas

La liste de la §7 recense ce qui disparaît à l'export. Celle-ci recense ce que l'ISO offre et
qu'OpenFSP n'a jamais pris, chaque élément étant absent pour la raison que
[ADR-0007](0007-capability-discovery.md) donne au sujet des capacités : ce qu'aucun
opérateur de ce marché n'expose est déclaré absent plutôt qu'émulé.

**8.1. Codes de finalité.** `Purp/Cd` et `CtgyPurp/Cd` classent la raison pour laquelle un
paiement est fait, à partir d'un vocabulaire contrôlé. La section 8 de la Circulaire 121 exige
d'un reçu qu'il indique la nature du service, ce qui est proche de ce à quoi sert un code de
finalité, et la §9.2 y revient.

**8.2. Date d'exécution demandée.** §7.5.

**8.3. Granularité des frais.** §7.4. Le chiffre et celui qui le supporte correspondent ; le
vocabulaire plus fin de l'ISO sur la charge des frais, et sa capacité à en détailler
plusieurs, non.

**8.4. Codes de transaction bancaire.** `BkTxCd`, la classification par domaine, famille et
sous-famille qui rend possible le rapprochement automatisé sur les relevés institutionnels.
L'adopter exigerait une classification dont OpenFSP n'a aucune source.

**8.5. Parties ultimes.** `UltmtDbtr` et `UltmtCdtr` distinguent la partie pour le compte de
laquelle un paiement est fait de celle qui le fait. Une place de marché payant un vendeur via
une plateforme a exactement cette forme, et OpenFSP n'a aucun moyen de l'exprimer. À retenir
quand viendront les flux de place de marché.

**8.6. Information de remise structurée.** L'ISO porte des références créancier structurées,
dont la norme ISO 11649, qui permettent de rattacher automatiquement un paiement à une
facture. [ADR-0002 §6.2](0002-core-data-model.md) obtient le même résultat avec une
`Reference` choisie par le marchand, autrement et plus simplement.

**8.7. Reporting réglementaire.** `RgltryRptg` porte des données réglementaires structurées
avec l'instruction. [ADR-0001](0001-architecture-and-scope.md) refuse de définir un
reporting réglementaire parce qu'il revient à l'autorité d'en fixer les exigences. Si la BRH
venait à les fixer, c'est dans cet élément qu'une réponse de forme ISO résiderait, et la §9 est
ce qui la rendrait dérivable.

**8.8. Mandats.** Mandats de prélèvement, leurs identifiants et leur historique d'amendement.
L'encaissement récurrent n'est pas dans le périmètre d'OpenFSP, et voici la machinerie qu'il
faudrait.

**8.9. Priorité et niveau de service.** `InstrPrty`, `SvcLvl`. Dénués de sens là où le
règlement est en temps réel et où il n'y a qu'un niveau de service.

## 9. Annexe réglementaire

[ADR-0001](0001-architecture-and-scope.md) promet que ce document porte une annexe faisant
correspondre les sections de la Circulaire 121 de la BRH du 6 décembre 2021 au champ ou à
l'invariant qui y répond [BRH-121]. Voici cette annexe, à laquelle se sont depuis ajoutées
deux autres circulaires et le texte de loi dont les trois procèdent.

Le cadre haïtien est une chaîne, et lire une circulaire sans elle empêche un lecteur de
mesurer sa portée. `HT-LAW-2012` est le texte de loi. Son article 83 habilite la BRH à établir
des règles, notamment à son alinéa 9 sur la protection des déposants et à son alinéa 10 sur
« les mécanismes de contrôle et de sécurité dans le domaine de l'informatique »
[HT-LAW-2012, p. 29] ; son article 161 donne le pouvoir de contrôler et de sanctionner, et de
différencier par catégorie d'institution [HT-LAW-2012, p. 53]. `BRH-121` régit les services de
paiement électronique, `BRH-126` la sécurité informatique, `BRH-131` la protection des
consommateurs. L'annexe fait correspondre les exigences de la circulaire à OpenFSP d'abord,
parce que c'est ce qu'un superviseur vérifierait, et à ISO 20022 ensuite, parce que c'est ce
qu'un export porterait.

**9.1. Section 8, le reçu.** La circulaire exige un reçu portant la référence de la
transaction, la nature du service, le nom du fournisseur, les parties, ainsi que la date, le
montant et les frais.

| Élément exigé | OpenFSP | ISO 20022 |
|---|---|---|
| Référence de la transaction | `reference`, et `provider_reference` lorsque l'opérateur en attribue une | `EndToEndId`, `AcctSvcrRef` |
| Nature du service | **absente** | `Purp/Cd` |
| Nom du fournisseur | `provider`, résolu par [`registries/providers.md`](https://github.com/openfspht/openfsp/blob/main/registries/providers.md) | `DbtrAgt`, propriétaire (§7.2) |
| Les parties | `payer`, plus le marchand connu du déploiement | `Dbtr`, `Cdtr` |
| Date | `completed_at` | `BookgDt` |
| Montant | `amount` | `InstdAmt` |
| Frais | `fee` ([ADR-0002 §8](0002-core-data-model.md)) | `ChrgsInf`, `ChrgBr` |

**9.2.** Six sur sept sont portés. Celui qui ne l'est pas, la nature du service, est nommé
ci-dessus plutôt que glosé : un marchand sait ce qu'il a vendu et peut l'inscrire dans
`description` ou `metadata`, et un code de finalité serait meilleur sans être nécessaire pour
se conformer.

Un reçu est au marchand de le produire, et rien dans la circulaire n'exige de la passerelle
qu'elle le produise, de sorte que rien ici n'est un manquement à la conformité. C'est une
question de ce qu'OpenFSP remet à un marchand face à ce que le marchand est ensuite tenu
d'imprimer.

**9.3. Le frais était la trouvaille de cette annexe, et il y a été donné suite.** Cette annexe
rapportait à l'origine cinq sur sept, le chiffre manquant étant le frais : un marchand à qui
l'on en facture un doit l'indiquer, et la ressource paiement ne lui donnait nulle part où le
lire, alors que tous les opérateurs de ce marché en facturent. C'était une omission de la voie
Standards, qu'une ADR informative peut identifier et non réparer.

Elle a été réparée. [ADR-0002 §8](0002-core-data-model.md) définit un `Fee`,
[ADR-0006 §3.5](0006-gateway-http-api-payments.md) le porte sur le paiement, et
[ADR-0007 §2.2](0007-capability-discovery.md) enregistre `payments.fee` pour les opérateurs
qui en divulguent un. La question de conception soulevée par cette annexe est ce qui l'a
façonné : un frais peut n'être connu qu'après l'achèvement du paiement, peut être supporté par
l'une ou l'autre partie, et n'est pas divulgué par tous les opérateurs, de sorte que l'absence
signifie « non connu » et jamais « aucun », et qu'un opérateur qui ne divulgue jamais rien est
déclaré comme tel plutôt que de renvoyer indéfiniment un champ vide.

Ceci est consigné plutôt que discrètement réécrit parce que la séquence est le propos. Un
exercice de correspondance a trouvé une omission dans la spécification normative qu'aucune
vérification de cohérence interne n'aurait fait apparaître, et la spécification a changé en
conséquence.

**9.4. Section 13.1, identification unique et traçabilité.**

| Exigence | OpenFSP | ISO 20022 |
|---|---|---|
| Chaque client uniquement identifié | `payer` en E.164, le marchand comme principal propre au déploiement ([ADR-0009 §5](0009-authentication-and-credentials.md)) | `Dbtr`, `InitgPty` |
| Chaque transaction traçable | `reference` inchangée de bout en bout, `id` immuable, `request_id` ([ADR-0005 §1.6](0005-error-taxonomy.md)) sur chaque réponse, et l'enregistrement d'audit de [ADR-0009 §10](0009-authentication-and-credentials.md) | `EndToEndId` |

**9.5. Section 13.4, le registre des opérations.** La ressource paiement est le registre. Le
journal d'événements de [ADR-0008](0008-webhooks-and-event-delivery.md) en est une vue
dérivée en ajout seul, et la section réglementaire d'ADR-0008 dit explicitement qu'il s'agit
d'une vue et non d'un substitut. La contrepartie ISO est le jeu d'écritures `camt.053` de la
§4.3.

**9.6. Section 13.5, temps réel et irrévocabilité.** La circulaire exige que les opérations se
dénouent en temps réel et rend l'ordre de paiement irrévocable. L'invariant OpenFSP qui s'y
aligne est la terminalité de `succeeded`, [ADR-0003 §3.1](0003-payment-lifecycle.md) : un
paiement réussi n'est jamais quitté. La circulaire ne dit rien des états d'échec, dont la
terminalité repose sur un autre motif, exposé dans la *Motivation*
d'[ADR-0003](0003-payment-lifecycle.md). La §7.15 consigne qu'OpenFSP est ici plus strict que
l'ISO, qui prévoit des contre-passations, et cette section en est la raison : une machine à
états qui permettrait de réviser un paiement réussi modéliserait un autre marché.

Les messages de contre-passation qu'offre l'ISO, `camt.056` et `pain.007`, sont donc
délibérément non mis en correspondance. Un remboursement, dans ce modèle, est un nouveau
paiement en sens inverse et auditable séparément, ce que
[ADR-0003](0003-payment-lifecycle.md) spécifie déjà.

**9.7. Section 15, protection des données.** La transmission est traitée par
[ADR-0006 §1.1](0006-gateway-http-api-payments.md) et
[ADR-0008 §7.2](0008-webhooks-and-event-delivery.md) ; la conservation et la gestion des
identifiants par [ADR-0009 §4](0009-authentication-and-credentials.md) et
[§9](0009-authentication-and-credentials.md). ISO 20022 n'a aucune contrepartie, étant une
norme de messagerie et non une norme de sécurité, et cette ligne existe pour le dire plutôt
que de laisser un lecteur s'interroger.

**9.8. Section 5, interopérabilité et audit.** La circulaire range l'interopérabilité parmi
les exigences techniques qu'un prestataire doit satisfaire et impose un audit externe au moins
tous les trois ans, sans prescrire de norme par laquelle l'interopérabilité serait jugée. Ce
document fait partie de la réponse : une correspondance qu'un superviseur peut lire, contre un
modèle de données qu'une suite de conformité peut tester. La correspondance n'est pas la
preuve ; la correspondance plus la suite l'est.

**9.9. `BRH-126`, sécurité informatique.** Ses quatre dispositions qui atteignent cette
spécification n'ont aucune contrepartie ISO 20022, et la ligne existe pour le dire : ISO 20022
est une norme de messagerie, et la sécurité informatique n'est pas ce qu'elle normalise.

| Exigence | OpenFSP | ISO 20022 |
|---|---|---|
| Disponibilité, intégrité, confidentialité, traçabilité de toutes les données [BRH-126, p. 1, § 2] | Les quatre propriétés autour desquelles les ADR de la voie Standards sont organisées | aucune |
| Documentation des systèmes, tenue à jour par consignation des évolutions [BRH-126, p. 4, § 3 p)] | L'ensemble des ADR lui-même, versionné, avec errata datés | aucune |
| Exigences de sécurité établies avant mise en production [BRH-126, p. 3, § 3 n)] | *Considérations de sécurité*, obligatoires et jamais vides, avant acceptation | aucune |
| Audit de sécurité informatique au moins tous les trois ans [BRH-126, p. 4, § 3 t)] | [ADR-0015](0015-conformance-levels-and-suite.md), et les enregistrements d'audit de [ADR-0009 §10](0009-authentication-and-credentials.md) | aucune |

**9.10. `BRH-131`, protection des consommateurs.** Quatre de ses dispositions ont une
contrepartie, et l'une d'elles change la lecture de la §9.3.

| Exigence | OpenFSP | ISO 20022 |
|---|---|---|
| Signaler et compenser toute perte du consommateur liée à une défaillance du système [BRH-131, p. 8, § 6.1 s)] | `effect` et le catalogue fermé de [ADR-0005 §9](0005-error-taxonomy.md) ; `failure_reason` de [ADR-0003 §7.2](0003-payment-lifecycle.md) | `StsRsnInf/Rsn/Cd`, §6, avec la fidélité qui y est consignée |
| Définir clairement les responsabilités respectives des parties en cas de pertes financières [BRH-131, p. 17, § 6.9 c)] | Un vocabulaire partagé de la défaillance en est la condition préalable | `StsRsnInf` |
| Aucune surfacturation par le marchand sur les paiements par carte ou autre moyen électronique [BRH-131, p. 8, § 6.1 p)] | Réponse structurelle : `fee.bearer` rapporte ce qu'a fait l'opérateur et un client ne peut pas le fixer ([ADR-0002 §8.4](0002-core-data-model.md)), de sorte que le protocole ne donne au marchand aucun moyen d'en ajouter une. §9.11. | `ChrgBr` |
| Minimisation des données, seules les données strictement nécessaires collectées [BRH-131, p. 18, § 6.10.2 c)] | [ADR-0012 §2.9 et §3.5](0012-proximity-payments-cpm.md) : le marchand n'apprend jamais l'identité du payeur | aucune |

**9.11. Ce qui a façonné le frais, une fois trois sources lues ensemble.** La §9.3 a identifié
l'omission à partir de la seule section 8 de `BRH-121`. Deux sources supplémentaires ont
déterminé ce que le champ devait signifier. `BRH-131` interdit à une institution de tolérer que
des marchands imposent des frais additionnels sur les paiements électroniques
[BRH-131, p. 8, § 6.1 p)], de sorte que le frais figurant sur le reçu est un frais supporté par
le marchand plutôt qu'un supplément répercuté sur le payeur, ce qui est la raison pour laquelle
`bearer` rapporte ce qu'a fait l'opérateur et ne peut pas être fixé par un client. Et la BRH
conditionne l'interopérabilité qu'elle promeut à un cadre garantissant, entre autres, « la
transparence des frais » [BRH-PILOT-2026], ce qui est la raison pour laquelle un opérateur qui
ne divulgue rien est déclaré absent sous `payments.fee` plutôt que de renvoyer un champ vide.

**9.12.** Rien dans cette annexe n'affirme qu'un déploiement OpenFSP satisfait la
Circulaire 121. La conformité d'un marchand est une affaire entre le marchand, son prestataire
agréé et l'autorité, et [ADR-0001](0001-architecture-and-scope.md) est explicite : l'éditeur
d'une spécification n'y est pas partie. L'annexe dit quel champ répondrait à quelle exigence,
et c'est tout ce qu'elle dit.

## Références

Citations complètes dans [`references.md`](references.md). Cette ADR est informative, donc
chaque référence est informative.

**ISO 20022.** `ISO20022`, et en son sein `pain.001`, `pain.002`, `pain.013`, `pain.014` et
`camt.053`. `ISO4217` pour les codes de devise et leurs exposants d'unité mineure, dont la
§4.5 dépend.

**Droit et réglementation haïtiens.** `HT-LAW-2012`, `BRH-121`, `BRH-126`, `BRH-131`,
`BRH-PILOT-2026`, tous en §9.

**OpenFSP.** `ADR-0002` gouverne le fil là où ce document et elle divergent (§1.2).

La §2.4 fixe le matériel ISO 20022 contre lequel cette correspondance a été établie, et
*Questions non résolues* consigne que les External Code Sets évoluent trimestriellement alors
que ce document, non.

## Alternatives écartées

**Mettre du XML ISO 20022 sur le fil.** La voie directe vers une revendication de conformité
défendable, et écartée dans [ADR-0001](0001-architecture-and-scope.md) avant que ce document
n'existe. Les définitions de messages portent une structure dimensionnée pour la compensation
interbancaire, dont la plus grande part serait constante ou vide pour chaque paiement de ce
marché, et un marchand intégrant un parcours de paiement la paierait en taille de charge utile,
en outillage, et en temps nécessaire pour comprendre un `GrpHdr`. Tout le pari d'OpenFSP est
que l'adoption dépend d'une surface réduite.

**Adopter les variantes JSON enregistrées par l'ISO.** Plus récentes, et elles suppriment
l'objection du XML tout en conservant les noms d'éléments. Écartées parce qu'elles conservent
la hiérarchie, qui était l'objection réelle, et qu'elles héritent de la cadence de
version de l'autorité d'enregistrement. La correspondance de la §4 en tire le bénéfice, qui est
une relation vérifiable à un vocabulaire partagé, sans en payer le coût.

**Nommer les champs OpenFSP d'après les éléments ISO.** `EndToEndId` au lieu de `reference`,
`InstdAmt` au lieu de `amount`. Superficiellement séduisant, et cela rendrait la §4 presque
triviale. Écarté parce que les noms promettraient alors une sémantique ISO que les champs n'ont
pas, et que la §7 est la liste exacte des endroits où cette promesse serait fausse. Un champ
nommé `DbtrAgt` contenant un identifiant propriétaire est un plus mauvais artefact qu'un champ
nommé `provider` qui n'a jamais prétendu en être un.

**Étendre `failure_reason` pour correspondre aux codes de motif de l'ISO.** Cela transformerait
la §6 d'un tableau de pertes en un tableau d'identités. Écarté, et
[ADR-0003 §7.4.1](0003-payment-lifecycle.md) l'écarte par avance : l'énumération répond à ce
sur quoi un marchand agirait. Plusieurs centaines de codes, dont la plupart ne seront jamais
rapportés par aucun opérateur haïtien, donneraient aux clients une vaste surface à traiter en
échange d'une fidélité que personne n'a demandée.

**Écrire ceci comme une ADR de la voie Standards.** Cela rendrait la correspondance
contraignante et testable. Écarté parce qu'une correspondance contraignante ferait des
publications de jeux de codes de l'ISO une source de ruptures de compatibilité pour OpenFSP,
ce qui est la queue qui remue le chien, et que les §7 et §8 existent pour consigner une
divergence honnête. Un document dont le contenu principal est une liste d'endroits où deux
modèles diffèrent ne peut pas raisonnablement exiger la conformité aux deux.

**Ne rien dire et laisser l'affirmation d'ADR-0001 sans appui.** L'état antérieur à ce
document. Il vaut la peine de le nommer comme une alternative, parce que c'est ce que la
plupart des projets choisissent, et que les deux trouvailles des §3.4 et §9.3 sont ce
que cela aurait coûté.

## Questions non résolues

**Jusqu'où `pain.013` et `pain.001` divergent réellement sous le niveau de la transaction.**
La §4.1 énonce les tableaux contre `pain.013` et note qu'un lecteur de `pain.001` substitue un
nom d'élément. Cette affirmation est faite au niveau de détail qu'atteignent ces tableaux, et
elle n'a pas été vérifiée élément par élément contre les schémas complets. Un implémenteur
d'exportateur le découvrirait le premier, et une correction ici serait un erratum plutôt qu'une
refonte.

**Faut-il scinder `limit_exceeded` ?** §6.4. Un plafond d'opérateur et un plafond réglementaire
ont des conséquences différentes pour un marchand, ce qui est le critère propre de
[ADR-0003](0003-payment-lifecycle.md) pour décider qu'une valeur mérite d'exister. Que ce
soit la correspondance qui l'ait révélé plaide en faveur de cet exercice.

**Faut-il adopter plus complètement le vocabulaire des frais de l'ISO ?** Le frais de
[ADR-0002 §8](0002-core-data-model.md) distingue deux porteurs là où `ChrgBr` en distingue
davantage, et porte un chiffre là où `ChrgsInf` peut en détailler plusieurs. C'est assez pour
le reçu de la section 8 de `BRH-121` et insuffisant pour un export fidèle. L'élargir importerait
un vocabulaire qu'aucun opérateur de ce marché ne renseigne actuellement.

**Quelle publication des External Code Sets fixer.** La §2.4 laisse cela imprécis. Fixer une
publication trimestrielle rend vérifiables les codes de motif de la §6 et périme ce document
selon un calendrier ; ne rien fixer laisse la §6.6 incapable de dire à quelle date « aucun code
n'existe ». Le second inconvénient est le pire, et le remède est probablement une note datée
sur la §6 plutôt qu'une fixation sur l'ensemble du document.

**Un exportateur a-t-il sa place dans le projet ?** Ce document est ce à partir de quoi on en
bâtirait un, et en bâtir un prouverait la correspondance de la seule manière qui compte
vraiment. C'est aussi un logiciel sans utilisateur tant qu'une institution ne le demande pas,
et le projet a des choses plus rares à financer en effort.

## Implémentation de référence

Aucune à ce jour, et *Questions non résolues* consigne pourquoi un exportateur n'est pas
manifestement la prochaine bonne chose à construire.

## Errata

Aucun.
