#!/usr/bin/env python3
"""Calculate volume using parameters loaded from config.yaml."""

import yaml

with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f) or {}

dimensions = config.get("dimensions", {})
length = dimensions.get("length", 1.0)
width = dimensions.get("width", 1.0)
depth = dimensions.get("depth", 1.0)
units = config.get("units", "metres")
shape = config.get("shape", "rectangular_prism")

volume = length * width * depth

print(f"Shape: {shape}")
print(f"Dimensions: {length} x {width} x {depth} {units}")
print(f"Volume: {volume} m³")
