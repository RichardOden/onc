"""Evidence source adapters.

Each adapter turns a raw public data source into a single score in [0, 1] for a
given gene. Live adapters query the real APIs; the bundled offline adapter reads
from ``data/sample_evidence.json`` so the pipeline is fully runnable (and
testable) without network access or API keys.

All adapters implement :class:`~onc.sources.base.EvidenceSource`.
"""

from onc.sources.base import EvidenceSource, OfflineEvidence, SOURCE_NAMES

__all__ = ["EvidenceSource", "OfflineEvidence", "SOURCE_NAMES"]
