from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

from mkdocs import exceptions
from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin

log = logging.getLogger('mkdocs.plugins.pydantic_docs')


BASE_CONFIG: Final = Path(__file__).parent / 'mkdocs.pydantic.yml'


class PydanticPluginConfig(Config):
    pass


class PydanticPlugin(BasePlugin[PydanticPluginConfig]):
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        with BASE_CONFIG.open(encoding='utf-8') as common_config_f:
            config.load_file(common_config_f)

        errors, warnings = config.validate()
        # Same logging logic as in `mkdocs.config.base.load_config()`:
        # TODO: is this necessary, as we control `BASE_CONFIG`?
        for config_name, warning in warnings:
            log.warning(f"Config value '{config_name}': {warning}")

        for config_name, error in errors:
            log.error(f"Config value '{config_name}': {error}")

        if len(errors) > 0:
            raise exceptions.Abort('Aborted with a configuration error!')
        elif config.strict and len(warnings) > 0:
            raise exceptions.Abort(f"Aborted with {len(warnings)} configuration warnings in 'strict' mode!")

        return config
