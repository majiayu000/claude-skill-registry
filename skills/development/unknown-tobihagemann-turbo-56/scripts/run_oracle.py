#!/usr/bin/env python3
"""Run the oracle CLI with configuration from ~/.turbo/config.json.

Configuration:
  oracle.chatgptUrl  ChatGPT URL (default: https://chatgpt.com/)

Usage: python3 scripts/run_oracle.py --prompt "<question>" --file <files...>

All arguments are forwarded to the oracle CLI. --engine, --browser-inline-cookies-file,
and --chatgpt-url are set automatically and should not be passed manually.
"""

import json, os, sys, subprocess


def load_config():
    """Load ~/.turbo/config.json and return the oracle section."""
    config_path = os.path.expanduser('~/.turbo/config.json')
    if not os.path.isfile(config_path):
        return {}
    with open(config_path) as f:
        return json.load(f).get('oracle', {})


config = load_config()

chatgpt_url = config.get('chatgptUrl', 'https://chatgpt.com/')
cookies_path = os.path.expanduser('~/.oracle/cookies.json')

cmd = [
    'npx', '-y', '@steipete/oracle',
    '--engine', 'browser',
    '--browser-inline-cookies-file', cookies_path,
    '--chatgpt-url', chatgpt_url,
    *sys.argv[1:],
]

sys.exit(subprocess.call(cmd))
