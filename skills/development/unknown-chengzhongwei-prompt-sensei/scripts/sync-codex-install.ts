#!/usr/bin/env node
/**
 * Sync this Prompt Sensei install into the Codex skill directory.
 *
 * Usage:
 *   sync-codex-install.js [--dry-run]
 */

import { existsSync, mkdirSync, rmSync, cpSync } from "fs";
import { homedir } from "os";
import { basename, join } from "path";
import { spawnSync } from "child_process";
import { SKILL_ROOT } from "./lib/host";

const CODEX_SKILL_ROOT = join(homedir(), ".codex", "skills", "prompt-sensei");
const EXCLUDED = new Set(["node_modules", "dist", ".git"]);

function copyInstall(source: string, target: string): void {
  mkdirSync(target, { recursive: true });

  for (const entry of ["SKILL.md", "README.md", "README-zh.md", "LICENSE", "package.json", "package-lock.json", "tsconfig.json"]) {
    const sourcePath = join(source, entry);
    if (existsSync(sourcePath)) cpSync(sourcePath, join(target, entry), { recursive: true });
  }

  for (const dir of ["scripts", "docs", "examples", "eval"]) {
    const sourcePath = join(source, dir);
    const targetPath = join(target, dir);
    if (!existsSync(sourcePath)) continue;
    if (existsSync(targetPath)) rmSync(targetPath, { recursive: true, force: true });
    cpSync(sourcePath, targetPath, {
      recursive: true,
      filter: (path) => !EXCLUDED.has(basename(path)),
    });
  }
}

function runStep(command: string, args: string[], cwd: string): void {
  const result = spawnSync(command, args, {
    cwd,
    stdio: "inherit",
  });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

function main(): void {
  const dryRun = process.argv.includes("--dry-run");

  console.log(`Source: ${SKILL_ROOT}`);
  console.log(`Target: ${CODEX_SKILL_ROOT}`);

  if (dryRun) {
    console.log("Dry run only. No files changed.");
    return;
  }

  copyInstall(SKILL_ROOT, CODEX_SKILL_ROOT);
  runStep("npm", ["install"], CODEX_SKILL_ROOT);
  runStep("npm", ["run", "build"], CODEX_SKILL_ROOT);
  console.log("Codex Prompt Sensei install synced.");
}

main();
