---
name: solid-deployment
description: "SolidStart deployment: build process, platform-specific configs, environment variables, SSR vs SPA deployment, edge deployment, Vercel, Netlify, Cloudflare, AWS."
metadata:
  globs:
    - "**/deployment*"
    - "**/deploy*"
    - "netlify.toml"
    - "vercel.json"
---

# SolidStart Deployment

Complete guide to deploying SolidStart applications to various platforms. Understand build processes, platform configurations, and deployment strategies.

## Build Process

SolidStart builds your application for production:

```bash
# Build for production
npm run build

# Output directory
dist/
```

**Build output:**
- Client bundle
- Server bundle (for SSR)
- Static assets
- HTML files

## Platform-Specific Deployment

### Vercel

**Web Interface:**
1. Connect GitHub repository
2. Configure build settings
3. Add environment variables
4. Deploy

**CLI:**
```bash
npm i -g vercel
vercel
```

**Configuration:**
- Automatic detection for SolidStart
- Serverless functions
- Edge functions support
- Environment variables in dashboard

### Netlify

**Web Interface:**
1. Connect Git repository
2. Set publish directory to `dist`
3. Configure build command
4. Add environment variables

**CLI:**
```bash
npm i -g netlify-cli
netlify init
```

**netlify.toml:**
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Cloudflare Pages

**Configuration:**
- Build command: `npm run build`
- Build output: `dist`
- Node.js version: 18+

**Environment variables:**
- Set in Cloudflare dashboard

### AWS (FlightControl/SST)

**FlightControl:**
- AWS deployment with minimal config
- Automatic infrastructure setup
- Environment variable management

**SST:**
- Infrastructure as code
- Serverless architecture
- Custom AWS resources

### Other Platforms

**Railway:**
- Simple Node.js deployment
- Automatic builds from Git
- Environment variables

**Firebase:**
- Hosting for static sites
- Functions for server code
- Environment config

**Stormkit:**
- Git-based deployment
- Environment management
- Preview deployments

**Zerops:**
- Container-based deployment
- Automatic scaling
- Environment variables

## Environment Variables

### Build-Time Variables

Set in platform dashboard or `.env` files:

```env
VITE_API_URL=https://api.example.com
VITE_APP_NAME=My App
```

### Runtime Variables (Server)

```env
DATABASE_URL=postgresql://...
API_SECRET_KEY=secret123
```

**Platform-specific:**
- Vercel: Dashboard → Settings → Environment Variables
- Netlify: Site settings → Environment variables
- Cloudflare: Pages → Settings → Environment variables

## SSR vs SPA Deployment

### SSR Deployment

**Requirements:**
- Node.js runtime
- Server-side rendering support
- Streaming support (optional)

**Platforms:**
- Vercel (serverless functions)
- Netlify (serverless functions)
- Cloudflare Workers
- AWS Lambda
- Node.js servers

**Configuration:**
```tsx
// app.config.ts
export default defineConfig({
  server: {
    preset: "node-server", // or platform-specific
  },
});
```

### SPA Deployment

**Requirements:**
- Static hosting
- Client-side routing
- No server needed

**Platforms:**
- Netlify (static)
- Vercel (static)
- Cloudflare Pages
- GitHub Pages
- Any static host

**Configuration:**
```tsx
// app.config.ts
export default defineConfig({
  ssr: false, // Disable SSR
});
```

## Edge Deployment

Deploy to edge locations for low latency:

**Cloudflare Workers:**
```tsx
// app.config.ts
export default defineConfig({
  server: {
    preset: "cloudflare-workers",
  },
});
```

**Vercel Edge:**
- Automatic edge deployment
- Edge functions support
- Global distribution

## Build Configuration

### Build Command

```bash
# Standard build
npm run build

# With environment
NODE_ENV=production npm run build
```

### Output Directory

Default: `dist/`

Configure in `app.config.ts`:
```tsx
export default defineConfig({
  vite: {
    build: {
      outDir: "dist",
    },
  },
});
```

## Common Deployment Patterns

### Static Site Generation

```tsx
// Generate static pages
export default defineConfig({
  ssr: false,
  prerender: true,
});
```

### Hybrid Rendering

```tsx
// Some routes SSR, some static
export default defineConfig({
  server: {
    preset: "node-server",
  },
});
```

### Serverless Functions

```tsx
// Deploy as serverless
export default defineConfig({
  server: {
    preset: "vercel", // or "netlify"
  },
});
```

## Environment-Specific Builds

### Development

```bash
npm run dev
```

### Production

```bash
npm run build
npm run start
```

### Preview

```bash
npm run build
npm run preview
```

## Best Practices

1. **Set environment variables:**
   - Use platform dashboard
   - Never commit secrets
   - Use different values per environment

2. **Configure build settings:**
   - Set correct build command
   - Set output directory
   - Configure Node.js version

3. **Handle routing:**
   - SPA: Redirect all to index.html
   - SSR: Configure server properly

4. **Optimize assets:**
   - Enable compression
   - Use CDN for static assets
   - Optimize images

5. **Monitor deployments:**
   - Check build logs
   - Test after deployment
   - Set up error tracking

## Troubleshooting

### Build Fails

- Check Node.js version
- Verify environment variables
- Review build logs
- Check dependencies

### Routing Issues

- Configure redirects for SPA
- Check server configuration for SSR
- Verify route definitions

### Environment Variables Not Working

- Check variable names (VITE_ prefix)
- Verify platform configuration
- Restart build after changes

## Summary

- **Build**: `npm run build` → `dist/`
- **Platforms**: Vercel, Netlify, Cloudflare, AWS, etc.
- **SSR**: Requires Node.js/serverless runtime
- **SPA**: Static hosting only
- **Environment**: Set variables in platform dashboard
- **Edge**: Deploy to edge locations for performance

