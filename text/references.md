# Références

Chaque source qu'une ADR cite, avec une clé stable, pour qu'une citation soit vérifiable
plutôt que décorative.

Une ADR cite une source par sa clé entre crochets, `[BRH-126]`, et liste les clés qu'elle
emploie dans sa propre section *Références*. Ce fichier porte la citation complète une seule
fois, de sorte qu'une correction se fait à un endroit et corrige avec elle toutes les ADR qui
s'y appuient.

Les clés sont permanentes. Une source remplacée garde sa clé et reçoit une note ; elle n'est
jamais supprimée, pour la même raison qu'une ADR rejetée ne l'est jamais.

## Comment citer

Les références **normatives** sont celles qu'un implémenteur doit lire pour implémenter
correctement. Les lire n'est pas facultatif, et une implémentation qui en ignore une n'est pas
conforme.

Les références **informatives** expliquent pourquoi une décision a été prise, ou consignent
d'où vient une affirmation. Une implémentation peut être correcte sans jamais en ouvrir une.

Une ADR de la voie Standards tient les deux listes séparées. Une ADR informative ou de
processus n'a que des références informatives, puisqu'elle n'impose rien.

Citer une source oblige l'ADR citante à être exacte sur ce que la source dit, y compris là où
la source est en désaccord avec OpenFSP. Une citation qui supprime la part d'une source qui
joue contre le projet est un défaut, et
[ADR-0001](0001-architecture-and-scope.md) contient au moins un exemple délibéré de la
pratique inverse.

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
| `ISO20022` | ISO 20022, *Financial services: universal financial industry message scheme*, International Organization for Standardization. Message definitions referenced individually: `pain.001`, `pain.002`, `pain.013`, `pain.014`, `camt.053`. |
| `E164` | ITU-T Recommendation E.164, *The international public telecommunication numbering plan*, International Telecommunication Union. |
| `OAS31` | *OpenAPI Specification*, version 3.1, OpenAPI Initiative. |

### Travaux en cours

| Clé | Référence |
|---|---|
| `IETF-IDEM` | J. Mehta *et al.*, *The Idempotency-Key HTTP Header Field*, draft-ietf-httpapi-idempotency-key-header-07, HTTPAPI Working Group, IETF, 15 October 2025. https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ |

Un Internet-Draft n'est pas une norme publiée et peut encore changer. Il est cité comme
travail en cours, jamais comme acquis. [ADR-0004](0004-idempotency-and-retries.md) consigne où OpenFSP
s'accorde avec lui et où il ne s'accorde pas.

---

## Droit et réglementation haïtiens

Le cadre principal. Les titres sont donnés en français, langue dans laquelle ils sont publiés.

| Clé | Référence |
|---|---|
| `HT-LAW-2012` | *Loi portant sur les banques et autres institutions financières* [Law on banks and other financial institutions], voted 14 May 2012, published in *Le Moniteur*, special issue no 4, 20 July 2012. 65 pages. https://www.brh.ht/wp-content/uploads/2018/08/loi_bancaire_2012.pdf |
| `HT-AML-2023` | *Décret sur le blanchiment de capitaux, le financement du terrorisme et le financement de la prolifération des armes de destruction massive*, *Le Moniteur*, special no 12, 4 May 2023. Not yet obtained; cited only through `EF-AYITI-2026`. |
| `BRH-121` | Banque de la République d'Haïti, *Circulaire no 121 relative aux services de paiement électronique*, 6 December 2021, signed Jean Baden Dubois, Governor. 46 pages. |
| `BRH-126` | Banque de la République d'Haïti, *Circulaire no 126 aux institutions financières* [IT security], 13 January 2022, in force 1 February 2022, signed Jean Baden Dubois, Governor. 5 pages. |
| `BRH-131` | Banque de la République d'Haïti, *Circulaire CIR. : BRH/IF/2026/131 aux institutions financières, relative à la protection des consommateurs de produits et services financiers*, 6 February 2026. 52 pages. |
| `BRH-DI-0011` | Banque de la République d'Haïti, *Le système de paiement en Haïti*, information document MAE/BRH DI-0011, August 2024. 10 pages. https://www.brh.ht/wp-content/uploads/Le-systeIme-de-Paiment-en-Haiti-02.pdf |
| `BRH-CR7` | Banque de la République d'Haïti, *Cahier de recherche* no 7, BRH/MAE CR-007, August 2025. 119 pages. A collection of three separate studies, each separately paginated; cite the study, not only the volume. https://www.brh.ht/wp-content/uploads/Cahier-de-recherche-No-7.13.3.pdf |
| `BRH-PILOT-2026` | R. Gabriel, *Piloter les systèmes de paiement et l'innovation pour accélérer la modernisation financière en Haïti*, Banque de la République d'Haïti, 9 September 2026. https://www.brh.ht/piloter-les-systemes-de-paiement-et-linnovation-pour-accelerer-la-modernisation-financiere-en-haiti/ |

### Notes sur la citation de ces sources

**`BRH-121` emploie des sections numérotées, pas des articles.** Sa propre section 20 d)
renvoie à « la section 19 », et le mot *article* est réservé aux lois. Une citation disant
« Article 5 de la circulaire 121 » est fausse.

**`BRH-121` et `BRH-126` sont des numérisations sans couche de texte.** Chaque citation qui en
est tirée dans ce projet a été transcrite en lisant les images des pages. Une citation
réutilisée ailleurs devrait être vérifiée contre l'original.

**`HT-LAW-2012` porte deux dates.** Le 14 mai 2012 est le vote, le 20 juillet 2012 la
publication au *Moniteur*. Les circulaires disent « la loi du 14 mai 2012 » ; une bibliographie
donne les deux.

**La chaîne légale.** `BRH-126` dérive des articles 83 et 161 de `HT-LAW-2012`, et
l'article 83(10) est le pouvoir précis d'édicter des règles sur « les mécanismes de contrôle
et de sécurité dans le domaine de l'informatique ». `BRH-131` dérive des articles 83, 192 et
193, et de `BRH-121`. Citer une circulaire sans sa base légale laisse le lecteur incapable de
voir jusqu'où elle porte.

---

## Organismes internationaux de politique et de normalisation

| Clé | Référence |
|---|---|
| `CPMI-PAFI-2016` | Committee on Payments and Market Infrastructures and World Bank Group, *Payment aspects of financial inclusion*, Bank for International Settlements, April 2016. https://www.bis.org/cpmi/publ/d144.htm |
| `CPMI-PAFI-2020` | Committee on Payments and Market Infrastructures and World Bank Group, *Payment aspects of financial inclusion in the fintech era*, Bank for International Settlements, April 2020. ISBN 978-92-9259-346-9 (online). 79 pages. https://www.bis.org/cpmi/publ/d191.pdf |
| `CPMI-PFMI-2012` | Committee on Payments and Market Infrastructures, *Principles for financial market infrastructures*, Bank for International Settlements, April 2012. Cited by `BRH-PILOT-2026`. |
| `AFI-2017` | Alliance for Financial Inclusion, *National Retail Payment Systems to Support Financial Inclusion*, Guideline Note no 29, August 2017. Cited by `BRH-PILOT-2026`. |
| `GSMA-MMAPI` | GSMA, *Mobile Money API Specification*, version 1.2, GSMA Mobile for Development. https://developer.mobilemoneyapi.io/ |
| `FINDEX-2021` | World Bank, *Global Findex Database 2021*. The Haitian figure used in this project is quoted at second hand through `BRH-PILOT-2026`. |
| `FINSCOPE-2023` | *FinScope MPME Haïti 2023*. Source of the 14 per cent figure for banked micro, small and medium enterprises, quoted at second hand through `BRH-PILOT-2026`. Not yet obtained. |

**`CPMI-PAFI-2020` est la référence à lire en premier.** Son paragraphe 146, page 53, énonce le
problème que cette spécification existe pour traiter et, dans la même phrase, l'objection la
plus forte à la manière dont elle le traite. [ADR-0001](0001-architecture-and-scope.md) cite
les deux moitiés.

---

## Sources régionales et sectorielles

| Clé | Référence |
|---|---|
| `EF-AYITI-2026` | C. Vaval, C. R. Nau and J. F. Saint-Paul, *Fintech, stablecoins et souveraineté financière : repenser l'architecture de contrôle des flux en Haïti*, Ekosistèm Fintèk Ayiti, analysis memo, August 2026. 29 pages. |
| `EF-AYITI-121` | Ekosistèm Fintèk Ayiti, *Analyse et recommandations sur la Circulaire 121 pour les FSP en Haïti*, analytical report, April 2026. 22 pages. https://www.linkedin.com/feed/update/urn:li:activity:7493015264590995456/ |
| `MOJALOOP` | Mojaloop Foundation, *Mojaloop*, open-source software for interoperable digital payments. Underlies `MOWALI`. |

`EF-AYITI-2026` is the position of the organised Haitian fintech industry association, not a
peer-reviewed study, and its authors have an interest in the sector they analyse. It is cited
for what it is: what the industry says about its own market, which is evidence of a particular
kind and not of another.

`EF-AYITI-121` is the same association's analysis of Circular 121, addressed to the regulator.
The same caveat applies, and the same value: it is what the industry tells its supervisor about
the gap this specification fills.

### Initiatives africaines d'interopérabilité

These are the comparators. All four are documented in `CPMI-PAFI-2020`, Box R, page 54, and
they are cited in this project for a reason that survives the details: **every one of them
operates at the switch or hub layer, and none of them is a merchant integration protocol.**

| Clé | Initiative | Ce qu'elle fait |
|---|---|---|
| `NCS` | Nigeria Central Switch | Lets mobile money operators interoperate with banks and other financial institutions. Mobile inter-scheme transactions grew 470 per cent by volume in 2019. |
| `GH-MMI` | Ghana Mobile Money Interoperability platform | Direct transfer of funds from one mobile money wallet to another across networks. Volume grew 317 per cent between 2018 and 2019. |
| `BCEAO-WAEMU` | BCEAO, with the African Development Bank and the Bill & Melinda Gates Foundation | A project to make mobile money solutions interoperable across the eight WAEMU countries, aiming at a common payments ecosystem. |
| `MOWALI` | Mowali, launched by MTN and Orange with GSMA support | An industry-owned and industry-governed payments hub for mobile money, built on `MOJALOOP`, open to any mobile money provider in Africa as well as banks and money transfer operators. |

**Pourquoi ce tableau mérite sa place.** Le transfert de portefeuille à portefeuille entre
réseaux, et l'acceptation des cartes entre institutions, sont les problèmes que ces initiatives
résolvent. Un marchand qui détient une intégration par opérateur est un autre problème, à une
autre couche, et aucune d'elles ne le résout. `BRH-DI-0011` fait le même constat sur le
commutateur haïtien sans le vouloir : sa note 10, page 10, définit l'interopérabilité que livre
le processeur national comme une carte de débit émise par l'institution A utilisable aux
terminaux de l'institution B.

**`MOWALI` est aussi le précédent de gouvernance.** Un hub détenu et gouverné par l'industrie,
bâti sur une plateforme libre, est proche de ce que décrit
[GOVERNANCE.md](https://github.com/openfspht/openfsp/blob/main/GOVERNANCE.md), et plus proche que tout ce qu'on trouve dans les réseaux de
cartes.

---

## Sources délibérément non citées

Consigner ce qui a été examiné puis écarté est aussi utile ici que dans une ADR.

Plusieurs articles de revue sur la sécurité des paiements et la tokenisation ont été examinés
et non retenus. Ils reprennent des chiffres de rapports sectoriels sans apport propre, et leur
sujet, la tokenisation des cartes et la détection de fraude en temps réel, est hors de ce que
fait cette spécification. Là où une affirmation de sécurité est nécessaire, `RFC9421`,
`RFC9530` et `BRH-126` sont des sources directes et de meilleures sources.

Un article examiné contenait un texte qui n'était pas de l'anglais cohérent. Il n'est pas
cité, et l'épisode est la raison pour laquelle ce fichier consigne une appréciation à côté de
chaque source plutôt qu'une citation nue : une bibliographie dont les entrées n'ont pas été
lues est un passif plutôt qu'un actif.
