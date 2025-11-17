"""
═══════════════════════════════════════════════════════════════════
MODULE: comms/storage.py
PURPOSE: SQLite database for mission archival
THEME: Remembering every transmission for analysis
═══════════════════════════════════════════════════════════════════

📡 STORY:
Every satellite pass is a mission. We want to save:
  • What message we sent
  • What message we received
  • Signal quality metrics (SNR, BER)
  • Timestamps
  • Error statistics

This creates a permanent record for learning and analysis!

DATABASE SCHEMA:
┌──────────────────────────────────────────────────────────────┐
│ missions table:                                               │
│  - id (PRIMARY KEY)                                          │
│  - timestamp (when mission occurred)                          │
│  - message_sent (original text)                              │
│  - message_received (decoded text)                            │
│  - ber (bit error rate)                                       │
│  - snr_db (signal-to-noise ratio)                            │
│  - packets_total (number of packets)                          │
│  - packets_corrupted (failed CRC)                            │
│  - metadata (JSON for extra info)                            │
└──────────────────────────────────────────────────────────────┘

LEARNING GOALS:
  • Database basics (SQLite)
  • Persistent storage
  • Querying historical data
  • Data analysis possibilities

SIMPLIFICATIONS:
  - Single table design
  - JSON for flexible metadata
  - No complex queries or indexes

═══════════════════════════════════════════════════════════════════
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional
import time


def get_default_db_path():
    """Get the default database path."""
    # Put database in src/data/ directory
    db_dir = Path(__file__).parent.parent / 'data'
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / 'missions.sqlite'


def init_database(db_path=None):
    """
    Initialize the missions database.

    🎓 TEACHING NOTE:
    This creates the database file and table structure.
    SQLite is a simple, file-based database - perfect for this project!

    The table stores one row per mission (satellite pass).

    Parameters
    ----------
    db_path : str or Path, optional
        Database file path. If None, uses default location.

    Returns
    -------
    db_path : Path
        The path where database was created
    """
    if db_path is None:
        db_path = get_default_db_path()
    else:
        db_path = Path(db_path)

    # 🎓 CONNECT TO DATABASE
    # SQLite creates the file if it doesn't exist
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # 🎓 CREATE TABLE
    # IF NOT EXISTS = safe to run multiple times
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            message_sent TEXT,
            message_received TEXT,
            ber REAL,
            snr_db REAL,
            packets_total INTEGER,
            packets_corrupted INTEGER,
            metadata TEXT
        )
    ''')

    # Save changes and close
    conn.commit()
    conn.close()

    return db_path


def save_mission(message_sent, message_received, ber=None, snr_db=None,
                packets_total=0, packets_corrupted=0, metadata=None,
                db_path=None):
    """
    Save a mission record to the database.

    🎓 TEACHING NOTE:
    Every satellite pass generates data. This function
    saves it for future analysis!

    You can query the database later to see:
    - How has performance changed over time?
    - What's the typical BER for our system?
    - Which messages had the most errors?

    Parameters
    ----------
    message_sent : str
        Original message transmitted
    message_received : str
        Message after decoding (may have errors)
    ber : float, optional
        Bit error rate (0.0 to 1.0)
    snr_db : float, optional
        Signal-to-noise ratio in dB
    packets_total : int
        Total packets in transmission
    packets_corrupted : int
        Packets that failed CRC
    metadata : dict, optional
        Extra info (will be stored as JSON)
    db_path : str or Path, optional
        Database path. If None, uses default.

    Returns
    -------
    mission_id : int
        ID of the inserted mission record
    """
    if db_path is None:
        db_path = get_default_db_path()

    # Ensure database exists
    if not Path(db_path).exists():
        init_database(db_path)

    # Current timestamp
    timestamp = time.time()

    # Convert metadata to JSON
    metadata_json = json.dumps(metadata) if metadata else None

    # 🎓 INSERT RECORD
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO missions (
            timestamp, message_sent, message_received, ber, snr_db,
            packets_total, packets_corrupted, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, message_sent, message_received, ber, snr_db,
          packets_total, packets_corrupted, metadata_json))

    mission_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return mission_id


def query_missions(limit=100, min_snr_db=None, max_ber=None, db_path=None):
    """
    Query missions from database with optional filters.

    🎓 TEACHING NOTE:
    This lets you retrieve historical data for analysis.

    Examples:
    - Get last 10 missions: query_missions(limit=10)
    - Get only good quality: query_missions(min_snr_db=20, max_ber=0.01)
    - Get all missions: query_missions(limit=None)

    Parameters
    ----------
    limit : int, optional
        Maximum number of records to return
    min_snr_db : float, optional
        Minimum SNR filter
    max_ber : float, optional
        Maximum BER filter
    db_path : str or Path, optional
        Database path

    Returns
    -------
    missions : List[dict]
        List of mission records
    """
    if db_path is None:
        db_path = get_default_db_path()

    if not Path(db_path).exists():
        return []  # No database yet

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row  # Return rows as dicts
    cursor = conn.cursor()

    # 🎓 BUILD QUERY
    query = 'SELECT * FROM missions WHERE 1=1'
    params = []

    if min_snr_db is not None:
        query += ' AND snr_db >= ?'
        params.append(min_snr_db)

    if max_ber is not None:
        query += ' AND ber <= ?'
        params.append(max_ber)

    # Order by most recent first
    query += ' ORDER BY timestamp DESC'

    if limit is not None:
        query += ' LIMIT ?'
        params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Convert to list of dicts
    missions = []
    for row in rows:
        mission = dict(row)
        # Parse metadata JSON
        if mission['metadata']:
            mission['metadata'] = json.loads(mission['metadata'])
        missions.append(mission)

    conn.close()

    return missions


def get_mission_by_id(mission_id, db_path=None):
    """
    Retrieve a specific mission by ID.

    Parameters
    ----------
    mission_id : int
        Mission ID
    db_path : str or Path, optional
        Database path

    Returns
    -------
    mission : dict or None
        Mission record or None if not found
    """
    if db_path is None:
        db_path = get_default_db_path()

    if not Path(db_path).exists():
        return None

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM missions WHERE id = ?', (mission_id,))
    row = cursor.fetchone()

    if row:
        mission = dict(row)
        if mission['metadata']:
            mission['metadata'] = json.loads(mission['metadata'])
    else:
        mission = None

    conn.close()

    return mission


def get_mission_statistics(db_path=None):
    """
    Calculate aggregate statistics across all missions.

    🎓 TEACHING NOTE:
    This shows you overall system performance!

    Useful for:
    - Tracking improvements over time
    - Understanding typical error rates
    - Finding problematic patterns

    Parameters
    ----------
    db_path : str or Path, optional
        Database path

    Returns
    -------
    stats : dict
        {
            'total_missions': int,
            'average_ber': float,
            'average_snr_db': float,
            'total_packets': int,
            'total_corrupted': int,
            'packet_error_rate': float
        }
    """
    if db_path is None:
        db_path = get_default_db_path()

    if not Path(db_path).exists():
        return {'total_missions': 0}

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # 🎓 AGGREGATE QUERIES
    # COUNT, AVG, SUM are SQL aggregate functions

    cursor.execute('''
        SELECT
            COUNT(*) as total_missions,
            AVG(ber) as avg_ber,
            AVG(snr_db) as avg_snr,
            SUM(packets_total) as total_packets,
            SUM(packets_corrupted) as total_corrupted
        FROM missions
    ''')

    row = cursor.fetchone()

    total_missions = row[0] or 0
    avg_ber = row[1] or 0.0
    avg_snr = row[2] or 0.0
    total_packets = row[3] or 0
    total_corrupted = row[4] or 0

    # Calculate packet error rate
    if total_packets > 0:
        per = total_corrupted / total_packets
    else:
        per = 0.0

    conn.close()

    return {
        'total_missions': total_missions,
        'average_ber': avg_ber,
        'average_snr_db': avg_snr,
        'total_packets': total_packets,
        'total_corrupted': total_corrupted,
        'packet_error_rate': per
    }


def clear_database(db_path=None):
    """
    Clear all missions from database (use with caution!).

    🎓 TEACHING NOTE:
    This is useful for starting fresh with experiments.
    In production systems, you'd rarely delete data!

    Parameters
    ----------
    db_path : str or Path, optional
        Database path

    Returns
    -------
    rows_deleted : int
        Number of missions deleted
    """
    if db_path is None:
        db_path = get_default_db_path()

    if not Path(db_path).exists():
        return 0

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute('DELETE FROM missions')
    rows_deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return rows_deleted


# ═══ DEBUGGING NOTES ═══
#
# Common Issues:
#   1. Database locked? Close all connections before new operations
#   2. File not found? init_database() creates it automatically
#   3. JSON decode error? Check metadata is valid JSON
#   4. Query returns nothing? Check filters aren't too restrictive
#
# Testing Tips:
#   - Use SQLite browser tool to inspect database
#   - Check file permissions if database won't create
#   - Verify data types match schema
#   - Test queries with different filters
#
# Gotchas:
#   - SQLite is file-based (not client-server)
#   - Concurrent writes can cause locking
#   - TEXT type can store large strings
#   - REAL type is floating-point (not exact decimal)


# ═══ FUTURE IMPROVEMENTS ═══
#
# For Advanced Version (ORBITER-1):
#   [ ] Add indexes for faster queries
#   [ ] Separate tables for packets and missions
#   [ ] Support for multiple ground stations
#   [ ] Export to CSV/Excel
#   [ ] Time-series analysis functions
#   [ ] Automatic cleanup of old records
#
# For Deep Space Version:
#   [ ] Store full signal waveforms
#   [ ] Support very large datasets (> 1GB)
#   [ ] Distributed database support
#   [ ] Real-time replication
