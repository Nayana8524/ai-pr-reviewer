# static_analysis.py
import subprocess

def run_flake8(filepath):
    result = subprocess.run(
        ["flake8", filepath, "--max-line-length=100"],
        capture_output=True, text=True
    )
    return result.stdout

def run_static_checks(changed_files):
    """changed_files: list of filenames from GitHub API"""
    report = {}
    for f in changed_files:
        if f.endswith(".py"):
            report[f] = run_flake8(f)
    return report