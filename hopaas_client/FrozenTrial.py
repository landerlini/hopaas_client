from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class FrozenTrial:
    """
    A copy read-only of a trial.
    """
    study_id: str
    trial_id: int
    loss: float
    properties: Dict[str, Any]