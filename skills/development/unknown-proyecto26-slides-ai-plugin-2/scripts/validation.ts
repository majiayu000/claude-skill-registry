import type { ValidationReport, ValidationIssue } from './types.js';

const MIN_FONT_SIZE = 14;
const MAX_BULLETS_PER_SLIDE = 6;

export function validateDeck(
  pptx: any,
  opts: Record<string, any> = {}
): ValidationReport {
  const issues: ValidationIssue[] = [];
  const warnings: ValidationIssue[] = [];
  const slides = (pptx && pptx._slides) || [];
  let totalFontSizes: number[] = [];

  slides.forEach((slide: any, idx: number) => {
    const slideNum = idx + 1;
    const objects = slide._slideObjects || [];

    // Check speaker notes
    const notes = slide._slideNotes || '';
    if (!notes || notes.trim().length === 0) {
      warnings.push({
        slide: slideNum,
        type: 'missing_notes',
        message: `Slide ${slideNum}: no speaker notes`,
        severity: 'medium',
      });
    }

    let bulletCount = 0;
    objects.forEach((obj: any, objIdx: number) => {
      const data = obj.data || obj.options || {};
      const fontSize = data.fontSize;
      if (typeof fontSize === 'number') {
        totalFontSizes.push(fontSize);
        if (fontSize < MIN_FONT_SIZE) {
          issues.push({
            slide: slideNum,
            type: 'font_too_small',
            message: `Slide ${slideNum}, element ${objIdx}: font size ${fontSize}pt < ${MIN_FONT_SIZE}pt minimum`,
            severity: 'high',
          });
        }
      }
      if (
        data.bullet ||
        (Array.isArray(data.text) && data.text.some((t: any) => t.options && t.options.bullet))
      ) {
        bulletCount++;
      }
    });

    if (bulletCount > MAX_BULLETS_PER_SLIDE) {
      issues.push({
        slide: slideNum,
        type: 'too_many_bullets',
        message: `Slide ${slideNum}: ${bulletCount} bullets exceeds max ${MAX_BULLETS_PER_SLIDE}`,
        severity: 'medium',
      });
    }

    const slideW = 10;
    const slideH = 5.625;
    objects.forEach((obj: any, objIdx: number) => {
      const d = obj.data || obj.options || {};
      const x = d.x || 0;
      const y = d.y || 0;
      const w = d.w || 0;
      const h = d.h || 0;
      if (x + w > slideW + 0.01 || y + h > slideH + 0.01) {
        warnings.push({
          slide: slideNum,
          type: 'out_of_bounds',
          message: `Slide ${slideNum}, element ${objIdx}: extends beyond slide boundary`,
          severity: 'low',
        });
      }
    });
  });

  const avgFontSize =
    totalFontSizes.length > 0
      ? totalFontSizes.reduce((a, b) => a + b, 0) / totalFontSizes.length
      : 0;
  const minFontSize = totalFontSizes.length > 0 ? Math.min(...totalFontSizes) : 0;

  return {
    passed: issues.length === 0,
    issues,
    warnings,
    stats: {
      slideCount: slides.length,
      avgFontSize: Math.round(avgFontSize * 10) / 10,
      minFontSize,
      hasNotes: warnings.filter((w) => w.type === 'missing_notes').length === 0,
    },
  };
}

export { MIN_FONT_SIZE, MAX_BULLETS_PER_SLIDE };
