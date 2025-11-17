"""
═══════════════════════════════════════════════════════════════════
MODULE: comms/packetizer.py
PURPOSE: Structure data into packets with headers and checksums
THEME: Organizing bits into neat, labeled packages
═══════════════════════════════════════════════════════════════════

📡 STORY:
You can't just throw random bits into space and hope for the best!
Real systems organize data into PACKETS - structured bundles with:
  - A header (who, what, when)
  - The actual data (payload)
  - A checksum (is it correct?)

Think of packets like mailing a letter:
  - Header = address and return address
  - Payload = the letter itself
  - Checksum = delivery confirmation

PACKET STRUCTURE:
┌──────────────────────────────────────────┐
│ PREAMBLE (sync pattern)  │ 4 bytes       │  ← "Hey, packet starting!"
├──────────────────────────────────────────┤
│ HEADER                   │ 8 bytes       │
│   - Packet ID            │ (2 bytes)     │  ← Unique identifier
│   - Length               │ (2 bytes)     │  ← How many data bytes
│   - Timestamp            │ (4 bytes)     │  ← When was this sent
├──────────────────────────────────────────┤
│ PAYLOAD                  │ N bytes       │  ← The actual message
├──────────────────────────────────────────┤
│ CRC-16 Checksum          │ 2 bytes       │  ← Error detection
└──────────────────────────────────────────┘

Total overhead: 14 bytes per packet

LEARNING GOALS:
  • Why we need packet structure
  • Header fields and their purposes
  • Checksums for error detection
  • Framing and synchronization
  • Trade-off between overhead and robustness

SIMPLIFICATIONS:
  - Fixed header format (real systems are more flexible)
  - Simple CRC-16 (real systems might use CRC-32)
  - No fragmentation/reassembly yet
  - No sequence numbers for ordering (added later if needed)

═══════════════════════════════════════════════════════════════════
"""

# ┌────────────────────────────────────────────────────────┐
# │              PACKETIZATION PROCESS                     │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │  Raw Bytes ──► Add Header ──► Add CRC ──► Packet      │
# │                                                        │
# │  "Hello"   ──► [ID|Len|Time] ──► [CRC] ──► Complete   │
# │  (5 bytes)     + Hello           (2B)      (19 bytes)  │
# │                (12 bytes)                              │
# │                                                        │
# └────────────────────────────────────────────────────────┘

# ┌────────────────────────────────────────────────────────┐
# │              DEPACKETIZATION PROCESS                   │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │  Packet ──► Verify CRC ──► Extract Payload ──► Bytes  │
# │                  │                                     │
# │                  ├─ OK ──► Success                     │
# │                  └─ BAD ──► Discard/Request Retx       │
# │                                                        │
# └────────────────────────────────────────────────────────┘


def create_packet(payload_bytes, packet_id=0, timestamp=None):
    """
    Create a packet with header, payload, and checksum.

    🎓 TEACHING NOTE:
    This function takes raw data and wraps it in a protective
    structure. Think of it like putting a letter in an envelope
    with an address.

    Steps:
    1. Create preamble (sync pattern: 0xAA 0xAA 0xAA 0xAA)
    2. Build header (ID, length, timestamp)
    3. Attach payload
    4. Calculate CRC over header + payload
    5. Append CRC

    WHY PREAMBLE?
    The receiver needs to know where a packet starts.
    The preamble is a distinctive pattern that's easy to detect.

    Parameters
    ----------
    payload_bytes : bytes
        Data to transmit
    packet_id : int
        Unique packet identifier (0-65535)
    timestamp : float, optional
        Unix timestamp (auto-generated if None)

    Returns
    -------
    packet : bytes
        Complete packet ready for transmission
    """
    # Implementation coming in Phase 3
    pass


def parse_packet(packet_bytes):
    """
    Parse a received packet into its components.

    🎓 TEACHING NOTE:
    Reverse of create_packet().
    Extract each field and verify the structure is valid.

    Steps:
    1. Check preamble
    2. Extract header fields
    3. Extract payload
    4. Verify CRC

    Parameters
    ----------
    packet_bytes : bytes
        Raw received packet

    Returns
    -------
    packet_dict : dict
        {
            'packet_id': int,
            'timestamp': float,
            'payload': bytes,
            'crc_valid': bool
        }
    """
    # Implementation coming in Phase 3
    pass


def validate_packet(packet_bytes):
    """
    Check if a packet is well-formed and uncorrupted.

    🎓 TEACHING NOTE:
    Quick validation without full parsing.
    Checks:
    - Minimum length
    - Preamble present
    - CRC matches

    Parameters
    ----------
    packet_bytes : bytes
        Packet to validate

    Returns
    -------
    valid : bool
        True if packet passes all checks
    """
    # Implementation coming in Phase 3
    pass


def calculate_overhead(payload_size):
    """
    Calculate packet overhead percentage.

    🎓 TEACHING NOTE:
    Overhead is the "tax" we pay for structure and error detection.

    For small payloads, overhead is significant!
    Example:
      1 byte payload → 14 bytes overhead → 93% overhead!
      100 byte payload → 14 bytes overhead → 14% overhead

    This is why we batch data when possible.

    Parameters
    ----------
    payload_size : int
        Payload size in bytes

    Returns
    -------
    overhead_percent : float
        Percentage of total packet that is overhead
    """
    # Implementation coming in Phase 3
    pass


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. CRC always fails? Check byte order (endianness)
#   2. Can't find preamble? Check for bit shifts or alignment
#   3. Timestamp errors? Verify float <-> bytes conversion
#   4. Length mismatch? Count header + payload + CRC bytes
#
# Testing Tips:
#   - Start with known payload (e.g., "Test")
#   - Manually verify CRC calculation
#   - Hexdump packets to inspect structure
#   - Test with various payload sizes (1, 10, 100, 1000 bytes)
#   - Deliberately corrupt packets to verify detection works
#
# Gotchas:
#   - Packet ID wraps at 65535 (16-bit)
#   - Timestamp is 4 bytes (limited precision)
#   - Preamble could appear in payload by chance (rare)
#   - CRC doesn't correct errors, only detects them!


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Add sequence numbers for packet ordering
#   [ ] Implement fragmentation for large messages
#   [ ] Add packet type field (data/control/ack)
#   [ ] Support variable-length headers
#   [ ] Add source/destination addresses
#   [ ] Implement ACK/NACK response packets
#   [ ] Add encryption fields
#
# For Deep Space Version:
#   [ ] Extended timestamps (nanosecond precision)
#   [ ] CCSDS packet format compliance
#   [ ] Reed-Solomon outer code
#   [ ] Consultative Committee for Space Data Systems (CCSDS) standard
