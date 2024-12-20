from __future__ import annotations

import os
import hashlib
from typing import TYPE_CHECKING
from argparse import Namespace

import platformdirs

from conda.env.installers.conda import install as conda_install
from conda.env.installers.pip import install as pip_install
from conda.gateways.disk.delete import rm_rf
from conda.base.context import context

if TYPE_CHECKING:
    from .script_metadata import ScriptMetadata


HASH_SIZE = 12


def _get_prefix_path(conda_specs: list[str], pip_specs: list[str]) -> str:
    hash_input = ";".join(conda_specs) + ";".join(pip_specs)
    dir_hash = hashlib.sha1(hash_input.encode("utf-8")).hexdigest()[:HASH_SIZE]
    prefix = os.path.join(
        platformdirs.user_cache_dir(),
        "conda-runx",
        dir_hash
    )
    return prefix


def create_conda_env(scriptmetadata: ScriptMetadata, refresh: bool) -> str:
    metadata = scriptmetadata
    conda_specs = [f"python {metadata.requires_python}", "pip"]
    pip_specs = sorted(metadata.dependencies)
    prefix = _get_prefix_path(conda_specs, pip_specs)
    if not refresh and os.path.exists(prefix):
        return prefix
    rm_rf(prefix)
    # Use installers from conda.env namespace
    # Another option is conda.cli.install which give more flexibility in channels, solver, etc
    env = Namespace()
    env.channels = context.channels
    args = Namespace()
    args.file = ""
    conda_install(prefix, conda_specs, args, env)
    pip_install(prefix, pip_specs, args, env)
    return prefix
