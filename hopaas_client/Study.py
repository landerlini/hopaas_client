import contextlib
from typing import Union, Dict, Any

from hopaas_client.Client import Client
from hopaas_client.Trial import Trial
from hopaas_client.Exceptions import HopaasConsistencyError

from hopaas_client.pruners import Pruner, NopPruner
from hopaas_client.samplers import Sampler, TPESampler
from hopaas_client.suggestions import Suggestion
from hopaas_client.FrozenTrial import FrozenTrial

from hopaas_client.utils import valid_properties


class Study:
    """
    Envelop for any Bayesian optimization study.

    name: `str`
        Title of the study to be used as a human-readable identifier.

    properties: `dict`
        Dictionary of variables representing the context of the study.
        Some or all the variables can be `hopaas_client.suggestions` to
        be replaced with values as prompted by Hopaas server.

    direction: `str`, default: `"minimize"`
        direction of the optimization, can be either "minimize" or "maximize".

    sampler: `Sampler`, default: `TPESampler`
        the sampler define the strategy adopted to pick a set of values
        for properties identified with suggestions.

    pruner: `Pruner`, default: `NopPruner`
        the pruner defines the strategy adopted to abort a study when
        considered not worth based on the preliminary or intermediate results.
        The `NopPruner`, used as default, never abort studies.

    client: `Client`, default: `None`
        handle to use a specially configured client. By default, the user is
        prompted for Client configuration in stdin, unless a configuration file
        `.hopaasrc` is found in the system.

    """
    def __init__(self,
                 name: str,
                 properties: dict,
                 special_properties: Union[dict, None] = None,
                 direction: str = 'minimize',
                 pruner: Pruner = NopPruner(),
                 sampler: Sampler = TPESampler(),
                 client: Union[Client, None] = None
                 ):
        self._name = name
        self._properties = valid_properties({
                k: str(v) if isinstance(v, Suggestion)
                else v for k, v in properties.items()
            }, allow_none=False
        )
        self._special_properties = valid_properties(
            special_properties, allow_none=True
        )
        self._direction = direction
        self._pruner = pruner
        self._sampler = sampler
        self._client = client if client is not None else Client()
        self._suid: Union[str, None] = None
        self._trials: Dict[str, Any] = dict()

    @property
    def direction(self) -> str:
        """Direction of the study, either `'maximize'` or `'minimize'`"""
        return self._direction

    @property
    def is_initialized(self) -> bool:
        """
        True if a `study_id` has been assigned by
        the Hopaas server to this study
        """
        return self._suid is not None

    @property
    def study_id(self) -> Union[str, None]:
        """The `study_id` (or `suid`) as defined by the Hopaas server"""
        return self._suid

    @property
    def best_trial_id(self) -> Union[int, None]:
        """The id (an integer) of the trial obtaining the best score"""
        if not self.is_initialized:
            raise HopaasConsistencyError("Study not initialized")
        else:
            return self._client.get_best_trial(self._suid, 0)

    @property
    def trials(self):
        """
        Dictionary of the trials run locally.

        Note that best trial may be obtained in an independent run,
        and therefore may not be accessible here.
        """
        return {k: FrozenTrial(self._suid, t.id, t.loss, t.properties)
                for k, t in self._trials.items()}

    @contextlib.contextmanager
    def trial(self):
        """
        Context manager handling a trial for this study.

        It takes care of getting the suggestion from the hopaas server and
        updating the server with the final result of the trial. It also informs
        the server in case the trial gets aborted for whatever reason.
        """
        properties = self._properties.copy()
        properties.update(hopaas_config=dict(
            title=self._name,
            direction=self.direction,
            sampler=self._sampler.asdict(),
            pruner=self._pruner.asdict()
        ))
        if self._special_properties is not None:
            properties.update({
                f"_{k}": v for k, v in self._special_properties.items()
            })
        properties = self._client.ask(properties)
        self._suid, trial_id = properties['hopaas_trial'].split(':')
        trial_id = int(trial_id)
        if trial_id in self._trials.keys():
            raise HopaasConsistencyError

        trial = Trial(study=self,
                      properties={k: v for k, v in properties.items()
                                  if k not in ['hopaas_trial']},
                      trial_id=trial_id)
        self._trials[trial_id] = trial

        try:
            yield trial
        finally:
            if trial.loss is not None:
                if not trial.should_prune:
                    self._client.tell(study_id=self._suid,
                                      trial_id=trial.id,
                                      loss=float(trial.loss))
            else:
                self._client.mark_as_failed(study_id=self._suid,
                                            trial_id=trial.id,
                                            error="Computation aborted")

    def should_prune(self, trial: Trial) -> bool:
        """
        Internal. Builds the requests to the hopaas server to enquiry on
        whether the trial is still worth.

        Use `trial.should_prune`, instead.
        """
        if trial.loss is None:
            return False
        else:
            return self._client.should_prune(study_id=self._suid,
                                             trial_id=trial.id,
                                             loss=trial.loss,
                                             step=trial.step)
