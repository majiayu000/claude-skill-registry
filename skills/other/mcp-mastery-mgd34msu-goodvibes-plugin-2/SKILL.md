---
name: mcp-mastery
description: >-
  Complete MCP tool reference and usage patterns. Load this skill to become an expert
  in all 80+ GoodVibes MCP tools. Use when you need to understand tool capabilities,
  find the right tool for a task, or learn proper tool invocation patterns.
---

# MCP Tool Mastery

Master the 80+ MCP tools available in the GoodVibes plugin. This skill teaches you when and how to use each tool for maximum effectiveness.

## THE LAW: Tool-First Development

**This is non-negotiable. Violating these rules means you're not doing your job.**

### Before ANY Task

```bash
# 1. ALWAYS check tool schema first
mcp-cli info plugin_goodvibes_goodvibes-tools/<tool_name>

# 2. THEN make the call
mcp-cli call plugin_goodvibes_goodvibes-tools/<tool_name> '{"param": "value"}'
```

### The Golden Rules

1. **Never skip `mcp-cli info`** - Schemas are tool-specific. Your assumptions are wrong.
2. **Never do manually what a tool can do** - If a tool exists, use it.
3. **Skills contain expertise you lack** - Load them to become an expert.
4. **Tools provide current information** - Your training data is outdated.

---

## Quick Reference: Tool Selection by Task

### Starting Any Task

| First Action | Tool | Command |
|--------------|------|---------|
| Understand project | `detect_stack` | `mcp-cli call .../detect_stack '{}'` |
| Find relevant skills | `recommend_skills` | `mcp-cli call .../recommend_skills '{"task": "..."}'` |
| Check for issues | `project_issues` | `mcp-cli call .../project_issues '{}'` |

### Before Writing Code

| Task | Tool | Why |
|------|------|-----|
| Follow patterns | `scan_patterns` | Match existing code style |
| Understand types | `get_schema` | Know the interfaces |
| Check conventions | `get_conventions` | Follow project standards |

### During Code Navigation

| Need | Tool | Use Case |
|------|------|----------|
| Find definition | `go_to_definition` | Jump to where symbol is defined |
| Find usages | `find_references` | See all places symbol is used |
| Find implementations | `get_implementations` | Find concrete implementations of interface |
| Search symbols | `workspace_symbols` | Find symbols by name across codebase |
| Understand hierarchy | `get_type_hierarchy` | See inheritance chain |

### Before Editing Code

| Task | Tool | Mandatory? |
|------|------|------------|
| Check patterns | `scan_patterns` | Yes |
| Preview errors | `validate_edits_preview` | Recommended |
| Check if safe to delete | `safe_delete_check` | Before deletion |
| Find affected tests | `find_tests_for_file` | Yes |

### After Editing Code

| Task | Tool | When |
|------|------|------|
| Type check | `check_types` | After TypeScript changes |
| Get diagnostics | `get_diagnostics` | For file-level issues |
| Run smoke test | `run_smoke_test` | Before committing |

### Debugging

| Problem | Tool | What It Does |
|---------|------|--------------|
| Stack trace | `parse_error_stack` | Parse and explain errors |
| Type error | `explain_type_error` | Explain TypeScript errors |
| Find dead code | `find_dead_code` | Identify unused code |
| Check circular deps | `find_circular_deps` | Find dependency cycles |

### Security & Quality

| Concern | Tool | Use |
|---------|------|-----|
| Secrets in code | `scan_for_secrets` | Find exposed credentials |
| Env config | `get_env_config` | Understand environment setup |
| Permissions | `check_permissions` | Verify file/dir permissions |

---

## Complete Tool Catalog

### Discovery & Search (6 tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `search_skills` | Find skills by keyword | Starting new domain task |
| `search_agents` | Find agents by capability | Need specialized help |
| `search_tools` | Find tools by function | Looking for specific capability |
| `recommend_skills` | AI-powered skill suggestions | Before any complex task |
| `get_skill_content` | Load skill into context | After finding relevant skill |
| `get_agent_content` | Read agent definition | Understanding agent capabilities |

### Dependencies & Stack (6 tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `skill_dependencies` | Find skill prerequisites | Before loading skills |
| `detect_stack` | Identify project technologies | First action in new project |
| `check_versions` | Verify package versions | Debugging version issues |
| `scan_patterns` | Find code patterns in project | Before writing similar code |
| `analyze_dependencies` | Deep dependency analysis | Understanding dep structure |
| `find_circular_deps` | Detect circular dependencies | Before refactoring |

### Documentation & Schema (5 tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `fetch_docs` | Get library documentation | Need API reference |
| `get_schema` | Get type/interface schemas | Before working with types |
| `read_config` | Read configuration files | Understanding project config |
| `get_database_schema` | Get DB schema info | Before database work |
| `get_api_routes` | Map API endpoints | Understanding API structure |

### Quality & Testing (7 tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `validate_implementation` | Check code meets specs | After implementation |
| `run_smoke_test` | Quick validation test | Before committing |
| `check_types` | TypeScript type checking | After any TS changes |
| `project_issues` | Find project problems | Start of any task |
| `find_tests_for_file` | Find related tests | Before modifying code |
| `get_test_coverage` | Get coverage metrics | Before writing tests |
| `suggest_test_cases` | AI test suggestions | When adding tests |

### Scaffolding (3 tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `scaffold_project` | Generate project structure | Starting new project |
| `list_templates` | Show available templates | Choosing scaffold template |
| `plugin_status` | Check plugin health | Debugging plugin issues |

### LSP/Code Intelligence (18 tools)

**Navigation:**
| Tool | Purpose |
|------|---------|
| `find_references` | Find all symbol usages |
| `go_to_definition` | Jump to symbol definition |
| `get_implementations` | Find interface implementations |
| `get_call_hierarchy` | See call relationships |
| `get_document_symbols` | List symbols in file |
| `workspace_symbols` | Search symbols globally |

**Analysis:**
| Tool | Purpose |
|------|---------|
| `get_symbol_info` | Get symbol documentation |
| `get_signature_help` | Get function signatures |
| `get_diagnostics` | Get file diagnostics |
| `get_type_hierarchy` | See inheritance chain |
| `get_inlay_hints` | See inferred types |
| `get_api_surface` | Map public API |

**Refactoring:**
| Tool | Purpose |
|------|---------|
| `rename_symbol` | Safely rename symbols |
| `get_code_actions` | Get available fixes |
| `apply_code_action` | Apply a code fix |
| `find_dead_code` | Find unused code |
| `safe_delete_check` | Verify safe deletion |
| `validate_edits_preview` | Preview edit errors |

### Error Analysis & Security (5 tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `parse_error_stack` | Parse stack traces | Debugging errors |
| `explain_type_error` | Explain TS errors | Complex type errors |
| `scan_for_secrets` | Find exposed secrets | Before commits, in reviews |
| `get_env_config` | Get env configuration | Working with env vars |
| `check_permissions` | Check file permissions | Deployment issues |

### Code Analysis & Diff (3 tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `get_conventions` | Get project conventions | Before writing code |
| `detect_breaking_changes` | Find breaking changes | Before API changes |
| `semantic_diff` | Semantic code comparison | Reviewing changes |

### Framework-Specific (3 tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `get_react_component_tree` | Map React components | Frontend work |
| `get_prisma_operations` | Get Prisma operations | Database work |
| `analyze_bundle` | Analyze bundle size | Performance work |

### Runtime & Frontend Tools (15+ tools)

| Tool | Purpose |
|------|---------|
| `start_dev_server` | Start development server |
| `health_monitor` | Monitor server health |
| `watch_for_errors` | Watch for runtime errors |
| `browser_automation` | Automate browser actions |
| `verify_runtime_behavior` | Verify runtime behavior |
| `lighthouse_audit` | Run Lighthouse audit |
| `visual_regression` | Visual regression testing |
| `analyze_responsive_breakpoints` | Check responsive design |
| `trace_component_state` | Trace React state |
| `analyze_render_triggers` | Find render causes |
| `analyze_layout_hierarchy` | Analyze CSS layout |
| `diagnose_overflow` | Debug overflow issues |
| `get_accessibility_tree` | Get a11y tree |
| `get_sizing_strategy` | Analyze sizing |
| `analyze_event_flow` | Trace events |
| `analyze_tailwind_conflicts` | Find CSS conflicts |

### Advanced Operations (10+ tools)

| Tool | Purpose |
|------|---------|
| `retry_with_learning` | Retry with error learning |
| `resolve_merge_conflict` | Help resolve conflicts |
| `atomic_multi_edit` | Atomic multi-file edits |
| `auto_rollback` | Automatic rollback |
| `validate_api_contract` | Validate API contracts |
| `profile_function` | Profile performance |
| `log_analyzer` | Analyze logs |
| `generate_types` | Generate TypeScript types |
| `identify_tech_debt` | Find technical debt |

---

## Tool Invocation Patterns

### Pattern 1: Schema Check First (MANDATORY)

```bash
# WRONG - Never do this
mcp-cli call plugin_goodvibes_goodvibes-tools/detect_stack '{}'

# CORRECT - Always check schema first
mcp-cli info plugin_goodvibes_goodvibes-tools/detect_stack
# Read the schema output
mcp-cli call plugin_goodvibes_goodvibes-tools/detect_stack '{}'
```

### Pattern 2: Parallel Info Calls

When using multiple tools, check all schemas first:

```bash
# Check all schemas in parallel
mcp-cli info plugin_goodvibes_goodvibes-tools/detect_stack
mcp-cli info plugin_goodvibes_goodvibes-tools/scan_patterns
mcp-cli info plugin_goodvibes_goodvibes-tools/project_issues

# Then make calls
mcp-cli call plugin_goodvibes_goodvibes-tools/detect_stack '{}'
mcp-cli call plugin_goodvibes_goodvibes-tools/project_issues '{}'
```

### Pattern 3: Skill Loading Workflow

```bash
# 1. Find relevant skills
mcp-cli info plugin_goodvibes_goodvibes-tools/recommend_skills
mcp-cli call plugin_goodvibes_goodvibes-tools/recommend_skills '{"task": "implement authentication"}'

# 2. Load the recommended skill
mcp-cli info plugin_goodvibes_goodvibes-tools/get_skill_content
mcp-cli call plugin_goodvibes_goodvibes-tools/get_skill_content '{"skill_path": "webdev/authentication/clerk"}'
```

### Pattern 4: Pre-Edit Validation

```bash
# Before making edits, validate they won't cause errors
mcp-cli info plugin_goodvibes_goodvibes-tools/validate_edits_preview
mcp-cli call plugin_goodvibes_goodvibes-tools/validate_edits_preview '{"file": "src/auth.ts", "changes": "..."}'
```

### Pattern 5: Safe Deletion

```bash
# Before deleting any symbol, verify it's safe
mcp-cli info plugin_goodvibes_goodvibes-tools/safe_delete_check
mcp-cli call plugin_goodvibes_goodvibes-tools/safe_delete_check '{"symbol": "oldFunction", "file": "src/utils.ts"}'
```

---

## Agent-Specific Tool Recommendations

### Backend Engineer Priority Tools

1. `get_database_schema` - Always before DB work
2. `get_api_routes` - Understand existing API
3. `get_prisma_operations` - When using Prisma
4. `get_implementations` - Find service implementations
5. `validate_api_contract` - Before API changes

### Frontend Architect Priority Tools

1. `get_react_component_tree` - Understand component hierarchy
2. `analyze_bundle` - Check bundle impact
3. `analyze_tailwind_conflicts` - Find CSS issues
4. `get_accessibility_tree` - Check a11y
5. `analyze_responsive_breakpoints` - Verify responsive design

### Test Engineer Priority Tools

1. `find_tests_for_file` - Find existing tests
2. `get_test_coverage` - Understand coverage gaps
3. `suggest_test_cases` - Get test suggestions
4. `validate_edits_preview` - Verify test code compiles
5. `run_smoke_test` - Quick validation

### Code Architect Priority Tools

1. `find_circular_deps` - Detect dependency cycles
2. `find_dead_code` - Identify unused code
3. `get_api_surface` - Understand public APIs
4. `detect_breaking_changes` - Before refactoring
5. `get_type_hierarchy` - Understand class relationships

### DevOps Deployer Priority Tools

1. `analyze_bundle` - Check bundle size
2. `scan_for_secrets` - Find exposed credentials
3. `get_env_config` - Understand env setup
4. `check_permissions` - Verify file permissions
5. `run_smoke_test` - Pre-deployment validation

---

## Troubleshooting

### Tool Not Found

```bash
# List all available tools
mcp-cli tools

# Search for tools by keyword
mcp-cli grep "database"
```

### Schema Mismatch

```bash
# Always re-check schema if call fails
mcp-cli info plugin_goodvibes_goodvibes-tools/<tool>
```

### Tool Returns Error

1. Check schema matches your call
2. Verify required parameters
3. Check parameter types (strings vs objects)
4. Use stdin for complex JSON:

```bash
mcp-cli call plugin_goodvibes_goodvibes-tools/<tool> - <<'EOF'
{
  "complex": {
    "nested": "value"
  }
}
EOF
```

---

## Checklist: Am I Using Tools Correctly?

Before any task:
- [ ] Did I run `detect_stack`?
- [ ] Did I check `project_issues`?
- [ ] Did I search for relevant skills?

Before editing:
- [ ] Did I run `scan_patterns`?
- [ ] Did I check `find_tests_for_file`?
- [ ] Did I use `validate_edits_preview`?

After editing:
- [ ] Did I run `check_types`?
- [ ] Did I run `get_diagnostics`?

Before deletion:
- [ ] Did I run `safe_delete_check`?
- [ ] Did I verify with `find_references`?

**If you answered "no" to any of these, GO BACK AND USE THE TOOL.**
