#!/usr/bin/env python3
"""Calculate volume using parameters loaded from config.toml."""

import sys
import tomllib

with open("config/config.toml", "rb") as f:
    config = tomllib.load(f)

dimensions = config.get("dimensions", {})
length = dimensions.get("length", 1.0)
width = dimensions.get("width", 1.0)
depth = dimensions.get("depth", 1.0)
units = config.get("units", "metres")
shape = config.get("shape", "rectangular_prism")

volume = length * width * depth

verbose = "--verbose" in sys.argv or "-v" in sys.argv

if verbose:
    print("--- Runtime Variables (explicit) ---")
    print(f"  length  = {length}")
    print(f"  width   = {width}")
    print(f"  depth   = {depth}")
    print(f"  units   = {units!r}")
    print(f"  shape   = {shape!r}")
    print(f"  volume  = {volume}")
    print("--- Runtime Variables (globals) ---")
    for name, value in globals().items():
        if not name.startswith("_") and not callable(value) and not isinstance(value, type(sys)):
            print(f"  {name} = {value!r}")
    print("------------------------------------")

print(f"Shape: {shape}")
print(f"Dimensions: {length} x {width} x {depth} {units}")
print(f"Volume: {volume} m³")
