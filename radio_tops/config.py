import os
from dynaconf import Dynaconf

current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    root_path=current_directory,
    envvar_prefix='RADIO_TOPS',
    settings_files=['default_config.toml'],
    merge_enabled=True,
)
