"""
═══════════════════════════════════════════════════════════════════
MODULE: channel/range_loss.py
PURPOSE: Simulate signal attenuation due to distance
THEME: The farther away, the weaker the signal
═══════════════════════════════════════════════════════════════════

📡 STORY:
Imagine shouting across a field. The farther your friend is,
the quieter they hear you. Same thing happens with radio signals!

As signals travel through space, they SPREAD OUT.
The energy gets distributed over a larger area, so less energy
reaches the receiver.

This is called FREE SPACE PATH LOSS (FSPL).

LEARNING GOALS:
  • Understanding inverse-square law (1/distance²)
  • How distance affects signal strength
  • Basic link budget concepts
  • Working with dB for large changes

SIMPLIFICATIONS:
  - No antenna gains
  - No atmospheric absorption (separate module)
  - Simplified FSPL formula
  - Distance in km (not orbital mechanics)

═══════════════════════════════════════════════════════════════════
"""

# ┌────────────────────────────────────────────────────────┐
# │              RANGE LOSS CONCEPT                        │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │         Satellite                                      │
# │            📡                                          │
# │             │ \                                        │
# │             │   \  Signal spreads                      │
# │             │     \  in a sphere                       │
# │        1000 km      \                                  │
# │             │         \                                │
# │         ────▼──────────▼────                           │
# │         Ground Station                                 │
# │                                                        │
# │  Signal strength ∝ 1/distance²                         │
# │  (Inverse square law)                                  │
# │                                                        │
# └────────────────────────────────────────────────────────┘

import numpy as np


def apply_free_space_loss(signal, distance_km, reference_distance_km=1.0):
    """
    Apply free space path loss to a signal (simplified model).

    🎓 TEACHING NOTE:
    In free space, signal power decreases with the square of distance.
    This is called the INVERSE SQUARE LAW.

    Why? The signal energy spreads over a sphere's surface area,
    which grows as 4πr². So received power ∝ 1/r².

    Simplified Formula:
        attenuation = (reference_distance / distance)²
        signal_attenuated = signal × attenuation

    Real Formula (Friis transmission):
        FSPL_dB = 20*log10(d) + 20*log10(f) + 20*log10(4π/c)

    We use the simplified version for teaching clarity!

    Parameters
    ----------
    signal : ndarray
        Input signal
    distance_km : float
        Distance from transmitter to receiver in kilometers
        (e.g., 1000 km for LEO satellite)
    reference_distance_km : float
        Reference distance for normalization (default: 1 km)

    Returns
    -------
    attenuated_signal : ndarray
        Signal with range loss applied
    attenuation_factor : float
        The multiplicative attenuation factor applied
    """
    # Handle edge case: zero or negative distance
    if distance_km <= 0:
        distance_km = reference_distance_km  # No loss

    # Step 1: Calculate attenuation factor using inverse square law
    # 🎓 Factor = (reference / actual)²
    # Example: At 10 km with 1 km reference:
    #   attenuation = (1/10)² = 0.01 = 1% of original power
    attenuation_factor = (reference_distance_km / distance_km) ** 2

    # Step 2: Apply attenuation to signal
    # 🎓 Simply multiply signal by the attenuation factor
    # This reduces the amplitude (and thus power) of the signal
    attenuated_signal = signal * attenuation_factor

    return attenuated_signal, attenuation_factor


def distance_to_attenuation_db(distance_km, reference_distance_km=1.0):
    """
    Calculate path loss in decibels for a given distance.

    🎓 TEACHING NOTE:
    This function tells you "How much weaker is the signal at distance D?"

    Uses simplified free space path loss formula:
        Attenuation_dB = 20 * log10(distance / reference)

    Note: This is NEGATIVE dB (loss), not gain!

    Typical Values:
        100 km → -40 dB (10,000× weaker)
        1000 km → -60 dB (1,000,000× weaker)
        10,000 km → -80 dB (100,000,000× weaker)

    Parameters
    ----------
    distance_km : float
        Distance from transmitter to receiver
    reference_distance_km : float
        Reference distance (default: 1 km)

    Returns
    -------
    attenuation_db : float
        Path loss in decibels (negative value)
    """
    # Handle edge case
    if distance_km <= 0:
        return 0.0  # No loss

    # Calculate distance ratio
    distance_ratio = distance_km / reference_distance_km

    # Convert to dB using: 20*log10(ratio) for amplitude/voltage
    # 🎓 Why 20 and not 10? We're dealing with amplitude, not power!
    # Power ∝ amplitude², so dB conversion uses 20*log10 for amplitude
    attenuation_db = 20 * np.log10(distance_ratio)

    return attenuation_db


def apply_attenuation_db(signal, attenuation_db):
    """
    Apply a specified attenuation in dB to a signal.

    🎓 TEACHING NOTE:
    Sometimes we know the loss in dB and want to apply it directly.
    This is common when working with link budgets.

    Parameters
    ----------
    signal : ndarray
        Input signal
    attenuation_db : float
        Attenuation to apply in dB (typically negative)

    Returns
    -------
    attenuated_signal : ndarray
        Signal with attenuation applied
    """
    # Convert dB to linear scale
    # 🎓 For amplitude: factor = 10^(dB/20)
    # Note: 20, not 10, because amplitude not power!
    attenuation_factor = 10 ** (attenuation_db / 20)

    # Apply attenuation
    attenuated_signal = signal * attenuation_factor

    return attenuated_signal


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Signal becomes zero? Distance too large (> 10,000 km for our simple model)
#   2. No visible attenuation? Distance might be ≤ reference_distance
#   3. Math errors? Check distance is positive
#
# Testing Tips:
#   - Test with distance = reference_distance → should be no loss
#   - Test with distance = 10× reference → should be 1/100 power
#   - Compare signal before/after visually
#   - Calculate expected dB loss: 20*log10(distance/ref)
#
# Gotchas:
#   - Attenuation is for AMPLITUDE, not power
#   - Power loss is 10*log10, amplitude is 20*log10
#   - Real FSPL includes frequency - we simplified it out
#   - This is free space only - no atmospheric effects


def apply_atmospheric_loss(signal, elevation_angle_deg=30, weather='clear'):
    """
    Apply simplified atmospheric absorption loss.

    🎓 TEACHING NOTE:
    Earth's atmosphere absorbs radio signals!
    How much depends on:
    - Elevation angle (lower = more atmosphere to pass through)
    - Weather (rain/clouds absorb more)
    - Frequency (higher frequencies absorbed more)

    SIMPLIFIED MODEL:
    We use a simple scalar loss based on angle and weather.
    Real models are MUCH more complex (ITU-R P.676, etc.)

    Typical Values:
    - Clear sky, high angle: ~0.5 dB loss
    - Clear sky, low angle: ~2 dB loss
    - Rain, low angle: ~5 dB loss

    Parameters
    ----------
    signal : ndarray
        Input signal
    elevation_angle_deg : float
        Angle above horizon in degrees (0-90)
        - 90° = directly overhead (minimum atmosphere)
        - 30° = 30° above horizon (moderate)
        - 10° = near horizon (maximum atmosphere)
    weather : str
        Weather condition: 'clear', 'cloudy', 'rain'

    Returns
    -------
    attenuated_signal : ndarray
        Signal with atmospheric loss applied
    loss_db : float
        Atmospheric loss in dB
    """
    # 🎓 WEATHER IMPACT
    # Different weather = different absorption
    weather_loss_db = {
        'clear': 0.5,
        'cloudy': 1.5,
        'rain': 4.0
    }
    base_loss = weather_loss_db.get(weather, 0.5)

    # 🎓 ELEVATION ANGLE IMPACT
    # Lower angles = signal passes through more atmosphere
    # Use cosecant law approximation
    elevation_angle_deg = np.clip(elevation_angle_deg, 5, 90)  # Avoid division by zero

    # At zenith (90°), path through atmosphere is minimum (factor = 1)
    # At lower angles, path is longer (factor > 1)
    elevation_rad = np.radians(elevation_angle_deg)
    path_length_factor = 1 / np.sin(elevation_rad)

    # 🎓 TOTAL ATMOSPHERIC LOSS
    # Longer path → more absorption
    total_loss_db = base_loss * path_length_factor

    # Apply attenuation
    attenuated_signal = apply_attenuation_db(signal, -total_loss_db)

    return attenuated_signal, total_loss_db


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Add antenna gain calculations
#   [ ] Include polarization losses
#   [ ] Add rain fade models (ITU-R P.618)
#   [ ] Support multiple frequency bands
#   [ ] Gas absorption (oxygen, water vapor)
#   [ ] Cloud attenuation models
