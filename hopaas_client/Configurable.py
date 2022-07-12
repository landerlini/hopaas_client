import os.path
from typing import Union
from configparser import ConfigParser


class Configurable:
    def __init__(self, config_filename: Union[str, None] = None, force_reconfig: bool = False):
        self._config_filename = config_filename if config_filename is not None else self.get_default_cfgfile()
        self.config = self.load_config(self._config_filename, force_reconfig)

    @staticmethod
    def load_config(config_filename: str, force_reconfig: bool) -> ConfigParser:
        if force_reconfig or not os.path.exists(config_filename):
            prompt_user_for_config(config_filename=config_filename)

        config = ConfigParser()
        config.read(config_filename)

        return config

    @staticmethod
    def get_default_cfgfile() -> str:
        try:
            return os.path.join(os.environ['HOME'], ".hopaasrc")
        except KeyError:
            return os.path.join(os.path.dirname(__file__), '.hopaasrc')


def prompt_user_for_config(config_filename: str) -> None:
    parser = ConfigParser()
    parser['server'] = dict(
        address=input("Server address: "),
        port=int(input("Server port: "))
    )
    parser['auth'] = dict(
        api_token=input("API token: ")
    )

    with open(config_filename, 'w') as configfile:
        parser.write(configfile)

