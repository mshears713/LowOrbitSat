"""
═══════════════════════════════════════════════════════════════════
CHAPTER 8: SATELLITE PASS SIMULATOR
Timeline-based visibility and signal strength
═══════════════════════════════════════════════════════════════════
"""

import streamlit as st

st.set_page_config(page_title="Satellite Pass Simulator", page_icon="🛸", layout="wide")

st.title("🛸 Chapter 8: Satellite Pass Simulator")

st.markdown("""
---

### The Orbital Dance 🌍

Satellites orbit Earth - they're not always overhead!
Each "pass" is a brief window when the satellite is visible
from your ground station.

**Pass Phases:**
- 🌅 **AOS (Acquisition of Signal):** Satellite rises above horizon
- 🎯 **TCA (Time of Closest Approach):** Directly overhead, strongest signal
- 🌆 **LOS (Loss of Signal):** Satellite sets below horizon

---

### 🎯 Learning Objectives

- ✅ Satellite visibility windows
- ✅ Signal strength variation over time
- ✅ Elevation angle effects
- ✅ Pass duration and timing
- ✅ Simplified orbital mechanics

---

### 📈 Signal Strength Timeline

```
Signal Strength
    ^
100%│         ╱───╲
    │        ╱     ╲
 50%│       ╱       ╲
    │      ╱         ╲
  0%│─────╱───────────╲──────> Time
         AOS   TCA   LOS
        Rise  Peak   Set
```

---

---
""")

# Add path to import our modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.timing import SatellitePass, elevation_angle_curve, signal_strength_curve, distance_curve, generate_pass_timeline
import numpy as np
import matplotlib.pyplot as plt
import time as pytime

# ═══════════════════════════════════════════════════════════════════
# INTERACTIVE PASS SIMULATOR
# ═══════════════════════════════════════════════════════════════════

st.header("🔬 Interactive Satellite Pass Simulator")

st.markdown("""
Configure a satellite pass and watch how signal strength varies over time!
""")

# Pass configuration
col1, col2, col3 = st.columns(3)

with col1:
    pass_duration = st.slider(
        "Pass Duration (minutes)",
        min_value=2,
        max_value=15,
        value=8,
        help="How long the satellite is visible"
    )

with col2:
    max_elevation = st.slider(
        "Maximum Elevation (degrees)",
        min_value=10,
        max_value=90,
        value=45,
        help="How high the satellite gets above horizon"
    )

with col3:
    min_elevation_threshold = st.slider(
        "Min Elevation for Comms (degrees)",
        min_value=0,
        max_value=30,
        value=10,
        help="Below this angle, signal too weak"
    )

# Create satellite pass
start_time = 0.0
end_time = pass_duration * 60  # Convert to seconds
sat_pass = SatellitePass(
    start_time=start_time,
    end_time=end_time,
    max_elevation_deg=max_elevation
)

# Generate timeline
time_array, _ = generate_pass_timeline(sat_pass, sample_rate_hz=10)

# Calculate curves
elevation_angles = elevation_angle_curve(time_array, sat_pass)
distances = distance_curve(time_array, sat_pass, satellite_altitude_km=500)
signal_strengths = signal_strength_curve(time_array, sat_pass, include_range_loss=True,
                                        satellite_altitude_km=500)

# Find communication window
comm_start_idx = np.where(elevation_angles >= min_elevation_threshold)[0]
if len(comm_start_idx) > 0:
    comm_start = time_array[comm_start_idx[0]]
    comm_end = time_array[comm_start_idx[-1]]
    comm_duration = comm_end - comm_start
else:
    comm_start = 0
    comm_end = 0
    comm_duration = 0

# Timeline scrubber
st.markdown("### ⏱️ Timeline Scrubber")

current_time = st.slider(
    "Current Time (seconds)",
    min_value=0.0,
    max_value=end_time,
    value=end_time / 2,
    step=1.0,
    help="Scrub through the satellite pass"
)

# Find current index
current_idx = np.argmin(np.abs(time_array - current_time))
current_elevation = elevation_angles[current_idx]
current_distance = distances[current_idx]
current_signal = signal_strengths[current_idx]

# Current status display
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    minutes = int(current_time // 60)
    seconds = int(current_time % 60)
    st.metric("Time", f"{minutes:02d}:{seconds:02d}")

with col_b:
    st.metric("Elevation", f"{current_elevation:.1f}°")

with col_c:
    st.metric("Distance", f"{current_distance:.0f} km")

with col_d:
    signal_pct = current_signal * 100
    st.metric("Signal", f"{signal_pct:.1f}%")

# Status indicator
if current_elevation < min_elevation_threshold:
    st.error(f"🔴 **NO SIGNAL** - Satellite below {min_elevation_threshold}° elevation threshold")
elif current_elevation < 30:
    st.warning(f"🟡 **WEAK SIGNAL** - Low elevation ({current_elevation:.1f}°)")
elif current_elevation < 60:
    st.info(f"🟢 **GOOD SIGNAL** - Medium elevation ({current_elevation:.1f}°)")
else:
    st.success(f"🟢 **EXCELLENT SIGNAL** - High elevation ({current_elevation:.1f}°)")

# Visualization
st.markdown("### 📊 Pass Visualization")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))

# Plot 1: Elevation Angle
ax1.plot(time_array / 60, elevation_angles, linewidth=2, color='blue', label='Elevation Angle')
ax1.axhline(y=min_elevation_threshold, color='red', linestyle='--', linewidth=1.5,
           alpha=0.7, label=f'Min Elevation ({min_elevation_threshold}°)')
ax1.axvline(x=current_time / 60, color='purple', linestyle='--', linewidth=2,
           alpha=0.8, label=f'Current Time')
ax1.fill_between(time_array / 60, 0, min_elevation_threshold, alpha=0.2, color='red',
                label='No Comms Zone')
ax1.set_xlabel('Time (minutes)', fontsize=11)
ax1.set_ylabel('Elevation Angle (degrees)', fontsize=11)
ax1.set_title('Satellite Elevation Over Time', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right')
ax1.set_ylim([0, 95])

# Mark AOS, TCA, LOS
aos_time = start_time / 60
los_time = end_time / 60
tca_time = (start_time + end_time) / 2 / 60
ax1.scatter([aos_time], [0], color='green', s=100, zorder=5, marker='^', label='AOS (Rise)')
ax1.scatter([tca_time], [max_elevation], color='orange', s=100, zorder=5, marker='*', label='TCA (Peak)')
ax1.scatter([los_time], [0], color='red', s=100, zorder=5, marker='v', label='LOS (Set)')

# Plot 2: Distance
ax2.plot(time_array / 60, distances, linewidth=2, color='green', label='Range')
ax2.axvline(x=current_time / 60, color='purple', linestyle='--', linewidth=2, alpha=0.8)
ax2.set_xlabel('Time (minutes)', fontsize=11)
ax2.set_ylabel('Distance (km)', fontsize=11)
ax2.set_title('Satellite Range (Distance from Ground Station)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right')

# Plot 3: Signal Strength
ax3.plot(time_array / 60, signal_strengths * 100, linewidth=2, color='red', label='Signal Strength')
ax3.axvline(x=current_time / 60, color='purple', linestyle='--', linewidth=2,
           alpha=0.8, label='Current Time')
# Shade communication window
if comm_duration > 0:
    ax3.axvspan(comm_start / 60, comm_end / 60, alpha=0.2, color='green',
               label=f'Comms Window ({comm_duration/60:.1f} min)')
ax3.set_xlabel('Time (minutes)', fontsize=11)
ax3.set_ylabel('Relative Signal Strength (%)', fontsize=11)
ax3.set_title('Signal Strength (with range loss)', fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.legend(loc='upper right')
ax3.set_ylim([0, 105])

plt.tight_layout()
st.pyplot(fig)
plt.close()

# Pass statistics
st.markdown("""
---
### 📊 Pass Statistics
""")

col_i, col_ii, col_iii = st.columns(3)

with col_i:
    st.markdown(f"""
    **Pass Duration:**
    - Total: {pass_duration:.1f} minutes
    - Comms Window: {comm_duration/60:.1f} minutes
    - Efficiency: {comm_duration/(pass_duration*60)*100:.1f}%
    """)

with col_ii:
    st.markdown(f"""
    **Elevation:**
    - Maximum: {max_elevation:.1f}°
    - Minimum (comms): {min_elevation_threshold:.1f}°
    - At scrubber: {current_elevation:.1f}°
    """)

with col_iii:
    st.markdown(f"""
    **Range:**
    - Closest: {distances.min():.0f} km (at TCA)
    - Farthest: {distances.max():.0f} km (at AOS/LOS)
    - Current: {current_distance:.0f} km
    """)

st.markdown("""
---

### 🎓 Understanding Satellite Passes

**Key Phases:**
1. **AOS (Acquisition of Signal):** Satellite rises above horizon (0°)
2. **TCA (Time of Closest Approach):** Peak elevation, strongest signal
3. **LOS (Loss of Signal):** Satellite sets below horizon

**Why Signal Varies:**
- **Elevation Angle:** Higher angle = shorter path through atmosphere
- **Distance:** Closer satellite = stronger signal (inverse-square law)
- **Horizon Effects:** Low elevation has more obstacles and atmospheric absorption

**Real-World Considerations:**
- LEO satellites move fast (~7 km/s orbital velocity)
- Typical pass duration: 5-15 minutes
- Only 2-6 passes per day per satellite
- Must track satellite with directional antennas

**Try This:**
1. Set max elevation to 90° → see overhead pass
2. Set to 15° → see grazing pass (weak signal)
3. Raise min elevation threshold → see comms window shrink
4. Scrub timeline → watch signal change with elevation

---

**➡️ Next:** Browse historical data in **Mission Archive**

""")

st.success("✅ **Interactive Demo Active:** Scrub through satellite passes and watch signal dynamics!")

st.divider()
st.caption("Chapter 8: Satellite Pass Simulator | Phase 4: Fully Interactive Learning Console")
