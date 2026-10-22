# ONC Methodology

How ONC turns raw public data into a ranked, auditable list of pediatric cancer
gene dependencies.

## 1. Scope restriction

ONC scores **only** pediatric cell lines and pediatric-cancer associations:
neuroblastoma, Ewing sarcoma, medulloblastoma, ALL/AML, Wilms tumor,
rhabdomyosarcoma, rhabdoid tumors, and DIPG / pediatric high-grade glioma. Adult
epithelial cancers are excluded from every source query. This matters because a
genome-scale study of 82 pediatric cancer cell lines found their dependencies
are often **distinct** from adult cancers (Dharia et al., *Nature Genetics*,
2021) — so adult drug pipelines systematically miss them.

## 2. The six evidence sources

| Source | Weight | Database | Normalisation |
|--------|--------|----------|---------------|
| Dependency | 0.30 | DepMap | Chronos gene-effect → `[0,1]`; `-1.0` (common essential) → ~1.0 |
| Genetics | 0.20 | Open Targets, COSMIC | pediatric gene-disease association strength |
| Novelty | 0.15 | PubMed | publication count inverted via `1 - log1p(n)/log1p(5000)` |
| Pathways | 0.15 | Reactome | membership in cancer-relevant developmental pathways |
| Tractability | 0.10 | ChEMBL | best tractability bucket → `{1.0, 0.6, 0.3, 0.0}` |
| Clinical | 0.10 | ClinicalTrials.gov | `(ongoing + 2·succeeded − 1.5·failed) / 5`, clamped |

**Novelty is inverted on purpose.** Understudied genes score higher — ONC is
built to surface the overlooked, not re-confirm the crowded.

## 3. Fusion

The weighted total is a simple linear combination:

```
weighted = Σ  wᵢ · scoreᵢ          (Σ wᵢ = 1.0)
```

All weights are version-pinned in `onc/scoring.py` and covered by a test that
fails if they drift from summing to 1.0.

## 4. Confirmation rule

A gene is **confirmed** as worth laboratory attention only if it clears two bars
at once:

```
weighted > 0.50   AND   dependency > 0.40
```

The second bar prevents a gene from being carried to confirmation on soft
evidence (novelty, pathways) without a real dependency signal.

## 5. Why the genetics weighting

Drug targets backed by human genetic evidence are roughly **twice as likely** to
reach clinical approval (Nelson et al. 2015; King et al. 2019; Minikel et al.
2020). The genetics source exists to bias ONC toward exactly that kind of
support.

## 6. Limitations

ONC is a prioritisation engine, not a laboratory. Scores are only as good as the
underlying public data; absence of evidence defaults to 0.0; and a confirmed
candidate is a hypothesis to test at the bench, never a conclusion.
