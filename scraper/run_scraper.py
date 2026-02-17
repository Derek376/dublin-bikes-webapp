# run_scrapers.py
import os
import sys
import time
import signal
import subprocess
import threading
from typing import Optional


def stream_output(pipe, prefix: str):
    """
    Read lines from a subprocess stream and print with a prefix.
    """
    try:
        for line in iter(pipe.readline, ''):
            if not line:
                break
            print(f"[{prefix}] {line.rstrip()}")
    finally:
        pipe.close()


def start_process(script_name: str) -> subprocess.Popen:
    """
    Start a Python script as a subprocess using the current Python interpreter.
    """
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script not found: {script_path}")

    # -u enables unbuffered output for real-time logs
    proc = subprocess.Popen(
        [sys.executable, "-u", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    return proc


def terminate_process(proc: Optional[subprocess.Popen], name: str):
    """
    Gracefully terminate a subprocess, then force kill if needed.
    """
    if proc is None or proc.poll() is not None:
        return

    print(f"Stopping {name} ...")
    proc.terminate()
    try:
        proc.wait(timeout=8)
    except subprocess.TimeoutExpired:
        print(f"{name} did not stop in time, killing...")
        proc.kill()
        proc.wait(timeout=5)


def main():
    """
    Run both scrapers concurrently and keep this process alive.
    """
    jc_proc = None
    ow_proc = None

    try:
        jc_proc = start_process("scrape_jcdecaux.py")
        ow_proc = start_process("scrape_openweather.py")

        jc_thread = threading.Thread(
            target=stream_output, args=(jc_proc.stdout, "JCDECAUX"), daemon=True
        )
        ow_thread = threading.Thread(
            target=stream_output, args=(ow_proc.stdout, "OPENWEATHER"), daemon=True
        )

        jc_thread.start()
        ow_thread.start()

        print("Both scrapers started. Press Ctrl+C to stop all.")

        while True:
            # If one process exits unexpectedly, stop everything to avoid silent failure
            jc_code = jc_proc.poll()
            ow_code = ow_proc.poll()

            if jc_code is not None:
                print(f"scrape_jcdecaux.py exited with code {jc_code}. Stopping all...")
                break

            if ow_code is not None:
                print(f"scrape_openweather.py exited with code {ow_code}. Stopping all...")
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received.")
    except Exception as e:
        print(f"Error in runner: {e}")
    finally:
        terminate_process(jc_proc, "scrape_jcdecaux.py")
        terminate_process(ow_proc, "scrape_openweather.py")
        print("All scrapers stopped.")


if __name__ == "__main__":
    main()
