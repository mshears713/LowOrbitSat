"""
═══════════════════════════════════════════════════════════════════
MODULE: comms/cleaner.py
PURPOSE: Error detection using checksums and CRC
THEME: Detecting when packets are corrupted
═══════════════════════════════════════════════════════════════════

📡 STORY:
Error DETECTION: Knowing something went wrong
(Different from CORRECTION: Fixing what went wrong)

This module provides validation and cleaning functions for received data.
Think of it as "quality control" for incoming packets!

ERROR DETECTION VS CORRECTION:
┌──────────────────────────────────────────────────────────────┐
│ DETECTION (this module):                                     │
│   ✓ Can tell if data is corrupted                           │
│   ✗ Cannot fix the corruption                               │
│   Example: CRC, checksum, parity check                       │
│                                                               │
│ CORRECTION (decoder.py):                                      │
│   ✓ Can tell if data is corrupted                           │
│   ✓ Can sometimes fix the corruption                         │
│   Example: Hamming codes, Reed-Solomon                       │
└──────────────────────────────────────────────────────────────┘

DETECTION METHODS:
┌──────────────────────────────────────────────────────────────┐
│ SIMPLE CHECKSUM:                                             │
│   Add all bytes, check sum                                   │
│   ✓ Fast, simple                                             │
│   ✗ Weak (can miss errors)                                   │
│                                                               │
│ CRC-16 (what we use):                                         │
│   Polynomial division over data                              │
│   ✓ Detects 99.998% of errors                                │
│   ✓ Industry standard                                        │
│   ✗ Slightly more complex                                    │
│                                                               │
│ CRC-32:                                                       │
│   Longer CRC (32 bits)                                        │
│   ✓ Even more robust                                         │
│   ✗ More overhead (4 bytes vs 2)                             │
└──────────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • Difference between detection and correction
  • How checksums work
  • CRC algorithm basics
  • Limitations of error detection
  • Batch processing of packets
  • Error statistics and reporting

SIMPLIFICATIONS:
  - Uses CRC from packetizer module (no reimplementation)
  - Simple pass/fail validation
  - No soft decision making

═══════════════════════════════════════════════════════════════════
"""

from typing import List, Dict
from .packetizer import parse_packet, validate_packet


def validate_packet_batch(packet_list: List[bytes]) -> Dict:
    """
    Validate a batch of packets and compute statistics.

    🎓 TEACHING NOTE:
    In real systems, packets arrive in batches.
    We need to:
    1. Check each packet
    2. Separate good from bad
    3. Compute error rates

    This is like quality control on an assembly line!

    Parameters
    ----------
    packet_list : List[bytes]
        List of packets to validate

    Returns
    -------
    results : dict
        {
            'total_packets': int,
            'valid_packets': int,
            'invalid_packets': int,
            'packet_error_rate': float,  # 0.0 to 1.0
            'valid_indices': List[int],  # Which packets are good
            'invalid_indices': List[int]  # Which packets are bad
        }
    """
    total = len(packet_list)
    valid_indices = []
    invalid_indices = []

    # 🎓 VALIDATE EACH PACKET
    for i, packet in enumerate(packet_list):
        if validate_packet(packet):
            valid_indices.append(i)
        else:
            invalid_indices.append(i)

    valid_count = len(valid_indices)
    invalid_count = len(invalid_indices)

    # 🎓 PACKET ERROR RATE (PER)
    # Percentage of packets that are corrupted
    per = invalid_count / total if total > 0 else 0.0

    return {
        'total_packets': total,
        'valid_packets': valid_count,
        'invalid_packets': invalid_count,
        'packet_error_rate': per,
        'valid_indices': valid_indices,
        'invalid_indices': invalid_indices
    }


def filter_valid_packets(packet_list: List[bytes]) -> List[bytes]:
    """
    Filter out corrupted packets, return only valid ones.

    🎓 TEACHING NOTE:
    Sometimes we just discard bad packets.
    This is called "ARQ" (Automatic Repeat reQuest) in real systems.

    If a packet fails CRC:
    - Option 1: Discard it (what this function does)
    - Option 2: Request retransmission
    - Option 3: Try to correct it (FEC)

    Parameters
    ----------
    packet_list : List[bytes]
        Mixed valid and invalid packets

    Returns
    -------
    valid_packets : List[bytes]
        Only packets that passed CRC check
    """
    # 🎓 FILTER: Keep only valid packets
    return [pkt for pkt in packet_list if validate_packet(pkt)]


def compute_simple_checksum(data: bytes) -> int:
    """
    Compute a simple additive checksum.

    🎓 TEACHING NOTE:
    This is the SIMPLEST form of error detection.
    Add up all byte values, return the sum.

    WEAKNESS: Can miss errors!
    Example: If two bytes flip in opposite directions,
    the checksum might still be correct.

    Real systems use CRC instead, but checksums are
    good for understanding the concept.

    Parameters
    ----------
    data : bytes
        Data to checksum

    Returns
    -------
    checksum : int
        Sum of all bytes (modulo 256)
    """
    # 🎓 SIMPLE SUM
    # Add all bytes, keep only lower 8 bits (mod 256)
    checksum = sum(data) % 256
    return checksum


def verify_simple_checksum(data: bytes, expected_checksum: int) -> bool:
    """
    Verify data against a simple checksum.

    🎓 TEACHING NOTE:
    Compare calculated checksum to expected value.
    Match = probably OK
    Mismatch = definitely corrupted

    Parameters
    ----------
    data : bytes
        Data to verify
    expected_checksum : int
        The checksum value to compare against

    Returns
    -------
    valid : bool
        True if checksum matches
    """
    calculated = compute_simple_checksum(data)
    return calculated == expected_checksum


def analyze_packet_quality(packet_list: List[bytes]) -> Dict:
    """
    Detailed quality analysis of packet batch.

    🎓 TEACHING NOTE:
    Beyond just "good" or "bad", we can analyze patterns:
    - Are errors clustered? (burst errors)
    - Are errors evenly distributed? (random errors)
    - What's the overall quality?

    This helps diagnose channel problems!

    Parameters
    ----------
    packet_list : List[bytes]
        Packets to analyze

    Returns
    -------
    analysis : dict
        Detailed quality metrics
    """
    if not packet_list:
        return {'error': 'No packets provided'}

    total = len(packet_list)
    parsed_packets = []
    crc_failures = []

    # Parse all packets
    for i, pkt in enumerate(packet_list):
        parsed = parse_packet(pkt)
        parsed_packets.append(parsed)
        if not parsed.get('crc_valid', False):
            crc_failures.append(i)

    # Compute statistics
    num_failures = len(crc_failures)
    failure_rate = num_failures / total if total > 0 else 0.0

    # 🎓 DETECT BURST ERRORS
    # If failures are clustered, it's likely burst errors
    # If they're spread out, it's likely random errors
    burst_detected = False
    if len(crc_failures) >= 2:
        # Check if consecutive failures exist
        for i in range(len(crc_failures) - 1):
            if crc_failures[i+1] - crc_failures[i] == 1:
                burst_detected = True
                break

    # Overall quality assessment
    if failure_rate == 0.0:
        quality = "Excellent"
    elif failure_rate < 0.01:
        quality = "Good"
    elif failure_rate < 0.1:
        quality = "Fair"
    elif failure_rate < 0.5:
        quality = "Poor"
    else:
        quality = "Very Poor"

    return {
        'total_packets': total,
        'successful_packets': total - num_failures,
        'failed_packets': num_failures,
        'packet_error_rate': failure_rate,
        'burst_errors_detected': burst_detected,
        'quality_rating': quality,
        'failed_packet_indices': crc_failures
    }


def extract_valid_payloads(packet_list: List[bytes]) -> List[bytes]:
    """
    Extract payloads from all valid packets.

    🎓 TEACHING NOTE:
    This is the final step in reception:
    1. Receive packets
    2. Validate CRC
    3. Extract payload from good packets
    4. Discard bad packets

    Parameters
    ----------
    packet_list : List[bytes]
        Received packets

    Returns
    -------
    payloads : List[bytes]
        Payloads from valid packets only
    """
    payloads = []

    for packet in packet_list:
        parsed = parse_packet(packet)

        # 🎓 ONLY KEEP VALID PAYLOADS
        if parsed.get('crc_valid', False):
            payloads.append(parsed['payload'])

    return payloads


def detect_preamble_sync_errors(packet_list: List[bytes]) -> Dict:
    """
    Detect synchronization issues (preamble errors).

    🎓 TEACHING NOTE:
    Sometimes the PREAMBLE gets corrupted, not the data!
    This makes the receiver lose sync - it can't find where
    packets start.

    This is different from CRC errors (data corruption).

    Parameters
    ----------
    packet_list : List[bytes]
        Packets to check

    Returns
    -------
    results : dict
        Sync error statistics
    """
    preamble_errors = 0
    crc_errors = 0
    both_errors = 0
    total = len(packet_list)

    expected_preamble = b'\xAA\xAA\xAA\xAA'

    for packet in packet_list:
        has_preamble_error = False
        has_crc_error = False

        # Check preamble
        if len(packet) >= 4:
            if packet[:4] != expected_preamble:
                has_preamble_error = True
                preamble_errors += 1

        # Check CRC
        if not validate_packet(packet):
            has_crc_error = True
            crc_errors += 1

        # Both?
        if has_preamble_error and has_crc_error:
            both_errors += 1

    return {
        'total_packets': total,
        'preamble_errors': preamble_errors,
        'crc_errors': crc_errors,
        'both_errors': both_errors,
        'preamble_error_rate': preamble_errors / total if total > 0 else 0.0,
        'crc_error_rate': crc_errors / total if total > 0 else 0.0
    }


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. All packets failing? Check if corruption happened before packetization
#   2. Intermittent failures? Check for burst errors vs random errors
#   3. High PER but low BER? Problem might be in sync, not data
#   4. Simple checksum weak? Use CRC instead
#
# Testing Tips:
#   - Start with known-good packets
#   - Add controlled corruption
#   - Check that detection triggers correctly
#   - Test batch processing with mixed good/bad packets
#   - Compare simple checksum vs CRC effectiveness
#
# Gotchas:
#   - CRC doesn't correct, only detects
#   - Multiple errors can cancel out in checksums
#   - Burst errors often defeat simple checksums
#   - Packet error rate != bit error rate


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] CRC-32 support for longer packets
#   [ ] Fletcher checksum implementation
#   [ ] Adler-32 checksum
#   [ ] Automatic error pattern detection
#   [ ] Adaptive quality thresholds
#   [ ] Real-time quality monitoring
#
# For Deep Space Version:
#   [ ] Consultative Committee for Space Data Systems (CCSDS) checksums
#   [ ] Frame synchronization detection
#   [ ] Viterbi soft-decision integration
#   [ ] Interleaver/deinterleaver support
