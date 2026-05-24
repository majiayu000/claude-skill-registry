---
name: esbuild
description: Configures esbuild for extremely fast JavaScript/TypeScript bundling with plugins, code splitting, and build optimization. Use when building libraries, rapid prototyping, or optimizing build performance.
---

# esbuild

Extremely fast JavaScript/TypeScript bundler written in Go, 10-100x faster than traditional bundlers.

## Quick Start

```bash
npm install --save-dev esbuild

# Bundle for browser
npx esbuild src/index.ts --bundle --outfile=dist/bundle.js

# Production build
npx esbuild src/index.ts --bundle --minify --outfile=dist/bundle.js

# Development with watch
npx esbuild src/index.ts --bundle --watch --outfile=dist/bundle.js
```

## API Usage

### Build API

```javascript
// build.js
import * as esbuild from 'esbuild';

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  minify: true,
  sourcemap: true,
  target: ['es2020'],
  outfile: 'dist/bundle.js',
});

console.log('Build complete!');
```

### Context API (Watch/Serve)

```javascript
import * as esbuild from 'esbuild';

const ctx = await esbuild.context({
  entryPoints: ['src/index.tsx'],
  bundle: true,
  outdir: 'dist',
  sourcemap: true,
});

// Watch mode
await ctx.watch();
console.log('Watching for changes...');

// Dev server
await ctx.serve({
  servedir: 'dist',
  port: 3000,
});
console.log('Server running at http://localhost:3000');
```

### Transform API

```javascript
import * as esbuild from 'esbuild';

// Transform code without bundling
const result = await esbuild.transform(code, {
  loader: 'tsx',
  target: 'es2020',
  minify: true,
});

console.log(result.code);
```

## Configuration Options

### Browser Build

```javascript
await esbuild.build({
  entryPoints: ['src/index.tsx'],
  bundle: true,
  outfile: 'dist/bundle.js',

  // Target browsers
  target: ['chrome90', 'firefox88', 'safari14', 'edge90'],

  // Platform
  platform: 'browser',

  // Module format
  format: 'esm', // 'iife', 'cjs', 'esm'

  // Minification
  minify: true,
  minifyWhitespace: true,
  minifyIdentifiers: true,
  minifySyntax: true,

  // Source maps
  sourcemap: true, // 'linked', 'inline', 'external', 'both'

  // Tree shaking
  treeShaking: true,

  // Define globals
  define: {
    'process.env.NODE_ENV': '"production"',
  },

  // Legal comments
  legalComments: 'none', // 'inline', 'external', 'linked', 'none'
});
```

### Node.js Build

```javascript
await esbuild.build({
  entryPoints: ['src/server.ts'],
  bundle: true,
  outfile: 'dist/server.js',

  platform: 'node',
  target: 'node20',
  format: 'esm',

  // Externalize node_modules
  packages: 'external',

  // Or specify externals
  external: ['express', 'pg'],

  // Node.js banner for ESM
  banner: {
    js: "import { createRequire } from 'module'; const require = createRequire(import.meta.url);",
  },
});
```

### Multiple Entry Points

```javascript
await esbuild.build({
  entryPoints: {
    main: 'src/index.ts',
    worker: 'src/worker.ts',
    admin: 'src/admin.ts',
  },
  bundle: true,
  outdir: 'dist',

  // Code splitting
  splitting: true,
  format: 'esm',

  // Chunk naming
  chunkNames: 'chunks/[name]-[hash]',
  entryNames: '[name]-[hash]',
  assetNames: 'assets/[name]-[hash]',
});
```

## Loaders

### Built-in Loaders

```javascript
await esbuild.build({
  entryPoints: ['src/index.tsx'],
  bundle: true,
  outdir: 'dist',

  loader: {
    '.tsx': 'tsx',
    '.ts': 'ts',
    '.jsx': 'jsx',
    '.js': 'js',
    '.json': 'json',
    '.css': 'css',
    '.svg': 'dataurl',
    '.png': 'file',
    '.woff2': 'file',
  },
});
```

### Asset Handling

```javascript
loader: {
  // Inline as data URL
  '.svg': 'dataurl',
  '.png': 'dataurl',

  // Copy to output directory
  '.woff': 'file',
  '.woff2': 'file',

  // Base64 inline
  '.small-icon': 'base64',

  // Raw text
  '.txt': 'text',

  // Copy without processing
  '.pdf': 'copy',
}
```

## Plugins

### Plugin Structure

```javascript
const myPlugin = {
  name: 'my-plugin',
  setup(build) {
    // Filter for matching files
    build.onResolve({ filter: /\.special$/ }, (args) => {
      return {
        path: path.resolve(args.resolveDir, args.path),
        namespace: 'special',
      };
    });

    // Load file content
    build.onLoad({ filter: /.*/, namespace: 'special' }, async (args) => {
      const content = await fs.readFile(args.path, 'utf8');
      return {
        contents: `export default ${JSON.stringify(content)}`,
        loader: 'js',
      };
    });

    // Build lifecycle hooks
    build.onStart(() => {
      console.log('Build starting...');
    });

    build.onEnd((result) => {
      console.log(`Build finished with ${result.errors.length} errors`);
    });
  },
};

await esbuild.build({
  plugins: [myPlugin],
  // ...
});
```

### Environment Variables Plugin

```javascript
import 'dotenv/config';

const envPlugin = {
  name: 'env',
  setup(build) {
    build.onResolve({ filter: /^env$/ }, (args) => ({
      path: args.path,
      namespace: 'env-ns',
    }));

    build.onLoad({ filter: /.*/, namespace: 'env-ns' }, () => ({
      contents: JSON.stringify(process.env),
      loader: 'json',
    }));
  },
};
```

### SVG as React Component

```javascript
import fs from 'fs';
import path from 'path';

const svgPlugin = {
  name: 'svg',
  setup(build) {
    build.onLoad({ filter: /\.svg$/ }, async (args) => {
      const svg = await fs.promises.readFile(args.path, 'utf8');
      const name = path.basename(args.path, '.svg');

      return {
        contents: `
          export default function ${name}(props) {
            return (
              <svg {...props} dangerouslySetInnerHTML={{ __html: ${JSON.stringify(svg)} }} />
            );
          }
        `,
        loader: 'jsx',
      };
    });
  },
};
```

### Sass Plugin

```javascript
import * as sass from 'sass';

const sassPlugin = {
  name: 'sass',
  setup(build) {
    build.onLoad({ filter: /\.scss$/ }, async (args) => {
      const result = sass.compile(args.path);
      return {
        contents: result.css,
        loader: 'css',
      };
    });
  },
};
```

## Development Server

```javascript
import * as esbuild from 'esbuild';
import http from 'http';

const ctx = await esbuild.context({
  entryPoints: ['src/index.tsx'],
  bundle: true,
  outdir: 'dist',
  sourcemap: true,
});

// Built-in server
const { host, port } = await ctx.serve({
  servedir: 'dist',
  port: 3000,
});

// Or with custom proxy
const proxy = http.createServer((req, res) => {
  const options = {
    hostname: host,
    port: port,
    path: req.url,
    method: req.method,
    headers: req.headers,
  };

  const proxyReq = http.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(res, { end: true });
  });

  req.pipe(proxyReq, { end: true });
});

proxy.listen(8000);
```

## Build Scripts

### package.json

```json
{
  "scripts": {
    "build": "node build.js",
    "dev": "node dev.js",
    "typecheck": "tsc --noEmit"
  }
}
```

### Production Build

```javascript
// build.js
import * as esbuild from 'esbuild';

const isProduction = process.env.NODE_ENV === 'production';

await esbuild.build({
  entryPoints: ['src/index.tsx'],
  bundle: true,
  outdir: 'dist',
  minify: isProduction,
  sourcemap: isProduction ? 'linked' : true,
  target: ['es2020'],
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
  },
  metafile: true,
}).then((result) => {
  // Analyze bundle
  console.log(
    esbuild.analyzeMetafileSync(result.metafile)
  );
});
```

## TypeScript

esbuild transpiles TypeScript but doesn't type-check:

```javascript
await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outfile: 'dist/bundle.js',

  // TypeScript options
  tsconfig: 'tsconfig.json',

  // JSX factory
  jsx: 'automatic',
  jsxImportSource: 'react',

  // Or transform
  jsx: 'transform',
  jsxFactory: 'React.createElement',
  jsxFragment: 'React.Fragment',
});
```

Run type-checking separately:

```bash
# In parallel
npx tsc --noEmit & node build.js
```

See [references/plugins.md](references/plugins.md) for community plugins and [references/recipes.md](references/recipes.md) for common patterns.
