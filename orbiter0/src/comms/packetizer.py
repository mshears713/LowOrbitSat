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
    import struct
    import time

    # 🎓 STEP 1: Create preamble (sync pattern)
    # The pattern 0xAA (10101010 in binary) is easy to detect
    # It creates a distinctive "square wave" pattern
    preamble = b'\xAA\xAA\xAA\xAA'

    # 🎓 STEP 2: Build header
    # Get current time if not provided
    if timestamp is None:
        timestamp = time.time()

    # Ensure packet_id is in valid range (16-bit unsigned)
    packet_id = packet_id % 65536

    # Calculate payload length
    payload_length = len(payload_bytes)

    # Pack header fields into bytes
    # Format: 'H' = unsigned short (2 bytes) for packet_id
    #         'H' = unsigned short (2 bytes) for length
    #         'f' = float (4 bytes) for timestamp
    header = struct.pack('>HHf', packet_id, payload_length, timestamp)

    # 🎓 NOTE: '>' means big-endian (network byte order)
    # This ensures consistent byte order across different systems

    # 🎓 STEP 3: Combine header and payload
    header_and_payload = header + payload_bytes

    # 🎓 STEP 4: Calculate CRC-16 checksum
    # CRC provides error detection - it's like a fingerprint for data
    crc_value = _compute_crc16(header_and_payload)

    # Pack CRC as 2-byte unsigned short
    crc_bytes = struct.pack('>H', crc_value)

    # 🎓 STEP 5: Assemble complete packet
    packet = preamble + header_and_payload + crc_bytes

    return packet


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
    import struct

    # 🎓 MINIMUM SIZE CHECK
    # Preamble (4) + Header (8) + CRC (2) = 14 bytes minimum
    HEADER_SIZE = 8
    PREAMBLE_SIZE = 4
    CRC_SIZE = 2
    MIN_PACKET_SIZE = PREAMBLE_SIZE + HEADER_SIZE + CRC_SIZE

    if len(packet_bytes) < MIN_PACKET_SIZE:
        return {
            'packet_id': None,
            'timestamp': None,
            'payload': b'',
            'crc_valid': False,
            'error': 'Packet too short'
        }

    # 🎓 STEP 1: Verify preamble
    expected_preamble = b'\xAA\xAA\xAA\xAA'
    actual_preamble = packet_bytes[:PREAMBLE_SIZE]

    if actual_preamble != expected_preamble:
        return {
            'packet_id': None,
            'timestamp': None,
            'payload': b'',
            'crc_valid': False,
            'error': 'Invalid preamble'
        }

    # 🎓 STEP 2: Extract header fields
    # Header starts after preamble
    header_start = PREAMBLE_SIZE
    header_end = header_start + HEADER_SIZE
    header = packet_bytes[header_start:header_end]

    # Unpack header: packet_id (H), length (H), timestamp (f)
    packet_id, payload_length, timestamp = struct.unpack('>HHf', header)

    # 🎓 STEP 3: Extract payload
    payload_start = header_end
    payload_end = payload_start + payload_length
    payload = packet_bytes[payload_start:payload_end]

    # 🎓 STEP 4: Extract and verify CRC
    # CRC is the last 2 bytes
    crc_start = payload_end
    crc_end = crc_start + CRC_SIZE

    # Check if packet has enough data
    if len(packet_bytes) < crc_end:
        return {
            'packet_id': packet_id,
            'timestamp': timestamp,
            'payload': payload,
            'crc_valid': False,
            'error': 'Packet truncated (missing CRC)'
        }

    received_crc = struct.unpack('>H', packet_bytes[crc_start:crc_end])[0]

    # Calculate expected CRC over header + payload
    header_and_payload = packet_bytes[PREAMBLE_SIZE:payload_end]
    calculated_crc = _compute_crc16(header_and_payload)

    # 🎓 CRC VALIDATION
    # If these match, the packet is very likely uncorrupted
    # (CRC-16 can detect >99.99% of errors)
    crc_valid = (received_crc == calculated_crc)

    return {
        'packet_id': packet_id,
        'timestamp': timestamp,
        'payload': payload,
        'payload_length': payload_length,
        'crc_valid': crc_valid,
        'crc_received': received_crc,
        'crc_calculated': calculated_crc
    }


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
    # 🎓 QUICK VALIDATION
    # Parse the packet and check if CRC is valid
    parsed = parse_packet(packet_bytes)

    # Valid if:
    # 1. No error occurred during parsing
    # 2. CRC matches
    return parsed.get('crc_valid', False) and 'error' not in parsed


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
    # 🎓 OVERHEAD CALCULATION
    # Overhead = Preamble (4) + Header (8) + CRC (2) = 14 bytes
    OVERHEAD_BYTES = 14

    # Total packet size
    total_size = OVERHEAD_BYTES + payload_size

    # Percentage of packet that is overhead
    overhead_percent = (OVERHEAD_BYTES / total_size) * 100

    return overhead_percent


def _compute_crc16(data):
    """
    Compute CRC-16-CCITT checksum.

    🎓 TEACHING NOTE:
    CRC (Cyclic Redundancy Check) is like a sophisticated checksum.
    It's designed to detect common transmission errors:
    - Single bit errors
    - Double bit errors
    - Burst errors up to 16 bits
    - Most other error patterns

    HOW IT WORKS:
    Think of CRC as polynomial division in binary.
    The remainder is the checksum.

    WHY CRC-16?
    - 16 bits = 65,536 possible values
    - Can detect 99.998% of all errors
    - Fast to compute
    - Industry standard for data links

    CCITT POLYNOMIAL: 0x1021 (x^16 + x^12 + x^5 + 1)

    Parameters
    ----------
    data : bytes
        Data to compute CRC over

    Returns
    -------
    crc : int
        16-bit CRC value (0-65535)
    """
    # 🎓 CRC-16-CCITT Implementation
    # This is the polynomial used in many communications protocols
    CRC16_CCITT_POLY = 0x1021
    crc = 0xFFFF  # Initial value (all 1s)

    for byte in data:
        # XOR byte into the high byte of CRC
        crc ^= (byte << 8)

        # Process each bit
        for _ in range(8):
            if crc & 0x8000:  # If high bit is set
                crc = (crc << 1) ^ CRC16_CCITT_POLY
            else:
                crc = crc << 1

            # Keep CRC in 16-bit range
            crc &= 0xFFFF

    return crc


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
