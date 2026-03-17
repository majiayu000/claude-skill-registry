---
description: "Generate CSS, Tailwind, and styled-components code from design style selections"
triggers:
  - css
  - tailwind
  - styled-components
  - design tokens
  - color palette
  - typography
  - spacing
globs:
  - "*.css"
  - "*.scss"
  - "*.ts"
  - "tailwind.config.*"
  - "theme.ts"
---

# CSS Generation Skill

Generate CSS, Tailwind, and styled-components code from design style selections.

## Overview

This skill provides tools and templates for converting design tokens and style selections into production-ready CSS, Tailwind configurations, and styled-components theme objects.

## CSS Variables Generation from Design Tokens

### Design Token Structure

```typescript
interface DesignTokens {
  colors: ColorTokens;
  spacing: SpacingTokens;
  typography: TypographyTokens;
  shadows: ShadowTokens;
  borders: BorderTokens;
  effects: EffectTokens;
}

interface ColorTokens {
  primary: ColorScale;
  secondary: ColorScale;
  neutral: ColorScale;
  success: ColorScale;
  warning: ColorScale;
  error: ColorScale;
  info: ColorScale;
}

interface ColorScale {
  50: string;
  100: string;
  200: string;
  300: string;
  400: string;
  500: string;  // Base color
  600: string;
  700: string;
  800: string;
  900: string;
}
```

### CSS Variables Template

**styles/tokens.css:**
```css
:root {
  /* Color Tokens - Primary */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-200: #bfdbfe;
  --color-primary-300: #93c5fd;
  --color-primary-400: #60a5fa;
  --color-primary-500: #3b82f6;  /* Base */
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;
  --color-primary-800: #1e40af;
  --color-primary-900: #1e3a8a;

  /* Semantic Color Mappings */
  --color-text-primary: var(--color-neutral-900);
  --color-text-secondary: var(--color-neutral-600);
  --color-text-disabled: var(--color-neutral-400);
  --color-bg-primary: #ffffff;
  --color-bg-secondary: var(--color-neutral-50);
  --color-border: var(--color-neutral-200);
  --color-focus: var(--color-primary-500);

  /* Spacing Tokens */
  --spacing-0: 0;
  --spacing-px: 1px;
  --spacing-0-5: 0.125rem;  /* 2px */
  --spacing-1: 0.25rem;     /* 4px */
  --spacing-1-5: 0.375rem;  /* 6px */
  --spacing-2: 0.5rem;      /* 8px */
  --spacing-2-5: 0.625rem;  /* 10px */
  --spacing-3: 0.75rem;     /* 12px */
  --spacing-3-5: 0.875rem;  /* 14px */
  --spacing-4: 1rem;        /* 16px */
  --spacing-5: 1.25rem;     /* 20px */
  --spacing-6: 1.5rem;      /* 24px */
  --spacing-7: 1.75rem;     /* 28px */
  --spacing-8: 2rem;        /* 32px */
  --spacing-9: 2.25rem;     /* 36px */
  --spacing-10: 2.5rem;     /* 40px */
  --spacing-12: 3rem;       /* 48px */
  --spacing-16: 4rem;       /* 64px */
  --spacing-20: 5rem;       /* 80px */
  --spacing-24: 6rem;       /* 96px */
  --spacing-32: 8rem;       /* 128px */

  /* Typography Tokens */
  --font-family-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-family-serif: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-family-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;

  --font-size-xs: 0.75rem;      /* 12px */
  --font-size-sm: 0.875rem;     /* 14px */
  --font-size-base: 1rem;       /* 16px */
  --font-size-lg: 1.125rem;     /* 18px */
  --font-size-xl: 1.25rem;      /* 20px */
  --font-size-2xl: 1.5rem;      /* 24px */
  --font-size-3xl: 1.875rem;    /* 30px */
  --font-size-4xl: 2.25rem;     /* 36px */
  --font-size-5xl: 3rem;        /* 48px */
  --font-size-6xl: 3.75rem;     /* 60px */

  --font-weight-thin: 100;
  --font-weight-extralight: 200;
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
  --font-weight-black: 900;

  --line-height-none: 1;
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;

  /* Shadow Tokens */
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);

  /* Border Radius Tokens */
  --radius-none: 0;
  --radius-sm: 0.125rem;   /* 2px */
  --radius-md: 0.375rem;   /* 6px */
  --radius-lg: 0.5rem;     /* 8px */
  --radius-xl: 0.75rem;    /* 12px */
  --radius-2xl: 1rem;      /* 16px */
  --radius-3xl: 1.5rem;    /* 24px */
  --radius-full: 9999px;

  /* Transition Tokens */
  --transition-fast: 150ms;
  --transition-base: 250ms;
  --transition-slow: 350ms;
  --transition-slower: 500ms;

  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dark Mode Tokens */
[data-theme="dark"] {
  --color-text-primary: var(--color-neutral-50);
  --color-text-secondary: var(--color-neutral-400);
  --color-text-disabled: var(--color-neutral-600);
  --color-bg-primary: var(--color-neutral-900);
  --color-bg-secondary: var(--color-neutral-800);
  --color-border: var(--color-neutral-700);
}
```

## Tailwind Configuration Templates

### Full Tailwind Config

**tailwind.config.ts:**
```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        success: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        },
        warning: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        error: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
        },
      },
      spacing: {
        '0.5': '0.125rem',
        '1.5': '0.375rem',
        '2.5': '0.625rem',
        '3.5': '0.875rem',
        '18': '4.5rem',
        '88': '22rem',
        '100': '25rem',
        '112': '28rem',
        '128': '32rem',
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['var(--font-merriweather)', 'ui-serif', 'Georgia', 'serif'],
        mono: ['var(--font-jetbrains-mono)', 'ui-monospace', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.75rem' }],
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
        '6xl': ['3.75rem', { lineHeight: '1' }],
        '7xl': ['4.5rem', { lineHeight: '1' }],
        '8xl': ['6rem', { lineHeight: '1' }],
        '9xl': ['8rem', { lineHeight: '1' }],
      },
      boxShadow: {
        'xs': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'sm': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
        'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
        // Style-specific shadows
        'neumorphic': '8px 8px 16px #d1d9e6, -8px -8px 16px #ffffff',
        'neumorphic-inset': 'inset 8px 8px 16px #d1d9e6, inset -8px -8px 16px #ffffff',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'brutalist': '8px 8px 0px 0px rgba(0, 0, 0, 1)',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      transitionDuration: {
        '0': '0ms',
        '2000': '2000ms',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
  ],
};

export default config;
```

## styled-components Theme Objects

### Theme Type Definition

**styles/theme.ts:**
```typescript
export interface Theme {
  colors: {
    primary: ColorScale;
    secondary: ColorScale;
    neutral: ColorScale;
    success: ColorScale;
    warning: ColorScale;
    error: ColorScale;
    info: ColorScale;
    text: {
      primary: string;
      secondary: string;
      disabled: string;
      inverse: string;
    };
    background: {
      primary: string;
      secondary: string;
      tertiary: string;
      inverse: string;
    };
    border: {
      default: string;
      hover: string;
      focus: string;
    };
  };
  spacing: {
    [key: string]: string;
  };
  typography: {
    fontFamily: {
      sans: string;
      serif: string;
      mono: string;
    };
    fontSize: {
      [key: string]: string;
    };
    fontWeight: {
      [key: string]: number;
    };
    lineHeight: {
      [key: string]: number;
    };
  };
  shadows: {
    [key: string]: string;
  };
  borderRadius: {
    [key: string]: string;
  };
  transitions: {
    duration: {
      [key: string]: string;
    };
    easing: {
      [key: string]: string;
    };
  };
}

interface ColorScale {
  50: string;
  100: string;
  200: string;
  300: string;
  400: string;
  500: string;
  600: string;
  700: string;
  800: string;
  900: string;
}
```

### Light Theme

**styles/themes/light.ts:**
```typescript
import { Theme } from '../theme';

export const lightTheme: Theme = {
  colors: {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93c5fd',
      400: '#60a5fa',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      800: '#1e40af',
      900: '#1e3a8a',
    },
    secondary: {
      50: '#f8fafc',
      100: '#f1f5f9',
      200: '#e2e8f0',
      300: '#cbd5e1',
      400: '#94a3b8',
      500: '#64748b',
      600: '#475569',
      700: '#334155',
      800: '#1e293b',
      900: '#0f172a',
    },
    neutral: {
      50: '#fafafa',
      100: '#f5f5f5',
      200: '#e5e5e5',
      300: '#d4d4d4',
      400: '#a3a3a3',
      500: '#737373',
      600: '#525252',
      700: '#404040',
      800: '#262626',
      900: '#171717',
    },
    success: {
      50: '#f0fdf4',
      100: '#dcfce7',
      200: '#bbf7d0',
      300: '#86efac',
      400: '#4ade80',
      500: '#22c55e',
      600: '#16a34a',
      700: '#15803d',
      800: '#166534',
      900: '#14532d',
    },
    warning: {
      50: '#fffbeb',
      100: '#fef3c7',
      200: '#fde68a',
      300: '#fcd34d',
      400: '#fbbf24',
      500: '#f59e0b',
      600: '#d97706',
      700: '#b45309',
      800: '#92400e',
      900: '#78350f',
    },
    error: {
      50: '#fef2f2',
      100: '#fee2e2',
      200: '#fecaca',
      300: '#fca5a5',
      400: '#f87171',
      500: '#ef4444',
      600: '#dc2626',
      700: '#b91c1c',
      800: '#991b1b',
      900: '#7f1d1d',
    },
    info: {
      50: '#eff6ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93c5fd',
      400: '#60a5fa',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      800: '#1e40af',
      900: '#1e3a8a',
    },
    text: {
      primary: '#171717',
      secondary: '#525252',
      disabled: '#a3a3a3',
      inverse: '#fafafa',
    },
    background: {
      primary: '#ffffff',
      secondary: '#f5f5f5',
      tertiary: '#e5e5e5',
      inverse: '#171717',
    },
    border: {
      default: '#e5e5e5',
      hover: '#d4d4d4',
      focus: '#3b82f6',
    },
  },
  spacing: {
    0: '0',
    px: '1px',
    0.5: '0.125rem',
    1: '0.25rem',
    1.5: '0.375rem',
    2: '0.5rem',
    2.5: '0.625rem',
    3: '0.75rem',
    3.5: '0.875rem',
    4: '1rem',
    5: '1.25rem',
    6: '1.5rem',
    7: '1.75rem',
    8: '2rem',
    9: '2.25rem',
    10: '2.5rem',
    12: '3rem',
    16: '4rem',
    20: '5rem',
    24: '6rem',
    32: '8rem',
  },
  typography: {
    fontFamily: {
      sans: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      serif: 'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif',
      mono: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '3.75rem',
    },
    fontWeight: {
      thin: 100,
      extralight: 200,
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
      black: 900,
    },
    lineHeight: {
      none: 1,
      tight: 1.25,
      snug: 1.375,
      normal: 1.5,
      relaxed: 1.625,
      loose: 2,
    },
  },
  shadows: {
    xs: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    sm: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
  },
  borderRadius: {
    none: '0',
    sm: '0.125rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    '2xl': '1rem',
    '3xl': '1.5rem',
    full: '9999px',
  },
  transitions: {
    duration: {
      fast: '150ms',
      base: '250ms',
      slow: '350ms',
      slower: '500ms',
    },
    easing: {
      linear: 'linear',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    },
  },
};
```

### Dark Theme

**styles/themes/dark.ts:**
```typescript
import { Theme } from '../theme';
import { lightTheme } from './light';

export const darkTheme: Theme = {
  ...lightTheme,
  colors: {
    ...lightTheme.colors,
    text: {
      primary: '#fafafa',
      secondary: '#a3a3a3',
      disabled: '#525252',
      inverse: '#171717',
    },
    background: {
      primary: '#0a0a0a',
      secondary: '#171717',
      tertiary: '#262626',
      inverse: '#ffffff',
    },
    border: {
      default: '#404040',
      hover: '#525252',
      focus: '#3b82f6',
    },
  },
};
```

### Usage with styled-components

**components/Button.tsx:**
```typescript
import styled from 'styled-components';

export const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: ${({ theme }) => `${theme.spacing[2]} ${theme.spacing[4]}`};
  font-family: ${({ theme }) => theme.typography.fontFamily.sans};
  font-size: ${({ theme }) => theme.typography.fontSize.base};
  font-weight: ${({ theme }) => theme.typography.fontWeight.medium};
  border-radius: ${({ theme }) => theme.borderRadius.md};
  border: none;
  cursor: pointer;
  transition: all ${({ theme }) => theme.transitions.duration.base}
    ${({ theme }) => theme.transitions.easing.inOut};

  background-color: ${({ theme, variant = 'primary' }) =>
    variant === 'primary'
      ? theme.colors.primary[500]
      : theme.colors.secondary[500]};

  color: ${({ theme }) => theme.colors.text.inverse};

  box-shadow: ${({ theme }) => theme.shadows.sm};

  &:hover {
    background-color: ${({ theme, variant = 'primary' }) =>
      variant === 'primary'
        ? theme.colors.primary[600]
        : theme.colors.secondary[600]};
    box-shadow: ${({ theme }) => theme.shadows.md};
  }

  &:active {
    transform: translateY(1px);
  }

  &:focus-visible {
    outline: 2px solid ${({ theme }) => theme.colors.border.focus};
    outline-offset: 2px;
  }

  &:disabled {
    background-color: ${({ theme }) => theme.colors.neutral[300]};
    color: ${({ theme }) => theme.colors.text.disabled};
    cursor: not-allowed;
    box-shadow: none;
  }
`;
```

## Format Conversion

### CSS to Tailwind

```typescript
// Convert CSS variables to Tailwind classes
function cssToTailwind(cssProperties: Record<string, string>): string {
  const mapping: Record<string, (value: string) => string> = {
    'background-color': (val) => {
      if (val.startsWith('var(--color-')) {
        const color = val.match(/--color-(\w+)-(\d+)/);
        if (color) return `bg-${color[1]}-${color[2]}`;
      }
      return '';
    },
    'color': (val) => {
      if (val.startsWith('var(--color-')) {
        const color = val.match(/--color-(\w+)-(\d+)/);
        if (color) return `text-${color[1]}-${color[2]}`;
      }
      return '';
    },
    'padding': (val) => {
      if (val.startsWith('var(--spacing-')) {
        const spacing = val.match(/--spacing-(\w+)/);
        if (spacing) return `p-${spacing[1]}`;
      }
      return '';
    },
    // Add more mappings...
  };

  return Object.entries(cssProperties)
    .map(([prop, value]) => mapping[prop]?.(value) || '')
    .filter(Boolean)
    .join(' ');
}
```

### Tailwind to styled-components

```typescript
// Convert Tailwind config to styled-components theme
function tailwindToStyledTheme(tailwindConfig: any): Theme {
  return {
    colors: tailwindConfig.theme.extend.colors,
    spacing: tailwindConfig.theme.extend.spacing,
    typography: {
      fontFamily: tailwindConfig.theme.extend.fontFamily,
      fontSize: tailwindConfig.theme.extend.fontSize,
      fontWeight: {
        thin: 100,
        // ... map all weights
      },
      lineHeight: {
        none: 1,
        // ... map all line heights
      },
    },
    shadows: tailwindConfig.theme.extend.boxShadow,
    borderRadius: tailwindConfig.theme.extend.borderRadius,
    transitions: {
      duration: {
        fast: '150ms',
        // ... map durations
      },
      easing: {
        linear: 'linear',
        // ... map easings
      },
    },
  };
}
```

## Dark Mode Variant Generation

### Automatic Dark Mode Classes

```typescript
// Generate dark mode variants for CSS
function generateDarkModeVariants(baseColors: ColorTokens): string {
  return `
    :root {
      ${Object.entries(baseColors).map(([name, scale]) =>
        Object.entries(scale).map(([weight, color]) =>
          `--color-${name}-${weight}: ${color};`
        ).join('\n')
      ).join('\n')}
    }

    [data-theme="dark"] {
      /* Invert color scales for dark mode */
      ${Object.entries(baseColors).map(([name, scale]) =>
        Object.entries(scale).map(([weight, _]) => {
          const invertedWeight = 1000 - parseInt(weight);
          return `--color-${name}-${weight}: var(--color-${name}-${invertedWeight});`;
        }).join('\n')
      ).join('\n')}
    }
  `;
}
```

## Style-Specific Generators

### Glassmorphism Generator

```typescript
export function generateGlassmorphismCSS(options: {
  blur?: number;
  opacity?: number;
  color?: string;
  borderOpacity?: number;
}) {
  const {
    blur = 10,
    opacity = 0.1,
    color = '#ffffff',
    borderOpacity = 0.2,
  } = options;

  return `
    background: rgba(${hexToRgb(color)}, ${opacity});
    backdrop-filter: blur(${blur}px);
    -webkit-backdrop-filter: blur(${blur}px);
    border: 1px solid rgba(${hexToRgb(color)}, ${borderOpacity});
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  `;
}
```

### Neumorphism Generator

```typescript
export function generateNeumorphismCSS(options: {
  lightColor?: string;
  darkColor?: string;
  distance?: number;
  intensity?: number;
  blur?: number;
}) {
  const {
    lightColor = '#ffffff',
    darkColor = '#d1d9e6',
    distance = 8,
    intensity = 1,
    blur = 16,
  } = options;

  return `
    background: #e0e5ec;
    box-shadow:
      ${distance}px ${distance}px ${blur}px ${darkColor},
      -${distance}px -${distance}px ${blur}px ${lightColor};
  `;
}
```

### Neo-Brutalism Generator

```typescript
export function generateNeoBrutalismCSS(options: {
  bgColor?: string;
  borderColor?: string;
  borderWidth?: number;
  shadowOffset?: number;
}) {
  const {
    bgColor = '#ffff00',
    borderColor = '#000000',
    borderWidth = 4,
    shadowOffset = 8,
  } = options;

  return `
    background-color: ${bgColor};
    border: ${borderWidth}px solid ${borderColor};
    box-shadow: ${shadowOffset}px ${shadowOffset}px 0px ${borderColor};
  `;
}
```

## Utility Functions

```typescript
function hexToRgb(hex: string): string {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}`
    : '0, 0, 0';
}

function rgbToHex(r: number, g: number, b: number): string {
  return '#' + [r, g, b].map(x => {
    const hex = x.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  }).join('');
}

function lighten(color: string, amount: number): string {
  // Implementation
  return color;
}

function darken(color: string, amount: number): string {
  // Implementation
  return color;
}
```

## Integration with Other Skills

- **design-styles**: Convert style selections to CSS/Tailwind
- **component-patterns**: Apply generated styles to components
- **keycloak-theming**: Generate theme CSS for Keycloak

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [styled-components Documentation](https://styled-components.com/docs)
- [CSS Custom Properties Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- Design Token Tools: Style Dictionary, Theo
- Color Tools: Coolors, Adobe Color, Paletton
