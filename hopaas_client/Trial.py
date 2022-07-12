from typing import Union

from hopaas_client import Study


class Trial:
    def __init__(self, study: Study, properties: dict, trial_id: int):
        self._properties = properties
        self._study = study
        self._loss = None
        self._step = -1
        self._id = trial_id

    def __getattr__(self, item):
        if item in self._properties.keys():
            return self._properties[item]

        raise KeyError(item)

    @property
    def id(self):
        return self._id

    @property
    def loss(self) -> Union[float, None]:
        if self._loss is None:
            return None

        return float(self._loss)

    @loss.setter
    def loss(self, value: float):
        self._step += 1
        self._loss = float(value)

    @property
    def step(self) -> int:
        return self._step

    @property
    def should_prune(self) -> bool:
        return self._study.should_prune(self)
