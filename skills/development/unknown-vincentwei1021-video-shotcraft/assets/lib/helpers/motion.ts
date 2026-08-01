// origin: disney-animation-rule-skill implementation-patterns (scanned 2026-07-13, absorbed 2026-07-15)

/**
 * Motion-derived signal: sample a pure trajectory at frame±dt (central
 * difference) to get velocity, speed and heading. Drive stretch, smear,
 * blur or shake intensity from `speed`; normalize amplitude by subject
 * size. Works on any pure `posAt` — no per-frame state.
 */
export const velocityAt = (
  posAt: (f: number) => { x: number; y: number },
  frame: number,
  dt = 0.5,
): { vx: number; vy: number; speed: number; direction: number } => {
  const before = posAt(frame - dt);
  const after = posAt(frame + dt);
  const vx = (after.x - before.x) / (2 * dt);
  const vy = (after.y - before.y) / (2 * dt);
  return { vx, vy, speed: Math.hypot(vx, vy), direction: Math.atan2(vy, vx) };
};

/**
 * Follow-through without stateful simulation: a trailing layer is just the
 * primary state sampled at `frame − delayFrames`. Build drag hierarchies by
 * giving each attachment a larger delay and a smaller amplitude (shadow 2f,
 * ghost 4f, …). Never accumulate state across rendered frames — every layer
 * stays a pure function of the frame number.
 */
export const lagged = <T>(
  stateAt: (f: number) => T,
  frame: number,
  delayFrames: number,
): T => stateAt(frame - delayFrames);

/**
 * Closed-form damped oscillation for recoil/settle tails, t in frames from
 * impact. Returns a signed offset factor decaying to 0; scale by the desired
 * peak amplitude. freq in cycles/frame (~0.1), damping per frame (~0.15).
 */
export const dampedSettle = (t: number, freq: number, damping: number): number =>
  t <= 0 ? 0 : Math.exp(-damping * t) * Math.sin(2 * Math.PI * freq * t);
