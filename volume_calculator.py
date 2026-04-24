#!/usr/bin/env python3
"""Calculate volume given width, height, and length with automatic SI unit conversion."""

import re

# SI length units and their conversion factors to meters
SI_LENGTH_UNITS = {
    "km": 1e3,
    "m": 1,
    "dm": 1e-1,
    "cm": 1e-2,
    "mm": 1e-3,
    "um": 1e-6,
    "μm": 1e-6,
}

# Volume display options
VOLUME_UNITS = {
    "km³": 1e9,
    "m³": 1,
    "dm³": 1e-3,
    "cm³": 1e-6,
    "mm³": 1e-9,
}


def parse_dimension(input_str: str) -> float:
    """Parse a dimension string like '5.2 cm' and return the value in meters.

    Accepts formats:
      - "5.2 cm"  (number + space + unit)
      - "5.2cm"   (number + unit, no space)
      - "5.2"     (number only, assumed meters)
    """
    input_str = input_str.strip().lower()
    match = re.match(r"^([\d.]+)\s*(km|m|dm|cm|mm|um|μm)?$", input_str)
    if not match:
        raise ValueError(f"Invalid dimension format: '{input_str}'")

    value = float(match.group(1))
    unit = match.group(2) or "m"  # default to meters

    if unit not in SI_LENGTH_UNITS:
        raise ValueError(f"Unknown unit: '{unit}'")

    return value * SI_LENGTH_UNITS[unit]


def format_volume(volume_m3: float) -> str:
    """Return the volume formatted in the most appropriate SI unit."""
    if volume_m3 == 0:
        return "0 m³"

    # Pick the unit that gives a value between 1 and 1000
    for unit_name, factor in VOLUME_UNITS.items():
        converted = volume_m3 / factor
        if abs(converted) >= 1:
            # Use compact notation for very large/small numbers
            if converted >= 1e6 or (converted < 1 and converted != 0):
                return f"{converted:.6e} {unit_name}"
            return f"{converted:.4g} {unit_name}"

    return f"{volume_m3:.6e} m³"


def calculate_volume(width: float, height: float, length: float) -> float:
    """Return the volume in cubic meters (all inputs should be in meters)."""
    return width * height * length


def main():
    print("Volume Calculator (SI Units)")
    print("-" * 30)
    print("Supported units: km, m, dm, cm, mm, μm")
    print("Examples: 5.2 cm, 100 mm, 3 m, 0.5 km")
    print("If no unit is given, meters (m) is assumed.\n")

    try:
        width_raw = input("Enter width: ")
        height_raw = input("Enter height: ")
        length_raw = input("Enter length: ")

        width = parse_dimension(width_raw)
        height = parse_dimension(height_raw)
        length = parse_dimension(length_raw)

        if width < 0 or height < 0 or length < 0:
            print("Error: Dimensions must be non-negative.")
            return

        volume_m3 = calculate_volume(width, height, length)
        formatted = format_volume(volume_m3)
        print(f"\nVolume: {formatted}")
        print(f"        ({volume_m3:.6e} m³)")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
