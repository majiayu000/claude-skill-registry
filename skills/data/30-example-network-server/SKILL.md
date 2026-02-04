# 30-example-network-server — Game Protocol TS 서버 예제

Status: ACTIVE
AppliesTo: v10
Type: GUIDE

---

## Scope / Purpose

Game protocol 기반 TypeScript **서버** 예제.

Devian 네트워크 서버 조립 방식과 ServerRuntime 사용법을 보여준다.

---

## 경로 SSOT

| 구분 | 경로 |
|------|------|
| **Server** | `framework-ts/apps/GameServer/` |

---

## 핵심 조립 포인트

```typescript
import { WsTransport, NetworkServer } from '@devian/core';
import { createServerRuntime, Game2C } from '@devian/protocol-game/server-runtime';

// 1. Runtime 생성
const runtime = createServerRuntime();

// 2. Stub 획득 (핸들러 등록용)
const stub = runtime.getStub();

// 3. Transport 생성
const transport = new WsTransport({ port: PORT }, {
    onBinaryMessage: (sessionId, data) => server.onBinaryMessage(sessionId, data),
    // ...events
});

// 4. NetworkServer 생성
const server = new NetworkServer(transport, runtime, {
    onUnknownInboundOpcode: async (event) => {
        // unknown opcode 처리 (disconnect 없이 로깅만)
        console.warn(`Unknown opcode ${event.opcode}`);
    },
});

// 5. Outbound Proxy 생성 (타입 안전)
const game2cProxy = server.createOutboundProxy<Game2C.Proxy>();

// 6. Handler 등록
stub.onPing(async (sessionId, msg) => {
    await game2cProxy.sendPong(sessionId, { ... });
});
```

---

## 코덱 전환 (USE_JSON)

```typescript
import { defaultCodec as jsonCodec } from '@devian/core';

// false = Protobuf (default), true = Json
const USE_JSON = false;

const runtime = USE_JSON ? createServerRuntime(jsonCodec) : createServerRuntime();
```

- **기본값**: Protobuf (바이너리, 성능 우선)
- **Json 옵션**: 디버깅/테스트용

---

## 실행 방법

```bash
npm -w GameServer run start
```

---

## 설정

| 항목 | 기본값 | 비고 |
|------|--------|------|
| Port | `8080` | WsTransport 바인딩 포트 |
| Unknown opcode | 로깅만, disconnect 안함 | `onUnknownInboundOpcode` 훅 |

---

## Related

- [31-example-network-client](../31-example-network-client/SKILL.md) — Game Protocol TS 클라이언트 예제
- [03-ssot](../03-ssot/SKILL.md) — Example Apps SSOT
- [20-example-protocol-game](../20-example-protocol-game/SKILL.md) — Game Protocol 예제
- [Protocol SSOT](../../devian-protocol/03-ssot/SKILL.md) — Opcode/Tag, Protocol UPM
