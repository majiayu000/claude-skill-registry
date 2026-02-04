# 32-example-webgl-server — Unity WebGL 서버 가이드

Status: ACTIVE
AppliesTo: v10
Type: GUIDE

---

## Scope

UnityExample WebGL 빌드 → NestJS(WebGLServer)로 로컬 서빙 → 브라우저 스모크 테스트

---

## SSOT Paths

| 구분 | 경로 |
|------|------|
| **Unity project** | `framework-cs/apps/UnityExample/` |
| **WebGL build output (default)** | `output/unity-webgl/UnityExample/` |
| **NestJS server app** | `framework-ts/apps/WebGLServer/` |
| **환경변수 정의 (SSOT)** | `framework-ts/apps/WebGLServer/env.spec.json` |
| **.env.example (자동 생성)** | `framework-ts/apps/WebGLServer/.env.example` |

---

## Build Steps (Unity)

1. Unity Editor에서 `framework-cs/apps/UnityExample` 프로젝트 열기
2. **File → Build Settings**
3. **Platform: WebGL** 선택 → **Switch Platform**
4. **Development Build: On** (스모크 테스트 동안)
5. **Build** 클릭 → 출력 경로: `output/unity-webgl/UnityExample/`

---

## Run Steps

### Step 1: (권장) GameServer 실행

```bash
cd framework-ts
npm ci
npm -w game-server run start
```

### Step 2: WebGL 정적 서버 실행

```bash
cd framework-ts
npm -w webgl-server run start:dev
```

### Step 3: 브라우저 접속

```
http://localhost:8081/
```

---

## Environment Variables

> **SSOT**: `env.spec.json` → `.env.example`는 자동 생성 (수동 편집 금지)
>
> 환경변수 변경 시: `env.spec.json` 수정 → `npm -w webgl-server run env:sync`

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `WEBGL_ROOT` | `output/unity-webgl/UnityExample` | WebGL 빌드 출력 경로 |
| `WEBGL_PORT` | `8081` | 서버 포트 (1..65535) |

```bash
# .env.example 생성/갱신
npm -w webgl-server run env:sync

# 기본 실행
cd framework-ts
npm -w webgl-server run start:dev

# 포트 지정
cd framework-ts
WEBGL_PORT=8091 npm -w webgl-server run start:dev

# 루트+포트 지정
cd framework-ts
WEBGL_ROOT=output/unity-webgl/UnityExample WEBGL_PORT=8091 npm -w webgl-server run start:dev
```

---

## Smoke Checklist

| 항목 | 확인 |
|------|------|
| 로딩/씬 진입 OK | [ ] |
| console error 0 (특히 `.jslib not found`, `undefined symbol`, `Module.*`, `ERR_*`) | [ ] |
| (권장) WS 연결 성공 (서버 로그 + 브라우저 로그) | [ ] |

---

## DoD (Definition of Done)

- [ ] WebGL 로딩 성공, 씬 진입
- [ ] 브라우저 콘솔 치명 에러 0
- [ ] `WEBGL_PORT` 설정 시 해당 포트로 기동 확인
- [ ] (권장) WS 연결 확인:
  - 서버 로그에 connect 흔적
  - 브라우저에서 연결 성공 로그 또는 게임 UI에 연결 표시

---

## Hard Rules

1. **WebGL은 반드시 HTTP 서버로 서빙한다** (파일 직접 열기 금지)
2. **로컬 서빙은 NestJS(WebGLServer)를 표준으로 사용한다**
3. **DoD는 "빌드 성공"이 아니라 브라우저 로드 + 콘솔 에러 0까지 포함한다**

---

## Server Features

- **Port**: `WEBGL_PORT` (기본값 8081)
- **Static serving**: `WEBGL_ROOT` 폴더 정적 서빙
- **SPA fallback**: 정적 파일 없으면 `index.html`로 fallback
- **MIME types**: `.wasm`, `.data`, `.gz`, `.br` 헤더 자동 설정
- **Validation**: `index.html` 없으면 명확한 에러 메시지 후 종료

---

## Related

- [30-example-network-server](../30-example-network-server/SKILL.md) — Game Protocol TS 서버 예제
- [31-example-network-client](../31-example-network-client/SKILL.md) — Game Protocol TS 클라이언트 예제
- [03-ssot](../03-ssot/SKILL.md) — Example Apps SSOT
- [30-env-management](../../devian-tools/30-env-management/SKILL.md) — 환경변수 관리 정책
