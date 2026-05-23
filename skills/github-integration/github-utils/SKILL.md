---
description: Imported skill github_utils from openai
name: github_utils
signature: 61c1bbe2ae217433b4b6f9f09f21aca4df52c12598068343ade719f706e4859b
source: /a0/tmp/skills_research/openai/skills/.system/skill-installer/scripts/github_utils.py
---

#!/usr/bin/env python3
"""Shared GitHub helpers for skill install scripts."""

from __future__ import annotations

import os
import urllib.request


def github_request(url: str, user_agent: str) -> bytes:
    headers = {"User-Agent": user_agent}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def github_api_contents_url(repo: str, path: str, ref: str) -> str:
    return f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
