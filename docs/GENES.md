# The ONC Gene Pool

ONC investigates 30 genes with known or emerging roles in pediatric cancers. As
each is investigated it leaves the active pool; when the pool empties it resets
for a fresh pass with new scoring. The authoritative list lives in
`data/genes.json`.

| # | Gene | Primary pediatric cancer | Rationale |
|---|------|--------------------------|-----------|
| 1 | MYCN | neuroblastoma (high-risk) | amplification drives the most aggressive disease |
| 2 | ALK | neuroblastoma | activating mutations; actionable kinase |
| 3 | EWSR1-FLI1 | Ewing sarcoma | the defining fusion oncogene |
| 4 | SMARCB1 | rhabdoid tumors / ATRT | biallelic loss defines the cancer |
| 5 | H3F3A | DIPG / pediatric high-grade glioma | H3 K27M oncohistone |
| 6 | TP53 | many (Li-Fraumeni) | the guardian of the genome |
| 7 | RB1 | retinoblastoma | the original tumor-suppressor story |
| 8 | BRAF | pediatric low-grade glioma | KIAA1549-BRAF fusion / V600E; druggable |
| 9 | WT1 | Wilms tumor | classic Wilms driver |
| 10 | DICER1 | pleuropulmonary blastoma | miRNA processing; DICER1 syndrome |
| 11 | PAX3-FOXO1 | alveolar rhabdomyosarcoma | the defining fusion oncogene |
| 12 | PHOX2B | neuroblastoma | germline predisposition gene |
| 13 | CTNNB1 | WNT medulloblastoma / Wilms | beta-catenin activation |
| 14 | MYC | group 3 medulloblastoma | amplification, poor prognosis |
| 15 | AURKA | neuroblastoma | stabilises MYCN; druggable kinase |
| 16 | CDK4 | multiple pediatric solid tumors | cell-cycle driver; CDK4/6 inhibitors exist |
| 17 | NTRK1 | infantile fibrosarcoma | TRK fusion; TRK inhibitors approved |
| 18 | PDGFRA | DIPG | amplification / mutation in brainstem glioma |
| 19 | ACVR1 | DIPG | recurrent activating mutation |
| 20 | PPM1D | brainstem glioma | truncating mutations stabilise the protein |
| 21 | ATRX | neuroblastoma / pediatric glioma | chromatin remodeller loss |
| 22 | TERT | neuroblastoma | rearrangements activate telomerase |
| 23 | MYB | pediatric low-grade glioma | MYB / MYBL1 alterations |
| 24 | FGFR1 | pediatric glioma | activating alterations; druggable |
| 25 | SMARCA4 | rhabdoid tumors / SCCOHT | SWI/SNF loss |
| 26 | STAG2 | Ewing sarcoma | cohesin loss; adverse marker |
| 27 | GLI2 | SHH medulloblastoma | hedgehog pathway effector |
| 28 | PTCH1 | SHH medulloblastoma | hedgehog receptor loss |
| 29 | IKZF1 | B-cell ALL | deletion drives high-risk disease |
| 30 | FLT3 | pediatric AML | activating ITD; druggable |

## Adding a gene

Append to `data/genes.json` and add a matching evidence row to
`data/sample_evidence.json` (see [CONTRIBUTING](../CONTRIBUTING.md)). The symbol
is matched case-insensitively.
