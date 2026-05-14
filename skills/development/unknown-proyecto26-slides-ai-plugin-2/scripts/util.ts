import type { ColorHex, ShadowConfig } from './types.js';

const EMU_PER_INCH = 914400;

export function safeOuterShadow(
  color: ColorHex = '000000',
  opacity: number = 0.25,
  angle: number = 45,
  blur: number = 3,
  offset: number = 2
): ShadowConfig {
  return { type: 'outer', color, opacity, angle, blur, offset };
}

export function inchesToEmu(inches: number): number {
  return Math.round(inches * EMU_PER_INCH);
}

export function emuToInches(emu: number): number {
  return emu / EMU_PER_INCH;
}

export function normalizeColor(color: unknown): ColorHex {
  if (typeof color !== 'string') throw new Error(`Invalid color: ${color}`);
  const hex = color.replace(/^#/, '');
  if (!/^[0-9a-fA-F]{3,8}$/.test(hex)) throw new Error(`Invalid hex color: ${color}`);
  return hex as ColorHex;
}

export function clampValue(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

export { EMU_PER_INCH };
