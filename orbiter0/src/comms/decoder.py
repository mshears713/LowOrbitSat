"""
═══════════════════════════════════════════════════════════════════
MODULE: comms/decoder.py
PURPOSE: Forward Error Correction (FEC) implementation
THEME: Not just detecting errors - FIXING them!
═══════════════════════════════════════════════════════════════════

📡 STORY:
FEC (Forward Error Correction) adds redundancy so we can
CORRECT errors without retransmission.

Think of it like: "I s_nt you a m_ssage"
Even with missing letters, you can figure it out!

We implement simple FEC:
  • Parity bits (detect single errors)
  • Hamming(7,4) code (correct single errors)

ERROR DETECTION VS CORRECTION:
┌──────────────────────────────────────────────────────────────┐
│ CRC (Detection Only):                                         │
│   Input:  "Hello"                                            │
│   Output: "Hello" + CRC                                       │
│   If corrupted: ✗ Detected, ✗ Cannot fix                     │
│                                                               │
│ HAMMING (Correction):                                         │
│   Input:  4 bits → [1011]                                    │
│   Output: 7 bits → [1011001] (3 parity bits added)           │
│   If 1 bit corrupted: ✓ Detected, ✓ Corrected!               │
└──────────────────────────────────────────────────────────────┘

HAMMING(7,4) STRUCTURE:
┌──────────────────────────────────────────────────────────┐
│ Position:  1  2  3  4  5  6  7                           │
│ Type:      P  P  D  P  D  D  D                           │
│                                                           │
│ P = Parity bit (calculated)                              │
│ D = Data bit (your actual data)                          │
│                                                           │
│ 4 data bits → 7 total bits = 4/7 = 57% efficiency        │
│ Overhead = 3 parity bits                                 │
└──────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • How redundancy enables correction
  • Trade-off: bandwidth vs reliability
  • Hamming distance concept
  • Limits of error correction

SIMPLIFICATIONS:
  - Only Hamming(7,4) (simplest useful code)
  - Can correct 1 bit error, detect 2 bit errors
  - Not optimized for speed

═══════════════════════════════════════════════════════════════════
"""

import numpy as np


def add_parity_bit(data_bits):
    """
    Add a simple parity bit to data.

    🎓 TEACHING NOTE:
    Parity is the SIMPLEST error detection.
    Count the 1s in the data:
    - Even number of 1s → parity = 0
    - Odd number of 1s → parity = 1

    This ensures the total (data + parity) always has EVEN parity.

    LIMITATION: Can only DETECT single-bit errors, not CORRECT them.

    Parameters
    ----------
    data_bits : list of int
        Data bits (each 0 or 1)

    Returns
    -------
    encoded : list of int
        Data bits + parity bit at end
    """
    # 🎓 COUNT THE 1s
    num_ones = sum(data_bits)

    # 🎓 PARITY BIT
    # Make total number of 1s even
    parity = num_ones % 2

    return data_bits + [parity]


def check_parity_bit(encoded_bits):
    """
    Check if parity is correct (error detection).

    🎓 TEACHING NOTE:
    If the total number of 1s is ODD, there's an error!
    (Because we ensured even parity when encoding)

    Parameters
    ----------
    encoded_bits : list of int
        Data + parity bit

    Returns
    -------
    is_valid : bool
        True if parity is correct
    """
    # 🎓 COUNT ALL 1s
    num_ones = sum(encoded_bits)

    # 🎓 CHECK PARITY
    # Should be even
    return (num_ones % 2) == 0


def hamming_encode_4bit(data_bits):
    """
    Encode 4 data bits using Hamming(7,4) code.

    🎓 TEACHING NOTE:
    Hamming(7,4) is the SMALLEST useful error-correcting code.

    We take 4 data bits and add 3 parity bits.
    The magic is WHERE we place the parity bits!

    Positions (1-indexed):
    1 = parity  (p1)
    2 = parity  (p2)
    3 = data    (d1)
    4 = parity  (p3)
    5 = data    (d2)
    6 = data    (d3)
    7 = data    (d4)

    Each parity bit covers certain positions:
    p1 covers: 1,3,5,7   (positions with bit 0 set in binary)
    p2 covers: 2,3,6,7   (positions with bit 1 set in binary)
    p3 covers: 4,5,6,7   (positions with bit 2 set in binary)

    Parameters
    ----------
    data_bits : list of int
        4 data bits [d1, d2, d3, d4]

    Returns
    -------
    encoded : list of int
        7 bits [p1, p2, d1, p3, d2, d3, d4]
    """
    if len(data_bits) != 4:
        raise ValueError("Hamming(7,4) requires exactly 4 data bits")

    d1, d2, d3, d4 = data_bits

    # 🎓 CALCULATE PARITY BITS
    # p1 covers positions 1,3,5,7 → covers d1, d2, d4
    p1 = (d1 ^ d2 ^ d4) % 2

    # p2 covers positions 2,3,6,7 → covers d1, d3, d4
    p2 = (d1 ^ d3 ^ d4) % 2

    # p3 covers positions 4,5,6,7 → covers d2, d3, d4
    p3 = (d2 ^ d3 ^ d4) % 2

    # 🎓 ASSEMBLE CODEWORD
    # Position: 1   2   3   4   5   6   7
    encoded = [p1, p2, d1, p3, d2, d3, d4]

    return encoded


def hamming_decode_4bit(encoded_bits):
    """
    Decode and correct Hamming(7,4) code.

    🎓 TEACHING NOTE:
    This is where the MAGIC happens!

    We recalculate the parity bits and compare to received ones.
    The differences tell us WHICH bit (if any) is wrong!

    SYNDROME CALCULATION:
    Compare received vs calculated parity:
    - All match → No error
    - Mismatch → Syndrome points to error position

    Can correct: 1-bit errors
    Can detect: 2-bit errors (but can't correct them)

    Parameters
    ----------
    encoded_bits : list of int
        7 received bits (possibly corrupted)

    Returns
    -------
    result : dict
        {
            'data_bits': [d1, d2, d3, d4],
            'error_detected': bool,
            'error_corrected': bool,
            'error_position': int or None
        }
    """
    if len(encoded_bits) != 7:
        raise ValueError("Hamming(7,4) requires exactly 7 encoded bits")

    # Extract received bits
    r1, r2, r3, r4, r5, r6, r7 = encoded_bits

    # 🎓 RECALCULATE PARITY BITS
    # These are what the parity bits SHOULD be
    # based on the data bits we received

    # p1 should cover positions 1,3,5,7
    calc_p1 = (r3 ^ r5 ^ r7) % 2

    # p2 should cover positions 2,3,6,7
    calc_p2 = (r3 ^ r6 ^ r7) % 2

    # p3 should cover positions 4,5,6,7
    calc_p3 = (r5 ^ r6 ^ r7) % 2

    # 🎓 SYNDROME CALCULATION
    # XOR received parity with calculated parity
    s1 = r1 ^ calc_p1
    s2 = r2 ^ calc_p2
    s3 = r4 ^ calc_p3

    # 🎓 SYNDROME → ERROR POSITION
    # The syndrome IS the error position in binary!
    # s3 s2 s1 → position (1-indexed)
    syndrome = s3 * 4 + s2 * 2 + s1

    error_detected = (syndrome != 0)
    error_position = syndrome if error_detected else None

    # 🎓 ERROR CORRECTION
    corrected = encoded_bits.copy()
    if error_detected and 1 <= syndrome <= 7:
        # Flip the erroneous bit
        corrected[syndrome - 1] ^= 1

    # Extract data bits from corrected codeword
    # Positions 3, 5, 6, 7 (indices 2, 4, 5, 6)
    data_bits = [corrected[2], corrected[4], corrected[5], corrected[6]]

    return {
        'data_bits': data_bits,
        'error_detected': error_detected,
        'error_corrected': error_detected,
        'error_position': error_position,
        'syndrome': syndrome
    }


def encode_bytes_with_hamming(data_bytes):
    """
    Encode bytes using Hamming(7,4) code.

    🎓 TEACHING NOTE:
    Real data is BYTES, not just 4 bits!
    We process bytes in 4-bit chunks (nibbles):

    1 byte = 8 bits = 2 nibbles
    Each nibble → Hamming(7,4) → 7 bits
    So 1 byte → 14 bits encoded

    Overhead: 75% increase in size!

    Parameters
    ----------
    data_bytes : bytes
        Data to encode

    Returns
    -------
    encoded_bits : list of int
        Hamming-encoded bits
    """
    encoded_bits = []

    for byte in data_bytes:
        # Split byte into two 4-bit nibbles
        high_nibble = [(byte >> (7 - i)) & 1 for i in range(4)]
        low_nibble = [(byte >> (3 - i)) & 1 for i in range(4)]

        # Encode each nibble
        encoded_high = hamming_encode_4bit(high_nibble)
        encoded_low = hamming_encode_4bit(low_nibble)

        # Add to output
        encoded_bits.extend(encoded_high)
        encoded_bits.extend(encoded_low)

    return encoded_bits


def decode_bytes_with_hamming(encoded_bits):
    """
    Decode Hamming(7,4) encoded bits back to bytes.

    🎓 TEACHING NOTE:
    Reverse of encode_bytes_with_hamming().

    Process 14 bits at a time:
    - First 7 bits → decode to high nibble (4 bits)
    - Next 7 bits → decode to low nibble (4 bits)
    - Combine nibbles → 1 byte

    Parameters
    ----------
    encoded_bits : list of int
        Hamming-encoded bits

    Returns
    -------
    result : dict
        {
            'data_bytes': bytes,
            'errors_corrected': int,
            'total_chunks': int
        }
    """
    if len(encoded_bits) % 14 != 0:
        # Pad with zeros if needed
        padding = 14 - (len(encoded_bits) % 14)
        encoded_bits = encoded_bits + [0] * padding

    data_bytes = []
    errors_corrected = 0
    total_chunks = len(encoded_bits) // 14

    for i in range(total_chunks):
        # Extract 14 bits (2 Hamming codewords)
        start = i * 14
        high_codeword = encoded_bits[start:start+7]
        low_codeword = encoded_bits[start+7:start+14]

        # Decode each nibble
        high_result = hamming_decode_4bit(high_codeword)
        low_result = hamming_decode_4bit(low_codeword)

        # Count corrections
        if high_result['error_corrected']:
            errors_corrected += 1
        if low_result['error_corrected']:
            errors_corrected += 1

        # Reconstruct byte
        high_nibble = high_result['data_bits']
        low_nibble = low_result['data_bits']

        byte_value = 0
        for bit in high_nibble:
            byte_value = (byte_value << 1) | bit
        for bit in low_nibble:
            byte_value = (byte_value << 1) | bit

        data_bytes.append(byte_value)

    return {
        'data_bytes': bytes(data_bytes),
        'errors_corrected': errors_corrected,
        'total_chunks': total_chunks,
        'correction_rate': errors_corrected / (total_chunks * 2) if total_chunks > 0 else 0.0
    }


def demonstrate_hamming_correction():
    """
    Demonstrate Hamming code correcting an error.

    🎓 TEACHING NOTE:
    This shows the "magic" of error correction!
    We deliberately introduce an error and watch it get fixed.
    """
    print("=" * 60)
    print("HAMMING(7,4) ERROR CORRECTION DEMONSTRATION")
    print("=" * 60)

    # Original data
    data = [1, 0, 1, 1]
    print(f"\nOriginal data (4 bits): {data}")

    # Encode
    encoded = hamming_encode_4bit(data)
    print(f"Encoded (7 bits):       {encoded}")
    print(f"  Parity bits: {[encoded[0], encoded[1], encoded[3]]}")
    print(f"  Data bits:   {[encoded[2], encoded[4], encoded[5], encoded[6]]}")

    # Introduce error
    error_position = 5  # Flip bit at position 5 (index 4)
    corrupted = encoded.copy()
    corrupted[error_position - 1] ^= 1
    print(f"\nCorrupted (error at position {error_position}): {corrupted}")

    # Decode and correct
    result = hamming_decode_4bit(corrupted)
    print(f"\nDecoding:")
    print(f"  Error detected: {result['error_detected']}")
    print(f"  Error position: {result['error_position']}")
    print(f"  Corrected data: {result['data_bits']}")
    print(f"  Original data:  {data}")
    print(f"  Match: {result['data_bits'] == data}")


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Hamming can't correct 2+ bit errors (will give wrong result!)
#   2. Parity only detects, doesn't correct
#   3. Byte encoding increases size by 75%
#   4. Position indexing is 1-based (not 0-based)
#
# Testing Tips:
#   - Test with all-zeros and all-ones data
#   - Introduce single-bit errors and verify correction
#   - Try double-bit errors (should fail gracefully)
#   - Compare encoded size to original size
#   - Verify no errors → data unchanged
#
# Gotchas:
#   - Hamming(7,4) works on 4-bit chunks only
#   - More than 1 error = correction FAILS
#   - Syndrome 0 = no error
#   - Position counting starts at 1, not 0


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Hamming(15,11) for better efficiency
#   [ ] Reed-Solomon codes (byte-level correction)
#   [ ] Convolutional codes
#   [ ] Turbo codes
#   [ ] LDPC (Low-Density Parity-Check) codes
#
# For Deep Space Version:
#   [ ] Concatenated codes (RS + convolutional)
#   [ ] Interleaving for burst error protection
#   [ ] Soft-decision decoding
#   [ ] Rate-adaptive coding
