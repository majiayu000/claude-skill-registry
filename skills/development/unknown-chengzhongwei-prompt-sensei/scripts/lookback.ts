#!/usr/bin/env node
/**
 * Discover and extract local conversation history for Prompt Sensei lookback.
 *
 * Usage:
 *   lookback.js --discover [--source claude|codex|all]
 *   lookback.js --extract [--source claude|codex] --path <file-or-dir> [--mode report|one-by-one] [--limit 30|all]
 *   lookback.js --extract --source claude|codex|all --session all [--mode report|one-by-one] [--limit 30|all]
 *   lookback.js --save-report [--title "Prompt Sensei Lookback"] < report.md
 *
 * The extract path prints redacted user prompts to stdout for the active agent
 * to analyze. It never writes raw history or derived metadata to Prompt Sensei
 * storage.
 */

import { createHash } from "crypto";
import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "fs";
import { homedir } from "os";
import { basename, join, resolve } from "path";
import * as readline from "readline";
import { DATA_DIR, REPORTS_DIR } from "./lib/paths";
import { redactSensitiveText } from "./lib/redact";
import {
  grantLookbackConsent,
  hasLookbackConsent,
  loadSettings,
  saveSettings,
} from "./lib/settings";

const CLAUDE_PROJECTS_DIR = join(homedir(), ".claude", "projects");
const CODEX_SESSIONS_DIR = join(homedir(), ".codex", "sessions");
const CODEX_SESSION_INDEX = join(homedir(), ".codex", "session_index.jsonl");
const DEFAULT_PROMPT_LIMIT = 30;
const CONFIRM_PROMPT_THRESHOLD = 50;
const MAX_PROMPT_LIMIT = 500;
const DEFAULT_DISCOVERY_LIMIT = 20;
const DEFAULT_PROMPT_CHAR_LIMIT = 1200;

type Source = "claude" | "codex";
type Mode = "report" | "one-by-one";

interface Args {
  [key: string]: string | boolean | undefined;
}

interface PromptRecord {
  source: Source;
  sessionId: string;
  path: string;
  ts: string;
  text: string;
  index: number;
}

interface SessionSummary {
  source: Source;
  sessionId: string;
  title?: string;
  path: string;
  promptCount?: number;
  firstTs?: string;
  lastTs?: string;
}

interface PromptSelection {
  selected: PromptRecord[];
  skippedLowSignal: number;
}

function parseArgs(argv: string[]): Args {
  const result: Args = {};
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

function asString(value: string | boolean | undefined): string | undefined {
  return typeof value === "string" ? value : undefined;
}

function readJsonLines(path: string): unknown[] {
  if (!existsSync(path)) return [];
  return readFileSync(path, "utf8")
    .split("\n")
    .filter((line) => line.trim())
    .flatMap((line) => {
      try {
        return [JSON.parse(line) as unknown];
      } catch {
        return [];
      }
    });
}

function walkJsonlFiles(root: string): string[] {
  if (!existsSync(root)) return [];
  const results: string[] = [];

  function visit(path: string): void {
    let stats;
    try {
      stats = statSync(path);
    } catch {
      return;
    }

    if (stats.isDirectory()) {
      for (const entry of readdirSync(path)) {
        visit(join(path, entry));
      }
      return;
    }

    if (stats.isFile() && path.endsWith(".jsonl")) {
      results.push(path);
    }
  }

  visit(root);
  return results.sort();
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function getString(value: unknown): string | undefined {
  return typeof value === "string" ? value : undefined;
}

function contentToText(content: unknown): string {
  if (typeof content === "string") return content;

  if (Array.isArray(content)) {
    return content
      .map((block) => {
        if (typeof block === "string") return block;
        if (!isRecord(block)) return "";
        const type = getString(block["type"]);
        if (type === "tool_result" || type === "image" || type === "input_image") return "";
        return getString(block["text"]) ?? getString(block["content"]) ?? "";
      })
      .filter(Boolean)
      .join("\n");
  }

  if (isRecord(content)) {
    return getString(content["text"]) ?? getString(content["content"]) ?? "";
  }

  return "";
}

function isLikelyUserPrompt(text: string): boolean {
  const trimmed = text.trim();
  if (!trimmed) return false;
  if (trimmed.startsWith("<environment_context>")) return false;
  if (trimmed.startsWith("<turn_aborted>")) return false;
  if (trimmed.startsWith("<user_editable_context>")) return false;
  if (trimmed.startsWith("<local-command-")) return false;
  return true;
}

function isLowSignalPrompt(text: string): boolean {
  const trimmed = text.trim();
  const lower = trimmed.toLowerCase();

  if (!trimmed) return true;
  if (/<command-name>[\s\S]*<\/command-name>/i.test(trimmed)) return true;
  if (/<command-message>[\s\S]*<\/command-message>/i.test(trimmed)) return true;
  if (/^\/prompt-sensei\b/i.test(trimmed)) return true;
  if (/^just reply\b/i.test(trimmed)) return true;
  if (/^reply (with )?["']?(ok|yes|no)["']?/i.test(trimmed)) return true;
  if (/^let'?s do\b/i.test(trimmed) && /\b(one-by-one|report|all|manual|[0-9]+)\b/i.test(trimmed)) return true;
  if (/^(y|yes|n|no|ok|okay|sure|continue|go ahead|proceed|confirm)$/i.test(trimmed)) return true;
  if (/^(all|manual|one-by-one|report)$/i.test(trimmed)) return true;
  if (/^[0-9]+$/.test(trimmed)) return true;
  if (/^[aam]$/i.test(trimmed)) return true;
  if (trimmed.startsWith("This session is being continued from a previous conversation that ran out of context.")) return true;
  if (trimmed.startsWith("Summary:") && lower.includes("primary request and intent")) return true;
  return false;
}

function normalizeTimestamp(value: unknown, fallbackPath: string): string {
  const ts = getString(value);
  if (ts && Number.isFinite(new Date(ts).getTime())) return ts;

  try {
    return statSync(fallbackPath).mtime.toISOString();
  } catch {
    return new Date(0).toISOString();
  }
}

function sessionIdFromPath(path: string): string {
  return basename(path).replace(/\.jsonl$/, "");
}

function codexSessionIdFromPath(path: string): string {
  const name = sessionIdFromPath(path);
  const match = name.match(/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$/i);
  return match?.[1] ?? name.replace(/^rollout-/, "");
}

function parseClaudePrompts(path: string): PromptRecord[] {
  const lines = readJsonLines(path);
  const prompts: PromptRecord[] = [];
  for (const line of lines) {
    if (!isRecord(line)) continue;
    const message = line["message"];
    if (!isRecord(message)) continue;
    if (message["role"] !== "user") continue;
    if (line["isMeta"] === true) continue;

    const text = contentToText(message["content"]);
    if (!isLikelyUserPrompt(text)) continue;

    prompts.push({
      source: "claude",
      sessionId: getString(line["sessionId"]) ?? sessionIdFromPath(path),
      path,
      ts: normalizeTimestamp(line["timestamp"], path),
      text,
      index: prompts.length + 1,
    });
  }
  return prompts;
}

function parseCodexPrompts(path: string): PromptRecord[] {
  const lines = readJsonLines(path);
  const sessionId = codexSessionIdFromFile(path, lines);
  const prompts: PromptRecord[] = [];
  for (const line of lines) {
    if (!isRecord(line) || line["type"] !== "response_item") continue;
    const payload = line["payload"];
    if (!isRecord(payload) || payload["role"] !== "user") continue;
    const text = contentToText(payload["content"]);
    if (!isLikelyUserPrompt(text)) continue;

    prompts.push({
      source: "codex",
      sessionId,
      path,
      ts: normalizeTimestamp(line["timestamp"], path),
      text,
      index: prompts.length + 1,
    });
  }
  return prompts;
}

function codexSessionIdFromFile(path: string, lines: unknown[]): string {
  const meta = lines.find((line) => isRecord(line) && line["type"] === "session_meta");
  if (isRecord(meta)) {
    const payload = meta["payload"];
    if (isRecord(payload)) {
      const id = getString(payload["id"]);
      if (id) return id;
    }
  }
  return codexSessionIdFromPath(path);
}

function parsePrompts(path: string, sourceHint?: Source): PromptRecord[] {
  const source = sourceHint ?? detectSource(path);
  if (source === "claude") return parseClaudePrompts(path);
  return parseCodexPrompts(path);
}

function detectSource(path: string): Source {
  const normalized = path.replaceAll("\\", "/");
  if (normalized.includes("/.codex/")) return "codex";
  return "claude";
}

function summarizeSession(path: string, source: Source, titleMap: Map<string, string>): SessionSummary | null {
  let stats;
  try {
    stats = statSync(path);
  } catch {
    return null;
  }

  const sessionId = source === "codex" ? codexSessionIdFromPath(path) : sessionIdFromPath(path);
  return {
    source,
    sessionId,
    title: titleMap.get(sessionId),
    path,
    lastTs: stats.mtime.toISOString(),
  };
}

function loadCodexTitleMap(): Map<string, string> {
  const titles = new Map<string, string>();
  if (!existsSync(CODEX_SESSION_INDEX)) return titles;

  for (const line of readJsonLines(CODEX_SESSION_INDEX)) {
    if (!isRecord(line)) continue;
    const id = getString(line["id"]);
    const title = getString(line["thread_name"]);
    if (id && title) titles.set(id, title);
  }
  return titles;
}

function sourceRoots(source: string): Array<{ source: Source; root: string }> {
  if (source === "claude") return [{ source: "claude", root: CLAUDE_PROJECTS_DIR }];
  if (source === "codex") return [{ source: "codex", root: CODEX_SESSIONS_DIR }];
  return [
    { source: "claude", root: CLAUDE_PROJECTS_DIR },
    { source: "codex", root: CODEX_SESSIONS_DIR },
  ];
}

function discoverSessions(sourceArg: string, maxSessions: number): SessionSummary[] {
  const titleMap = loadCodexTitleMap();
  const sessions = sourceRoots(sourceArg)
    .flatMap(({ source, root }) =>
      walkJsonlFiles(root)
        .filter((path) => !path.includes("/subagents/"))
        .map((path) => summarizeSession(path, source, titleMap))
        .filter((session): session is SessionSummary => session !== null)
    )
    .sort((a, b) => new Date(b.lastTs ?? 0).getTime() - new Date(a.lastTs ?? 0).getTime());

  return sessions.slice(0, maxSessions);
}

function printDiscovery(sessions: SessionSummary[]): void {
  console.log("# Prompt Sensei Lookback Sessions");
  if (sessions.length === 0) {
    console.log("No Claude Code or Codex sessions found.");
    return;
  }

  console.log("Select one session by path, or choose all sessions in the guided flow.\n");
  sessions.forEach((session, index) => {
    const title = session.title ? ` — ${session.title}` : "";
    const count = session.promptCount === undefined ? "prompt count available after consent" : `${session.promptCount} prompts`;
    console.log(`${index + 1}. ${session.source} · ${count} · latest ${session.lastTs ?? "unknown"}${title}`);
    console.log(`   session: ${session.sessionId}`);
    console.log(`   path: ${session.path}`);
  });
}

function parseLimit(value: string | undefined): number {
  if (!value) return DEFAULT_PROMPT_LIMIT;
  if (value === "all") return MAX_PROMPT_LIMIT;
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) return DEFAULT_PROMPT_LIMIT;
  return Math.min(parsed, MAX_PROMPT_LIMIT);
}

function shortHash(value: string): string {
  return createHash("sha256").update(value).digest("hex").slice(0, 16);
}

function lookbackConsentScope(args: Args): string {
  const pathArg = asString(args["path"]);
  const sourceArg = asString(args["source"]) ?? (pathArg ? detectSource(pathArg) : "all");
  const sessionArg = asString(args["session"]);
  const mode = asString(args["mode"]) ?? "report";
  const limit = asString(args["limit"]) ?? String(DEFAULT_PROMPT_LIMIT);
  const promptAccess = asString(args["prompt-access"]) ?? "redacted-prompts";
  const reportStorage = asString(args["report-storage"]) ?? "temporary-report";

  const selection = pathArg
    ? `path:${shortHash(resolve(pathArg.replace(/^~(?=$|\/)/, homedir())))}`
    : sessionArg === "all"
      ? "session:all"
      : `session:${sessionArg ?? "selected"}`;

  return [
    "lookback:v1",
    `source:${sourceArg}`,
    selection,
    `mode:${mode}`,
    `limit:${limit}`,
    `access:${promptAccess}`,
    `storage:${reportStorage}`,
  ].join("|");
}

function collectPrompts(args: Args): PromptRecord[] {
  const pathArg = asString(args["path"]);
  const sourceArg = asString(args["source"]) ?? "all";
  const sessionArg = asString(args["session"]);

  if (pathArg) {
    const resolved = resolve(pathArg.replace(/^~(?=$|\/)/, homedir()));
    if (!existsSync(resolved)) {
      process.stderr.write(`Path not found: ${resolved}\n`);
      process.exit(1);
    }

    const stats = statSync(resolved);
    const paths = stats.isDirectory() ? walkJsonlFiles(resolved) : [resolved];
    const sourceHint = sourceArg === "claude" || sourceArg === "codex" ? sourceArg : undefined;
    return paths.flatMap((path) => parsePrompts(path, sourceHint));
  }

  if (sessionArg === "all") {
    return sourceRoots(sourceArg).flatMap(({ source, root }) =>
      walkJsonlFiles(root)
        .filter((path) => !path.includes("/subagents/"))
        .flatMap((path) => parsePrompts(path, source))
    );
  }

  process.stderr.write("Provide --path <file-or-dir> or --session all with --source claude|codex|all.\n");
  process.exit(1);
}

function redact(text: string): string {
  return redactSensitiveText(text, { redactHome: true });
}

function truncate(text: string, maxChars: number): string {
  if (text.length <= maxChars) return text;
  return `${text.slice(0, maxChars).trimEnd()}\n[TRUNCATED]`;
}

function selectRecentPrompts(prompts: PromptRecord[], limit: number): PromptSelection {
  const candidates = [...prompts]
    .sort((a, b) => new Date(b.ts).getTime() - new Date(a.ts).getTime())
    .slice(0, limit);
  const selected = candidates
    .filter((prompt) => !isLowSignalPrompt(prompt.text))
    .sort((a, b) => new Date(a.ts).getTime() - new Date(b.ts).getTime());

  return {
    selected,
    skippedLowSignal: candidates.length - selected.length,
  };
}

function printAnalysisPack(prompts: PromptRecord[], mode: Mode, requestedLimit: string | undefined, maxChars: number): void {
  const selection = selectRecentPrompts(prompts, parseLimit(requestedLimit));
  const { selected, skippedLowSignal } = selection;
  const total = prompts.length;
  const limitLabel = requestedLimit ?? String(DEFAULT_PROMPT_LIMIT);
  const capped = requestedLimit === "all" && total > MAX_PROMPT_LIMIT;

  console.log("# Prompt Sensei Lookback Analysis Pack");
  console.log(`Mode: ${mode}`);
  console.log(`Selected prompts: ${selected.length} of ${total}`);
  console.log(`Selection: most recent ${limitLabel}, shown oldest to newest`);
  if (skippedLowSignal > 0) {
    console.log(`Skipped low-signal prompts: ${skippedLowSignal}`);
    console.log("[Sensei: skipped grading for low-signal prompt]");
  }
  if (capped) {
    console.log(`Limit note: "all" was capped at ${MAX_PROMPT_LIMIT} prompts.`);
  }
  if (selected.length > CONFIRM_PROMPT_THRESHOLD) {
    console.log(`Large-run note: this pack has more than ${CONFIRM_PROMPT_THRESHOLD} prompts; the guided flow should confirm this before analysis.`);
  }
  console.log("");
  console.log("Privacy: prompts below are redacted and printed for the active agent to analyze. Prompt Sensei does not save raw history or derived lookback metadata.");
  console.log("Instruction: avoid direct quotes in the final answer unless the user explicitly asks for examples.");

  if (mode === "one-by-one") {
    console.log("Analysis target: give concise coaching for each prompt, with one habit per prompt.");
  } else {
    console.log("Analysis target: produce a lookback report with repeated patterns, strong habits, and 1-5 next tips.");
  }

  console.log("\n## Redacted User Prompts");
  selected.forEach((prompt, index) => {
    const redacted = truncate(redact(prompt.text), maxChars);
    console.log(`\n### ${index + 1}. ${prompt.ts}`);
    console.log(`Session: ${prompt.sessionId}`);
    console.log(`Prompt index in session: ${prompt.index}`);
    console.log("```txt");
    console.log(redacted);
    console.log("```");
  });
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

function slugify(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 48) || "lookback";
}

async function saveReport(args: Args): Promise<void> {
  const body = await readStdin();
  if (!body.trim()) {
    process.stderr.write("No report content received on stdin.\n");
    process.exit(1);
  }

  const title = asString(args["title"]) ?? "Prompt Sensei Lookback";
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const file = join(REPORTS_DIR, `${stamp}-${slugify(title)}.md`);
  if (!existsSync(REPORTS_DIR)) {
    mkdirSync(REPORTS_DIR, { recursive: true });
  }

  writeFileSync(file, `${body.trim()}\n`, "utf8");
  console.log(`Saved lookback report: ${file}`);
}

function printHelp(): void {
  console.log(`Prompt Sensei Lookback

Commands:
  --discover [--source claude|codex|all]
  --extract [--source claude|codex] --path <file-or-dir> [--mode report|one-by-one] [--limit 30|all]
  --extract --source claude|codex|all --session all [--mode report|one-by-one] [--limit 30|all]
  --save-report [--title "Prompt Sensei Lookback"] < report.md
  --consent-scope [lookback selection flags]
  --consent-status --scope <scope>
  --grant-consent --scope <scope>

Defaults:
  mode: report
  limit: ${DEFAULT_PROMPT_LIMIT}
  max prompts: ${MAX_PROMPT_LIMIT}
  max chars per prompt: ${DEFAULT_PROMPT_CHAR_LIMIT}

Privacy:
  Raw history is read locally, redacted, and printed to stdout for the active
  agent to analyze. Prompt Sensei does not store raw history or lookback
  metadata by default.`);
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv);
  if (args["help"]) {
    printHelp();
    return;
  }

  if (args["consent-scope"]) {
    console.log(lookbackConsentScope(args));
    return;
  }

  if (args["consent-status"]) {
    const scope = asString(args["scope"]) ?? lookbackConsentScope(args);
    const settings = loadSettings();
    console.log(`Lookback consent: ${hasLookbackConsent(settings, scope) ? "granted" : "not granted"}`);
    console.log(`Scope: ${scope}`);
    return;
  }

  if (args["grant-consent"]) {
    const scope = asString(args["scope"]) ?? lookbackConsentScope(args);
    saveSettings(grantLookbackConsent(loadSettings(), scope));
    console.log("Lookback consent: granted");
    console.log(`Scope: ${scope}`);
    return;
  }

  if (args["save-report"]) {
    await saveReport(args);
    return;
  }

  if (args["extract"]) {
    const mode = (asString(args["mode"]) ?? "report") as Mode;
    if (mode !== "report" && mode !== "one-by-one") {
      process.stderr.write("Invalid --mode. Use report or one-by-one.\n");
      process.exit(1);
    }
    const maxChars = Number.parseInt(asString(args["max-chars-per-prompt"]) ?? "", 10) || DEFAULT_PROMPT_CHAR_LIMIT;
    const prompts = collectPrompts(args);
    printAnalysisPack(prompts, mode, asString(args["limit"]), maxChars);
    return;
  }

  const source = asString(args["source"]) ?? "all";
  const maxSessions = Number.parseInt(asString(args["max-sessions"]) ?? "", 10) || DEFAULT_DISCOVERY_LIMIT;
  printDiscovery(discoverSessions(source, maxSessions));
}

main().catch((err) => {
  process.stderr.write(`lookback error: ${err instanceof Error ? err.message : String(err)}\n`);
  process.exit(1);
});
