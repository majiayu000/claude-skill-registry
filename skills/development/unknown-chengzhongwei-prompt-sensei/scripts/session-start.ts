#!/usr/bin/env node
/**
 * Claude Code SessionStart hook support for opt-in auto observe.
 */

import * as readline from "readline";
import { loadSettings, hasObserveConsent } from "./lib/settings";

async function readStdin(): Promise<string> {
  if (process.stdin.isTTY) return "";
  const rl = readline.createInterface({ input: process.stdin });
  const lines: string[] = [];
  for await (const line of rl) {
    lines.push(line);
  }
  return lines.join("\n");
}

function printAdditionalContext(additionalContext: string): void {
  console.log(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext,
    },
  }));
}

async function main(): Promise<void> {
  await readStdin();
  const settings = loadSettings();

  if (!settings.autoObserve) {
    return;
  }

  if (!hasObserveConsent(settings)) {
    printAdditionalContext(
      "Prompt Sensei auto observe is enabled, but observe consent is not granted. Tell the user they can run `/prompt-sensei observe` to consent."
    );
    return;
  }

  printAdditionalContext(
    "Before responding to the user, use the Skill tool to invoke the `prompt-sensei` skill with args `observe --auto-start`. This is a silent auto-start path: do not announce setup, do not check settings in the visible response, and do not run setup scripts before answering. If the Skill tool is unavailable, follow Prompt Sensei observe mode exactly for this session. Every normal user-facing response must end with exactly one Sensei line in the required Prompt Sensei format. For scores below 90, pick one canonical Prompt Sensei tipKind first, then write `Tip:` using that habit phrase or a very close paraphrase so the Stop hook can persist tipKind. A grade label like `Good — minor gaps` is okay only if a concrete tip is also included. Score genuine questions and instructions even when they are short, factual, or ask for a terse answer. Skip only mechanical inputs: one-word acknowledgements, numeric menu choices, slash-command-only wrappers, explicit just-reply tests, and context-resume summaries. Keep feedback stage-aware, short, and privacy-preserving."
  );
}

main().catch((err) => {
  process.stderr.write(`session-start error: ${err instanceof Error ? err.message : String(err)}\n`);
  process.exit(1);
});
