# ORBITER-0: Claude Code Development Guide

## Project Overview

**ORBITER-0** is a beginner-friendly satellite communications simulation and Streamlit learning console. This is a **teaching-oriented** project that prioritizes clarity, visual learning, and intuition over production-level optimization or complex physics.

**Theme:** A tiny CubeSat drifting over Earth, sending packets to ground stations
**Audience:** Beginners learning wireless communications fundamentals
**Tech Stack:** Python, Streamlit, NumPy, Matplotlib, SQLite
**Structure:** 5 Phases, 50 Steps, 10 Interactive Learning Chapters

---

## Core Philosophy

### Teaching Over Performance
- **Clarity > Efficiency**: Write verbose, educational code with extensive comments
- **Visuals First**: Every concept should have a visualization or interactive demo
- **Gentle Math**: Simplify physics and mathematics for accessibility
- **Narrative Style**: Code should read like a story, not just execute

### Project Constraints
⚠️ **CRITICAL RULES:**
1. **DO NOT modify README.md after Phase 1**
2. **Follow phases sequentially** - do not skip ahead
3. **Do not merge steps** - each step is discrete
4. **Every file needs:** narrative header, ASCII diagram, teaching comments, debugging notes, future improvements
5. **No new directories** unless explicitly required by a step

---

## Required Code Documentation Style

### Every Python File Must Include:

#### 1. Narrative Header Docstring
```python
"""
═══════════════════════════════════════════════════════════════════
MODULE: signal/generator.py
PURPOSE: Generate beginner-friendly waveforms for satellite downlink
THEME: Teaching how signals are born before they travel to Earth
═══════════════════════════════════════════════════════════════════

📡 STORY:
Before a satellite can talk to Earth, it needs to create a SIGNAL.
Think of signals as waves of energy rippling through space.

This module generates the simplest possible waveforms:
  - Sine waves (smooth and predictable)
  - Square waves (abrupt and digital-like)
  - BPSK modulated signals (bits encoded as phase flips)

LEARNING GOALS:
  • What a signal is (samples over time)
  • How frequency and amplitude work
  • How to visualize waveforms
  • Intro to digital vs analog signals

SIMPLIFICATIONS:
  - No complex propagation physics
  - Time is discrete (sampled)
  - Perfect signal generation (no hardware noise)

═══════════════════════════════════════════════════════════════════
"""
```

#### 2. ASCII Diagrams for Major Components
```python
# ┌─────────────────────────────────────────────────┐
# │          SIGNAL GENERATION PIPELINE            │
# ├─────────────────────────────────────────────────┤
# │                                                 │
# │  Frequency   ──┐                               │
# │  Amplitude   ──┤─► Generator ─► Samples Array  │
# │  Duration    ──┘                               │
# │                                                 │
# │  Output: numpy array of time-domain samples    │
# └─────────────────────────────────────────────────┘
```

#### 3. Inline Teaching Commentary
```python
def generate_sine(frequency_hz, amplitude, duration_sec, sample_rate_hz):
    """
    Generate a pure sine wave.

    🎓 TEACHING NOTE:
    A sine wave is the most fundamental signal in nature.
    It's what you get when something oscillates smoothly.

    Formula: amplitude * sin(2π * frequency * time)

    WHY THIS MATTERS:
    Real satellite signals aren't pure sines, but understanding
    them is the foundation for understanding everything else.
    """
    # Create time axis (this is where our signal lives)
    num_samples = int(duration_sec * sample_rate_hz)
    time_axis = np.linspace(0, duration_sec, num_samples)

    # Generate the wave (magic happens here!)
    # 2π converts frequency to radians per second
    angular_freq = 2 * np.pi * frequency_hz
    signal = amplitude * np.sin(angular_freq * time_axis)

    return time_axis, signal
```

#### 4. Debugging Notes
```python
# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Signal all zeros? Check that amplitude > 0
#   2. Signal looks choppy? Increase sample_rate_hz
#   3. Wrong frequency? Verify units (Hz not MHz)
#
# Testing Tips:
#   - Plot first 100 samples to verify shape
#   - Check signal.max() == amplitude
#   - Count zero crossings to verify frequency
#
# Gotchas:
#   - NumPy uses radians, not degrees
#   - Sample rate must be ≥ 2× highest frequency (Nyquist)
```

#### 5. Future Improvements Section
```python
# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Add chirp signals (frequency sweeping)
#   [ ] Support I/Q complex signals
#   [ ] Add realistic carrier frequencies
#   [ ] Implement bandlimited signals
#   [ ] Add pulse shaping filters
#   [ ] Support multi-carrier signals
#
# For Deep Space Version:
#   [ ] Doppler shift simulation
#   [ ] Extremely low SNR scenarios
#   [ ] Long propagation delays
```

---

## Project Architecture Deep Dive

### System Block Diagram
```
┌────────────────────────────────────────────────────────────────┐
│                    ORBITER-0 FULL PIPELINE                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────┐         ┌─────────────┐                    │
│  │ Text Message │────────►│ Bits Stream │                    │
│  └──────────────┘         └──────┬──────┘                    │
│                                   │                            │
│                         ┌─────────▼──────────┐                │
│                         │  BPSK Modulation   │                │
│                         │  (+1 / -1 symbols) │                │
│                         └─────────┬──────────┘                │
│                                   │                            │
│                         ┌─────────▼──────────┐                │
│                         │  Signal Generator  │                │
│                         │  (carrier wave)    │                │
│                         └─────────┬──────────┘                │
│                                   │                            │
│  ┌────────────────────────────────▼──────────┐                │
│  │              CHANNEL EFFECTS               │                │
│  ├────────────────────────────────────────────┤                │
│  │  • Gaussian Noise (AWGN)                  │                │
│  │  • Range Loss (distance attenuation)       │                │
│  │  • Atmospheric Absorption                  │                │
│  │  • Fading Events (dropouts, bursts)        │                │
│  └────────────────────┬───────────────────────┘                │
│                       │                                        │
│             ┌─────────▼──────────┐                            │
│             │  BPSK Demodulator  │                            │
│             │  (sign detection)  │                            │
│             └─────────┬──────────┘                            │
│                       │                                        │
│              ┌────────▼─────────┐                             │
│              │   Packetizer     │                             │
│              │ (headers + CRC)  │                             │
│              └────────┬─────────┘                             │
│                       │                                        │
│              ┌────────▼──────────┐                            │
│              │ Error Detection   │                            │
│              │ & Correction      │                            │
│              │ (FEC, checksums)  │                            │
│              └────────┬──────────┘                            │
│                       │                                        │
│              ┌────────▼──────────┐                            │
│              │  Clean Message    │                            │
│              └───────────────────┘                            │
│                       │                                        │
│         ┌─────────────▼─────────────┐                         │
│         │   Mission Archive (DB)    │                         │
│         └───────────────────────────┘                         │
│                       │                                        │
│         ┌─────────────▼─────────────┐                         │
│         │  Streamlit Visualizations │                         │
│         └───────────────────────────┘                         │
└────────────────────────────────────────────────────────────────┘
```

### Directory Structure (Must Match Exactly)
```
orbiter0/
├── streamlit_app/
│   ├── Home.py                          # Mission intro & navigation
│   ├── pages/
│   │   ├── 01_Signals_101.py           # Interactive waveform generator
│   │   ├── 02_Noise_101.py             # Noise visualization & SNR
│   │   ├── 03_Modulation_101.py        # BPSK encoding demo
│   │   ├── 04_Channel_101.py           # Range loss & fading
│   │   ├── 05_Packets_101.py           # Packet structure viewer
│   │   ├── 06_Error_Correction_101.py  # FEC demonstrations
│   │   ├── 07_Downlink_Console.py      # Live decoding interface
│   │   ├── 08_Satellite_Pass_Simulator.py  # Timeline scrubber
│   │   ├── 09_Mission_Archive.py       # SQLite browser
│   │   └── 10_Engineering_Legacy.py    # Reference documentation
│   └── assets/                          # Images, icons, diagrams
├── src/
│   ├── signal/
│   │   ├── __init__.py
│   │   ├── generator.py                 # Waveform creation
│   │   ├── modulation.py                # BPSK encoding/decoding
│   │   └── spectrograms.py              # Time-frequency analysis
│   ├── channel/
│   │   ├── __init__.py
│   │   ├── noise.py                     # AWGN generator
│   │   ├── range_loss.py                # Distance attenuation
│   │   └── fades.py                     # Burst errors, dropouts
│   ├── comms/
│   │   ├── __init__.py
│   │   ├── packetizer.py                # Frame construction
│   │   ├── corruptor.py                 # Bit/byte error injection
│   │   ├── cleaner.py                   # Error detection
│   │   ├── decoder.py                   # Message reconstruction
│   │   ├── anomalies.py                 # Dropout logging
│   │   └── storage.py                   # SQLite persistence
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── timing.py                    # Satellite pass timeline
│   │   ├── math_helpers.py              # SNR, dB conversions
│   │   └── plotting.py                  # Matplotlib wrappers
│   ├── config/
│   │   └── default_params.yaml          # System parameters
│   ├── data/
│   │   └── missions.sqlite              # Persistent storage
│   └── caches/                          # Temporary computation cache
├── tests/                               # Unit tests (add if needed)
├── README.md                            # Main project specification
├── claude.md                            # This file
└── requirements.txt                     # Python dependencies
```

---

## Phase-by-Phase Implementation Guide

### 🔷 PHASE 1: FOUNDATIONS (Steps 1-10)

**Goal:** Set up project structure with teaching-oriented skeleton files

**Key Principles:**
- Create ALL directories and files upfront
- Every file gets a narrative header immediately
- No implementation yet, just structure + documentation
- This phase is about **planning** and **framing**

**Detailed Step Breakdown:**

**Step 1: Create Directory Structure**
```bash
mkdir -p orbiter0/{streamlit_app/pages,streamlit_app/assets,src/{signal,channel,comms,utils,config,data,caches}}
```

**Step 2: Create Empty Module Files**
- All `__init__.py` files in src subdirectories
- All `.py` files in src modules (as skeleton files)
- Purpose: Establish import structure early

**Step 3: Add Header Docstrings**
- Each file gets full narrative header (see style guide above)
- Include ASCII diagram where appropriate
- State learning goals explicitly
- Note simplifications made for beginners

**Step 4: Add ASCII Diagrams**
- `generator.py`: Signal creation flow
- `noise.py`: Noise addition process
- `modulation.py`: BPSK bit encoding
- `packetizer.py`: Packet structure
- `channel/`: Combined effects diagram

**Step 5: Create generator.py Stub**
```python
# Stub with:
# - Full header docstring
# - Function signatures with docstrings
# - Teaching comments explaining WHAT will be implemented
# - No actual implementation (just `pass`)
```

**Steps 6-8: Create Remaining Stubs**
- Same approach for noise.py, modulation.py, packetizer.py
- Each explains the CONCEPT before implementation

**Step 9: Initialize Streamlit Pages**
- Create all 10 page files with:
  - Narrative intro text
  - Placeholder for interactive demo
  - Learning objectives
  - "Coming in Phase X" note

**Step 10: Create default_params.yaml**
```yaml
# ═══════════════════════════════════════════════════════════════
# ORBITER-0 DEFAULT PARAMETERS
# Teaching-oriented configuration with explanatory comments
# ═══════════════════════════════════════════════════════════════

signal:
  # Sample rate (Hz) - how many measurements per second
  # 🎓 NOTE: Must be ≥ 2× highest frequency (Nyquist theorem)
  sample_rate_hz: 44100  # Same as CD quality audio!

  # Carrier frequency (Hz) - the main oscillation
  # 🎓 NOTE: Real satellites use GHz, we use Hz for simplicity
  carrier_freq_hz: 1000

  # ... etc
```

**Phase 1 Validation:**
- [ ] All directories exist
- [ ] All files have narrative headers
- [ ] All major modules have ASCII diagrams
- [ ] No implementation code yet (all stubs)
- [ ] README.md has NOT been modified
- [ ] Can run `python -c "import orbiter0.src.signal.generator"` without errors

---

### 🔷 PHASE 2: SIMPLE SIGNAL CHAIN (Steps 11-20)

**Goal:** Implement core signal generation and basic channel effects

**Key Principles:**
- Start with simplest implementations
- Add visualizations immediately
- Test each component in isolation
- Update Streamlit pages as you go

**Implementation Order (Critical):**

**Step 11: Basic Waveform Generator**
```python
# Implement in generator.py:
# 1. generate_sine() - pure sine wave
# 2. generate_square() - digital-like square wave
# 3. Helper: samples_to_time_axis()
#
# MUST INCLUDE:
# - NumPy array outputs
# - Time axis generation
# - Input validation
# - Simple matplotlib plot function
```

**Step 12: Gaussian Noise Engine**
```python
# Implement in noise.py:
# 1. add_awgn() - Add White Gaussian Noise
# 2. calculate_snr() - Signal-to-Noise Ratio
# 3. snr_to_db() - Convert to decibels
#
# TEACHING FOCUS:
# - Explain what "white" means
# - Visualize noise distribution
# - Show clean vs noisy signals side-by-side
```

**Step 13: Range Loss Model**
```python
# Implement in range_loss.py:
# 1. apply_free_space_loss() - Simple 1/r² attenuation
# 2. distance_to_attenuation_db() - dB calculator
#
# SIMPLIFICATION:
# - Use cartoon physics (no antenna gains)
# - Distance in kilometers (no orbital mechanics)
# - Scalar multiplication only
```

**Step 14: BPSK Modulation**
```python
# Implement in modulation.py:
# 1. bits_to_bpsk_symbols() - Convert [0,1] to [-1,+1]
# 2. bpsk_symbols_to_signal() - Multiply by carrier
# 3. Visualize phase flips
#
# TEACHING:
# - Why phase shift keying?
# - Show bit transitions clearly
# - Explain symbol vs bit
```

**Step 15: Text to Bits Converter**
```python
# Add to modulation.py:
# 1. text_to_bits() - UTF-8 encoding
# 2. bits_to_text() - Decoding
# 3. Handle errors gracefully
#
# Make it visual:
# - Print bit representations
# - Show ASCII values
```

**Step 16: Mini Spectrogram**
```python
# Implement in spectrograms.py:
# 1. generate_spectrogram() - Time-frequency plot
# 2. Use matplotlib specgram()
# 3. Teaching-oriented axis labels
#
# PURPOSE:
# - Show frequency content over time
# - Visualize modulation effects
```

**Step 17: Unified Channel Model**
```python
# Create new file: channel/channel_model.py
# 1. Combine modulation + noise + range loss
# 2. End-to-end signal degradation
# 3. Configurable parameters
#
# This ties Steps 11-16 together!
```

**Step 18: BPSK Demodulator**
```python
# Add to modulation.py:
# 1. demodulate_bpsk() - Detect sign of samples
# 2. symbols_to_bits() - Convert [-1,+1] to [0,1]
# 3. Handle threshold detection
#
# TEACHING:
# - Explain decision boundaries
# - Show errors from noise
```

**Step 19: Bit Error Metrics**
```python
# Add to utils/math_helpers.py:
# 1. calculate_ber() - Bit Error Rate
# 2. count_bit_errors() - Compare sent vs received
# 3. Teaching-oriented error reporting
```

**Step 20: Update Streamlit Pages**
- Update `01_Signals_101.py` with waveform demos
- Update `02_Noise_101.py` with SNR sliders
- Update `03_Modulation_101.py` with BPSK visualizer
- All should be interactive with st.slider()

**Phase 2 Validation:**
- [ ] Can generate sine and square waves
- [ ] Can add noise at specified SNR
- [ ] Can modulate text message to BPSK
- [ ] Can demodulate and recover text
- [ ] Can calculate BER
- [ ] Streamlit pages 1-3 are interactive
- [ ] All plots have clear labels and titles

---

### 🔷 PHASE 3: PACKETS, FADING, & REAL-WORLD CONSTRAINTS (Steps 21-30)

**Goal:** Add packet structure, error detection, and realistic impairments

**Key Implementations:**

**Step 21: Packetizer with Headers**
```python
# Implement in packetizer.py:
#
# Packet Structure:
# ┌──────────────────────────────────────────┐
# │ PREAMBLE (sync pattern)  │ 4 bytes       │
# ├──────────────────────────────────────────┤
# │ HEADER                   │ 8 bytes       │
# │   - Packet ID            │ (2 bytes)     │
# │   - Length               │ (2 bytes)     │
# │   - Timestamp            │ (4 bytes)     │
# ├──────────────────────────────────────────┤
# │ PAYLOAD                  │ N bytes       │
# ├──────────────────────────────────────────┤
# │ CRC-16 Checksum          │ 2 bytes       │
# └──────────────────────────────────────────┘
#
# Functions:
# 1. create_packet(payload: bytes) -> bytes
# 2. parse_packet(packet: bytes) -> dict
# 3. validate_packet(packet: bytes) -> bool
```

**Step 22: Corruption Functions**
```python
# Implement in corruptor.py:
# 1. flip_random_bits() - Bit error injection
# 2. drop_bytes() - Simulate packet loss
# 3. burst_errors() - Clustered corruption
#
# TEACHING:
# - Show before/after hex dumps
# - Visualize error patterns
```

**Step 23: Fade Events**
```python
# Implement in fades.py:
# 1. FadeEvent class (start_time, duration, severity)
# 2. apply_fade_to_signal() - Temporary attenuation
# 3. generate_random_fades() - Realistic patterns
#
# TYPES:
# - Atmospheric scintillation
# - Brief obstructions
# - Noise bursts
```

**Step 24: CRC Validator**
```python
# Add to cleaner.py:
# 1. compute_crc16() - Checksum calculation
# 2. verify_crc() - Validation function
# 3. Teaching notes on error detection limits
#
# Use standard CRC-16-CCITT
```

**Step 25: Forward Error Correction**
```python
# Implement in decoder.py:
# 1. simple_parity_encode() - Add parity bits
# 2. simple_parity_decode() - Detect single errors
# 3. Optional: Hamming(7,4) for correction
#
# TEACHING:
# - Difference between detection and correction
# - Trade-off: bandwidth vs reliability
```

**Step 26: Atmospheric Absorption**
```python
# Add to range_loss.py:
# 1. apply_atmospheric_loss() - Frequency-dependent
# 2. Simple scalar for beginner version
# 3. Teaching notes on real atmospheric effects
```

**Step 27: Satellite Pass Timeline**
```python
# Implement in utils/timing.py:
# 1. SatellitePass class (start, duration, max_elevation)
# 2. signal_strength_curve() - Strength over time
# 3. Simplified orbital mechanics
#
# Model:
#       Signal Strength
#            ^
#            |     /\
#            |    /  \
#            |   /    \
#            |__/______\___> Time
#           Rise  Peak  Set
```

**Step 28: Packet Visualization Page**
```python
# Update 05_Packets_101.py:
# - Show packet structure diagram
# - Hex dump viewer
# - Corruption simulator
# - CRC validation demo
```

**Step 29: Mission Archival**
```python
# Implement in storage.py:
# 1. init_database() - Create SQLite schema
# 2. save_mission() - Store pass data
# 3. query_missions() - Retrieve history
#
# Schema:
# CREATE TABLE missions (
#   id INTEGER PRIMARY KEY,
#   timestamp REAL,
#   message_sent TEXT,
#   message_received TEXT,
#   ber REAL,
#   snr_db REAL,
#   packets_total INTEGER,
#   packets_corrupted INTEGER,
#   metadata JSON
# );
```

**Step 30: Packet Debugging Helpers**
```python
# Add to utils/:
# 1. hexdump() - Pretty-print bytes
# 2. diff_packets() - Show differences
# 3. packet_inspector() - Full breakdown
```

**Phase 3 Validation:**
- [ ] Can create and parse packets
- [ ] CRC validation works
- [ ] Can inject and detect errors
- [ ] FEC can correct single-bit errors
- [ ] Satellite pass timeline generates curves
- [ ] Missions saved to SQLite
- [ ] Page 5 shows packet structure interactively

---

### 🔷 PHASE 4: STREAMLIT LEARNING CONSOLE (Steps 31-40)

**Goal:** Create polished, interactive learning experiences

**Streamlit Best Practices for This Project:**

```python
# Standard page structure:
import streamlit as st
import sys
sys.path.append('../../')  # Adjust as needed
from src.signal import generator

st.set_page_config(page_title="Signals 101", page_icon="📡", layout="wide")

# ═══════════════════════════════════════════════════════════════
st.title("📡 Signals 101: The Foundation of Communication")
st.markdown("""
### Welcome, Cadet! 🚀

Before our satellite can talk to Earth, it needs to create **signals**.
A signal is just a pattern of energy changing over time.

Think of it like:
- 🎵 Sound waves when you talk
- 🌊 Ripples on a pond
- 💡 A flashlight blinking a message

In this chapter, you'll learn to **generate** and **visualize** signals.
""")

# Interactive demo section
st.header("🎛️ Signal Generator")

col1, col2 = st.columns(2)

with col1:
    freq = st.slider("Frequency (Hz)", 1, 100, 10)
    amp = st.slider("Amplitude", 0.1, 2.0, 1.0)
    duration = st.slider("Duration (seconds)", 0.1, 2.0, 1.0)

with col2:
    wave_type = st.selectbox("Wave Type", ["Sine", "Square"])

# Generate and plot
if wave_type == "Sine":
    t, sig = generator.generate_sine(freq, amp, duration, 1000)
else:
    t, sig = generator.generate_square(freq, amp, duration, 1000)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, sig, linewidth=2)
ax.set_xlabel("Time (seconds)", fontsize=12)
ax.set_ylabel("Amplitude", fontsize=12)
ax.set_title(f"{wave_type} Wave: {freq} Hz", fontsize=14)
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# Teaching callout
st.info("""
🎓 **What's Happening:**
- **Frequency** = how many cycles per second (measured in Hertz)
- **Amplitude** = how strong the signal is
- **Time** = when each sample was measured

Try changing the sliders and watch the wave transform!
""")
```

**Steps 31-40 Implementation:**

**Step 31: Home Page** (`Home.py`)
- Mission briefing narrative
- System architecture diagram
- Navigation to all chapters
- "Quick Start" tutorial

**Step 32: Signals 101** (done above)

**Step 33: Noise 101** (`02_Noise_101.py`)
- Clean signal generator
- SNR slider (0-30 dB)
- Side-by-side clean/noisy comparison
- Histogram of noise distribution
- Teaching: "Noise is random interference"

**Step 34: Modulation 101** (`03_Modulation_101.py`)
- Text input box
- Convert to bits (show binary)
- BPSK encoding visualization
- Animated phase flips
- Decode back to text

**Step 35: Channel 101** (`04_Channel_101.py`)
- Distance slider
- Show range loss calculation
- Add fade events on timeline
- Combined effects demo

**Step 36: Packets 101** (already in Step 28, polish it)

**Step 37: Error Correction 101** (`06_Error_Correction_101.py`)
- Compare: No FEC vs Parity vs Hamming
- Error injection slider
- Show correction in action
- BER comparison charts

**Step 38: Satellite Pass Simulator** (`08_Satellite_Pass_Simulator.py`)
- Timeline scrubber
- Signal strength curve
- Elevation angle diagram
- Packet reception overlay
- "Play" button for animation

**Step 39: Downlink Console** (`07_Downlink_Console.py`)
- Live simulation mode
- Real-time bit decoding
- Scrolling packet log
- Statistics dashboard (BER, SNR, packet loss)

**Step 40: Mission Archive** (`09_Mission_Archive.py`)
- SQLite browser
- Filter by date/SNR/BER
- Detailed mission view
- Export to CSV

**Phase 4 Validation:**
- [ ] All 10 pages are functional
- [ ] Navigation works from Home
- [ ] Each page teaches one concept
- [ ] Interactive elements respond smoothly
- [ ] Plots have clear labels
- [ ] Teaching callouts explain concepts

---

### 🔷 PHASE 5: FULL INTEGRATION & POLISH (Steps 41-50)

**Goal:** Complete end-to-end pipeline and add professional touches

**Step 41: Orchestrated Runtime**
```python
# Create src/runtime/pipeline.py
#
# Full simulation flow:
# 1. Take text message
# 2. Convert to packets
# 3. Modulate to BPSK
# 4. Apply channel effects
# 5. Demodulate
# 6. Validate packets
# 7. Decode message
# 8. Log anomalies
# 9. Save to database
# 10. Return results dictionary
```

**Step 42: Async Downlink Loop**
```python
# Add async version for "live" mode:
import asyncio

async def simulate_live_downlink(duration_seconds):
    """
    Simulates real-time satellite communication.
    Yields packet data as it "arrives".
    """
    # Teaching: Intro to async programming
    # Useful for: Real-time UIs, concurrent tasks
```

**Step 43: Streamlit Session State**
```python
# Add to utils/streamlit_helpers.py
#
# Shared state across pages:
# - Current mission parameters
# - Last simulation results
# - User preferences
#
# Use st.session_state properly
```

**Step 44: Global Plotting Helpers**
```python
# Enhance utils/plotting.py:
# 1. plot_signal() - Standardized time-domain
# 2. plot_spectrum() - Frequency domain
# 3. plot_constellation() - BPSK scatter
# 4. plot_ber_vs_snr() - Performance curve
# 5. plot_timeline() - Satellite pass
#
# All with teaching-oriented annotations
```

**Step 45: Code Snippet Overlays**
```python
# Add to Streamlit pages:
# - Expandable "Show Code" sections
# - Explain the math behind each demo
# - Copy-pasteable examples
#
# Example:
with st.expander("🔍 Show the Code"):
    st.code('''
def add_noise(signal, snr_db):
    """Add Gaussian noise at specified SNR."""
    signal_power = np.mean(signal**2)
    noise_power = signal_power / (10**(snr_db/10))
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal))
    return signal + noise
    ''', language='python')
```

**Step 46: Tune Noise & Fading**
- Adjust default parameters for intuitive behavior
- Ensure demos are neither too easy nor too hard
- Target ~10% BER at moderate SNR
- Make fade events visible but not overwhelming

**Step 47: Import/Export Tools**
```python
# Add to utils/:
# 1. export_mission_json() - Save configuration
# 2. import_mission_json() - Load configuration
# 3. Share scenarios between users
```

**Step 48: Engineering Legacy Page** (`10_Engineering_Legacy.py`)
- Full system reference
- All equations documented
- Parameter tables
- Troubleshooting guide
- Links to further reading

**Step 49: Debugging Suite**
```python
# Create tests/self_test.py:
# 1. Test all signal functions
# 2. Validate packet creation
# 3. Check CRC implementation
# 4. Verify FEC correctness
# 5. Test database operations
#
# Run with: python tests/self_test.py
```

**Step 50: Future Extensions Guide**
```markdown
# Add FUTURE.md:
#
# Next Steps for ORBITER-1 (Intermediate):
# - Real orbital mechanics (Keplerian elements)
# - Multiple ground stations
# - QPSK modulation
# - Actual satellite frequencies (GHz)
# - Antenna gain patterns
#
# ORBITER-DEEP-SPACE (Advanced):
# - Doppler shift tracking
# - Reed-Solomon codes
# - Convolutional codes
# - Turbo codes
# - 10M km distances
# - Hour-long propagation delays
```

**Phase 5 Validation:**
- [ ] End-to-end pipeline works
- [ ] Can run full simulation from Home page
- [ ] Session state persists across pages
- [ ] All plots are publication-quality
- [ ] Code snippets are accurate
- [ ] Self-tests pass
- [ ] Documentation is complete
- [ ] Project is ready for students

---

## Technical Concepts Reference

### Signal Processing Fundamentals

**1. Sampling & Nyquist Theorem**
```python
# Sample rate must be ≥ 2× highest frequency
#
# Example:
# - Highest frequency: 1000 Hz
# - Minimum sample rate: 2000 Hz
# - Safe sample rate: 4000 Hz (2× margin)
#
# Why: Prevents aliasing (frequency ambiguity)
```

**2. Signal-to-Noise Ratio (SNR)**
```python
# SNR_dB = 10 * log10(P_signal / P_noise)
#
# Typical values:
# - 30 dB: Excellent (1000:1 power ratio)
# - 20 dB: Good (100:1)
# - 10 dB: Marginal (10:1)
# - 0 dB: Unusable (equal power)
```

**3. BPSK Modulation**
```
Bit → Symbol Mapping:
  0 → -1 (phase = 180°)
  1 → +1 (phase = 0°)

Demodulation (with noise):
  Sample > 0 → Bit = 1
  Sample < 0 → Bit = 0

  Errors occur when noise flips the sign!
```

**4. Bit Error Rate (BER)**
```python
# BER = (# of bit errors) / (# of total bits)
#
# Typical for BPSK in AWGN:
# - SNR = 10 dB → BER ≈ 10⁻⁵ (very few errors)
# - SNR = 5 dB → BER ≈ 10⁻² (1% error rate)
# - SNR = 0 dB → BER ≈ 0.1 (10% error rate)
```

**5. Range Loss (Free Space Path Loss)**
```python
# FSPL_dB = 20*log10(distance) + 20*log10(frequency) - 147.55
#
# Simplified for teaching:
# Attenuation ≈ 1 / (distance_km² )
#
# Example:
# - 1000 km → 1/1,000,000 = -60 dB
```

### Error Detection & Correction

**CRC-16 (Cyclic Redundancy Check)**
- Detects: All single-bit errors, all double-bit errors, burst errors ≤16 bits
- Does NOT correct (only detects)
- 16-bit checksum (2 bytes)

**Parity Bit**
- Simplest error detection
- Detects: Single-bit errors (and odd numbers of errors)
- Cannot correct

**Hamming Code (7,4)**
- 4 data bits → 7 total bits (3 parity bits)
- Can correct: 1-bit errors
- Can detect: 2-bit errors
- Efficiency: 4/7 = 57% (overhead = 43%)

---

## Common Pitfalls & How to Avoid Them

### ❌ PITFALL 1: Skipping Ahead
**Symptom:** "I'll just implement the whole signal chain at once"
**Why It Fails:** Impossible to debug when everything breaks
**Solution:** Follow phases sequentially. Test each component before moving on.

### ❌ PITFALL 2: Production-Quality Code
**Symptom:** "Let me optimize this with Cython and vectorization"
**Why It Fails:** Loses educational clarity
**Solution:** Prioritize readability. Use simple loops if they're clearer. Add "Performance Note" comments suggesting optimizations.

### ❌ PITFALL 3: Minimal Comments
**Symptom:** "The code is self-documenting"
**Why It Fails:** Students need guidance, not puzzles
**Solution:** Over-comment. Explain WHY, not just WHAT. Add teaching callouts.

### ❌ PITFALL 4: Missing Visualizations
**Symptom:** "I'll add plots later"
**Why It Fails:** Visualizations ARE the learning tool
**Solution:** Add a plot for every new concept immediately.

### ❌ PITFALL 5: Complex Math Without Explanation
**Symptom:** `signal = A * np.exp(2j * np.pi * f * t)`
**Why It Fails:** Students get lost in notation
**Solution:** Break complex equations into steps with intermediate variables and comments.

### ❌ PITFALL 6: Modifying README.md
**Symptom:** "Let me update the README with my changes"
**Why It Fails:** README is the spec, not a log
**Solution:** README is frozen after Phase 1. Use CHANGELOG.md or comments instead.

### ❌ PITFALL 7: Inconsistent Naming
**Symptom:** Mixed styles like `sample_rate`, `sampleRate`, `SR`
**Why It Fails:** Confuses learners
**Solution:** Use `snake_case` for everything. Full descriptive names, not abbreviations.

### ❌ PITFALL 8: No Units in Variable Names
**Symptom:** `frequency = 1000` (Hz? MHz? GHz?)
**Why It Fails:** Leads to unit conversion bugs
**Solution:** Always suffix units: `frequency_hz`, `distance_km`, `duration_sec`

---

## Testing Strategy

### Unit Testing (Phase 5, Step 49)
```python
# tests/test_signal_generator.py
import numpy as np
from src.signal.generator import generate_sine

def test_sine_amplitude():
    """Verify sine wave reaches expected amplitude."""
    _, signal = generate_sine(
        frequency_hz=10,
        amplitude=2.0,
        duration_sec=1.0,
        sample_rate_hz=1000
    )
    assert np.abs(signal.max() - 2.0) < 0.01  # Allow floating point error
    assert np.abs(signal.min() + 2.0) < 0.01

def test_sine_frequency():
    """Verify sine wave has correct frequency."""
    t, signal = generate_sine(10, 1.0, 1.0, 1000)

    # Count zero crossings (should be 2× frequency)
    zero_crossings = np.sum(np.diff(np.sign(signal)) != 0)
    expected = 2 * 10  # 20 crossings for 10 Hz over 1 second

    assert abs(zero_crossings - expected) <= 2  # Allow ±1 crossing
```

### Integration Testing
```python
# tests/test_pipeline.py
def test_end_to_end_lossless():
    """Test full pipeline with no noise or loss."""
    message = "Hello from orbit!"

    # Should recover message exactly in ideal conditions
    result = pipeline.simulate_transmission(
        message=message,
        snr_db=float('inf'),  # No noise
        distance_km=0,  # No range loss
        fades=[]  # No fading
    )

    assert result['message_received'] == message
    assert result['ber'] == 0.0
```

### Visual Testing (Manual)
- Run each Streamlit page
- Verify plots render correctly
- Test all sliders and inputs
- Check for errors in console

---

## Dependencies & Setup

### requirements.txt
```txt
# Core scientific stack
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0

# Web interface
streamlit>=1.28.0

# Data persistence
sqlite3  # Built-in to Python

# Error correction (if using advanced FEC)
# reedsolo>=1.7.0  # Uncomment for Reed-Solomon in ORBITER-1

# Development tools (optional)
pytest>=7.4.0
black>=23.0.0
pylint>=2.17.0
```

### Setup Commands
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python -c "import numpy, matplotlib, streamlit; print('OK')"

# Run application
streamlit run orbiter0/streamlit_app/Home.py

# Run tests (Phase 5)
pytest tests/ -v
```

---

## Git Workflow for This Project

### Branch Strategy
- **Main branch:** `main` (or as specified in git setup)
- **Development branch:** As specified in instructions (e.g., `claude/create-claude-docs-...`)
- Work on development branch exclusively
- Only push to specified branch

### Commit Message Style
```
Phase X, Step Y: Brief description

- Detailed change 1
- Detailed change 2
- Detailed change 3

Teaching focus: [what concept this teaches]
```

**Example:**
```
Phase 2, Step 11: Implement basic waveform generator

- Add generate_sine() with full docstrings
- Add generate_square() with teaching comments
- Create plotting helper for time-domain signals
- Add ASCII diagram to generator.py header

Teaching focus: Signal representation as time-series arrays
```

### When to Commit
- ✅ After completing each step
- ✅ After adding tests
- ✅ After significant documentation additions
- ❌ In the middle of a step
- ❌ With broken code

---

## Streamlit-Specific Tips

### Performance
```python
# Cache expensive computations
@st.cache_data
def generate_large_signal(duration_sec):
    """Cached to avoid regenerating on every widget change."""
    return generate_sine(1000, 1.0, duration_sec, 44100)
```

### Layout
```python
# Use columns for side-by-side content
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig_before)
with col2:
    st.pyplot(fig_after)

# Use expanders for optional content
with st.expander("Advanced Options"):
    noise_type = st.selectbox(...)
```

### State Management
```python
# Initialize session state
if 'mission_count' not in st.session_state:
    st.session_state.mission_count = 0

# Increment on button click
if st.button("Run Mission"):
    st.session_state.mission_count += 1
```

### Styling
```python
# Use markdown for rich text
st.markdown("""
### 🎯 Learning Objective
By the end of this chapter, you'll understand:
- ✅ What a signal is
- ✅ How to generate waveforms
- ✅ How to visualize time-domain data
""")

# Use status indicators
st.success("✅ Packet decoded successfully!")
st.warning("⚠️ High bit error rate detected")
st.error("❌ CRC validation failed")
st.info("ℹ️ Tip: Try lowering the noise level")
```

---

## Final Checklist

Before considering the project complete:

### Code Quality
- [ ] All files have narrative headers
- [ ] All major functions have ASCII diagrams
- [ ] Every concept has a visualization
- [ ] No function exceeds 50 lines without good reason
- [ ] Variable names are descriptive (no single letters except loop indices)
- [ ] Units are specified in variable names

### Teaching Quality
- [ ] Each Streamlit page teaches one clear concept
- [ ] Math is explained, not just implemented
- [ ] Interactive demos work smoothly
- [ ] Teaching callouts are present throughout
- [ ] Debugging notes help troubleshoot common issues

### Functionality
- [ ] All 10 Streamlit pages are complete
- [ ] End-to-end pipeline works
- [ ] Database persistence works
- [ ] Error detection and correction work
- [ ] Satellite pass simulation works

### Documentation
- [ ] README.md unchanged after Phase 1
- [ ] This claude.md is comprehensive
- [ ] Code comments are abundant
- [ ] Future extensions are documented

### Polish
- [ ] Plots have proper labels and titles
- [ ] No console errors or warnings
- [ ] Streamlit pages load quickly
- [ ] Navigation is intuitive
- [ ] Project feels cohesive

---

## Quick Reference Commands

```bash
# Start fresh
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run app
streamlit run orbiter0/streamlit_app/Home.py

# Run specific page directly
streamlit run orbiter0/streamlit_app/pages/01_Signals_101.py

# Run tests
pytest tests/ -v

# Check code style
black orbiter0/ --check
pylint orbiter0/src/

# Create database
python -c "from orbiter0.src.comms.storage import init_database; init_database()"

# Interactive Python with imports
python
>>> from orbiter0.src.signal.generator import generate_sine
>>> t, s = generate_sine(10, 1.0, 1.0, 1000)
>>> import matplotlib.pyplot as plt
>>> plt.plot(t, s); plt.show()
```

---

## Support Resources

### Python Concepts Needed
- NumPy arrays and vectorization
- Matplotlib plotting
- Basic async/await (Phase 5)
- SQLite database operations
- File I/O and YAML parsing

### Domain Concepts Needed
- Basic trigonometry (sine, cosine)
- Decibel calculations
- Binary representation
- Checksum algorithms
- Basic probability (Gaussian distribution)

### Learning Resources
- NumPy tutorial: https://numpy.org/doc/stable/user/quickstart.html
- Matplotlib gallery: https://matplotlib.org/stable/gallery/
- Streamlit docs: https://docs.streamlit.io/
- Digital communications intro: (search "BPSK tutorial")

---

## Philosophy Reminder

This is a **teaching project**. Every decision should ask:

> "Will this help a beginner understand wireless communications better?"

Not:

> "Is this the most efficient implementation?"

**Optimize for learning, not performance.**

**Prioritize clarity, not brevity.**

**Show, don't just tell.**

Good luck, and may your signals be strong and your noise be gentle! 📡🛰️

---

**END OF CLAUDE.MD**
