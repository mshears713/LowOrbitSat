"""
═══════════════════════════════════════════════════════════════════
MODULE: utils/streamlit_helpers.py
PURPOSE: Streamlit session state management and UI helpers
THEME: Sharing data across pages and making UI development easier
═══════════════════════════════════════════════════════════════════

📡 STORY:
Streamlit pages are stateless by default - each page loads fresh!
But we want to remember:
  • User preferences (SNR settings, FEC on/off, etc.)
  • Last simulation results (for visualization)
  • Mission history (recent transmissions)
  • Current satellite pass state

st.session_state is Streamlit's solution - a dictionary that
persists across page loads and reruns.

This module provides:
  • Clean initialization of session state
  • Helper functions for common state operations
  • Default values for all parameters
  • Type-safe accessors

SESSION STATE STRUCTURE:
┌──────────────────────────────────────────────────────────────┐
│ st.session_state:                                             │
│                                                               │
│  ├─ parameters (dict)                                         │
│  │   ├─ distance_km: float                                   │
│  │   ├─ snr_db: float                                        │
│  │   ├─ use_fec: bool                                        │
│  │   ├─ carrier_freq_hz: float                               │
│  │   └─ sample_rate_hz: int                                  │
│  │                                                            │
│  ├─ last_transmission (dict or None)                          │
│  │   └─ Full result from simulate_transmission()            │
│  │                                                            │
│  ├─ last_satellite_pass (dict or None)                        │
│  │   └─ Full result from simulate_satellite_pass()          │
│  │                                                            │
│  ├─ mission_history (list of dict)                            │
│  │   └─ Recent mission summaries                            │
│  │                                                            │
│  └─ ui_preferences (dict)                                     │
│      ├─ theme: str                                           │
│      ├─ show_advanced: bool                                  │
│      └─ plot_style: str                                      │
│                                                               │
└──────────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • Streamlit session state patterns
  • State persistence across pages
  • Clean state management architecture
  • Initialization and default values

═══════════════════════════════════════════════════════════════════
"""

from typing import Dict, Any, Optional, List
import streamlit as st


# ═══════════════════════════════════════════════════════════════
# DEFAULT PARAMETERS
# ═══════════════════════════════════════════════════════════════

DEFAULT_PARAMETERS = {
    # Transmission parameters
    'distance_km': 1000.0,
    'snr_db': 15.0,
    'use_fec': True,
    'carrier_freq_hz': 1000.0,
    'sample_rate_hz': 10000,

    # Satellite pass parameters
    'pass_duration_sec': 600.0,
    'max_elevation_deg': 80.0,
    'num_transmissions': 10,

    # Channel effects
    'enable_fading': False,
    'fade_severity': 0.5,
    'num_fades': 0,
}

DEFAULT_UI_PREFERENCES = {
    'theme': 'space',
    'show_advanced': False,
    'plot_style': 'default',
    'show_code_snippets': False,
    'auto_run': False,
}


# ═══════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════

def init_session_state():
    """
    Initialize Streamlit session state with default values.

    🎓 TEACHING NOTE:
    This function sets up all the state variables we'll use
    across different pages.

    We use "if key not in st.session_state" to avoid
    overwriting existing values when pages reload.

    Call this at the start of EVERY page to ensure state exists!

    Returns
    -------
    None
    """

    # ═══ PARAMETERS ═══
    if 'parameters' not in st.session_state:
        st.session_state.parameters = DEFAULT_PARAMETERS.copy()

    # ═══ LAST TRANSMISSION RESULT ═══
    if 'last_transmission' not in st.session_state:
        st.session_state.last_transmission = None

    # ═══ LAST SATELLITE PASS RESULT ═══
    if 'last_satellite_pass' not in st.session_state:
        st.session_state.last_satellite_pass = None

    # ═══ MISSION HISTORY ═══
    if 'mission_history' not in st.session_state:
        st.session_state.mission_history = []

    # ═══ UI PREFERENCES ═══
    if 'ui_preferences' not in st.session_state:
        st.session_state.ui_preferences = DEFAULT_UI_PREFERENCES.copy()

    # ═══ CURRENT MESSAGE ═══
    if 'current_message' not in st.session_state:
        st.session_state.current_message = "Hello from orbit!"

    # ═══ MISSION COUNTER ═══
    if 'mission_count' not in st.session_state:
        st.session_state.mission_count = 0


# ═══════════════════════════════════════════════════════════════
# PARAMETER ACCESSORS
# ═══════════════════════════════════════════════════════════════

def get_parameter(key: str, default=None) -> Any:
    """
    Get a parameter from session state.

    🎓 TEACHING NOTE:
    This provides safe access to parameters with fallback defaults.

    Parameters
    ----------
    key : str
        Parameter name
    default : any, optional
        Fallback value if key doesn't exist

    Returns
    -------
    value : any
        Parameter value
    """
    init_session_state()  # Ensure state exists
    return st.session_state.parameters.get(key, default)


def set_parameter(key: str, value: Any):
    """
    Set a parameter in session state.

    🎓 TEACHING NOTE:
    Updates a single parameter while preserving others.

    Parameters
    ----------
    key : str
        Parameter name
    value : any
        New value
    """
    init_session_state()
    st.session_state.parameters[key] = value


def get_all_parameters() -> Dict[str, Any]:
    """
    Get all parameters as a dictionary.

    Returns
    -------
    params : dict
        All current parameters
    """
    init_session_state()
    return st.session_state.parameters.copy()


def reset_parameters():
    """
    Reset all parameters to defaults.

    🎓 TEACHING NOTE:
    Useful for a "Reset to Defaults" button!
    """
    st.session_state.parameters = DEFAULT_PARAMETERS.copy()


# ═══════════════════════════════════════════════════════════════
# MISSION RESULT MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def save_transmission_result(result: Dict):
    """
    Save transmission result to session state.

    🎓 TEACHING NOTE:
    This stores the complete result from simulate_transmission()
    so other pages can visualize it.

    Parameters
    ----------
    result : dict
        Result from simulate_transmission()
    """
    init_session_state()

    # Save as last transmission
    st.session_state.last_transmission = result

    # Add to history (keep last 20)
    mission_summary = {
        'mission_id': st.session_state.mission_count,
        'message_sent': result['message_sent'],
        'message_received': result['message_received'],
        'ber': result['ber'],
        'snr_db': result['snr_actual_db'],
        'success': result['perfect_match'],
        'timestamp': result.get('timestamp', 'N/A')
    }

    st.session_state.mission_history.insert(0, mission_summary)
    st.session_state.mission_history = st.session_state.mission_history[:20]

    # Increment counter
    st.session_state.mission_count += 1


def get_last_transmission() -> Optional[Dict]:
    """
    Get the most recent transmission result.

    Returns
    -------
    result : dict or None
        Last transmission result, or None if no transmissions yet
    """
    init_session_state()
    return st.session_state.last_transmission


def save_satellite_pass_result(result: Dict):
    """
    Save satellite pass result to session state.

    Parameters
    ----------
    result : dict
        Result from simulate_satellite_pass()
    """
    init_session_state()
    st.session_state.last_satellite_pass = result


def get_last_satellite_pass() -> Optional[Dict]:
    """
    Get the most recent satellite pass result.

    Returns
    -------
    result : dict or None
        Last satellite pass result
    """
    init_session_state()
    return st.session_state.last_satellite_pass


def get_mission_history(max_count: int = 20) -> List[Dict]:
    """
    Get recent mission history.

    Parameters
    ----------
    max_count : int
        Maximum number of missions to return

    Returns
    -------
    history : list of dict
        Recent mission summaries
    """
    init_session_state()
    return st.session_state.mission_history[:max_count]


# ═══════════════════════════════════════════════════════════════
# UI PREFERENCE MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def get_ui_preference(key: str, default=None) -> Any:
    """Get a UI preference."""
    init_session_state()
    return st.session_state.ui_preferences.get(key, default)


def set_ui_preference(key: str, value: Any):
    """Set a UI preference."""
    init_session_state()
    st.session_state.ui_preferences[key] = value


# ═══════════════════════════════════════════════════════════════
# UI COMPONENT HELPERS
# ═══════════════════════════════════════════════════════════════

def render_parameter_controls(
    show_advanced: bool = False,
    key_prefix: str = ""
):
    """
    Render standard parameter control widgets.

    🎓 TEACHING NOTE:
    This creates the common sliders/inputs used across pages.
    By centralizing this, we ensure consistent UI and behavior.

    Parameters
    ----------
    show_advanced : bool
        Whether to show advanced parameters
    key_prefix : str
        Prefix for widget keys (avoids conflicts)

    Returns
    -------
    params : dict
        Current parameter values from widgets
    """
    init_session_state()

    st.subheader("🎛️ Transmission Parameters")

    col1, col2 = st.columns(2)

    with col1:
        distance_km = st.slider(
            "Distance (km)",
            min_value=100.0,
            max_value=5000.0,
            value=get_parameter('distance_km', 1000.0),
            step=100.0,
            key=f"{key_prefix}distance",
            help="Satellite-to-ground distance affects signal strength"
        )
        set_parameter('distance_km', distance_km)

        snr_db = st.slider(
            "Target SNR (dB)",
            min_value=-5.0,
            max_value=30.0,
            value=get_parameter('snr_db', 15.0),
            step=1.0,
            key=f"{key_prefix}snr",
            help="Signal-to-Noise Ratio: higher = cleaner signal"
        )
        set_parameter('snr_db', snr_db)

    with col2:
        use_fec = st.checkbox(
            "Enable Forward Error Correction (FEC)",
            value=get_parameter('use_fec', True),
            key=f"{key_prefix}fec",
            help="FEC can correct bit errors"
        )
        set_parameter('use_fec', use_fec)

        if show_advanced:
            carrier_freq = st.number_input(
                "Carrier Frequency (Hz)",
                min_value=100.0,
                max_value=10000.0,
                value=get_parameter('carrier_freq_hz', 1000.0),
                step=100.0,
                key=f"{key_prefix}carrier"
            )
            set_parameter('carrier_freq_hz', carrier_freq)

    return get_all_parameters()


def render_mission_summary(result: Dict):
    """
    Render a nice summary box for a mission result.

    🎓 TEACHING NOTE:
    This creates a consistent mission result display
    used across multiple pages.

    Parameters
    ----------
    result : dict
        Mission result from simulate_transmission()
    """
    if result is None:
        st.info("ℹ️ No mission data yet. Run a transmission first!")
        return

    # Success/failure styling
    if result['perfect_match']:
        st.success("✅ **TRANSMISSION SUCCESSFUL!**")
    else:
        st.warning("⚠️ **TRANSMISSION DEGRADED**")

    # Metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "BER",
            f"{result['ber']:.6f}",
            delta=f"{result['total_bit_errors']} errors"
        )

    with col2:
        st.metric(
            "SNR",
            f"{result['snr_actual_db']:.1f} dB",
            delta=f"Target: {result['snr_target_db']:.1f} dB"
        )

    with col3:
        st.metric(
            "Packet Status",
            "✓ Valid" if result['packet_valid'] else "✗ Invalid"
        )

    with col4:
        st.metric(
            "Message Match",
            "✓ Perfect" if result['perfect_match'] else "✗ Errors"
        )

    # Messages
    with st.expander("📨 Message Details"):
        st.write("**Sent:**")
        st.code(result['message_sent'])
        st.write("**Received:**")
        st.code(result['message_received'])

        if not result['perfect_match']:
            st.error("Messages do not match!")


def show_code_snippet(code: str, language: str = "python", title: str = "Code"):
    """
    Display a code snippet in an expandable section.

    🎓 TEACHING NOTE:
    Used to show the code behind each demo.

    Parameters
    ----------
    code : str
        Code to display
    language : str
        Syntax highlighting language
    title : str
        Section title
    """
    with st.expander(f"🔍 {title}"):
        st.code(code, language=language)


# ═══════════════════════════════════════════════════════════════
# PAGE NAVIGATION HELPER
# ═══════════════════════════════════════════════════════════════

def get_page_config() -> Dict[str, Any]:
    """
    Get standard page configuration for st.set_page_config().

    🎓 TEACHING NOTE:
    Every page should call st.set_page_config() as the first
    Streamlit command. This provides consistent settings.

    Returns
    -------
    config : dict
        Page configuration dictionary
    """
    return {
        'page_icon': '🛰️',
        'layout': 'wide',
        'initial_sidebar_state': 'expanded',
    }


# ═══════════════════════════════════════════════════════════════
# DEBUGGING NOTES
# ═══════════════════════════════════════════════════════════════
#
# Common Issues:
#   1. State not persisting between pages
#      → Make sure calling init_session_state() on every page
#   2. Widget value doesn't update state
#      → Check that you're calling set_parameter() after slider
#   3. "DuplicateWidgetID" error
#      → Use key_prefix parameter to make keys unique
#   4. State resets unexpectedly
#      → Check if you're assigning to st.session_state directly
#
# Testing Tips:
#   - Use st.write(st.session_state) to inspect state
#   - Add debug mode that shows current state
#   - Test page navigation thoroughly
#   - Check state persistence across reruns
#
# ═══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# FUTURE IMPROVEMENTS
# ═══════════════════════════════════════════════════════════════
#
# For ORBITER-1:
#   [ ] State persistence to disk (save/load sessions)
#   [ ] Undo/redo for parameter changes
#   [ ] State versioning (migration on updates)
#   [ ] Cross-user state sharing (cloud sync)
#   [ ] State validation and constraints
#   [ ] Automatic state cleanup (memory management)
#   [ ] State export to JSON/YAML
#
# ═══════════════════════════════════════════════════════════════
