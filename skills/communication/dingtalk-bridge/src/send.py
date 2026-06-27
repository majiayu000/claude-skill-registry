#!/usr/bin/env python3
"""DingTalk group messaging via OpenAPI.

Usage as CLI:
  python3 send.py "Markdown message"
  python3 send.py --title "Title" "Markdown message"
  python3 send.py --text "Plain text message"

Usage as module:
  from dingtalk_bridge.src.send import send_markdown, send_text, save_conv_info
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

# Allow running standalone or as module
try:
    from . import config
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import config


def _get_access_token():
    payload = json.dumps({
        "appKey": config.app_key(),
        "appSecret": config.app_secret(),
    }).encode()
    req = urllib.request.Request(
        "https://api.dingtalk.com/v1.0/oauth2/accessToken",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
    return resp["accessToken"]


def _get_conv_info():
    conv_path = config.conv_file()
    if not conv_path.exists():
        raise FileNotFoundError(
            f"No conversation file at {conv_path}. "
            "Send a message to the bot in a DingTalk group first "
            "so it can auto-save the conversation ID."
        )
    return json.loads(conv_path.read_text())


def save_conv_info(open_conversation_id, robot_code):
    conv_path = config.conv_file()
    conv_path.parent.mkdir(parents=True, exist_ok=True)
    data = {"openConversationId": open_conversation_id, "robotCode": robot_code}
    conv_path.write_text(json.dumps(data, indent=2))
    print(f"[DingTalk] Conv info saved: {conv_path}")


def send_markdown(title, text):
    conv = _get_conv_info()
    token = _get_access_token()
    payload = json.dumps({
        "robotCode": conv["robotCode"],
        "openConversationId": conv["openConversationId"],
        "msgKey": "sampleMarkdown",
        "msgParam": json.dumps({"title": title, "text": text}),
    }).encode()
    req = urllib.request.Request(
        "https://api.dingtalk.com/v1.0/robot/groupMessages/send",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-acs-dingtalk-access-token": token,
        },
    )
    return json.loads(urllib.request.urlopen(req, timeout=10).read())


def send_text(text):
    conv = _get_conv_info()
    token = _get_access_token()
    payload = json.dumps({
        "robotCode": conv["robotCode"],
        "openConversationId": conv["openConversationId"],
        "msgKey": "sampleText",
        "msgParam": json.dumps({"content": text}),
    }).encode()
    req = urllib.request.Request(
        "https://api.dingtalk.com/v1.0/robot/groupMessages/send",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-acs-dingtalk-access-token": token,
        },
    )
    return json.loads(urllib.request.urlopen(req, timeout=10).read())


def reply_via_webhook(webhook_url, title, content):
    payload = json.dumps({
        "msgtype": "markdown",
        "markdown": {"title": title, "text": content},
    }).encode()
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(req, timeout=10)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Send message to DingTalk group")
    parser.add_argument("message", nargs="*")
    parser.add_argument("--title", default="Notification")
    parser.add_argument("--text", action="store_true", help="Send as plain text instead of markdown")
    args = parser.parse_args()
    msg = " ".join(args.message) if args.message else "(empty)"
    if args.text:
        send_text(msg)
    else:
        send_markdown(args.title, msg)
    print("Sent.")
