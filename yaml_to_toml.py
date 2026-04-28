#!/usr/bin/env python3
"""Convert a YAML config file to a TOML config file."""

import sys
import tomllib
import tomllib as _  # noqa: confirm built-in available
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    print("Error: pyyaml is required. Install it with: pip install pyyaml")
    sys.exit(1)

try:
    import tomli_w
    def dump_toml(data):
        return tomli_w.dumps(data)
except ModuleNotFoundError:
    # Fallback: manual TOML serialisation for simple flat/one-level-nested dicts
    def dump_toml(data):
        lines = []
        top_level = {k: v for k, v in data.items() if not isinstance(v, dict)}
        nested = {k: v for k, v in data.items() if isinstance(v, dict)}

        for key, value in top_level.items():
            lines.append(f"{key} = {_toml_value(value)}")

        for section, contents in nested.items():
            lines.append(f"\n[{section}]")
            for key, value in contents.items():
                lines.append(f"{key} = {_toml_value(value)}")

        return "\n".join(lines) + "\n"

    def _toml_value(value):
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            items = ", ".join(_toml_value(v) for v in value)
            return f"[{items}]"
        else:
            return str(value)


if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <config.yaml>")
    sys.exit(1)

yaml_path = Path(sys.argv[1])
toml_path = yaml_path.with_suffix(".toml")

with open(yaml_path, "r") as f:
    config = yaml.safe_load(f) or {}

toml_output = dump_toml(config)

with open(toml_path, "w") as f:
    f.write(f"# Converted from {yaml_path.name}\n")
    f.write(toml_output)

print(f"Converted '{yaml_path}' -> '{toml_path}'")
