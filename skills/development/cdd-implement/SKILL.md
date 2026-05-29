---
name: cdd-implement
description: DECIDED決断を実装（Selection確定が前提）
allowed-tools: Read, Edit, Write, Bash(cdd:*, git:*, gh:*), Glob, Grep
---

# CDD Implementation

Start implementation for decision **$1**.

## 実行前の必須事項

**このスキルを開始する前に、必ず TodoWrite で以下のタスクを作成すること:**

1. [ ] cdd.md の存在確認と decisionStatus: DECIDED 検証
2. [ ] implementationStatus を IN_PROGRESS に変更
3. [ ] 実装タスクの分解（具体的なステップ）
4. [ ] ビルド・テスト
5. [ ] Git コミット（CDD: $1 を含む）
6. [ ] implementationStatus を IN_REVIEW に変更
7. [ ] ユーザーにレビュー依頼

**TodoWrite なしで実装を開始してはならない。**

**禁止事項:**
- `implementationStatus: DONE` への変更は **このスキル内で行わない**
- DONE はレビュー APPROVED 後にのみ変更可能

---

## Your Task

1. **Load and verify decision:**
   - Find the cdd.md file for $1
   - **CRITICAL**: Verify `decisionStatus: DECIDED`
   - If not DECIDED, stop with error: "Cannot implement - decision not finalized"

2. **Read the full specification:**
   - Goal: What we're achieving
   - Context: Constraints and background
   - Selection: What was decided and why
   - Rejections: What NOT to do

3. **Update implementation status (with confirmation):**
   - **Use AskUserQuestion tool** to confirm:
     - Question: "implementationStatusをIN_PROGRESSに変更しますか？"
     - Options: "はい" / "いいえ"
   - If "はい", change `implementationStatus: IN_PROGRESS`
   - If "いいえ", stop implementation

4. **Execute implementation:**
   - Follow the Selection section exactly
   - Respect all constraints in Context
   - DO NOT implement anything from Rejections
   - **DO NOT add `@cdd #$1` markers in code** (deprecated)

5. **Track changed files:**
   - Keep a list of all files you create or modify during implementation
   - This will be used in the commit message

6. **Create commit when implementation is complete:**
   - Use the Bash tool to run: `git status` to see changed files
   - Generate commit message in this format:
     ```
     <type>: <summary> ($1)

     <detailed description of changes>

     CDD: $1
     Files:
     - <file1>
     - <file2>
     - <file3>
     ```
   - **Use AskUserQuestion tool** to confirm before committing:
     - Question: "このコミットメッセージで良いですか？"
     - Options: "はい" / "修正が必要"
   - Use `git add` and `git commit` with the generated message

7. **Update implementation status to IN_REVIEW (with confirmation):**
   - **Use AskUserQuestion tool** to confirm:
     - Question: "implementationStatusをIN_REVIEWに変更しますか？"
     - Options: "はい" / "いいえ"
   - If "はい", change `implementationStatus: IN_REVIEW`
   - **DO NOT change to DONE** - wait for review approval

8. **Request review:**
   - Inform user that implementation is complete
   - Suggest running `/cdd-review-implementation $1`

## Important Rules

- **NEVER deviate from the decided approach**
- If you find issues during implementation, STOP and discuss first
- **DO NOT add `@cdd #$1` comments** - use Git commit messages instead
- **DO NOT set implementationStatus to DONE** - only IN_REVIEW after implementation

## Commit Message Format

**Type prefix**:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation changes
- `test`: Test additions or changes
- `chore`: Maintenance tasks

**Example**:
```
feat: Add review history tracking (PHASE3-003)

Implemented automatic review history updates when implementationStatus
changes. Added ReviewHistoryEntry type and review file generation.

CDD: PHASE3-003
Files:
- src/core/review-tracker.ts
- src/types.ts
- src/commands/review.ts
```
