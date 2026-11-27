"""
Streamlit Startup and Health Check Probe.
Spins up Streamlit app.py on a local port, verifies HTTP 200 on /_stcore/health,
and shuts down the process.
"""

import sys
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\Nisha\.gemini\antigravity\scratch\predictive-customer-churn-telecom")

def test_startup():
    port = 8503
    print(f"Launching Streamlit on port {port}...")
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m", "streamlit", "run",
            str(ROOT / "app.py"),
            f"--server.port={port}",
            "--server.headless=true"
        ],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    health_url = f"http://localhost:{port}/_stcore/health"
    success = False
    
    try:
        # Wait up to 10 seconds for startup
        for attempt in range(10):
            time.sleep(1)
            try:
                with urllib.request.urlopen(health_url, timeout=2) as response:
                    if response.status == 200:
                        print(f"Health check passed! Status code: {response.status}")
                        success = True
                        break
            except Exception as e:
                print(f"Attempt {attempt + 1}: Waiting for server... ({e})")
                
    finally:
        print("Terminating Streamlit process...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            
    if success:
        print("STREAMLIT STARTUP & HEALTH CHECK: PASSED")
    else:
        print("STREAMLIT STARTUP & HEALTH CHECK: FAILED")
        sys.exit(1)

if __name__ == "__main__":
    test_startup()
