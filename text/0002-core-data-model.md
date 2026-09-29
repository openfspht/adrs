# ADR-0002 : Modèle de données

- Statut : Proposée
- Date : 2026-08-17
- Règles : [spec/modele-de-donnees.md](../spec/modele-de-donnees.md)

## Contexte

Les échecs d'interopérabilité de paiement tiennent surtout aux primitives : arrondi, fuseau
horaire, format de téléphone local, identifiants ambigus. Ils sont invisibles dans le cas
courant et coûteux dans le cas rare, et deviennent des ruptures de compatibilité dès qu'une
autre spécification en dépend.

## Décision

- **Montant** : entier en centimes de gourde, borné à ±(2⁵³ - 1) pour rester exact dans les
  analyseurs JSON en double précision. Jamais de flottant, aucun arrondi.
- **Devise** : HTG uniquement. Le champ `currency` est conservé, fixé à `"HTG"`, pour qu'une
  devise supplémentaire puisse être ajoutée sans changer le format.
- **Téléphone** : E.164 uniquement. La conversion depuis un format national relève du SDK.
- **Identifiants** : `ResourceId` opaque et non devinable (UUIDv7 recommandé), `Reference`
  choisie par le marchand et unique par propriétaire, `ProviderReference` opaque et
  facultative.
- **Horodatage** : RFC 3339 en UTC avec `Z`. Haïti applique l'heure d'été ; un horodatage
  local est ambigu une heure par an.
- **Données de l'opérateur** : montants convertis sans flottant, numéros convertis en E.164,
  horodatages sans décalage lus à l'heure de Port-au-Prince. MonCash et NatCash envoient des
  décimaux, des numéros sans `+` et des dates sans fuseau.
- **Frais** (`Fee`) : montant et partie qui l'a supporté. Absent signifie « non connu ».
- **JSON** : champs inconnus ignorés en réponse, rejetés en requête : une faute de frappe sur
  `amount` ne doit pas produire un paiement d'un autre montant.
- Les formes suivent ISO 20022 comme dictionnaire ; la correspondance est dans
  [ISO 20022](../spec/iso-20022.md).

## Conséquences

- L'implémentation correcte est l'implémentation évidente : pas d'analyse décimale.
- L'unicité de `Reference` est partitionnée par propriétaire : une passerelle multi-marchands
  ne révèle pas l'activité d'un marchand à un autre.
- `Fee` permet de produire le reçu exigé par BRH-121 §8. `bearer` vaut `payer` seulement
  quand l'opérateur facture le payeur : BRH-131 interdit la surcharge marchande.
- La seule donnée personnelle est le numéro de téléphone.
- Modifier un type après acceptation est une rupture de compatibilité pour toute la
  spécification.

## Alternatives écartées

- **Montant en chaîne décimale** : chaque client doit analyser des décimaux correctement.
- **Montant flottant** : inexact par construction.
- **Chaîne unique `"HTG 1250.00"`** : un analyseur par implémentation.
- **Multi-devise (HTG et USD)** : imposerait des règles de conversion et de comparaison entre
  devises, sans besoin sur le marché visé.
- **Supprimer le champ `currency`** : ajouter une devise deviendrait une rupture de format.
- **Formats téléphoniques nationaux normalisés côté serveur** : l'ambiguïté est indétectable.
- **ULID imposé** : l'identifiant étant opaque, le format interne n'a pas d'enjeu
  d'interopérabilité.
- **Horodatage epoch** : unité non autodescriptive, illisible dans les journaux.
- **`camelCase`** : écarté pour la cohérence avec les API de paiement courantes.

## Questions ouvertes

- Réutilisation d'une même `Reference` chez deux opérateurs.
- Rendre obligatoire le préfixe de type des identifiants.
- Limites des métadonnées, fixées sans mesure.
- Convention d'affichage des montants pour les SDK.
