import type { ColorHex, ThemeConfig, SlideTheme, FontConfig } from './types.js';

const DEFAULT_THEME: SlideTheme = {
  bg: { primary: '0a0a0a', secondary: '1a1a1a' },
  text: { primary: 'ffffff', secondary: '999999' },
  accent: '4a9eff',
  accentSecondary: 'ff6b6b',
  font: { heading: 'Arial', body: 'Arial', mono: 'Consolas' },
  size: {
    title: { min: 36, max: 44 },
    heading: { min: 28, max: 36 },
    body: { min: 18, max: 24 },
    caption: { min: 14, max: 16 },
  },
  spacing: { margin: 0.5, gutter: 0.3, cardPad: 0.2 },
  radius: { card: 0.1, badge: 0.05 },
  shadow: {
    card: { type: 'outer', color: '000000', opacity: 0.15, blur: 3, offset: 1, angle: 45 },
    elevated: { type: 'outer', color: '000000', opacity: 0.25, blur: 5, offset: 2, angle: 45 },
  },
};

export const PRESETS: Record<string, ThemeConfig> = {
  darkMonospace: {
    bg: { primary: '0d1117', secondary: '161b22' },
    text: { primary: 'e6edf3', secondary: '8b949e' },
    accent: '58a6ff',
    accentSecondary: '3fb950',
    font: { heading: 'JetBrains Mono', body: 'IBM Plex Mono', mono: 'JetBrains Mono' },
  },
  swissModern: {
    bg: { primary: 'ffffff', secondary: 'f5f5f5' },
    text: { primary: '1a1a1a', secondary: '666666' },
    accent: 'ff3300',
    accentSecondary: '0066ff',
    font: { heading: 'Clash Display', body: 'IBM Plex Sans', mono: 'IBM Plex Mono' },
  },
  boldSignal: {
    bg: { primary: '0a0a0a', secondary: '1a1a1a' },
    text: { primary: 'ffffff', secondary: '999999' },
    accent: 'ff6b35',
    accentSecondary: 'ffd700',
    font: { heading: 'Cabinet Grotesk', body: 'General Sans', mono: 'Consolas' },
  },
  darkBotanical: {
    bg: { primary: '1a1a1a', secondary: '2a2a2a' },
    text: { primary: 'f0ebe3', secondary: 'c9b896' },
    accent: 'c9b896',
    accentSecondary: 'e8b4b8',
    font: { heading: 'Cormorant Garamond', body: 'IBM Plex Sans', mono: 'Consolas' },
  },
  cleanCorporate: {
    bg: { primary: 'ffffff', secondary: 'f8f9fa' },
    text: { primary: '212529', secondary: '6c757d' },
    accent: '4361ee',
    accentSecondary: '3a0ca3',
    font: { heading: 'Plus Jakarta Sans', body: 'Source Sans 3', mono: 'Consolas' },
  },
  neonCyber: {
    bg: { primary: '0a0a1a', secondary: '12122a' },
    text: { primary: 'e0e0ff', secondary: '8080b0' },
    accent: '00f0ff',
    accentSecondary: 'ff00aa',
    font: { heading: 'Orbitron', body: 'Exo 2', mono: 'Fira Code' },
  },
  warmMinimal: {
    bg: { primary: 'faf8f5', secondary: 'f0ece6' },
    text: { primary: '2d2d2d', secondary: '6b6b6b' },
    accent: 'c05c3c',
    accentSecondary: '4a7c6f',
    font: { heading: 'Fraunces', body: 'Outfit', mono: 'Consolas' },
  },
  vintageEditorial: {
    bg: { primary: 'f5f0e8', secondary: 'ebe5d9' },
    text: { primary: '1a1a1a', secondary: '555555' },
    accent: 'c41e3a',
    accentSecondary: '1a3a5c',
    font: { heading: 'Playfair Display', body: 'Lora', mono: 'Consolas' },
  },
  terminalGreen: {
    bg: { primary: '0a0a0a', secondary: '111111' },
    text: { primary: '33ff33', secondary: '1a991a' },
    accent: '33ff33',
    accentSecondary: '00ccff',
    font: { heading: 'Share Tech Mono', body: 'Fira Code', mono: 'Fira Code' },
  },
  gradientWave: {
    bg: { primary: '0f0c29', secondary: '302b63' },
    text: { primary: 'ffffff', secondary: 'b8b8d0' },
    accent: '24c6dc',
    accentSecondary: '514a9d',
    font: { heading: 'Sora', body: 'Nunito Sans', mono: 'Consolas' },
  },
  midnightBlue: {
    bg: { primary: '1a1f36', secondary: '252b48' },
    text: { primary: 'e0e4f0', secondary: '8892b0' },
    accent: '6366f1',
    accentSecondary: '22d3ee',
    font: { heading: 'Manrope', body: 'DM Sans', mono: 'Consolas' },
  },
  paperInk: {
    bg: { primary: 'fefdfb', secondary: 'f5f3ef' },
    text: { primary: '2c2c2c', secondary: '666666' },
    accent: '1a5276',
    accentSecondary: '7d3c98',
    font: { heading: 'EB Garamond', body: 'Crimson Pro', mono: 'Consolas' },
  },
};

function deepMerge(target: any, source: any): any {
  const result = { ...target };
  for (const key of Object.keys(source)) {
    if (
      source[key] &&
      typeof source[key] === 'object' &&
      !Array.isArray(source[key]) &&
      target[key] &&
      typeof target[key] === 'object'
    ) {
      result[key] = deepMerge(target[key], source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}

function deepFreeze<T extends Record<string, any>>(obj: T): T {
  Object.freeze(obj);
  for (const val of Object.values(obj)) {
    if (val && typeof val === 'object' && !Object.isFrozen(val)) deepFreeze(val);
  }
  return obj;
}

export function createTheme(overrides: ThemeConfig = {}): SlideTheme {
  return deepFreeze(deepMerge(DEFAULT_THEME, overrides));
}

interface SectionMapEntry {
  start: number;
  end: number;
  value: string;
}

function parseSectionMap(sectionMap: Record<string, string>): SectionMapEntry[] {
  const entries: SectionMapEntry[] = [];
  for (const [key, value] of Object.entries(sectionMap)) {
    if (key.includes('-')) {
      const [start, end] = key.split('-').map(Number);
      entries.push({ start, end, value });
    } else {
      const idx = Number(key);
      entries.push({ start: idx, end: idx, value });
    }
  }
  return entries;
}

export function sectionBackground(
  slideIndex: number,
  sectionMap: Record<string, string>,
  colors: Record<string, ColorHex>
): ColorHex {
  const entries = parseSectionMap(sectionMap);
  for (const { start, end, value } of entries) {
    if (slideIndex >= start && slideIndex <= end) {
      return colors[value];
    }
  }
  return (colors.default as ColorHex) || ('ffffff' as ColorHex);
}

export function resolveFont(theme: SlideTheme, role: keyof FontConfig): string {
  const font = theme.font[role] || theme.font.body;
  const fallback = role === 'mono' ? 'Consolas' : 'Arial';
  return `${font}, ${fallback}`;
}

export { DEFAULT_THEME };
