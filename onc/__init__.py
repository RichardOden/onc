"""ONC: an autonomous AI scientist for pediatric cancer gene dependencies.

ONC generates hypotheses about which genes childhood cancers depend on, scores
each candidate across six weighted evidence sources, cryptographically locks the
prediction *before* any test data is accessible, tests it against held-out
dependency data, has an independent verifier rule pass/fail, and publishes an
immutable, hash-chained receipt for every experiment.

The public surface is intentionally small:

    from onc import GENE_POOL, score_gene, run_experiment, HashChain
"""

from onc.genes import GENE_POOL, Gene, pool
from onc.scoring import WEIGHTS, ScoreCard, score_gene, is_confirmed
from onc.hashchain import HashChain, Receipt
from onc.pipeline import Experiment, run_experiment

__version__ = "0.5.0"

__all__ = [
    "GENE_POOL",
    "Gene",
    "pool",
    "WEIGHTS",
    "ScoreCard",
    "score_gene",
    "is_confirmed",
    "HashChain",
    "Receipt",
    "Experiment",
    "run_experiment",
    "__version__",
]
