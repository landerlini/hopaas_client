import contextlib
from typing import Union

from hopaas_client.Client import Client
from hopaas_client.Trial import Trial
from hopaas_client.Exceptions import HopaasConsistencyError

from hopaas_client.pruners import Pruner, NopPruner
from hopaas_client.samplers import Sampler, TPESampler
from hopaas_client.suggestions import Suggestion

class Study:
    def __init__(self,
                 name: str,
                 properties: dict,
                 direction: str = 'minimize',
                 pruner: Pruner = NopPruner(),
                 sampler: Sampler = TPESampler(),
                 client: Union[Client, None] = None
                 ):
        self._name = name
        self._client = client if client is not None else Client()
        self._properties = {k: str(v) if isinstance(v, Suggestion) else v for k, v in properties.items()}
        self._suid = None
        self._direction = direction
        self._trials = {}
        self._pruner = pruner
        self._sampler = sampler

    @property
    def direction(self):
        return self._direction

    @property
    def is_initialized(self):
        return self._suid is not None

    @property
    def study_id(self):
        return self._suid

    @contextlib.contextmanager
    def trial(self):
        properties = self._properties.copy()
        properties.update(hopaas_config=dict(
            title=self._name,
            direction=self.direction,
            sampler=self._sampler.asdict(),
            pruner=self._pruner.asdict()
        ))
        properties = self._client.ask(properties)
        self._suid, trial_id = properties['hopaas_trial'].split(':')
        trial_id = int(trial_id)
        if trial_id in self._trials.keys():
            raise HopaasConsistencyError

        trial = Trial(self, {k: v for k, v in properties.items() if k not in ['hopaas_trial']}, trial_id=trial_id)
        self._trials[trial_id] = trial

        try:
            yield trial
        finally:
            if trial.loss is not None:
                self._client.tell(self._suid, trial.id, float(trial.loss))
            else:
                self._client.mark_as_failed(self._suid, trial.id, "Computation aborted")

    def should_prune(self, trial: Trial) -> bool:
        if trial.loss is None:
            return False

        return self._client.should_prune(self._suid, trial.id, trial.loss, trial.step)




