"""
═══════════════════════════════════════════════════════════════════
CHAPTER 1: SIGNALS 101
The foundation of all communication
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Signals 101", page_icon="📡", layout="wide")

# ═══════════════════════════════════════════════════════════════════
# CHAPTER INTRODUCTION
# ═══════════════════════════════════════════════════════════════════

st.title("📡 Chapter 1: Signals 101")

st.markdown("""
---

### Welcome, Cadet! 🚀

Before our satellite can talk to Earth, it needs to create **SIGNALS**.

**What is a signal?**
A signal is just a pattern of energy changing over time. Think of it like:
- 🎵 Sound waves when you talk
- 🌊 Ripples spreading across a pond
- 💡 A flashlight blinking a message in Morse code

In wireless communications, signals are **electromagnetic waves** that
carry information through space.

---

### 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- ✅ What a signal is (samples over time)
- ✅ How frequency and amplitude work
- ✅ The difference between sine and square waves
- ✅ How to visualize waveforms
- ✅ The concept of sampling rate

---

### 📚 Key Concepts

**Amplitude:** How "tall" the wave is (signal strength)

**Frequency:** How many cycles happen per second (measured in Hertz)
- 1 Hz = 1 cycle per second
- 1000 Hz = 1000 cycles per second

**Sample Rate:** How many measurements we take per second
- Must be at least 2× the highest frequency (Nyquist theorem)

**Waveforms:**
- **Sine wave:** Smooth, fundamental oscillation
- **Square wave:** Digital-like, abrupt transitions

---
""")

# ═══════════════════════════════════════════════════════════════════
# INTERACTIVE DEMO
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Interactive Signal Generator")

st.markdown("""
Play with the controls below to generate different waveforms!
Watch how changing parameters affects the signal.
""")

# Add path to import our modules
import sys
sys.path.append('../../src')

from signal.generator import generate_sine, generate_square
import matplotlib.pyplot as plt
import numpy as np

# Create two columns for controls
col1, col2 = st.columns(2)

with col1:
    st.subheader("Signal Parameters")
    frequency_hz = st.slider(
        "Frequency (Hz)",
        min_value=1,
        max_value=50,
        value=10,
        help="How many cycles per second"
    )

    amplitude = st.slider(
        "Amplitude",
        min_value=0.1,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Peak signal strength"
    )

    duration_sec = st.slider(
        "Duration (seconds)",
        min_value=0.1,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="How long to generate"
    )

with col2:
    st.subheader("Wave Type")
    wave_type = st.radio(
        "Choose waveform:",
        ["Sine Wave", "Square Wave"],
        help="Sine = smooth, Square = digital-like"
    )

    st.info(f"""
    **Current Settings:**
    - {frequency_hz} cycles per second
    - Amplitude of {amplitude}
    - {duration_sec} seconds duration
    """)

# Generate signal based on selection
sample_rate_hz = 1000  # Fixed sample rate for visualization

if wave_type == "Sine Wave":
    time_axis, signal = generate_sine(frequency_hz, amplitude, duration_sec, sample_rate_hz)
    wave_description = "smooth and continuous"
else:
    time_axis, signal = generate_square(frequency_hz, amplitude, duration_sec, sample_rate_hz)
    wave_description = "abrupt and digital-like"

# Plot the signal
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(time_axis, signal, linewidth=2, color='#2E86AB')
ax.set_xlabel('Time (seconds)', fontsize=12)
ax.set_ylabel('Amplitude', fontsize=12)
ax.set_title(f'{wave_type}: {frequency_hz} Hz, Amplitude {amplitude}', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)

# Highlight one cycle for teaching
if time_axis[-1] > 0:
    cycle_duration = 1.0 / frequency_hz
    if cycle_duration < time_axis[-1]:
        ax.axvspan(0, cycle_duration, alpha=0.1, color='green')
        ax.text(cycle_duration/2, amplitude*1.2, '← One Cycle →',
                ha='center', fontsize=10, color='green', fontweight='bold')

plt.tight_layout()
st.pyplot(fig)
plt.close()

# Teaching insights
st.markdown(f"""
---

### 🎓 What You're Seeing

This is a **{wave_type.lower()}** - it's {wave_description}.

**Key Observations:**
- The signal oscillates **{frequency_hz} times per second**
- Peak height is **{amplitude}** (amplitude)
- One complete cycle takes **{1/frequency_hz:.3f} seconds**
- Sample rate: **{sample_rate_hz} samples/second** (enough to capture shape)

**Try This:**
1. Increase frequency → waves get closer together
2. Increase amplitude → waves get taller
3. Switch wave types → see the difference in shape

---

### 💡 Why This Matters

Understanding signals is the **foundation** of everything in wireless communications:
- Without signals, there's no way to transmit information
- Every other concept (noise, modulation, errors) builds on this
- Real satellite systems use complex signals, but the basics are the same

---

### 🎓 Try This Next

Once Phase 2 is implemented, experiment with:
1. Generate a 10 Hz sine wave - count the cycles
2. Increase frequency to 50 Hz - notice how it oscillates faster
3. Switch to square wave - see the digital-like transitions
4. Lower the sample rate - see what happens (spoiler: aliasing!)

---

### ➡️ Next Chapter

When you're ready, move on to **Noise 101** to see how signals
get corrupted during transmission.

---

""")

st.success("✅ **Phase 2 Complete:** Interactive signal generator is now operational!")

# Footer
st.divider()
st.caption("Chapter 1: Signals 101 | Phase 2 Complete - Interactive Demo Active")
