"""
═══════════════════════════════════════════════════════════════════
MODULE: utils/import_export.py
PURPOSE: Import/export tools for mission configurations and results
THEME: Sharing and reproducibility
═══════════════════════════════════════════════════════════════════

📡 STORY:
Found an interesting scenario? Want to share it with others?
Need to reproduce exact conditions for debugging?

This module provides tools to save and load:
  • Mission configurations (parameters)
  • Complete mission results
  • Satellite pass scenarios
  • Custom channel conditions

Export formats:
  • JSON (human-readable, sharable)
  • YAML (configuration files)
  • CSV (for analysis in Excel/Python)

LEARNING GOALS:
  • Reproducible experiments
  • Sharing scenarios with others
  • Data analysis workflows
  • Configuration management

═══════════════════════════════════════════════════════════════════
"""

import json
import yaml
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np


# ═══════════════════════════════════════════════════════════════
# JSON EXPORT/IMPORT
# ═══════════════════════════════════════════════════════════════

def export_mission_json(result: Dict, filepath: str) -> str:
    """
    Export mission result to JSON file.

    🎓 TEACHING NOTE:
    JSON is great for:
    - Human-readable data
    - Web sharing (JavaScript can read it)
    - Structured data with nested fields

    Parameters
    ----------
    result : dict
        Mission result from simulate_transmission()
    filepath : str
        Output file path

    Returns
    -------
    filepath : str
        Actual path where file was saved
    """
    # Convert numpy arrays to lists (JSON-serializable)
    serializable_result = _make_json_serializable(result)

    # Add export metadata
    export_data = {
        'metadata': {
            'export_time': datetime.now().isoformat(),
            'orbiter_version': '0.1.0',
            'format': 'mission_result'
        },
        'mission': serializable_result
    }

    # Write to file
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"✅ Mission exported to: {filepath}")
    return str(filepath)


def import_mission_json(filepath: str) -> Dict:
    """
    Import mission result from JSON file.

    🎓 TEACHING NOTE:
    This loads a previously exported mission.
    You can then re-plot, re-analyze, or compare results!

    Parameters
    ----------
    filepath : str
        Path to JSON file

    Returns
    -------
    result : dict
        Mission result dictionary
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Extract mission data
    if 'mission' in data:
        result = data['mission']
    else:
        # Assume old format (direct mission data)
        result = data

    print(f"✅ Mission imported from: {filepath}")
    return result


# ═══════════════════════════════════════════════════════════════
# CONFIGURATION EXPORT/IMPORT
# ═══════════════════════════════════════════════════════════════

def export_config_yaml(config: Dict, filepath: str) -> str:
    """
    Export configuration parameters to YAML file.

    🎓 TEACHING NOTE:
    YAML is perfect for configuration files:
    - Very human-readable (no quotes needed!)
    - Supports comments (explain your settings)
    - Standard for config files

    Parameters
    ----------
    config : dict
        Configuration dictionary
    filepath : str
        Output file path

    Returns
    -------
    filepath : str
        Actual path where file was saved
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Add header comment
    header = f"""# ORBITER-0 Mission Configuration
# Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# This file can be loaded to reproduce the exact same scenario.
# Modify values and re-import to experiment!
#
"""

    with open(filepath, 'w') as f:
        f.write(header)
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"✅ Configuration exported to: {filepath}")
    return str(filepath)


def import_config_yaml(filepath: str) -> Dict:
    """
    Import configuration from YAML file.

    Parameters
    ----------
    filepath : str
        Path to YAML file

    Returns
    -------
    config : dict
        Configuration dictionary
    """
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)

    print(f"✅ Configuration imported from: {filepath}")
    return config


# ═══════════════════════════════════════════════════════════════
# CSV EXPORT (for analysis)
# ═══════════════════════════════════════════════════════════════

def export_satellite_pass_csv(pass_results: Dict, filepath: str) -> str:
    """
    Export satellite pass timeline to CSV for analysis.

    🎓 TEACHING NOTE:
    CSV (Comma-Separated Values) is great for:
    - Opening in Excel/Google Sheets
    - Data analysis in Python/R
    - Plotting in other tools

    Parameters
    ----------
    pass_results : dict
        Results from simulate_satellite_pass()
    filepath : str
        Output CSV file path

    Returns
    -------
    filepath : str
        Actual path where file was saved
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Extract timeline data
    timeline = pass_results.get('timeline', {})
    transmissions = pass_results.get('transmissions', [])

    # Create CSV rows
    rows = []
    for i, tx in enumerate(transmissions):
        row = {
            'transmission_num': i + 1,
            'time_sec': timeline['times'][i] if 'times' in timeline else i * 30,
            'elevation_deg': timeline['elevations'][i] if 'elevations' in timeline else 0,
            'snr_db': timeline['snrs'][i] if 'snrs' in timeline else tx.get('snr_actual_db', 0),
            'ber': timeline['bers'][i] if 'bers' in timeline else tx.get('ber', 0),
            'packet_valid': tx.get('packet_valid', False),
            'message_match': tx.get('perfect_match', False),
            'bit_errors': tx.get('total_bit_errors', 0),
        }
        rows.append(row)

    # Write CSV
    if rows:
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"✅ Pass data exported to: {filepath}")
    return str(filepath)


def export_mission_summary_csv(missions: List[Dict], filepath: str) -> str:
    """
    Export multiple mission summaries to CSV.

    🎓 TEACHING NOTE:
    Perfect for comparing many missions:
    - Different SNR values
    - With/without FEC
    - Various distances

    Parameters
    ----------
    missions : list of dict
        List of mission results
    filepath : str
        Output CSV file path

    Returns
    -------
    filepath : str
        Path where file was saved
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Extract key metrics from each mission
    rows = []
    for i, mission in enumerate(missions):
        row = {
            'mission_id': i + 1,
            'message_sent': mission.get('message_sent', ''),
            'message_received': mission.get('message_received', ''),
            'ber': mission.get('ber', 0),
            'snr_db': mission.get('snr_actual_db', 0),
            'distance_km': mission.get('config', {}).get('distance_km', 0),
            'use_fec': mission.get('config', {}).get('use_fec', False),
            'packet_valid': mission.get('packet_valid', False),
            'perfect_match': mission.get('perfect_match', False),
        }
        rows.append(row)

    # Write CSV
    if rows:
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"✅ Mission summary exported to: {filepath} ({len(rows)} missions)")
    return str(filepath)


# ═══════════════════════════════════════════════════════════════
# SCENARIO TEMPLATES
# ═══════════════════════════════════════════════════════════════

SCENARIO_TEMPLATES = {
    'perfect_conditions': {
        'name': 'Perfect Conditions',
        'description': 'Ideal scenario with no noise or fading',
        'params': {
            'distance_km': 500,
            'snr_db': 30,
            'use_fec': False,
            'fading_events': None
        }
    },

    'typical_leo': {
        'name': 'Typical LEO Satellite',
        'description': 'Standard low Earth orbit scenario',
        'params': {
            'distance_km': 1000,
            'snr_db': 15,
            'use_fec': True,
            'fading_events': None
        }
    },

    'challenging': {
        'name': 'Challenging Conditions',
        'description': 'Low SNR with fading',
        'params': {
            'distance_km': 2000,
            'snr_db': 8,
            'use_fec': True,
            'fading_events': []  # Would add FadeEvent objects
        }
    },

    'deep_space': {
        'name': 'Deep Space (Extreme)',
        'description': 'Very weak signal, FEC essential',
        'params': {
            'distance_km': 5000,
            'snr_db': 3,
            'use_fec': True,
            'fading_events': None
        }
    },
}


def get_scenario_template(name: str) -> Dict:
    """
    Get a predefined scenario template.

    🎓 TEACHING NOTE:
    Templates provide starting points for experiments.
    Load one, modify it, and see what changes!

    Parameters
    ----------
    name : str
        Scenario name (see SCENARIO_TEMPLATES)

    Returns
    -------
    scenario : dict
        Scenario configuration
    """
    if name not in SCENARIO_TEMPLATES:
        available = ', '.join(SCENARIO_TEMPLATES.keys())
        raise ValueError(f"Unknown scenario: {name}. Available: {available}")

    return SCENARIO_TEMPLATES[name].copy()


def list_scenarios() -> List[str]:
    """List all available scenario templates."""
    return list(SCENARIO_TEMPLATES.keys())


def export_scenario_template(name: str, filepath: str) -> str:
    """
    Export a scenario template to YAML file.

    Parameters
    ----------
    name : str
        Scenario name
    filepath : str
        Output file path

    Returns
    -------
    filepath : str
        Path where file was saved
    """
    scenario = get_scenario_template(name)
    return export_config_yaml(scenario, filepath)


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def _make_json_serializable(obj: Any) -> Any:
    """
    Convert numpy arrays and other non-JSON types to JSON-serializable forms.

    🎓 TEACHING NOTE:
    JSON can't store numpy arrays or complex numbers directly.
    We convert them to lists first.
    """
    if isinstance(obj, dict):
        return {key: _make_json_serializable(val) for key, val in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_make_json_serializable(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert numpy array to list
    elif isinstance(obj, (np.integer, np.floating)):
        return float(obj)  # Convert numpy scalars
    elif isinstance(obj, complex):
        return {'real': obj.real, 'imag': obj.imag}
    elif isinstance(obj, Path):
        return str(obj)
    else:
        return obj


def create_export_filename(base_name: str, format: str = 'json') -> str:
    """
    Create timestamped export filename.

    🎓 TEACHING NOTE:
    Timestamps prevent overwriting previous exports.

    Parameters
    ----------
    base_name : str
        Base name (e.g., "mission", "pass", "config")
    format : str
        File extension (json, yaml, csv)

    Returns
    -------
    filename : str
        Timestamped filename
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{base_name}_{timestamp}.{format}"


# ═══════════════════════════════════════════════════════════════
# BATCH OPERATIONS
# ═══════════════════════════════════════════════════════════════

def export_batch_missions(missions: List[Dict], output_dir: str) -> List[str]:
    """
    Export multiple missions to separate JSON files.

    Parameters
    ----------
    missions : list of dict
        List of mission results
    output_dir : str
        Output directory path

    Returns
    -------
    filepaths : list of str
        Paths to all exported files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filepaths = []
    for i, mission in enumerate(missions):
        filename = f"mission_{i+1:03d}.json"
        filepath = output_dir / filename
        export_mission_json(mission, str(filepath))
        filepaths.append(str(filepath))

    print(f"✅ Exported {len(missions)} missions to {output_dir}")
    return filepaths


def import_batch_missions(directory: str) -> List[Dict]:
    """
    Import all JSON mission files from a directory.

    Parameters
    ----------
    directory : str
        Directory containing JSON files

    Returns
    -------
    missions : list of dict
        List of imported mission results
    """
    directory = Path(directory)
    json_files = sorted(directory.glob("*.json"))

    missions = []
    for filepath in json_files:
        try:
            mission = import_mission_json(str(filepath))
            missions.append(mission)
        except Exception as e:
            print(f"⚠️ Failed to import {filepath}: {e}")

    print(f"✅ Imported {len(missions)} missions from {directory}")
    return missions


# ═══════════════════════════════════════════════════════════════
# DEBUGGING NOTES
# ═══════════════════════════════════════════════════════════════
#
# Common Issues:
#   1. "JSON not serializable" → Use _make_json_serializable()
#   2. File path doesn't exist → We create parent dirs automatically
#   3. Import fails → Check file format (JSON vs YAML)
#   4. CSV opens weird in Excel → Use UTF-8 encoding
#
# Testing Tips:
#   - Export then import to verify round-trip works
#   - Check CSV files open correctly in Excel
#   - Verify YAML files are human-readable
#   - Test with numpy arrays in data
#
# ═══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# FUTURE IMPROVEMENTS
# ═══════════════════════════════════════════════════════════════
#
# For ORBITER-1:
#   [ ] Compressed formats (gzip JSON)
#   [ ] Binary export (HDF5, NetCDF)
#   [ ] Cloud storage integration (S3, Drive)
#   [ ] Automatic scenario tagging/search
#   [ ] Version migration (handle format changes)
#   [ ] Export to other tools (MATLAB, GNU Radio)
#   [ ] Real-time streaming export
#
# ═══════════════════════════════════════════════════════════════
