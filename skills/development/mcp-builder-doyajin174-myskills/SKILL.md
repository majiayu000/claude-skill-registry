---
name: mcp-builder
description: Guide for creating MCP (Model Context Protocol) servers. Use this when building integrations with external services, creating new MCP servers, or connecting Claude to APIs.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: anthropics
  version: "1.0"
---

# MCP Server Builder

MCP 서버를 생성하여 Claude를 외부 서비스와 연결하는 가이드입니다.

## Overview

> "MCP 서버의 품질은 LLM이 실제 작업을 얼마나 잘 수행할 수 있게 하는가로 측정된다"

## Four-Phase Development

### Phase 1: Research & Planning

```
1. MCP 설계 원칙 이해
2. 프로토콜 문서 학습 (mcp.io)
3. 프레임워크 선택 (TypeScript 권장)
4. 대상 API 분석
```

### Phase 2: Implementation

```
project/
├── src/
│   ├── index.ts      # 진입점
│   ├── client.ts     # API 클라이언트
│   ├── tools/        # 도구 구현
│   └── types.ts      # 타입 정의
├── package.json
└── tsconfig.json
```

**도구 어노테이션:**
| 타입 | 설명 |
|------|------|
| `read-only` | 데이터 조회만 |
| `destructive` | 데이터 수정/삭제 |
| `idempotent` | 반복 실행 안전 |
| `open-world` | 외부 시스템 영향 |

### Phase 3: Review & Test

```bash
# MCP Inspector로 테스트
npx @anthropic/mcp-inspector

# 도구 호출 테스트
mcp-inspector --server ./dist/index.js
```

### Phase 4: Create Evaluations

10개의 복잡한 평가 질문 생성:
- 독립적이고 읽기 전용
- 검증 가능한 답변
- 실제 사용 시나리오 반영

## Technical Recommendations

### Transport 선택

| 환경 | 권장 Transport |
|------|---------------|
| 로컬 CLI | stdio |
| 원격 서버 | Streamable HTTP |
| 브라우저 | SSE |

### TypeScript 구조

```typescript
import { Server } from "@modelcontextprotocol/sdk/server";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";

const server = new Server({
  name: "my-mcp-server",
  version: "1.0.0",
}, {
  capabilities: {
    tools: {},
  },
});

// 도구 등록
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_data",
      description: "데이터 조회",
      inputSchema: {
        type: "object",
        properties: {
          id: { type: "string" }
        },
        required: ["id"]
      }
    }
  ]
}));

// 도구 실행
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_data") {
    // 구현
  }
});

// 서버 시작
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Best Practices

### 도구 네이밍
```
✅ get_user_profile
✅ create_document
✅ search_files

❌ doThing
❌ process
❌ handle
```

### 에러 처리
```typescript
// 액션 가능한 에러 메시지
throw new Error(
  `API rate limit exceeded. Retry after ${retryAfter} seconds.`
);

// 사용자 가이드 포함
throw new Error(
  `Invalid API key. Get your key at https://api.example.com/keys`
);
```

### 상태 관리
- Stateless JSON 선호 (확장 용이)
- 세션 상태는 클라이언트에서 관리
- 캐싱은 선택적으로 구현

## Evaluation Format

```xml
<evaluation>
  <question>How many active users are in the system?</question>
  <expected_tools>["get_user_count"]</expected_tools>
  <validation>Response contains numeric count</validation>
</evaluation>
```

## References

- [MCP 공식 문서](https://modelcontextprotocol.io)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK (FastMCP)](https://github.com/jlowin/fastmcp)
