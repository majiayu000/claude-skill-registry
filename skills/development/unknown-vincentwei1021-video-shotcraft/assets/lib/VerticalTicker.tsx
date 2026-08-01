// origin: vibe-motion/skills remotion-3d-ticker assets/VerticalTicker.tsx
//         (2026-07-13 扫描，2026-07-15 吸收；改动：items 泛化为 ReactNode、
//          遮罩高度/透视角/scale/列宽/间距提为 props)
import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';

export interface TickerColumn {
  /** Column content — any ReactNode (screenshot-slice divs, <Img>, text cards…) */
  items: React.ReactNode[];
  /** Seconds for one full loop (one copy of items scrolling its own height) */
  durationInSeconds: number;
  /** -1 scrolls up, 1 scrolls down */
  direction: -1 | 1;
}

export interface VerticalTickerProps {
  columns: TickerColumn[];
  /** Background color, also used by the top/bottom fade masks */
  backgroundColor?: string;
  /** Height of each fade mask in px */
  maskHeight?: number;
  /** rotateX tilt of the whole wall, degrees */
  tiltDeg?: number;
  /** CSS perspective distance in px */
  perspective?: number;
  /** Overall scale of the tilted wall (compensates perspective shrink) */
  scale?: number;
  /** Column width in px */
  columnWidth?: number;
  /** Gap between columns and between items within a column, px */
  gap?: number;
}

/**
 * 3D 透视多列无限纵向滚动墙。每列 [...items, ...items] 翻倍 +
 * progress 取模 translateY 0→-50%：前半段恰好滚出视口时归零，
 * 后半段与前半段像素级一致，循环点不可见。
 * 接缝无痕的前提：-50% 必须恰等于单副本周期（内容高 + n 个 gap）。
 * 源实现用 flex gap（翻倍后只有 2n-1 个 gap）会差 gap/2 px 跳一下，
 * 这里改为每项 marginBottom = gap，容器高恰为周期两倍。
 */
export const VerticalTicker: React.FC<VerticalTickerProps> = ({
  columns,
  backgroundColor = '#000',
  maskHeight = 200,
  tiltDeg = 20,
  perspective = 1000,
  scale = 1.2,
  columnWidth = 400,
  gap = 30,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor, overflow: 'hidden' }}>
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          justifyContent: 'center',
          gap,
          transform: `perspective(${perspective}px) rotateX(${tiltDeg}deg) scale(${scale})`,
          transformOrigin: 'center center',
        }}
      >
        {columns.map((col, idx) => (
          <Column key={idx} {...col} width={columnWidth} gap={gap} />
        ))}
      </div>
      {/* Fade masks sit above the wall so rows enter/exit softly */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: maskHeight,
          background: `linear-gradient(to bottom, ${backgroundColor} 0%, transparent 100%)`,
          zIndex: 10,
        }}
      />
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: maskHeight,
          background: `linear-gradient(to top, ${backgroundColor} 0%, transparent 100%)`,
          zIndex: 10,
        }}
      />
    </AbsoluteFill>
  );
};

const Column: React.FC<TickerColumn & { width: number; gap: number }> = ({
  items,
  durationInSeconds,
  direction,
  width,
  gap,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const loopFrames = durationInSeconds * fps;
  const progress = (frame % loopFrames) / loopFrames;
  // up: 0 → -50%; down: -50% → 0（起点即偏移半程，首帧无空白）
  const translateY = direction === -1 ? progress * -50 : -50 + progress * 50;

  return (
    <div style={{ width, height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          transform: `translateY(${translateY}%)`,
          willChange: 'transform',
        }}
      >
        {[...items, ...items].map((node, i) => (
          <div key={i} style={{ marginBottom: gap }}>
            {node}
          </div>
        ))}
      </div>
    </div>
  );
};
