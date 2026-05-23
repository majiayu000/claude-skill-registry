---
name: ta-ui-polish
description: UI and visual polish checklist for game presentation. Use when adding final polish, styling, animations, visual feedback.
category: ui
---

# Visual Polish Skill

> "The last 10% of polish takes 90% of the time – but it's worth it."

## When to Use This Skill

Use when:

- Finalizing visual presentation
- Creating UI elements and HUD
- Adding feedback animations
- Implementing transitions

## Polish Checklist

### Core Visuals

- [ ] **Lighting is balanced** - No blown highlights, no crushed shadows
- [ ] **Colors match GDD palette** - Consistent art direction
- [ ] **Materials look correct** - PBR values appropriate for materials
- [ ] **Silhouette is readable** - Objects identifiable from outline
- [ ] **Framing guides the eye** - Important elements draw attention

### Animation & Feedback

- [ ] **Buttons have hover states** - Visual feedback on interaction
- [ ] **Transitions are smooth** - No jarring cuts
- [ ] **Loading states exist** - User knows something is happening
- [ ] **Error states are clear** - Problems are visible and understandable
- [ ] **Success feedback exists** - Positive reinforcement
- [ ] **Connection status visible** - Multiplayer shows network state

---

## Connection Status UI Pattern (Multiplayer)

**CRITICAL for multiplayer games:** Players need to see connection state and network quality.

### States to Indicate

| State      | Visual Indicator                    | Color     | Animation    |
| ---------- | ----------------------------------- | --------- | ------------ |
| Connecting | Spinner + "Connecting..." text      | Yellow    | Rotate       |
| Connected  | Checkmark icon + ping in ms         | Green     | Pulse (subtle) |
| Disconnected | X icon + "Disconnected" text      | Red       | Blink        |
| Reconnecting | Spinner + "Reconnecting..."      | Orange    | Rotate       |

### Ping Quality Color Coding

```tsx
function PingIndicator({ ping }: { ping: number }) {
  const getPingColor = (ping: number) => {
    if (ping < 50) return '#22c55e';  // Green
    if (ping < 100) return '#eab308'; // Yellow
    return '#ef4444';                  // Red
  };

  const getPingStatus = (ping: number) => {
    if (ping < 50) return 'Excellent';
    if (ping < 100) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="ping-indicator" style={{ color: getPingColor(ping) }}>
      <WifiIcon className={`animate-pulse ${ping > 100 ? 'animate-ping' : ''}`} />
      <span>{ping}ms</span>
      <span className="status">{getPingStatus(ping)}</span>
    </div>
  );
}
```

### Implementation Example

```tsx
// ConnectionStatus.tsx
import { useEffect, useState } from 'react';
import { useConnectionStore } from '@/store/connectionStore';

export function ConnectionStatus() {
  const { connected, connecting, roomId } = useConnectionStore();
  const [ping, setPing] = useState(0);

  // Measure ping every second
  useEffect(() => {
    if (!connected) return;

    const interval = setInterval(async () => {
      const start = performance.now();
      // Send ping to server and await response
      await fetch('/api/ping');
      setPing(Math.round(performance.now() - start));
    }, 1000);

    return () => clearInterval(interval);
  }, [connected]);

  if (connecting) {
    return (
      <div className="connection-status connecting">
        <Spinner className="animate-spin" />
        <span>Connecting...</span>
      </div>
    );
  }

  if (!connected) {
    return (
      <div className="connection-status disconnected">
        <XIcon className="animate-pulse" />
        <span>Disconnected</span>
      </div>
    );
  }

  const pingColor = ping < 50 ? 'green' : ping < 100 ? 'yellow' : 'red';

  return (
    <div className="connection-status connected">
      <CheckIcon className="text-green-500" />
      <span>Connected</span>
      <span className={`ping ping-${pingColor}`}>{ping}ms</span>
    </div>
  );
}
```

### Placement in HUD

```
┌─────────────────────────────────────────────────────┐
│                              [Connection: ● 45ms] │
│  Health: 100█████████████                           │
│  Armor:  50█████                                    │
│                                  [Alive: 42/64]     │
└─────────────────────────────────────────────────────┘
```

### Icon Patterns

| Icon          | When to Use              | Styling                      |
| ------------- | ------------------------ | ---------------------------- |
| Spinner       | Connecting, Reconnecting | `animate-spin` rotation      |
| Checkmark     | Connected                | Green, subtle pulse          |
| X mark        | Disconnected             | Red, `animate-ping` blink     |
| Warning       | High ping (>100ms)       | Yellow, `animate-pulse`       |
| Wifi bars     | Signal strength          | 3-4 bars based on ping       |

### UI Presentation

- [ ] **Typography is readable** - Appropriate sizes, weights, line heights
- [ ] **Contrast meets accessibility** - WCAG AA minimum (4.5:1 for text)
- [ ] **Spacing is consistent** - Grid/spacing system used
- [ ] **Alignment is intentional** - Elements line up properly
- [ ] **Hierarchy is clear** - Most important elements stand out

### Performance Polish

- [ ] **No visible frame drops** - 60 FPS maintained
- [ ] **Loading times are acceptable** - Assets optimized
- [ ] **Memory usage is stable** - No leaks or growing allocation
- [ ] **Mobile tested** - Works on target mobile devices

## UI Component Polish Template

```tsx
import { useState } from 'react';
import { html } from '@react-three/drei';
import { motion, AnimatePresence } from 'framer-motion';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  loading?: boolean;
}

export function PolishedButton({
  label,
  onClick,
  variant = 'primary',
  disabled = false,
  loading = false,
}: ButtonProps) {
  const [isHovered, setIsHovered] = useState(false);

  const baseStyles = {
    padding: '12px 24px',
    borderRadius: '8px',
    fontWeight: 600,
    fontSize: '16px',
    border: 'none',
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'all 0.2s ease',
    opacity: disabled ? 0.5 : 1,
  };

  const variantStyles = {
    primary: {
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      boxShadow: isHovered ? '0 8px 20px rgba(102, 126, 234, 0.4)' : '0 4px 10px rgba(102, 126, 234, 0.3)',
      transform: isHovered ? 'translateY(-2px)' : 'translateY(0)',
    },
    secondary: {
      background: 'white',
      color: '#667eea',
      border: '2px solid #667eea',
      boxShadow: isHovered ? '0 4px 15px rgba(102, 126, 234, 0.2)' : 'none',
    },
    danger: {
      background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      color: 'white',
      boxShadow: isHovered ? '0 8px 20px rgba(245, 87, 108, 0.4)' : '0 4px 10px rgba(245, 87, 108, 0.3)',
    },
  };

  return (
    <motion.button
      style={{ ...baseStyles, ...variantStyles[variant] }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={!disabled && !loading ? onClick : undefined}
      whileTap={{ scale: disabled || loading ? 1 : 0.95 }}
      disabled={disabled || loading}
    >
      <AnimatePresence mode="wait">
        {loading ? (
          <motion.span
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <LoadingSpinner />
          </motion.span>
        ) : (
          <motion.span
            key="label"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {label}
          </motion.span>
        )}
      </AnimatePresence>
    </motion.button>
  );
}
```

## Visual Feedback Patterns

### Hover Feedback

```tsx
<mesh
  onPointerOver={(e) => {
    e.object.scale.setScalar(1.1);
    document.body.style.cursor = 'pointer';
  }}
  onPointerOut={(e) => {
    e.object.scale.setScalar(1.0);
    document.body.style.cursor = 'default';
  }}
>
  <boxGeometry />
  <meshStandardMaterial color="orange" />
</mesh>
```

### Click Feedback

```tsx
function InteractiveMesh() {
  const meshRef = useRef<THREE.Mesh>(null);

  const handleClick = () => {
    // Scale animation
    if (meshRef.current) {
      gsap.to(meshRef.current.scale, {
        x: 1.2,
        y: 1.2,
        z: 1.2,
        duration: 0.1,
        yoyo: true,
        repeat: 1,
      });
    }
  };

  return (
    <mesh ref={meshRef} onClick={handleClick}>
      <sphereGeometry />
      <meshStandardMaterial color="blue" />
    </mesh>
  );
}
```

### Progress Feedback

```tsx
function ProgressBar({ progress }: { progress: number }) {
  return (
    <div className="progress-container">
      <div
        className="progress-bar"
        style={{
          width: `${Math.min(100, Math.max(0, progress * 100))}%`,
          transition: 'width 0.3s ease',
        }}
      />
    </div>
  );
}
```

## Color Guidelines

### Accessible Color Combinations

| Background | Text       | Ratio  | WCAG Level |
| ---------- | ---------- | ------ | ---------- |
| #FFFFFF    | #000000    | 21:1   | AAA        |
| #F5F5F5    | #333333    | 12.6:1 | AAA        |
| #667EEA    | #FFFFFF    | 4.5:1  | AA         |
| #F5576C    | #FFFFFF    | 4.2:1  | AA         |

### Common Mistakes

- ❌ Red/green as only differentiators (colorblindness)
- ❌ Light text on light background
- ❌ Pure colors (#FF0000, #00FF00) - too harsh
- ❌ Too many colors in one view

## Typography Guidelines

```css
/* Font scale - modular scale */
.text-xs { font-size: 0.75rem; }    /* 12px */
.text-sm { font-size: 0.875rem; }   /* 14px */
.text-base { font-size: 1rem; }     /* 16px */
.text-lg { font-size: 1.125rem; }   /* 18px */
.text-xl { font-size: 1.25rem; }    /* 20px */
.text-2xl { font-size: 1.5rem; }    /* 24px */
.text-3xl { font-size: 1.875rem; }  /* 30px */
.text-4xl { font-size: 2.25rem; }   /* 36px */

/* Weights */
.font-light { font-weight: 300; }
.font-normal { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
```

## Spacing System

```css
/* 8px base unit */
.space-1 { padding: 0.25rem; }  /* 4px */
.space-2 { padding: 0.5rem; }   /* 8px */
.space-3 { padding: 0.75rem; }  /* 12px */
.space-4 { padding: 1rem; }     /* 16px */
.space-5 { padding: 1.25rem; }  /* 20px */
.space-6 { padding: 1.5rem; }   /* 24px */
.space-8 { padding: 2rem; }     /* 32px */
.space-10 { padding: 2.5rem; }  /* 40px */
.space-12 { padding: 3rem; }    /* 48px */
```

## Anti-Patterns

❌ **DON'T:**

- Use placeholder colors (magenta, lime green)
- Skip hover states on interactive elements
- Use too many fonts (>2 typefaces)
- Inconsistent spacing
- No feedback for user actions
- Text on busy backgrounds without contrast

✅ **DO:**

- Use colors from GDD palette
- Provide visual feedback for all interactions
- Limit fonts to 1-2 typefaces
- Follow spacing system consistently
- Test for color blindness
- Ensure text readability

## Checklist

Before considering visual polish complete:

- [ ] All interactive elements have hover/click states
- [ ] Loading states exist for async operations
- [ ] Error messages are clear and actionable
- [ ] Success feedback is provided
- [ ] Colors meet accessibility standards
- [ ] Typography is consistent and readable
- [ ] Spacing follows system
- [ ] Transitions are smooth (200-300ms)
- [ ] Performance tested on target devices
- [ ] Visual style matches GDD

## Related Skills

For post-processing polish: `Skill("ta-vfx-postfx")`

## External References

- [WCAG Color Contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [Type Scale Calculator](https://type-scale.com/)
- [Easing functions - Motion.dev](https://motion.dev/docs/easing-functions) - Official Framer Motion easing documentation
- [The Easing Blueprint - Reuben Rapose](https://www.reubence.com/articles/the-easing-blueprint) - Comprehensive easing guide for Framer Motion
- [Creating Metallic Effect with CSS](https://ibelick.com/blog/creating-metallic-effect-with-css) - CSS gradients for metallic buttons

---

## Professional Game UI Design System (Added: ui-001 Playtest Findings)

**Learned from ui-001 playtest:** Current UI lacked professional polish. This section documents patterns for shipping-quality game UI.

### 16:9 Aspect Ratio Enforcement

**Pattern:** All UI screens must maintain 16:9 aspect ratio, centered on screen with letterbox bars for other ratios.

```tsx
// src/components/ui/AspectContainer.tsx
const ASPECT_RATIO = 16 / 9;

export function AspectContainer({ children }: { children: React.ReactNode }) {
  return (
    <div className="fixed inset-0 z-10 flex items-center justify-center bg-black">
      <div
        className="relative overflow-hidden"
        style={{
          aspectRatio: ASPECT_RATIO,
          maxWidth: '100vw',
          maxHeight: '100vh',
          width: 'min(100vw, 100vh * 16/9)',
          height: 'min(100vh, 100vw * 9/16)',
        }}
      >
        {children}
      </div>
    </div>
  );
}
```

**Letterbox CSS:**
```css
/* Letterbox bars for non-16:9 displays */
.ui-letterbox-top,
.ui-letterbox-bottom {
  position: fixed;
  left: 0; right: 0;
  height: calc((100vh - (100vw * 9 / 16)) / 2);
  background: #000;
  z-index: 50;
}
.ui-letterbox-top { top: 0; }
.ui-letterbox-bottom { bottom: 0; }

@media (min-aspect-ratio: 16/9) {
  .ui-letterbox-top, .ui-letterbox-bottom { display: none; }
}
```

### Adaptive Scaling Tokens

```typescript
// src/components/ui/tokens.ts
export const UIScale = {
  base: { width: 1920, height: 1080 },

  getScaleFactor(windowWidth: number, windowHeight: number): number {
    const baseWidth = 1920;
    const scale = Math.min(
      windowWidth / baseWidth,
      windowHeight / (baseWidth * 9 / 16)
    );
    return Math.max(0.5, Math.min(2, scale));
  },

  fontSize: {
    xs: '14px',   // 0.875rem
    sm: '16px',   // 1rem
    base: '18px', // 1.125rem
    lg: '24px',   // 1.5rem
    xl: '32px',   // 2rem
    '2xl': '48px', // 3rem
    '3xl': '64px', // 4rem
    display: '128px', // 8rem
  },
};
```

### Metallic Button Design System

**Inspired by:** Quake III Arena, modern Call of Duty, Overwatch

```tsx
// Metallic gradient backgrounds
const metallicBackgrounds = {
  primary: `linear-gradient(180deg,
    rgba(249, 115, 22, 0.1) 0%,
    rgba(0, 0, 0, 0.9) 20%,
    rgba(0, 0, 0, 1) 50%,
    rgba(0, 0, 0, 0.9) 80%,
    rgba(249, 115, 22, 0.1) 100%
  )`,

  secondary: `linear-gradient(180deg,
    rgba(38, 38, 38, 0.9) 0%,
    rgba(10, 10, 10, 1) 50%,
    rgba(38, 38, 38, 0.9) 100%
  )`,
};

// Hover glow effects
const metallicGlow = {
  hover: `box-shadow:
    0 0 20px rgba(251, 115, 22, 0.4),
    inset 0 0 20px rgba(251, 115, 22, 0.1)`,

  active: `box-shadow:
    0 0 40px rgba(251, 115, 22, 0.6),
    inset 0 0 30px rgba(251, 115, 22, 0.2)`,
};
```

### Custom Easing Curves for Game UI

**Sources:** [Motion.dev Easing](https://motion.dev/docs/easing-functions), [The Easing Blueprint](https://www.reubence.com/articles/the-easing-blueprint)

```typescript
// Easing curve library for game UI
export const GameEasing = {
  // Snappy entrance (menu reveal)
  snap: [0.22, 1, 0.36, 1] as const,

  // Smooth reveal (screen transitions)
  reveal: [0.16, 1, 0.3, 1] as const,

  // Elastic bounce (button release)
  bounce: [0.34, 1.56, 0.64, 1] as const,

  // Weighty press (button click)
  press: [0.4, 0, 0.2, 1] as const,
};

// Animation timing specifications
const buttonAnimations = {
  idleEnter: { duration: 400, ease: GameEasing.snap },
  hover: { duration: 150, ease: GameEasing.press },
  active: { duration: 50, ease: GameEasing.press },
  release: { duration: 300, ease: GameEasing.bounce },
};
```

### Gaming Typography

```css
/* Import Google Fonts for game UI */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@500;600;700&display=swap');

:root {
  --font-display: 'Orbitron', 'Impact', sans-serif;
  --font-ui: 'Rajdhani', 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Courier New', monospace;
}
```

| Usage          | Font      | Size  | Weight | Letter Spacing | Transform |
| -------------- | --------- | ----- | ------ | -------------- | --------- |
| Game Logo      | Orbitron  | 128px | 900    | 0.05em         | Uppercase  |
| Screen Title   | Orbitron  | 64px  | 700    | 0.1em          | Uppercase  |
| Button Text    | Rajdhani  | 24px  | 600    | 0.15em         | Uppercase  |
| Body Text      | Rajdhani  | 18px  | 500    | 0.02em         | None       |
| Data/Stats     | JetBrains Mono | 16px | 500  | 0              | None       |

### Industrial Color Palette

```css
:root {
  /* Primary - Electric Orange (Quake-inspired) */
  --color-primary-500: #f97316;
  --color-primary-600: #ea580c;

  /* Secondary - Cyan/Blue */
  --color-secondary-500: #06b6d4;

  /* Metallic Grays */
  --color-metal-900: #0a0a0a;
  --color-metal-700: #262626;
  --color-metal-500: #525252;

  /* Surface Colors */
  --color-surface-bg: rgba(10, 10, 10, 0.95);
  --color-surface-border: rgba(251, 115, 22, 0.3);

  /* Glow Effects */
  --color-glow-primary: rgba(249, 115, 22, 0.6);
}
```

### UI Design System Checklist

Before considering UI polished:

- [ ] **16:9 Enforcement** - All screens maintain aspect ratio
- [ ] **Adaptive Scaling** - UI scales to any window size
- [ ] **Design Tokens** - Colors, typography, spacing systematized
- [ ] **Metallic Buttons** - Industrial styling with gradients
- [ ] **Custom Easing** - Game-appropriate animation curves
- [ ] **Gaming Fonts** - Orbitron/Rajdhani or similar
- [ ] **Hover Glow** - Visual feedback on interaction
- [ ] **Sound Feedback** - Optional but recommended
- [ ] **60+ FPS** - Animations maintain performance
- [ ] **E2E Tests** - Visual regression tests pass
