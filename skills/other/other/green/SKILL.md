---
name: green
description: Completion criteria -- typecheck, build, test, format must all pass
---

# Green

Before considering work complete, verify affected packages are "green":

```bash
npm run typecheck -w packages/<name>    # or workspaces/<name>
npm run build -w packages/<name>        # or workspaces/<name>
npm test -w packages/<name>             # or workspaces/<name>
npm run format packages/<name>          # or workspaces/<name>
```

All four must pass with zero errors or warnings for each affected package.
