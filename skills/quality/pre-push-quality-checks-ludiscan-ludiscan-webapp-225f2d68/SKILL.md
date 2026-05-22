---
name: pre-push-quality-checks
description: PR作成・git push前に必ず使用。bun install → fix → format → type → lint を順番に実行。
---

## When to Use This Skill

このスキルは以下の場合に**必ず**実行してください:

1. **PR作成前** - `gh pr create` を実行する前
2. **Git push前** - `git push` を実行する前
3. **コード変更後** - src/ 配下のファイルを変更した後
4. **ユーザーが明示的に品質チェックを要求した場合**

## When NOT to Use This Skill

以下の場合はこのスキルをスキップできます:

1. ドキュメントのみの変更 (README.md, CLAUDE.md等)
2. 設定ファイルのみの変更 (.gitignore, .envファイル等)
3. src/ 配下のコードが変更されていない場合

## Quality Check Process

### Step 0: Install Dependencies (MANDATORY)

**まず最初に、必ず依存関係をインストールしてください:**

```bash
bun install
```

**重要**: このステップをスキップすると、lintやtype checkが失敗する可能性があります。**必ず実行してください。**

### Step 1: Run Auto-Fix Commands

まず、自動修正可能な問題を修正します:

```bash
# 1. ESLintとStylelintの自動修正
bun run fix

# 2. Prettierでコード整形
bun run format
```

**重要**: これらのコマンドでファイルが変更された場合、変更をgit addする必要があります。

### Step 2: Run Type Check

TypeScript型チェックを実行します:

```bash
bun run type
```

**型エラーが1つでもある場合、PRやpushは禁止です。**

### Step 3: Final Lint Check

最終的なlintチェックを実行します:

```bash
bun run lint
```

**lintエラーが1つでもある場合、PRやpushは禁止です。**

## Complete Workflow

### For PR Creation

PR作成時は以下の順序で実行してください:

```markdown
0. `bun install` を実行 (MANDATORY - 最初に必ず実行)
1. コード変更を完了
2. `bun run fix` を実行 → ファイルが変更された場合は git add
3. `bun run format` を実行 → ファイルが変更された場合は git add
4. `bun run type` を実行 → エラーがある場合は修正して再度実行
5. `bun run lint` を実行 → エラーがある場合は修正して再度実行
6. すべてのチェックが通ったら git commit
7. git push
8. gh pr create
```

**エラーが発生した場合**:

- 型エラーの場合: エラーメッセージを読み、該当ファイルを修正
- lintエラーの場合: エラーメッセージを読み、該当ファイルを修正
- 自動修正で解決しない場合: 手動で修正

### For Git Push

git push前は以下の順序で実行してください:

```markdown
0. `bun install` を実行 (MANDATORY - 最初に必ず実行)
1. コード変更を完了
2. `bun run fix` を実行 → ファイルが変更された場合は git add
3. `bun run format` を実行 → ファイルが変更された場合は git add
4. `bun run type` を実行 → エラーがある場合は修正して再度実行
5. `bun run lint` を実行 → エラーがある場合は修正して再度実行
6. すべてのチェックが通ったら git commit
7. git push
```

## CRITICAL: All Errors Must Be Fixed

**🚨 絶対に守るべきルール 🚨**

検出された**すべてのエラー**を修正する必要があります。以下の言い訳は**一切認められません**:

❌ **禁止される言い訳**:
- ❌ 「このエラーは既存のもので、私の変更によるものではありません」
- ❌ 「このエラーは以前から存在していました」
- ❌ 「この型エラーは自分のコードとは関係ありません」
- ❌ 「このlintエラーは別の人が作ったコードです」

✅ **正しい対応**:
- ✅ 検出されたエラーが既存のものであっても、**全て修正する**
- ✅ エラーの原因が自分の変更かどうかに関わらず、**全て修正する**
- ✅ エラーが見つかった時点で、**その場で全て修正する**

**理由**:
- コード品質を維持するためには、既存のエラーも含めて全て修正する必要があります
- 「既存のエラー」という概念は品質チェックにおいては存在しません
- エラーが検出された時点で、それは修正すべき問題です

**重要**: このルールに違反した場合、PRやpushは**絶対に許可されません**。

## Error Handling

### Type Errors

型エラーが発生した場合:

```bash
# エラーメッセージ例:
src/component/atoms/Button.tsx(15,7): error TS2322: Type 'string' is not assignable to type 'number'.
```

**対処法**:
1. エラーメッセージから該当ファイルと行番号を特定
2. ファイルを開いて問題を確認
3. 型を修正
4. 再度 `bun run type` を実行して確認

**絶対にやってはいけないこと**:
- ❌ `any` 型を使用してエラーを隠す
- ❌ `@ts-ignore` コメントでエラーを無視する
- ❌ 型チェックをスキップする

### Lint Errors

lintエラーが発生した場合:

```bash
# エラーメッセージ例:
src/component/atoms/Button.tsx
  15:7  error  'handleClick' is assigned a value but never used  @typescript-eslint/no-unused-vars
```

**対処法**:
1. `bun run fix` で自動修正を試みる
2. 自動修正できない場合、エラーメッセージを読んで手動で修正
3. 再度 `bun run lint` を実行して確認

**よくあるlintエラーと対処法**:
- `no-unused-vars`: 未使用の変数を削除するか、使用する
- `@typescript-eslint/no-explicit-any`: `any` 型を適切な型に置き換える
- `react-hooks/exhaustive-deps`: useEffectの依存配列を修正

## Integration with Other Skills

このスキルは他のスキルと組み合わせて使用してください:

### With Implementation Planning Skill

実装計画の最終ステップとしてこのスキルを実行:

```markdown
## Implementation Steps

### 5. Final Quality Checks (最終ステップ)
**Status**: PENDING

**What to do**:
- Run `bun install` to ensure dependencies are installed (MANDATORY)
- Run `bun run fix` to auto-fix linting issues
- Run `bun run format` to format code
- Run `bun run type` to check TypeScript errors
- Run `bun run lint` to verify no linting errors
- Fix ALL errors found (既存のエラーも含めて全て修正)
- Commit any changes from auto-fix
- Ready for PR creation

**Completion criteria**:
- Dependencies installed successfully
- Type check passes (no errors - including existing errors)
- Lint check passes (no errors - including existing errors)
- All code properly formatted
- No excuses about "existing errors" - all errors must be fixed
```

## Example Execution

### Successful Case

```bash
# Step 0: Install dependencies (MANDATORY)
$ bun install
✓ Dependencies installed successfully

# Step 1: Auto-fix
$ bun run fix
✓ ESLint: Fixed 5 issues automatically
✓ Stylelint: Fixed 2 issues automatically

# ファイルが変更された場合
$ git add .

# Step 2: Format
$ bun run format
✓ Prettier: Formatted 10 files

# ファイルが変更された場合
$ git add .

# Step 3: Type check
$ bun run type
✓ No type errors found

# Step 4: Lint check
$ bun run lint
✓ ESLint: No errors found
✓ Stylelint: No errors found

# すべて成功 - PRやpush可能
✅ All quality checks passed! Ready to push/create PR.
```

### Error Case

```bash
# Step 0: Install dependencies (MANDATORY)
$ bun install
✓ Dependencies installed successfully

# Step 1: Auto-fix
$ bun run fix
✓ ESLint: Fixed 5 issues automatically

# Step 2: Format
$ bun run format
✓ Prettier: Formatted 10 files

# Step 3: Type check
$ bun run type
❌ Error: Type errors found

src/component/atoms/Button.tsx(15,7): error TS2322: Type 'string' is not assignable to type 'number'.

# ⚠️ 重要: このエラーが既存のものでも、必ず修正してください
# 「既存のエラー」という言い訳は認められません

# エラーを修正する
# ... ファイルを修正 ...

# 再度type checkを実行
$ bun run type
✓ No type errors found

# Step 4: Lint check
$ bun run lint
✓ ESLint: No errors found
✓ Stylelint: No errors found

# すべて成功
✅ All quality checks passed! Ready to push/create PR.
```

## Reporting to User

品質チェック完了後、ユーザーに結果を報告してください:

### Success Report

```markdown
✅ コード品質チェックが完了しました

**実行したチェック:**
- [x] bun install (dependencies)
- [x] ESLint & Stylelint auto-fix
- [x] Prettier format
- [x] TypeScript type check
- [x] Final lint check

**結果:**
- 型エラー: 0件
- Lintエラー: 0件
- フォーマット: 完了

PRの作成またはpushを実行できます。
```

### Error Report

```markdown
⚠️ コード品質チェックでエラーが見つかりました

**実行したチェック:**
- [x] bun install (dependencies)
- [x] ESLint & Stylelint auto-fix
- [x] Prettier format
- [ ] TypeScript type check (エラーあり)

**エラー詳細:**
```
src/component/atoms/Button.tsx(15,7): error TS2322: Type 'string' is not assignable to type 'number'.
```

⚠️ **重要**: このエラーが既存のものでも、必ず修正してください。
「既存のエラー」や「私の変更によるものではない」という言い訳は認められません。

エラーを修正してから、再度チェックを実行してください。
```

## Important Notes

1. **必ず`bun install`から開始** - 最初に依存関係をインストールしてください
2. **品質チェックは必須です** - スキップしないでください
3. **すべてのエラーを修正** - 既存のエラーも含めて、検出された全てのエラーを修正してください
4. **エラーがある場合、PRやpushは禁止** - すべてのエラーを修正してください
5. **自動修正を優先** - `bun run fix` と `bun run format` を先に実行
6. **型安全性を維持** - `any` 型や `@ts-ignore` でエラーを隠さない
7. **言い訳は禁止** - 「既存のエラー」や「私の変更ではない」という言い訳は認められません
8. **ユーザーに報告** - チェック結果を明確に伝える

## Automation Reminder

このスキルは以下のタイミングで**自動的に**実行されるべきです:

- ✅ ユーザーがPR作成を依頼したとき
- ✅ ユーザーがgit pushを依頼したとき
- ✅ 実装計画の最終ステップとして
- ✅ コード変更が完了したとき

**ユーザーが明示的に依頼しなくても、Claude Codeは自動的にこのスキルを実行してください。**

## Summary

このスキルにより以下が保証されます:

1. **依存関係の整合性** - `bun install`により常に最新の依存関係が利用可能
2. **コード品質の一貫性** - すべてのコードがlintとformatルールに従う
3. **型安全性** - TypeScriptエラーがない状態を維持
4. **スムーズなCI/CD** - ローカルでチェックするため、CIでのエラーを防ぐ
5. **効率的な開発** - 自動修正により手動修正の手間を削減
6. **完全なエラー修正** - 既存のエラーも含めて全て修正され、コードベース全体の品質が向上

**Remember**:
- **必ず`bun install`から開始してください**
- 品質チェックは面倒に見えますが、長期的にはバグを減らし、コードの保守性を高めます
- **「既存のエラー」という言い訳は絶対に認められません** - 検出されたエラーは全て修正してください
- 絶対にスキップしないでください
