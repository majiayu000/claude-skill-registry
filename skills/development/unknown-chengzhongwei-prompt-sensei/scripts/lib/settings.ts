import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { DATA_DIR, CONFIG_FILE, SETTINGS_FILE } from "./paths";

export interface ConsentRecord {
  granted: boolean;
  grantedAt: string | null;
}

export interface LookbackConsentRecord extends ConsentRecord {
  scope: string | null;
}

export interface PromptSenseiSettings {
  version: 1;
  autoObserve: boolean;
  saveRedactedPrompts: boolean;
  consent: {
    observe: ConsentRecord;
    lookback: LookbackConsentRecord;
    saveRedactedPrompts: ConsentRecord;
  };
}

interface LegacyConfig {
  v?: number;
  consentGiven?: boolean;
  consentAt?: string;
}

function defaultConsent(): ConsentRecord {
  return {
    granted: false,
    grantedAt: null,
  };
}

export function defaultSettings(): PromptSenseiSettings {
  return {
    version: 1,
    autoObserve: false,
    saveRedactedPrompts: false,
    consent: {
      observe: defaultConsent(),
      lookback: {
        ...defaultConsent(),
        scope: null,
      },
      saveRedactedPrompts: defaultConsent(),
    },
  };
}

export function ensureDataDir(): void {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function asBoolean(value: unknown, fallback: boolean): boolean {
  return typeof value === "boolean" ? value : fallback;
}

function asNullableString(value: unknown, fallback: string | null): string | null {
  return typeof value === "string" || value === null ? value : fallback;
}

function mergeConsent(value: unknown, fallback: ConsentRecord): ConsentRecord {
  if (!isRecord(value)) return fallback;
  return {
    granted: asBoolean(value["granted"], fallback.granted),
    grantedAt: asNullableString(value["grantedAt"], fallback.grantedAt),
  };
}

function mergeSettings(raw: unknown): PromptSenseiSettings {
  const base = defaultSettings();
  if (!isRecord(raw)) return base;

  const consent = isRecord(raw["consent"]) ? raw["consent"] : {};
  const lookback = mergeConsent(consent["lookback"], base.consent.lookback);
  const saveRedactedPrompts = mergeConsent(
    consent["saveRedactedPrompts"],
    base.consent.saveRedactedPrompts
  );

  return {
    version: 1,
    autoObserve: asBoolean(raw["autoObserve"], base.autoObserve),
    saveRedactedPrompts: asBoolean(raw["saveRedactedPrompts"], base.saveRedactedPrompts),
    consent: {
      observe: mergeConsent(consent["observe"], base.consent.observe),
      lookback: {
        ...lookback,
        scope: isRecord(consent["lookback"])
          ? asNullableString(consent["lookback"]["scope"], base.consent.lookback.scope)
          : base.consent.lookback.scope,
      },
      saveRedactedPrompts,
    },
  };
}

function loadLegacyConfig(): LegacyConfig | null {
  if (!existsSync(CONFIG_FILE)) return null;
  try {
    const parsed = JSON.parse(readFileSync(CONFIG_FILE, "utf8")) as unknown;
    return isRecord(parsed) ? (parsed as LegacyConfig) : null;
  } catch {
    return null;
  }
}

function applyLegacyConfig(settings: PromptSenseiSettings): PromptSenseiSettings {
  const legacy = loadLegacyConfig();
  if (!legacy?.consentGiven) return settings;

  return {
    ...settings,
    consent: {
      ...settings.consent,
      observe: {
        granted: true,
        grantedAt: settings.consent.observe.grantedAt ?? legacy.consentAt ?? new Date().toISOString(),
      },
    },
  };
}

export function loadSettings(): PromptSenseiSettings {
  if (!existsSync(SETTINGS_FILE)) {
    return applyLegacyConfig(defaultSettings());
  }

  try {
    return applyLegacyConfig(mergeSettings(JSON.parse(readFileSync(SETTINGS_FILE, "utf8")) as unknown));
  } catch {
    return applyLegacyConfig(defaultSettings());
  }
}

export function saveSettings(settings: PromptSenseiSettings): void {
  ensureDataDir();
  writeFileSync(SETTINGS_FILE, JSON.stringify(mergeSettings(settings), null, 2) + "\n", "utf8");
}

export function ensureSettings(): PromptSenseiSettings {
  const settings = loadSettings();
  saveSettings(settings);
  return settings;
}

export function grantObserveConsent(settings: PromptSenseiSettings, at = new Date().toISOString()): PromptSenseiSettings {
  return {
    ...settings,
    consent: {
      ...settings.consent,
      observe: {
        granted: true,
        grantedAt: settings.consent.observe.grantedAt ?? at,
      },
    },
  };
}

export function setAutoObserve(settings: PromptSenseiSettings, enabled: boolean): PromptSenseiSettings {
  return {
    ...settings,
    autoObserve: enabled,
  };
}

export function setSaveRedactedPrompts(
  settings: PromptSenseiSettings,
  enabled: boolean,
  at = new Date().toISOString()
): PromptSenseiSettings {
  return {
    ...settings,
    saveRedactedPrompts: enabled,
    consent: {
      ...settings.consent,
      saveRedactedPrompts: enabled
        ? {
            granted: true,
            grantedAt: settings.consent.saveRedactedPrompts.grantedAt ?? at,
          }
        : settings.consent.saveRedactedPrompts,
    },
  };
}

export function hasObserveConsent(settings: PromptSenseiSettings): boolean {
  return settings.consent.observe.granted;
}

export function hasLookbackConsent(settings: PromptSenseiSettings, scope: string): boolean {
  return settings.consent.lookback.granted && settings.consent.lookback.scope === scope;
}

export function grantLookbackConsent(
  settings: PromptSenseiSettings,
  scope: string,
  at = new Date().toISOString()
): PromptSenseiSettings {
  return {
    ...settings,
    consent: {
      ...settings.consent,
      lookback: {
        granted: true,
        grantedAt: settings.consent.lookback.grantedAt ?? at,
        scope,
      },
    },
  };
}
