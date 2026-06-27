#!/usr/bin/env python3
"""DingTalk Stream Bot — bridges DingTalk group chat to Claude Code CLI.

Receives @mentions in group, executes via `claude -p`, replies with result.

Features:
  - 20s keepalive ping (prevents DingTalk 30-min WebSocket timeout)
  - Exponential backoff on crash (5s -> 60s)
  - Webhook + OpenAPI dual reply path
  - Threaded execution (non-blocking)

Run:
  python3 -m dingtalk_bridge.src.stream_bot
  # or
  python3 stream_bot.py
"""

import asyncio
import json
import os
import subprocess
import sys
import threading
import time
import types
from pathlib import Path

# Allow running standalone or as module
try:
    from . import config
    from .send import save_conv_info, send_markdown, reply_via_webhook
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import config
    from send import save_conv_info, send_markdown, reply_via_webhook

import dingtalk_stream
from dingtalk_stream import AckMessage


def reply(webhook_url, title, content):
    try:
        if webhook_url:
            reply_via_webhook(webhook_url, title, content)
        else:
            send_markdown(title, content)
    except Exception:
        try:
            send_markdown(title, content)
        except Exception as e2:
            print(f"[Bot] Reply failed: {e2}", flush=True)


def execute_prompt(prompt, webhook_url):
    claude_bin = config.claude_bin()
    workdir = config.workdir()
    max_len = config.max_reply_len()

    try:
        print(f"[Bot] Executing: {prompt[:80]}...", flush=True)
        reply(webhook_url, "Executing", f"Processing: **{prompt[:100]}**\n\nPlease wait...")

        result = subprocess.run(
            [
                claude_bin, "-p", prompt,
                "--continue",
                "--output-format", "text",
                "--dangerously-skip-permissions",
            ],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=workdir,
            env=os.environ,
        )

        output = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode == 0 and output:
            if len(output) > max_len:
                output = output[:max_len] + "\n\n... (truncated)"
            send_markdown("Done", f"**Prompt:** {prompt[:100]}\n\n---\n\n{output}")
        else:
            error_info = stderr[:1000] if stderr else "(no error output)"
            send_markdown("Failed", f"**Prompt:** {prompt[:100]}\n\nExit: {result.returncode}\n\n{error_info}")

        print(f"[Bot] Done (exit={result.returncode})", flush=True)

    except subprocess.TimeoutExpired:
        send_markdown("Timeout", f"Exceeded 5 minutes.\n\n**Prompt:** {prompt[:100]}")
    except Exception as e:
        print(f"[Bot] Exec error: {e}", flush=True)
        try:
            send_markdown("Error", f"**Prompt:** {prompt[:100]}\n\n**Error:** {e}")
        except Exception:
            pass


class BridgeHandler(dingtalk_stream.ChatbotHandler):

    async def process(self, callback):
        try:
            data = callback.data
            text = data.get("text", {}).get("content", "").strip()
            conversation_id = data.get("conversationId", "")
            robot_code = data.get("robotCode", "")
            webhook_url = data.get("sessionWebhook", "")

            print(f"[Bot] Received: '{text[:80]}' (conv={conversation_id[:16]}...)", flush=True)

            if conversation_id and robot_code:
                save_conv_info(conversation_id, robot_code)

            if not text:
                return AckMessage.STATUS_OK, "OK"

            threading.Thread(
                target=execute_prompt,
                args=(text, webhook_url),
                daemon=True,
            ).start()

        except Exception as e:
            print(f"[Bot] Handler error: {e}", flush=True)

        return AckMessage.STATUS_OK, "OK"


def _make_client():
    credential = dingtalk_stream.Credential(config.app_key(), config.app_secret())
    client = dingtalk_stream.DingTalkStreamClient(credential)

    keepalive_sec = config.keepalive_interval()
    try:
        import websockets
        async def _keepalive(self, ws, ping_interval=keepalive_sec):
            while True:
                await asyncio.sleep(ping_interval)
                try:
                    await ws.ping()
                except websockets.exceptions.ConnectionClosed:
                    break
        client.keepalive = types.MethodType(_keepalive, client)
    except ImportError:
        pass

    client.register_callback_handler(
        dingtalk_stream.chatbot.ChatbotMessage.TOPIC,
        BridgeHandler(),
    )
    return client


def main():
    workdir = config.workdir()
    os.chdir(workdir)

    print(f"[DingTalk Bridge] Bot starting", flush=True)
    print(f"[DingTalk Bridge] PID: {os.getpid()}", flush=True)
    print(f"[DingTalk Bridge] CWD: {workdir}", flush=True)
    print(f"[DingTalk Bridge] APP_KEY: {config.app_key()[:10]}...", flush=True)
    print(f"[DingTalk Bridge] Keepalive: {config.keepalive_interval()}s", flush=True)

    backoff = 5
    while True:
        try:
            _make_client().start_forever()
        except (KeyboardInterrupt, SystemExit):
            print("[DingTalk Bridge] Shutting down", flush=True)
            break
        except BaseException as e:
            print(f"[DingTalk Bridge] Crashed: {type(e).__name__}: {e}, retry in {backoff}s...", flush=True)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)
        else:
            backoff = 5


if __name__ == "__main__":
    main()
