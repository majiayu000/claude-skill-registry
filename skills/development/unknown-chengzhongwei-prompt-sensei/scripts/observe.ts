#!/usr/bin/env node
/**
 * Record a prompt observation to the local session store.
 *
 * Usage:
 *   observe.js --init
 *   observe.js --hash-only
 *   observe.js --stage execution --score 3.8 --task-type debugging --flags missing-context,no-constraints --tip-kind name-file-or-function
 *
 * Raw prompt text is never stored. Only metadata: timestamp, stage, task type,
 * score, and lightweight flags. A SHA-256 hash of the prompt may be stored
 * if the prompt text is provided via stdin and hashing is enabled.
 *
 * Storage: ~/.prompt-sensei/events.jsonl
 */

import { appendFileSync, existsSync, writeFileSync } from "fs";
import { join } from "path";
import * as readline from "readline";
import { spawn } from "child_process";
import { DATA_DIR, EVENTS_FILE, CONFIG_FILE } from "./lib/paths";
import { hashPrompt, redactedPromptPreview } from "./lib/redact";
import {
  ensureDataDir,
  grantObserveConsent,
  hasObserveConsent,
  loadSettings,
  saveSettings,
} from "./lib/settings";
import { normalizeTipKind, selectTipKind, type TipKind } from "./lib/coaching";

const UPDATE_SCRIPT = join(__dirname, "update.js");

function parseArgs(argv: string[]): Record<string, string | boolean> {
  const result: Record<string, string | boolean> = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith("--")) {
        result[key] = next;
        i++;
      } else {
        result[key] = true;
      }
    }
  }
  return result;
}

function printInteractiveHelp(): void {
  console.log(`Prompt Sensei Observe

This command records local observation metadata. It does not start live coaching by itself.

Use one of:
  npm run init
  node dist/scripts/observe.js --init
  node dist/scripts/observe.js --stage execution --score 4 --task-type debugging --tip-kind add-verification-command

In Claude Code, start live coaching with:
  /prompt-sensei observe

In Codex, ask the agent:
  Use prompt-sensei observe mode.
`);
}

interface Config {
  v: number;
  consentGiven: boolean;
  consentAt: string;
  storeRaw?: boolean;
}

function saveConfig(config: Config): void {
  ensureDataDir();
  writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2) + "\n", "utf8");
}

interface PromptEvent {
  v: 1 | 2;
  ts: string;
  type: "session-start" | "prompt-observed" | "prompt-hashed";
  stage?: string;
  taskType?: string;
  score?: number;
  flags?: string[];
  tipKind?: TipKind;
  promptHash?: string;
  redactedPromptPreview?: string;
}

function appendEvent(event: PromptEvent): void {
  ensureDataDir();
  appendFileSync(EVENTS_FILE, JSON.stringify(event) + "\n", "utf8");
}

function runBackgroundUpdateCheck(): void {
  if (process.env["PROMPT_SENSEI_DISABLE_UPDATE_CHECK"] === "1") return;
  if (!existsSync(UPDATE_SCRIPT)) return;

  try {
    const child = spawn(process.execPath, [UPDATE_SCRIPT, "--check", "--quiet"], {
      detached: true,
      stdio: "ignore",
    });
    child.unref();
  } catch {
    // Update checks are best-effort and must never block prompt observation.
  }
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

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function promptTextFromStdin(stdinText: string): string {
  try {
    const parsed = JSON.parse(stdinText) as unknown;
    if (isRecord(parsed) && typeof parsed["prompt"] === "string") {
      return parsed["prompt"];
    }
    return "";
  } catch {
    // Plain stdin is the normal path for direct script usage.
  }
  return stdinText;
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv);

  if (process.argv.length <= 2 && process.stdin.isTTY) {
    printInteractiveHelp();
    return;
  }

  if (args["init"] === true) {
    const at = new Date().toISOString();
    const settings = grantObserveConsent(loadSettings(), at);
    saveSettings(settings);

    appendEvent({
      v: 1,
      ts: at,
      type: "session-start",
    });

    // Keep the legacy consent file for older installed script versions.
    saveConfig({
      v: 1,
      consentGiven: true,
      consentAt: settings.consent.observe.grantedAt ?? at,
    });

    console.log(`Session started. Data: ${DATA_DIR}`);
    runBackgroundUpdateCheck();
    return;
  }

  const settings = loadSettings();
  if (!hasObserveConsent(settings)) {
    process.stderr.write(
      "Prompt Sensei has not been initialized. Run `/prompt-sensei observe` and consent before recording observations.\n"
    );
    return;
  }

  runBackgroundUpdateCheck();

  const hasObservationArgs =
    args["stage"] !== undefined ||
    args["score"] !== undefined ||
    args["task-type"] !== undefined ||
    args["flags"] !== undefined ||
    args["tip-kind"] !== undefined;
  const hashOnly = args["hash-only"] === true || !hasObservationArgs;
  const stdinText = await readStdin();
  const promptText = promptTextFromStdin(stdinText);

  if (hashOnly) {
    if (!promptText.trim()) return;
    appendEvent({
      v: 1,
      ts: new Date().toISOString(),
      type: "prompt-hashed",
      promptHash: hashPrompt(promptText),
      ...(settings.saveRedactedPrompts && { redactedPromptPreview: redactedPromptPreview(promptText) }),
    });
    return;
  }

  // Record a scored prompt observation. This path is used by the skill after it
  // classifies and scores the prompt in conversation context.
  const stage = args["stage"] ? String(args["stage"]) : "unknown";
  const score = args["score"] !== undefined ? parseFloat(String(args["score"])) : undefined;
  const taskType = args["task-type"] ? String(args["task-type"]) : "other";
  const flagsRaw = args["flags"] ? String(args["flags"]) : "";
  const flags = flagsRaw ? flagsRaw.split(",").map((f) => f.trim()).filter(Boolean) : [];
  const explicitTipKind = normalizeTipKind(args["tip-kind"] ? String(args["tip-kind"]) : undefined);
  const tipKind = explicitTipKind ?? selectTipKind(flags, stage, taskType);

  if (score !== undefined && (isNaN(score) || score < 1 || score > 5)) {
    process.stderr.write("Error: --score must be between 1 and 5\n");
    process.exit(1);
  }

  appendEvent({
    v: 2,
    ts: new Date().toISOString(),
    type: "prompt-observed",
    stage,
    taskType,
    ...(score !== undefined && { score }),
    ...(flags.length > 0 && { flags }),
    ...(tipKind && { tipKind }),
    ...(promptText.trim() && { promptHash: hashPrompt(promptText) }),
    ...(promptText.trim() &&
      settings.saveRedactedPrompts && { redactedPromptPreview: redactedPromptPreview(promptText) }),
  });
  console.log("Prompt observation recorded.");
}

main().catch((err) => {
  process.stderr.write(`observe error: ${err}\n`);
  process.exit(1);
});
