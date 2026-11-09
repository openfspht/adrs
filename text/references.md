# Références

Je cite les sources des ADR et de la spécification sous une clé (`BRH-126`) ; la citation
complète n'apparaît qu'ici.

Les clés sont permanentes. Une source remplacée garde sa clé et reçoit une note ; elle n'est
jamais supprimée.

## Comment citer

- **Normative** : nécessaire pour implémenter ; une implémentation qui en ignore une n'est pas
  conforme.
- **Informative** : justifie une décision ou source une affirmation.

Un document normatif peut citer les deux ; un document informatif ou de processus, seulement
des références informatives.

Quand je cite une source, j'en rends aussi la part qui contredit OpenFSP
(exemple : [ADR-0001](0001-architecture-and-scope.md), avertissement du CPMI).

---

## Normes techniques

| Clé | Référence |
|---|---|
| `RFC2119` | S. Bradner, *Key words for use in RFCs to Indicate Requirement Levels*, BCP 14, RFC 2119, IETF, March 1997. |
| `RFC8174` | B. Leiba, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*, BCP 14, RFC 8174, IETF, May 2017. |
| `RFC3339` | G. Klyne and C. Newman, *Date and Time on the Internet: Timestamps*, RFC 3339, IETF, July 2002. |
| `RFC6901` | P. Bryan, K. Zyp and M. Nottingham, *JavaScript Object Notation (JSON) Pointer*, RFC 6901, IETF, April 2013. |
| `RFC8615` | M. Nottingham, *Well-Known Uniform Resource Identifiers (URIs)*, RFC 8615, IETF, May 2019. |
| `RFC8785` | A. Rundgren, B. Jordan and S. Erdtman, *JSON Canonicalization Scheme (JCS)*, RFC 8785, IETF, June 2020. |
| `RFC8941` | M. Nottingham and P-H. Kamp, *Structured Field Values for HTTP*, RFC 8941, IETF, February 2021. |
| `RFC9110` | R. Fielding, M. Nottingham and J. Reschke (eds), *HTTP Semantics*, STD 97, RFC 9110, IETF, June 2022. |
| `RFC9421` | A. Backman, J. Richer and M. Sporny, *HTTP Message Signatures*, RFC 9421, IETF, February 2024. |
| `RFC9457` | M. Nottingham, E. Wilde and S. Dalal, *Problem Details for HTTP APIs*, RFC 9457, IETF, July 2023. |
| `RFC9530` | R. Polli and L. Pardue, *Digest Fields*, RFC 9530, IETF, February 2024. |
| `RFC9562` | K. Davis, B. Peabody and P. Leach, *Universally Unique IDentifiers (UUIDs)*, RFC 9562, IETF, May 2024. |
| `ISO4217` | ISO 4217, *Currency codes*, International Organization for Standardization. |
| `E164` | ITU-T Recommendation E.164, *The international public telecommunication numbering plan*, International Telecommunication Union. |
| `OAS31` | *OpenAPI Specification*, version 3.1, OpenAPI Initiative. |

### Travaux en cours

| Clé | Référence |
|---|---|
| `IETF-IDEM` | J. Mehta *et al.*, *The Idempotency-Key HTTP Header Field*, draft-ietf-httpapi-idempotency-key-header-07, HTTPAPI Working Group, IETF, 15 October 2025. https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ |

Je le cite comme travail en cours. Accords et écarts d'OpenFSP :
[ADR-0006](0006-gateway-http-api-payments.md).

---

## Droit et réglementation haïtiens

Titres dans leur langue de publication.

| Clé | Référence |
|---|---|
| `HT-LAW-2012` | *Loi portant sur les banques et autres institutions financières* [Law on banks and other financial institutions], voted 14 May 2012, published in *Le Moniteur*, special issue no 4, 20 July 2012. 65 pages. https://www.brh.ht/wp-content/uploads/2018/08/loi_bancaire_2012.pdf |
| `HT-AML-2023` | *Décret sur le blanchiment de capitaux, le financement du terrorisme et le financement de la prolifération des armes de destruction massive*, *Le Moniteur*, special no 12, 4 May 2023. Non obtenu ; cité seulement par `EF-AYITI-2026`. |
| `BRH-121` | Banque de la République d'Haïti, *Circulaire no 121 relative aux services de paiement électronique*, 6 December 2021, signed Jean Baden Dubois, Governor. 46 pages. |
| `BRH-126` | Banque de la République d'Haïti, *Circulaire no 126 aux institutions financières* [IT security], 13 January 2022, in force 1 February 2022, signed Jean Baden Dubois, Governor. 5 pages. |
| `BRH-131` | Banque de la République d'Haïti, *Circulaire CIR. : BRH/IF/2026/131 aux institutions financières, relative à la protection des consommateurs de produits et services financiers*, 6 February 2026. 52 pages. |
| `BRH-DI-0011` | Banque de la République d'Haïti, *Le système de paiement en Haïti*, information document MAE/BRH DI-0011, August 2024. 10 pages. https://www.brh.ht/wp-content/uploads/Le-systeIme-de-Paiment-en-Haiti-02.pdf |
| `BRH-CR7` | Banque de la République d'Haïti, *Cahier de recherche* no 7, BRH/MAE CR-007, August 2025. 119 pages. Recueil de trois études paginées séparément ; citer l'étude, pas seulement le volume. https://www.brh.ht/wp-content/uploads/Cahier-de-recherche-No-7.13.3.pdf |
| `BRH-PILOT-2026` | R. Gabriel, *Piloter les systèmes de paiement et l'innovation pour accélérer la modernisation financière en Haïti*, Banque de la République d'Haïti, 9 September 2026. https://www.brh.ht/piloter-les-systemes-de-paiement-et-linnovation-pour-accelerer-la-modernisation-financiere-en-haiti/ |

### Notes sur la citation de ces sources

**`BRH-121` est divisée en sections, pas en articles** (sa section 20 d) renvoie à « la
section 19 » ; *article* est réservé aux lois). Citer « BRH-121 5 », jamais « article 5 ».

**`BRH-121` et `BRH-126` sont des numérisations sans couche de texte.** J'ai transcrit
les citations depuis les images ; à vérifier contre l'original avant réemploi.

**`HT-LAW-2012` porte deux dates** : vote le 14 mai 2012 (date citée par les circulaires),
publication au *Moniteur* le 20 juillet 2012.

**La chaîne légale.** `BRH-126` dérive des articles 83 et 161 de `HT-LAW-2012`, et
l'article 83(10) est le pouvoir précis d'édicter des règles sur « les mécanismes de contrôle
et de sécurité dans le domaine de l'informatique ». `BRH-131` dérive des articles 83, 192 et
193, et de `BRH-121`. Citer une circulaire avec sa base légale.

---

## Organismes internationaux de politique et de normalisation

| Clé | Référence |
|---|---|
| `CPMI-PAFI-2016` | Committee on Payments and Market Infrastructures and World Bank Group, *Payment aspects of financial inclusion*, Bank for International Settlements, April 2016. https://www.bis.org/cpmi/publ/d144.htm |
| `CPMI-PAFI-2020` | Committee on Payments and Market Infrastructures and World Bank Group, *Payment aspects of financial inclusion in the fintech era*, Bank for International Settlements, April 2020. ISBN 978-92-9259-346-9 (online). 79 pages. https://www.bis.org/cpmi/publ/d191.pdf |
| `CPMI-PFMI-2012` | Committee on Payments and Market Infrastructures, *Principles for financial market infrastructures*, Bank for International Settlements, April 2012. Cité par `BRH-PILOT-2026`. |
| `AFI-2017` | Alliance for Financial Inclusion, *National Retail Payment Systems to Support Financial Inclusion*, Guideline Note no 29, August 2017. Cité par `BRH-PILOT-2026`. |
| `GSMA-MMAPI` | GSMA, *Mobile Money API Specification*, version 1.2, GSMA Mobile for Development. https://developer.mobilemoneyapi.io/ |
| `FINDEX-2021` | World Bank, *Global Findex Database 2021*. Le chiffre haïtien utilisé dans ce projet est cité de seconde main par `BRH-PILOT-2026`. |
| `FINSCOPE-2023` | *FinScope MPME Haïti 2023*. Source du chiffre de 14 % de micro, petites et moyennes entreprises bancarisées, cité de seconde main par `BRH-PILOT-2026`. Non obtenu. |

**`CPMI-PAFI-2020`, 146, page 53** : énonce la question à laquelle OpenFSP répond et, dans la même
phrase, une objection à une passerelle. [ADR-0001](0001-architecture-and-scope.md)
cite les deux.

---

## Sources régionales et sectorielles

| Clé | Référence |
|---|---|
| `EF-AYITI-2026` | C. Vaval, C. R. Nau and J. F. Saint-Paul, *Fintech, stablecoins et souveraineté financière : repenser l'architecture de contrôle des flux en Haïti*, Ekosistèm Fintèk Ayiti, analysis memo, August 2026. 29 pages. |
| `EF-AYITI-121` | Ekosistèm Fintèk Ayiti, *Analyse et recommandations sur la Circulaire 121 pour les FSP en Haïti*, analytical report, April 2026. 22 pages. https://www.linkedin.com/feed/update/urn:li:activity:7493015264590995456/ |
| `MOJALOOP` | Mojaloop Foundation, *Mojaloop*, open-source software for interoperable digital payments. Base de `MOWALI`. |

`EF-AYITI-2026` et `EF-AYITI-121` (ce dernier adressé au régulateur) expriment la position de
l'association professionnelle des fintech haïtiennes, intéressée au secteur ; pas d'évaluation
par les pairs. Je les cite comme position de l'industrie.

### Initiatives africaines d'interopérabilité

Documentées dans `CPMI-PAFI-2020`, encadré R, page 54.

| Clé | Initiative | Ce qu'elle fait |
|---|---|---|
| `NCS` | Nigeria Central Switch | Permet aux opérateurs de mobile money d'interopérer avec les banques et les autres institutions financières. Volume des transactions mobiles entre systèmes en hausse de 470 % en 2019. |
| `GH-MMI` | Ghana Mobile Money Interoperability platform | Transfert direct de fonds d'un portefeuille de mobile money à un autre, entre réseaux. Volume en hausse de 317 % entre 2018 et 2019. |
| `BCEAO-WAEMU` | BCEAO, avec la Banque africaine de développement et la Fondation Bill & Melinda Gates | Projet d'interopérabilité des solutions de mobile money entre les huit pays de l'UEMOA, en vue d'un écosystème de paiement commun. |
| `MOWALI` | Mowali, lancée par MTN et Orange avec le soutien de la GSMA | Plateforme d'interconnexion de paiement pour le mobile money, détenue et gouvernée par l'industrie, construite sur `MOJALOOP`, ouverte à tout fournisseur de mobile money en Afrique ainsi qu'aux banques et aux opérateurs de transfert d'argent. |

Ces initiatives traitent le transfert entre portefeuilles de réseaux différents et
l'acceptation des cartes entre institutions, pas l'intégration par opérateur chez le marchand.
Même constat pour le commutateur haïtien : `BRH-DI-0011`, note 10, page 10, définit
l'interopérabilité du processeur national comme une carte de débit de l'institution A
utilisable aux terminaux de l'institution B.

**`MOWALI`, précédent de gouvernance** : plateforme d'interconnexion détenue et gouvernée par
ses participants, sur logiciel libre ; modèle comparable à celui de
[GOVERNANCE.md](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md).

---

## Sources que je ne cite pas

- Articles de revue sur la sécurité des paiements et la tokenisation : reprennent des chiffres
  sectoriels sans apport propre ; sujet (tokenisation des cartes, détection de fraude en temps
  réel) hors périmètre. Je cite plutôt les sources directes : `RFC9421`, `RFC9530`, `BRH-126`.
