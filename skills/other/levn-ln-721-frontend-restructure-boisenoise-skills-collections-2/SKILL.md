---
name: ln-721-frontend-restructure
description: "Frontend structure worker: SCAFFOLD new React project or RESTRUCTURE existing monolith to component-based architecture"
---

# ln-721-frontend-restructure

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-720-structure-migrator

Frontend structure worker with two modes: SCAFFOLD (generate minimal React project from template) or RESTRUCTURE (migrate monolith to component-based architecture).

---

## Mode Selection

| Mode | When | Input | Output |
|------|------|-------|--------|
| **SCAFFOLD** | CREATE pipeline — no existing frontend | Target stack config from ln-720 | Minimal React + Vite project (~7 files) |
| **RESTRUCTURE** | TRANSFORM pipeline — existing frontend found | Monolithic React source | Component-based architecture |

---

## Purpose & Scope

| Aspect | Description |
|--------|-------------|
| **Input** | Target stack config (SCAFFOLD) or monolithic React source (RESTRUCTURE) |
| **Output** | Minimal project (SCAFFOLD) or component-based architecture (RESTRUCTURE) |
| **Framework** | React + TypeScript + Vite |

**Scope boundaries:**
- SCAFFOLD: generates minimal starter files, no business logic
- RESTRUCTURE: restructures existing code, does not add new functionality
- Works with React + TypeScript projects
- Applies transformation rules from reference files

---

## Workflow

### SCAFFOLD Mode (CREATE pipeline)

| Phase | Name | Actions | Output |
|-------|------|---------|--------|
| S1 | Generate | Create minimal React + Vite + TypeScript project files | ~7 starter files |
| S2 | Verify | Check file structure, validate configs | Valid project skeleton |

### RESTRUCTURE Mode (TRANSFORM pipeline)

| Phase | Name | Actions | Output |
|-------|------|---------|--------|
| 1 | Analyze | Scan source, detect component types, measure complexity | File inventory, complexity metrics |
| 2 | Plan | Apply split thresholds, calculate file moves, detect conflicts | Migration plan |
| 3 | Execute | Create folders, extract content, update imports | Restructured files |
| 4 | Verify | Run build, check imports, validate structure | Build success report |

---

## SCAFFOLD Mode Phases

### Phase S1: Generate Starter Files

Create minimal React + Vite + TypeScript project.

| File | Purpose |
|------|---------|
| `package.json` | Dependencies: react, react-dom, typescript, vite, @vitejs/plugin-react |
| `vite.config.ts` | Vite config with React plugin, port, proxy settings |
| `tsconfig.json` | Strict TypeScript config with path aliases |
| `index.html` | Entry HTML with root div |
| `src/main.tsx` | React entry point with StrictMode |
| `src/App.tsx` | Root App component with router placeholder |
| `src/index.css` | Base styles (reset, variables, layout) |

### Phase S2: Verify Scaffold

| Check | Method | Expected |
|-------|--------|----------|
| All files created | File existence check | 7 files present |
| package.json valid | JSON parse | No syntax errors |
| tsconfig.json valid | JSON parse | No syntax errors |
| No hardcoded values | Content scan | Project name from config, not hardcoded |

---

## RESTRUCTURE Mode Phases

### Phase 1: Analyze

Scan current frontend structure and classify components.

| Step | Action | Reference |
|------|--------|-----------|
| 1.1 | Scan all `.tsx` and `.ts` files in source | — |
| 1.2 | Measure file complexity (lines, hooks, types) | `transformation_rules.md` |
| 1.3 | Classify components by category | `component_patterns.md` |
| 1.4 | Build import dependency graph | `import_strategy.md` |

**Output:** Component inventory with classifications and metrics.

---

### Phase 2: Plan

Generate migration plan based on analysis.

| Step | Action | Reference |
|------|--------|-----------|
| 2.1 | Apply split thresholds to identify files to restructure | `transformation_rules.md` |
| 2.2 | Calculate target paths for each file | `react_folder_structure.md` |
| 2.3 | Identify import updates needed | `import_strategy.md` |
| 2.4 | Detect potential conflicts (name collisions, circular deps) | — |

**Output:** Migration plan with Before/After mapping.

---

### Phase 3: Execute

Apply transformations in correct order.

| Step | Action | Notes |
|------|--------|-------|
| 3.1 | Create directory structure | All target folders |
| 3.2 | Extract types to `types.ts` | Types have no dependencies |
| 3.3 | Extract constants to `constants.ts` | Constants depend only on types |
| 3.4 | Extract hooks to `hooks.ts` | Hooks depend on types, constants |
| 3.5 | Extract sub-components | Components use all above |
| 3.6 | Create barrel exports (`index.ts`) | For clean imports |
| 3.7 | Update all import paths | Fix references |

**Order is critical:** Execute in sequence to avoid broken imports.

---

### Phase 4: Verify

Validate restructured project.

| Check | Command | Expected |
|-------|---------|----------|
| TypeScript compilation | `npx tsc --noEmit` | No errors |
| Build | `npm run build` | Success |
| No orphan files | Manual check | Source location empty |
| Imports resolve | Build success | No module not found errors |

---

## Transformation Summary

| Transformation | Before State | After State |
|----------------|--------------|-------------|
| Component Split | Single file >300 lines | Feature folder with co-located files |
| Type Extraction | Inline interfaces | Separate `types.ts` |
| Constant Extraction | Inline magic values | Separate `constants.ts` |
| Hook Extraction | Inline useState/useEffect | Separate `hooks.ts` or shared hooks |
| UI Component Move | Scattered in features | Centralized in `components/ui/` |
| Layout Component Move | Mixed with features | Centralized in `components/layout/` |

---

## Critical Rules

- **Mode Awareness:** SCAFFOLD creates from template; RESTRUCTURE transforms existing — never mix
- **Single Responsibility:** Handle only frontend structure, no backend changes
- **Idempotent:** Can re-run without duplicate files or corruption
- **Build Verification:** Must verify build passes after changes (RESTRUCTURE: `npm run build`)
- **Preserve Functionality:** No behavioral changes, only structural (RESTRUCTURE mode)
- **Backup Strategy:** Do not delete source files until verification passes (RESTRUCTURE mode)
- **Import Consistency:** Use path aliases for shared, relative for co-located

---

## Definition of Done

**SCAFFOLD mode:**
- [ ] All 7 starter files generated
- [ ] package.json and tsconfig.json valid
- [ ] No hardcoded project names (uses config values)

**RESTRUCTURE mode:**
- [ ] All source files analyzed and classified
- [ ] Migration plan generated with Before/After mapping
- [ ] Directory structure created per template
- [ ] All extractions completed (types, constants, hooks, components)
- [ ] Import paths updated throughout project
- [ ] `npm run build` passes successfully
- [ ] No orphan imports or missing files
- [ ] Barrel exports created for shared folders

---

## Risk Mitigation

| Risk | Detection | Mitigation |
|------|-----------|------------|
| Build failure after restructure | `npm run build` fails | Rollback: restore from source, investigate specific error |
| Missing imports | Module not found errors | Scan all imports before/after, update missed paths |
| Circular dependencies | Build warning or runtime error | Analyze dependency graph, break cycles by extracting shared code |
| Lost functionality | Tests fail or UI broken | Run existing tests before/after transformation |
| Name collisions | Duplicate export names | Rename with feature prefix before moving |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/transformation_rules.md` | Split thresholds, extraction rules, transformation order |
| `references/component_patterns.md` | Component classification by category |
| `references/import_strategy.md` | Import update rules, path aliases, barrel exports |
| `references/react_folder_structure.md` | Target directory structure template |

---

**Version:** 3.0.0
**Last Updated:** 2026-02-07
