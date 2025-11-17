"""
═══════════════════════════════════════════════════════════════════
MODULE: comms/corruptor.py
PURPOSE: Deliberately inject errors for testing
THEME: Breaking things to learn how to fix them
═══════════════════════════════════════════════════════════════════

📡 STORY:
To test our error detection and correction, we need to CREATE errors!
This module provides controlled corruption for testing.

Think of this like:
  - Shaking a letter in the mail (bits get scrambled)
  - Dropping packages in transit (bytes go missing)
  - Rain blurring ink (burst errors)

Real satellite links experience all these kinds of errors!

ERROR TYPES:
┌──────────────────────────────────────────────────────────────┐
│ RANDOM BIT ERRORS                                            │
│   Before: 01001000  01100101  01101100  01101100             │
│   After:  01001001  01100101  01101100  01101100             │
│             ▲                                                 │
│         Single bit flipped                                    │
├──────────────────────────────────────────────────────────────┤
│ BURST ERRORS                                                  │
│   Before: ...01001000  01100101  01101100  01101100...       │
│   After:  ...01001000  ████████  ████████  01101100...       │
│                        └─ Corrupted ─┘                        │
│         Multiple consecutive bytes affected                   │
├──────────────────────────────────────────────────────────────┤
│ BYTE DROPS (Packet Loss)                                      │
│   Before: [Packet 1] [Packet 2] [Packet 3] [Packet 4]        │
│   After:  [Packet 1] [───────] [Packet 3] [Packet 4]         │
│                       ▲ Dropped                               │
└──────────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • Different types of errors (random, burst, dropout)
  • Testing error detection mechanisms
  • Understanding error patterns in real systems
  • How error rates affect communication quality

SIMPLIFICATIONS:
  - Errors are deterministic (can control exactly where)
  - No sophisticated fading models
  - Byte-level corruption (real systems have bit-level)

═══════════════════════════════════════════════════════════════════
"""

import random
import numpy as np


def flip_random_bits(data_bytes, bit_error_rate=0.01):
    """
    Flip random bits in data to simulate transmission errors.

    🎓 TEACHING NOTE:
    In real communications, noise can cause bits to flip.
    This simulates random bit errors (like AWGN channel effects).

    BER (Bit Error Rate) Examples:
    - 0.001 (0.1%) = Pretty good channel
    - 0.01  (1%)   = Marginal channel
    - 0.1   (10%)  = Very bad channel

    Parameters
    ----------
    data_bytes : bytes
        Data to corrupt
    bit_error_rate : float
        Probability of each bit being flipped (0.0 to 1.0)

    Returns
    -------
    corrupted : bytes
        Data with random bit flips
    """
    # Convert to mutable bytearray
    corrupted = bytearray(data_bytes)

    # Total number of bits
    total_bits = len(corrupted) * 8

    # 🎓 CALCULATE: How many bits to flip
    # This is probabilistic - each bit has BER chance of flipping
    bits_to_flip = []
    for bit_index in range(total_bits):
        if random.random() < bit_error_rate:
            bits_to_flip.append(bit_index)

    # 🎓 FLIP THE BITS
    for bit_index in bits_to_flip:
        # Which byte does this bit belong to?
        byte_index = bit_index // 8
        # Which bit within that byte?
        bit_position = bit_index % 8

        # Flip the bit using XOR
        # (XOR with 1 flips a bit: 0^1=1, 1^1=0)
        corrupted[byte_index] ^= (1 << bit_position)

    return bytes(corrupted)


def drop_bytes(data_bytes, byte_drop_rate=0.05):
    """
    Randomly drop (delete) bytes from data.

    🎓 TEACHING NOTE:
    Sometimes entire chunks of data just vanish!
    This simulates packet loss or severe fading.

    WHY THIS HAPPENS:
    - Buffer overflows
    - Deep fades
    - Interference bursts
    - Sync loss

    Parameters
    ----------
    data_bytes : bytes
        Data to corrupt
    byte_drop_rate : float
        Probability of each byte being dropped (0.0 to 1.0)

    Returns
    -------
    corrupted : bytes
        Data with random bytes removed
    """
    # 🎓 KEEP ONLY NON-DROPPED BYTES
    # For each byte, randomly decide if we keep it
    kept_bytes = []
    for byte in data_bytes:
        if random.random() > byte_drop_rate:
            kept_bytes.append(byte)

    return bytes(kept_bytes)


def burst_errors(data_bytes, num_bursts=2, burst_length=4):
    """
    Inject clustered errors (bursts) into data.

    🎓 TEACHING NOTE:
    Errors often come in BURSTS, not randomly distributed.
    Why? Because the channel conditions change over time:
    - Vehicle passes behind building → burst of errors
    - Lightning strike → burst of errors
    - Interference pulse → burst of errors

    Burst errors are HARDER to correct than random errors!

    Parameters
    ----------
    data_bytes : bytes
        Data to corrupt
    num_bursts : int
        Number of error bursts to inject
    burst_length : int
        Length of each burst in bytes

    Returns
    -------
    corrupted : bytes
        Data with burst errors
    """
    if len(data_bytes) == 0:
        return data_bytes

    corrupted = bytearray(data_bytes)

    # 🎓 INJECT EACH BURST
    for _ in range(num_bursts):
        # Pick random starting position
        # (Make sure burst doesn't go past end)
        max_start = max(0, len(corrupted) - burst_length)
        if max_start <= 0:
            continue

        burst_start = random.randint(0, max_start)

        # 🎓 CORRUPT: Randomize bytes in burst region
        # We'll completely randomize them (worst case scenario)
        for i in range(burst_start, min(burst_start + burst_length, len(corrupted))):
            corrupted[i] = random.randint(0, 255)

    return bytes(corrupted)


def corrupt_specific_byte(data_bytes, byte_index, new_value=None):
    """
    Corrupt a specific byte (useful for targeted testing).

    🎓 TEACHING NOTE:
    Sometimes we want to test SPECIFIC error scenarios:
    - What if the packet ID gets corrupted?
    - What if the CRC itself is wrong?
    - What if the preamble is damaged?

    This function lets us test these cases precisely.

    Parameters
    ----------
    data_bytes : bytes
        Data to corrupt
    byte_index : int
        Index of byte to corrupt
    new_value : int, optional
        New value for byte (0-255). If None, randomize it.

    Returns
    -------
    corrupted : bytes
        Data with specified byte corrupted
    """
    if byte_index >= len(data_bytes) or byte_index < 0:
        # Index out of bounds, return unchanged
        return data_bytes

    corrupted = bytearray(data_bytes)

    if new_value is None:
        # Randomize the byte
        new_value = random.randint(0, 255)
    else:
        # Use specified value
        new_value = new_value % 256

    corrupted[byte_index] = new_value

    return bytes(corrupted)


def add_noise_to_signal(signal_array, noise_power_db=-10):
    """
    Add Gaussian noise to a signal (for signal-level corruption).

    🎓 TEACHING NOTE:
    This is different from the other corruption functions!
    Those work on BITS/BYTES (after demodulation).
    This works on the SIGNAL itself (before demodulation).

    Use this to corrupt analog signals before they're decoded to bits.

    Parameters
    ----------
    signal_array : np.ndarray
        Signal samples
    noise_power_db : float
        Noise power in dB relative to signal

    Returns
    -------
    noisy_signal : np.ndarray
        Signal with added noise
    """
    # Calculate signal power
    signal_power = np.mean(signal_array ** 2)

    # Convert noise power from dB
    noise_power = signal_power * (10 ** (noise_power_db / 10))

    # Generate Gaussian noise
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal_array))

    # 🎓 ADD NOISE TO SIGNAL
    noisy_signal = signal_array + noise

    return noisy_signal


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. BER too high? Reduce bit_error_rate parameter
#   2. All bytes dropped? Check byte_drop_rate < 1.0
#   3. Bursts too short? Increase burst_length
#   4. Not enough errors? Increase num_bursts
#
# Testing Tips:
#   - Start with high error rates to see effects clearly
#   - Gradually reduce error rates to realistic levels
#   - Compare corrupted vs original using hexdump
#   - Test with different packet sizes
#   - Verify error detection triggers correctly
#
# Gotchas:
#   - Random corruption means results vary each run
#   - Set random.seed() for reproducible tests
#   - Burst errors can overlap (not prevented)
#   - Dropping bytes changes packet length!


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Add correlated error patterns (Markov model)
#   [ ] Implement Gilbert-Elliott burst model
#   [ ] Add frequency-selective fading
#   [ ] Support erasure markers (know which bytes are bad)
#   [ ] Add interleaver/deinterleaver testing
#
# For Deep Space Version:
#   [ ] Solar flare burst errors
#   [ ] Cosmic ray bit flips (single-event upsets)
#   [ ] Extremely long burst durations
