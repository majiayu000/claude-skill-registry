#!/usr/bin/env node
/**
 * Generate a session report from local observation data.
 * Usage: report.js [--days 7]
 *
 * Reads ~/.prompt-sensei/events.jsonl and prints a Markdown report to stdout.
 */

import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { homedir } from "os";
import { spawn } from "child_process";
import {
  TIP_COACHING,
  normalizeStage,
  normalizeTaskType,
  selectTipKind,
  type TipKind,
} from "./lib/coaching";

const DATA_DIR = join(homedir(), ".prompt-sensei");
const EVENTS_FILE = join(DATA_DIR, "events.jsonl");
const UPDATE_FILE = join(DATA_DIR, "update-check.json");
const UPDATE_SCRIPT = join(__dirname, "update.js");

interface PromptEvent {
  v: number;
  ts: string;
  type: string;
  stage?: string;
  taskType?: string;
  score?: number;
  flags?: string[];
  tipKind?: string;
}

interface UpdateState {
  v: number;
  checkedAt: string;
  status: string;
  branch?: string;
  currentSha?: string;
  remoteSha?: string;
}

function loadEvents(days: number): PromptEvent[] {
  if (!existsSync(EVENTS_FILE)) return [];

  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);

  const lines = readFileSync(EVENTS_FILE, "utf8")
    .split("\n")
    .filter(Boolean);

  const events: PromptEvent[] = [];
  for (const line of lines) {
    try {
      const event = JSON.parse(line) as PromptEvent;
      if (
        (event.type === "prompt-observed" || event.type === "prompt-hashed") &&
        new Date(event.ts) >= cutoff
      ) {
        events.push(event);
      }
    } catch {
      // skip malformed lines
    }
  }
  return events;
}

function hasSessionStart(days: number): boolean {
  if (!existsSync(EVENTS_FILE)) return false;

  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);

  const lines = readFileSync(EVENTS_FILE, "utf8")
    .split("\n")
    .filter(Boolean);

  for (const line of lines) {
    try {
      const event = JSON.parse(line) as PromptEvent;
      if (event.type === "session-start" && new Date(event.ts) >= cutoff) {
        return true;
      }
    } catch {
      // skip malformed lines
    }
  }
  return false;
}

function loadUpdateState(): UpdateState | null {
  if (!existsSync(UPDATE_FILE)) return null;
  try {
    return JSON.parse(readFileSync(UPDATE_FILE, "utf8")) as UpdateState;
  } catch {
    return null;
  }
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
    // Reports should still work if update checks fail.
  }
}

function printUpdateNotice(): void {
  const state = loadUpdateState();
  if (state?.status !== "update-available") return;

  console.log("\n## Update");
  console.log(`Update available on \`${state.branch ?? "current branch"}\`.`);
  if (state.currentSha && state.remoteSha) {
    console.log(`- Local: ${state.currentSha.slice(0, 7)}`);
    console.log(`- Remote: ${state.remoteSha.slice(0, 7)}`);
  }
  console.log("- Run `/prompt-sensei update` to update.");
}

function avg(nums: number[]): number {
  if (nums.length === 0) return 0;
  return nums.reduce((a, b) => a + b, 0) / nums.length;
}

function gradeLabel(score100: number): string {
  if (score100 >= 90) return "Excellent";
  if (score100 >= 70) return "Good";
  if (score100 >= 50) return "Developing";
  if (score100 >= 30) return "Early stage";
  return "Needs work";
}

function topN<T>(map: Map<T, number>, n: number): Array<[T, number]> {
  return [...map.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, n);
}

function increment<T>(map: Map<T, number>, key: T): void {
  map.set(key, (map.get(key) ?? 0) + 1);
}

function percent(count: number, total: number): string {
  return total === 0 ? "0" : ((count / total) * 100).toFixed(0);
}

function sparkline(scores: number[]): string {
  const chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"];
  return scores
    .map((s) => chars[Math.min(Math.floor((s / 5) * chars.length), chars.length - 1)])
    .join("");
}

function topFlagByTask(
  taskFlagCounts: Map<string, Map<string, number>>,
  topTasks: Array<[string, number]>,
  limit: number
): Array<{ task: string; flag: string; count: number }> {
  const rows: Array<{ task: string; flag: string; count: number }> = [];
  for (const [task] of topTasks) {
    const topFlag = topN(taskFlagCounts.get(task) ?? new Map<string, number>(), 1)[0];
    if (topFlag) {
      rows.push({ task, flag: topFlag[0], count: topFlag[1] });
    }
    if (rows.length >= limit) break;
  }
  return rows;
}

function eventTipKind(event: PromptEvent): TipKind | null {
  if (event.tipKind && Object.prototype.hasOwnProperty.call(TIP_COACHING, event.tipKind)) {
    return event.tipKind as TipKind;
  }
  return selectTipKind(event.flags ?? [], event.stage, event.taskType);
}

function topTipByTask(
  taskTipCounts: Map<string, Map<TipKind, number>>,
  topTasks: Array<[string, number]>,
  limit: number
): Array<{ task: string; tipKind: TipKind; count: number }> {
  const rows: Array<{ task: string; tipKind: TipKind; count: number }> = [];
  for (const [task] of topTasks) {
    const topTip = topN(taskTipCounts.get(task) ?? new Map<TipKind, number>(), 1)[0];
    if (topTip) {
      rows.push({ task, tipKind: topTip[0], count: topTip[1] });
    }
    if (rows.length >= limit) break;
  }
  return rows;
}

function describeStageShift(events: PromptEvent[]): string | null {
  if (events.length < 10) return null;

  const recent = events.slice(-5);
  const previous = events.slice(-10, -5);
  const stages = new Set<string>();
  for (const event of [...recent, ...previous]) {
    const stage = normalizeStage(event.stage);
    if (stage) stages.add(stage);
  }

  let biggestShift: { stage: string; delta: number; recentCount: number; previousCount: number } | null = null;
  for (const stage of stages) {
    const recentCount = recent.filter((event) => normalizeStage(event.stage) === stage).length;
    const previousCount = previous.filter((event) => normalizeStage(event.stage) === stage).length;
    const delta = recentCount / recent.length - previousCount / previous.length;
    if (!biggestShift || Math.abs(delta) > Math.abs(biggestShift.delta)) {
      biggestShift = { stage, delta, recentCount, previousCount };
    }
  }

  if (!biggestShift || biggestShift.delta === 0) return null;

  const direction = biggestShift.delta > 0 ? "more" : "less";
  return `${direction} ${biggestShift.stage} prompts recently (${biggestShift.recentCount}/5 vs ${biggestShift.previousCount}/5 previous)`;
}

function momentumMessage(trend100: number): string {
  if (trend100 > 8) {
    return "Your recent prompts are scoring higher, but treat that as a signal to inspect, not proof of better outcomes.";
  }
  if (trend100 > 4) {
    return "Your scores are trending upward. Check whether the same habits also reduced clarification or rework.";
  }
  if (trend100 < -8) {
    return "Your recent prompts are scoring lower, which often means the work got harder or less familiar.";
  }
  if (trend100 < -4) {
    return "Your scores dipped recently. That can happen when tasks get harder.";
  }
  return "Your scores are steady. This is a good moment to focus on one repeatable habit.";
}

function scoreBandMessage(avgScore100: number, topTask: string): string {
  if (avgScore100 >= 90) {
    return `Your ${topTask} prompts are consistently strong for their stage. Keep protecting that clarity when tasks get bigger.`;
  }
  if (avgScore100 >= 70) {
    return `Your ${topTask} prompts are already useful. One sharper habit can move them from good to consistently excellent.`;
  }
  if (avgScore100 >= 50) {
    return `Your ${topTask} prompts are in the developing range. The next gain is likely one missing detail, not a full rewrite.`;
  }
  return `Your ${topTask} prompts are still mostly early-stage. Start by making the desired action unmistakable.`;
}

function formatCoaching(area: { task: string; tipKind: TipKind; count: number }): string | null {
  const note = TIP_COACHING[area.tipKind];
  if (!note) return null;

  return [
    `\nNext habit for ${area.task}: ${note.habit}`,
    `Why it matters: ${note.why}`,
    `Practice: ${note.practice}`,
  ].join("\n");
}

function generateEncouragement(
  avgScore100: number,
  trend100: number,
  topTask: string,
  topTips: Array<[TipKind, number]>,
  taskGrowthAreas: Array<{ task: string; tipKind: TipKind; count: number }>
): string {
  const lines: string[] = [];

  lines.push(momentumMessage(trend100));
  lines.push(scoreBandMessage(avgScore100, topTask));

  const topTaskArea = taskGrowthAreas.find((area) => area.task === topTask) ?? taskGrowthAreas[0];
  if (topTaskArea) {
    const coaching = formatCoaching(topTaskArea);
    if (coaching) {
      lines.push(coaching);
      return lines.join("\n");
    }
  }

  if (topTips.length > 0) {
    const [topTip] = topTips[0];
    const coaching = formatCoaching({ task: topTask, tipKind: topTip, count: 0 });
    if (coaching) {
      lines.push(coaching);
    }
  }

  return lines.join("\n");
}

function main(): void {
  const daysArg = process.argv.find((a) => a.startsWith("--days="));
  const days = daysArg ? parseInt(daysArg.split("=")[1]!) : 7;

  runBackgroundUpdateCheck();
  const events = loadEvents(days);

  if (events.length === 0) {
    if (!existsSync(EVENTS_FILE)) {
      console.log("No session data found.");
      console.log(
        "Activate observation with `/prompt-sensei observe` to start tracking."
      );
    } else if (hasSessionStart(days)) {
      console.log("# Prompt Sensei Report");
      console.log(`Session started, but no prompts have been scored in the last ${days} days.`);
      console.log(
        "Keep prompting — scores will appear here after the first observed prompt."
      );
    } else {
      console.log("# Prompt Sensei Report");
      console.log(`No prompt observations found in the last ${days} days.`);
      console.log(
        "Use `/prompt-sensei observe` to start a new scored session."
      );
    }
    printUpdateNotice();
    return;
  }

  const scoredEvents = events.filter(
    (event) => event.type === "prompt-observed" && typeof event.score === "number"
  );
  const hashOnlyCount = events.filter((event) => event.type === "prompt-hashed").length;
  const scores = scoredEvents.map((e) => e.score).filter((s): s is number => s !== undefined);

  if (scores.length === 0) {
    console.log("# Prompt Sensei Report");
    console.log(`Observed 0 scored prompts in the last ${days} days.`);
    if (hashOnlyCount > 0) {
      console.log(`\n**Hash-only prompt captures:** ${hashOnlyCount}`);
      console.log(
        "These came from the local hook and are excluded from scoring because no stage or score was recorded."
      );
    }
    console.log("\nNo scored session data found.");
    console.log(
      "Activate observation with `/prompt-sensei observe` to start receiving scored feedback."
    );
    printUpdateNotice();
    return;
  }

  const avgScore = avg(scores);
  const recent5 = scores.slice(-5);
  const older5 = scores.slice(-10, -5);
  const trend = recent5.length > 0 && older5.length > 0
    ? avg(recent5) - avg(older5)
    : 0;

  const stageCounts = new Map<string, number>();
  const taskCounts = new Map<string, number>();
  const flagCounts = new Map<string, number>();
  const tipCounts = new Map<TipKind, number>();
  const taskFlagCounts = new Map<string, Map<string, number>>();
  const taskTipCounts = new Map<string, Map<TipKind, number>>();

  for (const event of scoredEvents) {
    const task = normalizeTaskType(event.taskType);
    const stage = normalizeStage(event.stage);
    if (stage) {
      increment(stageCounts, stage);
    }
    increment(taskCounts, task);
    for (const flag of event.flags ?? []) {
      increment(flagCounts, flag);
      let nested = taskFlagCounts.get(task);
      if (!nested) {
        nested = new Map<string, number>();
        taskFlagCounts.set(task, nested);
      }
      increment(nested, flag);
    }
    const tipKind = eventTipKind(event);
    if (tipKind) {
      increment(tipCounts, tipKind);
      let nested = taskTipCounts.get(task);
      if (!nested) {
        nested = new Map<TipKind, number>();
        taskTipCounts.set(task, nested);
      }
      increment(nested, tipKind);
    }
  }

  const topStage = topN(stageCounts, 1)[0]?.[0] ?? "unknown";
  const topTasks = topN(taskCounts, 3);
  const usefulTopTasks = topTasks.some(([task]) => task !== "other")
    ? topTasks.filter(([task]) => task !== "other")
    : topTasks;
  const topTask = topTasks[0]?.[0] ?? "unknown";
  const displayTask = usefulTopTasks[0]?.[0] ?? topTask;
  const topFlags = topN(flagCounts, 3);
  const topTips = topN(tipCounts, 3);
  const taskGrowthAreas = topFlagByTask(taskFlagCounts, topTasks, 3);
  const taskHabitAreas = topTipByTask(taskTipCounts, usefulTopTasks, 3);
  const stageShift = describeStageShift(scoredEvents);

  const avgScore100 = Math.round(avgScore * 20);
  const trend100 = Math.round(trend * 20);
  const trendSymbol = trend100 > 2 ? "↑" : trend100 < -2 ? "↓" : "→";
  const topHabit = topTips[0]?.[0];
  const topHabitNote = topHabit ? TIP_COACHING[topHabit] : null;

  console.log("# Prompt Sensei Report");
  console.log(`Observed ${scores.length} scored prompts in the last ${days} days.`);
  if (hashOnlyCount > 0) {
    console.log(`Hash-only prompt captures: ${hashOnlyCount} (excluded from scoring)`);
  }
  console.log("");
  if (topHabitNote) {
    console.log(`**Next habit:**      ${topHabitNote.habit}`);
  }
  if (topHabit) {
    console.log(`**Repeated gap:**    ${topHabit} (${tipCounts.get(topHabit)}×)`);
  }
  console.log(`**Average score:**    ${avgScore100} / 100  (${gradeLabel(avgScore100)})`);
  if (scores.length >= 10) {
    console.log(`**Trend:**            ${trendSymbol}  ${Math.abs(trend100)} pts vs previous 5 prompts`);
  }
  console.log(`**Most common type:** ${displayTask}`);
  console.log(`**Most common stage:** ${topStage}`);
  if (stageShift) {
    console.log(`**Stage trend:**      ${stageShift}`);
  }

  if (scores.length >= 3) {
    console.log(`\n**Score history:**    ${sparkline(scores.slice(-20))}`);
  }

  if (topFlags.length > 0) {
    console.log("\n## Most common gaps");
    for (const [flag, count] of topFlags) {
      console.log(`- ${flag} (${count}×)`);
    }
  }

  if (topTips.length > 0) {
    console.log("\n## Most common habits");
    for (const [tipKind, count] of topTips) {
      console.log(`- ${tipKind}: ${TIP_COACHING[tipKind].habit} (${count}×)`);
    }
  }

  if (taskHabitAreas.length > 0) {
    console.log("\n## Habit by task type");
    for (const area of taskHabitAreas) {
      console.log(`- ${area.task}: ${area.tipKind} (${area.count}×)`);
    }
  } else if (taskGrowthAreas.length > 0) {
    console.log("\n## Growth area by task type");
    for (const area of taskGrowthAreas) {
      console.log(`- ${area.task}: ${area.flag} (${area.count}×)`);
    }
  }

  const stageEntries = topN(stageCounts, 5);
  if (stageEntries.length > 0) {
    console.log("\n## Stage breakdown");
    for (const [stage, count] of stageEntries) {
      const pct = percent(count, scoredEvents.length);
      console.log(`- ${stage}: ${count} (${pct}%)`);
    }
  }

  printUpdateNotice();

  console.log("\n## Feedback");
  console.log(generateEncouragement(avgScore100, trend100, displayTask, topTips, taskHabitAreas));
}

main();
