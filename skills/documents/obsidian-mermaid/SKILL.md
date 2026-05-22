---
name: obsidian-mermaid
description: Create Obsidian-compatible Mermaid diagrams. Prefer square layouts (TB + subgraph LR), avoid markdown in labels. Use when creating flowcharts, sequence diagrams, or any Mermaid diagrams in markdown files.
allowed-tools:
  - Read
  - Edit
license: MIT
---

# Obsidian Mermaid Diagrams

Create Mermaid diagrams that render correctly in Obsidian and publish without issues.

## When to Use This Skill

Activate when you need to:
- Create flowcharts, sequence diagrams, ER diagrams
- Convert ASCII art to Mermaid
- Fix Mermaid rendering errors in Obsidian

## Core Principle: Simplicity First

> **다이어그램은 한눈에 들어와야 한다**

복잡한 다이어그램은 읽기 어렵다. 항상 최소한의 노드와 연결로 핵심만 표현하라.

### Node Minimization

**Before** (9개 노드):
```mermaid
flowchart LR
    A[수집] --> B[정리] --> C[보관]
    D[목표] --> E[학습] --> F[실행] --> G[측정] --> H[달성]
```

**After** (2개 노드 - 순차 흐름을 노드 내 텍스트로):
```mermaid
flowchart LR
    A[수집 → 정리 → 보관]
    B[목표 → 학습 → 실행 → 달성]
```

### Connection Minimization

- 핵심 흐름만 표현, 세부사항은 본문에서 설명
- 노드 5개 이하, 연결선 교차 금지
- 복잡한 관계는 여러 개의 단순한 다이어그램으로 분리

### Table vs Mermaid 선택

| 형식 | 용도 | 예시 |
|------|------|------|
| **테이블** | 속성-값 매핑, 비교, 옵션 | 에너지 레벨별 작업 |
| **Mermaid** | 흐름, 프로세스, 피드백 루프 | 입력→처리→출력 |
| **인라인** | 단순 순차 흐름 | `A → B → C` |

**원칙**: 같은 정보를 더 컴팩트하게 표현하는 형식 선택

---

## Critical Rules

### 1. NO Markdown in Labels

**Common Errors**:
```
Node["1. First"]     → "Unsupported markdown: list"
Node["Text<br/>More"] → "Unsupported markdown: heading"
Node["## Header"]    → "Unsupported markdown: heading"
```

**Correct**:
```
Node[First]
Node[Text]
```

**Rule**: Keep labels plain text. Move complex descriptions outside the diagram.

### 2. Prefer Square Layout (정사각형 레이아웃)

**Problem**: `flowchart LR`은 너무 넓고, `flowchart TB`는 너무 길어진다.

**Solution**: TB + 내부 LR 조합으로 정사각형에 가까운 레이아웃 만들기

```mermaid
flowchart TB
    subgraph Layer1["레이어 1"]
        direction LR
        A[항목A] ~~~ B[항목B] ~~~ C[항목C]
    end

    subgraph Layer2["레이어 2"]
        direction LR
        D[항목D] ~~~ E[항목E]
    end

    Layer1 --> Layer2
```

**패턴**:
- `flowchart TB`: 전체 흐름은 위→아래
- `direction LR`: 각 subgraph 내부는 가로 배치
- `~~~`: 보이지 않는 연결 (화살표 없이 정렬용)

**Rule**: 세로로 너무 길어지면 subgraph + `direction LR` 사용.

### 3. Keep Labels Short

```markdown
❌ Too long:
Node["This is a very long description that will break layout"]

✅ Short and clear:
Node[Short Label]
```

**Rule**: Labels should be under 15 characters. Add details in text below the diagram.

### 4. Avoid Special Characters in Subgraph Names

```markdown
❌ May cause issues:
subgraph "1. Phase One"
subgraph "Phase: Setup"

✅ Safe:
subgraph Phase_One["Phase One"]
subgraph Setup["Setup Phase"]
```

## Good Examples

### Simple Flowchart
```mermaid
flowchart TB
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
```

### Process Flow with Details Outside
```mermaid
flowchart TB
    Input[Input] --> Process[Process]
    Process --> Output[Output]
```

**Process Details**:
- Input: User data from form
- Process: Validation and transformation
- Output: Saved to database

### Subgraph Example
```mermaid
flowchart TB
    subgraph Frontend["Frontend"]
        UI[UI] --> API[API Call]
    end
    subgraph Backend["Backend"]
        Server[Server] --> DB[Database]
    end
    API --> Server
```

## Bad Examples (Don't Do This)

### Markdown in Labels
```mermaid
flowchart LR
    A["1. Start<br/>with details"] --> B{"2. Decision"}
```
This will show "Unsupported markdown" errors.

### Too Wide
```mermaid
flowchart LR
    A[Very Long Process Name Here] --> B[Another Long Name] --> C[Yet Another] --> D[And More]
```
This gets cut off on mobile and narrow screens.

## Converting ASCII to Mermaid

**ASCII Art**:
```
┌───────┐     ┌───────┐
│ Start │────→│  End  │
└───────┘     └───────┘
```

**Mermaid**:
```mermaid
flowchart TB
    Start[Start] --> End[End]
```

## Quality Checklist

Before completing diagram creation:

- [ ] No `<br/>` tags in node labels
- [ ] No numbered list format (`1.`, `2.`) in labels
- [ ] **정사각형 레이아웃**: TB + subgraph 내 LR 조합 사용
- [ ] All labels are short (under 15 characters)
- [ ] Complex details moved to text outside diagram
- [ ] No special characters in subgraph names
- [ ] Tested rendering in Obsidian preview
