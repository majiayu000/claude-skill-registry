---
name: update-plugin
description: "설치된 Oh My TIL 플러그인을 최신 버전으로 업데이트합니다"
argument-hint: "<vault-path>"
---

# Update Plugin Skill

이미 설치된 Oh My TIL 플러그인을 최신 소스로 업데이트합니다.

## 활성화 조건

- `/update-plugin <vault-path>`
- "플러그인 업데이트해줘"

## 인수 처리

- **첫 번째 인수**: Obsidian vault 경로 (필수)
  - 예: `~/workspace/my-vault`, `/Users/name/Documents/obsidian-vault`

## 업데이트 절차

### 1. 사전 검증

```bash
# vault 경로 + 기존 설치 검증
ls <vault-path>/.obsidian/plugins/oh-my-til/manifest.json
```

플러그인이 설치되어 있지 않으면 `/install-plugin`을 사용하라고 안내하고 중단한다.

### 2. 최신 소스 가져오기

```bash
# 현재 브랜치가 main인지 확인
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "[ERROR] 현재 브랜치가 main이 아닙니다: $CURRENT_BRANCH"
  echo "main 브랜치에서 실행하세요: git checkout main"
  exit 1
fi

git pull origin main
```

현재 브랜치가 main이 아니면 사용자에게 안내하고 중단한다. 충돌이 발생하면 사용자에게 알린다.

### 3. 배포

스킬/규칙을 항상 포함하여 배포한다 (`plugin-version` frontmatter로 사용자 커스터마이즈 파일은 자동 보호됨).

```bash
npm run deploy -- --refresh-skills <vault-path>
```

deploy 스크립트가 빌드, 에셋 복사, node-pty 재빌드(Electron 버전 변경 시에만), 스킬/규칙 재설치를 자동 처리한다.

### 4. 완료 안내

```
업데이트 완료!

Obsidian을 재시작하거나 플러그인을 다시 로드하세요.
```

## 주의사항

- 이 스킬은 프로젝트 루트 디렉토리에서 실행해야 한다
- 에셋(main.js, manifest.json, styles.css)만 교체하므로 사용자 설정은 유지된다
- node-pty 재빌드는 Electron 버전이 변경된 경우에만 실행된다 (`.electron-version` 파일로 추적)
