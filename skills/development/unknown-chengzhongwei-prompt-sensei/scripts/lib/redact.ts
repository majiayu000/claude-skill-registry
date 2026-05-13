import { createHash } from "crypto";
import { homedir } from "os";

export const REDACTED_PROMPT_PREVIEW_CHARS = 600;

const REDACT_PATTERNS: Array<[RegExp, string]> = [
  [/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g, "[EMAIL]"],
  [/\b(sk-|sk-ant-|ghp_|github_pat_|xox[baprs]-)[A-Za-z0-9\-_]{10,}/g, "[API_KEY]"],
  [/\b(?:bearer|token)\s+[A-Za-z0-9._~+/=-]{20,}/gi, "[TOKEN]"],
  [/\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b/g, "[TOKEN]"],
  [/\b(password|passwd|secret|token|api_?key)\s*[:=]\s*["']?[^"'\s]+["']?/gi, "[CREDENTIAL]"],
  [/-----BEGIN [A-Z ]+-----[\s\S]+?-----END [A-Z ]+-----/g, "[PRIVATE_KEY]"],
  [/https?:\/\/[^\s"'<>]+\?[^\s"'<>]+/g, "[URL_WITH_PARAMS]"],
  [/\b[A-Za-z0-9+/=_-]{40,}\b/g, "[SECRET]"],
];

export function redactSensitiveText(text: string, options: { redactHome?: boolean } = {}): string {
  let result = options.redactHome ? text.replaceAll(homedir(), "~") : text;
  for (const [pattern, replacement] of REDACT_PATTERNS) {
    result = result.replace(pattern, replacement);
  }
  return result;
}

export function hashPrompt(text: string): string {
  return createHash("sha256").update(redactSensitiveText(text)).digest("hex").slice(0, 16);
}

export function redactedPromptPreview(text: string): string {
  const redacted = redactSensitiveText(text, { redactHome: true }).trim();
  if (redacted.length <= REDACTED_PROMPT_PREVIEW_CHARS) return redacted;
  return `${redacted.slice(0, REDACTED_PROMPT_PREVIEW_CHARS).trimEnd()}\n[TRUNCATED]`;
}
