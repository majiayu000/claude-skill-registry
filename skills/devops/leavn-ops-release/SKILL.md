---
name: Leavn Ops: Release Pipeline Skill
description: Use this skill when preparing releases, generating changelogs, or creating release announcements.
allowed-tools: Edit, Grep
---

# Leavn Ops: Release Pipeline Skill

Use this skill when preparing releases, generating changelogs, or creating release announcements.

## CLI Commands Available

```bash
# Generate release notes from commits
leavn-ops release notes --since v1.2.0 --version v1.3.0

# Update changelog
leavn-ops release changelog --version v1.3.0

# Generate social announcements
leavn-ops release social --version v1.3.0
```

## Release Workflow

### Pre-Release Checklist

1. **Code Freeze**
   - [ ] All PRs merged
   - [ ] No critical bugs open
   - [ ] Tests passing

2. **Version Bump**
   - [ ] Update version in Xcode
   - [ ] Update build number
   - [ ] Tag commit

3. **Documentation**
   - [ ] Run `leavn-ops release notes`
   - [ ] Run `leavn-ops release changelog`
   - [ ] Review and edit generated content

4. **Testing**
   - [ ] TestFlight build uploaded
   - [ ] Internal testing complete
   - [ ] Beta feedback addressed

5. **App Store Submission**
   - [ ] Screenshots updated (if needed)
   - [ ] What's New text ready
   - [ ] Submit for review

### Commit Message Convention

Use emoji prefixes for automatic categorization:

| Emoji | Category | Example |
|-------|----------|---------|
| `feat` or `add` | Features | `feat: Add prayer reminder notifications` |
| `fix` or `bug` | Bug Fixes | `fix: Resolve audio playback crash` |
| `refactor` or `improve` | Improvements | `refactor: Optimize Bible search performance` |
| `docs` | Documentation | `docs: Update API documentation` |

### Release Notes Best Practices

#### User-Facing Notes
- Lead with biggest/most requested feature
- Use plain language (no tech jargon)
- Include 2-4 bullet points max
- End with appreciation

**Example:**
```
What's New in Leavn 1.3.0:

- New prayer reminders help you stay consistent
- Improved Bible search finds verses faster
- Audio playback is now smoother than ever
- Bug fixes and performance improvements

Thank you for being part of our community!
```

#### Developer Notes
- Include all commits since last release
- Categorize by type (features, fixes, improvements)
- Reference issue/PR numbers
- Note breaking changes

### Social Announcement Templates

#### Twitter Thread
```
1/ Leavn [version] is here!

We've been working hard on this update, and we can't wait
for you to try it. Here's what's new...

2/ [Feature 1 description with benefit]

3/ [Feature 2 description with benefit]

4/ Update now from the App Store and let us know what
you think!

[App Store link]

#Leavn #Update
```

#### Instagram Post
```
Update Alert!

Leavn [version] just dropped with:
- [Feature 1]
- [Feature 2]
- [Feature 3]

Update now and let us know your favorite new feature!

Link in bio

#Leavn #AppUpdate #ChristianApp
```

### Version Numbering

Follow Semantic Versioning:
- **Major** (X.0.0): Breaking changes, major redesigns
- **Minor** (1.X.0): New features, significant improvements
- **Patch** (1.0.X): Bug fixes, minor improvements

### App Store What's New

#### Character Limit
- 4000 characters max
- First ~80 characters most visible

#### Structure
```
[Emoji] [Main Feature/Update]

[2-4 bullet points of changes]

[Thank you message]
```

## Integration with CI/CD

After generating release content:
1. Review generated notes in `~/.local/share/leavn-ops/outputs/`
2. Copy to App Store Connect
3. Create GitHub release with detailed notes
4. Schedule social posts using content from `release social`

## Hotfix Protocol

For urgent fixes:
1. Branch from main: `hotfix/description`
2. Fix and test
3. Version bump (patch only)
4. Run `leavn-ops release notes --since [last-tag]`
5. Submit immediately

## Output Location
All release content saved to: `~/.local/share/leavn-ops/outputs/`
