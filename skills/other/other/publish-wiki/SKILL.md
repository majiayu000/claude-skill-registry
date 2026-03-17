---
name: publish-wiki
description: >
  Publish pending changes in the sibling hmis.wiki repository to GitHub. Use when wiki
  documentation has been created or edited in the sibling ../hmis.wiki directory and
  needs to be committed and pushed to https://github.com/hmislk/hmis/wiki.
disable-model-invocation: true
allowed-tools: Bash, Read, Glob
---

# Publish to GitHub Wiki

Commit and push pending changes in the sibling `../hmis.wiki` repository to the GitHub Wiki.

**IMPORTANT**: Wiki files live ONLY in the sibling `../hmis.wiki` directory. Do NOT create wiki markdown files inside the main project repository (no `wiki-docs/` folder) - this causes git submodule issues.

## Steps

1. **Check if sibling wiki directory exists**:
   ```bash
   test -d "../hmis.wiki" && echo "EXISTS" || echo "NOT_FOUND"
   ```

2. **If NOT_FOUND, clone the wiki repo**:
   ```bash
   cd .. && git clone https://github.com/hmislk/hmis.wiki.git && cd hmis
   ```

3. **Pull latest changes**:
   ```bash
   cd ../hmis.wiki && git pull origin master
   ```

4. **Check for pending changes**:
   ```bash
   cd ../hmis.wiki && git status
   ```

5. **If there are changes, commit and push**:
   ```bash
   cd ../hmis.wiki
   git add .
   git commit -m "Add/update wiki documentation

   Co-Authored-By: Claude <noreply@anthropic.com>"
   git push origin master
   ```

6. **Report published pages** with wiki URLs: `https://github.com/hmislk/hmis/wiki/Page-Name`

## Important Notes

- Wiki page names come from file names (dashes become spaces)
- Always pull latest wiki before committing to avoid conflicts
- Publish IMMEDIATELY after creating docs, don't wait for PR merge
- All wiki content is in `../hmis.wiki` - NEVER in the main project repo
