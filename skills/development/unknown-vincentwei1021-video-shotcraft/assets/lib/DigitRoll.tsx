// origin: template/src/aifl/DigitRoll.tsx（模板片同源组件）
import { interpolate, useCurrentFrame, Easing } from 'remotion';

const DIGITS = '0123456789';

/** Odometer-style digit column roll for monospace numerals. */
export const DigitRoll: React.FC<{
  value: string;
  delay?: number;
  fontSize?: number;
  color?: string;
}> = ({ value, delay = 0, fontSize = 30, color = 'oklch(52% 0.115 65)' }) => {
  const frame = useCurrentFrame();
  const lineH = fontSize * 1.15;
  return (
    <span style={{ display: 'inline-flex', overflow: 'hidden', height: lineH, verticalAlign: 'bottom' }}>
      {value.split('').map((ch, i) => {
        const target = DIGITS.indexOf(ch);
        if (target < 0) {
          return (
            <span key={i} style={{ fontSize, lineHeight: `${lineH}px`, color }}>{ch}</span>
          );
        }
        const t = interpolate(frame, [delay + i * 4, delay + i * 4 + 22], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.bezier(0.25, 0.8, 0.25, 1),
        });
        // roll through one full strip then land on the target digit
        const offset = (10 + target) * t * lineH;
        return (
          <span key={i} style={{ display: 'inline-block', height: lineH }}>
            <span style={{ display: 'block', transform: `translateY(${-offset}px)` }}>
              {(DIGITS + DIGITS).split('').map((d, j) => (
                <span key={j} style={{ display: 'block', fontSize, lineHeight: `${lineH}px`, color, fontVariantNumeric: 'tabular-nums' }}>
                  {d}
                </span>
              ))}
            </span>
          </span>
        );
      })}
    </span>
  );
};
