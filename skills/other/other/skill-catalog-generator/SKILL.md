---
name: "Skill: Skill Catalog Generator"
description: "Generate dynamic skill catalogs with network diagrams to visualize Alex's capabilities and track learning progress."
---

# Skill: Skill Catalog Generator

> Generate dynamic skill catalogs with network diagrams to visualize Alex's capabilities and track learning progress.

---

## Purpose

This skill enables Alex to:

1. **Generate skill catalogs** — List all installed skills with categories, inheritance, and purposes
2. **Create network diagrams** — Mermaid flowcharts showing skill relationships
3. **Track learning progress** — Show which skills have been activated, user-created skills
4. **Post-migration reporting** — Display what skills are available after upgrade

---

## Activation Triggers

- "show my skills" / "what skills do I have"
- "skill catalog" / "generate catalog"
- "skill network" / "show skill diagram"
- "learning progress" / "what have I learned"
- Post-migration completion
- `/skills` slash command

---

## Output Format

### Catalog Structure

```markdown
# My Alex Skills

> Generated: {timestamp}
> Total Skills: {count} ({system} system, {user} user-created)

## Summary

| Category | Count | Active |
| -------- | ----- | ------ |
| 🧠 Cognitive | 8 | 6 |
| 🔧 Engineering | 7 | 7 |
| ... | ... | ... |

## Skills by Category

### 🧠 Cognitive & Learning

| Skill | Type | Status | Last Used |
| ----- | ---- | ------ | --------- |
| cognitive-load | system | ✅ active | 2026-01-30 |
| my-project-patterns | user | ✅ active | 2026-01-29 |
| ... | ... | ... | ... |

## Network Diagram

{mermaid diagram}

## User-Created Skills

| Skill | Created | Connections |
| ----- | ------- | ----------- |
| my-project-patterns | 2026-01-15 | 3 |
| team-conventions | 2026-01-20 | 1 |
```

---

## Generation Algorithm

### Step 1: Scan Skills Directory

```typescript
interface SkillInfo {
  name: string;
  category: string;
  inheritance: 'inheritable' | 'master-only' | 'heir:vscode' | 'heir:m365' | 'user';
  purpose: string;
  hasSynapses: boolean;
  connectionCount: number;
  lastModified: Date;
  isUserCreated: boolean;
  isTemporary: boolean;      // From synapses.json "temporary": true
  removeAfter?: string;      // From synapses.json "removeAfter"
  staleProne: boolean;       // True if skill depends on rapidly changing tech
}

async function scanSkills(skillsPath: string): Promise<SkillInfo[]> {
  const skills: SkillInfo[] = [];
  const folders = await fs.readdir(skillsPath);

  for (const folder of folders) {
    const skillPath = path.join(skillsPath, folder);
    const skillMd = path.join(skillPath, 'SKILL.md');
    const synapsesJson = path.join(skillPath, 'synapses.json');

    if (!await fs.pathExists(skillMd)) continue;

    const content = await fs.readFile(skillMd, 'utf8');
    const synapses = await fs.pathExists(synapsesJson)
      ? await fs.readJson(synapsesJson)
      : null;

    skills.push({
      name: folder,
      category: extractCategory(content),
      inheritance: extractInheritance(content, synapses),
      purpose: extractPurpose(content),
      hasSynapses: !!synapses,
      connectionCount: synapses ? Object.keys(synapses.connections || {}).length : 0,
      lastModified: (await fs.stat(skillMd)).mtime,
      isUserCreated: !SYSTEM_SKILLS.includes(folder),
      isTemporary: synapses?.temporary === true,
      removeAfter: synapses?.removeAfter,
    });
  }

  return skills;
}
```

### Step 2: Categorize Skills

```typescript
const CATEGORIES = {
  'cognitive': { emoji: '🧠', skills: ['cognitive-load', 'learning-psychology', 'appropriate-reliance', 'bootstrap-learning', 'meditation', 'meditation-facilitation', 'knowledge-synthesis', 'global-knowledge'] },
  'engineering': { emoji: '🔧', skills: ['testing-strategies', 'refactoring-patterns', 'debugging-patterns', 'code-review', 'git-workflow', 'project-scaffolding', 'vscode-environment'] },
  'operations': { emoji: '🚨', skills: ['error-recovery-patterns', 'root-cause-analysis', 'incident-response', 'release-preflight'] },
  'security': { emoji: '🔐', skills: ['privacy-responsible-ai', 'microsoft-sfi'] },
  'documentation': { emoji: '📝', skills: ['writing-publication', 'markdown-mermaid', 'lint-clean-markdown', 'ascii-art-alignment', 'llm-model-selection'] },
  'visual': { emoji: '🎨', skills: ['svg-graphics', 'image-handling'] },
  'architecture': { emoji: '🏗️', skills: ['architecture-refinement', 'architecture-health', 'self-actualization', 'heir-curation'] },
  'vscode': { emoji: '💻', skills: ['vscode-extension-patterns', 'chat-participant-patterns'] },
  'm365': { emoji: '☁️', skills: ['m365-agent-debugging', 'teams-app-patterns'] },
  'user': { emoji: '👤', skills: [] },  // Dynamically populated
};
```

### Step 3: Generate Mermaid Diagram (High Fidelity)

The diagram generator must produce output matching the baseline catalog's richness.

#### Connection Schema in synapses.json

```typescript
interface Connection {
  target: string;           // Target skill name
  type: string;             // enables, applies, extends, complements, triggers, curates
  strength: number;         // 0.0-1.0
  bidirectional?: boolean;  // true = <--> arrow
  weak?: boolean;           // true = -.-> dashed arrow
}
```

#### Arrow Types

| Condition | Arrow | Meaning |
| --------- | ----- | ------- |
| `bidirectional: true` | `<-->` | Mutual reinforcement |
| `weak: true` OR `strength < 0.5` | `-.->` | Optional/weak link |
| Default | `-->` | Direct dependency |

#### Multi-Target Syntax

When a skill connects to multiple targets, use Mermaid's multi-target syntax:

```text
SCG --> MM & AH & KS
```

Not individual lines (reduces diagram clutter).

```typescript
function generateNetworkDiagram(skills: SkillInfo[]): string {
  const lines: string[] = [
    '```mermaid',
    "%%{init: {'theme': 'base', 'themeVariables': { 'lineColor': '#666', 'primaryColor': '#e8f4f8', 'primaryBorderColor': '#0969da'}}}%%",
    'flowchart LR',
  ];

  // Group by category
  for (const [category, config] of Object.entries(CATEGORIES)) {
    const categorySkills = skills.filter(s => config.skills.includes(s.name) || (category === 'user' && s.isUserCreated));
    if (categorySkills.length === 0) continue;

    lines.push(`    subgraph ${capitalize(category)}["${config.emoji} ${capitalize(category)}"]`);
    for (const skill of categorySkills) {
      const abbrev = toAbbreviation(skill.name);
      lines.push(`        ${abbrev}[${skill.name}]`);
    }
    lines.push('    end');
  }

  // Add connections from synapses - GROUP by source for multi-target syntax
  const connectionGroups = new Map<string, { targets: string[], arrow: string }>();

  for (const skill of skills) {
    if (!skill.hasSynapses) continue;
    const synapses = loadSynapses(skill.name);
    const connections = normalizeConnections(synapses.connections);

    for (const conn of connections) {
      const sourceAbbrev = toAbbreviation(skill.name);
      const targetAbbrev = toAbbreviation(conn.target);

      // Determine arrow type
      let arrow = '-->';
      if (conn.bidirectional) {
        arrow = '<-->';
      } else if (conn.weak || (conn.strength && conn.strength < 0.5)) {
        arrow = '-.->';
      }

      // Group connections by source+arrow for multi-target syntax
      const key = `${sourceAbbrev}|${arrow}`;
      if (!connectionGroups.has(key)) {
        connectionGroups.set(key, { targets: [], arrow });
      }
      connectionGroups.get(key)!.targets.push(targetAbbrev);
    }
  }

  // Output grouped connections using multi-target syntax
  for (const [key, group] of connectionGroups) {
    const source = key.split('|')[0];
    if (group.targets.length === 1) {
      lines.push(`    ${source} ${group.arrow} ${group.targets[0]}`);
    } else {
      // Multi-target: A --> B & C & D
      lines.push(`    ${source} ${group.arrow} ${group.targets.join(' & ')}`);
    }
  }

  // Add styling - Inheritance colors
  lines.push('');
  lines.push('    %% Styling - Inheritance');
  lines.push('    classDef master fill:#fff3cd,stroke:#856404');
  lines.push('    classDef vscode fill:#e1f0ff,stroke:#0969da');
  lines.push('    classDef m365 fill:#e6f4ea,stroke:#1a7f37');
  lines.push('    classDef inheritable fill:#e0f7fa,stroke:#00838f');
  lines.push('    classDef user fill:#e6ffe6,stroke:#2da02d');
  lines.push('');
  lines.push('    %% Styling - Staleness (dashed border)');
  lines.push('    classDef stale stroke-dasharray:5 5,stroke-width:2px');
  lines.push('');
  lines.push('    %% Styling - Temporary (purple dashed)');
  lines.push('    classDef temp fill:#f3e8ff,stroke:#7c3aed,stroke-dasharray:5 5');

  // Apply classes based on inheritance
  const masterSkills = skills.filter(s => s.inheritance === 'master-only').map(s => toAbbreviation(s.name));
  const vscodeSkills = skills.filter(s => s.inheritance === 'heir:vscode').map(s => toAbbreviation(s.name));
  const m365Skills = skills.filter(s => s.inheritance === 'heir:m365').map(s => toAbbreviation(s.name));
  const inheritableSkills = skills.filter(s => s.inheritance === 'inheritable' && !s.isTemporary).map(s => toAbbreviation(s.name));
  const userSkills = skills.filter(s => s.isUserCreated).map(s => toAbbreviation(s.name));
  const tempSkills = skills.filter(s => s.isTemporary).map(s => toAbbreviation(s.name));
  const staleSkills = skills.filter(s => s.staleProne).map(s => toAbbreviation(s.name));

  // Apply classes to nodes (classDef alone does nothing without this!)
  if (masterSkills.length > 0) lines.push(`    class ${masterSkills.join(',')} master`);
  if (vscodeSkills.length > 0) lines.push(`    class ${vscodeSkills.join(',')} vscode`);
  if (m365Skills.length > 0) lines.push(`    class ${m365Skills.join(',')} m365`);
  if (inheritableSkills.length > 0) lines.push(`    class ${inheritableSkills.join(',')} inheritable`);
  if (userSkills.length > 0) lines.push(`    class ${userSkills.join(',')} user`);
  if (tempSkills.length > 0) lines.push(`    class ${tempSkills.join(',')} temp`);
  if (staleSkills.length > 0) lines.push(`    class ${staleSkills.join(',')} stale`);

  lines.push('```');

  return lines.join('\n');
}

// Normalize connections to array format (supports both object and array)
function normalizeConnections(connections: any): Connection[] {
  if (Array.isArray(connections)) {
    return connections;
  }
  // Object format: { "target-name": { weight, relationship } }
  return Object.entries(connections).map(([target, data]: [string, any]) => ({
    target,
    type: data.relationship || data.type || 'enables',
    strength: data.weight || data.strength || 0.5,
    bidirectional: data.bidirectional || false,
    weak: data.weak || false,
  }));
}
```

### Diagram Legend

Include this legend in generated catalogs:

```markdown
### Legend

| Color | Inheritance |
| ----- | ----------- |
| 🟨 Yellow | Master-only |
| 🟦 Blue | VS Code heir |
| 🟩 Green | M365 heir |
| 🟪 Purple (dashed) | Temporary |
| 🧊 Cyan | Inheritable |

| Border | Meaning |
| ------ | ------- |
| ┅ Dashed | Staleness-prone or temporary |
| ── Solid | Standard skill |

| Arrow | Meaning |
| ----- | ------- |
| → Solid | Strong connection (weight > 0.7) |
| ⇢ Dashed | Weak connection (weight ≤ 0.7) |
```

### Step 4: Generate Full Catalog

```typescript
async function generateSkillCatalog(rootPath: string): Promise<string> {
  const skillsPath = path.join(rootPath, '.github', 'skills');
  const skills = await scanSkills(skillsPath);

  const systemSkills = skills.filter(s => !s.isUserCreated);
  const userSkills = skills.filter(s => s.isUserCreated);

  const catalog = `# My Alex Skills

> Generated: ${new Date().toISOString().split('T')[0]}
> Total Skills: ${skills.length} (${systemSkills.length} system, ${userSkills.length} user-created)

## Summary

| Category | Count |
| -------- | ----- |
${generateCategorySummary(skills)}

## Skills by Category

${generateSkillTables(skills)}

## Network Diagram

${generateNetworkDiagram(skills)}

${userSkills.length > 0 ? generateUserSkillsSection(userSkills) : ''}

---

*Catalog generated by Alex Skill Catalog Generator*
`;

  return catalog;
}
```

---

## VS Code Integration

### Command: `Alex: Show Skill Catalog`

```typescript
vscode.commands.registerCommand('alex.showSkillCatalog', async () => {
  const rootPath = getWorkspaceRoot();
  const catalog = await generateSkillCatalog(rootPath);

  // Create virtual document
  const uri = vscode.Uri.parse('alex-catalog://skills/catalog.md');
  const doc = await vscode.workspace.openTextDocument(uri);
  await vscode.window.showTextDocument(doc, { preview: true });

  // Or save to file
  const catalogPath = path.join(rootPath, '.github', 'SKILL-CATALOG.md');
  await fs.writeFile(catalogPath, catalog);

  vscode.window.showInformationMessage(
    `Skill catalog generated with ${skills.length} skills`,
    'Open Catalog'
  ).then(choice => {
    if (choice === 'Open Catalog') {
      vscode.commands.executeCommand('markdown.showPreview', vscode.Uri.file(catalogPath));
    }
  });
});
```

### Post-Migration Hook

```typescript
// In migration completion
async function showPostMigrationCatalog(rootPath: string, migrationReport: MigrationReport) {
  const catalog = await generateSkillCatalog(rootPath);

  // Add migration-specific header
  const header = `# 🎉 Migration Complete!

## What Was Migrated

- **Skills restored:** ${migrationReport.skills.length}
- **Domain knowledge:** ${migrationReport.dk.length} files
- **User profile:** ${migrationReport.profileRestored ? '✅' : '❌'}

---

`;

  const fullCatalog = header + catalog;
  await showCatalogDocument(fullCatalog);
}
```

---

## User-Created Skills Tracking

### Identifying User Skills

A skill is user-created if:

1. Not in the `SYSTEM_SKILLS` list (shipped with extension)
2. Or has `"userCreated": true` in synapses.json
3. Or was created after initial installation (compare to manifest)

### Learning Progress Metrics

```typescript
interface LearningProgress {
  totalSkills: number;
  systemSkills: number;
  userSkills: number;
  skillsWithConnections: number;
  totalConnections: number;
  mostConnectedSkill: string;
  recentlyUsedSkills: string[];  // From episodic records
  suggestedNextSkills: string[]; // Based on current connections
}
```

---

## Output Locations

| Trigger | Output |
| ------- | ------ |
| Command | Preview in VS Code |
| Slash command | Chat response |
| Post-migration | Modal + saved file |
| `/skills` | Inline in chat |

---

## Related Skills

- `markdown-mermaid` — Diagram generation
- `architecture-health` — Skill validation
- `knowledge-synthesis` — Pattern extraction

---

## Inheritance

**Inheritable** — All heirs can generate catalogs for their installed skills.
