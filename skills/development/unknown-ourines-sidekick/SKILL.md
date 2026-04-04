# OSS Promoter Skill

Batch promote open source projects to tech weeklies and communities.

## What this skill does

1. **Search for weeklies**: Use WebSearch to find new tech weeklies that accept submissions
2. **Extract project info**: Use `gh` to get repo description, README, stars, etc.
3. **Generate submissions**: Create tailored issue content for each weekly
4. **Batch submit**: Use `gh issue create` or `gh issue comment` to submit

## Usage

When the user wants to promote an open source project:

1. First, ask for the GitHub repo URL if not provided
2. Load the weeklies config from `${CLAUDE_PLUGIN_ROOT}/config/weeklies.json`
3. Use `gh repo view <repo> --json name,description,url,stargazerCount,readme` to get project info
4. For each enabled weekly in the config:
   - Generate title using the `title_template`
   - Generate body using the project info
   - If `type` is "issue": use `gh issue create --repo <weekly_repo> --title "<title>" --body "<body>"`
   - If `type` is "comment": use `gh issue comment <issue_number> --repo <weekly_repo> --body "<body>"`
5. Track submissions and report results

## Commands

- `/oss-promoter:promote <repo-url>` - Promote a project to all enabled weeklies
- `/oss-promoter:search` - Search for new weeklies to add to config
- `/oss-promoter:list` - List all configured weeklies and their status

## Submission Template

For Chinese weeklies, use this template:

```markdown
## 项目介绍

[{name}]({url}) - {description}

## 核心功能

{features_from_readme}

## 使用示例

{usage_example}

## 链接

- GitHub: {url}
- Stars: {stars}
```

## Tools Available

- `WebSearch` - Search for new weeklies
- `Bash` with `gh` - GitHub CLI for repo info and issue creation
- `Read` - Read config files

## Important Notes

- Always check if an issue already exists before creating a new one
- Respect rate limits - add delays between submissions if needed
- Some weeklies require specific formats - check their README first
- Set `enabled: false` for weeklies that are language/topic specific and don't match the project
