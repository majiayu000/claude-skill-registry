#!/usr/bin/env node
/**
 * Print calibration fixtures for reviewing Prompt Sensei behavior.
 *
 * This does not score prompts locally. Live scoring is produced by the host AI
 * following SKILL.md, so this script gives maintainers a consistent eval set
 * to compare against.
 */

import { existsSync, readFileSync } from "fs";
import { join } from "path";

interface EvalCase {
  id: string;
  category: string;
  prompt: string;
  expectedStage: string;
  acceptableStages?: string[];
  expectedScoreBand: string;
  expectedFlags: string[];
  expectedTipKinds?: string[];
  badTipKinds?: string[];
  expectedTipTheme: string;
  notes?: string;
}

function parseArgs(argv: string[]): Record<string, string | boolean> {
  const result: Record<string, string | boolean> = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith("--")) continue;

    const eq = arg.indexOf("=");
    if (eq !== -1) {
      result[arg.slice(2, eq)] = arg.slice(eq + 1);
      continue;
    }

    const key = arg.slice(2);
    const next = argv[i + 1];
    if (next !== undefined && !next.startsWith("--")) {
      result[key] = next;
      i++;
    } else {
      result[key] = true;
    }
  }
  return result;
}

function repoRoot(): string {
  // dist/scripts/eval.js -> project root
  return join(__dirname, "..", "..");
}

function loadCases(): EvalCase[] {
  const path = join(repoRoot(), "eval", "prompts.json");
  if (!existsSync(path)) {
    process.stderr.write(`Missing eval fixture file: ${path}\n`);
    process.exit(1);
  }

  return JSON.parse(readFileSync(path, "utf8")) as EvalCase[];
}

function printHelp(): void {
  console.log(`Prompt Sensei Eval

Usage:
  npm run eval
  npm run eval -- --case execution-medium-001
  npm run eval -- --category coding-agent
  npm --silent run eval -- --json

This prints calibration fixtures. It does not score prompts locally because live
Sensei scoring depends on the host agent applying SKILL.md in conversation.
`);
}

function printMarkdown(cases: EvalCase[]): void {
  console.log("# Prompt Sensei Eval");
  console.log("");
  console.log(`Cases: ${cases.length}`);
  console.log("");
  console.log("Use these fixtures to compare live Sensei output against expected stage, score band, flags, and tip theme.");
  console.log("");

  for (const item of cases) {
    console.log(`## ${item.id}`);
    console.log("");
    console.log(`Category: ${item.category}`);
    console.log(`Expected stage: ${item.expectedStage}`);
    if (item.acceptableStages && item.acceptableStages.length > 0) {
      console.log(`Acceptable stages: ${item.acceptableStages.join(", ")}`);
    }
    console.log(`Expected score band: ${item.expectedScoreBand}`);
    console.log(`Expected flags: ${item.expectedFlags.length > 0 ? item.expectedFlags.join(", ") : "none"}`);
    if (item.expectedTipKinds && item.expectedTipKinds.length > 0) {
      console.log(`Expected tip kinds: ${item.expectedTipKinds.join(", ")}`);
    }
    if (item.badTipKinds && item.badTipKinds.length > 0) {
      console.log(`Bad first tip kinds: ${item.badTipKinds.join(", ")}`);
    }
    console.log(`Expected tip theme: ${item.expectedTipTheme}`);
    if (item.notes) {
      console.log(`Notes: ${item.notes}`);
    }
    console.log("");
    console.log("Prompt:");
    console.log("```txt");
    console.log(item.prompt);
    console.log("```");
    console.log("");
    console.log("Review questions:");
    console.log("- Did Sensei classify the stage reasonably?");
    console.log("- If acceptable stages are listed, did Sensei choose one of them or explain why not?");
    console.log("- Did the score land in the expected band?");
    console.log("- Did the tip focus on the most useful next habit?");
    console.log("- Did the response avoid overclaiming that structure guarantees a better result?");
    console.log("");
  }
}

function main(): void {
  const args = parseArgs(process.argv);
  if (args["help"] === true || args["h"] === true) {
    printHelp();
    return;
  }

  let cases = loadCases();
  const caseId = typeof args["case"] === "string" ? args["case"] : undefined;
  const category = typeof args["category"] === "string" ? args["category"] : undefined;

  if (caseId) {
    cases = cases.filter((item) => item.id === caseId);
  }
  if (category) {
    cases = cases.filter((item) => item.category === category);
  }

  if (cases.length === 0) {
    process.stderr.write("No eval cases matched the requested filters.\n");
    process.exit(1);
  }

  if (args["json"] === true) {
    console.log(JSON.stringify(cases, null, 2));
    return;
  }

  printMarkdown(cases);
}

main();
