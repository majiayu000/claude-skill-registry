#!/usr/bin/env node
/**
 * Claude Code PreCompact hook support for compact-safe coaching continuity.
 */

import { appendFileSync } from "fs";
import * as readline from "readline";
import { EVENTS_FILE } from "./lib/paths";
import { ensureDataDir, hasObserveConsent, loadSettings } from "./lib/settings";

interface CompactEvent {
  v: 1;
  ts: string;
  type: "session-compacted";
  autoObserve: boolean;
  observeConsent: boolean;
}

async function readStdin(): Promise<string> {
  if (process.stdin.isTTY) return "";
  const rl = readline.createInterface({ input: process.stdin });
  const lines: string[] = [];
  for await (const line of rl) {
    lines.push(line);
  }
  return lines.join("\n");
}

function appendEvent(event: CompactEvent): void {
  ensureDataDir();
  appendFileSync(EVENTS_FILE, JSON.stringify(event) + "\n", "utf8");
}

async function main(): Promise<void> {
  await readStdin();
  const settings = loadSettings();
  if (!settings.autoObserve || !hasObserveConsent(settings)) {
    return;
  }

  appendEvent({
    v: 1,
    ts: new Date().toISOString(),
    type: "session-compacted",
    autoObserve: settings.autoObserve,
    observeConsent: settings.consent.observe.granted,
  });

  console.log(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PreCompact",
      additionalContext:
        "Prompt Sensei was active before compaction. Continue stage-aware prompt coaching if the user consented. Keep feedback short and avoid scoring trivial acknowledgements.",
    },
  }));
}

main().catch((err) => {
  process.stderr.write(`pre-compact error: ${err instanceof Error ? err.message : String(err)}\n`);
  process.exit(1);
});
