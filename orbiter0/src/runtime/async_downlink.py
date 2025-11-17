"""
═══════════════════════════════════════════════════════════════════
MODULE: runtime/async_downlink.py
PURPOSE: Asynchronous real-time downlink simulation
THEME: Simulating live satellite communication streams
═══════════════════════════════════════════════════════════════════

📡 STORY:
Real satellites don't transmit everything at once!
They send data continuously as packets arrive over time.

This module uses Python's async/await to simulate:
  • Live packet streams
  • Real-time telemetry updates
  • Concurrent ground station operations
  • Non-blocking UI updates (perfect for Streamlit!)

ASYNC vs SYNC:
┌──────────────────────────────────────────────────────────────┐
│ SYNCHRONOUS (blocking):                                       │
│   transmit_packet_1()  ← Wait...                             │
│   transmit_packet_2()  ← Wait...                             │
│   transmit_packet_3()  ← Wait...                             │
│                                                               │
│ ASYNCHRONOUS (non-blocking):                                 │
│   await transmit_packet_1()  ← Can do other things!          │
│   await transmit_packet_2()                                   │
│   await transmit_packet_3()                                   │
│   (UI stays responsive!)                                      │
└──────────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • Introduction to async/await in Python
  • Concurrent programming concepts
  • Real-time simulation patterns
  • Event-driven architecture
  • Streaming data processing

SIMPLIFICATIONS:
  - Simulated delays (not actual I/O)
  - Single satellite (no multi-sat coordination)
  - Simplified event loop
  - No advanced async patterns (no workers/pools)

═══════════════════════════════════════════════════════════════════
"""

# ┌────────────────────────────────────────────────────────────┐
# │              ASYNC DOWNLINK PIPELINE                       │
# ├────────────────────────────────────────────────────────────┤
# │                                                            │
# │  Satellite (async generator)                               │
# │       ↓  yields packets continuously                       │
# │  Ground Station (async consumer)                           │
# │       ↓  processes as they arrive                          │
# │  Telemetry Logger (async writer)                           │
# │       ↓  saves in background                               │
# │  UI Updater (async callback)                               │
# │       ↓  displays without blocking                         │
# │                                                            │
# └────────────────────────────────────────────────────────────┘

import asyncio
import time
import numpy as np
from typing import AsyncGenerator, Dict, List, Optional, Callable
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from runtime.pipeline import simulate_transmission


# ═══════════════════════════════════════════════════════════════
# ASYNC PACKET STREAM GENERATOR
# ═══════════════════════════════════════════════════════════════

async def packet_stream(
    messages: List[str],
    interval_sec: float = 1.0,
    **transmission_params
) -> AsyncGenerator[Dict, None]:
    """
    Generate packet stream asynchronously.

    🎓 TEACHING NOTE:
    This is an "async generator" - it yields packets one at a time
    without blocking the program.

    Think of it like a water fountain:
    - Regular function: gives you all the water at once (flood!)
    - Generator: gives you water in sips
    - Async generator: gives you water in sips while you do other stuff

    The "yield" keyword returns a value but keeps the function alive
    for the next call. The "await" keyword lets other code run while
    we're waiting.

    Parameters
    ----------
    messages : list of str
        Messages to transmit in sequence
    interval_sec : float
        Time between packet transmissions
    **transmission_params
        Parameters passed to simulate_transmission()

    Yields
    ------
    result : dict
        Transmission result for each packet
    """

    print(f"📡 Starting async packet stream ({len(messages)} packets)...")
    print(f"   Interval: {interval_sec} sec")
    print()

    for i, message in enumerate(messages):
        print(f"⏱️  Transmitting packet {i+1}/{len(messages)}: \"{message}\"")

        # Simulate transmission (runs synchronously but quickly)
        result = simulate_transmission(
            message=message,
            save_to_db=False,  # We'll batch save later
            **transmission_params
        )

        # Add metadata
        result['packet_number'] = i + 1
        result['total_packets'] = len(messages)
        result['timestamp'] = time.time()

        # 🎓 YIELD: Return this packet but keep function alive
        yield result

        # 🎓 AWAIT: Pause without blocking (let other tasks run)
        if i < len(messages) - 1:  # Don't wait after last packet
            await asyncio.sleep(interval_sec)

    print()
    print("✅ Packet stream complete!")


# ═══════════════════════════════════════════════════════════════
# ASYNC LIVE DOWNLINK SIMULATION
# ═══════════════════════════════════════════════════════════════

async def simulate_live_downlink(
    messages: List[str],
    interval_sec: float = 1.0,
    on_packet_callback: Optional[Callable] = None,
    **transmission_params
) -> Dict:
    """
    Simulate live downlink with real-time packet processing.

    🎓 TEACHING NOTE:
    This is the main async function that orchestrates everything.
    It's declared with "async def" and must be run with "await".

    The "on_packet_callback" lets you hook in a function that runs
    each time a packet arrives - perfect for updating a UI!

    Parameters
    ----------
    messages : list of str
        Messages to transmit
    interval_sec : float
        Time between packets
    on_packet_callback : callable, optional
        Function called with each packet: callback(result)
    **transmission_params
        Parameters for transmission

    Returns
    -------
    summary : dict
        Complete downlink summary with all packets
    """

    start_time = time.time()
    results = []
    total_errors = 0
    total_bits = 0
    total_bit_errors = 0

    print("=" * 60)
    print("🛰️  LIVE DOWNLINK SIMULATION")
    print("=" * 60)

    # 🎓 ASYNC FOR: Iterate over async generator
    # As each packet arrives, process it immediately
    async for result in packet_stream(messages, interval_sec, **transmission_params):

        # Collect statistics
        results.append(result)
        total_bits += len(result['transmitted_bits'])
        total_bit_errors += result['total_bit_errors']

        if not result['packet_valid']:
            total_errors += 1

        # 🎓 CALLBACK: Notify external code (e.g., UI update)
        if on_packet_callback:
            # Callback can be sync or async
            if asyncio.iscoroutinefunction(on_packet_callback):
                await on_packet_callback(result)
            else:
                on_packet_callback(result)

    elapsed_time = time.time() - start_time
    overall_ber = total_bit_errors / total_bits if total_bits > 0 else 0

    # Summary
    summary = {
        'total_packets': len(messages),
        'successful_packets': len(messages) - total_errors,
        'corrupted_packets': total_errors,
        'overall_ber': overall_ber,
        'total_bit_errors': total_bit_errors,
        'total_bits': total_bits,
        'elapsed_time_sec': elapsed_time,
        'packets': results
    }

    print()
    print("=" * 60)
    print("LIVE DOWNLINK COMPLETE!")
    print("=" * 60)
    print(f"Packets: {summary['successful_packets']}/{summary['total_packets']} successful")
    print(f"Overall BER: {overall_ber:.6f}")
    print(f"Time: {elapsed_time:.2f} seconds")
    print("=" * 60)

    return summary


# ═══════════════════════════════════════════════════════════════
# ASYNC SATELLITE PASS WITH LIVE UPDATES
# ═══════════════════════════════════════════════════════════════

async def simulate_live_satellite_pass(
    message: str,
    pass_duration_sec: float = 300,
    num_transmissions: int = 10,
    on_packet_callback: Optional[Callable] = None,
    **transmission_params
) -> Dict:
    """
    Simulate satellite pass with live updates as it happens.

    🎓 TEACHING NOTE:
    This simulates a satellite pass in real-time, with signal
    strength changing as the satellite moves across the sky.

    Perfect for live dashboards and visualizations!

    Parameters
    ----------
    message : str
        Message to transmit repeatedly
    pass_duration_sec : float
        Total pass duration
    num_transmissions : int
        Number of transmissions during pass
    on_packet_callback : callable, optional
        Called with each packet result
    **transmission_params
        Transmission parameters

    Returns
    -------
    summary : dict
        Complete pass summary
    """

    print("=" * 60)
    print("🛰️  LIVE SATELLITE PASS SIMULATION")
    print("=" * 60)

    # Calculate transmission schedule
    interval = pass_duration_sec / num_transmissions

    # Create list of messages (same message repeated)
    messages = [message] * num_transmissions

    # Simulate with varying SNR
    # SNR follows a parabolic curve (low → high → low)
    results = []
    start_time = time.time()

    for i in range(num_transmissions):
        # Calculate progress through pass (0 to 1)
        progress = i / (num_transmissions - 1) if num_transmissions > 1 else 0.5

        # SNR follows inverted parabola: peaks at middle of pass
        # y = -4(x - 0.5)^2 + 1
        # Normalized to 0-1, then scale to SNR range
        snr_normalized = 1 - 4 * (progress - 0.5)**2
        min_snr = transmission_params.get('snr_db', 5) - 10
        max_snr = transmission_params.get('snr_db', 5) + 10
        current_snr = min_snr + snr_normalized * (max_snr - min_snr)

        # Distance inversely related to SNR (closer = better signal)
        distance_km = 2500 - 1000 * snr_normalized

        # Elevation angle (0° at horizon, peaks at zenith)
        elevation_deg = 90 * snr_normalized

        print(f"\n📡 Transmission {i+1}/{num_transmissions}")
        print(f"   Progress: {progress*100:.0f}% through pass")
        print(f"   Elevation: {elevation_deg:.1f}°")
        print(f"   Distance: {distance_km:.0f} km")
        print(f"   Dynamic SNR: {current_snr:.1f} dB")

        # Run transmission with dynamic parameters
        params = transmission_params.copy()
        params['snr_db'] = current_snr
        params['distance_km'] = distance_km

        result = simulate_transmission(
            message=message,
            save_to_db=False,
            **params
        )

        # Add pass-specific metadata
        result['packet_number'] = i + 1
        result['total_packets'] = num_transmissions
        result['pass_progress'] = progress
        result['elevation_deg'] = elevation_deg
        result['timestamp'] = time.time()

        results.append(result)

        # Callback for real-time updates
        if on_packet_callback:
            if asyncio.iscoroutinefunction(on_packet_callback):
                await on_packet_callback(result)
            else:
                on_packet_callback(result)

        # Wait before next transmission
        if i < num_transmissions - 1:
            await asyncio.sleep(interval)

    elapsed_time = time.time() - start_time

    # Calculate summary statistics
    total_errors = sum(1 for r in results if not r['packet_valid'])
    avg_ber = np.mean([r['ber'] for r in results])
    avg_snr = np.mean([r['snr_actual_db'] for r in results])

    summary = {
        'pass_duration_sec': pass_duration_sec,
        'num_transmissions': num_transmissions,
        'successful_packets': num_transmissions - total_errors,
        'corrupted_packets': total_errors,
        'avg_ber': avg_ber,
        'avg_snr': avg_snr,
        'elapsed_time_sec': elapsed_time,
        'packets': results
    }

    print()
    print("=" * 60)
    print("SATELLITE PASS COMPLETE!")
    print("=" * 60)
    print(f"Transmissions: {summary['successful_packets']}/{num_transmissions} successful")
    print(f"Average BER: {avg_ber:.6f}")
    print(f"Average SNR: {avg_snr:.1f} dB")
    print(f"Time: {elapsed_time:.2f} seconds")
    print("=" * 60)

    return summary


# ═══════════════════════════════════════════════════════════════
# HELPER: RUN ASYNC FUNCTION IN SYNC CONTEXT
# ═══════════════════════════════════════════════════════════════

def run_async(async_func, *args, **kwargs):
    """
    Run an async function from synchronous code.

    🎓 TEACHING NOTE:
    Async functions need to run in an "event loop".
    This helper creates one and runs your async function.

    Use this when calling async functions from:
    - Regular Python scripts
    - Jupyter notebooks
    - Streamlit apps

    Parameters
    ----------
    async_func : async function
        The async function to run
    *args, **kwargs
        Arguments to pass to the function

    Returns
    -------
    result
        Whatever the async function returns
    """

    # 🎓 TRY TO GET EXISTING EVENT LOOP
    # (Jupyter/Streamlit might already have one running)
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Can't use run_until_complete on running loop
            # Create a new event loop in a thread (advanced)
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(async_func(*args, **kwargs))
    except RuntimeError:
        pass

    # 🎓 CREATE NEW EVENT LOOP
    # This is the simple case for regular Python scripts
    return asyncio.run(async_func(*args, **kwargs))


# ═══════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════

async def example_live_downlink():
    """
    Example of live downlink with callback.

    🎓 TEACHING NOTE:
    This shows how to use the async downlink with a callback
    function that updates in real-time.
    """

    print("Example: Live downlink with callback\n")

    # Define callback for packet arrival
    def on_packet_received(result):
        """Called each time a packet arrives."""
        msg = result['message_received']
        ber = result['ber']
        status = "✅" if result['perfect_match'] else "⚠️"
        print(f"   {status} Received: \"{msg}\" (BER: {ber:.4f})")

    # Messages to transmit
    messages = [
        "Hello from orbit!",
        "Satellite status: nominal",
        "Temperature: 25°C",
        "Battery: 87%",
        "Mission complete!"
    ]

    # Run live downlink
    summary = await simulate_live_downlink(
        messages=messages,
        interval_sec=0.5,
        snr_db=12,
        distance_km=1500,
        use_fec=True,
        on_packet_callback=on_packet_received
    )

    return summary


# ═══════════════════════════════════════════════════════════════
# MAIN (for testing)
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("ORBITER-0 Async Downlink Test")
    print("=" * 60)
    print()

    # Run example
    result = run_async(example_live_downlink)

    print()
    print("Test complete!")


# ═══════════════════════════════════════════════════════════════
# DEBUGGING NOTES
# ═══════════════════════════════════════════════════════════════
#
# Common Issues:
#   1. "RuntimeError: Event loop is already running"
#      → Use run_async() helper or nest_asyncio
#   2. "TypeError: object is not iterable"
#      → Make sure using "async for" not regular "for"
#   3. Callback not being called
#      → Check if callback function is defined correctly
#   4. Streamlit crashes with async
#      → Wrap async calls with run_async() helper
#
# Testing Tips:
#   - Start with small packet counts (2-3)
#   - Test callback with print() first
#   - Use short intervals (0.1 sec) for faster testing
#   - Check asyncio.run() vs run_until_complete() behavior
#
# Performance Notes:
#   - Async doesn't make computation faster
#   - It makes waiting non-blocking (good for UI)
#   - For CPU-bound work, consider multiprocessing instead
#
# ═══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# FUTURE IMPROVEMENTS
# ═══════════════════════════════════════════════════════════════
#
# For ORBITER-1:
#   [ ] Concurrent multi-ground-station reception
#   [ ] Async packet queue with priorities
#   [ ] Backpressure handling (slow consumers)
#   [ ] Websocket streaming to browser
#   [ ] Real-time plotting updates
#   [ ] Async database writes (bulk insert)
#   [ ] Cancellation support (abort mission)
#
# For Advanced Version:
#   [ ] Distributed async (multiple satellites)
#   [ ] Task pools and worker queues
#   [ ] Async context managers
#   [ ] Stream processing with buffering
#   [ ] Rate limiting and throttling
#
# ═══════════════════════════════════════════════════════════════
