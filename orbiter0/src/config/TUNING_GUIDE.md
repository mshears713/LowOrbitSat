# ORBITER-0 Parameter Tuning Guide
## Phase 5: Intuitive Behavior for Learning

### 🎓 Teaching Philosophy

Parameters are tuned to provide **intuitive cause-and-effect** for learners:
- Changes should be **visually obvious**
- Effects should match **real-world intuition**
- Errors should be **noticeable but not overwhelming**
- Demos should run **quickly** (no waiting)

---

## Recommended Parameter Ranges

### 🔊 Signal-to-Noise Ratio (SNR)

**Purpose**: Control signal quality and error rate

**Tuned Values**:
- **Excellent (25-30 dB)**: Near-perfect transmission, <0.1% BER
  - Use for: Demonstrating ideal case
  - Expected BER: ~0.0001
  - Visible errors: Almost none

- **Good (15-20 dB)**: Some errors visible, still mostly reliable
  - Use for: Default demos, showing FEC benefits
  - Expected BER: ~0.001-0.01
  - Visible errors: 1-10 per 1000 bits

- **Moderate (10-15 dB)**: Noticeable degradation, FEC helpful
  - Use for: **DEFAULT VALUE (15 dB)**
  - Expected BER: ~0.01-0.05
  - Visible errors: Clearly visible, but message usually recoverable

- **Poor (5-10 dB)**: Significant errors, FEC essential
  - Use for: Demonstrating error correction necessity
  - Expected BER: ~0.05-0.15
  - Visible errors: Many, message may be corrupted

- **Unusable (<5 dB)**: Too noisy, mostly errors
  - Use for: Showing failure modes
  - Expected BER: >0.2
  - Visible errors: Message unrecoverable without strong FEC

**Why 15 dB default?**
- Errors are **visible** (teaches that noise matters)
- Messages usually **recoverable** (not frustrating)
- FEC makes **obvious difference** (motivating)
- Matches "moderate quality" real-world scenario

---

### 📡 Distance Parameters

**Purpose**: Affect signal strength via path loss

**Tuned Values**:
- **Close (100-500 km)**: Minimal path loss, strong signal
  - Altitude: Very low orbit
  - Signal loss: ~0-10 dB
  - Use for: Basic demos

- **Typical (500-1500 km)**: Moderate path loss
  - Altitude: **DEFAULT (1000 km)** - Low Earth Orbit
  - Signal loss: ~10-20 dB
  - Use for: Most demos

- **Far (1500-5000 km)**: Significant path loss
  - Altitude: High orbit
  - Signal loss: ~20-40 dB
  - Use for: Challenging scenarios

**Why 1000 km default?**
- Representative of real LEO satellites (ISS, Starlink, etc.)
- Produces noticeable but not extreme path loss
- Easy to remember round number

---

### 🌊 Fading Event Parameters

**Purpose**: Simulate temporary signal dropouts

**Carefully Tuned for Intuitiveness**:

**Duration**: 0.5 seconds (DEFAULT)
- Long enough to be **clearly visible** in plots
- Short enough to **not dominate** the transmission
- Human-perceptible timescale

**Severity**: 10 dB reduction (DEFAULT)
- Reduces signal to ~1/10 power
- **Noticeable** but not complete blackout
- Usually causes errors but not total loss

**Frequency**: 0-3 fades per transmission
- 0 fades = baseline (compare against)
- 1-2 fades = realistic scenario
- 3+ fades = challenging scenario

**Teaching Tip**: Show transmission **with and without** fading side-by-side!

---

### 🛡️ Forward Error Correction (FEC)

**Purpose**: Demonstrate error correction capability

**Tuned Behavior**:

**Hamming(7,4) Code** (DEFAULT):
- Corrects: **1-bit errors** per 7-bit block
- Overhead: **75%** (3 parity bits for 4 data bits)
- Best use: SNR 10-15 dB
- Expected improvement: **2-5× reduction** in BER

**When to Enable/Disable**:
- **Disabled**: Show "raw" error rates (good for motivation)
- **Enabled**: Show correction in action (satisfying!)

**Teaching Sequence**:
1. Run without FEC at moderate SNR (15 dB) → See errors
2. Run with FEC at same SNR → See errors corrected!
3. Compare BER values → Quantify improvement

---

## Demo Scenarios (Recommended)

### Scenario 1: "Perfect Day"
```yaml
snr_db: 30
distance_km: 500
fading: none
fec: disabled
```
**Expected**: Nearly perfect transmission
**Teaching Point**: "This is the ideal case"

### Scenario 2: "Typical Operation" (DEFAULT)
```yaml
snr_db: 15
distance_km: 1000
fading: 1-2 events @ 10 dB, 0.5 sec
fec: enabled
```
**Expected**: Some errors, mostly corrected by FEC
**Teaching Point**: "Real systems have noise and corrections"

### Scenario 3: "Challenging Conditions"
```yaml
snr_db: 8
distance_km: 2000
fading: 3 events @ 15 dB, 0.8 sec
fec: enabled
```
**Expected**: Many errors, FEC helps but not perfect
**Teaching Point**: "FEC has limits"

### Scenario 4: "System Failure"
```yaml
snr_db: 2
distance_km: 4000
fading: continuous
fec: disabled
```
**Expected**: Unrecoverable errors
**Teaching Point**: "When things go wrong"

---

## Satellite Pass Tuning

**Purpose**: Simulate realistic pass with varying signal quality

**Tuned Values**:
- **Duration**: 300 sec (5 min) - **DEFAULT**
  - Shorter than real passes (~10 min) for faster demos
  - Long enough to show rise/peak/set curve

- **Max Elevation**: 60° - **DEFAULT**
  - High enough for good signal at peak
  - Not directly overhead (90°) to show variation

- **SNR Range**: 5-25 dB (varies with elevation)
  - Horizon (0°): 5 dB - poor quality
  - Peak (60°): 25 dB - excellent quality
  - Matches real-world physics (higher = closer = stronger)

- **Transmissions**: 10 per pass - **DEFAULT**
  - Enough to see the trend
  - Not so many that demo drags on

**Expected Behavior**:
```
Time    Elev    SNR    BER       Result
0s      0°      5dB    ~0.15     Many errors
60s     20°     12dB   ~0.05     Some errors
150s    60°     25dB   ~0.001    Nearly perfect  ← PEAK
240s    20°     12dB   ~0.05     Some errors again
300s    0°      5dB    ~0.15     Many errors
```

---

## Visualization Tuning

### Plot Parameters
- **Max bits to display**: 100
  - More = cluttered, harder to see individual bits
  - Less = not enough to see patterns

- **Time window**: 0.5-2.0 seconds
  - Shows multiple symbol periods
  - Fits on screen without scrolling

### Color Choices (Colorblind-Safe)
```
Signal:    Blue (#2E86AB)   - calm, reliable
Noise:     Purple (#A23B72) - chaotic, random
Corrected: Green (#06A77D)  - success, fixed
Error:     Red (#C73E1D)    - danger, problem
```

**Why these colors?**
- Distinguishable for deuteranopia (red-green colorblind)
- High contrast
- Match common conventions (green=good, red=bad)

---

## Common Tuning Mistakes to Avoid

### ❌ Too Easy
```yaml
snr_db: 40  # No errors at all
```
**Problem**: Students don't learn about noise/errors
**Fix**: Use 10-20 dB range

### ❌ Too Hard
```yaml
snr_db: 0  # Everything fails
```
**Problem**: Frustrating, looks broken
**Fix**: Use ≥5 dB for educational scenarios

### ❌ Too Slow
```yaml
satellite_pass:
  duration_sec: 900  # 15 minutes!
  num_transmissions: 50
```
**Problem**: Students lose interest waiting
**Fix**: Keep demos under 60 seconds when possible

### ❌ Imperceptible Changes
```yaml
fade_duration_sec: 0.01  # Too brief to see
```
**Problem**: Effect not noticeable
**Fix**: Use 0.5-1.0 sec for visibility

---

## Testing Your Tuning

**Checklist**:
- [ ] Run demo 3 times → Should see **different** results (randomness)
- [ ] But same **trend** (reproducible behavior)
- [ ] Errors are **visible** in plots (not all green or all red)
- [ ] Demo completes in **<60 seconds** (impatience threshold)
- [ ] Parameter changes cause **obvious** visual difference
- [ ] Students can **predict** what will happen ("more noise → more errors")

---

## Advanced: Calibration Curves

For research or advanced teaching, generate calibration data:

```python
# BER vs SNR sweep
snr_range = range(0, 30, 2)
for snr in snr_range:
    result = simulate_transmission(snr_db=snr, ...)
    plot(snr, result['ber'])
# Should see classic waterfall curve
```

**Expected Theoretical Curve (BPSK)**:
```
SNR (dB)    Theoretical BER
0           0.079
5           0.016
10          0.0004
15          10^-6
20          10^-9
```

**If your measured values differ significantly**:
- Check noise generation (should be Gaussian)
- Verify SNR calculation (power not amplitude!)
- Ensure proper BPSK demodulation

---

## Summary: Golden Rules

1. **Default = Moderate Challenge**
   - Some errors, not overwhelming
   - FEC makes noticeable difference

2. **Make Changes Obvious**
   - 2× change should look clearly different
   - Use side-by-side comparisons

3. **Match Intuition**
   - "Farther away" → weaker signal ✓
   - "More noise" → more errors ✓
   - "FEC enabled" → fewer errors ✓

4. **Keep It Fast**
   - Demos under 60 sec when possible
   - Use fewer transmissions if needed

5. **Enable Exploration**
   - Sliders for all key parameters
   - Reset to defaults button
   - Save/load parameter sets

---

**Remember**: We're optimizing for **learning**, not **realism**!

Real satellites operate at:
- GHz frequencies (we use kHz)
- Mbps data rates (we use 100 bps)
- Hours of operation (we use seconds)

**That's okay!** Simplified parameters teach the same concepts faster.

🚀 **Happy tuning!**
