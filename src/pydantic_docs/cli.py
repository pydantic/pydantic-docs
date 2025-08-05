from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any, Final, cast

import click
from mkdocs import __version__ as mkdocs_version
from mkdocs.__main__ import (
    color_option,
    common_options,
    config_help,
    dev_addr_help,
    no_reload_help,
    serve_clean_help,
    serve_dirty_help,
    serve_open_help,
    strict_help,
    use_directory_urls_help,
    watch_help,
    watch_theme_help,
)
from mkdocs.commands import serve
from ruamel.yaml import YAML

from pydantic_docs import __version__

BASE_CONFIG: Final = Path(__file__).parent / 'mkdocs.pydantic.yml'


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(
    __version__,
    message=f'%(prog)s, version %(version)s (mkdocs {mkdocs_version})',
)
@common_options
@color_option
def cli():
    """pydantic-docs - Wrapper around the MkDocs CLI."""


@cli.command(name='serve')
@click.option('-a', '--dev-addr', help=dev_addr_help, metavar='<IP:PORT>')
@click.option('-o', '--open', 'open_in_browser', help=serve_open_help, is_flag=True)
@click.option('--no-livereload', 'livereload', flag_value=False, help=no_reload_help)
@click.option('--livereload', 'livereload', flag_value=True, default=True, hidden=True)
@click.option('--dirtyreload', 'build_type', flag_value='dirty', hidden=True)
@click.option('--dirty', 'build_type', flag_value='dirty', help=serve_dirty_help)
@click.option('-c', '--clean', 'build_type', flag_value='clean', help=serve_clean_help)
@click.option('--watch-theme', help=watch_theme_help, is_flag=True)
@click.option('-w', '--watch', help=watch_help, type=click.Path(exists=True), multiple=True, default=[])
# Adapted from the `mkdocs.__main__.common_config_options`:
@click.option('-f', '--config-file', type=click.Path(exists=True, dir_okay=False, resolve_path=True), help=config_help)
@click.option('-s', '--strict/--no-strict', is_flag=True, default=None, help=strict_help)
@click.option(
    '--use-directory-urls/--no-directory-urls',
    is_flag=True,
    default=None,
    help=use_directory_urls_help,
)
@common_options
def serve_command(**kwargs: Any) -> None:
    if (path_str := kwargs.pop('config_file', None)) is not None:
        config_path = Path(path_str)
    else:
        for path_str in ('mkdocs.yml', 'mkdocs.yaml'):
            if Path(path_str).is_file():
                config_path = Path(path_str)
                break
        else:
            raise click.UsageError("Unable to find a 'mkdocs.yml' configuration file")

    # Using ruamel's roundtrip parser to avoid processing any custom constructor (e.g. `!ENV`):
    yaml = YAML(typ='rt')
    project_docs_config = cast(dict[str, Any], yaml.load(config_path))
    common_docs_config = cast(dict[str, Any], yaml.load(BASE_CONFIG))

    existing_theme_freatures: list[str] = project_docs_config.get('theme', {}).get('features', [])

    project_docs_config['theme'] = common_docs_config['theme']
    project_docs_config['theme']['features'].extend(existing_theme_freatures)

    project_docs_config.setdefault('extra_css', []).extend(common_docs_config['extra_css'])
    project_docs_config.setdefault('extra_javascript', []).extend(common_docs_config['extra_javascript'])

    out_config = BytesIO()
    # `mkdocs.config.base.load_config()` uses the `name` attribute:
    out_config.name = path_str
    yaml.dump(project_docs_config, out_config)

    serve.serve(
        config_file=out_config,  # pyright: ignore[reportArgumentType]
        **kwargs,
    )
