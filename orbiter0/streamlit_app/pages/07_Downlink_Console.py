"""
═══════════════════════════════════════════════════════════════════
CHAPTER 7: DOWNLINK CONSOLE
Live satellite communications simulator
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Downlink Console", page_icon="🖥️", layout="wide")

st.title("🖥️ Chapter 7: Downlink Console")

st.markdown("""
---

### Mission Control Interface 🎮

This is where everything comes together!
The **Downlink Console** simulates a real-time satellite
communication session.

**Features:**
- 📤 Send messages to the satellite
- 📥 Receive decoded transmissions
- 📊 Live signal quality metrics
- 📈 Real-time BER/SNR monitoring
- 📜 Scrolling packet log

---

### 🎯 Learning Objectives

- ✅ End-to-end communication pipeline
- ✅ Real-time signal processing
- ✅ Monitoring and diagnostics
- ✅ Understanding system behavior
- ✅ Quality metrics interpretation

---

---
""")

# Add path to import our modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from signals.modulation import text_to_bits, bits_to_text, bits_to_bpsk_symbols, bpsk_symbols_to_bits, modulate_bpsk, demodulate_bpsk
from channel.noise import add_awgn, calculate_snr_db
from channel.range_loss import apply_free_space_loss
from channel.fades import generate_random_fades, apply_fades_to_signal
from comms.packetizer import create_packet, parse_packet, validate_packet
from comms.corruptor import flip_random_bits
from comms.decoder import hamming_encode_4bit, hamming_decode_4bit, encode_bytes_with_hamming, decode_bytes_with_hamming
from utils.math_helpers import calculate_ber
import numpy as np
import time

# ═══════════════════════════════════════════════════════════════════
# DOWNLINK CONSOLE SIMULATOR
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Live Downlink Console")

st.markdown("""
Simulate a complete satellite downlink session! Send messages through the full communication pipeline.
""")

# Initialize session state for packet log
if 'packet_log' not in st.session_state:
    st.session_state.packet_log = []

# Configuration
st.markdown("### ⚙️ Link Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    snr_db = st.slider(
        "SNR (dB)",
        min_value=0,
        max_value=30,
        value=15,
        help="Signal-to-noise ratio"
    )

with col2:
    distance_km = st.slider(
        "Satellite Distance (km)",
        min_value=300,
        max_value=2000,
        value=500,
        step=50,
        help="Range to satellite"
    )

with col3:
    use_fec = st.checkbox(
        "Enable FEC (Hamming)",
        value=True,
        help="Forward error correction"
    )

# Message input
st.markdown("### 📤 Transmit Message")

col_a, col_b = st.columns([3, 1])

with col_a:
    message = st.text_input(
        "Your Message",
        value="Hello Ground!",
        max_chars=30,
        help="Message to send from satellite"
    )

with col_b:
    send_button = st.button("📡 Send Message", type="primary", use_container_width=True)

# Link quality indicator
link_quality = "Excellent" if snr_db >= 20 else "Good" if snr_db >= 15 else "Marginal" if snr_db >= 10 else "Poor"
link_color = "green" if snr_db >= 20 else "blue" if snr_db >= 15 else "orange" if snr_db >= 10 else "red"

st.markdown(f"""
**Current Link Status:** :{link_color}[●] **{link_quality}** (SNR: {snr_db} dB, Range: {distance_km} km, FEC: {'ON' if use_fec else 'OFF'})
""")

# Process transmission
if send_button and message:
    with st.spinner("Transmitting..."):
        # Step 1: Encode message
        payload_bytes = message.encode('utf-8')

        # Optional FEC encoding
        if use_fec:
            # Encode with Hamming
            payload_bits_list = []
            for byte in payload_bytes:
                # Convert byte to 8 bits, then encode in pairs of 4
                byte_bits = [(byte >> i) & 1 for i in range(7, -1, -1)]
                nibble1 = byte_bits[:4]
                nibble2 = byte_bits[4:]
                payload_bits_list.extend(hamming_encode_4bit(nibble1))
                payload_bits_list.extend(hamming_encode_4bit(nibble2))
            # Convert bits back to bytes for packet
            fec_bytes = bytearray()
            for i in range(0, len(payload_bits_list), 8):
                if i + 8 <= len(payload_bits_list):
                    byte_val = sum(bit << (7 - j) for j, bit in enumerate(payload_bits_list[i:i+8]))
                    fec_bytes.append(byte_val)
            packet_payload = bytes(fec_bytes)
        else:
            packet_payload = payload_bytes

        # Create packet
        packet_bytes = create_packet(packet_payload, packet_id=len(st.session_state.packet_log))

        # Step 2: Convert to bits and modulate
        packet_bits = [int(b) for byte in packet_bytes for b in format(byte, '08b')]
        symbols = bits_to_bpsk_symbols(packet_bits)

        # Step 3: Modulate to signal
        carrier_freq = 100
        sample_rate = 10000
        signal, time_axis = modulate_bpsk(symbols, carrier_freq, sample_rate)

        # Step 4: Apply channel effects
        # Range loss
        attenuated_signal = apply_free_space_loss(signal, distance_km, reference_distance_km=300)

        # Add noise
        noisy_signal, noise = add_awgn(attenuated_signal, snr_db)

        # Step 5: Demodulate
        demod_symbols = demodulate_bpsk(noisy_signal, carrier_freq, sample_rate, len(symbols))
        demod_bits = bpsk_symbols_to_bits(demod_symbols)

        # Step 6: Convert back to bytes (packet)
        received_bytes = bytearray()
        for i in range(0, len(demod_bits), 8):
            if i + 8 <= len(demod_bits):
                byte_val = sum(bit << (7 - j) for j, bit in enumerate(demod_bits[i:i+8]))
                received_bytes.append(byte_val)
        received_packet = bytes(received_bytes)

        # Step 7: Validate packet
        packet_valid = validate_packet(received_packet)

        # Step 8: Decode payload
        decoded_message = ""
        if packet_valid:
            try:
                parsed = parse_packet(received_packet)
                decoded_payload = parsed['payload']

                # If FEC was used, decode it
                if use_fec:
                    # Convert payload back to bits
                    fec_bits_received = [int(b) for byte in decoded_payload for b in format(byte, '08b')]

                    # Decode Hamming
                    decoded_bits = []
                    for i in range(0, len(fec_bits_received), 7):
                        if i + 7 <= len(fec_bits_received):
                            hamming_bits = fec_bits_received[i:i+7]
                            data_bits = hamming_decode_4bit(hamming_bits)
                            decoded_bits.extend(data_bits)

                    # Convert bits back to bytes
                    decoded_bytes = bytearray()
                    for i in range(0, len(decoded_bits), 8):
                        if i + 8 <= len(decoded_bits):
                            byte_val = sum(bit << (7 - j) for j, bit in enumerate(decoded_bits[i:i+8]))
                            decoded_bytes.append(byte_val)

                    decoded_message = decoded_bytes.decode('utf-8', errors='replace')
                else:
                    decoded_message = decoded_payload.decode('utf-8', errors='replace')

            except Exception as e:
                decoded_message = f"[DECODE ERROR: {str(e)}]"
        else:
            decoded_message = "[CRC FAILED - PACKET REJECTED]"

        # Calculate statistics
        ber, num_errors, total_bits = calculate_ber(packet_bits, demod_bits[:len(packet_bits)])
        success = (decoded_message == message)

        # Log the transmission
        log_entry = {
            'time': time.strftime("%H:%M:%S"),
            'original': message,
            'decoded': decoded_message,
            'snr': snr_db,
            'distance': distance_km,
            'fec': use_fec,
            'packet_valid': packet_valid,
            'ber': ber,
            'success': success
        }
        st.session_state.packet_log.append(log_entry)

# Display results
if st.session_state.packet_log:
    latest = st.session_state.packet_log[-1]

    st.markdown("### 📥 Reception Results")

    col_i, col_ii, col_iii = st.columns(3)

    with col_i:
        st.metric("Packet CRC", "✅ Valid" if latest['packet_valid'] else "❌ Invalid")
        st.metric("Message Match", "✅ Success" if latest['success'] else "❌ Failed")

    with col_ii:
        st.metric("Bit Error Rate", f"{latest['ber']:.6f}")
        st.metric("BER %", f"{latest['ber']*100:.4f}%")

    with col_iii:
        st.metric("SNR", f"{latest['snr']} dB")
        st.metric("Range", f"{latest['distance']} km")

    # Message comparison
    col_x, col_y = st.columns(2)

    with col_x:
        st.markdown("**Original Message:**")
        st.code(latest['original'], language="")

    with col_y:
        st.markdown("**Received Message:**")
        st.code(latest['decoded'], language="")

    if latest['success']:
        st.success("🎉 **Perfect Reception!** Message decoded successfully.")
    elif latest['packet_valid']:
        st.warning(f"⚠️ **Partial Success:** Packet valid but message corrupted (BER: {latest['ber']*100:.4f}%)")
    else:
        st.error("❌ **Reception Failed:** Packet CRC check failed")

# Packet log
if len(st.session_state.packet_log) > 0:
    st.markdown("---")
    st.markdown("### 📜 Transmission Log")

    # Summary stats
    total_sent = len(st.session_state.packet_log)
    total_success = sum(1 for entry in st.session_state.packet_log if entry['success'])
    avg_ber = np.mean([entry['ber'] for entry in st.session_state.packet_log])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transmissions", total_sent)
    col2.metric("Successful", total_success)
    col3.metric("Success Rate", f"{total_success/total_sent*100:.1f}%")
    col4.metric("Avg BER", f"{avg_ber:.6f}")

    # Show last 5 entries
    st.markdown("**Recent Transmissions:**")
    for i, entry in enumerate(reversed(st.session_state.packet_log[-5:])):
        status_icon = "✅" if entry['success'] else "❌"
        fec_status = "FEC" if entry['fec'] else "No FEC"
        st.text(f"{status_icon} [{entry['time']}] SNR:{entry['snr']}dB Range:{entry['distance']}km {fec_status} | \"{entry['original']}\" → \"{entry['decoded']}\"")

    if st.button("🗑️ Clear Log"):
        st.session_state.packet_log = []
        st.rerun()

st.markdown("""
---

### 🎓 Understanding the Downlink Console

**End-to-End Pipeline:**
1. **Encode:** Text → Bytes → (Optional: Hamming FEC) → Packet
2. **Modulate:** Packet → Bits → BPSK Symbols → Signal
3. **Transmit:** Signal → Channel (range loss, noise)
4. **Receive:** Noisy Signal → Demodulate → Bits → Packet
5. **Decode:** Validate CRC → (Optional: Hamming Decode) → Text

**Key Observations:**
- **Higher SNR** = Fewer bit errors = Better success rate
- **Closer satellite** = Stronger signal = Better reception
- **FEC enabled** = Can correct some errors automatically
- **CRC validation** = Detects corrupted packets (but can't fix them without FEC)

**Try This:**
1. Send at 20+ dB SNR → Should be perfect
2. Drop to 5 dB → See errors appear
3. Enable/disable FEC → Compare error correction
4. Vary distance → See range loss effect
5. Send multiple messages → Build transmission log

---

**➡️ Next:** Explore **Satellite Pass Simulator** for timeline view

""")

st.success("✅ **Interactive Demo Active:** Send messages through the complete communication system!")

st.divider()
st.caption("Chapter 7: Downlink Console | Phase 4: Fully Interactive Learning Console")
