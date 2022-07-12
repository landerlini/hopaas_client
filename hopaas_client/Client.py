import json

from typing import Union
from hopaas_client.Configurable import Configurable
from hopaas_client.Exceptions import HopaasServerError

import requests


class Client (Configurable):
    def __init__(self,
                 server: Union[str, None] = None,
                 token: Union[str, None] = None,
                 config_filename: Union[str, None] = None,
                 force_reconfig: bool = False
                 ):
        if server is None or token is None:
            Configurable.__init__(self, config_filename, force_reconfig)
            self.server = server if server is not None else \
                f"{self.config['server']['address']}:{self.config['server']['port']}"
            self.token = token if token is not None else \
                self.config['auth']['api_token']
        else:
            self.server = server
            self.token = token

        # Active studies
        self._studies = []

    @property
    def backend_version(self):
        res = requests.get(f"{self.server}/api/version")
        if res.status_code == 200:
            return res.text

        raise HopaasServerError(res.status_code)

    def ask(self, properties: dict) -> dict:
        res = requests.post(f"{self.server}/api/ask/{self.token}",
                            data=json.dumps(properties))

        if res.status_code == 200:
            return json.loads(res.text)

        raise HopaasServerError(res.status_code)

    def tell(self, study_id: str, trial_id: int, loss: float):
        res = requests.post(f"{self.server}/api/tell/{self.token}",
                            data=json.dumps(dict(
                                hopaas_trial=f"{study_id}:{trial_id}",
                                loss=loss
                            )))

        if res.status_code != 200:
            raise HopaasServerError

    def mark_as_failed(self, study_id: str, trial_id: int, error: str):
        res = requests.post(f"{self.server}/api/mark_as_failed/{self.token}",
                            data=json.dumps(dict(
                                hopaas_trial=f"{study_id}:{trial_id}",
                                error=error
                            )))

        if res.status_code != 200:
            raise HopaasServerError

    def should_prune(self, study_id: str, trial_id: int, loss: float, step: int):
        res = requests.post(f"{self.server}/api/should_prune/{self.token}",
                            data=json.dumps(dict(
                                hopaas_trial=f"{study_id}:{trial_id}",
                                loss=loss,
                                step=step
                            )))

        if res.status_code != 200:
            raise HopaasServerError

        if res.text.lower() not in ['true', 'false']:
            raise HopaasServerError

        if res.text.lower() == 'true':
            return True
        return False




