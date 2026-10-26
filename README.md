<div align="center">

```
  ____  _   _  _____
 / __ \| \ | |/ ____|
| |  | |  \| | |
| |  | | . ` | |
| |__| | |\  | |____
 \____/|_| \_|\_____|
```

### Finding the genes childhood cancer can't live without.

*An autonomous AI scientist for pediatric cancer genetics. Every prediction hash-locked before testing. Every result published, failures included.*

[![CI](https://github.com/RichardOden/onc/actions/workflows/ci.yml/badge.svg)](https://github.com/RichardOden/onc/actions/workflows/ci.yml)
![status](https://img.shields.io/badge/status-autonomous%20%C2%B7%20continuous-brightgreen)
![focus](https://img.shields.io/badge/focus-pediatric%20oncology-blue)
![evidence](https://img.shields.io/badge/evidence-6%20weighted%20sources-orange)
![transparency](https://img.shields.io/badge/predictions-hash--chained-critical)
![license](https://img.shields.io/badge/license-MIT-lightgrey)

</div>

## The problem

Cancer is the leading cause of death by disease in children past infancy. Each year roughly **400,000 children** worldwide are diagnosed. Survival for common types like acute lymphoblastic leukemia has improved over the decades, but for others like **DIPG, neuroblastoma, and certain sarcomas, outcomes have barely moved.**

Pediatric cancers are *biologically different* from adult cancers:

```
   ADULT TUMORS                        PEDIATRIC TUMORS
   ────────────                        ────────────────
   many mutations          vs.         few mutations
   driven by damage        vs.         driven by development
   decades to form         vs.         arise in young tissue
   large drug pipelines    vs.         systematically overlooked
```

Children aren't small adults. Their tumors aren't either. A genome-scale study of 82 pediatric cancer cell lines found their dependencies are **often distinct from adult cancers**, meaning repurposing adult oncology drugs will not be enough (Dharia et al., *Nature Genetics*, 2021).

Yet children are **less than 1%** of cancer diagnoses, and pediatric research receives a sliver of the funding. The targets that matter most for kids fall through the cracks of adult-focused drug pipelines.

**ONC exists to find those targets.**

## What ONC does

ONC is an autonomous AI scientist that researches pediatric cancer genetics **continuously**. It:

1. **Generates hypotheses** about which genes childhood cancers depend on,
2. **Tests** them against real CRISPR knockout data, and
3. **Publishes every result**, including the failures. Nothing is hidden.

It focuses *exclusively* on pediatric malignancies, scanning CRISPR screens, genetic databases, and trial records for the vulnerabilities adult pipelines miss.

## How ONC works: the research pipeline

Every candidate gene flows through six stages. The order is the whole point: **the prediction is cryptographically locked (stage 3) before any test data can be touched (stage 4).** ONC cannot move the goalposts after seeing the answer.

```
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐
  │ 1 SCREEN │──▶ │ 2 SCORE  │──▶ │ 3 LOCK   │──▶ │ 4 TEST   │──▶ │ 5 VERIFY │──▶ │ 6 RECEIPT │
  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └─────┬─────┘
       │               │               │               │               │                │
  pick a gene     query all 6     SHA-256 hash     evaluate vs     independent      immutable
  from the pool   databases,      the prediction   held-out        judge rules      public record
                  weighted total  (seals it)       CRISPR data     pass / fail      + hash-chain link
                                       │                                │
                                       └──── NO test data visible ──────┘
                                              until the hash is sealed
```

> **Confirmation threshold:** a gene must score a **weighted total above 0.50** *and* a **dependency score above 0.40** to be confirmed as a candidate worth lab attention.

## The scoring engine: six independent lines of evidence

ONC doesn't trust a single signal. It fuses six public evidence sources, each weighted toward *pediatric* relevance:

```
  EVIDENCE SOURCE                WEIGHT   ASKS...
  ─────────────────────────────────────────────────────────────────────────────
  Dependency    DepMap           30%  ███████████████   Does killing this gene kill the cancer cell?
  Genetics      OpenTargets      20%  ██████████        Is the gene genetically linked to the cancer?
                COSMIC
  Novelty       PubMed (inv.)    15%  ███████▌          Is it understudied? (fewer papers → higher)
  Pathways      Reactome         15%  ███████▌          Is it in a cancer-relevant developmental pathway?
  Tractability  ChEMBL           10%  █████             Can a drug physically reach this target?
  Clinical      ClinicalTrials   10%  █████             Existing pediatric trials? (penalized if failed)
  ─────────────────────────────────────────────────────────────────────────────
                                100%
```

**Novelty is inverted on purpose.** Genes drowning in publications are already crowded. ONC is built to *hunt the overlooked*: the gene a child's life may depend on that nobody has had time to chase.

Only pediatric cell lines are scored:

```
  neuroblastoma · Ewing sarcoma · medulloblastoma · ALL
  Wilms tumor · rhabdomyosarcoma · DIPG
```

Adult epithelial cancers are excluded from scoring entirely.

## Transparency by design: the hash chain

This is what makes ONC a *scientist* and not a black box. Every prediction is SHA-256 hashed **before** it can see the evaluation data, and each experiment is chained to the one before it, like a lab notebook that can never be erased or back-dated.

```
     EXPERIMENT #001        EXPERIMENT #002        EXPERIMENT #003
   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │ gene   : MYCN    │   │ gene   : EWSR1   │   │ gene   : SMARCB1 │
   │ predict: DEPEND  │   │ predict: DEPEND  │   │ predict: NO-DEP  │
   │ sealed : 🔒       │   │ sealed : 🔒       │   │ sealed : 🔒       │
   │ prev   : ∅        │   │ prev   : a3f9c1  │   │ prev   : 7c21e0  │
   │ hash   : a3f9c1 ──┼──▶│ hash   : 7c21e0 ──┼──▶│ hash   : e84d55  │
   └──────────────────┘   └──────────────────┘   └──────────────────┘
        genesis              links to #001           links to #002

   Change ANY past prediction → its hash changes → every later link breaks.
   The tampering is instantly visible to anyone who re-computes the chain.
```

- ONC **cannot** retroactively change what it predicted.
- ONC **cannot** judge its own work; an independent verifier rules pass/fail.
- **Failed experiments stay public forever.** There is no retract, no edit, no delete.

A negative result is still a result. Knowing a gene is *not* a dependency saves the next lab from a dead end.

## How ONC helps save lives

ONC does not cure cancer. It does something achievable and valuable: **it narrows the search** so that scarce lab time and funding land on the targets most likely to matter.

```
                         THE FUNNEL ONC NARROWS

   ~20,000 human genes
   ████████████████████████████████████████████████████████████
        │
        │  ONC: pediatric-weighted scoring across 6 evidence sources
        ▼
   ranked candidate dependencies
   ████████████████████████
        │
        │  thresholds: weighted > 0.50  AND  dependency > 0.40
        ▼
   high-confidence, genetically-supported targets
   ██████████
        │
        │  handed to human scientists with the full evidence + hash receipt
        ▼
   wet-lab validation  ─▶  pediatric clinical trial  ─▶  a child who lives
   ███                     █                              ♥
```

Why the genetics weighting matters: drug targets backed by **human genetic evidence are roughly twice as likely to reach clinical approval** (Nelson et al. 2015; replicated by King et al. 2019 and Minikel et al. 2020). ONC systematically scans the pediatric cancer genome for exactly that kind of support, at a pace and scale no human team can match.

## For researchers & clinicians: reading an ONC record

Every confirmed (or rejected) gene is published as a permanent **receipt**. It's designed to be audited, not just trusted:

```
  ┌─ ONC RECEIPT ─────────────────────────────── experiment #0042 ─┐
  │                                                                 │
  │  GENE            MYCN                                           │
  │  CANCER          neuroblastoma (high-risk)                      │
  │  PREDICTION      strong dependency        [sealed before test]  │
  │                                                                 │
  │  SCORE BREAKDOWN                                                │
  │    dependency    0.91   ███████████████████  (DepMap)          │
  │    genetics      0.78   ███████████████▌     (OpenTargets)     │
  │    novelty       0.22   ████▌                (well studied)    │
  │    pathways      0.85   █████████████████    (Reactome)        │
  │    tractability  0.40   ████████             (ChEMBL)          │
  │    clinical      0.60   ████████████         (trials ongoing)  │
  │    ─────────────────────────────────────────────────────────  │
  │    WEIGHTED      0.73   ▶ CONFIRMED (>0.50 and dep >0.40)       │
  │                                                                 │
  │  VERIFIED BY     independent judge  ✓ PASS                      │
  │  PREDICTION HASH a3f9c1...   PREV e84d55...                     │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
```

Anyone can re-compute the hash chain from the public log and confirm no record was altered after the fact. The evidence, the weights, the threshold, and the verdict are all on the table.

## The gene pool

ONC investigates 30 genes with known or emerging roles in pediatric cancers. As each is studied it leaves the active pool; when the pool empties, it resets for a fresh pass with new scoring.

| Gene | Primary pediatric cancer | Why it's on the board |
|------|--------------------------|-----------------------|
| **MYCN** | Neuroblastoma (high-risk) | Amplification drives the most aggressive disease |
| **ALK** | Neuroblastoma | Activating mutations; actionable kinase |
| **EWSR1-FLI1** | Ewing sarcoma | The defining fusion oncogene |
| **SMARCB1** | Rhabdoid tumors / ATRT | Loss defines the cancer |
| **H3F3A** | DIPG / pediatric glioma | H3 K27M "oncohistone" |
| **TP53** | Many (Li-Fraumeni) | The guardian of the genome |
| **RB1** | Retinoblastoma | The original tumor-suppressor story |
| **BRAF** | Pediatric low-grade glioma | Fusion / V600E; druggable |
| **WT1** | Wilms tumor (kidney) | Classic Wilms driver |
| **DICER1** | Pleuropulmonary blastoma | miRNA-processing; DICER1 syndrome |

*...and 20 more.*

## What ONC is and is not

- ✅ A continuous, transparent **hypothesis-prioritization engine** for pediatric cancer targets.
- ✅ An **auditable record** of predictions and outcomes, built to be checked.
- ❌ **Not** a replacement for laboratory science. It narrows the search; the bench confirms.
- ❌ **Not** a medical device or clinical advice. It informs researchers deciding what to pursue next.

> The goal is simple: **find what childhood cancer can't live without.**

## Run it yourself

ONC runs fully offline against a bundled evidence fixture, so a full pass over the gene pool needs no network access or API keys:

```bash
git clone https://github.com/RichardOden/onc.git
cd onc
pip install -e ".[dev]"

onc list-genes            # show the active gene pool
onc run                   # score every gene, verify, print the hash chain
onc run --gene MYCN       # run a single gene
onc run --out run.chain.json
onc chain verify run.chain.json
```

Example output:

```
  MYCN       weighted=0.69 dep=0.91  CONFIRMED  verify=PASS  hash=394d7c5b73
  RB1        weighted=0.48 dep=0.55  rejected   verify=FAIL  hash=4905b6c2bf
  ...
  30 genes · 22 confirmed · 26/30 verified · chain intact: True
```

The four FAIL verdicts are kept on purpose: ONC publishes the experiments it gets wrong.

## Repository layout

```
onc/
├── onc/                     the package
│   ├── genes.py             30-gene pediatric pool (resettable)
│   ├── scoring.py           weights + two-threshold confirmation rule
│   ├── hashchain.py         SHA-256 sealing + tamper-evident chain
│   ├── verify.py            the independent verifier
│   ├── pipeline.py          Screen→Score→Lock→Test→Verify→Receipt
│   ├── cli.py               the `onc` command
│   └── sources/             six evidence-source adapters (+ offline)
├── data/                    gene pool + offline evidence fixture
├── docs/                    METHODOLOGY · ARCHITECTURE · HASH_CHAIN · GENES
└── tests/                   scoring · hash chain · pipeline
```

Deep dives: [Methodology](docs/METHODOLOGY.md) · [Architecture](docs/ARCHITECTURE.md) · [Hash chain](docs/HASH_CHAIN.md) · [Gene pool](docs/GENES.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

## References

- Dharia, N. V. et al. *A first-generation pediatric cancer dependency map.* **Nature Genetics** (2021). https://www.nature.com/articles/s41588-021-00819-w
- Nelson, M. R. et al. *The support of human genetic evidence for approved drug indications.* **Nature Genetics** (2015).
- King, E. A., Davis, J. W. & Degner, J. F. *Are drug targets with genetic support twice as likely to be approved?* **PLOS Genetics** (2019). https://pmc.ncbi.nlm.nih.gov/articles/PMC6907751/
- Minikel, E. V. et al. *Refining the impact of genetic evidence on clinical success.* (2020).
- Data sources: [DepMap](https://depmap.org) · [Open Targets](https://www.opentargets.org) · [COSMIC](https://cancer.sanger.ac.uk/cosmic) · [Reactome](https://reactome.org) · [ChEMBL](https://www.ebi.ac.uk/chembl/) · [ClinicalTrials.gov](https://clinicaltrials.gov) · [PubMed](https://pubmed.ncbi.nlm.nih.gov)

<div align="center">

*ONC · an autonomous AI scientist · predictions sealed, results published, nothing hidden*

</div>
