# LowOrbitSat Setup Instructions

## Quick Start

### 1. Install Python Dependencies

The application requires several Python packages to function correctly. Install them using:

```bash
pip install -r requirements.txt
```

### 2. Required Dependencies

The following packages are required:
- **numpy** (≥1.24.0) - Numerical computing for signal arrays
- **scipy** (≥1.10.0) - Signal processing and spectrograms
- **matplotlib** (≥3.7.0) - Waveform plots and visualizations
- **streamlit** (≥1.28.0) - Interactive web interface
- **pyyaml** (≥6.0) - Configuration file parsing

### 3. Verify Installation

Test that all modules import correctly:

```bash
cd orbiter0
python3 -c "import sys; sys.path.append('src'); from signals.generator import generate_sine; from comms.packetizer import create_packet; from utils.math_helpers import calculate_ber; from channel.noise import add_awgn; print('✅ All modules loaded successfully!')"
```

### 4. Run the Application

Launch the Streamlit application:

```bash
cd orbiter0/streamlit_app
streamlit run Home.py
```

## Troubleshooting

### Module Import Errors

If you see errors like `ModuleNotFoundError: No module named 'numpy'` or similar, it means the dependencies are not installed. Run:

```bash
pip install -r requirements.txt
```

### Python Cache Issues

If you encounter import errors after updating code, clear the Python cache:

```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### Module Structure

The project uses the following module structure:
- `signals/` - Signal generation and modulation (formerly `signal/`, renamed to avoid conflict with Python's standard library)
- `comms/` - Communications, packetization, and error correction
- `utils/` - Utility functions for math, timing, and plotting
- `channel/` - Channel effects (noise, fading, range loss)

All Streamlit pages import these modules using:
```python
import sys
sys.path.append('../../src')
from signals.generator import generate_sine
```

## Common Issues

### Issue: Graphs not displaying
**Cause:** Missing dependencies (numpy, matplotlib, scipy)
**Solution:** Install requirements: `pip install -r requirements.txt`

### Issue: "No module named 'signal'" error
**Cause:** Old cache files from before the `signal` → `signals` rename
**Solution:** Clear Python cache and restart

### Issue: Import errors in all pages
**Cause:** Dependencies not installed
**Solution:** Run `pip install -r requirements.txt`
