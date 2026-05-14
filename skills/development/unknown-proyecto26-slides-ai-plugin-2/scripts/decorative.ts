import { normalizeColor } from './util.js';
import type { SlideTheme, StaircaseOpts, BadgeOpts, ProgressBarOpts } from './types.js';

export function addStaircase(slide: any, opts: StaircaseOpts = {}): void {
  const position = opts.position || 'bottom-right';
  const color = opts.color || '4a9eff';
  const steps = opts.steps || 4;
  const stepW = opts.stepWidth || 0.4;
  const stepH = opts.stepHeight || 0.3;
  const opacity = opts.opacity || 0.15;
  const isRight = position.includes('right');
  const isBottom = position.includes('bottom');
  const slideW = 10;
  const slideH = 5.625;

  for (let i = 0; i < steps; i++) {
    const w = stepW * (steps - i);
    const h = stepH * (i + 1);
    const x = isRight ? slideW - w : 0;
    const y = isBottom ? slideH - h : 0;
    slide.addShape('rect', {
      x,
      y,
      w,
      h,
      fill: { color: normalizeColor(color), transparency: (1 - opacity) * 100 },
    });
  }
}

export function addSectionBadge(
  slide: any,
  text: string,
  position: BadgeOpts = {},
  theme: SlideTheme
): void {
  const { x = 0.5, y = 0.3 } = position;
  const badgeW = Math.max(text.length * 0.12 + 0.3, 1.2);
  const badgeH = 0.3;
  slide.addShape('roundRect', {
    x,
    y,
    w: badgeW,
    h: badgeH,
    fill: { color: theme.accent, transparency: 80 },
    rectRadius: theme.radius.badge,
  });
  slide.addText(text, {
    x,
    y,
    w: badgeW,
    h: badgeH,
    fontSize: 10,
    fontFace: theme.font.body,
    color: theme.accent,
    bold: true,
    align: 'center',
    valign: 'middle',
  });
}

export function addProgressBar(
  slide: any,
  current: number,
  total: number,
  theme: SlideTheme,
  opts: ProgressBarOpts = {}
): void {
  const position = opts.position || 'bottom';
  const barH = opts.height || 0.04;
  const slideW = 10;
  const y = position === 'top' ? 0 : 5.625 - barH;
  const progress = current / total;
  slide.addShape('rect', {
    x: 0,
    y,
    w: slideW,
    h: barH,
    fill: { color: theme.bg.secondary },
  });
  slide.addShape('rect', {
    x: 0,
    y,
    w: slideW * progress,
    h: barH,
    fill: { color: theme.accent },
  });
}

export function addSectionDivider(slide: any, heading: string, theme: SlideTheme): void {
  slide.addShape('rect', {
    x: 0,
    y: 0,
    w: 10,
    h: 5.625,
    fill: { color: theme.bg.secondary },
  });
  slide.addText(heading, {
    x: 0.5,
    y: 1.5,
    w: 9,
    h: 2,
    fontSize: 40,
    fontFace: theme.font.heading,
    color: theme.text.primary,
    bold: true,
    align: 'center',
    valign: 'middle',
  });
}

export function addSlideNumber(
  slide: any,
  number: number,
  total: number,
  theme: SlideTheme,
  opts: any = {}
): void {
  const { x = 9.2, y = 5.2, w = 0.6, h = 0.3 } = opts;
  slide.addText(`${number} / ${total}`, {
    x,
    y,
    w,
    h,
    fontSize: 10,
    fontFace: theme.font.body,
    color: theme.text.secondary,
    align: 'right',
    valign: 'bottom',
  });
}
