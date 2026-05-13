#!/usr/bin/env node
/**
 * Delete local Prompt Sensei data.
 * Usage: clear.js [--force] [--all]
 *
 * --force   Skip confirmation prompt
 * --all     Also delete config.json and settings.json (resets consent/settings)
 */

import { existsSync, unlinkSync, readFileSync, rmSync } from "fs";
import * as readline from "readline";
import { CONFIG_FILE, EVENTS_FILE, REPORTS_DIR, SETTINGS_FILE, UPDATE_FILE } from "./lib/paths";

function countEntries(): number {
  if (!existsSync(EVENTS_FILE)) return 0;
  return readFileSync(EVENTS_FILE, "utf8")
    .split("\n")
    .filter((l) => l.trim() && l.includes("prompt-observed")).length;
}

function deleteData(all: boolean): void {
  let deleted = 0;

  if (existsSync(EVENTS_FILE)) {
    unlinkSync(EVENTS_FILE);
    deleted++;
    console.log(`Deleted: ${EVENTS_FILE}`);
  }

  if (existsSync(UPDATE_FILE)) {
    unlinkSync(UPDATE_FILE);
    deleted++;
    console.log(`Deleted: ${UPDATE_FILE}`);
  }

  if (existsSync(REPORTS_DIR)) {
    rmSync(REPORTS_DIR, { recursive: true, force: true });
    deleted++;
    console.log(`Deleted: ${REPORTS_DIR}`);
  }

  const resetConsent = all && (existsSync(CONFIG_FILE) || existsSync(SETTINGS_FILE));

  if (all && existsSync(CONFIG_FILE)) {
    unlinkSync(CONFIG_FILE);
    deleted++;
    console.log(`Deleted: ${CONFIG_FILE}`);
  }

  if (all && existsSync(SETTINGS_FILE)) {
    unlinkSync(SETTINGS_FILE);
    deleted++;
    console.log(`Deleted: ${SETTINGS_FILE}`);
  }

  if (resetConsent) {
    console.log("Consent and settings reset. Prompt Sensei will ask for consent again on next use.");
  }

  if (deleted === 0) {
    console.log("Nothing to delete — no data found.");
  } else {
    console.log("Done. Fresh start.");
  }
}

async function confirm(question: string): Promise<boolean> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === "y");
    });
  });
}

async function main(): Promise<void> {
  const force = process.argv.includes("--force");
  const all = process.argv.includes("--all");

  const entries = countEntries();

  if (
    entries === 0 &&
    !existsSync(CONFIG_FILE) &&
    !existsSync(SETTINGS_FILE) &&
    !existsSync(UPDATE_FILE) &&
    !existsSync(REPORTS_DIR)
  ) {
    console.log("Nothing to clear — no session data found.");
    return;
  }

  if (force) {
    deleteData(all);
    return;
  }

  const what = all
    ? "events, update cache, saved reports, config, and settings (resets consent/settings)"
    : "events, update cache, and saved reports";
  const ok = await confirm(
    `Delete ${entries} prompt entries (${what})? [y/N] `
  );

  if (ok) {
    deleteData(all);
  } else {
    console.log("Aborted. Data preserved.");
  }
}

main().catch((err) => {
  process.stderr.write(`clear error: ${err}\n`);
  process.exit(1);
});
