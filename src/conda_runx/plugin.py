from conda import plugins

from typing import Generator

def cli_runx_main(args):
    print("Hello World!!!!")


@plugins.hookimpl
def conda_subcommands() -> Generator[plugins.CondaSubcommand, None, None]:
    yield plugins.CondaSubcommand(
        name="runx",
        summary="run a script with inline PEP 723 metadata",
        action=cli_runx_main,
    )
