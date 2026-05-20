# 🧭 Environment Drift Detector

A zero-dependency DevSecOps alignment engine designed to prevent deployment crashes caused by "Configuration Drift."

This framework cross-references environment files (`.env`, `config.json`) across distinct deployment stages (e.g., Staging vs. Production). It mathematically proves that a target environment possesses all the required configuration keys mapped in the source of truth, blocking the CI/CD pipeline if critical variables are missing.

---

## 💡 System Blueprint: The Three Ws

### 1. WHEN to use this tool?
*   **Pre-Deployment CI Gates:** Run this script strictly before container orchestration triggers. If a developer added a new `STRIPE_API_KEY` to Staging but forgot to add it to the Production secrets manager, this tool halts the deployment before the live app crashes.
*   **Routine Infrastructure Audits:** Run as a cron job to verify that Disaster Recovery (DR) environments have not drifted away from live Production environments.

### 2. WHERE does it run?
*   **Any Automated Runner:** Written in pure, dependency-free Python, this framework executes in milliseconds on GitHub Actions, GitLab CI runners, AWS CodeBuild, or a local developer's Mac/Linux terminal.

### 3. WHY use this over other solutions?
*   **Zero Integration Friction:** It doesn't require complex Terraform state tracking or HashiCorp Vault integrations to do its job. It simply reads text buffers and parses tree logic natively, making it a perfect drop-in guardrail for legacy systems transitioning to CI/CD.

---

## ✨ Architectural Differentiators (Why This Stands Out)

*   **Value-Agnostic Comparison:** The engine compares the *existence* of keys, not the values. It understands that `DB_PASSWORD` will correctly be different in Staging vs. Production, but it enforces that the key *must exist* in both.
*   **Multi-Format Parsing:** Supports both standard line-delimited `.env` structures and nested `.json` deployment matrices out of the box.

---

## 📋 Prerequisites

*   **Runtime Core:** Standard Python 3.8 or higher.
*   **Dependencies:** None. Engineered using core Python (`json`, `os`, `sys`) to ensure it runs on highly restricted, minimal deployment nodes without requiring `pip install`.

---

## 🔧 Tailoring to Your Infrastructure

The script is built to accommodate different configuration formats. You can expand the `file_type` parameter inside `drift_analyzer.py` if your team uses YAML for configurations:

```python
# The engine accepts file_type toggles
detector.analyze_drift("source.env", source_data, "target.env", target_data, file_type="env")
# Or for JSON architectures:
detector.analyze_drift("source.json", source_data, "target.json", target_data, file_type="json")
