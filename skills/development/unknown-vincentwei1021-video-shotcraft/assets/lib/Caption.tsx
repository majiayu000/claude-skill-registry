// origin: template/src/aifl/Caption.tsx（模板片同源组件）
import { interpolate, useCurrentFrame } from 'remotion';

const MONO = 'ui-monospace, SFMono-Regular, Menlo, monospace';
const AMBER = 'oklch(52% 0.115 65)';

/** Screen-space narration caption: a mono UI info-strip at the bottom of the
 * frame, led by a small amber square. Fades/rises in over 8 frames and fades
 * out over the last 8 of its window. */
export const Caption: React.FC<{ text: string; duration: number; bottom?: number }> = ({
  text,
  duration,
  bottom = 72,
}) => {
  const frame = useCurrentFrame();
  const inT = interpolate(frame, [0, 8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const outT = interpolate(frame, [duration - 8, duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'baseline',
        gap: 14,
        fontFamily: MONO,
        fontSize: 22,
        letterSpacing: '0.14em',
        textTransform: 'uppercase',
        color: 'oklch(45% 0.006 82)',
        opacity: inT * outT,
        transform: `translateY(${(1 - inT) * 8}px)`,
        pointerEvents: 'none',
      }}
    >
      <span style={{ width: 6, height: 6, background: AMBER, display: 'inline-block' }} />
      <span>{text}</span>
    </div>
  );
};
