"""
═══════════════════════════════════════════════════════════════════
CHAPTER 2: NOISE 101
Understanding interference and signal degradation
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Noise 101", page_icon="📻", layout="wide")

st.title("📻 Chapter 2: Noise 101")

st.markdown("""
---

### The Imperfect Universe 🌌

Signals traveling through space don't stay perfect. They pick up **NOISE** -
random interference that corrupts the signal.

**What is noise?**
Think of noise like:
- 📺 Static on an old TV
- 📻 Hiss on a radio between stations
- ☎️ Background crackle on a bad phone call

**Where does noise come from?**
- ☀️ Thermal radiation from the sun
- 🌌 Cosmic background radiation
- ⚡ Electronics in the receiver
- 🌧️ Atmospheric interference

---

### 🎯 Learning Objectives

- ✅ What noise is and its sources
- ✅ Understanding AWGN (Additive White Gaussian Noise)
- ✅ Signal-to-Noise Ratio (SNR)
- ✅ How noise causes bit errors
- ✅ Converting to/from decibels (dB)

---
""")

# ═══════════════════════════════════════════════════════════════════
# INTERACTIVE DEMO
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Interactive Noise Simulator")

st.markdown("""
Add noise to a signal and see how SNR affects signal quality!
""")

# Add path to import our modules
import sys
sys.path.append('../../src')

from signals.generator import generate_sine
from channel.noise import add_awgn, calculate_snr_db
import matplotlib.pyplot as plt
import numpy as np

# Controls
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Signal Settings")
    freq = st.slider("Signal Frequency (Hz)", 5, 30, 10)
    amplitude = 1.0  # Fixed for clearer noise comparison

with col2:
    st.subheader("Noise Settings")
    snr_db = st.slider(
        "SNR (dB)",
        min_value=0,
        max_value=30,
        value=15,
        help="Higher SNR = less noise, Lower SNR = more noise"
    )

# Generate clean signal
duration = 1.0
sample_rate = 1000
time_axis, clean_signal = generate_sine(freq, amplitude, duration, sample_rate)

# Add noise
noisy_signal, noise = add_awgn(clean_signal, snr_db)

# Calculate actual SNR
actual_snr = calculate_snr_db(clean_signal, noise)

# Create comparison plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Plot 1: Clean vs Noisy Signal
ax1.plot(time_axis, clean_signal, linewidth=2, color='green', label='Clean Signal', alpha=0.7)
ax1.plot(time_axis, noisy_signal, linewidth=1, color='red', label='Noisy Signal', alpha=0.8)
ax1.set_xlabel('Time (seconds)', fontsize=11)
ax1.set_ylabel('Amplitude', fontsize=11)
ax1.set_title(f'Signal Comparison: SNR = {snr_db} dB', fontsize=13, fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim([0, 0.5])  # Show first 0.5 seconds for clarity

# Plot 2: Noise Distribution (Histogram)
ax2.hist(noise, bins=50, color='orange', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Noise Value', fontsize=11)
ax2.set_ylabel('Frequency', fontsize=11)
ax2.set_title('Noise Distribution (Should be Gaussian/Bell Curve)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--')

# Add Gaussian overlay for teaching
noise_std = np.std(noise)
x = np.linspace(noise.min(), noise.max(), 100)
gaussian = (1/(noise_std * np.sqrt(2*np.pi))) * np.exp(-0.5*((x/noise_std)**2))
gaussian_scaled = gaussian * len(noise) * (noise.max() - noise.min()) / 50  # Scale to histogram
ax2_twin = ax2.twinx()
ax2_twin.plot(x, gaussian_scaled, 'r-', linewidth=2, label='Theoretical Gaussian')
ax2_twin.set_ylabel('Theoretical Density', fontsize=11)
ax2_twin.legend(loc='upper right')

plt.tight_layout()
st.pyplot(fig)
plt.close()

# Teaching insights
st.markdown(f"""
---

### 🎓 What You're Seeing

**SNR = {snr_db} dB** (Target) | **Actual SNR = {actual_snr:.2f} dB**

**Signal Quality:**
""")

if snr_db >= 25:
    st.success("**Excellent!** Signal is very clean - noise barely visible")
elif snr_db >= 15:
    st.info("**Good:** Signal visible with moderate noise")
elif snr_db >= 10:
    st.warning("**Marginal:** Signal partially obscured by noise")
else:
    st.error("**Poor:** Signal heavily corrupted - hard to detect")

st.markdown(f"""
**Understanding the Plots:**

**Top Plot:** Shows clean signal (green) overlaid with noisy signal (red)
- At high SNR, the curves match closely
- At low SNR, the noisy signal looks very different

**Bottom Plot:** Shows the distribution of noise values
- Should form a bell curve (Gaussian distribution)
- Width of the curve = noise strength
- This is the \"G\" in AWGN (Additive White Gaussian Noise)

**Try This:**
1. Set SNR to 30 dB → noise almost invisible
2. Set SNR to 5 dB → signal buried in noise
3. Watch the noise histogram stay Gaussian at all SNR levels

---

### 📊 Understanding SNR

**SNR (Signal-to-Noise Ratio)** measures signal quality:

- **30 dB:** Excellent (signal 1000× stronger than noise)
- **20 dB:** Good (100× stronger)
- **10 dB:** Marginal (10× stronger)
- **0 dB:** Unusable (equal power)

---

**➡️ Next:** Learn how we encode bits into signals in **Modulation 101**

""")

st.success("✅ **Interactive Demo Active:** Adjust SNR to see signal degradation in real-time!")

st.divider()
st.caption("Chapter 2: Noise 101 | Phase 4: Fully Interactive Learning Console")
