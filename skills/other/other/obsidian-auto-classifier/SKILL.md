---
name: obsidian-auto-classifier
description: "Intelligently organize and categorize Markdown notes within an Obsidian vault. This skill leverages Obsidian MCP tools to analyze the vault's current folder structure and note content, ensuring new or misplaced notes are moved to their most contextually appropriate locations (e.g., PARA, Zettelkasten, or custom taxonomies)."
---

# Obsidian Auto Classifier (MCP-Powered)

This skill provides an intelligent workflow for maintaining a clean and organized Obsidian vault by leveraging Model Context Protocol (MCP) tools for real-time vault analysis.

## Categorization Workflow

### 1. Structure Discovery (via Obsidian MCP)
The agent must use MCP tools to map the vault's existing organizational logic.
- **Action**: Call `list_directory` starting from the root (`/`) to identify top-level folders (e.g., `00 Inbox`, `20 Areas`, `30 Zettelkasten`).
- **Deep Scan**: For folders like `30 Zettelkasten` or `40 Resources`, call `list_directory` on subfolders to understand the nested hierarchy.
- **Logic**: Identify if the vault follows PARA, Zettelkasten, Johnny.Decimal, or a custom system.

### 2. Note Analysis
Before moving a note, the agent must understand its "intent" and "content".
- **Action**: Call `read_note` for the target file in the inbox or source folder.
- **Key Indicators**:
    - **Frontmatter**: Look for `tags`, `category`, `project`, or `alias`.
    - **Content Analysis**: Check for keywords, wiki-links to existing projects, or specific templates (e.g., Meeting Notes vs. Paper Summaries).
    - **Contextual Search**: Use `search_notes` with the note's primary topic to see where similar notes are currently stored.

### 3. Smart Classification Decisions
Compare the note's profile against the discovered taxonomy:
- **Daily/Periodic**: Move to `00 Daily Notes` or `Log` (often sorted by year/month).
- **Slipbox/Zettel**: Move to `31 Literature` or `32 Permanent` based on depth and source citations.
- **Projects/Areas**: Move based on active project names found in the text.
- **Archive**: Move finalized research, completed project logs, or legacy notes to `50 Archive`.

### 4. Verified Execution
- **Move**: Use `move_note` (via MCP) or `Move-Item` (via Shell) to relocate the note.
- **Cleanup**: If the note was moved from a temporary folder (like `00 Inbox`), confirm the source is clean.
- **Metadata Update**: (Optional) Call `update_frontmatter` to reflect the new category or update the `modified` timestamp.

## Example Obsidian Triggers
- "整理一下我的 `00 Inbox`，把笔记归位。" (Organize my inbox and put notes back in their place.)
- "把这个 Zettel 笔记放到我的 Slipbox/Literature 里。" (Move this Zettel note into my Slipbox/Literature.)
- "识别这个笔记的内容，看看它属于哪个项目文件夹。" (Identify the content of this note and see which project folder it belongs to.)
- "我刚写了一篇论文综述，把它存到合适的文献库位置。" (I just wrote a paper review, save it to the appropriate literature library location.)
- "扫描我的 Daily Notes，把其中关于 'Robotics' 的内容提取或移动到资源库。" (Scan my Daily Notes and extract or move content about 'Robotics' to the Resources library.)

## Note for Agents
- **MCP Priority**: Always use `list_directory` and `read_note` via the Obsidian MCP first to ensure you are working with the real-time state of the vault.
- **No Hallucination**: Do not assume folder names (e.g., `Archives` vs `50 Archive`). Always verify path existence before moving.
- **Link Integrity**: Be aware that moving notes might affect internal links. Obsidian usually handles this, but verify if the user's settings require manual link updates.
