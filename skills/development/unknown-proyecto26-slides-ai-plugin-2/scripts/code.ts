import { readFileSync } from 'node:fs';
// @ts-ignore
import Prism from 'prismjs';
import type { CodeRun } from './types.js';

let THEME_MAP: Record<string, string> | undefined;

function loadPrismLanguage(lang: string = 'plaintext'): any {
  const normalized = String(lang || 'plaintext').toLowerCase();
  const map: Record<string, string> = {
    js: 'javascript',
    ts: 'typescript',
    py: 'python',
    sh: 'bash',
    yml: 'yaml',
    html: 'markup',
    xml: 'markup',
  };
  const id = map[normalized] || normalized;
  if (!Prism.languages[id]) {
    try {
      require.resolve(`prismjs/components/prism-${id}`);
      // @ts-ignore
      import(`prismjs/components/prism-${id}`);
    } catch (_e) {
      // Language not found
    }
  }
  return Prism.languages[id] || Prism.languages.plain || {};
}

function buildThemeMap(themeCssModule: string = 'prismjs/themes/prism-okaidia.css'): Record<string, string> {
  try {
    let cssPath: string;
    try {
      cssPath = require.resolve(themeCssModule);
    } catch {
      // For ESM, try to construct a path
      cssPath = themeCssModule;
    }
    const css = readFileSync(cssPath, 'utf8');
    return Object.fromEntries(
      [...css.matchAll(/\.token\.([\w-]+)[^{]*\{[^}]*color:\s*([^;\s]+)[^}]*\}/g)].map(
        ([, t, c]: string[]) => [t, c.replace(/#|!important/g, '').trim()]
      )
    );
  } catch (err) {
    return { plain: 'FFFFFF', comment: '999999' };
  }
}

function getThemeMap(): Record<string, string> {
  if (!THEME_MAP) THEME_MAP = buildThemeMap();
  return THEME_MAP;
}

function run(text: string, type: string = 'plain'): CodeRun {
  const theme = getThemeMap();
  return {
    text,
    options: {
      fontFace: 'Consolas',
      color: (theme[type] || theme.plain || 'FFFFFF') as any,
      fontSize: 14,
    },
  };
}

function tokensToRuns(tokens: any[]): CodeRun[] {
  return tokens.flatMap((t) =>
    typeof t === 'string'
      ? [run(t)]
      : Array.isArray(t.content)
        ? tokensToRuns(t.content)
        : [run(t.content, t.type)]
  );
}

export function codeToRuns(code: string = '', lang: string = 'plaintext'): CodeRun[] {
  const grammar = loadPrismLanguage(lang);
  const lines = String(code || '').split('\n');
  const pad = lines.length.toString().length;
  return lines.flatMap((line, i) => [
    run(`${(i + 1).toString().padStart(pad, ' ')} `, 'comment'),
    ...tokensToRuns(Prism.tokenize(line, grammar)),
    ...(i < lines.length - 1 ? [run('\n')] : []),
  ]);
}

export { buildThemeMap };
