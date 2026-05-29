---
name: install-plugin
description: "Obsidian vault에 Oh My TIL 플러그인을 설치합니다"
argument-hint: "<vault-path>"
---

# Install Plugin Skill

Oh My TIL 플러그인을 Obsidian vault에 설치합니다.

## 활성화 조건

- `/install-plugin <vault-path>`
- "플러그인 설치해줘"

## 인수 처리

- **첫 번째 인수**: Obsidian vault 경로 (필수)
  - 예: `~/workspace/my-vault`, `/Users/name/Documents/obsidian-vault`
  - vault 경로에 `.obsidian` 폴더가 있는지 검증

## 설치 절차

아래 단계를 순서대로 실행한다. 각 단계에서 오류가 발생하면 중단하고 사용자에게 알린다.

### 1. 사전 검증

```bash
# vault 경로 검증
ls <vault-path>/.obsidian

# Node.js 설치 확인
node --version   # 18 이상 필요

# npm 설치 확인
npm --version
```

vault 경로가 유효하지 않거나 Node.js가 없으면 안내 메시지를 출력하고 중단한다.

### 2. 의존성 설치

프로젝트 루트에서:

```bash
npm install
```

### 3. 배포

deploy 스크립트를 실행한다. 빌드, 에셋 복사, 네이티브 모듈 설치, node-pty 재빌드를 자동 처리한다.

```bash
npm run deploy -- <vault-path>
```

### 4. 완료 안내

설치 완료 후 사용자에게 안내:

```
설치 완료!

1. Obsidian을 재시작하세요
2. 설정 > Community plugins에서 "Oh My TIL"을 활성화하세요
3. (선택) MCP 서버 연결:
   claude mcp add --transport http oh-my-til http://localhost:22360/mcp
```

## 주의사항

- 이 스킬은 프로젝트 루트 디렉토리에서 실행해야 한다 (`package.json`이 있는 위치)
- Electron 버전 감지에 실패하면 사용자에게 Obsidian 개발자 도구(Ctrl+Shift+I)에서 `process.versions.electron`을 확인하도록 안내한다
- 기존 설치가 있으면 덮어쓴다 (에셋만 교체, node_modules는 유지)
