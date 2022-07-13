from copy import deepcopy
from typing import Union

from hopaas_client import Study


class Trial:
    """
    Trial is a pythonic representation of a set of parameters to be evaluated in the context of the study.

    It is designed to ease the access to the suggested values for the hyperparameters and to provide handles to
    update the computation of the loss during the study.

    A Trial should never be constructed by the user, but rather obtained from a study with the Study.trial()
    context manager.

    For example:
    ```
    with Study("A study", properties=dict(x=3)).trial() as trial:
        trial.loss = trial.x**2
    ```
    """
    def __init__(self, study: Study, properties: dict, trial_id: int):
        self._properties = properties
        self._study = study
        self._loss = None
        self._step = -1
        self._id = trial_id

    def __getattr__(self, item):
        """
        Simplified method to access the properties
        """
        if item in self._properties.keys():
            return self._properties[item]

        raise KeyError(item)

    @property
    def id(self) -> int:
        """
        The trial id (an integer)
        """
        return self._id

    @property
    def loss(self) -> Union[float, None]:
        """The most recent loss evaluation"""
        if self._loss is None:
            return None

        return float(self._loss)

    @property
    def properties(self):
        """Read-only version of the properties (here suggestions are parsed, already)"""
        return deepcopy(self.properties)

    @loss.setter
    def loss(self, value: float):
        """Setter for the loss, used to update the loss computation. Automatically updates the step number."""
        self._step += 1
        self._loss = float(value)

    @property
    def step(self) -> int:
        """The step number is the number of updates of the loss from the beginning of the trial"""
        return self._step

    @property
    def should_prune(self) -> bool:
        """
        Requests to the hopaas server whether the current trial is worth continuing,
        given the most recent update of the loss.
        """
        return self._study.should_prune(self)
