"""
Script to initialize a SQLite database with proper tables for testing.
"""
import os
import sys
import sqlite3

# Add this to make imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the database file path
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_threat_intel.db")

# SQL to create tables
CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS threat_intelligence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        indicator TEXT NOT NULL,
        indicator_type TEXT NOT NULL,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_analysis TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        risk_score INTEGER DEFAULT 0,
        analysis_count INTEGER DEFAULT 1,
        indicator_metadata JSON,
        malware_data JSON
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS provider_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        indicator_id INTEGER NOT NULL,
        provider TEXT NOT NULL,
        report_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        detected BOOLEAN DEFAULT 0,
        confidence INTEGER DEFAULT 0,
        raw_data JSON,
        categories JSON,
        FOREIGN KEY (indicator_id) REFERENCES threat_intelligence (id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS indicator_relationships (
        source_id INTEGER NOT NULL,
        target_id INTEGER NOT NULL,
        relationship_type TEXT,
        confidence INTEGER DEFAULT 50,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (source_id, target_id),
        FOREIGN KEY (source_id) REFERENCES threat_intelligence (id) ON DELETE CASCADE,
        FOREIGN KEY (target_id) REFERENCES threat_intelligence (id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS threat_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS indicator_tags (
        indicator_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (indicator_id, tag_id),
        FOREIGN KEY (indicator_id) REFERENCES threat_intelligence (id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES threat_tags (id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS threat_feeds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        url TEXT,
        feed_type TEXT,
        last_updated TIMESTAMP,
        update_frequency INTEGER DEFAULT 24,
        active BOOLEAN DEFAULT 1,
        description TEXT,
        configuration JSON,
        stats JSON
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS analytics_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_type TEXT,
        report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        time_period INTEGER DEFAULT 30,
        report_data JSON,
        visualization_config JSON
    )
    """
]

# Sample data to insert
SAMPLE_INDICATORS = [
    {
        "indicator": "8.8.8.8",
        "indicator_type": "ip",
        "risk_score": 20,
        "analysis_count": 5,
        "indicator_metadata": '{"geolocation": {"country": "United States", "country_code": "US", "city": "Mountain View", "region": "California", "latitude": 37.4223, "longitude": -122.0847}, "asn_details": {"asn": "AS15169", "name": "Google LLC", "route": "8.8.8.0/24", "domain": "google.com"}}',
        "malware_data": '{}'
    },
    {
        "indicator": "example.com",
        "indicator_type": "domain",
        "risk_score": 65,
        "analysis_count": 3,
        "indicator_metadata": '{}',
        "malware_data": '{"trojan": 2, "spyware": 1}'
    },
    {
        "indicator": "https://malicious.com/file.exe",
        "indicator_type": "url",
        "risk_score": 85,
        "analysis_count": 2,
        "indicator_metadata": '{}',
        "malware_data": '{"trojan": 5, "ransomware": 3}'
    },
    {
        "indicator": "44d88612fea8a8f36de82e1278abb02f",
        "indicator_type": "file_hash",
        "risk_score": 90,
        "analysis_count": 7,
        "indicator_metadata": '{}',
        "malware_data": '{"ransomware": 7, "backdoor": 4, "trojan": 2}'
    }
]

SAMPLE_REPORTS = [
    {
        "indicator_id": 1,  # For 8.8.8.8
        "provider": "virustotal",
        "detected": False,
        "confidence": 15,
        "categories": '["dns"]',
        "raw_data": '{}'
    },
    {
        "indicator_id": 1,  # For 8.8.8.8
        "provider": "abuseipdb",
        "detected": False,
        "confidence": 10,
        "categories": '["dns"]',
        "raw_data": '{}'
    },
    {
        "indicator_id": 2,  # For example.com
        "provider": "virustotal",
        "detected": True,
        "confidence": 65,
        "categories": '["malicious", "phishing"]',
        "raw_data": '{}'
    },
    {
        "indicator_id": 3,  # For https://malicious.com/file.exe
        "provider": "urlscan",
        "detected": True,
        "confidence": 85,
        "categories": '["malware", "trojan"]',
        "raw_data": '{}'
    },
    {
        "indicator_id": 4,  # For the file hash
        "provider": "virustotal",
        "detected": True,
        "confidence": 90,
        "categories": '["ransomware", "trojan"]',
        "raw_data": '{}'
    },
    {
        "indicator_id": 4,  # For the file hash
        "provider": "otx",
        "detected": True,
        "confidence": 85,
        "categories": '["ransomware", "backdoor"]',
        "raw_data": '{}'
    }
]

def initialize_database():
    """Create tables and insert sample data."""
    # Remove existing database if it exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    for create_table_sql in CREATE_TABLES:
        cursor.execute(create_table_sql)
    
    # Insert sample indicators
    for indicator in SAMPLE_INDICATORS:
        cursor.execute(
            """
            INSERT INTO threat_intelligence 
            (indicator, indicator_type, risk_score, analysis_count, indicator_metadata, malware_data) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                indicator["indicator"],
                indicator["indicator_type"],
                indicator["risk_score"],
                indicator["analysis_count"],
                indicator["indicator_metadata"],
                indicator["malware_data"]
            )
        )
    
    # Insert sample reports
    for report in SAMPLE_REPORTS:
        cursor.execute(
            """
            INSERT INTO provider_reports 
            (indicator_id, provider, detected, confidence, categories, raw_data) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                report["indicator_id"],
                report["provider"],
                report["detected"],
                report["confidence"],
                report["categories"],
                report["raw_data"]
            )
        )
    
    # Commit changes and close
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {DB_FILE}")

if __name__ == "__main__":
    initialize_database()
