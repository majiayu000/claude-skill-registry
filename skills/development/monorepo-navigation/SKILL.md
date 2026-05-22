---
name: monorepo-navigation
description: Monorepo navigation utilities for finding packages by type, locating workspace roots, and resolving cross-package dependencies. Provides findPackagesByType, locateWorkspaceRoot, resolveWorkspaceDependencies, and getPackagesBuildOrder functions for Turborepo and pnpm workspace navigation. Use when navigating monorepo structures, analyzing dependency graphs, or performing workspace-aware operations.
---

# Monorepo Navigation Skill

## Purpose

Provides utilities to navigate monorepo structures, find packages by type, locate workspace roots, and resolve workspace dependencies.

## Input Parameters

```typescript
interface NavigationOptions {
  workspaceRoot: string; // Absolute path to monorepo root
  packageType?: "apps" | "packages" | "services" | "all";
  includePrivate?: boolean; // Include private packages (default: true)
  depth?: number; // Search depth (default: 2)
}
```

## Output Format

```typescript
interface WorkspaceInfo {
  workspaces: WorkspacePackage[];
  byType: {
    apps: WorkspacePackage[];
    packages: WorkspacePackage[];
    services: WorkspacePackage[];
  };
  dependencies: DependencyGraph;
}

interface WorkspacePackage {
  name: string; // Package name from package.json
  path: string; // Absolute path to package
  relativePath: string; // Relative to workspace root
  type: "app" | "package" | "service";
  private: boolean;
  dependencies: string[]; // Workspace dependencies
  packageJson: any;
}

interface DependencyGraph {
  [packageName: string]: {
    dependencies: string[];
    dependents: string[];
  };
}
```

## Core Functions

### 1. Find Packages by Type

```bash
#!/bin/bash
# find-packages.sh

find_packages_by_type() {
  local workspace_root="$1"
  local package_type="$2"  # apps, packages, services, or all

  cd "$workspace_root" || exit 1

  local search_dirs=()

  case "$package_type" in
    apps)
      search_dirs=("apps")
      ;;
    packages)
      search_dirs=("packages")
      ;;
    services)
      search_dirs=("services")
      ;;
    all)
      search_dirs=("apps" "packages" "services")
      ;;
  esac

  local results=()

  for dir in "${search_dirs[@]}"; do
    if [ -d "$dir" ]; then
      # Find all package.json files
      while IFS= read -r pkg_file; do
        pkg_dir=$(dirname "$pkg_file")
        results+=("$pkg_dir")
      done < <(find "$dir" -name "package.json" -maxdepth 3)
    fi
  done

  printf '%s\n' "${results[@]}"
}
```

### 2. Locate Workspace Root

```bash
#!/bin/bash
# locate-workspace-root.sh

locate_workspace_root() {
  local current_dir="$1"

  while [ "$current_dir" != "/" ]; do
    # Check for monorepo indicators
    if [ -f "$current_dir/turbo.json" ] || \
       [ -f "$current_dir/pnpm-workspace.yaml" ] || \
       [ -f "$current_dir/nx.json" ]; then
      echo "$current_dir"
      return 0
    fi

    # Check for package.json with workspaces
    if [ -f "$current_dir/package.json" ]; then
      if grep -q '"workspaces"' "$current_dir/package.json"; then
        echo "$current_dir"
        return 0
      fi
    fi

    current_dir=$(dirname "$current_dir")
  done

  return 1
}
```

### 3. Resolve Workspace Dependencies

```typescript
function resolveWorkspaceDependencies(workspaceRoot: string): DependencyGraph {
  const graph: DependencyGraph = {};
  const packages = findAllPackages(workspaceRoot);

  // Build dependency graph
  for (const pkg of packages) {
    graph[pkg.name] = {
      dependencies: [],
      dependents: [],
    };

    // Parse dependencies from package.json
    const deps = Object.keys(pkg.packageJson.dependencies || {});
    const devDeps = Object.keys(pkg.packageJson.devDependencies || {});

    // Filter workspace dependencies (workspace:* protocol or @metasaver/*)
    const workspaceDeps = [...deps, ...devDeps].filter(
      (dep) =>
        dep.startsWith("@metasaver/") ||
        pkg.packageJson.dependencies?.[dep]?.startsWith("workspace:")
    );

    graph[pkg.name].dependencies = workspaceDeps;
  }

  // Build reverse dependencies (dependents)
  for (const [pkgName, data] of Object.entries(graph)) {
    for (const dep of data.dependencies) {
      if (graph[dep]) {
        graph[dep].dependents.push(pkgName);
      }
    }
  }

  return graph;
}
```

## Usage Examples

### Example 1: Find All Apps

```typescript
import { findPackagesByType } from ".claude/skills/monorepo-navigation.skill";

const apps = await findPackagesByType({
  workspaceRoot: "/mnt/f/code/resume-builder",
  packageType: "apps",
});

console.log(
  "Found apps:",
  apps.map((a) => a.name)
);
// Output: ['@metasaver/resume-portal']
```

### Example 2: Navigate from Package to Root

```typescript
import { locateWorkspaceRoot } from ".claude/skills/monorepo-navigation.skill";

const currentPackage = "/mnt/f/code/resume-builder/services/data/resume-api";
const root = await locateWorkspaceRoot(currentPackage);

console.log("Workspace root:", root);
// Output: '/mnt/f/code/resume-builder'
```

### Example 3: Build Dependency Graph

```typescript
import { resolveWorkspaceDependencies } from ".claude/skills/monorepo-navigation.skill";

const graph = await resolveWorkspaceDependencies("/mnt/f/code/resume-builder");

// Find all packages that depend on contracts
const contractConsumers =
  graph["@metasaver/resume-builder-contracts"].dependents;
console.log("Packages using contracts:", contractConsumers);
// Output: ['@metasaver/resume-api', '@metasaver/resume-portal']
```

### Example 4: Find Package by Name

```typescript
import { findPackageByName } from ".claude/skills/monorepo-navigation.skill";

const pkg = await findPackageByName({
  workspaceRoot: "/mnt/f/code/resume-builder",
  packageName: "@metasaver/resume-builder-contracts",
});

console.log("Package location:", pkg.path);
// Output: '/mnt/f/code/resume-builder/packages/contracts/resume-builder-contracts'
```

## Implementation Helpers

```typescript
// monorepo-navigation.ts

export interface MonorepoNavigator {
  findPackagesByType(options: NavigationOptions): Promise<WorkspacePackage[]>;
  locateWorkspaceRoot(startPath: string): Promise<string | null>;
  resolveWorkspaceDependencies(root: string): Promise<DependencyGraph>;
  findPackageByName(
    root: string,
    name: string
  ): Promise<WorkspacePackage | null>;
  getPackagesBuildOrder(root: string): Promise<string[]>; // Topological sort
}

// Example: Get build order
export async function getPackagesBuildOrder(
  workspaceRoot: string
): Promise<string[]> {
  const graph = await resolveWorkspaceDependencies(workspaceRoot);
  const sorted: string[] = [];
  const visited = new Set<string>();

  function visit(pkgName: string) {
    if (visited.has(pkgName)) return;
    visited.add(pkgName);

    // Visit dependencies first
    for (const dep of graph[pkgName]?.dependencies || []) {
      visit(dep);
    }

    sorted.push(pkgName);
  }

  // Visit all packages
  for (const pkgName of Object.keys(graph)) {
    visit(pkgName);
  }

  return sorted;
}
```

## Common Patterns

### Pattern 1: Workspace-Aware Operations

```typescript
async function performWorkspaceOperation(packagePath: string) {
  // Always find workspace root first
  const root = await locateWorkspaceRoot(packagePath);

  // Then find all affected packages
  const packages = await findPackagesByType({
    workspaceRoot: root,
    packageType: "all",
  });

  // Perform operation on each package
  for (const pkg of packages) {
    await processPackage(pkg);
  }
}
```

### Pattern 2: Dependency-Aware Updates

```typescript
async function updatePackageWithDependencies(
  packageName: string,
  root: string
) {
  const graph = await resolveWorkspaceDependencies(root);
  const dependencies = graph[packageName].dependencies;

  // Update dependencies first
  for (const dep of dependencies) {
    await updatePackage(dep);
  }

  // Then update target package
  await updatePackage(packageName);
}
```

## Used By

- Project manager agent
- Domain agents (frontend, backend, testing)
- Config agents (when applying to multiple packages)
- Build orchestration
- Dependency management
