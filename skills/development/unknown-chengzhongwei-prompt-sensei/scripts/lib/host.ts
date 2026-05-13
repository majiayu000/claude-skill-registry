import { resolve } from "path";

export type HostTool = "claude-code" | "codex" | "unknown";

export const SKILL_ROOT = resolve(__dirname, "..", "..", "..");

export function detectHostFromSkillRoot(root = SKILL_ROOT): HostTool {
  const normalized = root.replaceAll("\\", "/");
  if (normalized.includes("/.codex/skills/")) return "codex";
  if (normalized.includes("/.claude/skills/")) return "claude-code";
  return "unknown";
}

export function hostLabel(host = detectHostFromSkillRoot()): string {
  if (host === "claude-code") return "Claude Code";
  if (host === "codex") return "Codex";
  return "Unknown";
}

export function supportsClaudeHooks(host = detectHostFromSkillRoot()): boolean {
  return host === "claude-code" || host === "unknown";
}
