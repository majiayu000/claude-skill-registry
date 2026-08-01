// origin: 模板片源仓库 helpers
/**
 * Deterministic hand-held camera noise. Layered sines at incommensurate
 * frequencies read as organic drift; amplitude in world units.
 */
export const handheld = (frame: number, amp = 0.012): [number, number, number] => [
  amp * (Math.sin(frame * 0.31) + 0.6 * Math.sin(frame * 0.83 + 1.7)),
  amp * (Math.sin(frame * 0.47 + 0.9) + 0.5 * Math.sin(frame * 1.13 + 3.1)),
  0,
];
