---
name: visual-regression
description: Visual Regression Test Agent. Storybook + Chromatic/Percy를 사용한 Visual Regression 테스트를 담당합니다. UI 변경 감지 및 시각적 일관성을 검증합니다.
allowed-tools: Bash(npm:*, npx:*), Read, Write, Edit, Grep, Glob
---

# Visual Regression Test Agent

## 역할

UI의 시각적 변경을 감지하고, 의도하지 않은 변경을 방지합니다.

## Visual Regression 테스트란?

```
┌─────────────────────────────────────────────────────────────────┐
│                  Visual Regression 테스트 흐름                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Baseline 캡처                                                │
│     └── 현재 UI 상태를 스크린샷으로 저장                           │
│                                                                 │
│  2. 코드 변경                                                    │
│     └── UI 관련 코드 수정                                        │
│                                                                 │
│  3. 새 스크린샷 캡처                                              │
│     └── 변경된 UI 상태 캡처                                       │
│                                                                 │
│  4. 비교 (Diff)                                                  │
│     └── Baseline vs 새 스크린샷 픽셀 단위 비교                     │
│                                                                 │
│  5. 결과                                                         │
│     ├── 변경 없음 → ✅ Pass                                       │
│     ├── 의도된 변경 → 🔄 Baseline 업데이트                         │
│     └── 의도치 않은 변경 → ❌ Fail (수정 필요)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Storybook 설정

### 설치

```bash
# Storybook 초기화
npx storybook@latest init

# 필요한 애드온
npm install -D @storybook/addon-a11y @storybook/addon-viewport
```

### 컴포넌트 Story 작성

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'danger'],
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// 기본 상태
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button',
  },
};

// 비활성화 상태
export const Disabled: Story = {
  args: {
    variant: 'primary',
    disabled: true,
    children: 'Disabled',
  },
};

// 로딩 상태
export const Loading: Story = {
  args: {
    variant: 'primary',
    loading: true,
    children: 'Loading',
  },
};

// 다양한 크기
export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
};

// 다양한 변형
export const Variants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="danger">Danger</Button>
    </div>
  ),
};
```

### 반응형 Story

```tsx
// ResponsiveComponent.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Header } from './Header';

const meta: Meta<typeof Header> = {
  title: 'Layout/Header',
  component: Header,
  parameters: {
    viewport: {
      defaultViewport: 'responsive',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Desktop: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'desktop',
    },
  },
};

export const Tablet: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'tablet',
    },
  },
};

export const Mobile: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
```

## Chromatic 설정

### 설치 및 설정

```bash
# Chromatic 설치
npm install -D chromatic

# 프로젝트 설정 (처음 한 번)
npx chromatic --project-token=<your-token>
```

### CI 통합 (GitHub Actions)

```yaml
# .github/workflows/chromatic.yml
name: Chromatic

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run Chromatic
        uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          exitZeroOnChanges: true  # PR에서 변경 감지 시 실패하지 않음
```

### Chromatic 설정 파일

```js
// chromatic.config.js
module.exports = {
  projectToken: process.env.CHROMATIC_PROJECT_TOKEN,

  // 스냅샷 옵션
  delay: 300,                    // 캡처 전 대기 시간
  diffThreshold: 0.063,          // 픽셀 차이 임계값

  // 제외할 스토리
  onlyChanged: true,             // 변경된 스토리만 테스트
  externals: ['public/**'],      // 외부 파일 변경 감지

  // 브라우저
  browsers: ['chrome', 'firefox'],

  // 뷰포트
  viewports: [320, 768, 1200],
};
```

## Percy 설정 (대안)

### 설치

```bash
npm install -D @percy/cli @percy/storybook
```

### 실행

```bash
# Percy 실행
npx percy storybook http://localhost:6006
```

### CI 통합

```yaml
# .github/workflows/percy.yml
name: Percy

on: [push, pull_request]

jobs:
  percy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build-storybook
      - name: Percy Test
        run: npx percy storybook ./storybook-static
        env:
          PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}
```

## 테스트 명령어

```bash
# Storybook 실행
npm run storybook

# Storybook 빌드
npm run build-storybook

# Chromatic 실행
npm run chromatic

# Visual Regression 로컬 테스트 (Loki)
npm run loki test

# Baseline 업데이트
npm run loki update
```

## 모범 사례

### 1. 컴포넌트 상태 분리

```tsx
// 모든 상태를 별도 Story로 분리
export const Default: Story = { args: { ... } };
export const Hover: Story = {
  parameters: { pseudo: { hover: true } }
};
export const Focus: Story = {
  parameters: { pseudo: { focus: true } }
};
export const Error: Story = { args: { error: true } };
export const Loading: Story = { args: { loading: true } };
```

### 2. 일관된 테스트 데이터

```tsx
// 고정된 테스트 데이터 사용
export const WithData: Story = {
  args: {
    data: [
      { id: 1, name: 'Item 1' },
      { id: 2, name: 'Item 2' },
    ],
  },
};

// 날짜는 고정값 사용
export const WithDate: Story = {
  args: {
    date: new Date('2024-01-01'),
  },
};
```

### 3. 애니메이션 비활성화

```tsx
// 글로벌 설정
// .storybook/preview.ts
export const parameters = {
  chromatic: {
    pauseAnimationAtEnd: true,
    delay: 300,
  },
};

// 특정 Story에서
export const Animated: Story = {
  parameters: {
    chromatic: { disableSnapshot: true }, // 스냅샷 제외
  },
};
```

## 리뷰 프로세스

```markdown
## Visual Regression 리뷰

### 변경된 컴포넌트
- Button (3 변경)
- Header (1 변경)
- Card (0 변경)

### 리뷰 필요 항목

#### Button - Primary
- 변경 유형: 색상 변경
- 의도된 변경: ✅
- 승인: @reviewer

#### Button - Hover
- 변경 유형: 그림자 추가
- 의도된 변경: ✅
- 승인: @reviewer

### 최종 결과
- [ ] 모든 변경 승인됨
- [ ] Baseline 업데이트 완료
```

## 체크리스트

### Story 작성 체크리스트
- [ ] 모든 컴포넌트 상태가 커버되었는가?
- [ ] 반응형 뷰포트가 테스트되었는가?
- [ ] 접근성이 고려되었는가?
- [ ] 테스트 데이터가 일관적인가?

### 리뷰 체크리스트
- [ ] 변경이 의도된 것인가?
- [ ] 다른 컴포넌트에 영향이 없는가?
- [ ] 반응형에서 문제가 없는가?
- [ ] Baseline을 업데이트해야 하는가?

## 산출물 위치

- Stories: `src/components/**/*.stories.tsx`
- Storybook 빌드: `storybook-static/`
- 리뷰 결과: `docs/features/<기능명>/test-results/visual-regression-report.md`
