import os

from conda.base.context import context
from conda.common.compat import encode_environment
from conda.common.constants import NULL
from conda.gateways.disk.delete import rm_rf
from conda.gateways.subprocess import subprocess_call
from conda.utils import wrap_subprocess_call


def run_in_conda_env(prefix: str, executable_call: list[str]) -> int:
    # adapted from conda.cli.main_run::execute
    # create run script
    script, command = wrap_subprocess_call(
        context.root_prefix,
        prefix,
        NULL,
        NULL,
        executable_call,
        use_system_tmp_path=True,
    )
    # run script
    response = subprocess_call(
        command,
        env=encode_environment(os.environ.copy()),
        path=os.getcwd(),
        raise_on_error=False,
        capture_output=False,
    )
    rm_rf(script)
    return response.rc
