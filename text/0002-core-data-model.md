# ADR-0002 : Modèle de données

- Date : 2026-08-17
- Règles : [spec/modele-de-donnees.md](../spec/modele-de-donnees.md)

## Contexte

Je fixe d'abord les primitives (arrondi, fuseau horaire, format de téléphone local,
identifiants), qui conditionnent toutes les autres spécifications.

## Décision

Je propose :

- **Montant** : entier en centimes de gourde, borné à ±(2⁵³ - 1) pour rester exact dans les
  analyseurs JSON en double précision. Jamais de flottant, aucun arrondi.
- **Devise** : HTG uniquement. Je conserve le champ `currency`, fixé à `"HTG"`, pour qu'une
  devise supplémentaire puisse être ajoutée sans changer le format.
- **Téléphone** : E.164 uniquement. La conversion depuis un format national relève du SDK.
- **Identifiants** : `ResourceId` opaque et non devinable (UUIDv7 recommandé), `Reference`
  choisie par le marchand et unique par passerelle, `ProviderReference` opaque et
  facultative.
- **Horodatage** : RFC 3339 en UTC avec `Z`. Haïti applique l'heure d'été ; un horodatage
  local est ambigu une heure par an.
- **Données de l'opérateur** : montants convertis sans flottant, numéros convertis en E.164,
  horodatages sans décalage lus à l'heure de Port-au-Prince. MonCash et NatCash envoient des
  montants décimaux et des numéros sans `+` ; MonCash date sans fuseau.
- **Frais** (`Fee`) : montant et partie qui l'a supporté. Absent signifie « non connu ».
- **JSON** : champs inconnus ignorés en réponse, rejetés en requête, pour qu'une faute de
  frappe sur le nom d'un champ facultatif (`expires_at`) ne passe pas en silence.

## Conséquences

- Aucune analyse décimale côté client.
- L'unicité de `Reference` porte sur la passerelle entière, qui sert un seul marchand : deux
  clés du même marchand ne peuvent pas créer deux paiements de même référence.
- `Fee` permet de produire le reçu exigé par BRH-121 8. `bearer` vaut `payer` seulement
  quand l'opérateur facture le payeur : BRH-131 6.1 p) interdit la surcharge
  marchande.
- La seule donnée personnelle définie par le modèle est le numéro de téléphone.
- Modifier un type une fois publié est une rupture de compatibilité pour toute la
  spécification.

## Ce que je n'ai pas retenu

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
- **`camelCase`** : je retiens `lower_snake_case` (spec 2.2).

## Questions ouvertes

- Rendre obligatoire le préfixe de type des identifiants.
- Limites des métadonnées, fixées sans mesure.
- Convention d'affichage des montants pour les SDK.
