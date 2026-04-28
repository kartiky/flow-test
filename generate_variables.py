#!/usr/bin/env python3
"""Read a YAML config file and generate a Python file with variables initialised from it."""

import sys
import yaml
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <config.yaml>")
    sys.exit(1)

yaml_path = Path(sys.argv[1])
OUTPUT_FILE = Path("generated") / (yaml_path.stem + "_variables.py")

with open(yaml_path, "r") as f:
    config = yaml.safe_load(f) or {}

lines = [
    f"# Auto-generated from {yaml_path.name} — do not edit manually.",
    "",
]

def flatten(data, prefix=""):
    """Recursively flatten nested dicts into variable assignments."""
    entries = []
    for key, value in data.items():
        var_name = f"{prefix}{key}".upper()
        if isinstance(value, dict):
            entries.extend(flatten(value, prefix=f"{prefix}{key}_"))
        else:
            entries.append(f"{var_name} = {repr(value)}")
    return entries

lines.extend(flatten(config))
lines.append("")  # trailing newline

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(lines))

print(f"Generated '{OUTPUT_FILE}' with {len(lines) - 3} variable(s).")
