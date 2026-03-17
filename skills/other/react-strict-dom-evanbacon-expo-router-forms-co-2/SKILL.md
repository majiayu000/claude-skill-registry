---
name: react-strict-dom
description: Set up react-strict-dom with Babel, PostCSS, and CSS-wrapped HTML components for universal Expo apps
---

# React Strict DOM Setup for Expo

This guide covers setting up react-strict-dom in an Expo project with Tailwind CSS v4 and react-native-css for universal app development.

## Overview

react-strict-dom provides a subset of HTML/CSS that works identically across web and native platforms. This setup includes:

- **Babel preset** - Transforms react-strict-dom components for each platform
- **PostCSS plugin** - Processes styles for web builds
- **CSS directive** - Enables react-strict-dom styles in global CSS
- **HTML wrapper components** - CSS-wrapped primitives with Tailwind className support

## Installation

Install react-strict-dom using bun:

```bash
bun install react-strict-dom@0.0.54
```

> Note: Version 0.0.55 has a broken dependency (`postcss-react-strict-dom@0.0.55` doesn't exist). Use 0.0.54 until this is resolved.

## Babel Configuration

Create or update `babel.config.js` in the project root:

```javascript
const reactStrictPreset = require("react-strict-dom/babel-preset");

function getPlatform(caller) {
  return caller && caller.platform;
}

function getIsDev(caller) {
  if (caller?.isDev != null) return caller.isDev;
  // https://babeljs.io/docs/options#envname
  return (
    process.env.BABEL_ENV === "development" ||
    process.env.NODE_ENV === "development"
  );
}

module.exports = function (api) {
  //api.cache(true);
  const platform = api.caller(getPlatform);
  const dev = api.caller(getIsDev);

  return {
    presets: [
      "babel-preset-expo",
      [reactStrictPreset, { debug: true, dev, platform }],
    ],
  };
};
```

### Configuration Options

- `debug: true` - Enables debug output during development
- `dev` - Automatically detected from environment
- `platform` - Passed by Metro/bundler for platform-specific transforms

## PostCSS Configuration

Update `postcss.config.mjs` to include the react-strict-dom plugin:

```javascript
export default {
  plugins: {
    "@tailwindcss/postcss": {},
    "react-strict-dom/postcss-plugin": {
      include: ["src/**/*.{js,jsx,mjs,ts,tsx}"],
    },
  },
};
```

The `include` option specifies which files to process for react-strict-dom styles.

## Global CSS Directive

Add the `@react-strict-dom` directive at the top of your global CSS file (e.g., `src/global.css`):

```css
@react-strict-dom;

@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/preflight.css" layer(base);
@import "tailwindcss/utilities.css";

/* ... rest of your styles */
```

This directive must be the first rule in the file for react-strict-dom styles to work correctly.

## HTML Components with Tailwind Support

Create CSS-wrapped HTML components that support Tailwind className at `src/html/index.tsx`:

```typescript
import { useCssElement } from "react-native-css";

import React from "react";

import { html as rsd } from "react-strict-dom";
import { StyleSheet } from "react-native";

function createCssComponent<T extends keyof typeof rsd>(
  elementName: T,
  displayName?: string
) {
  type Props = React.ComponentProps<(typeof rsd)[T]> & {
    className?: string;
  };

  let Component: (props: Props) => React.ReactElement;
  if (process.env.EXPO_OS === "web") {
    Component = (props: Props) => {
      // eslint-disable-next-line import/namespace
      return useCssElement(rsd[elementName], props, {
        // @ts-expect-error
        className: "style",
      });
    };
  } else {
    Component = ({ style, ...props }: Props) => {
      const normal = props as any;
      if (style) {
        normal.style = normalizeStyle(style);
      }
      return useCssElement(
        // eslint-disable-next-line import/namespace
        rsd[elementName],
        normal,
        {
          // @ts-expect-error
          className: "style",
        }
      );
    };
  }

  (Component as any).displayName = displayName || `CSS(${elementName})`;

  return Component;
}

function normalizeStyle(style: any) {
  if (!style) return style;
  const flat = StyleSheet.flatten(style);
  if (flat.backgroundImage) {
    flat.experimental_backgroundImage = flat.backgroundImage;
    delete flat.backgroundImage;
  }
  return flat;
}

export const html = {
  button: createCssComponent("button"),
  div: createCssComponent("div"),
  h1: createCssComponent("h1"),
  h2: createCssComponent("h2"),
  h3: createCssComponent("h3"),
  h4: createCssComponent("h4"),
  h5: createCssComponent("h5"),
  h6: createCssComponent("h6"),
  p: createCssComponent("p"),
  span: createCssComponent("span"),
  img: createCssComponent("img"),
  input: createCssComponent("input"),
  textarea: createCssComponent("textarea"),
  a: createCssComponent("a"),
  ul: createCssComponent("ul"),
  ol: createCssComponent("ol"),
  li: createCssComponent("li"),
  nav: createCssComponent("nav"),
  header: createCssComponent("header"),
  footer: createCssComponent("footer"),
  main: createCssComponent("main"),
  section: createCssComponent("section"),
  article: createCssComponent("article"),
  aside: createCssComponent("aside"),
  label: createCssComponent("label"),
  form: createCssComponent("form"),
  i: createCssComponent("i"),
  b: createCssComponent("b"),
  strong: createCssComponent("strong"),
  em: createCssComponent("em"),
  code: createCssComponent("code"),
  pre: createCssComponent("pre"),
  blockquote: createCssComponent("blockquote"),
  hr: createCssComponent("hr"),
};
```

### Usage

Import and use the HTML components with Tailwind classes:

```tsx
import { html } from "@/html";

export function MyComponent() {
  return (
    <html.div className="flex flex-col gap-4 p-4 bg-sf-bg">
      <html.h1 className="text-2xl font-bold text-sf-text">
        Hello World
      </html.h1>
      <html.p className="text-sf-text-2">
        This works on both web and native!
      </html.p>
      <html.button className="px-4 py-2 bg-sf-blue text-white rounded-lg">
        Click me
      </html.button>
    </html.div>
  );
}
```

## How It Works

### Web

On web, react-strict-dom renders actual HTML elements (`<div>`, `<button>`, etc.) with the PostCSS plugin processing styles. The `useCssElement` wrapper enables Tailwind className support.

### Native (iOS/Android)

On native, react-strict-dom transforms HTML elements into equivalent React Native components:
- `<div>` → `<View>`
- `<span>`, `<p>` → `<Text>`
- `<img>` → `<Image>`
- etc.

The Babel preset handles these transformations at build time.

## Style Normalization

The `normalizeStyle` function handles platform-specific style differences:

- Flattens style arrays using `StyleSheet.flatten()`
- Converts `backgroundImage` to `experimental_backgroundImage` for native compatibility

## Benefits

1. **Semantic HTML**: Write semantic HTML that works everywhere
2. **Better SEO**: Real HTML elements on web
3. **Accessibility**: Native HTML semantics for screen readers
4. **Tailwind Integration**: Full className support with react-native-css
5. **Type Safety**: Full TypeScript support with proper component props
6. **Platform Optimizations**: Platform-specific transforms at build time

## Troubleshooting

### "postcss-react-strict-dom version not found"

Use react-strict-dom@0.0.54 instead of the latest version. Version 0.0.55 has a missing dependency.

### Styles not applying on native

Ensure the `@react-strict-dom` directive is at the top of your global CSS file.

### TypeScript errors with displayName

Use type assertions when setting displayName:
```typescript
(Component as any).displayName = displayName;
```

### backgroundImage not working on native

The `normalizeStyle` function handles this automatically by mapping to `experimental_backgroundImage`.
