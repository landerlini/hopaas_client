import json

from typing import List, Optional
from dataclasses import dataclass


class Suggestion:
    pass


@dataclass(frozen=True)
class Int(Suggestion):
    low: int
    high: int
    step: int = 1
    log: bool = False

    def __str__(self):
        low = json.dumps(self.low)
        high = json.dumps(self.high)
        step = json.dumps(self.step)
        log = json.dumps(self.log)
        return f"optuna#int({low},{high},{step},{str(log)})"


@dataclass(frozen=True)
class Float(Suggestion):
    low: float
    high: float
    step: Optional[float] = None
    log: bool = False

    def __str__(self):
        low = json.dumps(self.low)
        high = json.dumps(self.high)
        step = json.dumps(self.step) if self.step is not None else "NaN"
        log = json.dumps(self.log)
        return f"optuna#float({low},{high},{step},{log})"


@dataclass(frozen=True)
class Categorical(Suggestion):
    choices: List[str]

    def __str__(self):
        return f"optuna#categorical({','.join(self.choices)})"
