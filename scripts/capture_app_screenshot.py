"""
Script to capture actual high-resolution screenshots of the running Streamlit app.
ConnectTel / Persevex AI Internship Project - Phase 7.3.
"""

import os
import subprocess
import time
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = ROOT / "outputs" / "app_screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BROWSER_BIN = CHROME_PATH if os.path.exists(CHROME_PATH) else EDGE_PATH

def capture_screenshot(port=8504, output_filename="01_connecttel_app_overview.png"):
    print(f"Starting Streamlit on port {port}...")
    proc = subprocess.Popen(
        [
            "python", "-m", "streamlit", "run",
            str(ROOT / "app.py"),
            f"--server.port={port}",
            "--server.headless=true"
        ],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    health_url = f"http://localhost:{port}/_stcore/health"
    app_url = f"http://localhost:{port}"
    output_path = SCREENSHOTS_DIR / output_filename

    try:
        # Wait up to 12 seconds for startup
        started = False
        for attempt in range(12):
            time.sleep(1)
            try:
                with urllib.request.urlopen(health_url, timeout=2) as resp:
                    if resp.status == 200:
                        print("Streamlit server is ready!")
                        started = True
                        break
            except Exception:
                pass

        if not started:
            raise RuntimeError("Streamlit failed to start within timeout.")

        # Give extra time for React/Streamlit client components to render
        time.sleep(4)

        print(f"Capturing screenshot using {BROWSER_BIN}...")
        cmd = [
            BROWSER_BIN,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--window-size=1400,1050",
            "--virtual-time-budget=7000",
            "--run-all-compositor-stages-before-draw",
            f"--screenshot={str(output_path)}",
            app_url
        ]
        res = subprocess.run(cmd, capture_output=True, timeout=15)
        print(f"Browser return code: {res.returncode}")

        if output_path.exists() and output_path.stat().st_size > 1000:
            print(f"Screenshot successfully captured: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
            with Image.open(output_path) as img:
                print(f"Image dimensions: {img.size}")
        else:
            raise FileNotFoundError(f"Failed to generate valid screenshot at {output_path}")

    finally:
        print("Stopping Streamlit server...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()

if __name__ == "__main__":
    capture_screenshot()
