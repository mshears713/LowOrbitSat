#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════
ORBITER-0 SELF-TEST SUITE
Complete validation and debugging tests
═══════════════════════════════════════════════════════════════════

📡 PURPOSE:
Validates that all components of ORBITER-0 are working correctly.
Run this before demos to ensure everything is operational!

USAGE:
  python tests/self_test.py

All tests should PASS. If any fail, see debugging notes.

═══════════════════════════════════════════════════════════════════
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np

print("=" * 70)
print("ORBITER-0 SELF-TEST SUITE")
print("=" * 70)
print()

# Track test results
tests_run = 0
tests_passed = 0
tests_failed = 0


def test(name, condition, error_msg=""):
    """Helper function to run a test."""
    global tests_run, tests_passed, tests_failed
    tests_run += 1

    if condition:
        print(f"✅ PASS: {name}")
        tests_passed += 1
        return True
    else:
        print(f"❌ FAIL: {name}")
        if error_msg:
            print(f"   Error: {error_msg}")
        tests_failed += 1
        return False


# ═══════════════════════════════════════════════════════════════
# TEST 1: IMPORTS
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST GROUP 1: Module Imports")
print("=" * 70)

try:
    from src.signals.generator import generate_sine
    test("Import signals.generator", True)
except Exception as e:
    test("Import signals.generator", False, str(e))

try:
    from src.signals.modulation import text_to_bits, bits_to_bpsk_symbols
    test("Import signals.modulation", True)
except Exception as e:
    test("Import signals.modulation", False, str(e))

try:
    from src.channel.noise import add_awgn
    test("Import channel.noise", True)
except Exception as e:
    test("Import channel.noise", False, str(e))

try:
    from src.comms.packetizer import create_packet, validate_packet
    test("Import comms.packetizer", True)
except Exception as e:
    test("Import comms.packetizer", False, str(e))

try:
    from src.runtime.pipeline import simulate_transmission
    test("Import runtime.pipeline", True)
except Exception as e:
    test("Import runtime.pipeline", False, str(e))

print()

# ═══════════════════════════════════════════════════════════════
# TEST 2: SIGNAL GENERATION
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST GROUP 2: Signal Generation")
print("=" * 70)

try:
    t, sig = generate_sine(10, 1.0, 1.0, 1000)
    test("Generate sine wave", len(sig) > 0)
    test("Sine amplitude correct", abs(np.max(sig) - 1.0) < 0.01,
         f"Expected ~1.0, got {np.max(sig):.3f}")
    test("Time axis length matches signal", len(t) == len(sig))
except Exception as e:
    test("Signal generation", False, str(e))

print()

# ═══════════════════════════════════════════════════════════════
# TEST 3: MODULATION
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST GROUP 3: Modulation")
print("=" * 70)

try:
    # Test text to bits
    bits = text_to_bits("Hi")
    test("Text to bits conversion", len(bits) == 16,  # 2 chars * 8 bits
         f"Expected 16 bits, got {len(bits)}")

    # Test BPSK mapping
    symbols = bits_to_bpsk_symbols([0, 1, 0, 1])
    expected = np.array([-1, 1, -1, 1])
    test("BPSK symbol mapping", np.allclose(symbols, expected),
         f"Expected {expected}, got {symbols}")
except Exception as e:
    test("Modulation", False, str(e))

print()

# ═══════════════════════════════════════════════════════════════
# TEST 4: NOISE
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST GROUP 4: Noise Addition")
print("=" * 70)

try:
    signal = np.ones(1000)
    noisy = add_awgn(signal, snr_db=20)

    test("Noise generation", len(noisy) == len(signal))
    test("Noise changes signal", not np.allclose(signal, noisy),
         "Signal unchanged - no noise added!")

    # Check that noise is reasonable
    snr_measured = 10 * np.log10(np.mean(signal**2) / np.mean((noisy-signal)**2))
    test("SNR approximately correct", abs(snr_measured - 20) < 5,
         f"Expected ~20 dB, got {snr_measured:.1f} dB")
except Exception as e:
    test("Noise addition", False, str(e))

print()

# ═══════════════════════════════════════════════════════════════
# TEST 5: PACKETS
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST GROUP 5: Packetization")
print("=" * 70)

try:
    payload = b"Test message"
    packet = create_packet(payload)

    test("Packet creation", len(packet) > len(payload),
         "Packet should be larger than payload (has headers)")

    # Packet should be valid (no corruption)
    test("Packet validation (clean)", validate_packet(packet))

    # Corrupted packet should fail
    corrupted = bytearray(packet)
    corrupted[10] ^= 0xFF  # Flip bits in middle
    test("Packet validation (corrupted)", not validate_packet(bytes(corrupted)))
except Exception as e:
    test("Packetization", False, str(e))

print()

# ═══════════════════════════════════════════════════════════════
# TEST 6: END-TO-END PIPELINE
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST GROUP 6: End-to-End Pipeline")
print("=" * 70)

try:
    # Test 1: Perfect conditions
    result = simulate_transmission(
        message="Hello",
        snr_db=40,  # Very high SNR
        distance_km=100,
        use_fec=False,
        save_to_db=False
    )

    test("Pipeline execution", result is not None)
    test("Message sent stored", result['message_sent'] == "Hello")
    test("Perfect transmission (high SNR)", result['ber'] < 0.01,
         f"BER = {result['ber']:.4f}")

    # Test 2: Noisy conditions
    result_noisy = simulate_transmission(
        message="Test",
        snr_db=10,
        distance_km=1000,
        use_fec=False,
        save_to_db=False
    )

    test("Noisy transmission has errors", result_noisy['ber'] > 0,
         "Expected some errors at 10 dB SNR")

except Exception as e:
    test("End-to-end pipeline", False, str(e))

print()

# ═══════════════════════════════════════════════════════════════
# TEST 7: UTILITIES
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST GROUP 7: Utilities")
print("=" * 70)

try:
    from src.utils.math_helpers import calculate_ber
    ber = calculate_ber([0, 1, 0, 1], [0, 1, 1, 1])  # 1 error out of 4
    test("BER calculation", abs(ber - 0.25) < 0.01,
         f"Expected 0.25, got {ber}")
except Exception as e:
    test("Utility functions", False, str(e))

try:
    from src.utils.plotting import plot_signal
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend

    t = np.linspace(0, 1, 100)
    sig = np.sin(2 * np.pi * 5 * t)
    fig = plot_signal(t, sig, show_teaching_notes=False)
    test("Plotting functions", fig is not None)
except Exception as e:
    test("Plotting functions", False, str(e))

print()

# ═══════════════════════════════════════════════════════════════
# TEST 8: CONFIGURATION
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST GROUP 8: Configuration")
print("=" * 70)

config_path = Path(__file__).parent.parent / "src" / "config" / "default_params.yaml"
test("Config file exists", config_path.exists(),
     f"Not found: {config_path}")

if config_path.exists():
    try:
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
        test("Config file valid YAML", config is not None)
        test("Config has signal section", 'signal' in config)
        test("Config has channel section", 'channel' in config)
    except Exception as e:
        test("Config file parsing", False, str(e))

print()

# ═══════════════════════════════════════════════════════════════
# FINAL RESULTS
# ═══════════════════════════════════════════════════════════════

print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)
print(f"Tests Run:    {tests_run}")
print(f"Tests Passed: {tests_passed} ✅")
print(f"Tests Failed: {tests_failed} ❌")
print()

if tests_failed == 0:
    print("🎉 ALL TESTS PASSED! System is operational.")
    print()
    print("You're ready to:")
    print("  • Run Streamlit demos")
    print("  • Execute simulations")
    print("  • Show to students")
    print()
    sys.exit(0)
else:
    print("⚠️  SOME TESTS FAILED!")
    print()
    print("Debugging tips:")
    print("  1. Check import paths (src/ directory structure)")
    print("  2. Verify dependencies installed (requirements.txt)")
    print("  3. Review error messages above")
    print("  4. Check Phase 5 implementation status")
    print()
    sys.exit(1)
