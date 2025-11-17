"""
═══════════════════════════════════════════════════════════════════
MODULE: channel/noise.py
PURPOSE: Add realistic noise to simulate imperfect channels
THEME: Nothing in the real world is perfect - welcome to noise!
═══════════════════════════════════════════════════════════════════

📡 STORY:
When signals travel through space, they pick up NOISE.
Think of noise like static on an old radio, or snow on a TV.

Noise is RANDOM INTERFERENCE that corrupts our signal.
It comes from:
  - Thermal radiation from the sun
  - Cosmic background radiation
  - Electronics in the receiver
  - Atmospheric interference

We simulate noise using AWGN (Additive White Gaussian Noise):
  - Additive: We ADD it to the signal
  - White: Contains all frequencies equally
  - Gaussian: Random values follow a bell curve distribution

LEARNING GOALS:
  • What noise is and where it comes from
  • How SNR (Signal-to-Noise Ratio) measures signal quality
  • How noise causes bit errors
  • Understanding the Gaussian distribution
  • Converting to/from decibels (dB)

SIMPLIFICATIONS:
  - Only Gaussian noise (no impulse noise, pink noise, etc.)
  - Noise is constant over time (no time-varying fading yet)
  - Simplified SNR calculation

═══════════════════════════════════════════════════════════════════
"""

# ┌────────────────────────────────────────────────────────┐
# │              NOISE ADDITION PROCESS                    │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │  Clean Signal ─────┐                                  │
# │                    │                                   │
# │                    ├──► Σ ──► Noisy Signal            │
# │                    │                                   │
# │  Gaussian Noise ───┘                                  │
# │  (random values)                                       │
# │                                                        │
# │  SNR controls noise strength:                          │
# │    High SNR (30 dB) → Weak noise → Clear signal       │
# │    Low SNR (0 dB)   → Strong noise → Unusable         │
# │                                                        │
# └────────────────────────────────────────────────────────┘

import numpy as np


def add_awgn(signal, snr_db):
    """
    Add Additive White Gaussian Noise to a signal.

    🎓 TEACHING NOTE:
    This function calculates how much noise power to add
    based on the desired SNR (Signal-to-Noise Ratio).

    Process:
    1. Calculate signal power: P_signal = mean(signal²)
    2. Calculate required noise power from SNR
    3. Generate random Gaussian noise with that power
    4. Add noise to signal

    WHY GAUSSIAN?
    Real-world noise from many random sources follows
    a Gaussian (normal) distribution due to the Central
    Limit Theorem. It's a good model for thermal noise.

    Parameters
    ----------
    signal : ndarray
        Clean input signal
    snr_db : float
        Desired Signal-to-Noise Ratio in decibels
        (e.g., 20 dB = good quality, 5 dB = poor quality)

    Returns
    -------
    noisy_signal : ndarray
        Signal with noise added
    noise : ndarray
        The noise that was added (useful for visualization)
    """
    # Step 1: Calculate signal power
    # 🎓 Power is the mean of the squared signal values
    # This measures total energy in the signal
    signal_power = np.mean(signal ** 2)

    # Step 2: Convert SNR from dB to linear scale
    # 🎓 SNR_linear = 10^(SNR_dB / 10)
    snr_linear = db_to_linear(snr_db)

    # Step 3: Calculate required noise power
    # 🎓 From definition: SNR = P_signal / P_noise
    # Therefore: P_noise = P_signal / SNR
    noise_power = signal_power / snr_linear

    # Step 4: Calculate noise standard deviation
    # 🎓 For Gaussian: power = variance = std_dev²
    # Therefore: std_dev = sqrt(power)
    noise_std = np.sqrt(noise_power)

    # Step 5: Generate Gaussian noise
    # 🎓 np.random.normal(mean, std_dev, size)
    # Mean = 0 (noise centered around zero)
    # Std = calculated noise_std
    # Size = same as signal length
    noise = np.random.normal(0, noise_std, len(signal))

    # Step 6: Add noise to signal
    # 🎓 This is the "Additive" part of AWGN!
    noisy_signal = signal + noise

    return noisy_signal, noise


def calculate_snr_db(signal, noise):
    """
    Calculate Signal-to-Noise Ratio in decibels.

    🎓 TEACHING NOTE:
    SNR measures how much stronger the signal is than the noise.

    Formula:
      SNR = P_signal / P_noise
      SNR_dB = 10 * log10(SNR)

    Typical values:
      30 dB = Excellent (signal is 1000× stronger)
      20 dB = Good (100×)
      10 dB = Marginal (10×)
      0 dB = Unusable (equal power)

    Parameters
    ----------
    signal : ndarray
        Clean signal
    noise : ndarray
        Noise component

    Returns
    -------
    snr_db : float
        SNR in decibels
    """
    # Step 1: Calculate signal power
    # 🎓 Power = mean of squared values
    signal_power = np.mean(signal ** 2)

    # Step 2: Calculate noise power
    noise_power = np.mean(noise ** 2)

    # Step 3: Calculate SNR as power ratio
    # 🎓 Avoid division by zero!
    if noise_power == 0:
        return float('inf')  # Perfect signal, no noise

    snr_linear = signal_power / noise_power

    # Step 4: Convert to decibels
    # 🎓 dB = 10 * log10(linear_ratio)
    snr_db = 10 * np.log10(snr_linear)

    return snr_db


def db_to_linear(db_value):
    """
    Convert decibels to linear scale.

    🎓 TEACHING NOTE:
    Decibels are a logarithmic scale (like pH or Richter scale).
    They're useful because they compress large ranges.

    Formula: linear = 10^(dB/10)

    Examples:
      0 dB → 1.0 (no change)
      10 dB → 10.0 (10× increase)
      20 dB → 100.0 (100× increase)
      -10 dB → 0.1 (10× decrease)

    Parameters
    ----------
    db_value : float
        Value in decibels

    Returns
    -------
    linear_value : float
        Linear scale value
    """
    # 🎓 Formula: 10^(dB/10)
    # This is the inverse of the dB formula
    linear_value = 10 ** (db_value / 10)

    return linear_value


def linear_to_db(linear_value):
    """
    Convert linear scale to decibels.

    🎓 TEACHING NOTE:
    Reverse of db_to_linear().

    Formula: dB = 10 * log10(linear)

    Parameters
    ----------
    linear_value : float
        Linear scale value (must be > 0)

    Returns
    -------
    db_value : float
        Value in decibels
    """
    # 🎓 Formula: 10 * log10(linear)
    # Handle edge case: log of zero is undefined
    if linear_value <= 0:
        return float('-inf')  # Negative infinity dB

    db_value = 10 * np.log10(linear_value)

    return db_value


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Noise too strong? Check SNR is positive (e.g., 10 dB, not -10 dB)
#   2. Signal completely buried? SNR might be too low (< 0 dB)
#   3. No visible noise? SNR too high (> 40 dB)
#   4. Math errors? Make sure signal isn't all zeros
#
# Testing Tips:
#   - Plot signal + noise together to see effect visually
#   - Plot histogram of noise to verify Gaussian distribution
#   - Try SNR values: 0, 5, 10, 15, 20, 30 dB to see progression
#   - Calculate SNR after adding noise to verify it matches target
#
# Gotchas:
#   - SNR is a ratio of POWER (signal²), not amplitude
#   - dB scale is logarithmic (20 dB is 100×, not 2× 10 dB)
#   - Negative dB means noise is stronger than signal!


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Add colored noise (pink, brown, blue)
#   [ ] Implement impulse noise (random spikes)
#   [ ] Add time-varying SNR
#   [ ] Support different noise distributions
#   [ ] Add noise figure calculations
#   [ ] Implement noise temperature models
#
# For Deep Space Version:
#   [ ] Extremely low SNR scenarios (< -10 dB)
#   [ ] Quantum noise limits
#   [ ] Solar noise burst events
