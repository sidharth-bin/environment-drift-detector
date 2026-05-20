#!/usr/bin/env python3
"""
Module Name:    drift_analyzer.py
Description:    Multi-Environment Configuration Drift & Anomaly Detector
Author:         Sidharth (sidharth-bin)
Architecture:   Zero-dependency tree comparison engine for .env and JSON configs
"""

import os
import sys
import json

class ConfigDriftDetector:
    def __init__(self):
        """Initializes the drift detection engine metrics."""
        self.total_keys_scanned = 0
        self.drift_anomalies_found = 0

    def _parse_env_file(self, raw_content: str) -> dict:
        """Parses raw .env string structures into a comparable dictionary map."""
        config_map = {}
        for line in raw_content.splitlines():
            line = line.strip()
            # Ignore comments and empty lines
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                config_map[key.strip()] = val.strip().strip("'").strip('"')
        return config_map

    def analyze_drift(self, base_config_name: str, base_content: str, target_config_name: str, target_content: str, file_type: str = "env") -> dict:
        """
        Cross-references a Target environment against a Base (Source of Truth) environment 
        to detect missing variables and architectural drift.
        """
        # Parse based on file type
        if file_type == "json":
            try:
                base_map = json.loads(base_content)
                target_map = json.loads(target_content)
            except json.JSONDecodeError as e:
                return {"error": f"JSON Parsing Failure: {str(e)}"}
        else:
            base_map = self._parse_env_file(base_content)
            target_map = self._parse_env_file(target_content)

        self.total_keys_scanned += len(base_map)
        
        drift_report = {
            "source_of_truth": base_config_name,
            "target_evaluated": target_config_name,
            "missing_keys_in_target": [],
            "empty_values_in_target": []
        }

        # Compare Base against Target
        for key, base_val in base_map.items():
            if key not in target_map:
                drift_report["missing_keys_in_target"].append(key)
                self.drift_anomalies_found += 1
            elif target_map[key] in ["", "null", "None"]:
                drift_report["empty_values_in_target"].append(key)
                self.drift_anomalies_found += 1

        # Calculate environment health score (100% means perfect alignment)
        total_checks = len(base_map)
        if total_checks > 0:
            health_pct = ((total_checks - len(drift_report["missing_keys_in_target"])) / total_checks) * 100
        else:
            health_pct = 100.0

        drift_report["alignment_score"] = round(health_pct, 2)
        drift_report["status"] = "DRIFT_DETECTED" if self.drift_anomalies_found > 0 else "SYNCED"

        return drift_report

if __name__ == "__main__":
    print("=== ENVIRONMENT DRIFT DETECTOR INITIALIZING ===")
    detector = ConfigDriftDetector()
    
    # Simulating a Source of Truth (e.g., Staging environment .env)
    mock_staging_env = """
    DB_HOST=staging-db.internal
    DB_PORT=5432
    STRIPE_API_KEY=sk_test_12345
    REDIS_CACHE_URL=redis://cache:6379
    FEATURE_NEW_UI=true
    """
    
    # Simulating a drifting Target (e.g., Production environment .env missing the new Redis/UI keys)
    mock_production_env = """
    DB_HOST=prod-db.internal
    DB_PORT=5432
    STRIPE_API_KEY=sk_live_98765
    # Missing REDIS_CACHE_URL
    # Missing FEATURE_NEW_UI
    """
    
    print(f"[INFO] Cross-referencing STAGING vs PRODUCTION configurations...")
    report = detector.analyze_drift("staging.env", mock_staging_env, "production.env", mock_production_env, file_type="env")
    
    print("\n[DRIFT ANALYSIS REPORT]:")
    print(json.dumps(report, indent=2))
    print("\n---------------------------------------------------------")
    print(f"Total Keys Evaluated: {detector.total_keys_scanned}")
    print(f"Drift Anomalies Flagged: {detector.drift_anomalies_found}")
    
    if detector.drift_anomalies_found > 0:
        print("RESULT: DEPLOYMENT BLOCKED. Production is missing critical configuration keys.")
        print("Please synchronize environment variables before launching application.")
        print("---------------------------------------------------------")
        sys.exit(1)
    else:
        print("RESULT: DEPLOYMENT APPROVED. Environments are perfectly synchronized.")
        print("---------------------------------------------------------")
        sys.exit(0)
