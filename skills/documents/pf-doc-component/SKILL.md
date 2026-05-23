---
name: pf-doc-component
description: 컴포넌트 README 생성. "문서화", "README 만들어", "컴포넌트 문서" 요청 시 사용.
allowed-tools: Read, Write, Glob
---

# PF 컴포넌트 문서 생성기

$ARGUMENTS 컴포넌트에 대한 README를 생성합니다.

---

## README 템플릿

```markdown
# ComponentName

간단한 설명 (한 줄)

## 설치

\`\`\`tsx
import { ComponentName } from "@pf-dev/ui";
\`\`\`

## 기본 사용법

\`\`\`tsx
<ComponentName>기본 사용</ComponentName>
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `"default" \| "secondary"` | `"default"` | 스타일 변형 |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | 크기 |
| `disabled` | `boolean` | `false` | 비활성화 |
| `onClick` | `() => void` | - | 클릭 핸들러 |

## 예제

### Variants

\`\`\`tsx
<ComponentName variant="default">Default</ComponentName>
<ComponentName variant="secondary">Secondary</ComponentName>
\`\`\`

### Sizes

\`\`\`tsx
<ComponentName size="sm">Small</ComponentName>
<ComponentName size="md">Medium</ComponentName>
<ComponentName size="lg">Large</ComponentName>
\`\`\`

### With Icon

\`\`\`tsx
<ComponentName>
  <Icon className="mr-2" />
  With Icon
</ComponentName>
\`\`\`

## 접근성

- 키보드: Tab으로 포커스, Enter/Space로 활성화
- ARIA: 적절한 role과 aria-* 속성 자동 적용
- 포커스: focus-visible 스타일 제공

## 관련 컴포넌트

- [RelatedComponent1](../RelatedComponent1/README.md)
- [RelatedComponent2](../RelatedComponent2/README.md)
```

---

## Composition 컴포넌트 템플릿

```markdown
# Sidebar

접을 수 있는 사이드바 컴포넌트

## 설치

\`\`\`tsx
import { Sidebar } from "@pf-dev/ui";
\`\`\`

## 기본 사용법

\`\`\`tsx
<Sidebar defaultCollapsed={false}>
  <Sidebar.Header title="Dashboard" />
  <Sidebar.Content>
    <Sidebar.Section label="메뉴">
      <Sidebar.Item icon={<HomeIcon />} active>홈</Sidebar.Item>
      <Sidebar.Item icon={<SettingsIcon />}>설정</Sidebar.Item>
    </Sidebar.Section>
  </Sidebar.Content>
  <Sidebar.Footer>
    <Sidebar.Item icon={<LogOutIcon />}>로그아웃</Sidebar.Item>
  </Sidebar.Footer>
</Sidebar>
\`\`\`

## 서브 컴포넌트

### Sidebar (Root)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `defaultCollapsed` | `boolean` | `false` | 초기 접힘 상태 |
| `collapsed` | `boolean` | - | 제어 모드용 접힘 상태 |
| `onCollapsedChange` | `(collapsed: boolean) => void` | - | 접힘 상태 변경 콜백 |
| `width` | `number` | `240` | 펼친 상태 너비 |
| `collapsedWidth` | `number` | `64` | 접힌 상태 너비 |

### Sidebar.Header

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | - | 헤더 제목 |
| `logo` | `ReactNode` | - | 로고 이미지 |

### Sidebar.Item

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `icon` | `ReactNode` | - | 아이콘 |
| `active` | `boolean` | `false` | 활성 상태 |
| `badge` | `number` | - | 뱃지 숫자 |
| `onClick` | `() => void` | - | 클릭 핸들러 |

### Sidebar.Section

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | - | 섹션 레이블 |
| `collapsible` | `boolean` | `false` | 접을 수 있는지 |

### Sidebar.CollapseButton

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `iconOnly` | `boolean` | `false` | 아이콘만 표시 |

## Context Hook

\`\`\`tsx
import { useSidebarContext } from "@pf-dev/ui";

function CustomItem() {
  const { collapsed, toggleCollapse } = useSidebarContext();

  return (
    <button onClick={toggleCollapse}>
      {collapsed ? "펼치기" : "접기"}
    </button>
  );
}
\`\`\`

## 제어 모드

\`\`\`tsx
function App() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <Sidebar
      collapsed={collapsed}
      onCollapsedChange={setCollapsed}
    >
      {/* ... */}
    </Sidebar>
  );
}
\`\`\`

## 스타일 커스터마이징

\`\`\`tsx
<Sidebar className="bg-gray-900">
  <Sidebar.Item className="hover:bg-gray-800">
    커스텀 스타일
  </Sidebar.Item>
</Sidebar>
\`\`\`
```

---

## 문서 작성 체크리스트

- [ ] 컴포넌트 설명 (한 줄)
- [ ] import 문
- [ ] 기본 사용법
- [ ] 모든 Props 테이블
- [ ] 주요 사용 예제
- [ ] 접근성 정보
- [ ] 관련 컴포넌트 링크
- [ ] (Composition) 서브 컴포넌트 문서
- [ ] (Composition) Context Hook 설명
- [ ] (선택) 스타일 커스터마이징 가이드
