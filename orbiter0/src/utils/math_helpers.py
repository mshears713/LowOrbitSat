"""
═══════════════════════════════════════════════════════════════════
MODULE: utils/math_helpers.py
PURPOSE: Common calculations for signal analysis
THEME: Math tools used throughout the system
═══════════════════════════════════════════════════════════════════

📡 STORY:
Some calculations happen everywhere:
  • Converting to/from decibels
  • Calculating Signal-to-Noise Ratio
  • Bit Error Rate
  • Power calculations

Rather than duplicate code, we centralize them here.

LEARNING GOALS:
  • Decibel scale and why it's useful
  • SNR calculation and interpretation
  • BER as a quality metric
  • Code reusability

═══════════════════════════════════════════════════════════════════
"""

# ┌────────────────────────────────────────────────────────┐
# │              BIT ERROR RATE (BER) CONCEPT              │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │  BER = (Number of bit errors) / (Total bits)          │
# │                                                        │
# │  Examples:                                             │
# │    0 errors in 100 bits  →  BER = 0.00 (perfect!)     │
# │    1 error  in 100 bits  →  BER = 0.01 (1%)           │
# │    10 errors in 100 bits →  BER = 0.10 (10%)          │
# │                                                        │
# │  Typical Values:                                       │
# │    BER < 10⁻⁶   →  Excellent (< 1 error per million)  │
# │    BER ≈ 10⁻³   →  Acceptable (1 error per thousand)  │
# │    BER > 0.01   →  Poor (1+ errors per 100 bits)      │
# │    BER ≈ 0.5    →  Random guessing (useless!)         │
# │                                                        │
# └────────────────────────────────────────────────────────┘

import numpy as np


def count_bit_errors(transmitted_bits, received_bits):
    """
    Count the number of bit errors between two bit sequences.

    🎓 TEACHING NOTE:
    This does a simple comparison: how many bits are different?

    Example:
      Transmitted: [1, 0, 1, 1, 0]
      Received:    [1, 0, 0, 1, 0]
                           ↑
                        1 error (bit 2 flipped)

    Parameters
    ----------
    transmitted_bits : list or ndarray
        Original bit sequence (0s and 1s)
    received_bits : list or ndarray
        Received bit sequence (may have errors)

    Returns
    -------
    num_errors : int
        Number of bits that differ
    error_positions : list
        Indices where errors occurred
    """
    # Convert to numpy arrays for easy comparison
    tx_bits = np.array(transmitted_bits)
    rx_bits = np.array(received_bits)

    # Handle length mismatch (pad shorter sequence with zeros)
    # 🎓 In real systems, length mismatch is a big problem!
    # We handle it gracefully here for teaching purposes
    if len(tx_bits) != len(rx_bits):
        max_len = max(len(tx_bits), len(rx_bits))
        if len(tx_bits) < max_len:
            tx_bits = np.pad(tx_bits, (0, max_len - len(tx_bits)))
        if len(rx_bits) < max_len:
            rx_bits = np.pad(rx_bits, (0, max_len - len(rx_bits)))

    # Find where bits differ
    # 🎓 != operator creates boolean array: True where different
    errors = (tx_bits != rx_bits)

    # Count total errors
    num_errors = np.sum(errors)

    # Find positions of errors (useful for debugging!)
    error_positions = np.where(errors)[0].tolist()

    return int(num_errors), error_positions


def calculate_ber(transmitted_bits, received_bits):
    """
    Calculate Bit Error Rate (BER).

    🎓 TEACHING NOTE:
    BER is the fundamental quality metric in digital communications.
    It tells us: "What fraction of bits were received incorrectly?"

    Lower BER = better quality
    BER = 0 means perfect transmission
    BER = 0.5 means random garbage (worse than useless!)

    Parameters
    ----------
    transmitted_bits : list or ndarray
        Original bit sequence
    received_bits : list or ndarray
        Received bit sequence (may have errors)

    Returns
    -------
    ber : float
        Bit Error Rate (between 0.0 and 1.0)
    num_errors : int
        Number of bit errors
    total_bits : int
        Total number of bits compared
    """
    # Count errors
    num_errors, _ = count_bit_errors(transmitted_bits, received_bits)

    # Total bits is the maximum length (in case of mismatch)
    total_bits = max(len(transmitted_bits), len(received_bits))

    # Avoid division by zero
    if total_bits == 0:
        return 0.0, 0, 0

    # Calculate BER
    # 🎓 BER = errors / total
    ber = num_errors / total_bits

    return ber, num_errors, total_bits


def ber_to_quality_string(ber):
    """
    Convert BER to a human-readable quality assessment.

    🎓 TEACHING NOTE:
    Raw numbers like "0.001" aren't intuitive.
    This converts BER to descriptive quality ratings.

    Parameters
    ----------
    ber : float
        Bit Error Rate (0.0 to 1.0)

    Returns
    -------
    quality : str
        Quality description
    """
    if ber == 0.0:
        return "Perfect (0 errors)"
    elif ber < 1e-6:
        return "Excellent (< 1 error per million bits)"
    elif ber < 1e-3:
        return "Good (< 1 error per thousand bits)"
    elif ber < 0.01:
        return "Acceptable (< 1% error rate)"
    elif ber < 0.1:
        return "Poor (high error rate)"
    elif ber < 0.4:
        return "Very Poor (unusable)"
    else:
        return "Random Noise (worse than guessing)"


def print_error_report(transmitted_bits, received_bits, show_positions=False):
    """
    Generate a teaching-oriented error report.

    🎓 TEACHING NOTE:
    This creates a formatted report showing transmission quality.
    Perfect for learning and debugging!

    Parameters
    ----------
    transmitted_bits : list or ndarray
        Original bits
    received_bits : list or ndarray
        Received bits
    show_positions : bool
        If True, show where errors occurred

    Returns
    -------
    report : str
        Formatted error report
    """
    # Calculate metrics
    ber, num_errors, total_bits = calculate_ber(transmitted_bits, received_bits)
    _, error_positions = count_bit_errors(transmitted_bits, received_bits)
    quality = ber_to_quality_string(ber)

    # Build report
    report = "═" * 60 + "\n"
    report += "              BIT ERROR ANALYSIS REPORT\n"
    report += "═" * 60 + "\n"
    report += f"Total Bits Transmitted:  {total_bits}\n"
    report += f"Total Bit Errors:        {num_errors}\n"
    report += f"Bit Error Rate (BER):    {ber:.6f} ({ber*100:.4f}%)\n"
    report += f"Quality Assessment:      {quality}\n"

    if show_positions and error_positions and len(error_positions) <= 20:
        report += f"\nError Positions (indices): {error_positions}\n"
    elif show_positions and len(error_positions) > 20:
        report += f"\nError Positions: {len(error_positions)} errors "
        report += "(too many to show)\n"

    report += "═" * 60 + "\n"

    return report


def snr_db_to_estimated_ber_bpsk(snr_db):
    """
    Estimate theoretical BER for BPSK given SNR.

    🎓 TEACHING NOTE:
    For BPSK in AWGN channel, there's a theoretical relationship
    between SNR and BER. This helps us predict performance!

    Formula (approximate):
        BER ≈ Q(√(2 * SNR_linear))
    where Q() is the Q-function (tail of Gaussian distribution)

    This is a simplified version for teaching.

    Parameters
    ----------
    snr_db : float
        Signal-to-Noise Ratio in dB

    Returns
    -------
    estimated_ber : float
        Theoretical BER for this SNR
    """
    from scipy.special import erfc

    # Convert SNR from dB to linear
    snr_linear = 10 ** (snr_db / 10)

    # Calculate BER using Q-function approximation
    # 🎓 Q(x) ≈ (1/2) * erfc(x/√2)
    # For BPSK: BER = Q(√(2*SNR))
    ber = 0.5 * erfc(np.sqrt(snr_linear))

    return ber


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. BER > 0.5? Something is very wrong (phase inversion?)
#   2. BER = 0 but message is wrong? Check character encoding
#   3. Different lengths? Bits might be lost or duplicated
#
# Testing Tips:
#   - Test with no noise → should get BER = 0
#   - Test with high noise → should get BER ≈ 0.5
#   - Plot BER vs SNR to verify it matches theory
#   - Compare calculated vs theoretical BER
#
# Gotchas:
#   - BER is for BITS, not bytes or characters
#   - Even 1% BER can corrupt text badly
#   - FEC codes improve BER (coming in Phase 3!)


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Phase 3:
#   [ ] Symbol Error Rate (SER) calculations
#   [ ] BER after error correction
#   [ ] Confidence intervals for BER measurements
#
# For Advanced Version (ORBITER-1):
#   [ ] BER vs SNR curve plotting
#   [ ] Support for other modulations (QPSK, QAM)
#   [ ] Realistic BER estimation from actual signals
#   [ ] Error burst detection

