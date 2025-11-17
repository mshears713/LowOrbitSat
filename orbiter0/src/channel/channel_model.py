"""
═══════════════════════════════════════════════════════════════════
MODULE: channel/channel_model.py
PURPOSE: Unified channel model combining all signal impairments
THEME: The complete journey from satellite to ground station
═══════════════════════════════════════════════════════════════════

📡 STORY:
This module ties together everything that happens to a signal
as it travels from our satellite down to Earth.

The signal goes through multiple stages:
  1. Modulation (bits → BPSK signal)
  2. Range loss (weakens with distance)
  3. Noise addition (cosmic + atmospheric + receiver)

This is our "end-to-end" signal chain for Phase 2!

LEARNING GOALS:
  • Understanding the complete transmission pipeline
  • How multiple impairments combine
  • Configurable channel parameters
  • Realistic signal degradation modeling

SIMPLIFICATIONS:
  - No fading yet (that's Phase 3)
  - No atmospheric absorption yet
  - Perfect timing and synchronization
  - Simplified physics

═══════════════════════════════════════════════════════════════════
"""

# ┌────────────────────────────────────────────────────────┐
# │           UNIFIED CHANNEL MODEL PIPELINE               │
# ├────────────────────────────────────────────────────────┤
# │                                                        │
# │  Text Message                                          │
# │       │                                                │
# │       ▼                                                │
# │  [BPSK Modulation]  ──► Modulated Signal              │
# │       │                                                │
# │       ▼                                                │
# │  [Range Loss]       ──► Attenuated Signal             │
# │       │                                                │
# │       ▼                                                │
# │  [AWGN Noise]       ──► Noisy Signal                  │
# │       │                                                │
# │       ▼                                                │
# │  Received Signal (ready for demodulation)             │
# │                                                        │
# └────────────────────────────────────────────────────────┘

import numpy as np
import sys
sys.path.append('..')  # To import from sibling directories

from signal.modulation import (
    text_to_bits, bits_to_bpsk_symbols, modulate_bpsk,
    demodulate_bpsk, bpsk_symbols_to_bits, bits_to_text
)
from channel.noise import add_awgn
from channel.range_loss import apply_free_space_loss


class ChannelModel:
    """
    Unified channel model for satellite-to-ground transmission.

    🎓 TEACHING NOTE:
    This class encapsulates all the channel effects we've learned about.
    It provides a simple interface for end-to-end simulation.

    Parameters
    ----------
    carrier_freq_hz : float
        Carrier frequency for modulation (e.g., 1000 Hz)
    sample_rate_hz : int
        Sampling rate (e.g., 10000 Hz)
    distance_km : float
        Satellite-to-ground distance (e.g., 1000 km)
    snr_db : float
        Signal-to-noise ratio in dB (e.g., 15 dB)
    """

    def __init__(self, carrier_freq_hz=1000, sample_rate_hz=10000,
                 distance_km=1000, snr_db=15):
        self.carrier_freq_hz = carrier_freq_hz
        self.sample_rate_hz = sample_rate_hz
        self.distance_km = distance_km
        self.snr_db = snr_db

    def transmit(self, message_text):
        """
        Simulate complete transmission through the channel.

        🎓 TEACHING NOTE:
        This function runs the full signal chain:
        text → bits → symbols → modulated → degraded

        Parameters
        ----------
        message_text : str
            Message to transmit

        Returns
        -------
        results : dict
            Dictionary containing:
            - 'transmitted_signal': Original modulated signal
            - 'received_signal': Signal after channel effects
            - 'noise': Noise that was added
            - 'bits_transmitted': Original bit sequence
            - 'symbols_transmitted': Original BPSK symbols
            - 'message_text': Original message
        """
        # Step 1: Convert text to bits
        # 🎓 This is how computers represent text
        bits = text_to_bits(message_text)

        # Step 2: Convert bits to BPSK symbols
        # 🎓 0 → -1, 1 → +1
        symbols = bits_to_bpsk_symbols(bits)

        # Step 3: Modulate symbols onto carrier
        # 🎓 Creates the actual radio wave
        transmitted_signal, time_axis = modulate_bpsk(
            symbols,
            self.carrier_freq_hz,
            self.sample_rate_hz
        )

        # Step 4: Apply range loss (distance attenuation)
        # 🎓 Signal weakens as it travels through space
        attenuated_signal, attenuation_factor = apply_free_space_loss(
            transmitted_signal,
            self.distance_km,
            reference_distance_km=1.0
        )

        # Step 5: Add noise (AWGN)
        # 🎓 Real channels always have noise
        received_signal, noise = add_awgn(attenuated_signal, self.snr_db)

        # Return all intermediate results for inspection
        return {
            'transmitted_signal': transmitted_signal,
            'attenuated_signal': attenuated_signal,
            'received_signal': received_signal,
            'noise': noise,
            'time_axis': time_axis,
            'bits_transmitted': bits,
            'symbols_transmitted': symbols,
            'message_text': message_text,
            'attenuation_factor': attenuation_factor
        }

    def receive(self, received_signal, num_symbols):
        """
        Demodulate and decode a received signal.

        🎓 TEACHING NOTE:
        This reverses the modulation process:
        noisy signal → symbols → bits → text

        Parameters
        ----------
        received_signal : ndarray
            Signal to demodulate (with noise and attenuation)
        num_symbols : int
            Number of symbols to expect

        Returns
        -------
        results : dict
            Dictionary containing:
            - 'symbols_received': Demodulated symbols
            - 'bits_received': Decoded bits
            - 'message_received': Recovered text
        """
        # Step 1: Demodulate BPSK signal to symbols
        # 🎓 Try to recover the +1/-1 symbols despite noise
        symbols_received = demodulate_bpsk(
            received_signal,
            self.carrier_freq_hz,
            self.sample_rate_hz,
            num_symbols
        )

        # Step 2: Convert symbols back to bits
        # 🎓 +1 → 1, -1 → 0
        bits_received = bpsk_symbols_to_bits(symbols_received)

        # Step 3: Convert bits back to text
        # 🎓 May have errors if noise was too strong!
        message_received = bits_to_text(bits_received)

        return {
            'symbols_received': symbols_received,
            'bits_received': bits_received,
            'message_received': message_received
        }

    def end_to_end(self, message_text):
        """
        Complete end-to-end transmission and reception.

        🎓 TEACHING NOTE:
        This is the complete simulation: transmit → channel → receive

        Useful for:
        - Testing different SNR values
        - Seeing how distance affects quality
        - Comparing transmitted vs received messages

        Parameters
        ----------
        message_text : str
            Message to send through the channel

        Returns
        -------
        results : dict
            Combined results from transmit() and receive()
        """
        # Transmit through channel
        tx_results = self.transmit(message_text)

        # Receive and decode
        num_symbols = len(tx_results['symbols_transmitted'])
        rx_results = self.receive(tx_results['received_signal'], num_symbols)

        # Combine results
        results = {**tx_results, **rx_results}

        # Add comparison metrics
        bits_match = (tx_results['bits_transmitted'] ==
                      rx_results['bits_received'])
        results['bit_errors'] = np.sum(~bits_match) if hasattr(bits_match, '__iter__') else 0
        results['total_bits'] = len(tx_results['bits_transmitted'])

        return results


# ═══ CONVENIENCE FUNCTIONS ═══

def simulate_transmission(message, carrier_freq_hz=1000, sample_rate_hz=10000,
                         distance_km=1000, snr_db=15):
    """
    Quick function to simulate a transmission with default parameters.

    🎓 TEACHING NOTE:
    Use this for quick tests without creating a ChannelModel object.

    Parameters
    ----------
    message : str
        Text message to transmit
    carrier_freq_hz : float
        Carrier frequency (default: 1000 Hz)
    sample_rate_hz : int
        Sampling rate (default: 10000 Hz)
    distance_km : float
        Distance (default: 1000 km)
    snr_db : float
        Signal-to-noise ratio (default: 15 dB)

    Returns
    -------
    results : dict
        Complete simulation results
    """
    channel = ChannelModel(carrier_freq_hz, sample_rate_hz,
                          distance_km, snr_db)
    return channel.end_to_end(message)


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Received message is gibberish? SNR too low or distance too far
#   2. No signal at all? Check carrier frequency and sample rate
#   3. Message partially correct? That's normal with noise! Check BER
#
# Testing Tips:
#   - Start with high SNR (30 dB) to verify modulation works
#   - Gradually lower SNR to see degradation
#   - Try different distances: 100 km, 1000 km, 10000 km
#   - Compare transmitted vs received signals visually
#
# Gotchas:
#   - Very long messages need more samples (memory!)
#   - Sample rate must be high enough for carrier frequency
#   - Too much noise can make everything random


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Phase 3:
#   [ ] Add fade events to the channel
#   [ ] Implement atmospheric absorption
#   [ ] Support time-varying channels
#
# For Advanced Version (ORBITER-1):
#   [ ] Multiple paths (multipath fading)
#   [ ] Doppler shift
#   [ ] Frequency-selective fading
#   [ ] Real orbital mechanics
