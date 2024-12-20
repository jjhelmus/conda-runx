# conda-runx

A conda plugin for running script containing [inline metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata).

## Quick-start

The script:

``` python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests<3",
# ]
# ///
import sys
import requests

print("Hello from the script!")
print(f"The Python version is: {sys.version}")
print(f"The requests module is: {requests}")
print(f"The requests version is: {requests.__version__}")
```

Can be run using:
```
conda install --name base -c jjhelmus conda-runx
conda runx example.py
```

An environment with an Python interpreter and dependencies as defined in the script will be created
automatically.

This is similar to `ux run --script example.py`
