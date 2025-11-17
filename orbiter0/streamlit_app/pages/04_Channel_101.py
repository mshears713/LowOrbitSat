"""
═══════════════════════════════════════════════════════════════════
CHAPTER 4: CHANNEL 101
How signals degrade over distance and through atmosphere
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Channel 101", page_icon="🛰️", layout="wide")

st.title("🛰️ Chapter 4: Channel 101")

st.markdown("""
---

### The Journey Through Space 🌌

Signals don't magically teleport from satellite to ground station.
They travel through the **CHANNEL** - space and atmosphere - where
they get weaker and corrupted.

**Channel Effects:**
- 📏 **Range Loss:** Signal spreads out (inverse-square law)
- 🌫️ **Atmospheric Absorption:** Air isn't transparent to radio
- ⚡ **Fading:** Temporary dropouts from obstructions

---

### 🎯 Learning Objectives

- ✅ Free-space path loss (1/distance²)
- ✅ How distance affects signal strength
- ✅ Atmospheric absorption basics
- ✅ Fading events and burst errors
- ✅ Combined channel effects

---
""")

# Add path to import our modules
import sys
sys.path.append('../../src')

from signal.generator import generate_sine
from channel.range_loss import apply_free_space_loss, distance_to_attenuation_db, apply_atmospheric_loss
from channel.fades import generate_random_fades, apply_fades_to_signal, FadeEvent
from channel.noise import add_awgn
import matplotlib.pyplot as plt
import numpy as np

# ═══════════════════════════════════════════════════════════════════
# DEMO 1: RANGE LOSS
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Demo 1: Range Loss (Inverse-Square Law)")

st.markdown("""
As the satellite moves farther away, the signal spreads out over a larger area.
This causes **path loss** - the signal gets weaker with distance.

**Formula:** Signal strength ∝ 1/distance²
""")

col1, col2 = st.columns([2, 1])

with col1:
    distance_km = st.slider(
        "Satellite Distance (km)",
        min_value=100,
        max_value=2000,
        value=500,
        step=50,
        help="Typical LEO satellites: 300-2000 km"
    )

with col2:
    st.markdown("**Satellite Types:**")
    st.markdown("""
    - 🛰️ ISS: ~400 km
    - 🛰️ LEO: 300-2000 km
    - 🛰️ MEO: 2000-35000 km
    """)

# Generate signal
time_axis, clean_signal = generate_sine(10, 1.0, 1.0, 1000)

# Apply range loss
attenuated_signal = apply_free_space_loss(clean_signal, distance_km, reference_distance_km=100)
attenuation_db = distance_to_attenuation_db(distance_km, reference_distance_km=100)

# Calculate signal power ratio
signal_ratio = np.mean(attenuated_signal**2) / np.mean(clean_signal**2)
power_loss_percent = (1 - signal_ratio) * 100

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7))

# Plot 1: Signal comparison
show_samples = 500
ax1.plot(time_axis[:show_samples], clean_signal[:show_samples],
         linewidth=2, color='green', label=f'At 100 km (reference)', alpha=0.8)
ax1.plot(time_axis[:show_samples], attenuated_signal[:show_samples],
         linewidth=2, color='red', label=f'At {distance_km} km', alpha=0.8)
ax1.set_xlabel('Time (seconds)', fontsize=11)
ax1.set_ylabel('Amplitude', fontsize=11)
ax1.set_title(f'Range Loss Effect: {distance_km} km distance', fontsize=13, fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

# Plot 2: Path loss vs distance
distances = np.linspace(100, 2000, 100)
losses_db = [distance_to_attenuation_db(d, 100) for d in distances]

ax2.plot(distances, losses_db, linewidth=2, color='blue')
ax2.axvline(x=distance_km, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'Current: {distance_km} km')
ax2.axhline(y=attenuation_db, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax2.set_xlabel('Distance (km)', fontsize=11)
ax2.set_ylabel('Path Loss (dB)', fontsize=11)
ax2.set_title('Free-Space Path Loss vs Distance', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown(f"""
### 📊 Range Loss Analysis

**Current Distance:** {distance_km} km
**Path Loss:** {attenuation_db:.2f} dB
**Signal Power Lost:** {power_loss_percent:.2f}%
**Signal Power Remaining:** {(1-power_loss_percent/100)*100:.2f}%

**What This Means:**
""")

if distance_km <= 500:
    st.success("🟢 **Close Range:** Strong signal, minimal loss")
elif distance_km <= 1000:
    st.info("🟡 **Medium Range:** Noticeable signal weakening")
else:
    st.warning("🔴 **Far Range:** Significant signal attenuation")

st.markdown("""
**Try This:**
1. Start at 100 km - signal stays strong
2. Move to 200 km - notice it's not half strength, it's 1/4!
3. Move to 1000 km - see the dramatic signal drop
4. Observe the dB scale - it's logarithmic to handle huge ranges

---
""")

# ═══════════════════════════════════════════════════════════════════
# DEMO 2: ATMOSPHERIC ABSORPTION
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Demo 2: Atmospheric Absorption")

st.markdown("""
The atmosphere isn't perfectly transparent to radio waves.
Water vapor, oxygen, and weather absorb some signal energy.
""")

col_a, col_b = st.columns(2)

with col_a:
    elevation_angle = st.slider(
        "Satellite Elevation Angle (degrees)",
        min_value=5,
        max_value=90,
        value=30,
        help="Angle above horizon: Low = more atmosphere to pass through"
    )

with col_b:
    weather = st.selectbox(
        "Weather Conditions",
        ["clear", "light_clouds", "rain", "heavy_rain"],
        help="Weather affects signal absorption"
    )

# Apply atmospheric loss
atmos_signal = apply_atmospheric_loss(attenuated_signal, elevation_angle, weather)

# Plot
fig, ax = plt.subplots(figsize=(12, 4))
show_samples = 500
ax.plot(time_axis[:show_samples], attenuated_signal[:show_samples],
        linewidth=2, color='orange', label='After range loss only', alpha=0.7)
ax.plot(time_axis[:show_samples], atmos_signal[:show_samples],
        linewidth=2, color='purple', label='After range loss + atmosphere', alpha=0.8)
ax.set_xlabel('Time (seconds)', fontsize=11)
ax.set_ylabel('Amplitude', fontsize=11)
ax.set_title(f'Atmospheric Effects: {elevation_angle}° elevation, {weather}', fontsize=13, fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)
plt.close()

# Calculate additional loss
atmos_ratio = np.mean(atmos_signal**2) / np.mean(attenuated_signal**2)
atmos_loss_db = 10 * np.log10(1 / atmos_ratio) if atmos_ratio > 0 else 0

st.markdown(f"""
**Additional Atmospheric Loss:** {atmos_loss_db:.2f} dB
**Total Loss:** {attenuation_db + atmos_loss_db:.2f} dB

**Physical Explanation:**
- **Low elevation:** Signal passes through more atmosphere (longer path)
- **High elevation:** Nearly straight down, minimal atmosphere
- **Weather:** Rain/clouds absorb and scatter radio energy

---
""")

# ═══════════════════════════════════════════════════════════════════
# DEMO 3: FADING EVENTS
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Demo 3: Fading Events")

st.markdown("""
Sometimes signals experience **fades** - sudden temporary drops in strength.
Causes include:
- Satellite rotation (antenna pointed away)
- Passing behind obstacles
- Ionospheric disturbances
- Multipath interference
""")

col_i, col_ii = st.columns(2)

with col_i:
    num_fades = st.slider(
        "Number of Fade Events",
        min_value=0,
        max_value=5,
        value=2,
        help="Random temporary signal dropouts"
    )

with col_ii:
    fade_severity = st.selectbox(
        "Fade Severity",
        ["light", "moderate", "severe", "mixed"],
        index=3,
        help="How much the signal drops during fades"
    )

# Generate fades
duration = 1.0
if num_fades > 0:
    fade_events = generate_random_fades(duration, num_fades=num_fades, fade_severity=fade_severity)
    faded_signal = apply_fades_to_signal(atmos_signal, time_axis, fade_events)
else:
    fade_events = []
    faded_signal = atmos_signal

# Plot signal with fades
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(time_axis, atmos_signal, linewidth=1.5, color='blue', label='Without fades', alpha=0.6)
ax.plot(time_axis, faded_signal, linewidth=1.5, color='red', label='With fade events', alpha=0.8)

# Highlight fade regions
if fade_events:
    for fade in fade_events:
        ax.axvspan(fade.start_time, fade.start_time + fade.duration,
                  alpha=0.2, color='red', label='Fade event' if fade == fade_events[0] else '')
        ax.text(fade.start_time + fade.duration/2,
               max(faded_signal)*0.9,
               f'{fade.depth:.1f}×\n{fade.duration:.2f}s',
               ha='center', fontsize=9, color='darkred', fontweight='bold')

ax.set_xlabel('Time (seconds)', fontsize=11)
ax.set_ylabel('Amplitude', fontsize=11)
ax.set_title(f'Fading Events: {num_fades} fades, {fade_severity} severity', fontsize=13, fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)
plt.close()

if fade_events:
    st.markdown("**Fade Event Details:**")
    for i, fade in enumerate(fade_events, 1):
        st.markdown(f"- **Fade {i}:** at {fade.start_time:.2f}s, duration {fade.duration:.2f}s, depth {fade.depth:.2f}× (type: {fade.fade_type})")

st.markdown("""
---

### 🎓 Combined Channel Effects

**Real satellite links experience ALL of these:**
1. 📏 Range loss (always present)
2. 🌫️ Atmospheric absorption (always present)
3. ⚡ Occasional fading (intermittent)

**Impact on Communications:**
- Signal can drop by 30-40 dB total
- Fades cause burst errors (many bits corrupted in sequence)
- Error correction must handle these harsh conditions!

**Try This:**
1. Set distance to 1500 km, low elevation (10°), rain → see combined loss
2. Add 3-4 severe fades → simulate a difficult pass
3. Compare to ideal conditions (400 km, 90°, clear, no fades)

---

**➡️ Next:** Learn how to structure data in **Packets 101**

""")

st.success("✅ **Interactive Demo Active:** Explore how distance, atmosphere, and fading affect signals!")

st.divider()
st.caption("Chapter 4: Channel 101 | Phase 4: Fully Interactive Learning Console")
