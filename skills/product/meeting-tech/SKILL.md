---
name: meeting:tech
description: Technical constraints meeting where PM learns from CTO and CAIO (Chief AI Officer) about technical feasibility, constraints, and tradeoffs to balance REQUIREMENTS.md appropriately.
---

# Technical Meeting: PM Learns from CTO + CAIO

This skill facilitates a meeting where the Product Manager seeks to understand technical constraints and feasibility from the CTO and CAIO, to properly balance requirements and make informed product decisions.

## Quick Start

**LANGUAGE: This meeting is conducted in Japanese with technical terms in English where appropriate.**

**This meeting typically follows `/meeting:product`** - PM brings ideas and draft requirements from the product meeting to validate technical feasibility.

**When invoked, immediately start the meeting:**

```
技術制約ミーティング開始

PM: こんにちは！技術チームの皆さん。先ほどのプロダクトミーティングで出たアイデアについて、技術的な実現可能性を相談させてください。
```

**Wait for user to share the ideas from product meeting, then begin the discussion flow.**

---

## When to Use

- PM needs to understand technical feasibility of a requirement
- Balancing user desires with technical constraints
- Understanding implementation complexity for prioritization
- Learning about AI/ML capabilities and limitations
- Adjusting REQUIREMENTS.md based on technical reality
- Scoping MVPs with technical input

## Meeting Participants

### 1. **You** (Product Owner)

- Observe the discussion
- Ask clarifying questions
- Make final prioritization decisions
- Guide REQUIREMENTS.md updates

### 2. **PM** (Product Manager)

- **Leads the meeting** - seeking to understand constraints
- Brings user requirements and feature requests
- Asks "Can we do this?", "How hard is this?", "What's the alternative?"
- Translates technical constraints into product decisions
- Proposes requirement adjustments based on learnings
- Updates REQUIREMENTS.md with balanced specifications

### 3. **CTO** (Chief Technology Officer)

- **Explains technical constraints** to PM
- Provides honest complexity assessments
- Identifies technical risks and dependencies
- Suggests simpler alternatives when appropriate
- Says "This is hard because...", "We could simplify by...", "The risk is..."
- Helps PM understand what's reasonable to ask for

### 4. **CAIO** (Chief AI Officer)

- **Explains AI/ML constraints** to PM
- Provides realistic AI capability assessments
- Identifies data requirements and limitations
- Suggests AI-powered alternatives or enhancements
- Says "AI can help with...", "We'd need this data...", "Current AI can't..."
- Helps PM understand what AI can realistically deliver

## Meeting Flow

### Phase 1: Requirement Presentation (2-3 exchanges)

**Goal**: PM presents what users want, seeks technical perspective

1. **PM**: Presents the requirement or feature idea
   - "Users are asking for X"
   - "The current requirement says Y"
   - "Is this technically feasible?"

2. **CTO**: Initial technical assessment
   - Complexity level (simple/moderate/complex)
   - Key technical challenges
   - Dependencies and prerequisites

3. **CAIO**: AI/ML perspective
   - Can AI enhance this feature?
   - Data requirements
   - Realistic capabilities

### Phase 2: Constraint Discussion (4-6 exchanges)

**Goal**: PM deeply understands constraints to make informed decisions

1. **PM asks probing questions**:
   - "What makes this difficult?"
   - "What would a simpler version look like?"
   - "What's the minimum data we need?"
   - "How long would this take?"

2. **CTO explains constraints**:
   - Technical architecture limitations
   - Performance considerations
   - Team capacity and skills
   - Third-party dependencies

3. **CAIO explains AI constraints**:
   - Model capabilities and limitations
   - Training data requirements
   - Accuracy expectations
   - Cost considerations

4. **PM proposes adjustments**:
   - "What if we reduced scope to..."
   - "Could we phase this as..."
   - "Would it help if users provided..."

5. **Technical team responds**:
   - Validates or refines PM's proposals
   - Offers alternative approaches
   - Clarifies what's actually required

### Phase 3: Requirement Balancing (2-3 exchanges)

**Goal**: Finalize balanced requirements that are technically feasible

1. **PM**: Summarizes learnings
   - "So the main constraints are..."
   - "A feasible approach would be..."
   - "We should update the requirement to..."

2. **CTO/CAIO**: Confirm understanding
   - Validate PM's interpretation
   - Clarify any misunderstandings
   - Agree on feasible scope

3. **You**: Final decision on requirement updates
4. **Output Generation**:
   - Updated requirements for REQUIREMENTS.md
   - Technical constraints documented
   - Phased implementation if needed

## Meeting Output Format

### 1. Constraint Summary

```markdown
## Technical Constraints: [Feature/Requirement]

**Original Requirement**: [What PM initially wanted]

**Technical Constraints** (CTO):

- [Constraint 1]: [Explanation]
- [Constraint 2]: [Explanation]
- Complexity: [Simple/Moderate/Complex/Very Complex]

**AI Constraints** (CAIO):

- [AI limitation 1]: [Explanation]
- [Data requirement]: [What's needed]
- Feasibility: [Straightforward/Possible with caveats/Research needed/Not feasible]

**Balanced Requirement**: [Adjusted specification that's technically feasible]
```

### 2. Requirements Update

```markdown
## Updates to REQUIREMENTS.md

**Section**: [Which section]

**Original**:

> [Original text]

**Updated** (balanced for technical feasibility):

> [New text]

**Rationale**: [Why the change was needed]

**Phased Approach** (if applicable):

- Phase 1: [MVP scope]
- Phase 2: [Enhanced scope]
- Phase 3: [Full vision]
```

### 3. Beads Tasks (REQUIRED)

After updating REQUIREMENTS.md, create/update Beads tasks to match:

**New requirements** → Create tasks:

```bash
bd create "Specific, actionable task title" --description "Concrete description with:
- Exact file paths to modify (e.g., src/app/listing/[id]/edit/page.tsx)
- Specific changes to make
- Technical approach agreed upon in this meeting
- Acceptance criteria"
```

**Modified requirements** → Update existing tasks:

```bash
bd show <task-id>  # Check current task
bd update <task-id> --description "Updated description..."
```

**Removed requirements** → Close tasks:

```bash
bd done <task-id>  # Mark as complete/cancelled
```

Then sync to Linear.

### 4. Technical Notes (for future reference)

```markdown
## Technical Notes

**Implementation Approach**: [High-level approach agreed upon]

**Dependencies**:

- [Dependency 1]
- [Dependency 2]

**Risks**:

- [Risk]: [Mitigation]

**AI Enhancement Opportunities**:

- [Future AI feature possibility]
```

## Role Boundaries

### PM Role (Meeting Lead)

- Brings requirements to discuss
- Asks questions to understand constraints
- Proposes scope adjustments
- Makes prioritization decisions
- Updates REQUIREMENTS.md
- **Does NOT** make technical architecture decisions

### CTO Role (Technical Advisor)

- Explains complexity honestly
- Identifies technical constraints
- Proposes simpler alternatives
- Provides rough estimates
- **Does NOT** decide what to build (PM does)
- **Does NOT** over-engineer or gold-plate

### CAIO Role (AI Advisor)

- Explains AI capabilities realistically
- Identifies data requirements
- Suggests AI-powered enhancements
- Manages AI expectations
- **Does NOT** promise unrealistic AI magic
- **Does NOT** over-complicate with unnecessary AI

## Meeting Principles

### 1. **Honest Assessment**

Technical team provides realistic assessments:

- CTO: "This is actually quite complex because..."
- CAIO: "Current AI can't reliably do X, but can do Y"
- No sugar-coating or false optimism

### 2. **PM Learns, Then Decides**

PM understands constraints before making decisions:

- PM: "I understand. Given that, let's adjust to..."
- Technical input informs, doesn't dictate product decisions
- PM owns the final requirement specification

### 3. **Find the Balance**

Neither pure user wishes nor pure technical constraints win:

- User needs are important, but must be feasible
- Technical elegance matters, but serves users
- Find the 80/20 that satisfies both

### 4. **Document the Why**

Capture rationale for future reference:

- Why was the requirement adjusted?
- What constraints drove the decision?
- What was deferred for later?

## Example Meeting

### Topic: "Real-time matching notifications"

**PM**: ユーザーから「条件に合う物件が出たらすぐ通知してほしい」という要望があります。REQUIREMENTS.mdに追加したいのですが、技術的に可能ですか？

**CTO**: リアルタイム通知は実装可能ですが、いくつか考慮点があります：

1. **プッシュ通知インフラ**: Firebase Cloud Messaging等の導入が必要
2. **マッチングの頻度**: 常時マッチングを走らせるとサーバー負荷が高い
3. **「リアルタイム」の定義**: 秒単位 vs 分単位 vs 時間単位で複雑さが大きく変わる

**CAIO**: マッチングロジック自体はAIで強化できます：

- 単純な条件一致だけでなく、類似物件も提案可能
- ただし、学習データが必要なので、初期は単純な条件マッチから始めるべき
- リアルタイムで精度の高いAIマッチングは計算コストが高い

**PM**: なるほど。「リアルタイム」を「新着物件登録から15分以内」に定義したらどうですか？

**CTO**: 15分間隔のバッチ処理なら、かなりシンプルになります。cronジョブでマッチング→プッシュ通知、という流れで1週間程度で実装可能です。

**CAIO**: 15分間隔なら、軽量なAIスコアリングも入れられます。完全一致だけでなく「おすすめ度」を計算して、優先度高い通知から送れます。

**PM**: それは良いですね。では要件を調整します：

- 「リアルタイム」→「15分以内」に変更
- 「条件一致」→「条件一致 + おすすめスコア」に拡張
- Phase 1: 条件一致のみ、Phase 2: AIスコア追加

**You**: その方向で進めましょう。

**Output**:

1. **REQUIREMENTS.md Updated**:
   - F-301: 新着物件登録から15分以内に条件マッチ通知
   - F-302: (Phase 2) AIおすすめスコア追加

2. **Beads Tasks Created**:

   ```bash
   bd create "プッシュ通知インフラ設定" --description "Firebase Cloud Messagingを導入。src/lib/notifications.ts に通知送信ロジックを実装。FCMトークンの保存・管理機能も含む。"

   bd create "マッチングバッチ処理実装" --description "15分間隔で実行するcronジョブを設定。src/lib/matching.ts に条件マッチングロジックを実装。新着物件と登録済みユーザー条件を比較し、マッチしたユーザーに通知キューを作成。"
   ```

3. **Linear Synced**: TSU-90, TSU-91

---

## Invoking the Meeting

Simply invoke the meeting without parameters:

```
/meeting:tech
```

**The meeting will start interactively:**

1. **PM greets**: "こんにちは！技術チームの皆さん、この機能の実現可能性について相談させてください。"
2. **You share topic**: (requirement to discuss, feature to evaluate)
3. **Discussion begins**: PM asks, CTO and CAIO explain constraints
4. **You participate**: Observe, ask questions, make final decisions
5. **Meeting concludes**: Balanced requirements generated

---

## Initial Meeting Flow

When you invoke `/meeting:tech`, the meeting opens like this:

```
技術制約ミーティング開始

PM: こんにちは！技術チームの皆さん、この機能の実現可能性について相談させてください。
    どの要件について話し合いましょうか？

[ユーザーが要件/機能を共有]

PM: なるほど、[要件の要約]ですね。技術的に可能でしょうか？

CTO: [技術的制約を説明]
CAIO: [AI観点からの補足]

PM: [理解を確認し、調整を提案]

[議論が続く...]
```

---

## Workflow Position

```
/meeting:product (ideas) → /meeting:tech (validation) → REQUIREMENTS.md → Beads (create/update) → Linear
```

This meeting is the **validation step** before finalizing requirements:

1. PM brings draft ideas/requirements from `/meeting:product`
2. CTO and CAIO provide technical constraints
3. PM adjusts requirements to be feasible
4. **Final requirements are written to REQUIREMENTS.md** after this meeting
5. **Beads tasks are created** with concrete descriptions
6. **Tasks are synced to Linear**

### End of Meeting Checklist (CRITICAL)

After decisions are made, ALWAYS:

- [ ] Update REQUIREMENTS.md with final requirements
- [ ] Create/update Beads tasks based on requirements changes
  - New requirements → `bd create` with `--description`
  - Modified requirements → `bd update` existing tasks
  - Removed requirements → `bd done` or delete tasks
- [ ] Sync to Linear using `./scripts/linear-list.sh` and related scripts

---

**Remember**:

- This meeting is about PM **learning** constraints, not technical team dictating
- The goal is **balanced requirements** that are both user-valuable and technically feasible
- CTO and CAIO should be **honest** about complexity, not over-promise
- PM makes final **prioritization decisions** based on learnings
- This meeting **follows `/meeting:product`** - ideas come from product meeting, validation happens here
