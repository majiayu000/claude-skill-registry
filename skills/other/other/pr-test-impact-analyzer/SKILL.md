---
name: PR Test Impact Analyzer
description: Analyze pull request code changes to determine which tests are affected, recommend test execution order, and identify missing test coverage for modified code paths
version: 1.0.0
author: Pramod
license: MIT
tags: [test-impact, pr-analysis, change-detection, test-selection, affected-tests, code-change, test-optimization]
testingTypes: [code-quality, tdd]
frameworks: [jest, vitest]
languages: [typescript, javascript]
domains: [devops]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# PR Test Impact Analyzer Skill

You are an expert QA automation engineer specializing in test impact analysis for pull requests. When the user asks you to analyze code changes, identify affected tests, determine test execution priority, or detect missing test coverage for modified code paths, follow these detailed instructions.

## Core Principles

1. **Change awareness drives test selection** -- Every code change has a blast radius. Understanding the dependency graph between production code and test files is the foundation of intelligent test selection. Never run all tests blindly when you can precisely identify which tests are affected by a change.

2. **Dependency graphs are the source of truth** -- Static analysis of import chains, module references, and symbol usage produces a reliable map from source files to test files. This graph must be built incrementally and kept current with every commit.

3. **Risk scoring informs execution order** -- Not all changes carry equal risk. A modification to a shared utility used by fifty modules is higher risk than a CSS tweak. Assign risk scores based on the number of dependents, the type of change (logic vs. style), and the historical defect rate of the file.

4. **Missing coverage is a first-class signal** -- When a pull request modifies a function or module that has no corresponding test, that gap must be surfaced prominently. Silent gaps lead to regressions in production.

5. **Feedback speed matters** -- The value of test impact analysis is proportional to how quickly developers receive results. Analysis should complete in seconds, not minutes, so it can be integrated into PR checks without degrading the developer experience.

6. **Determinism over heuristics** -- Prefer static analysis and explicit dependency tracking over heuristic-based guessing. Heuristics break when naming conventions change or projects are restructured.

7. **Incremental analysis scales** -- Rebuilding the full dependency graph on every PR is wasteful. Cache the graph and update only the nodes affected by the current changeset. This keeps analysis time constant regardless of repository size.

8. **Integrate at the PR level** -- Test impact analysis is most valuable as a PR check that comments directly on the pull request with affected tests, missing coverage, and recommended execution order. Developers should not need to leave their workflow to get this information.

## Project Structure

Organize your PR test impact analysis tooling with this structure:

```
test-impact/
  src/
    analyzer/
      git-diff-parser.ts
      dependency-graph.ts
      test-mapper.ts
      risk-scorer.ts
      coverage-gap-detector.ts
    reporters/
      pr-comment-reporter.ts
      json-reporter.ts
      console-reporter.ts
    config/
      impact-config.ts
      path-mappings.ts
    cache/
      graph-cache.ts
      file-hash-cache.ts
    utils/
      file-resolver.ts
      pattern-matcher.ts
      ast-helpers.ts
  scripts/
    build-graph.ts
    analyze-pr.ts
    update-cache.ts
  __tests__/
    git-diff-parser.test.ts
    dependency-graph.test.ts
    test-mapper.test.ts
    risk-scorer.test.ts
    coverage-gap-detector.test.ts
  impact-config.json
  tsconfig.json
  package.json
```

## How It Works: Git Diff Analysis

The first step in test impact analysis is understanding exactly what changed in the pull request. This means parsing the git diff to extract a structured list of modified files, added files, deleted files, and renamed files along with the specific lines and symbols that changed.

### Parsing the Git Diff

The diff parser extracts structured change information from the git diff output, providing the foundation for all downstream analysis.

```typescript
import { execSync } from 'child_process';
import * as path from 'path';

export interface FileChange {
  filePath: string;
  changeType: 'added' | 'modified' | 'deleted' | 'renamed';
  oldPath?: string;
  additions: number;
  deletions: number;
  changedLines: LineChange[];
}

export interface LineChange {
  lineNumber: number;
  type: 'add' | 'delete';
  content: string;
}

export interface DiffResult {
  baseBranch: string;
  headBranch: string;
  files: FileChange[];
  totalAdditions: number;
  totalDeletions: number;
}

export function parsePRDiff(baseBranch: string = 'main'): DiffResult {
  const mergeBase = execSync(`git merge-base ${baseBranch} HEAD`)
    .toString()
    .trim();

  const diffNameStatus = execSync(
    `git diff --name-status ${mergeBase}...HEAD`
  )
    .toString()
    .trim();

  const files: FileChange[] = [];

  for (const line of diffNameStatus.split('\n')) {
    if (!line.trim()) continue;

    const parts = line.split('\t');
    const status = parts[0];
    let changeType: FileChange['changeType'];
    let filePath: string;
    let oldPath: string | undefined;

    if (status.startsWith('R')) {
      changeType = 'renamed';
      oldPath = parts[1];
      filePath = parts[2];
    } else if (status === 'A') {
      changeType = 'added';
      filePath = parts[1];
    } else if (status === 'D') {
      changeType = 'deleted';
      filePath = parts[1];
    } else {
      changeType = 'modified';
      filePath = parts[1];
    }

    const changedLines = getChangedLines(mergeBase, filePath, oldPath);
    const additions = changedLines.filter((l) => l.type === 'add').length;
    const deletions = changedLines.filter((l) => l.type === 'delete').length;

    files.push({
      filePath,
      changeType,
      oldPath,
      additions,
      deletions,
      changedLines,
    });
  }

  return {
    baseBranch,
    headBranch: execSync('git rev-parse --abbrev-ref HEAD').toString().trim(),
    files,
    totalAdditions: files.reduce((sum, f) => sum + f.additions, 0),
    totalDeletions: files.reduce((sum, f) => sum + f.deletions, 0),
  };
}

function getChangedLines(
  mergeBase: string,
  filePath: string,
  oldPath?: string
): LineChange[] {
  const target = oldPath ? `${oldPath} ${filePath}` : filePath;
  try {
    const diff = execSync(
      `git diff -U0 ${mergeBase}...HEAD -- ${target}`
    ).toString();

    const lines: LineChange[] = [];
    let currentLine = 0;

    for (const line of diff.split('\n')) {
      const hunkMatch = line.match(/^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@/);
      if (hunkMatch) {
        currentLine = parseInt(hunkMatch[1], 10);
        continue;
      }

      if (line.startsWith('+') && !line.startsWith('+++')) {
        lines.push({ lineNumber: currentLine, type: 'add', content: line.slice(1) });
        currentLine++;
      } else if (line.startsWith('-') && !line.startsWith('---')) {
        lines.push({ lineNumber: currentLine, type: 'delete', content: line.slice(1) });
      } else if (!line.startsWith('\\')) {
        currentLine++;
      }
    }

    return lines;
  } catch {
    return [];
  }
}
```

### Filtering Relevant Source Files

Not every changed file is relevant for test impact analysis. Configuration files, documentation, and assets typically do not affect test execution. Filter the diff results to focus on source code and test files.

```typescript
export interface ImpactConfig {
  sourcePatterns: string[];
  testPatterns: string[];
  ignorePatterns: string[];
  sourceRoot: string;
  testRoot: string;
}

const DEFAULT_CONFIG: ImpactConfig = {
  sourcePatterns: ['src/**/*.ts', 'src/**/*.tsx', 'lib/**/*.ts'],
  testPatterns: [
    '**/*.test.ts',
    '**/*.spec.ts',
    '**/*.test.tsx',
    '**/*.spec.tsx',
    '__tests__/**/*.ts',
  ],
  ignorePatterns: [
    '**/*.md',
    '**/*.json',
    '**/*.css',
    '**/*.svg',
    '**/node_modules/**',
    '**/dist/**',
  ],
  sourceRoot: 'src',
  testRoot: '__tests__',
};

export function filterRelevantFiles(
  diff: DiffResult,
  config: ImpactConfig = DEFAULT_CONFIG
): { sourceFiles: FileChange[]; testFiles: FileChange[]; otherFiles: FileChange[] } {
  const { minimatch } = require('minimatch');

  const sourceFiles: FileChange[] = [];
  const testFiles: FileChange[] = [];
  const otherFiles: FileChange[] = [];

  for (const file of diff.files) {
    if (config.ignorePatterns.some((p) => minimatch(file.filePath, p))) {
      otherFiles.push(file);
      continue;
    }

    if (config.testPatterns.some((p) => minimatch(file.filePath, p))) {
      testFiles.push(file);
    } else if (config.sourcePatterns.some((p) => minimatch(file.filePath, p))) {
      sourceFiles.push(file);
    } else {
      otherFiles.push(file);
    }
  }

  return { sourceFiles, testFiles, otherFiles };
}
```

## Building the Dependency Graph

The dependency graph maps every source file to the files that import it and every test file to the source files it exercises. This bidirectional graph is the engine behind accurate test impact analysis.

### Static Import Analysis

Parse TypeScript and JavaScript files to extract their import declarations and build a complete dependency map.

```typescript
import * as ts from 'typescript';
import * as path from 'path';
import * as fs from 'fs';

export interface DependencyNode {
  filePath: string;
  imports: string[];
  importedBy: string[];
  isTestFile: boolean;
  lastModified: number;
}

export interface DependencyGraph {
  nodes: Map<string, DependencyNode>;
  buildTimestamp: number;
}

export function buildDependencyGraph(
  rootDir: string,
  config: ImpactConfig
): DependencyGraph {
  const graph: DependencyGraph = {
    nodes: new Map(),
    buildTimestamp: Date.now(),
  };

  const allFiles = collectFiles(rootDir, [
    ...config.sourcePatterns,
    ...config.testPatterns,
  ]);

  for (const filePath of allFiles) {
    const absolutePath = path.resolve(rootDir, filePath);
    const imports = extractImports(absolutePath, rootDir);
    const isTestFile = config.testPatterns.some((p) =>
      require('minimatch')(filePath, p)
    );

    const stat = fs.statSync(absolutePath);

    graph.nodes.set(filePath, {
      filePath,
      imports,
      importedBy: [],
      isTestFile,
      lastModified: stat.mtimeMs,
    });
  }

  // Build reverse edges
  for (const [filePath, node] of graph.nodes) {
    for (const importPath of node.imports) {
      const target = graph.nodes.get(importPath);
      if (target) {
        target.importedBy.push(filePath);
      }
    }
  }

  return graph;
}

function extractImports(absolutePath: string, rootDir: string): string[] {
  const content = fs.readFileSync(absolutePath, 'utf-8');
  const sourceFile = ts.createSourceFile(
    absolutePath,
    content,
    ts.ScriptTarget.Latest,
    true
  );

  const imports: string[] = [];

  function visit(node: ts.Node): void {
    if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)) {
      const specifier = node.moduleSpecifier.text;
      const resolved = resolveImportPath(absolutePath, specifier, rootDir);
      if (resolved) {
        imports.push(resolved);
      }
    }

    if (
      ts.isCallExpression(node) &&
      node.expression.kind === ts.SyntaxKind.ImportKeyword &&
      node.arguments.length === 1 &&
      ts.isStringLiteral(node.arguments[0])
    ) {
      const specifier = (node.arguments[0] as ts.StringLiteral).text;
      const resolved = resolveImportPath(absolutePath, specifier, rootDir);
      if (resolved) {
        imports.push(resolved);
      }
    }

    ts.forEachChild(node, visit);
  }

  visit(sourceFile);
  return imports;
}

function resolveImportPath(
  fromFile: string,
  specifier: string,
  rootDir: string
): string | null {
  if (!specifier.startsWith('.') && !specifier.startsWith('/')) {
    return null; // Skip node_modules imports
  }

  const dir = path.dirname(fromFile);
  const extensions = ['.ts', '.tsx', '.js', '.jsx'];
  const basePath = path.resolve(dir, specifier);

  for (const ext of extensions) {
    const candidate = basePath + ext;
    if (fs.existsSync(candidate)) {
      return path.relative(rootDir, candidate);
    }
  }

  // Check for index files
  for (const ext of extensions) {
    const candidate = path.join(basePath, `index${ext}`);
    if (fs.existsSync(candidate)) {
      return path.relative(rootDir, candidate);
    }
  }

  return null;
}

function collectFiles(rootDir: string, patterns: string[]): string[] {
  const glob = require('fast-glob');
  return glob.sync(patterns, {
    cwd: rootDir,
    ignore: ['**/node_modules/**', '**/dist/**'],
  });
}
```

### Traversing the Graph for Affected Tests

Given a set of changed files, traverse the dependency graph to find all test files that directly or transitively depend on any of the changed files.

```typescript
export interface AffectedTestResult {
  testFile: string;
  reason: string;
  depth: number;
  dependencyChain: string[];
}

export function findAffectedTests(
  changedFiles: string[],
  graph: DependencyGraph
): AffectedTestResult[] {
  const affectedTests: Map<string, AffectedTestResult> = new Map();
  const visited = new Set<string>();

  function traverse(
    filePath: string,
    chain: string[],
    depth: number
  ): void {
    if (visited.has(filePath)) return;
    visited.add(filePath);

    const node = graph.nodes.get(filePath);
    if (!node) return;

    if (node.isTestFile && depth > 0) {
      const existing = affectedTests.get(filePath);
      if (!existing || existing.depth > depth) {
        affectedTests.set(filePath, {
          testFile: filePath,
          reason: `Depends on changed file: ${chain[0]}`,
          depth,
          dependencyChain: [...chain, filePath],
        });
      }
      return;
    }

    for (const dependent of node.importedBy) {
      traverse(dependent, [...chain, filePath], depth + 1);
    }
  }

  for (const changedFile of changedFiles) {
    traverse(changedFile, [], 0);
  }

  return Array.from(affectedTests.values()).sort((a, b) => a.depth - b.depth);
}
```

## Test File Mapping Heuristics

When the dependency graph does not cover all relationships (for example, when tests use dynamic imports or configuration-based test discovery), heuristic mapping fills the gaps.

```typescript
export interface TestMapping {
  sourceFile: string;
  testFiles: string[];
  mappingType: 'graph' | 'convention' | 'colocated' | 'directory';
  confidence: number;
}

export function mapSourceToTests(
  sourceFile: string,
  config: ImpactConfig
): TestMapping {
  const testFiles: string[] = [];
  const baseName = path.basename(sourceFile, path.extname(sourceFile));
  const dirName = path.dirname(sourceFile);

  // Convention: src/utils/parser.ts -> src/utils/parser.test.ts
  const colocatedTest = path.join(dirName, `${baseName}.test.ts`);
  if (fs.existsSync(colocatedTest)) {
    testFiles.push(colocatedTest);
  }

  const colocatedSpec = path.join(dirName, `${baseName}.spec.ts`);
  if (fs.existsSync(colocatedSpec)) {
    testFiles.push(colocatedSpec);
  }

  // Convention: src/utils/parser.ts -> __tests__/utils/parser.test.ts
  const relativePath = path.relative(config.sourceRoot, sourceFile);
  const mirroredTestPath = path.join(
    config.testRoot,
    path.dirname(relativePath),
    `${baseName}.test.ts`
  );
  if (fs.existsSync(mirroredTestPath)) {
    testFiles.push(mirroredTestPath);
  }

  // Convention: src/utils/parser.ts -> tests/utils/parser.test.ts
  const altTestPath = path.join(
    'tests',
    path.dirname(relativePath),
    `${baseName}.test.ts`
  );
  if (fs.existsSync(altTestPath)) {
    testFiles.push(altTestPath);
  }

  // Directory-based: find any test in the same directory
  const dirTests = fs
    .readdirSync(dirName)
    .filter((f) => f.endsWith('.test.ts') || f.endsWith('.spec.ts'))
    .map((f) => path.join(dirName, f));

  const uniqueTests = [...new Set([...testFiles, ...dirTests])];
  const confidence = testFiles.length > 0 ? 0.9 : dirTests.length > 0 ? 0.5 : 0.1;

  return {
    sourceFile,
    testFiles: uniqueTests,
    mappingType: testFiles.length > 0 ? 'convention' : 'directory',
    confidence,
  };
}
```

## Change Risk Scoring

Not all changes carry equal risk. A one-line fix in a leaf module is far less risky than a refactor of a shared utility. Risk scoring helps prioritize which tests to run first and which changes deserve the most scrutiny.

```typescript
export interface RiskScore {
  filePath: string;
  score: number; // 0-100
  factors: RiskFactor[];
}

export interface RiskFactor {
  name: string;
  weight: number;
  value: number;
  description: string;
}

export function calculateRiskScore(
  file: FileChange,
  graph: DependencyGraph
): RiskScore {
  const factors: RiskFactor[] = [];
  const node = graph.nodes.get(file.filePath);

  // Factor 1: Number of dependents (fan-out risk)
  const dependentCount = node?.importedBy.length ?? 0;
  factors.push({
    name: 'dependent_count',
    weight: 0.3,
    value: Math.min(dependentCount / 20, 1),
    description: `${dependentCount} files depend on this module`,
  });

  // Factor 2: Change size (larger changes are riskier)
  const totalChanges = file.additions + file.deletions;
  factors.push({
    name: 'change_size',
    weight: 0.2,
    value: Math.min(totalChanges / 100, 1),
    description: `${totalChanges} lines changed (${file.additions}+/${file.deletions}-)`,
  });

  // Factor 3: File type risk
  const isSharedModule =
    file.filePath.includes('/utils/') ||
    file.filePath.includes('/shared/') ||
    file.filePath.includes('/lib/') ||
    file.filePath.includes('/helpers/');
  factors.push({
    name: 'file_type',
    weight: 0.2,
    value: isSharedModule ? 0.9 : 0.3,
    description: isSharedModule
      ? 'Shared utility module (high risk)'
      : 'Regular module (standard risk)',
  });

  // Factor 4: Logic change detection
  const hasLogicChange = file.changedLines.some(
    (line) =>
      line.content.includes('if') ||
      line.content.includes('switch') ||
      line.content.includes('return') ||
      line.content.includes('throw') ||
      line.content.includes('catch') ||
      line.content.includes('await')
  );
  factors.push({
    name: 'logic_change',
    weight: 0.2,
    value: hasLogicChange ? 0.8 : 0.2,
    description: hasLogicChange
      ? 'Contains logic/control flow changes'
      : 'No significant logic changes detected',
  });

  // Factor 5: File is new (no existing test coverage)
  factors.push({
    name: 'new_file',
    weight: 0.1,
    value: file.changeType === 'added' ? 1.0 : 0.0,
    description:
      file.changeType === 'added'
        ? 'New file -- likely has no test coverage'
        : 'Existing file',
  });

  const score = Math.round(
    factors.reduce((sum, f) => sum + f.weight * f.value, 0) * 100
  );

  return { filePath: file.filePath, score, factors };
}
```

## Test Execution Priority

Once affected tests and risk scores are computed, produce a prioritized execution plan that runs the highest-risk, most-affected tests first.

```typescript
export interface TestExecutionPlan {
  priorityGroups: PriorityGroup[];
  totalTests: number;
  estimatedDuration: number;
}

export interface PriorityGroup {
  priority: 'critical' | 'high' | 'medium' | 'low';
  tests: PrioritizedTest[];
}

export interface PrioritizedTest {
  testFile: string;
  score: number;
  reasons: string[];
  estimatedDuration: number;
}

export function buildExecutionPlan(
  affectedTests: AffectedTestResult[],
  riskScores: Map<string, RiskScore>,
  timingData?: Map<string, number>
): TestExecutionPlan {
  const prioritizedTests: PrioritizedTest[] = affectedTests.map((test) => {
    const maxRisk = Math.max(
      ...test.dependencyChain
        .filter((f) => riskScores.has(f))
        .map((f) => riskScores.get(f)!.score),
      0
    );

    const depthPenalty = test.depth * 5;
    const score = Math.max(maxRisk - depthPenalty, 0);
    const estimatedDuration = timingData?.get(test.testFile) ?? 5000;

    return {
      testFile: test.testFile,
      score,
      reasons: [test.reason, `Dependency depth: ${test.depth}`],
      estimatedDuration,
    };
  });

  prioritizedTests.sort((a, b) => b.score - a.score);

  const groups: PriorityGroup[] = [
    { priority: 'critical', tests: prioritizedTests.filter((t) => t.score >= 75) },
    { priority: 'high', tests: prioritizedTests.filter((t) => t.score >= 50 && t.score < 75) },
    { priority: 'medium', tests: prioritizedTests.filter((t) => t.score >= 25 && t.score < 50) },
    { priority: 'low', tests: prioritizedTests.filter((t) => t.score < 25) },
  ];

  return {
    priorityGroups: groups.filter((g) => g.tests.length > 0),
    totalTests: prioritizedTests.length,
    estimatedDuration: prioritizedTests.reduce((sum, t) => sum + t.estimatedDuration, 0),
  };
}
```

## Missing Test Detection

One of the most valuable outputs of test impact analysis is identifying code that was changed but has no corresponding test coverage.

```typescript
export interface CoverageGap {
  sourceFile: string;
  changeType: FileChange['changeType'];
  additions: number;
  hasDirectTest: boolean;
  hasTransitiveTest: boolean;
  recommendation: string;
  severity: 'critical' | 'warning' | 'info';
}

export function detectCoverageGaps(
  sourceFiles: FileChange[],
  affectedTests: AffectedTestResult[],
  graph: DependencyGraph,
  config: ImpactConfig
): CoverageGap[] {
  const testedFiles = new Set(
    affectedTests.flatMap((t) => t.dependencyChain.filter((f) => !f.endsWith('.test.ts')))
  );

  const gaps: CoverageGap[] = [];

  for (const file of sourceFiles) {
    const hasDirectTest = affectedTests.some(
      (t) => t.dependencyChain.length === 2 && t.dependencyChain[0] === file.filePath
    );

    const hasTransitiveTest = testedFiles.has(file.filePath);

    if (!hasDirectTest && !hasTransitiveTest) {
      const severity =
        file.changeType === 'added'
          ? 'critical'
          : file.additions > 20
            ? 'warning'
            : 'info';

      gaps.push({
        sourceFile: file.filePath,
        changeType: file.changeType,
        additions: file.additions,
        hasDirectTest: false,
        hasTransitiveTest: false,
        recommendation: generateRecommendation(file, config),
        severity,
      });
    } else if (!hasDirectTest && hasTransitiveTest) {
      gaps.push({
        sourceFile: file.filePath,
        changeType: file.changeType,
        additions: file.additions,
        hasDirectTest: false,
        hasTransitiveTest: true,
        recommendation: `Consider adding direct unit tests for ${path.basename(file.filePath)}`,
        severity: 'info',
      });
    }
  }

  return gaps.sort((a, b) => {
    const severityOrder = { critical: 0, warning: 1, info: 2 };
    return severityOrder[a.severity] - severityOrder[b.severity];
  });
}

function generateRecommendation(file: FileChange, config: ImpactConfig): string {
  const baseName = path.basename(file.filePath, path.extname(file.filePath));
  const relativePath = path.relative(config.sourceRoot, file.filePath);
  const suggestedTestPath = path.join(
    config.testRoot,
    path.dirname(relativePath),
    `${baseName}.test.ts`
  );

  if (file.changeType === 'added') {
    return `New file has no tests. Create ${suggestedTestPath} to cover this module.`;
  }

  return `Modified file has no test coverage. Create ${suggestedTestPath} or add tests to an existing test file that imports this module.`;
}
```

## Integration with Jest --changedSince

Jest provides built-in support for running only tests related to changed files through the `--changedSince` flag. This can be combined with our more sophisticated analysis for a layered approach.

```typescript
import { execSync } from 'child_process';

export interface JestImpactOptions {
  baseBranch: string;
  jestConfig?: string;
  collectCoverage: boolean;
  verbose: boolean;
}

export function runJestChangedTests(options: JestImpactOptions): void {
  const { baseBranch, jestConfig, collectCoverage, verbose } = options;

  const args = [
    'npx jest',
    `--changedSince=${baseBranch}`,
    '--passWithNoTests',
    jestConfig ? `--config=${jestConfig}` : '',
    collectCoverage ? '--coverage --coverageReporters=json-summary' : '',
    verbose ? '--verbose' : '',
    '--forceExit',
  ]
    .filter(Boolean)
    .join(' ');

  console.log(`Running: ${args}`);

  try {
    execSync(args, { stdio: 'inherit', env: { ...process.env, CI: 'true' } });
  } catch (error) {
    process.exitCode = 1;
  }
}

export function runVitestRelated(changedFiles: string[]): void {
  if (changedFiles.length === 0) {
    console.log('No relevant files changed. Skipping tests.');
    return;
  }

  const fileArgs = changedFiles.join(' ');
  const command = `npx vitest related ${fileArgs} --run --reporter=verbose`;

  console.log(`Running: ${command}`);

  try {
    execSync(command, { stdio: 'inherit' });
  } catch (error) {
    process.exitCode = 1;
  }
}
```

## GitHub PR Integration

Generate structured comments for pull requests that summarize the test impact analysis, making it easy for reviewers to understand the testing implications of a change.

```typescript
export interface PRCommentData {
  summary: string;
  affectedTestCount: number;
  coverageGaps: CoverageGap[];
  executionPlan: TestExecutionPlan;
  riskScores: RiskScore[];
}

export function generatePRComment(data: PRCommentData): string {
  const lines: string[] = [];

  lines.push('## Test Impact Analysis');
  lines.push('');

  // Summary section
  const gapCount = data.coverageGaps.filter((g) => g.severity === 'critical').length;
  const statusIcon = gapCount > 0 ? 'WARNING' : 'PASS';
  lines.push(`**Status:** ${statusIcon} | **Affected Tests:** ${data.affectedTestCount} | **Coverage Gaps:** ${gapCount}`);
  lines.push('');

  // Risk scores
  const highRisk = data.riskScores.filter((r) => r.score >= 50);
  if (highRisk.length > 0) {
    lines.push('### High Risk Changes');
    lines.push('| File | Risk Score | Reason |');
    lines.push('|------|-----------|--------|');
    for (const risk of highRisk) {
      const topFactor = risk.factors.sort((a, b) => b.value * b.weight - a.value * a.weight)[0];
      lines.push(`| \`${risk.filePath}\` | ${risk.score}/100 | ${topFactor.description} |`);
    }
    lines.push('');
  }

  // Coverage gaps
  const criticalGaps = data.coverageGaps.filter((g) => g.severity === 'critical');
  if (criticalGaps.length > 0) {
    lines.push('### Missing Test Coverage');
    for (const gap of criticalGaps) {
      lines.push(`- **${gap.sourceFile}** -- ${gap.recommendation}`);
    }
    lines.push('');
  }

  // Execution plan
  lines.push('### Recommended Test Execution Order');
  for (const group of data.executionPlan.priorityGroups) {
    lines.push(`**${group.priority.toUpperCase()}** (${group.tests.length} tests)`);
    for (const test of group.tests.slice(0, 10)) {
      lines.push(`- \`${test.testFile}\` (score: ${test.score})`);
    }
    if (group.tests.length > 10) {
      lines.push(`- ... and ${group.tests.length - 10} more`);
    }
    lines.push('');
  }

  // Selective execution command
  const criticalTests = data.executionPlan.priorityGroups
    .filter((g) => g.priority === 'critical' || g.priority === 'high')
    .flatMap((g) => g.tests.map((t) => t.testFile));

  if (criticalTests.length > 0) {
    lines.push('### Quick Run Command');
    lines.push('```bash');
    lines.push(`npx jest ${criticalTests.slice(0, 20).join(' ')}`);
    lines.push('```');
  }

  return lines.join('\n');
}
```

## Selective Test Execution in CI

Integrate test impact analysis into your CI pipeline to run only the affected tests, dramatically reducing pipeline duration while maintaining confidence.

```yaml
# .github/workflows/test-impact.yml
name: Test Impact Analysis
on:
  pull_request:
    branches: [main]

jobs:
  analyze-impact:
    runs-on: ubuntu-latest
    outputs:
      affected-tests: ${{ steps.impact.outputs.tests }}
      has-gaps: ${{ steps.impact.outputs.has-gaps }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: npm ci

      - name: Run Impact Analysis
        id: impact
        run: |
          node scripts/analyze-pr.js --base=origin/main --format=json > impact-result.json
          TESTS=$(jq -r '.affectedTests[].testFile' impact-result.json | tr '\n' ' ')
          GAPS=$(jq '.coverageGaps | length' impact-result.json)
          echo "tests=$TESTS" >> $GITHUB_OUTPUT
          echo "has-gaps=$([[ $GAPS -gt 0 ]] && echo true || echo false)" >> $GITHUB_OUTPUT

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const impact = JSON.parse(fs.readFileSync('impact-result.json', 'utf-8'));
            const body = generatePRComment(impact);
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body
            });

  run-affected-tests:
    needs: analyze-impact
    if: needs.analyze-impact.outputs.affected-tests != ''
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - name: Run Affected Tests
        run: npx jest ${{ needs.analyze-impact.outputs.affected-tests }} --ci --coverage
```

## Configuration

Create an `impact-config.json` file at the project root to customize the analyzer:

```json
{
  "sourceRoot": "src",
  "testRoot": "__tests__",
  "sourcePatterns": ["src/**/*.ts", "src/**/*.tsx"],
  "testPatterns": ["**/*.test.ts", "**/*.spec.ts", "**/__tests__/**/*.ts"],
  "ignorePatterns": [
    "**/*.d.ts",
    "**/*.css",
    "**/*.json",
    "**/node_modules/**",
    "**/dist/**",
    "**/coverage/**"
  ],
  "riskThresholds": {
    "critical": 75,
    "high": 50,
    "medium": 25
  },
  "maxDependencyDepth": 10,
  "enableTimingData": true,
  "timingDataPath": ".test-timing.json",
  "cacheEnabled": true,
  "cachePath": ".impact-cache",
  "ciProvider": "github-actions",
  "commentOnPR": true,
  "failOnCriticalGaps": false,
  "customMappings": {
    "src/config/": ["__tests__/integration/config.test.ts"],
    "src/db/migrations/": ["__tests__/integration/database.test.ts"]
  }
}
```

## Test Timing Data Collection

Collecting test execution timing data enables more accurate estimated durations and smarter test splitting in CI.

```typescript
import * as fs from 'fs';

export interface TestTimingEntry {
  testFile: string;
  duration: number;
  lastRun: number;
  runCount: number;
  averageDuration: number;
}

export class TimingCollector {
  private timingPath: string;
  private data: Map<string, TestTimingEntry>;

  constructor(timingPath: string = '.test-timing.json') {
    this.timingPath = timingPath;
    this.data = this.loadTimings();
  }

  private loadTimings(): Map<string, TestTimingEntry> {
    try {
      const raw = fs.readFileSync(this.timingPath, 'utf-8');
      const entries: TestTimingEntry[] = JSON.parse(raw);
      return new Map(entries.map((e) => [e.testFile, e]));
    } catch {
      return new Map();
    }
  }

  recordTiming(testFile: string, duration: number): void {
    const existing = this.data.get(testFile);
    if (existing) {
      existing.runCount++;
      existing.averageDuration =
        (existing.averageDuration * (existing.runCount - 1) + duration) /
        existing.runCount;
      existing.duration = duration;
      existing.lastRun = Date.now();
    } else {
      this.data.set(testFile, {
        testFile,
        duration,
        lastRun: Date.now(),
        runCount: 1,
        averageDuration: duration,
      });
    }
  }

  save(): void {
    const entries = Array.from(this.data.values());
    fs.writeFileSync(this.timingPath, JSON.stringify(entries, null, 2));
  }

  getEstimatedDuration(testFile: string): number {
    return this.data.get(testFile)?.averageDuration ?? 5000;
  }
}
```

## Best Practices

1. **Build the dependency graph in CI and cache it** -- Do not rebuild the full graph on every PR. Cache the serialized graph as a CI artifact and update only the changed nodes. This keeps analysis time under two seconds for repositories with thousands of files.

2. **Combine static analysis with test timing data** -- Static analysis tells you which tests are affected. Timing data tells you how long they take. Together, they enable intelligent test splitting that keeps every CI runner busy for roughly the same duration.

3. **Treat coverage gaps as PR review items** -- Surface missing coverage in the PR comment, not as a blocking gate initially. Let the team build the habit of reviewing test impact before making it a hard requirement.

4. **Maintain custom mappings for non-obvious dependencies** -- Some relationships cannot be discovered through import analysis. Database migration files affect integration tests. Configuration changes affect everything. Maintain a custom mapping file for these cases.

5. **Track risk scores over time** -- Store historical risk scores to identify modules that are frequently changed and frequently break. These are candidates for refactoring or increased test coverage investment.

6. **Use fail-fast ordering for critical tests** -- Run the highest-risk tests first so that failures surface early. A ten-minute test suite that fails in the first thirty seconds is far better than one that fails at minute nine.

7. **Validate the graph against actual test runs** -- Periodically run the full test suite and compare the pass/fail results with what impact analysis would have selected. Any test that fails but was not in the affected set indicates a gap in the dependency graph.

8. **Handle dynamic imports and barrel files explicitly** -- Barrel files (index.ts re-exports) can create false positives by making the graph think every consumer depends on every module in the barrel. Consider resolving through barrels to the actual target file.

9. **Account for configuration file changes** -- Changes to tsconfig.json, jest.config.ts, or .env files potentially affect all tests. Treat configuration changes as high-risk triggers for broader test execution.

10. **Version your dependency graph schema** -- As the analysis tool evolves, the graph format may change. Include a version number in the cached graph to avoid deserialization errors when the schema is updated.

11. **Separate unit and integration test impact** -- Unit tests typically have a clear one-to-one mapping with source files. Integration tests have many-to-many mappings. Treat them differently in the analysis to avoid over-selecting or under-selecting.

12. **Provide a manual override mechanism** -- Sometimes developers know that a change requires running a specific set of tests not captured by the graph. Provide a PR label or comment command like `/run-tests path/to/specific.test.ts` for manual overrides.

## Anti-Patterns to Avoid

1. **Running all tests on every PR** -- This is the opposite of test impact analysis. It wastes CI resources, increases wait times, and provides no prioritization information. Even if you run all tests as a safety net, the impact-selected tests should run first and report first.

2. **Relying solely on file naming conventions** -- Assuming that `src/foo.ts` is tested by `src/foo.test.ts` misses transitive dependencies entirely. A change to a shared utility affects dozens of tests that have no naming relationship with the changed file.

3. **Ignoring deleted and renamed files** -- When a file is deleted or renamed, all tests that imported it are now broken. The impact analyzer must handle these cases or it will miss failing tests that should have been flagged.

4. **Caching the graph indefinitely without invalidation** -- The dependency graph must be refreshed when the merge base changes or when enough commits have accumulated. Stale graphs produce inaccurate results that erode developer trust in the tool.

5. **Treating all changes as equal risk** -- A typo fix in a comment and a rewrite of business logic have vastly different risk profiles. Without risk scoring, the analyzer provides a flat list that does not help developers focus their review.

6. **Blocking PRs on missing test coverage for trivial changes** -- Requiring test coverage for every single-line change creates friction that developers will work around by adding meaningless tests. Reserve blocking gates for critical gaps only.

7. **Ignoring test-to-test dependencies** -- Test utilities, fixtures, and shared helpers create dependencies between test files. A change to a test helper can affect hundreds of tests. Include test infrastructure in the dependency graph.

## Debugging Tips

**The analyzer reports no affected tests for a clearly impactful change.** Check whether the dependency graph is up to date. Run the graph builder manually and inspect the node for the changed file. Verify that the import paths are resolved correctly, especially for path aliases configured in tsconfig.json. Path aliases like `@/utils/foo` need to be resolved to their actual file paths during graph construction.

**Too many tests are flagged as affected.** This usually indicates a barrel file or widely-imported utility is in the dependency chain. Inspect the dependency chain for each affected test and look for hub nodes with many dependents. Consider adding more granular imports to reduce the blast radius.

**Risk scores do not match intuition.** Review the individual risk factors for the file in question. The scoring weights may need tuning for your specific codebase. For example, if your project has a flat structure with no shared utilities, the file type factor carries less significance and should be weighted down.

**CI pipeline runs the wrong tests after a merge conflict.** When the merge base changes due to rebasing or merging, the diff calculation changes. Ensure the CI pipeline uses `git merge-base` to compute the correct diff target rather than hardcoding a branch name that may have moved.

**Custom mappings are ignored.** Verify that the paths in the custom mappings configuration match the format used by the dependency graph (relative paths from the repository root, forward slashes, no leading dot-slash). Log the resolved paths during analysis to confirm they match.

**Test timing data is stale.** If your tests have been refactored but the timing data was not updated, the execution plan will have inaccurate duration estimates. Delete the timing data file and let it rebuild over the next few CI runs. Alternatively, set an expiration period on timing entries so that old data ages out automatically.

**Graph construction is slow on a large monorepo.** Profile the import extraction step. If the TypeScript AST parsing is the bottleneck, consider using a faster parser like SWC or esbuild for import extraction. These tools can parse thousands of files per second while the full TypeScript compiler may take minutes on a large codebase.

**The PR comment is not posted.** Verify that the GitHub token used in CI has write permissions for pull requests. The `GITHUB_TOKEN` provided by GitHub Actions has `pull-requests: write` by default for workflows triggered by `pull_request`, but forked PRs have read-only tokens. Check the workflow permissions and consider using a personal access token or GitHub App token for fork-based workflows.
