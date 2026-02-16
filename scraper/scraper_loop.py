import time
import traceback
from scrape_once import main as scrape_once_main

def run_loop(interval_seconds=300):
    while True:
        try:
            scrape_once_main()
        except Exception:
            print("Scrape failed:")
            print(traceback.format_exc())
        finally:
            time.sleep(interval_seconds)

if __name__ == "__main__":
    run_loop(300) 
