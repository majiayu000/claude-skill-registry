import { homedir } from "os";
import { join } from "path";

export const DATA_DIR = join(homedir(), ".prompt-sensei");
export const EVENTS_FILE = join(DATA_DIR, "events.jsonl");
export const CONFIG_FILE = join(DATA_DIR, "config.json");
export const SETTINGS_FILE = join(DATA_DIR, "settings.json");
export const UPDATE_FILE = join(DATA_DIR, "update-check.json");
export const REPORTS_DIR = join(DATA_DIR, "reports");
