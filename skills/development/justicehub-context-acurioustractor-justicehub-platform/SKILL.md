---
name: justicehub-context
description: This skill ensures Claude always works in the JusticeHub codebase located
  at /Users/benknight/Code/JusticeHub and never accidentally works in the wrong repository.
---

# JusticeHub Context Skill

## Purpose
This skill ensures Claude always works in the JusticeHub codebase located at `/Users/benknight/Code/JusticeHub` and never accidentally works in the wrong repository.

## When to Use
This skill is automatically invoked at the start of every conversation about JusticeHub development.

## Instructions

You are working on the **JusticeHub** project located at:
```
/Users/benknight/Code/JusticeHub
```

### Critical Rules:
1. **ALWAYS** use absolute paths starting with `/Users/benknight/Code/JusticeHub/`
2. **NEVER** work in `/Users/benknight/act-global-infrastructure/` unless explicitly asked
3. **ALWAYS** verify you're in the correct directory before making changes
4. When creating or editing files, use the full path: `/Users/benknight/Code/JusticeHub/src/...`

### Project Structure:
```
/Users/benknight/Code/JusticeHub/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── stories/
│   │   │   ├── the-pattern/
│   │   │   └── intelligence/
│   │   └── ...
│   ├── components/       # React components
│   │   └── visualizations/
│   ├── lib/             # Utilities and helpers
│   └── contexts/        # React contexts
├── scripts/             # Build and data scripts
├── .claude/             # Claude configuration
│   └── skills/          # Custom skills
└── package.json

```

### Common Mistakes to Avoid:
- ❌ Working in `/Users/benknight/act-global-infrastructure/`
- ❌ Using relative paths without verifying current directory
- ❌ Creating files in the wrong codebase
- ✅ Always use full paths: `/Users/benknight/Code/JusticeHub/...`
- ✅ Verify directory before file operations
- ✅ Check git status to confirm you're in JusticeHub repo

### Verification Command:
Before making changes, always verify:
```bash
pwd  # Should output: /Users/benknight/Code/JusticeHub
```

### Key Technologies:
- Next.js 14 (App Router)
- React 18
- TypeScript
- Supabase (PostgreSQL)
- D3.js (visualizations)
- TailwindCSS
- PM2 (process manager)

### ALMA Integration:
JusticeHub uses the ALMA (Adaptive Learning for Meaningful Accountability) system for:
- Media sentiment tracking (`alma_media_articles` table)
- Daily sentiment aggregation (`alma_daily_sentiment` view)
- Continuous intelligence gathering

### Local Development:
- Dev server: `http://localhost:3003`
- PM2 process name: `justicehub`
- Restart command: `pm2 restart justicehub`

## Output
This skill does not produce output - it sets context for the conversation.
