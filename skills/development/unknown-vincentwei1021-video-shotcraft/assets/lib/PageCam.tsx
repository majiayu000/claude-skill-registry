// origin: template/src/aifl/live/PageCam.tsx（模板片同源组件）
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, Easing } from 'remotion';

export type CamKey = {
  frame: number;
  cx: number;
  cy: number;
  zoom: number;
  rotX?: number; // deg, tilt about the horizontal axis (positive = top leans away, like looking at a table)
  rotY?: number; // deg, tilt about the vertical axis (positive = right edge recedes, i.e. seen from the LEFT)
  rotZ?: number; // deg, in-plane roll
  persp?: number; // px, perspective strength (default 1400; smaller = stronger)
};

const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/**
 * 2.5D camera over a full-page screenshot. (cx, cy) is the page-space CSS
 * point centered in the 1920x1080 viewport; zoom is scale (1 = 1 CSS px
 * -> 1 output px). Page textures are 2x, rendered at CSS size via width.
 *
 * Optional 3D: keys may carry rotX/rotZ/persp to tilt the page like a plane
 * seen from an oblique camera. When NO key declares any 3D field, the markup
 * degrades to the original flat pan/zoom and renders pixel-identical.
 *
 * Optional DOF: a screen-space gradient-blur band approximating a focal plane
 * near `focusY` (blurring the far/top part of a tilted page).
 */
export const PageCam: React.FC<{
  src: string; // staticFile path under textures/live/
  pageH: number; // CSS page height
  keys: CamKey[];
  children?: React.ReactNode; // page-space overlays (positioned in CSS px)
  blur?: number;
  saturate?: number;
  ease?: (t: number) => number;
  dof?: { focusY: number; strength: number };
  // Optional absolute-frame override: when PageCam is rendered inside a
  // <Sequence> (which rebases useCurrentFrame), the parent can pass the
  // restored absolute comp frame so CAM_KEYS keep their absolute frame refs.
  frame?: number;
}> = ({ src, pageH, keys, children, blur = 0, saturate = 1, ease = Easing.bezier(0.33, 0, 0.15, 1), dof, frame: frameProp }) => {
  const ownFrame = useCurrentFrame();
  const frame = frameProp ?? ownFrame;
  // find segment
  let a = keys[0], b = keys[keys.length - 1];
  for (let i = 0; i < keys.length - 1; i++) {
    if (frame >= keys[i].frame && frame <= keys[i + 1].frame) { a = keys[i]; b = keys[i + 1]; break; }
  }
  const t = a.frame === b.frame ? 1 : interpolate(frame, [a.frame, b.frame], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease,
  });
  const cx = lerp(a.cx, b.cx, t);
  const cy = lerp(a.cy, b.cy, t);
  const zoom = lerp(a.zoom, b.zoom, t);

  const filters: string[] = [];
  if (blur > 0) filters.push(`blur(${blur}px)`);
  if (saturate !== 1) filters.push(`saturate(${saturate})`);

  // Does any key request 3D? If not, keep the original flat markup exactly.
  const has3D = keys.some((k) => k.rotX !== undefined || k.rotY !== undefined || k.rotZ !== undefined || k.persp !== undefined);

  if (!has3D) {
    return (
      <AbsoluteFill style={{ overflow: 'hidden', backgroundColor: '#faf7f2' }}>
        <div
          style={{
            position: 'absolute', width: 1920, height: pageH,
            transform: `translate(${960 - cx * zoom}px, ${540 - cy * zoom}px) scale(${zoom})`,
            transformOrigin: '0 0',
            filter: filters.length ? filters.join(' ') : undefined,
          }}
        >
          <Img src={staticFile(src)} style={{ position: 'absolute', width: 1920, height: pageH }} />
          {children}
        </div>
      </AbsoluteFill>
    );
  }

  // 3D mode: pivot rotation/scale about the focal page-point (cx, cy) so it
  // stays centered in the viewport. With rotX=rotZ=0 this reduces to the flat
  // transform (proven identical: (960,540) + zoom*(p - (cx,cy))).
  const rotX = lerp(a.rotX ?? 0, b.rotX ?? 0, t);
  const rotY = lerp(a.rotY ?? 0, b.rotY ?? 0, t);
  const rotZ = lerp(a.rotZ ?? 0, b.rotZ ?? 0, t);
  const persp = lerp(a.persp ?? 1400, b.persp ?? 1400, t);

  return (
    <AbsoluteFill style={{ overflow: 'hidden', backgroundColor: '#faf7f2' }}>
      <div
        style={{
          position: 'absolute', inset: 0,
          perspective: `${persp * zoom}px`,
          perspectiveOrigin: '960px 540px',
        }}
      >
        {/* LAYOUT-SCALE zoom: instead of scale(zoom) in the transform chain (which
            makes Chromium rasterize the 3D-composited layer at 1920-wide LAYOUT
            size and then GPU-upscale by zoom — everything inside gets downsampled
            before magnification, hence blurry text), we apply the magnification as
            the CSS `zoom` property. `zoom` enlarges the layout box itself, so the
            page + card textures rasterize at the ENLARGED device size and sample
            down from their hi-res sources → sharp glyph edges under perspective.

            Coordinate math: `zoom` scales this element's local coordinate space by
            `zoom`, so a page point (cx,cy) renders at (cx*zoom, cy*zoom) device px
            from the box origin, and a `translate(Tx px)` renders as Tx*zoom device
            px. To land the focal point (cx,cy) at viewport centre (960,540):
              cx*zoom + Tx*zoom = 960  ⟹  Tx = 960/zoom - cx  (likewise Ty).
            Rotations pivot about transform-origin (cx,cy) = the focal point, so
            they leave its screen position unchanged. With rot=0 this reduces to
            translate(960/zoom - cx, 540/zoom - cy) under zoom — identical framing
            to the old scale-based transform, just rasterized at layout scale. */}
        <div
          style={{
            position: 'absolute', width: 1920, height: pageH,
            zoom,
            transform: `translate(${960 / zoom - cx}px, ${540 / zoom - cy}px) rotateY(${rotY}deg) rotateX(${rotX}deg) rotateZ(${rotZ}deg)`,
            transformOrigin: `${cx}px ${cy}px`,
            transformStyle: 'preserve-3d',
            filter: filters.length ? filters.join(' ') : undefined,
          }}
        >
          <Img src={staticFile(src)} style={{ position: 'absolute', width: 1920, height: pageH }} />
          {children}
        </div>
      </div>

      {/* Depth-of-field approximation: a top-band gradient blur (far part of a
          tilted page reads soft). Screen-space, over the page. */}
      {dof ? (
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: 0,
            height: Math.max(0, dof.focusY),
            backdropFilter: `blur(${dof.strength}px)`,
            WebkitBackdropFilter: `blur(${dof.strength}px)`,
            maskImage: 'linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 45%, rgba(0,0,0,0) 100%)',
            WebkitMaskImage: 'linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 45%, rgba(0,0,0,0) 100%)',
            pointerEvents: 'none',
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};
