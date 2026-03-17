---
name: watcher-management
description: Manages watcher processes that monitor Gmail, WhatsApp, filesystem, and other external sources. Use when starting, stopping, or monitoring watcher scripts, configuring process management, or troubleshooting watcher issues.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Watcher Management Skill

This skill manages the perception layer of the Personal AI Employee - the watcher processes that monitor external sources and feed data into the Obsidian vault.

## Watcher Types

| Watcher | Source | Check Interval | Output Folder |
|---------|--------|----------------|---------------|
| Gmail Watcher | Gmail API | 2 minutes | /Needs_Action/ |
| WhatsApp Watcher | WhatsApp Web | 30 seconds | /Needs_Action/ |
| Filesystem Watcher | Drop folder | Realtime | /Needs_Action/ |
| Finance Watcher | Bank API | 1 hour | /Needs_Action/ |

## Base Watcher Pattern

```python
class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval

    @abstractmethod
    def check_for_updates(self) -> list:
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        pass

    def run(self):
        while True:
            items = self.check_for_updates()
            for item in items:
                self.create_action_file(item)
            time.sleep(self.check_interval)
```

## Process Management

Use PM2 or supervisord to keep watchers running:

```bash
# Start with PM2
pm2 start gmail_watcher.py --interpreter python3

# Save and set to auto-start
pm2 save
pm2 startup
```

## Reference

For detailed implementation, see [reference.md](reference.md)

For watcher examples, see [examples.md](examples.md)
