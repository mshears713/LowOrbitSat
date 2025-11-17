"""
═══════════════════════════════════════════════════════════════════
CHAPTER 5: PACKETS 101
Structuring data for reliable transmission
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Packets 101", page_icon="📦", layout="wide")

st.title("📦 Chapter 5: Packets 101")

st.markdown("""
---

### Organizing the Data 📬

You can't just throw random bits into space! Real systems organize
data into **PACKETS** - structured bundles with headers and checksums.

**Packet = Header + Payload + Checksum**

Think of it like mailing a letter:
- 📮 Header = address and return address
- 📄 Payload = the letter itself
- ✅ Checksum = delivery confirmation

---

### 🎯 Learning Objectives

- ✅ Why we need packet structure
- ✅ Header fields (ID, length, timestamp)
- ✅ Checksums for error detection (CRC)
- ✅ Packet overhead trade-offs
- ✅ Framing and synchronization

---

### 📋 Packet Structure

```
┌──────────────────────────────────────────┐
│ PREAMBLE (sync)      │ 4 bytes           │
├──────────────────────────────────────────┤
│ HEADER               │ 8 bytes           │
│   - Packet ID        │ (2 bytes)         │
│   - Length           │ (2 bytes)         │
│   - Timestamp        │ (4 bytes)         │
├──────────────────────────────────────────┤
│ PAYLOAD              │ N bytes           │
├──────────────────────────────────────────┤
│ CRC-16 Checksum      │ 2 bytes           │
└──────────────────────────────────────────┘
```

---
""")

# Add path to import our modules
import sys
sys.path.append('../../src')

from comms.packetizer import create_packet, parse_packet, validate_packet, calculate_overhead
from comms.corruptor import flip_random_bits, burst_errors, corrupt_specific_byte
import time

# ═══════════════════════════════════════════════════════════════════
# DEMO 1: CREATE AND VIEW PACKETS
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Demo 1: Packet Creation")

st.markdown("""
Let's create a packet from your message and see how it's structured!
""")

col1, col2 = st.columns([2, 1])

with col1:
    message = st.text_input(
        "Your Message",
        value="Hello Satellite!",
        max_chars=50,
        help="Enter text to be packetized"
    )

with col2:
    packet_id = st.number_input(
        "Packet ID",
        min_value=0,
        max_value=65535,
        value=42,
        help="Unique identifier for this packet"
    )

if message:
    # Create packet
    payload_bytes = message.encode('utf-8')
    packet_bytes = create_packet(payload_bytes, packet_id=packet_id, timestamp=int(time.time()))

    # Parse it back
    parsed = parse_packet(packet_bytes)
    is_valid = validate_packet(packet_bytes)

    # Display packet structure
    st.markdown("### 📦 Packet Structure Breakdown")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Total Packet Size", f"{len(packet_bytes)} bytes")
        st.metric("Payload Size", f"{len(payload_bytes)} bytes")

    with col_b:
        st.metric("Header Overhead", f"{parsed['header_size']} bytes")
        st.metric("CRC Overhead", "2 bytes")

    with col_c:
        overhead_pct = calculate_overhead(len(payload_bytes))
        st.metric("Total Overhead", f"{overhead_pct:.1f}%")
        st.metric("CRC Valid", "✅" if is_valid else "❌")

    # Hex dump visualization
    st.markdown("### 🔍 Packet Hex Dump")

    # Create hex dump with annotations
    hex_str = packet_bytes.hex()

    # Break down packet into sections
    preamble_hex = hex_str[:8]  # 4 bytes = 8 hex chars
    header_hex = hex_str[8:24]  # 8 bytes = 16 hex chars
    payload_hex = hex_str[24:-4]  # everything except last 2 bytes
    crc_hex = hex_str[-4:]  # 2 bytes = 4 hex chars

    st.code(f"""
╔════════════════════════════════════════════════════════════════╗
║ PREAMBLE (sync marker)                                         ║
╠════════════════════════════════════════════════════════════════╣
  {preamble_hex}
  (Magic bytes for synchronization: 0xDEADBEEF)

╔════════════════════════════════════════════════════════════════╗
║ HEADER (ID={parsed['packet_id']}, Length={parsed['payload_length']}, Timestamp={parsed['timestamp']})   ║
╠════════════════════════════════════════════════════════════════╣
  {header_hex}

╔════════════════════════════════════════════════════════════════╗
║ PAYLOAD ("{message}")                                          ║
╠════════════════════════════════════════════════════════════════╣
  {payload_hex}

╔════════════════════════════════════════════════════════════════╗
║ CRC-16 CHECKSUM (error detection)                             ║
╠════════════════════════════════════════════════════════════════╣
  {crc_hex}
  (Computed: 0x{crc_hex})
""", language="")

    st.markdown(f"""
    **Parsed Packet Details:**
    - **Packet ID:** {parsed['packet_id']}
    - **Payload Length:** {parsed['payload_length']} bytes
    - **Timestamp:** {parsed['timestamp']} (Unix time)
    - **Payload (decoded):** "{parsed['payload'].decode('utf-8', errors='replace')}"
    - **CRC-16 Checksum:** 0x{parsed['crc']:04x}
    - **Validation:** {'✅ PASS' if is_valid else '❌ FAIL'}
    """)

    st.markdown("""
    ---
    """)

    # ═══════════════════════════════════════════════════════════════════
    # DEMO 2: ERROR INJECTION AND DETECTION
    # ═══════════════════════════════════════════════════════════════════

    st.header("🔬 Demo 2: Corruption & Error Detection")

    st.markdown("""
    Now let's see what happens when the packet gets corrupted during transmission!
    The CRC checksum will detect if any bits were flipped.
    """)

    col_i, col_ii = st.columns(2)

    with col_i:
        corruption_type = st.selectbox(
            "Corruption Type",
            ["None (Clean)", "Random Bit Flips", "Burst Errors", "Corrupt Specific Byte"],
            help="Different types of transmission errors"
        )

    with col_ii:
        if corruption_type == "Random Bit Flips":
            ber = st.slider("Bit Error Rate", 0.0, 0.5, 0.05, 0.01, help="Probability of each bit flipping")
        elif corruption_type == "Burst Errors":
            num_bursts = st.slider("Number of Bursts", 1, 5, 2, help="How many burst error events")
        elif corruption_type == "Corrupt Specific Byte":
            byte_to_corrupt = st.slider("Byte Index", 0, len(packet_bytes)-1, 14, help="Which byte to corrupt")

    # Apply corruption
    corrupted_packet = packet_bytes
    corruption_applied = False

    if corruption_type == "Random Bit Flips":
        corrupted_packet = flip_random_bits(packet_bytes, bit_error_rate=ber)
        corruption_applied = (corrupted_packet != packet_bytes)
    elif corruption_type == "Burst Errors":
        corrupted_packet = burst_errors(packet_bytes, num_bursts=num_bursts, burst_length=4)
        corruption_applied = (corrupted_packet != packet_bytes)
    elif corruption_type == "Corrupt Specific Byte":
        corrupted_packet = corrupt_specific_byte(packet_bytes, byte_to_corrupt, new_value=0xFF)
        corruption_applied = True

    # Validate corrupted packet
    is_corrupted_valid = validate_packet(corrupted_packet)

    # Display results
    st.markdown("### 🔍 Corruption Results")

    col_x, col_y = st.columns(2)

    with col_x:
        st.markdown("**Original Packet:**")
        st.code(packet_bytes.hex()[:80] + "..." if len(packet_bytes.hex()) > 80 else packet_bytes.hex())
        st.markdown(f"**CRC Status:** ✅ Valid")

    with col_y:
        st.markdown("**Corrupted Packet:**")
        st.code(corrupted_packet.hex()[:80] + "..." if len(corrupted_packet.hex()) > 80 else corrupted_packet.hex())
        st.markdown(f"**CRC Status:** {'✅ Valid (no errors detected)' if is_corrupted_valid else '❌ INVALID - Errors detected!'}")

    # Count differences
    differences = sum(b1 != b2 for b1, b2 in zip(packet_bytes, corrupted_packet))
    total_bits = len(packet_bytes) * 8
    bits_flipped = bin(int.from_bytes(bytes(b1 ^ b2 for b1, b2 in zip(packet_bytes, corrupted_packet)), 'big')).count('1')

    if corruption_applied:
        st.markdown(f"""
        **Corruption Statistics:**
        - **Bytes Changed:** {differences} out of {len(packet_bytes)}
        - **Bits Flipped:** {bits_flipped} out of {total_bits}
        - **Bit Error Rate:** {bits_flipped/total_bits:.4f} ({bits_flipped/total_bits*100:.2f}%)
        """)

        if is_corrupted_valid:
            st.warning("⚠️ **CRC passed but packet was corrupted!** This is rare but possible (CRC false negative)")
        else:
            st.success("✅ **CRC successfully detected the corruption!** Packet would be rejected and retransmission requested.")

        # Try to parse corrupted packet anyway (for educational purposes)
        try:
            corrupted_parsed = parse_packet(corrupted_packet)
            st.markdown(f"""
            **Attempting to decode corrupted packet:**
            - **Payload (may be garbage):** `{corrupted_parsed['payload'][:50]}`
            - **Decoded text attempt:** "{corrupted_parsed['payload'].decode('utf-8', errors='replace')}"
            """)
        except:
            st.error("❌ Packet so corrupted it can't even be parsed!")
    else:
        st.info("No corruption applied - packet is clean!")

    st.markdown("""
    ---

    ### 🎓 What You're Seeing

    **Packet Structure Benefits:**
    1. **Preamble:** Helps receiver find start of packet (synchronization)
    2. **Header:** Metadata tells us what to expect
    3. **Payload:** The actual data we want to transmit
    4. **CRC Checksum:** Detects if any bits were corrupted

    **CRC-16 Error Detection:**
    - Can detect all single-bit errors
    - Can detect all double-bit errors
    - Can detect bursts up to 16 bits long
    - Can detect ~99.998% of all other error patterns
    - **Cannot** fix errors - only detect them!

    **Try This:**
    1. Send a clean packet → CRC validates
    2. Add random bit flips (5% BER) → CRC usually catches it
    3. Try burst errors → simulates fade events
    4. Corrupt specific bytes → see exactly which byte fails
    5. Notice: Even 1 corrupted bit fails the CRC check!

    **Real-World Impact:**
    - Packets with bad CRC are **discarded**
    - Ground station requests **retransmission**
    - This is why we need **forward error correction** (next chapter!)

    ---

    **➡️ Next:** Learn how to **fix** errors in **Error Correction 101**

    """)

else:
    st.warning("👆 Enter a message above to create a packet!")

st.success("✅ **Interactive Demo Active:** Create packets and watch corruption detection in action!")

st.divider()
st.caption("Chapter 5: Packets 101 | Phase 4: Fully Interactive Learning Console")
