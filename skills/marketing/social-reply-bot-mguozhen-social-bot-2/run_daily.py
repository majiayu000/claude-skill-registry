#!/usr/bin/env python3
"""
Daily social media reply bot.
Scheduled via macOS LaunchAgent at 10:05 AM.
Runs standalone — no Claude Code, no confirmation prompts.

Usage:
    python run_daily.py              # run both platforms
    python run_daily.py --x-only
    python run_daily.py --reddit-only
"""
import sys
import json
import logging
import time
import argparse
from pathlib import Path
from datetime import datetime

# Load env vars from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

# Setup logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"run_{datetime.now():%Y-%m-%d}.log"),
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger("main")

# Import bot modules
sys.path.insert(0, str(Path(__file__).parent))
from bot.db import init_db
from bot import x_bot, reddit_bot

CONFIG = json.loads((Path(__file__).parent / "config.json").read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--x-only",      action="store_true")
    parser.add_argument("--reddit-only", action="store_true")
    args = parser.parse_args()

    run_x      = not args.reddit_only
    run_reddit = not args.x_only

    init_db()
    start = time.time()
    results = {}

    logger.info("=" * 60)
    logger.info(f"Daily bot started — {datetime.now():%Y-%m-%d %H:%M}")
    logger.info("=" * 60)

    # ── X/Twitter ──────────────────────────────────────────────
    if run_x:
        logger.info("Starting X/Twitter run...")
        try:
            results["x"] = x_bot.run(CONFIG["x"])
            logger.info(f"X done: {results['x']}")
        except Exception as e:
            logger.error(f"X run failed: {e}", exc_info=True)
            results["x"] = {"error": str(e)}

    # ── Reddit ─────────────────────────────────────────────────
    if run_reddit:
        logger.info("Starting Reddit run...")
        try:
            results["reddit"] = reddit_bot.run(CONFIG["reddit"])
            logger.info(f"Reddit done: {results['reddit']}")
        except Exception as e:
            logger.error(f"Reddit run failed: {e}", exc_info=True)
            results["reddit"] = {"error": str(e)}

    elapsed = int(time.time() - start)
    logger.info(f"All done in {elapsed}s — {results}")

    # Write today's summary for dashboard
    summary_file = LOG_DIR / f"summary_{datetime.now():%Y-%m-%d}.json"
    import json as _json
    summary_file.write_text(_json.dumps({
        "date": datetime.now().isoformat(),
        "elapsed_secs": elapsed,
        "results": results,
    }, indent=2))


if __name__ == "__main__":
    main()
