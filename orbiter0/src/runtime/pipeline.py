"""
═══════════════════════════════════════════════════════════════════
MODULE: runtime/pipeline.py
PURPOSE: Orchestrated end-to-end satellite communications pipeline
THEME: The complete mission from message to space and back
═══════════════════════════════════════════════════════════════════

📡 STORY:
This is where EVERYTHING comes together!

We've built all the pieces:
  • Signal generation
  • Modulation (BPSK)
  • Channel effects (noise, fading, range loss)
  • Packetization
  • Error correction
  • Mission archival

Now we orchestrate them into a complete satellite communications
simulation. One function call runs the ENTIRE pipeline!

COMPLETE PIPELINE:
┌────────────────────────────────────────────────────────────────┐
│              ORBITER-0 COMPLETE RUNTIME                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. TEXT MESSAGE                                               │
│       ↓                                                        │
│  2. PACKETIZATION (add headers, CRC)                           │
│       ↓                                                        │
│  3. ERROR CORRECTION ENCODING (Hamming/FEC)                    │
│       ↓                                                        │
│  4. BITS → BPSK SYMBOLS (+1/-1)                                │
│       ↓                                                        │
│  5. MODULATION (multiply by carrier)                           │
│       ↓                                                        │
│  6. CHANNEL EFFECTS:                                           │
│       • Range loss (distance attenuation)                      │
│       • Atmospheric absorption                                 │
│       • Fading events (dropouts, bursts)                       │
│       • Additive white Gaussian noise (AWGN)                   │
│       ↓                                                        │
│  7. DEMODULATION (BPSK symbol detection)                       │
│       ↓                                                        │
│  8. ERROR CORRECTION DECODING                                  │
│       ↓                                                        │
│  9. PACKET VALIDATION (CRC check)                              │
│       ↓                                                        │
│  10. MESSAGE RECONSTRUCTION                                     │
│       ↓                                                        │
│  11. ANOMALY LOGGING (track errors)                            │
│       ↓                                                        │
│  12. MISSION ARCHIVAL (save to database)                       │
│       ↓                                                        │
│  13. RESULTS DICTIONARY (metrics, plots, etc.)                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • Understanding end-to-end system design
  • How components interact
  • Pipeline orchestration patterns
  • Comprehensive error handling
  • Performance metrics collection

SIMPLIFICATIONS:
  • Single-packet messages for now (no fragmentation)
  • Perfect timing synchronization
  • No retransmission logic yet
  • Simplified satellite pass model

═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════

import numpy as np
import time
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Signal processing
from signal.modulation import (
    text_to_bits, bits_to_bpsk_symbols, modulate_bpsk,
    demodulate_bpsk, bpsk_symbols_to_bits, bits_to_text
)
from signal.generator import generate_sine

# Channel effects
from channel.noise import add_awgn, calculate_snr_db
from channel.range_loss import apply_free_space_loss, apply_atmospheric_loss
from channel.fades import apply_fading_events, FadeEvent

# Communications
from comms.packetizer import create_packet, parse_packet, validate_packet
from comms.decoder import (
    hamming_encode_message, hamming_decode_message,
    add_parity_bit, check_parity_bit
)
from comms.cleaner import compute_crc16, verify_crc
from comms.corruptor import flip_random_bits, add_burst_errors
from comms.anomalies import log_anomaly, AnomalyDetector
from comms.storage import save_mission, init_database

# Utilities
from utils.math_helpers import calculate_ber, count_bit_errors
from utils.timing import SatellitePass, signal_strength_over_time


# ═══════════════════════════════════════════════════════════════
# MAIN ORCHESTRATION FUNCTION
# ═══════════════════════════════════════════════════════════════

def simulate_transmission(
    message,
    distance_km=1000,
    snr_db=15,
    use_fec=True,
    fading_events=None,
    carrier_freq_hz=1000,
    sample_rate_hz=10000,
    save_to_db=True
):
    """
    Run complete satellite transmission simulation.

    🎓 TEACHING NOTE:
    This function is the "main" orchestrator. It runs the entire
    pipeline from message input to decoded output.

    Think of it as a conductor leading an orchestra - each
    component plays its part at the right time!

    Parameters
    ----------
    message : str
        Text message to transmit
    distance_km : float
        Satellite-to-ground distance (affects signal strength)
    snr_db : float
        Target signal-to-noise ratio in dB
    use_fec : bool
        Whether to apply Forward Error Correction
    fading_events : list of FadeEvent, optional
        Fade events to apply during transmission
    carrier_freq_hz : float
        Carrier frequency for modulation
    sample_rate_hz : int
        Sampling rate
    save_to_db : bool
        Whether to save mission to database

    Returns
    -------
    result : dict
        Complete mission results including:
        - message_sent: original message
        - message_received: decoded message
        - ber: bit error rate
        - packet_errors: number of corrupted packets
        - metrics: detailed statistics
        - anomalies: list of detected issues
    """

    # ═══════════════════════════════════════════════════════════
    # STEP 1: INITIALIZATION
    # ═══════════════════════════════════════════════════════════

    print("📡 ORBITER-0 Mission Starting...")
    print(f"   Message: \"{message}\"")
    print(f"   Distance: {distance_km} km")
    print(f"   Target SNR: {snr_db} dB")
    print(f"   FEC: {'Enabled' if use_fec else 'Disabled'}")
    print()

    start_time = time.time()
    anomaly_detector = AnomalyDetector()

    # Initialize database if saving
    if save_to_db:
        init_database()

    # ═══════════════════════════════════════════════════════════
    # STEP 2: TEXT → BITS
    # ═══════════════════════════════════════════════════════════

    print("🔢 Converting text to bits...")
    message_bytes = message.encode('utf-8')
    original_bits = text_to_bits(message)
    print(f"   {len(message_bytes)} bytes → {len(original_bits)} bits")

    # ═══════════════════════════════════════════════════════════
    # STEP 3: PACKETIZATION
    # ═══════════════════════════════════════════════════════════

    print("📦 Creating packet...")
    packet_id = int(time.time() * 1000) % 65536  # Unique ID
    packet = create_packet(message_bytes, packet_id=packet_id)
    print(f"   Payload: {len(message_bytes)} bytes")
    print(f"   Total packet: {len(packet)} bytes (includes header + CRC)")

    # ═══════════════════════════════════════════════════════════
    # STEP 4: ERROR CORRECTION ENCODING
    # ═══════════════════════════════════════════════════════════

    if use_fec:
        print("🛡️  Applying Forward Error Correction...")
        packet_bits = []
        for byte in packet:
            packet_bits.extend([int(b) for b in format(byte, '08b')])

        encoded_bits = hamming_encode_message(packet_bits)
        print(f"   {len(packet_bits)} bits → {len(encoded_bits)} bits")
        print(f"   Overhead: {len(encoded_bits) - len(packet_bits)} bits ({100*(len(encoded_bits)/len(packet_bits)-1):.1f}%)")

        bits_to_transmit = encoded_bits
    else:
        # No FEC - just convert packet to bits
        packet_bits = []
        for byte in packet:
            packet_bits.extend([int(b) for b in format(byte, '08b')])
        bits_to_transmit = packet_bits

    # ═══════════════════════════════════════════════════════════
    # STEP 5: BPSK MODULATION
    # ═══════════════════════════════════════════════════════════

    print("📻 Modulating to BPSK...")
    symbols = bits_to_bpsk_symbols(bits_to_transmit)

    # Generate carrier and modulate
    samples_per_symbol = int(sample_rate_hz / 100)  # 100 symbols/sec
    modulated_signal, time_axis = modulate_bpsk(
        symbols, carrier_freq_hz, sample_rate_hz, samples_per_symbol
    )
    print(f"   {len(symbols)} symbols → {len(modulated_signal)} samples")

    # ═══════════════════════════════════════════════════════════
    # STEP 6: CHANNEL EFFECTS
    # ═══════════════════════════════════════════════════════════

    print("🌍 Applying channel effects...")

    # 6a. Range loss (free space path loss)
    signal_after_range = apply_free_space_loss(
        modulated_signal, distance_km, carrier_freq_hz
    )
    range_loss_db = -10 * np.log10(np.mean(signal_after_range**2) / np.mean(modulated_signal**2))
    print(f"   Range loss: -{range_loss_db:.1f} dB")

    # 6b. Atmospheric absorption
    signal_after_atmo = apply_atmospheric_loss(signal_after_range, carrier_freq_hz)
    atmo_loss_db = -10 * np.log10(np.mean(signal_after_atmo**2) / np.mean(signal_after_range**2))
    print(f"   Atmospheric loss: -{atmo_loss_db:.1f} dB")

    # 6c. Fading events
    if fading_events:
        print(f"   Applying {len(fading_events)} fade events...")
        signal_after_fades = apply_fading_events(
            signal_after_atmo, fading_events, sample_rate_hz, time_axis
        )
    else:
        signal_after_fades = signal_after_atmo

    # 6d. Additive White Gaussian Noise (AWGN)
    received_signal = add_awgn(signal_after_fades, snr_db)
    actual_snr = calculate_snr_db(modulated_signal, received_signal - signal_after_fades)
    print(f"   AWGN added: SNR = {actual_snr:.1f} dB")

    # ═══════════════════════════════════════════════════════════
    # STEP 7: DEMODULATION
    # ═══════════════════════════════════════════════════════════

    print("🔊 Demodulating BPSK...")
    received_symbols = demodulate_bpsk(
        received_signal, carrier_freq_hz, sample_rate_hz, samples_per_symbol
    )
    received_bits_raw = bpsk_symbols_to_bits(received_symbols)

    # Ensure correct length
    received_bits_raw = received_bits_raw[:len(bits_to_transmit)]
    print(f"   Recovered {len(received_bits_raw)} bits")

    # ═══════════════════════════════════════════════════════════
    # STEP 8: ERROR CORRECTION DECODING
    # ═══════════════════════════════════════════════════════════

    if use_fec:
        print("🔧 Applying FEC decoding...")
        corrected_bits = hamming_decode_message(received_bits_raw)
        errors_corrected = count_bit_errors(packet_bits, corrected_bits)
        print(f"   Errors corrected by FEC: {errors_corrected}")

        received_packet_bits = corrected_bits
    else:
        received_packet_bits = received_bits_raw

    # ═══════════════════════════════════════════════════════════
    # STEP 9: BITS → BYTES (reconstruct packet)
    # ═══════════════════════════════════════════════════════════

    # Convert bits back to bytes
    received_packet = bytearray()
    for i in range(0, len(received_packet_bits), 8):
        if i + 8 <= len(received_packet_bits):
            byte_bits = received_packet_bits[i:i+8]
            byte_val = int(''.join(map(str, byte_bits)), 2)
            received_packet.append(byte_val)

    received_packet = bytes(received_packet)

    # ═══════════════════════════════════════════════════════════
    # STEP 10: PACKET VALIDATION
    # ═══════════════════════════════════════════════════════════

    print("✅ Validating packet...")
    packet_valid = validate_packet(received_packet)

    if packet_valid:
        print("   ✓ CRC check passed!")
        parsed = parse_packet(received_packet)
        received_message = parsed['payload'].decode('utf-8', errors='replace')
        packet_corrupted = False
    else:
        print("   ✗ CRC check failed - packet corrupted")
        # Try to extract payload anyway for analysis
        try:
            parsed = parse_packet(received_packet)
            received_message = parsed['payload'].decode('utf-8', errors='replace')
        except:
            received_message = "[UNRECOVERABLE]"
        packet_corrupted = True
        anomaly_detector.add_anomaly("CRC validation failed", time.time())

    # ═══════════════════════════════════════════════════════════
    # STEP 11: CALCULATE METRICS
    # ═══════════════════════════════════════════════════════════

    print("📊 Calculating metrics...")
    ber = calculate_ber(original_bits, received_bits_raw[:len(original_bits)])
    total_errors = count_bit_errors(original_bits, received_bits_raw[:len(original_bits)])

    print(f"   Bit errors: {total_errors}/{len(original_bits)}")
    print(f"   BER: {ber:.6f} ({ber*100:.3f}%)")

    # ═══════════════════════════════════════════════════════════
    # STEP 12: ANOMALY DETECTION
    # ═══════════════════════════════════════════════════════════

    if ber > 0.1:
        anomaly_detector.add_anomaly(f"High BER: {ber:.3f}", time.time())

    if actual_snr < 5:
        anomaly_detector.add_anomaly(f"Low SNR: {actual_snr:.1f} dB", time.time())

    # ═══════════════════════════════════════════════════════════
    # STEP 13: MISSION ARCHIVAL
    # ═══════════════════════════════════════════════════════════

    elapsed_time = time.time() - start_time

    if save_to_db:
        print("💾 Saving mission to database...")
        metadata = {
            'distance_km': distance_km,
            'snr_db': snr_db,
            'actual_snr_db': actual_snr,
            'carrier_freq_hz': carrier_freq_hz,
            'use_fec': use_fec,
            'elapsed_time_sec': elapsed_time,
            'range_loss_db': range_loss_db,
            'atmo_loss_db': atmo_loss_db
        }

        mission_id = save_mission(
            message_sent=message,
            message_received=received_message,
            ber=ber,
            snr_db=actual_snr,
            packets_total=1,
            packets_corrupted=1 if packet_corrupted else 0,
            metadata=metadata
        )
        print(f"   Saved as mission #{mission_id}")

    # ═══════════════════════════════════════════════════════════
    # STEP 14: RESULTS PACKAGE
    # ═══════════════════════════════════════════════════════════

    print()
    print("=" * 60)
    print("MISSION COMPLETE!")
    print("=" * 60)
    print(f"Sent:     \"{message}\"")
    print(f"Received: \"{received_message}\"")
    print(f"Match:    {message == received_message}")
    print(f"Time:     {elapsed_time:.3f} seconds")
    print("=" * 60)

    result = {
        # Messages
        'message_sent': message,
        'message_received': received_message,
        'perfect_match': message == received_message,

        # Bits and signals
        'transmitted_bits': bits_to_transmit,
        'received_bits': received_bits_raw,
        'transmitted_signal': modulated_signal,
        'received_signal': received_signal,
        'time_axis': time_axis,

        # Metrics
        'ber': ber,
        'total_bit_errors': total_errors,
        'snr_target_db': snr_db,
        'snr_actual_db': actual_snr,
        'range_loss_db': range_loss_db,
        'atmo_loss_db': atmo_loss_db,

        # Packet info
        'packet_valid': packet_valid,
        'packets_total': 1,
        'packets_corrupted': 1 if packet_corrupted else 0,

        # Anomalies
        'anomalies': anomaly_detector.get_all_anomalies(),

        # Timing
        'elapsed_time_sec': elapsed_time,

        # Config
        'config': {
            'distance_km': distance_km,
            'carrier_freq_hz': carrier_freq_hz,
            'sample_rate_hz': sample_rate_hz,
            'use_fec': use_fec,
            'fading_events': fading_events
        }
    }

    return result


# ═══════════════════════════════════════════════════════════════
# SATELLITE PASS SIMULATION
# ═══════════════════════════════════════════════════════════════

def simulate_satellite_pass(
    message,
    pass_duration_sec=600,
    max_elevation_deg=80,
    min_snr_db=5,
    max_snr_db=20,
    use_fec=True,
    num_transmissions=10
):
    """
    Simulate complete satellite pass with varying signal strength.

    🎓 TEACHING NOTE:
    As a satellite passes overhead, signal strength changes:
    - Rises as satellite appears over horizon
    - Peaks when satellite is directly overhead
    - Falls as satellite moves away

    This simulates multiple transmissions during one pass,
    each with different signal quality.

    Parameters
    ----------
    message : str
        Message to transmit repeatedly
    pass_duration_sec : float
        Total pass duration (rise to set)
    max_elevation_deg : float
        Maximum elevation angle (90° = directly overhead)
    min_snr_db : float
        SNR when satellite is at horizon
    max_snr_db : float
        SNR when satellite is at peak elevation
    use_fec : bool
        Whether to use error correction
    num_transmissions : int
        Number of transmissions during pass

    Returns
    -------
    results : dict
        Complete pass results including all transmissions
    """

    print("🛰️  SATELLITE PASS SIMULATION")
    print("=" * 60)

    # Create satellite pass model
    sat_pass = SatellitePass(
        duration_sec=pass_duration_sec,
        max_elevation_deg=max_elevation_deg
    )

    # Generate timestamps for transmissions
    transmission_times = np.linspace(0, pass_duration_sec, num_transmissions)

    results = {
        'pass_info': {
            'duration_sec': pass_duration_sec,
            'max_elevation_deg': max_elevation_deg,
            'num_transmissions': num_transmissions
        },
        'transmissions': [],
        'timeline': {
            'times': transmission_times,
            'elevations': [],
            'snrs': [],
            'bers': []
        }
    }

    # Run transmission at each time point
    for i, t in enumerate(transmission_times):
        elevation = sat_pass.elevation_at_time(t)

        # SNR varies with elevation (higher = better signal)
        # Simple model: SNR scales linearly with elevation
        snr_db = min_snr_db + (max_snr_db - min_snr_db) * (elevation / max_elevation_deg)

        # Distance varies with elevation (higher = closer)
        # Simple model: distance decreases as satellite rises
        distance_km = 2000 - 1000 * (elevation / max_elevation_deg)

        print(f"\n📡 Transmission {i+1}/{num_transmissions}")
        print(f"   Time: {t:.1f} sec into pass")
        print(f"   Elevation: {elevation:.1f}°")
        print(f"   Distance: {distance_km:.0f} km")

        # Run transmission
        tx_result = simulate_transmission(
            message=message,
            distance_km=distance_km,
            snr_db=snr_db,
            use_fec=use_fec,
            save_to_db=False  # Don't save individual transmissions
        )

        # Store results
        results['transmissions'].append(tx_result)
        results['timeline']['elevations'].append(elevation)
        results['timeline']['snrs'].append(tx_result['snr_actual_db'])
        results['timeline']['bers'].append(tx_result['ber'])

    # Save aggregate pass data
    avg_ber = np.mean(results['timeline']['bers'])
    avg_snr = np.mean(results['timeline']['snrs'])
    total_errors = sum(tx['packets_corrupted'] for tx in results['transmissions'])

    print("\n" + "=" * 60)
    print("SATELLITE PASS COMPLETE!")
    print("=" * 60)
    print(f"Transmissions: {num_transmissions}")
    print(f"Average BER: {avg_ber:.6f}")
    print(f"Average SNR: {avg_snr:.1f} dB")
    print(f"Packet errors: {total_errors}/{num_transmissions}")
    print("=" * 60)

    # Save pass summary to database
    save_mission(
        message_sent=f"Satellite Pass: {num_transmissions} transmissions",
        message_received=f"{num_transmissions - total_errors} successful",
        ber=avg_ber,
        snr_db=avg_snr,
        packets_total=num_transmissions,
        packets_corrupted=total_errors,
        metadata={
            'pass_duration_sec': pass_duration_sec,
            'max_elevation_deg': max_elevation_deg,
            'type': 'satellite_pass'
        }
    )

    return results


# ═══════════════════════════════════════════════════════════════
# DEBUGGING NOTES
# ═══════════════════════════════════════════════════════════════
#
# Common Issues:
#   1. "Module not found" → Check sys.path and imports
#   2. BER always 0 or 1 → Check SNR settings (too high/low)
#   3. Crashes on decode → Check bit length alignment
#   4. CRC always fails → Check packet format consistency
#
# Testing Tips:
#   - Start with high SNR (30 dB) to verify pipeline works
#   - Gradually decrease SNR to see error behavior
#   - Test with/without FEC to see difference
#   - Try different message lengths
#
# Performance Notes:
#   - Current implementation prioritizes clarity over speed
#   - For long messages, consider batching or streaming
#   - Signal arrays can get large - watch memory usage
#
# ═══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# FUTURE IMPROVEMENTS
# ═══════════════════════════════════════════════════════════════
#
# For ORBITER-1 (Intermediate):
#   [ ] Multi-packet messages with fragmentation
#   [ ] Automatic Repeat Request (ARQ) protocol
#   [ ] Adaptive FEC based on channel quality
#   [ ] Reed-Solomon codes for burst errors
#   [ ] Multiple ground stations
#   [ ] Handoff between ground stations
#   [ ] Real-time visualization during transmission
#   [ ] Doppler shift simulation
#
# For ORBITER-DEEP-SPACE (Advanced):
#   [ ] Convolutional codes
#   [ ] Turbo codes and LDPC
#   [ ] Extremely low SNR scenarios (-10 dB)
#   [ ] Long propagation delays (minutes/hours)
#   [ ] Interplanetary communication protocols
#   [ ] Power-limited transmission
#   [ ] Multi-antenna systems (MIMO)
#
# ═══════════════════════════════════════════════════════════════
