import { spawnSync } from 'node:child_process';
// @ts-ignore
import { Canvas } from 'skia-canvas';
// @ts-ignore
import LineBreaker from 'linebreak';
// @ts-ignore
import * as fontkit from 'fontkit';
import type { AutoFontSizeOpts, TextBoxOpts, TextBoxLayout, TextRun } from './types.js';

const TEXT_MEASURER = getTextMeasurer();
const registeredFontVariants = new Set<string>();
const fontPathCache = new Map<string, string | null>();
const fontKitCache = new Map<string, any>();

export function calcTextBoxHeightSimple(
  fontSize: number,
  lines: number = 1,
  leading: number = 1.15,
  padding: number = 0.3
): number {
  const lineHeightIn = (fontSize / 72) * leading;
  return lines * lineHeightIn + padding;
}

export function autoFontSize(
  textOrRuns: string | TextRun[],
  fontFace: string,
  opts: AutoFontSizeOpts = {}
): AutoFontSizeOpts & { fontSize: number } {
  const x = toNumber(opts.x, 0);
  const y = toNumber(opts.y, 0);
  const w = toNumber(opts.w, 0);
  const h = toNumber(opts.h, 0);
  if (!(w > 0 && h > 0)) throw new Error('autoFontSize(): non-positive w or h');

  const face = typeof fontFace === 'string' ? fontFace.trim() : '';
  if (face.length === 0) {
    throw new Error('autoFontSize(): fontFace is required as the 2nd positional argument.');
  }

  const hasAnyText =
    normalizeText(textOrRuns).trim().length > 0 ||
    (Array.isArray(textOrRuns) &&
      textOrRuns.some((run) => run && typeof run.text === 'string' && run.text.trim().length));

  const fontStyle = opts.italic === true || opts.fontStyle === 'italic' ? 'italic' : 'normal';
  const fontWeight =
    opts.bold === true || String(opts.fontWeight || '').toLowerCase() === 'bold' ? 'bold' : 'normal';
  const leading = toNumber(opts.leading, 1.15) || 1.15;

  const modeRaw = typeof opts.mode === 'string' ? opts.mode : 'auto';
  const mode = modeRaw.toLowerCase();
  const isShrink = mode === 'shrink';
  const isEnlarge = mode === 'enlarge';
  const isAuto = mode === 'auto';

  const refPtRaw = toNumber(opts.fontSize, NaN);
  const hasRefPt = Number.isFinite(refPtRaw);
  const refPt = hasRefPt ? refPtRaw : NaN;

  let minPt = toNumber(opts.minFontSize, NaN);
  let maxPt = toNumber(opts.maxFontSize, NaN);
  const userProvidedMax = Number.isFinite(maxPt);
  if (!Number.isFinite(minPt)) {
    minPt = 1;
  }
  if (!Number.isFinite(maxPt)) {
    maxPt = 1000;
  }

  if (isShrink || isEnlarge) {
    if (!hasRefPt) {
      throw new Error("autoFontSize(): mode 'shrink' or 'enlarge' requires fontSize");
    }
  }

  if (isShrink) {
    maxPt = Math.min(maxPt, refPt);
  } else if (isEnlarge) {
    minPt = Math.max(minPt, refPt);
  } else if (isAuto && hasRefPt && userProvidedMax) {
    // Auto mode with explicit max: honor bounds
  } else if (!isAuto) {
    throw new Error(
      `autoFontSize(): unsupported mode "${modeRaw}", expected "auto" | "shrink" | "enlarge"`
    );
  }

  if (!(maxPt > 0 && maxPt >= minPt)) {
    throw new Error('autoFontSize(): invalid minFontSize/maxFontSize bounds after normalization');
  }

  if (!hasAnyText) {
    const chosen = (hasRefPt && Math.max(minPt, Math.min(maxPt, refPt))) || minPt;
    const out = { ...opts, x, y, w, h, fontSize: chosen };
    if (isShrink) out.fit = 'shrink';
    return out;
  }

  const precision = 0.05;
  const safetyFactor = 0.97;

  let lo = minPt;
  let hi = maxPt;
  let best = lo;
  while (hi - lo > precision) {
    const mid = (lo + hi) / 2;
    const layout = calcTextBox(mid, {
      text: textOrRuns,
      w,
      fontFace: face,
      fontStyle,
      fontWeight,
      leading,
      margin: opts.margin,
      padding: opts.padding,
      paraSpaceAfter: opts.paraSpaceAfter,
    });
    const fits = layout.h <= h * safetyFactor + 1e-6;
    if (fits) {
      best = mid;
      lo = mid;
    } else {
      hi = mid;
    }
  }
  const finalPt = Math.max(minPt, Math.min(maxPt, best));

  const out = { ...opts, x, y, w, h, fontSize: finalPt };
  if (isShrink) out.fit = 'shrink';
  return out;
}

export function calcTextBox(fontSizePt: number, opts: TextBoxOpts = {}): TextBoxLayout {
  const textInput = opts.text ?? '';
  const text = normalizeText(textInput || '');
  const face =
    typeof opts.fontFace === 'string' && opts.fontFace.trim().length > 0 ? opts.fontFace.trim() : '';
  const fontStyle = opts.italic === true || opts.fontStyle === 'italic' ? 'italic' : 'normal';
  const fontWeight =
    opts.bold === true || String(opts.fontWeight || '').toLowerCase() === 'bold' ? 'bold' : 'normal';
  const leading = toNumber(opts.leading, 1.15) || 1.15;
  const padding = toNumber(opts.padding, 0.3);
  const paraSpaceAfterPt = toNumber(opts.paraSpaceAfter, 0) || 0;
  const lineHeightIn = (fontSizePt / 72) * leading;
  const margins = normalizeMargins(opts.margin);
  const measurer = TEXT_MEASURER;

  const hasLines = Number.isFinite(toNumber(opts.lines, NaN));
  const hasWidth = Number.isFinite(toNumber(opts.w, NaN));
  const hasHeight = Number.isFinite(toNumber(opts.h, NaN));
  const paragraphs = buildParagraphModels(textInput, {
    fontSizePt,
    fontFace: face,
    fontStyle,
    fontWeight,
    leading,
    paraSpaceAfterPt,
  });
  const hasAnyText = paragraphs.some((p) => p.text.length > 0);

  const topInsetIn = (fontSizePt / 72) * 0.2;

  if (hasLines) {
    const lines = toNumber(opts.lines, 1);
    const contentH = Math.max(0, lines * lineHeightIn + padding);
    const h = contentH + margins.top + margins.bottom;
    const passthrough = buildPassthroughOptions(opts, fontSizePt, margins);
    return {
      ...passthrough,
      w: toNumber(opts.w, NaN) || null,
      h,
      lines,
      contentH,
      margins,
      topInset: topInsetIn,
    };
  }

  if (hasWidth && hasAnyText) {
    if (face.length === 0) {
      throw new Error('calcTextBox(): opts.fontFace is required when measuring by width.');
    }
    const boxW = toNumber(opts.w, 0);
    if (!(boxW > 0)) throw new Error("calcTextBox(): width must be > 0 in mode 'width'");
    const innerW = Math.max(0, boxW - margins.left - margins.right);
    const { lines, heightIn } = layoutGivenWidth(paragraphs, innerW);
    const contentH = Math.max(0, heightIn + padding);
    const h = contentH + margins.top + margins.bottom;
    const passthrough = buildPassthroughOptions(opts, fontSizePt, margins);
    return {
      ...passthrough,
      w: boxW,
      h,
      lines,
      contentH,
      margins,
      topInset: topInsetIn,
    };
  }

  if (hasHeight && hasAnyText) {
    if (face.length === 0) {
      throw new Error('calcTextBox(): opts.fontFace is required when measuring by height.');
    }
    const boxH = toNumber(opts.h, 0);
    if (!(boxH > 0)) throw new Error("calcTextBox(): height must be > 0 in mode 'height'");
    const innerH = Math.max(0, boxH - margins.top - margins.bottom);
    const singleLineWidth = paragraphs.reduce((mx, p) => {
      const width = measureRunWidth(p, p.text) + p.textIndentIn;
      return Math.max(mx, width);
    }, 0);
    const minHeightOneLine = Math.max(
      0,
      paragraphs.reduce((sum, p, idx) => {
        const lineHeight = (p.fontSizePt / 72) * p.leading;
        sum += lineHeight;
        if (idx !== paragraphs.length - 1) sum += p.paraSpaceAfterIn;
        return sum;
      }, 0)
    );
    if (minHeightOneLine + padding - innerH > 1e-6) {
      throw new Error('calcTextBox(): height too small for one-line layout at this font size');
    }
    const longestTokenWidth = paragraphs.reduce((mx, p) => {
      const tokens = splitTextIntoTokens(p.text);
      for (const tk of tokens) {
        if (tk.length === 0) continue;
        const wIn = measureRunWidth(p, tk) + p.textIndentIn;
        if (wIn > mx) mx = wIn;
      }
      return mx;
    }, 0);
    let lo = Math.max(0.01, longestTokenWidth);
    let hi = Math.max(lo, singleLineWidth);
    let best = hi;
    for (let iter = 0; iter < 32; iter++) {
      const mid = (lo + hi) / 2;
      const { lines, heightIn } = layoutGivenWidth(paragraphs, mid);
      const totalH = heightIn + padding;
      if (totalH <= innerH + 1e-6) {
        best = mid;
        hi = mid;
      } else {
        lo = mid;
      }
    }
    const { lines, heightIn } = layoutGivenWidth(paragraphs, best);
    const contentH = heightIn + padding;
    const passthrough = buildPassthroughOptions(opts, fontSizePt, margins);
    return {
      ...passthrough,
      w: best + margins.left + margins.right,
      h: contentH + margins.top + margins.bottom,
      lines,
      contentH,
      margins,
      topInset: topInsetIn,
    };
  }

  throw new Error(
    'calcTextBox(): insufficient information. Provide {lines} or ({w,text}) or ({h,text}).'
  );
}

export function scale(min: number, max: number, density: any = {}): number {
  const bullets = density.bullets || 0;
  const textLength = density.textLength || 0;
  const bulletFactor = Math.min(Math.max(bullets / 8, 0), 1);
  const textFactor = Math.min(Math.max(textLength / 1500, 0), 1);
  const d = Math.max(bulletFactor, textFactor);
  const size = max - d * (max - min);
  return Math.round(size);
}

function layoutGivenWidth(
  paragraphs: any[],
  boxW: number
): { lines: number; heightIn: number } {
  let totalLines = 0;
  let heightIn = 0;
  for (let i = 0; i < paragraphs.length; i++) {
    const para = paragraphs[i];
    const widthScale = getWidthScaleForParagraph(para);
    const usableWidth = Math.max(0.01, boxW - para.textIndentIn) * widthScale;
    const lines = greedyWrap(para, usableWidth);
    const count = Math.max(1, lines.length);
    totalLines += count;
    const lineHeightIn = (para.fontSizePt / 72) * para.leading;
    heightIn += count * lineHeightIn;
    if (i !== paragraphs.length - 1) heightIn += para.paraSpaceAfterIn;
  }
  return { lines: totalLines, heightIn };
}

function greedyWrap(paragraph: any, maxWidthIn: number): string[] {
  const text = paragraph.text || '';
  if (text.length === 0) return [''];
  const breaker = new LineBreaker(text);
  const breakpoints: any[] = [];
  let bk;
  while ((bk = breaker.nextBreak())) {
    breakpoints.push({ pos: bk.position, required: bk.required });
  }
  const lines: string[] = [];
  let start = skipTextWhitespace(text, 0);
  let idx = 0;
  while (start < text.length) {
    while (idx < breakpoints.length && breakpoints[idx].pos <= start) idx++;
    let chosen = null;
    let probe = idx;
    while (probe < breakpoints.length) {
      const br = breakpoints[probe];
      const slice = text.slice(start, br.pos);
      const width = measureRunWidth(paragraph, trimLineEnd(slice));
      if (width <= maxWidthIn + 1e-6) {
        chosen = br;
        probe++;
        if (br.required) break;
      } else {
        break;
      }
    }
    if (!chosen) {
      const forced = forceBreakSegment(text, start, maxWidthIn, paragraph);
      if (forced.segment.length === 0) break;
      lines.push(trimLineEnd(forced.segment));
      start = skipTextWhitespace(text, forced.nextIndex);
      continue;
    }
    const lineText = text.slice(start, chosen.pos);
    lines.push(trimLineEnd(lineText));
    start = skipTextWhitespace(text, chosen.pos);
  }
  if (!lines.length) lines.push('');
  return lines;
}

function splitTextIntoTokens(text: string): string[] {
  if (typeof text !== 'string') return [''];
  const tokens = text.split(/(\s+)/);
  return tokens.length ? tokens : [''];
}

function trimLineEnd(value: string): string {
  return typeof value === 'string' ? value.replace(/\s+$/u, '') : '';
}

function measureRunWidth(paragraph: any, text: string): number {
  if (!text || text.length === 0) return 0;
  const fontData = getFontData(paragraph.fontFace, paragraph.fontStyle, paragraph.fontWeight);
  if (fontData && fontData.font) {
    const layout = fontData.font.layout(text);
    const widthPts = (layout.advanceWidth / fontData.font.unitsPerEm) * paragraph.fontSizePt;
    return Math.max(0, widthPts / 72);
  }
  return TEXT_MEASURER(text, paragraph.fontSizePt, paragraph.fontFace, paragraph.fontStyle, paragraph.fontWeight);
}

function forceBreakSegment(
  text: string,
  start: number,
  maxWidthIn: number,
  paragraph: any
): { segment: string; nextIndex: number } {
  const chars = Array.from(text.slice(start));
  if (chars.length === 0) return { segment: '', nextIndex: text.length };
  let buffer = '';
  let consumedUnits = 0;
  for (let i = 0; i < chars.length; i++) {
    const candidate = buffer + chars[i];
    const width = measureRunWidth(paragraph, trimLineEnd(candidate));
    if (width <= maxWidthIn + 1e-6) {
      buffer = candidate;
      consumedUnits += chars[i].length;
      continue;
    }
    if (buffer.length === 0) {
      buffer = chars[i];
      consumedUnits += chars[i].length;
    }
    break;
  }
  if (buffer.length === 0) {
    buffer = chars[0] || '';
    consumedUnits = buffer.length;
  }
  return { segment: buffer, nextIndex: start + consumedUnits };
}

function skipTextWhitespace(text: string, index: number): number {
  let idx = index;
  while (idx < text.length && /\s/.test(text[idx])) idx++;
  return idx;
}

function buildParagraphModels(textOrRuns: string | TextRun[], baseStyle: any): any[] {
  const entries = collectParagraphEntries(textOrRuns);
  if (entries.length === 0) {
    return [resolveParagraphStyle({ text: '' }, baseStyle)];
  }
  return entries.map((entry) => resolveParagraphStyle(entry, baseStyle));
}

function collectParagraphEntries(
  textOrRuns: string | TextRun[]
): Array<{ text: string; options?: any }> {
  const result: Array<{ text: string; options?: any }> = [];
  if (Array.isArray(textOrRuns)) {
    for (const entry of textOrRuns) {
      if (typeof entry === 'string') {
        pushParagraphSegments(entry, undefined, result);
      } else if (entry && typeof entry === 'object') {
        pushParagraphSegments(entry.text ?? '', entry.options || {}, result);
      }
    }
    return result;
  }
  pushParagraphSegments(textOrRuns ?? '', undefined, result);
  return result;
}

function pushParagraphSegments(text: string, options: any, target: any[]): void {
  const normalized = String(text ?? '');
  const parts = normalized.split(/\r?\n/);
  if (parts.length === 0) {
    target.push({ text: '', options });
    return;
  }
  for (const part of parts) {
    target.push({ text: part, options });
  }
}

function resolveParagraphStyle(entry: any, baseStyle: any): any {
  const opts = entry.options || {};
  const fontFace =
    (opts.fontFace && String(opts.fontFace).trim()) || baseStyle.fontFace || 'Arial';
  const fontStyle =
    opts.italic === true || opts.fontStyle === 'italic'
      ? 'italic'
      : baseStyle.fontStyle || 'normal';
  const fontWeight =
    opts.bold === true || String(opts.fontWeight || '').toLowerCase() === 'bold'
      ? 'bold'
      : baseStyle.fontWeight || 'normal';
  const fontSizePt = toNumber(opts.fontSize, baseStyle.fontSizePt) || baseStyle.fontSizePt;
  const leading = toNumber(opts.leading, baseStyle.leading) || baseStyle.leading || 1.15;
  const paraSpaceAfterPt =
    toNumber(opts.paraSpaceAfter, baseStyle.paraSpaceAfterPt) || baseStyle.paraSpaceAfterPt || 0;
  const hasBullet = !!opts.bullet;
  let indentPt = toNumber(opts.indent, NaN);
  if (!Number.isFinite(indentPt) && hasBullet) {
    indentPt = toNumber(opts.bullet.indent, NaN);
  }
  if (!Number.isFinite(indentPt)) indentPt = 0;
  const hangingPt = toNumber(opts.hanging, 0) || 0;
  let textIndentIn = 0;
  if (indentPt > 0) {
    if (hasBullet) {
      textIndentIn = indentPt / 72;
    } else {
      textIndentIn = Math.max(0, (indentPt - hangingPt) / 72);
    }
  }
  return {
    text: entry.text || '',
    fontFace,
    fontStyle,
    fontWeight,
    fontSizePt,
    leading,
    paraSpaceAfterIn: paraSpaceAfterPt / 72,
    textIndentIn,
  };
}

function getFontData(face: string, fontStyle: string, fontWeight: string): any {
  const key = makeFontCacheKey(face, fontStyle, fontWeight);
  if (fontKitCache.has(key)) return fontKitCache.get(key);
  const fontPath = findFontPath(face, fontStyle, fontWeight);
  if (!fontPath) {
    fontKitCache.set(key, null);
    return null;
  }
  try {
    let font = fontkit.openSync(fontPath);
    if (font && typeof font.fonts === 'object') {
      font = selectCollectionFont(font, fontStyle, fontWeight);
    }
    if (!font || typeof font.layout !== 'function') {
      fontKitCache.set(key, null);
      return null;
    }
    registerCanvasFontVariant(fontPath, face, fontStyle, fontWeight, key);
    const payload = { font, path: fontPath };
    fontKitCache.set(key, payload);
    return payload;
  } catch (err) {
    fontKitCache.set(key, null);
    return null;
  }
}

function makeFontCacheKey(face: string, fontStyle: string, fontWeight: string): string {
  const family = (face || 'Arial').trim();
  const style = (fontStyle || 'normal').toLowerCase();
  const weight = (fontWeight || 'normal').toLowerCase();
  return `${family}::${style}::${weight}`;
}

function registerCanvasFontVariant(
  fontPath: string,
  face: string,
  fontStyle: string,
  fontWeight: string,
  cacheKey: string
): void {
  if (registeredFontVariants.has(cacheKey)) return;
  try {
    Canvas.registerFont(fontPath, {
      family: face,
      style: fontStyle || 'normal',
      weight: fontWeight || 'normal',
    });
    registeredFontVariants.add(cacheKey);
  } catch (err) {
    // ignore registration failure
  }
}

function findFontPath(face: string, fontStyle: string, fontWeight: string): string | null {
  const family = (face || '').trim();
  if (family.length === 0) return null;
  const key = makeFontCacheKey(family, fontStyle, fontWeight);
  if (fontPathCache.has(key)) return fontPathCache.get(key) || null;
  const styleParts: string[] = [];
  if ((fontWeight || '').toLowerCase() === 'bold') styleParts.push('Bold');
  if ((fontStyle || '').toLowerCase() === 'italic') styleParts.push('Italic');
  const styleQuery = styleParts.length > 0 ? `:style=${styleParts.join(' ')}` : '';
  const query = `${family}${styleQuery}`;
  const result = spawnSync('fc-match', ['-f', '%{file}', query], {
    encoding: 'utf8',
  });
  if (result.status === 0) {
    const output = String(result.stdout || '').trim();
    if (output.length > 0) {
      fontPathCache.set(key, output);
      return output;
    }
  }
  fontPathCache.set(key, null);
  return null;
}

function selectCollectionFont(collection: any, fontStyle: string, fontWeight: string): any {
  const fonts = collection.fonts || [];
  if (fonts.length === 0) return null;
  const wantItalic = (fontStyle || '').toLowerCase() === 'italic';
  const wantBold = (fontWeight || '').toLowerCase() === 'bold';
  let best = fonts[0];
  let bestScore = scoreFontVariant(best, wantItalic, wantBold);
  for (let i = 1; i < fonts.length; i++) {
    const candidate = fonts[i];
    const score = scoreFontVariant(candidate, wantItalic, wantBold);
    if (score > bestScore) {
      best = candidate;
      bestScore = score;
    }
  }
  return best;
}

function scoreFontVariant(font: any, wantItalic: boolean, wantBold: boolean): number {
  if (!font) return -1;
  const name = String(font.fullName || font.postscriptName || '').toLowerCase();
  const isItalic = /italic|oblique/.test(name);
  const isBold = /bold|black|heavy|semibold|extrabold/.test(name);
  let score = 0;
  if (isItalic === wantItalic) score += 1;
  if (isBold === wantBold) score += 1;
  return score;
}

function getWidthScaleForParagraph(paragraph: any): number {
  if (!paragraph || typeof paragraph.text !== 'string') return 1;
  const text = paragraph.text;
  if (/[ก-๛]/u.test(text)) {
    return 1.2;
  }
  if (/[\u0600-\u06FF]/u.test(text)) {
    return 0.97;
  }
  return 0.985;
}

function buildPassthroughOptions(opts: any, fontSizePt: number, margins: any): any {
  const exclude = new Set(['text', 'lines', 'w', 'h', 'leading', 'padding']);
  const out: any = {};
  for (const k of Object.keys(opts)) {
    if (!exclude.has(k)) out[k] = opts[k];
  }
  if (out.fontSize == null) out.fontSize = fontSizePt;
  if (opts.margin != null) out.margin = margins;
  return out;
}

function getTextMeasurer(): Function {
  const canvas = new Canvas(2, 2);
  const ctx = canvas.getContext('2d');
  const PX_PER_IN = 96;
  return (text: string, fontSizePt: number, fontFace: string, fontStyle: string, fontWeight: string) => {
    const px = (fontSizePt / 72) * PX_PER_IN;
    const style = fontStyle || 'normal';
    const weight = fontWeight || 'normal';
    ctx.font = `${style} ${weight} ${px}px ${fontFace || 'Arial'}`;
    const metrics = ctx.measureText(text);
    return (metrics.width || 0) / PX_PER_IN;
  };
}

function normalizeMargins(m: any): { left: number; right: number; top: number; bottom: number } {
  const toInches = (value: any) =>
    typeof value === 'number' && Number.isFinite(value) ? value / 72 : 0;
  if (m && typeof m === 'object') {
    if (Number.isFinite(m.left) || Number.isFinite(m.top)) {
      return {
        left: toInches(m.left),
        right: toInches(m.right),
        top: toInches(m.top),
        bottom: toInches(m.bottom),
      };
    }
  }
  const all = toInches(m);
  return { left: all, right: all, top: all, bottom: all };
}

function normalizeText(textOrRuns: string | TextRun[]): string {
  if (Array.isArray(textOrRuns)) {
    return textOrRuns
      .map((item) => {
        if (typeof item === 'string') return item;
        if (item && typeof item.text === 'string') return item.text;
        return '';
      })
      .join('');
  }
  return typeof textOrRuns === 'string' ? textOrRuns : String(textOrRuns ?? '');
}

function toNumber(v: any, fallback: any): any {
  const n = typeof v === 'string' ? parseFloat(v) : v;
  return Number.isFinite(n) ? n : fallback;
}
