"""
Capture high-fidelity Streamlit screenshots via Chrome DevTools Protocol (CDP).
Uses Python's standard library + websockets to wait for the DOM to fully render.
"""

import asyncio
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path
import websockets
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = ROOT / "outputs" / "app_screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BROWSER_BIN = CHROME_PATH if os.path.exists(CHROME_PATH) else EDGE_PATH


async def capture_cdp_screenshot(app_port=8504, cdp_port=9222, output_filename="01_connecttel_app_overview.png"):
    output_path = SCREENSHOTS_DIR / output_filename
    
    # 1. Start Streamlit
    print(f"Starting Streamlit on port {app_port}...")
    st_proc = subprocess.Popen(
        [
            "python", "-m", "streamlit", "run",
            str(ROOT / "app.py"),
            f"--server.port={app_port}",
            "--server.headless=true"
        ],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 2. Start Chrome in headless mode with remote debugging
    chrome_proc = None
    try:
        # Wait for Streamlit server health
        health_url = f"http://localhost:{app_port}/_stcore/health"
        for _ in range(12):
            time.sleep(1)
            try:
                with urllib.request.urlopen(health_url, timeout=2) as resp:
                    if resp.status == 200:
                        print("Streamlit server is ready!")
                        break
            except Exception:
                pass

        print(f"Starting Chrome with remote debugging port {cdp_port}...")
        chrome_proc = subprocess.Popen(
            [
                BROWSER_BIN,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                f"--remote-debugging-port={cdp_port}",
                f"--window-size=1440,1100",
                f"http://localhost:{app_port}"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Wait for CDP endpoint
        cdp_json_url = f"http://localhost:{cdp_port}/json"
        ws_url = None
        for _ in range(10):
            time.sleep(1)
            try:
                with urllib.request.urlopen(cdp_json_url, timeout=2) as resp:
                    tabs = json.loads(resp.read().decode())
                    if tabs:
                        ws_url = tabs[0]["webSocketDebuggerUrl"]
                        print(f"Found CDP WebSocket: {ws_url}")
                        break
            except Exception:
                pass

        if not ws_url:
            raise RuntimeError("Could not connect to Chrome CDP WebSocket endpoint.")

        # Connect to CDP WebSocket
        async with websockets.connect(ws_url) as ws:
            msg_id = 1

            async def send_cmd(method, params=None):
                nonlocal msg_id
                cid = msg_id
                msg_id += 1
                msg = {"id": cid, "method": method, "params": params or {}}
                await ws.send(json.dumps(msg))
                while True:
                    resp_str = await ws.recv()
                    resp_obj = json.loads(resp_str)
                    if resp_obj.get("id") == cid:
                        return resp_obj.get("result", {})

            await send_cmd("Page.enable")
            await send_cmd("Runtime.enable")

            # Wait until Streamlit renders .main-header and .result-banner-churn
            print("Waiting for Streamlit DOM elements to render...")
            rendered = False
            for attempt in range(20):
                await asyncio.sleep(1.0)
                eval_res = await send_cmd("Runtime.evaluate", {
                    "expression": "document.querySelector('.result-banner-churn') !== null || document.querySelector('.result-banner-retain') !== null"
                })
                val = eval_res.get("result", {}).get("value")
                if val:
                    print(f"DOM elements rendered successfully on attempt {attempt+1}!")
                    rendered = True
                    break

            if not rendered:
                print("Warning: Timeout waiting for specific result banner, proceeding with capture...")

            # Wait an extra 2 seconds for visual animations/gauges to stabilize
            await asyncio.sleep(2.0)

            # Capture screenshot 1 (Default High-Risk Profile)
            print("Capturing full page screenshot 1 via CDP...")
            shot_res = await send_cmd("Page.captureScreenshot", {
                "format": "png",
                "quality": 100,
                "captureBeyondViewport": False
            })
            b64_data = shot_res.get("data")
            import base64
            img_bytes = base64.b64decode(b64_data)
            output_path.write_bytes(img_bytes)
            print(f"Screenshot 1 saved: {output_path} ({len(img_bytes)/1024:.1f} KB)")

            # Click the "🛡️ Loyal Long-Term Subscriber" button
            print("Clicking '🛡️ Loyal Long-Term Subscriber' preset button...")
            await send_cmd("Runtime.evaluate", {
                "expression": """
                (() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const loyalBtn = buttons.find(b => b.innerText.includes('Loyal Long-Term'));
                    if (loyalBtn) {
                        loyalBtn.click();
                        return true;
                    }
                    return false;
                })()
                """
            })

            # Wait 3 seconds for Streamlit to rerun and display RETAINED SUBSCRIBER banner
            print("Waiting for Retained Subscriber banner to render...")
            for _ in range(10):
                await asyncio.sleep(1.0)
                eval_res = await send_cmd("Runtime.evaluate", {
                    "expression": "document.querySelector('.result-banner-retain') !== null"
                })
                if eval_res.get("result", {}).get("value"):
                    print("Retained banner rendered!")
                    break

            await asyncio.sleep(1.5)

            # Capture screenshot 2 (Loyal Subscriber Profile)
            output_path_2 = SCREENSHOTS_DIR / "02_connecttel_app_loyal_profile.png"
            shot_res_2 = await send_cmd("Page.captureScreenshot", {
                "format": "png",
                "quality": 100,
                "captureBeyondViewport": False
            })
            b64_data_2 = shot_res_2.get("data")
            img_bytes_2 = base64.b64decode(b64_data_2)
            output_path_2.write_bytes(img_bytes_2)
            print(f"Screenshot 2 saved: {output_path_2} ({len(img_bytes_2)/1024:.1f} KB)")

    finally:
        if chrome_proc:
            print("Terminating Chrome...")
            chrome_proc.terminate()
            try:
                chrome_proc.wait(timeout=2)
            except Exception:
                chrome_proc.kill()

        if st_proc:
            print("Terminating Streamlit...")
            st_proc.terminate()
            try:
                st_proc.wait(timeout=2)
            except Exception:
                st_proc.kill()


if __name__ == "__main__":
    asyncio.run(capture_cdp_screenshot())
