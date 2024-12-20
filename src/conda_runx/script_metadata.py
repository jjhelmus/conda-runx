import sys
import re
import dataclasses

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

PEP_723_PATTERN = r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$"


@dataclasses.dataclass
class ScriptMetadata:
    requires_python: str = ""
    dependencies: list[str] = dataclasses.field(default_factory=list)


def _remove_leading_comments(text: str) -> str:
    return "\n".join([line.removeprefix("#") for line in text.split("\n")])


def parse_script_metadata(script: str) -> ScriptMetadata:
    """ Return inline script metadata as specified in PEP 723. """
    with open(script) as fh:
        script_text = fh.read()
    match = re.match(PEP_723_PATTERN, script_text)
    if match is None:
        return ScriptMetadata()
    content = _remove_leading_comments(match["content"])
    metadata = tomllib.loads(content)
    return ScriptMetadata(
        requires_python=metadata.get("requires-python", ""),
        dependencies=metadata.get("dependencies", []),
    )

