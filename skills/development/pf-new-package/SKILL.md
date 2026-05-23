---
name: pf-new-package
description: 새 패키지 생성 가이드. "패키지 만들어", "새 패키지", "package 추가" 요청 시 사용.
allowed-tools: Read, Write, Bash, Glob
---

# PF 새 패키지 생성 가이드

$ARGUMENTS 새로운 공유 패키지를 생성합니다.

---

## 패키지 구조

```
packages/
├── ui/           # UI 컴포넌트
├── api/          # API 클라이언트
├── services/     # 공통 서비스
├── map/          # CesiumJS 지도
├── three/        # Three.js 3D
├── cctv/         # 영상 스트리밍
└── [new-pkg]/    # 새 패키지
```

---

## 1단계: 폴더 구조 생성

```bash
mkdir -p packages/새패키지/src
cd packages/새패키지
```

### 기본 구조

```
packages/새패키지/
├── src/
│   ├── index.ts          # 진입점 (exports)
│   ├── components/       # 컴포넌트 (있다면)
│   ├── hooks/            # 훅
│   ├── stores/           # Zustand 스토어
│   ├── utils/            # 유틸리티
│   └── types/            # 타입 정의
│       └── index.ts
├── package.json
├── tsconfig.json
├── vite.config.ts        # 빌드 설정
└── README.md
```

---

## 2단계: package.json 생성

```json
{
  "name": "@pf-dev/새패키지",
  "version": "0.1.0",
  "type": "module",
  "main": "./dist/index.js",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist"],
  "scripts": {
    "dev": "vite build --watch",
    "build": "vite build && tsc --emitDeclarationOnly",
    "lint": "eslint src --ext .ts,.tsx",
    "clean": "rimraf dist"
  },
  "peerDependencies": {
    "react": "catalog:",
    "react-dom": "catalog:"
  },
  "devDependencies": {
    "@pf-dev/eslint-config": "workspace:*",
    "@pf-dev/typescript-config": "workspace:*",
    "typescript": "catalog:",
    "vite": "catalog:"
  }
}
```

---

## 3단계: tsconfig.json 생성

```json
{
  "extends": "@pf-dev/typescript-config/library.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## 4단계: vite.config.ts 생성

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: resolve(__dirname, "src/index.ts"),
      formats: ["es"],
      fileName: "index",
    },
    rollupOptions: {
      external: ["react", "react-dom"],
    },
  },
});
```

---

## 5단계: src/index.ts 생성

```ts
// Components
export * from "./components";

// Hooks
export * from "./hooks";

// Stores
export * from "./stores";

// Types
export type * from "./types";
```

---

## 6단계: ESLint 설정

```js
// eslint.config.js
import baseConfig from "@pf-dev/eslint-config/library";

export default [...baseConfig];
```

---

## 7단계: README.md 작성

```markdown
# @pf-dev/새패키지

간단한 설명

## 설치

이 패키지는 모노레포 내부 패키지입니다.

\`\`\`json
{
  "dependencies": {
    "@pf-dev/새패키지": "workspace:*"
  }
}
\`\`\`

## 사용법

\`\`\`tsx
import { Something } from "@pf-dev/새패키지";
\`\`\`

## API

### Components

- `ComponentName` - 설명

### Hooks

- `useHookName` - 설명

### Stores

- `useStoreName` - 설명
```

---

## 8단계: pnpm-workspace에 추가

`pnpm-workspace.yaml`에 이미 `packages/*`가 있으므로 자동 인식됩니다.

```bash
# 의존성 설치
pnpm install

# 빌드 테스트
pnpm --filter @pf-dev/새패키지 build
```

---

## 9단계: 다른 앱/패키지에서 사용

```json
// apps/앱이름/package.json
{
  "dependencies": {
    "@pf-dev/새패키지": "workspace:*"
  }
}
```

```bash
pnpm install
```

```tsx
// 사용
import { Something } from "@pf-dev/새패키지";
```

---

## 의존성 추가 시

### catalog 사용 (공통 패키지)

```yaml
# pnpm-workspace.yaml
catalog:
  새의존성: ^1.0.0
```

```json
// package.json
{
  "dependencies": {
    "새의존성": "catalog:"
  }
}
```

### 패키지 전용 의존성

```json
{
  "dependencies": {
    "특수패키지": "^1.0.0"
  }
}
```

---

## 체크리스트

- [ ] 폴더 구조 생성
- [ ] package.json 작성
- [ ] tsconfig.json 작성
- [ ] vite.config.ts 작성
- [ ] src/index.ts 생성
- [ ] eslint.config.js 작성
- [ ] README.md 작성
- [ ] pnpm install 실행
- [ ] 빌드 테스트
- [ ] 다른 패키지에서 import 테스트
