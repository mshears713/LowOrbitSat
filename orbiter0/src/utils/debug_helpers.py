"""
═══════════════════════════════════════════════════════════════════
MODULE: utils/debug_helpers.py
PURPOSE: Debugging tools for packet inspection and analysis
THEME: Making invisible bits visible and understandable
═══════════════════════════════════════════════════════════════════

📡 STORY:
When debugging communications, you need to SEE what's happening!
This module provides tools to inspect packets, compare data,
and understand errors.

Think of it like a microscope for digital data!

DEBUGGING TOOLS:
  • Hexdump (view bytes in hex format)
  • Packet comparison (find differences)
  • Bit visualization (see individual bits)
  • Error highlighting
  • Statistics reporting

LEARNING GOALS:
  • Understanding byte/bit representations
  • Debugging techniques for binary data
  • Difference detection
  • Visualization of digital data

═══════════════════════════════════════════════════════════════════
"""

from typing import List, Tuple
import sys
sys.path.insert(0, '..')
from comms.packetizer import parse_packet


def hexdump(data: bytes, bytes_per_line=16, show_ascii=True):
    """
    Create a hexdump of binary data (like hexdump -C).

    🎓 TEACHING NOTE:
    Hexdump shows bytes in hexadecimal format.
    It's the standard way to inspect binary data!

    Format:
    ADDRESS  | HEX VALUES                       | ASCII
    00000000 | AA AA AA AA 00 2A 00 11 44 ..   | .....*..D...

    Parameters
    ----------
    data : bytes
        Data to dump
    bytes_per_line : int
        How many bytes per line (default: 16)
    show_ascii : bool
        Whether to show ASCII representation

    Returns
    -------
    dump : str
        Formatted hexdump string
    """
    lines = []

    for i in range(0, len(data), bytes_per_line):
        # Get chunk of bytes
        chunk = data[i:i+bytes_per_line]

        # Format address (offset)
        address = f"{i:08x}"

        # Format hex bytes
        hex_bytes = ' '.join(f"{b:02x}" for b in chunk)
        # Pad if last line is short
        hex_bytes = hex_bytes.ljust(bytes_per_line * 3 - 1)

        # Format ASCII (printable chars only)
        if show_ascii:
            ascii_repr = ''.join(
                chr(b) if 32 <= b < 127 else '.'
                for b in chunk
            )
            line = f"{address}  {hex_bytes}  |{ascii_repr}|"
        else:
            line = f"{address}  {hex_bytes}"

        lines.append(line)

    return '\n'.join(lines)


def diff_bytes(data1: bytes, data2: bytes):
    """
    Find differences between two byte sequences.

    🎓 TEACHING NOTE:
    This shows you EXACTLY which bytes changed!
    Useful for debugging corruption.

    Parameters
    ----------
    data1 : bytes
        First data sequence
    data2 : bytes
        Second data sequence

    Returns
    -------
    differences : List[dict]
        List of differences: [{'offset': int, 'byte1': int, 'byte2': int}, ...]
    """
    max_len = max(len(data1), len(data2))
    differences = []

    for i in range(max_len):
        byte1 = data1[i] if i < len(data1) else None
        byte2 = data2[i] if i < len(data2) else None

        if byte1 != byte2:
            differences.append({
                'offset': i,
                'byte1': byte1,
                'byte2': byte2
            })

    return differences


def format_diff_report(data1: bytes, data2: bytes):
    """
    Create a human-readable diff report.

    🎓 TEACHING NOTE:
    Shows side-by-side comparison of two byte sequences.

    Parameters
    ----------
    data1 : bytes
        Original data
    data2 : bytes
        Modified data

    Returns
    -------
    report : str
        Formatted comparison report
    """
    diffs = diff_bytes(data1, data2)

    if not diffs:
        return "✓ Data sequences are identical"

    lines = [f"Found {len(diffs)} differences:"]
    lines.append(f"{'Offset':<10} {'Original':<12} {'Modified':<12} {'Change'}")
    lines.append("-" * 60)

    for diff in diffs[:20]:  # Limit to first 20 differences
        offset = diff['offset']
        b1 = diff['byte1']
        b2 = diff['byte2']

        if b1 is None:
            b1_str = "(missing)"
            change = "ADDED"
        else:
            b1_str = f"0x{b1:02X} ({b1})"

        if b2 is None:
            b2_str = "(missing)"
            change = "REMOVED"
        else:
            b2_str = f"0x{b2:02X} ({b2})"

        if b1 is not None and b2 is not None:
            # Show which bits flipped
            xor = b1 ^ b2
            bits_flipped = bin(xor).count('1')
            change = f"{bits_flipped} bit(s)"

        lines.append(f"{offset:<10} {b1_str:<12} {b2_str:<12} {change}")

    if len(diffs) > 20:
        lines.append(f"... and {len(diffs) - 20} more differences")

    return '\n'.join(lines)


def inspect_packet(packet_bytes: bytes):
    """
    Detailed inspection of a packet structure.

    🎓 TEACHING NOTE:
    Shows you everything inside a packet!
    - Structure breakdown
    - Field values
    - CRC status
    - Hexdump

    Parameters
    ----------
    packet_bytes : bytes
        Packet to inspect

    Returns
    -------
    report : str
        Detailed inspection report
    """
    lines = ["═" * 60]
    lines.append("PACKET INSPECTION")
    lines.append("═" * 60)

    # Basic info
    lines.append(f"\nTotal size: {len(packet_bytes)} bytes")

    # Parse packet
    parsed = parse_packet(packet_bytes)

    # Preamble
    lines.append("\n[PREAMBLE] (bytes 0-3):")
    preamble = packet_bytes[:4]
    lines.append(f"  Hex: {' '.join(f'{b:02X}' for b in preamble)}")
    lines.append(f"  Expected: AA AA AA AA")
    if preamble == b'\xAA\xAA\xAA\xAA':
        lines.append("  ✓ Valid")
    else:
        lines.append("  ✗ INVALID!")

    # Header
    if 'packet_id' in parsed:
        lines.append("\n[HEADER] (bytes 4-11):")
        lines.append(f"  Packet ID: {parsed['packet_id']}")
        lines.append(f"  Payload length: {parsed.get('payload_length', 'N/A')} bytes")
        lines.append(f"  Timestamp: {parsed.get('timestamp', 'N/A')}")

    # Payload
    if 'payload' in parsed:
        payload = parsed['payload']
        lines.append("\n[PAYLOAD]:")
        lines.append(f"  Length: {len(payload)} bytes")
        if payload:
            # Try to decode as text
            try:
                text = payload.decode('utf-8')
                lines.append(f"  Text: \"{text}\"")
            except:
                lines.append(f"  Text: (non-UTF8 data)")
            lines.append(f"  Hex: {payload.hex()}")

    # CRC
    if 'crc_valid' in parsed:
        lines.append("\n[CRC] (last 2 bytes):")
        lines.append(f"  Received: 0x{parsed.get('crc_received', 0):04X}")
        lines.append(f"  Calculated: 0x{parsed.get('crc_calculated', 0):04X}")
        if parsed['crc_valid']:
            lines.append("  ✓ CRC Valid")
        else:
            lines.append("  ✗ CRC MISMATCH!")

    # Full hexdump
    lines.append("\n" + "─" * 60)
    lines.append("HEXDUMP:")
    lines.append(hexdump(packet_bytes))

    lines.append("═" * 60)

    return '\n'.join(lines)


def bits_to_string(byte_value: int):
    """
    Convert a byte to binary string representation.

    🎓 TEACHING NOTE:
    Shows individual bits in a byte.
    Useful for understanding bit-level operations!

    Parameters
    ----------
    byte_value : int
        Byte value (0-255)

    Returns
    -------
    bits : str
        Binary representation (e.g., "10101010")
    """
    return f"{byte_value:08b}"


def visualize_bit_errors(original: bytes, corrupted: bytes):
    """
    Visualize bit-level differences between two byte sequences.

    🎓 TEACHING NOTE:
    Shows EXACTLY which bits flipped!
    Each difference is highlighted.

    Parameters
    ----------
    original : bytes
        Original data
    corrupted : bytes
        Corrupted data

    Returns
    -------
    visualization : str
        Visual comparison showing bit flips
    """
    lines = ["BIT-LEVEL ERROR VISUALIZATION"]
    lines.append("─" * 60)

    max_len = min(len(original), len(corrupted), 10)  # Limit to first 10 bytes

    for i in range(max_len):
        orig_byte = original[i]
        corr_byte = corrupted[i]

        orig_bits = bits_to_string(orig_byte)
        corr_bits = bits_to_string(corr_byte)

        # Highlight differences
        highlight = ''.join(
            '^' if ob != cb else ' '
            for ob, cb in zip(orig_bits, corr_bits)
        )

        lines.append(f"\nByte {i}:")
        lines.append(f"  Original:  {orig_bits}  (0x{orig_byte:02X})")
        lines.append(f"  Corrupted: {corr_bits}  (0x{corr_byte:02X})")
        lines.append(f"  Errors:    {highlight}")

    if len(original) > 10:
        lines.append(f"\n... ({len(original) - 10} more bytes)")

    return '\n'.join(lines)


def compare_packets(packet1: bytes, packet2: bytes):
    """
    High-level packet comparison.

    🎓 TEACHING NOTE:
    Compares packets field-by-field.
    Shows which parts differ (header vs payload vs CRC).

    Parameters
    ----------
    packet1 : bytes
        First packet
    packet2 : bytes
        Second packet

    Returns
    -------
    comparison : dict
        {
            'identical': bool,
            'size_match': bool,
            'preamble_match': bool,
            'header_match': bool,
            'payload_match': bool,
            'crc_match': bool
        }
    """
    # Parse both packets
    p1 = parse_packet(packet1)
    p2 = parse_packet(packet2)

    comparison = {
        'identical': packet1 == packet2,
        'size_match': len(packet1) == len(packet2),
        'preamble_match': packet1[:4] == packet2[:4] if len(packet1) >= 4 and len(packet2) >= 4 else False,
        'header_match': (
            p1.get('packet_id') == p2.get('packet_id') and
            p1.get('payload_length') == p2.get('payload_length') and
            p1.get('timestamp') == p2.get('timestamp')
        ),
        'payload_match': p1.get('payload') == p2.get('payload'),
        'crc_match': p1.get('crc_received') == p2.get('crc_received')
    }

    return comparison


# ═══ DEBUGGING NOTES ═══
#
# Common Uses:
#   1. hexdump() - First thing to do when debugging binary data
#   2. inspect_packet() - Quick packet overview
#   3. diff_bytes() - Find corruption locations
#   4. visualize_bit_errors() - Understand bit-level changes
#
# Tips:
#   - Always hexdump both original and corrupted data
#   - Look for patterns in bit errors (random vs burst)
#   - Check if errors align with byte boundaries
#   - Compare parsed fields, not just raw bytes
#
# Gotchas:
#   - Hexdump is base-16, not base-10
#   - Byte order matters (big-endian vs little-endian)
#   - ASCII display can be misleading for binary data
