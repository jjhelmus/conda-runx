from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from conda import plugins

if TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace
    from typing import Generator


def configure_parser(parser: ArgumentParser) -> None:
    parser.add_argument("--refresh", action="store_true", help="Refresh the cache even if it exists")
    parser.add_argument("script", help="Python script to run")


def cli_runx_main(args: Namespace) -> None:
    from .script_metadata import parse_script_metadata
    from .run_script import run_in_conda_env
    from .create_env import create_conda_env

    script: str = args.script
    scriptmetadata = parse_script_metadata(script)
    prefix = create_conda_env(scriptmetadata, args.refresh)
    executable_call = ["python", script]
    exit_code = run_in_conda_env(prefix, executable_call)
    sys.exit(exit_code)


@plugins.hookimpl
def conda_subcommands() -> Generator[plugins.CondaSubcommand, None, None]:
    yield plugins.CondaSubcommand(
        name="runx",
        summary="run a script with inline PEP 723 metadata",
        action=cli_runx_main,
        configure_parser=configure_parser,
    )
