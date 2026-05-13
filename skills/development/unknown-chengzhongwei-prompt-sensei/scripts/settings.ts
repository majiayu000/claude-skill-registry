#!/usr/bin/env node
/**
 * Manage local Prompt Sensei settings.
 *
 * Usage:
 *   settings.js
 *   settings.js auto-observe on|off
 *   settings.js auto-observe user|folder
 *   settings.js save-redacted-prompts on|off
 */

import { spawnSync } from "child_process";
import { join } from "path";
import { detectHostFromSkillRoot, hostLabel } from "./lib/host";
import {
  ensureSettings,
  loadSettings,
  saveSettings,
  setAutoObserve,
  setSaveRedactedPrompts,
} from "./lib/settings";

function onOff(value: boolean): string {
  return value ? "on" : "off";
}

function granted(value: boolean): string {
  return value ? "granted" : "not granted";
}

function printSettings(): void {
  const settings = ensureSettings();
  const host = detectHostFromSkillRoot();
  console.log("Prompt Sensei Settings");
  console.log(`- Host: ${hostLabel(host)}`);
  console.log(`- Auto observe: ${onOff(settings.autoObserve)}`);
  if (host === "codex") {
    console.log("- Codex auto-start: not supported; use `Use prompt-sensei observe mode.`");
  }
  console.log(`- Save redacted prompts: ${onOff(settings.saveRedactedPrompts)}`);
  console.log(`- Save redacted prompts consent: ${granted(settings.consent.saveRedactedPrompts.granted)}`);
  console.log(`- Observe consent: ${granted(settings.consent.observe.granted)}`);
  console.log(`- Lookback consent: ${granted(settings.consent.lookback.granted)}`);
  if (settings.consent.lookback.granted && settings.consent.lookback.scope) {
    console.log(`- Lookback scope: ${settings.consent.lookback.scope}`);
  }
  console.log("- Storage: ~/.prompt-sensei/");
}

function parseToggle(value: string | undefined): boolean | null {
  if (value === "on") return true;
  if (value === "off") return false;
  return null;
}

function usage(): void {
  console.log(`Prompt Sensei Settings

Commands:
  settings
  settings auto-observe on
  settings auto-observe off
  settings auto-observe user
  settings auto-observe folder
  settings save-redacted-prompts on
  settings save-redacted-prompts off`);
}

function runHookSetup(scope: string): void {
  const script = join(__dirname, "setup-hooks.js");
  const result = spawnSync(process.execPath, [script, "auto-observe", scope], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
  if (result.status !== 0) process.exit(result.status ?? 1);
}

function main(): void {
  const command = process.argv[2];
  const value = process.argv[3];

  if (!command || command === "show") {
    printSettings();
    return;
  }

  if (command === "help" || command === "--help") {
    usage();
    return;
  }

  if (command === "auto-observe") {
    const host = detectHostFromSkillRoot();
    if (value === "user" || value === "system" || value === "folder") {
      if (host === "codex") {
        console.log("Codex auto-start hooks are not supported.");
        console.log("Use natural language to start coaching: `Use prompt-sensei observe mode.`");
        console.log("For Claude Code hooks, run this from ~/.claude/skills/prompt-sensei.");
        process.exit(1);
      }
      runHookSetup(value);
      return;
    }

    const enabled = parseToggle(value);
    if (enabled === null) {
      usage();
      process.exit(1);
    }

    const settings = setAutoObserve(loadSettings(), enabled);
    saveSettings(settings);
    console.log(`Auto observe: ${onOff(settings.autoObserve)}`);
    if (host === "codex" && settings.autoObserve) {
      console.log("Note: Codex does not support Prompt Sensei auto-start hooks. Start with `Use prompt-sensei observe mode.`");
    }
    if (settings.autoObserve && !settings.consent.observe.granted) {
      console.log("Run `/prompt-sensei observe` once to grant observe consent before auto-start can begin.");
    }
    return;
  }

  if (command === "save-redacted-prompts") {
    const enabled = parseToggle(value);
    if (enabled === null) {
      usage();
      process.exit(1);
    }

    const settings = setSaveRedactedPrompts(loadSettings(), enabled);
    saveSettings(settings);
    console.log(`Save redacted prompts: ${onOff(settings.saveRedactedPrompts)}`);
    if (settings.saveRedactedPrompts) {
      console.log("Only redacted prompt previews are stored. Raw prompt text is never stored.");
    }
    return;
  }

  usage();
}

main();
