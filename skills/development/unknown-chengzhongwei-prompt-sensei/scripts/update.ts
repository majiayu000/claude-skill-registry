#!/usr/bin/env node
/**
 * Check for and apply Prompt Sensei updates.
 *
 * Usage:
 *   update.js --check [--quiet] [--force]
 *   update.js --apply
 *
 * The check path is networked and cached. It compares the local git HEAD to the
 * remote HEAD for the current branch and stores the result in
 * ~/.prompt-sensei/update-check.json.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { homedir } from "os";
import { join, resolve } from "path";
import { execFileSync, spawnSync } from "child_process";

const DATA_DIR = join(homedir(), ".prompt-sensei");
const UPDATE_FILE = join(DATA_DIR, "update-check.json");
const CHECK_INTERVAL_MS = 24 * 60 * 60 * 1000;

// dist/scripts/update.js -> skill root
const SKILL_ROOT = resolve(__dirname, "..", "..");

interface UpdateState {
  v: 1;
  checkedAt: string;
  status: "up-to-date" | "update-available" | "unknown";
  branch?: string;
  currentSha?: string;
  remoteSha?: string;
  message?: string;
}

function ensureDataDir(): void {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }
}

function parseArgs(argv: string[]): Record<string, boolean> {
  const result: Record<string, boolean> = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      result[arg.slice(2)] = true;
    }
  }
  return result;
}

function git(args: string[]): string {
  return execFileSync("git", ["-C", SKILL_ROOT, ...args], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  }).trim();
}

function loadState(): UpdateState | null {
  if (!existsSync(UPDATE_FILE)) return null;
  try {
    return JSON.parse(readFileSync(UPDATE_FILE, "utf8")) as UpdateState;
  } catch {
    return null;
  }
}

function saveState(state: UpdateState): void {
  ensureDataDir();
  writeFileSync(UPDATE_FILE, JSON.stringify(state, null, 2) + "\n", "utf8");
}

function shouldUseCachedState(force: boolean): boolean {
  if (force) return false;
  const state = loadState();
  if (!state) return false;
  const checkedAt = new Date(state.checkedAt).getTime();
  return Number.isFinite(checkedAt) && Date.now() - checkedAt < CHECK_INTERVAL_MS;
}

function isGitInstall(): boolean {
  try {
    return git(["rev-parse", "--is-inside-work-tree"]) === "true";
  } catch {
    return false;
  }
}

function currentBranch(): string {
  return git(["rev-parse", "--abbrev-ref", "HEAD"]);
}

function checkForUpdate(force: boolean, quiet: boolean): UpdateState {
  if (shouldUseCachedState(force)) {
    const state = loadState()!;
    if (!quiet) printState(state);
    return state;
  }

  if (!isGitInstall()) {
    const state: UpdateState = {
      v: 1,
      checkedAt: new Date().toISOString(),
      status: "unknown",
      message: "Prompt Sensei is not installed from a git checkout, so update checks are unavailable.",
    };
    saveState(state);
    if (!quiet) printState(state);
    return state;
  }

  try {
    const branch = currentBranch();
    const currentSha = git(["rev-parse", "HEAD"]);
    const remoteLine = git(["ls-remote", "origin", `refs/heads/${branch}`]);
    const remoteSha = remoteLine.split(/\s+/)[0];

    const state: UpdateState = {
      v: 1,
      checkedAt: new Date().toISOString(),
      status: remoteSha && remoteSha !== currentSha ? "update-available" : "up-to-date",
      branch,
      currentSha,
      remoteSha,
    };
    saveState(state);
    if (!quiet) printState(state);
    return state;
  } catch (err) {
    const state: UpdateState = {
      v: 1,
      checkedAt: new Date().toISOString(),
      status: "unknown",
      message: err instanceof Error ? err.message : String(err),
    };
    saveState(state);
    if (!quiet) printState(state);
    return state;
  }
}

function printState(state: UpdateState): void {
  if (state.status === "update-available") {
    console.log(`# Prompt Sensei Update\n\nUpdate available on \`${state.branch}\`.`);
    console.log(`Local:  ${state.currentSha?.slice(0, 7)}`);
    console.log(`Remote: ${state.remoteSha?.slice(0, 7)}`);
    console.log("\nRun `/prompt-sensei update` to update.");
    return;
  }

  if (state.status === "up-to-date") {
    console.log("Prompt Sensei is up to date.");
    return;
  }

  console.log("Prompt Sensei update status is unknown.");
  if (state.message) {
    console.log(state.message);
  }
}

function runStep(command: string, args: string[]): void {
  console.log(`$ ${[command, ...args].join(" ")}`);
  const result = spawnSync(command, args, {
    cwd: SKILL_ROOT,
    stdio: "inherit",
  });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

function applyUpdate(): void {
  if (!isGitInstall()) {
    process.stderr.write("Prompt Sensei is not installed from a git checkout; update is unavailable.\n");
    process.exit(1);
  }

  const status = git(["status", "--porcelain"]);
  if (status.trim()) {
    process.stderr.write(
      "Working tree has local changes. Commit, stash, or discard them before running `/prompt-sensei update`.\n"
    );
    process.exit(1);
  }

  const branch = currentBranch();
  runStep("git", ["pull", "--ff-only", "origin", branch]);
  runStep("npm", ["install"]);
  runStep("npm", ["run", "build"]);
  checkForUpdate(true, false);
}

function main(): void {
  const args = parseArgs(process.argv);

  if (args["apply"] || args["update"]) {
    applyUpdate();
    return;
  }

  checkForUpdate(Boolean(args["force"]), Boolean(args["quiet"]));
}

main();
