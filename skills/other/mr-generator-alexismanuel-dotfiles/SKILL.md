---
name: mr-generator
description: Generates intelligent GitLab merge request descriptions from git commits with automatic categorization and Jira integration
---

## Features

- **Automatic commit analysis**: Analyzes git commits since diverging from main branch
- **Smart categorization**: Categorizes commits with appropriate emojis (🎉, ✨, 🐛, 💄, 🔥, 🚀, etc.)
- **Jira integration**: Supports Jira ticket numbers and can fetch descriptions
- **Template-based**: Uses your team's MR template format
- **GitLab integration**: Can create MRs directly using `glab` CLI
- **Interactive preview**: Shows MR preview before creation with edit capabilities

## Installation

1. Ensure you have the required dependencies:
   ```bash
   # GitLab CLI
   pip install glab
   
   # Or follow installation instructions at https://gitlab.com/gitlab-org/cli
   ```

2. Make sure the script is executable:
   ```bash
   chmod +x /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py
   ```

## Usage

### Basic usage (outputs to terminal):
```bash
python3 /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py
```

### With Jira ticket:
```bash
python3 /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py --jira PROJ-123
```

### Create MR directly:
```bash
python3 /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py --create --jira PROJ-123
```

The tool will:
1. Generate the MR description
2. Ask for Jira ticket title if not found
3. Show a preview for confirmation
4. Create the MR with title format: `RD-[ticket] [title]`

### Save to file:
```bash
python3 /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py --output mr_description.md
```

### Create MR with custom title:
```bash
python3 /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py --create --title "Custom MR Title" --jira PROJ-123
```

## MR Template

The tool uses this template format:

```
Closes #X or Relates to [link to backlog]

## What's new
- 🎉 Init of a new component
- ✨ [New feature](url)
- 🐛 [Bug fixed](url)
- 💄 [Glitch fixed](url)
- 🔥 [P1 bug fixed](url)
- 🚀 Something is deployed
- ...

## BTW
Something relevant fixed along the way (tech debt, doc).

## SCREENSHOTS
Screenshots of the app with your fix/new feature on.

## Requirements & Dependencies
- Required software (ex. Docker, Node)?
- Critical new dependency (ex. framework)

## Testing

Run the following commands
```
cd ...
make help
make tests
```
```

## Commit Categorization

The tool automatically categorizes commits based on message content:

- **🎉 Init**: `init`, `initial`, `start`
- **✨ Feature**: `feat`, `feature`, `add`
- **🐛 Bug**: `fix`, `bug`, `patch`
- **🔥 P1 Bug**: `p1`, `critical` (with bug keywords)
- **💄 Style/UI**: `style`, `ui`, `glitch`
- **🚀 Deploy**: `deploy`, `release`
- **🔧 Refactor**: `refactor`, `tech debt`, `cleanup`
- **📚 Docs**: `docs`, `documentation`
- **🧪 Tests**: `test`, `tests`
- **🔄 Changes**: Default for other commits

## Configuration

### Jira Integration
Currently, Jira integration is manual (you provide the ticket number). Future versions could include:
- Automatic Jira API integration
- Ticket description fetching
- Status synchronization

### Custom Template
To customize the MR template, modify the `template` variable in the `MRGenerator.__init__` method in `/Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py`.

## Examples

### Example 1: Generate MR for a feature branch
```bash
# On your feature branch
python3 /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py --jira PROJ-456 --create
```

Output:
```
✅ MR created successfully!
https://gitlab.com/cnty-ai/continuity/-/merge_requests/789
```

### Example 2: Generate description without creating MR
```bash
python3 /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py --jira PROJ-789 --output description.md
```

## Troubleshooting

### Common Issues

1. **"Not in a git repository"**
   - Make sure you're in a git repository
   - Check that you have a remote named `origin` or `main`

2. **"glab command not found"**
   - Install GitLab CLI: https://gitlab.com/gitlab-org/cli
   - Authenticate: `glab auth login`

3. **"Could not find main branch"**
   - Ensure you have a `main` or `origin/main` branch
   - The tool tries both `main` and `origin/main`

### Debug Mode

Add debug output by setting environment variable:
```bash
DEBUG=1 python3 /Users/alexismanuel/.config/opencode/skill/mr-generator/scripts/mr_generator.py
```

## Contributing

To extend this tool:

1. **Add new commit categories**: Update the `categorize_commit` method in `mr_generator.py`
2. **Customize template**: Modify the `template` variable in `MRGenerator.__init__`
3. **Add new integrations**: Extend the Jira integration or add other ticket systems
4. **Improve categorization**: Enhance the commit analysis logic

## License

This skill is part of the OpenCode project and follows the same license terms.