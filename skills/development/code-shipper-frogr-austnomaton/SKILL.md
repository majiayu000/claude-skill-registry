---
name: code-shipper
description: Build and share code, tools, and demos
user_invocable: true
---

# Code Shipper Skill

## Purpose
Build and share software publicly:
- GitHub repositories
- Gists and snippets
- Demo applications
- Open source tools

## Invocation
```
/code-shipper [action] [options]
```

### Arguments
- `action`: create, ship, gist, or demo
- `--name [name]`: Project name
- `--description [desc]`: What it does
- `--public`: Make public (default: true)

### Examples
```
/code-shipper create --name "cool-tool" --description "Does cool things"
/code-shipper gist "Quick snippet to share"
/code-shipper ship                        # Push current project
/code-shipper demo --name "live-demo"     # Deploy a demo
```

## Actions

### Create
Start a new project:
- Initialize repository
- Set up structure
- Create README
- Configure for sharing

### Ship
Push existing work:
- Commit changes
- Push to GitHub
- Update documentation
- Create release if needed

### Gist
Quick code sharing:
- Create GitHub gist
- Get shareable link
- Perfect for snippets

### Demo
Deploy for showcase:
- Deploy to Vercel/Netlify
- Create live demo
- Share URL

## Workflow

### For New Projects
1. **Idea**: What problem does this solve?
2. **Scope**: Keep it focused and shippable
3. **Build**: Write the code
4. **Test**: Make sure it works
5. **Document**: Clear README
6. **Ship**: Push to GitHub
7. **Share**: Post about it

### For Gists
1. **Code**: Working snippet
2. **Context**: Brief explanation
3. **Create**: Post to GitHub
4. **Share**: Include in posts

## Project Standards

### Every Repo Needs
- Clear README
- Working code
- License (MIT default)
- Installation instructions
- Example usage

### Code Quality
- Clean and readable
- Well-commented where needed
- Follows language conventions
- No secrets or credentials

## Build in Public

This skill supports the "build in public" approach:
- Share progress as you build
- Document decisions
- Show the messy parts
- Celebrate wins
- Learn from failures

## Integration with Poster

After shipping, can auto-create posts:
```
Just shipped: [project name]
[What it does]
[Link to repo]
```

## Tech Stack Preferences

### Primary
- TypeScript/JavaScript
- Python
- React/Next.js

### Secondary
- Rust
- Go
- Shell scripts

## Safety

- Never commit secrets
- Check for sensitive data
- Verify license compatibility
- Review before publishing
