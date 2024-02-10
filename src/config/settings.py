from configparser import ConfigParser
from os import getenv
from typing import Any


class Settings:
    __slots__ = ['config_parser', 'env']
    config_parser: ConfigParser
    env: str

    def __init__(self, file: str = 'settings.conf'):
        self.config_parser = ConfigParser()
        self.config_parser.read(file)
        self.env = getenv('ENV', 'dev')

    def get(self, name: str, default_value: Any = None) -> Any:
        return self._get_from_section(self.env, name) or self._get_from_section('default', name) or default_value

    def _get_from_section(self, section: str, var: str) -> Any:
        if section in self.config_parser and var in self.config_parser[section]:
            return self.config_parser[section][var]
        return None

settings = Settings()
