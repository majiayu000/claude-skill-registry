---
name: lsp
description: LSP 통합 가이드. Cursor IDE의 내장 LSP 기능을 에이전트가 활용하도록 안내합니다. Go to Definition, Find References, Rename Symbol 등의 워크플로우를 Grep/SemanticSearch로 보완합니다. Use when performing precise code navigation, refactoring, or dependency analysis.
---

# LSP — Language Server Protocol 통합 가이드

Cursor IDE의 내장 LSP 기능을 에이전트가 최대한 활용하도록 안내합니다.

## 현재 Cursor에서의 LSP 접근

Cursor 에이전트는 직접적인 LSP API 호출이 제한적이므로 다음 도구로 보완합니다:

| LSP 기능 | Cursor 에이전트 대안 |
|---------|-------------------|
| Go to Definition | Grep `"class\|struct\|func\|protocol NAME"` + SemanticSearch |
| Find References | Grep `"NAME"` + SemanticSearch `"Where is NAME used?"` |
| Rename Symbol | Grep → StrReplace (replace_all: true) 또는 ast-refactor 스킬 |
| Diagnostics | ReadLints |
| Hover (type info) | Grep + Read (타입 선언 파일 직접 읽기) |
| Code Actions | 수동 패턴 매칭 + StrReplace |

## 워크플로우

### Go to Definition
1. Grep으로 심볼의 선언 패턴을 검색:
   - Swift: `"(class|struct|enum|protocol|func)\s+SymbolName"`
   - TypeScript: `"(class|interface|function|type)\s+SymbolName"`
   - Python: `"(class|def)\s+SymbolName"`
2. 결과가 모호하면 SemanticSearch `"Where is SymbolName defined?"`
3. 파일과 라인 번호 확인 후 Read로 컨텍스트 읽기

### Find References
1. Grep으로 심볼명을 전체 코드베이스에서 검색
2. import/use 문과 실제 사용처를 구분
3. 결과를 사용 유형별로 분류:
   - 선언 (Declaration)
   - Import
   - 호출 (Call site)
   - 타입 참조 (Type reference)
   - 상속/채택 (Inheritance/Conformance)

### Rename Symbol
1. Grep으로 모든 참조 위치 확인
2. 각 참조가 동일 심볼인지 검증 (동명 이의어 구분)
3. StrReplace (replace_all: true)로 각 파일에서 치환
4. 또는 `.claude/skills/ast-refactor/SKILL.md`의 AST 기반 리네이밍 사용

### Diagnostics
1. ReadLints로 현재 오류/경고 수집
2. 오류를 유형별로 분류 (타입, import, 문법, 논리)
3. 우선순위에 따라 수정

## 원칙

- 정확 매칭(Grep) 우선, 의미 검색(SemanticSearch)은 보완
- 리네이밍 시 반드시 모든 참조를 확인한 후 일괄 치환
- ReadLints를 적극 활용하여 변경 후 검증
- 대규모 리팩토링은 ast-refactor 스킬과 병행
