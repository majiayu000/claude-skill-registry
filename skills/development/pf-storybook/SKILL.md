---
name: pf-storybook
description: Storybook 스토리 생성. "스토리북", "스토리 만들어", "Storybook" 요청 시 사용.
allowed-tools: Read, Write, Glob
---

# PF Storybook 스토리 생성기

$ARGUMENTS 컴포넌트에 대한 Storybook 스토리를 생성합니다.

---

## 스토리 파일 위치

```
packages/ui/src/atoms/Button/
├── Button.tsx
├── Button.stories.tsx  ← 생성
├── types.ts
└── variants.ts
```

---

## 기본 스토리 구조

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Atoms/Button",
  component: Button,
  tags: ["autodocs"],
  parameters: {
    layout: "centered",
  },
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "secondary", "outline", "ghost", "destructive"],
      description: "버튼 스타일 변형",
    },
    size: {
      control: "select",
      options: ["sm", "md", "lg"],
      description: "버튼 크기",
    },
    disabled: {
      control: "boolean",
      description: "비활성화 상태",
    },
    onClick: {
      action: "clicked",
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

// 기본 스토리
export const Default: Story = {
  args: {
    children: "버튼",
    variant: "default",
    size: "md",
  },
};

// Variants
export const Secondary: Story = {
  args: {
    children: "Secondary",
    variant: "secondary",
  },
};

export const Outline: Story = {
  args: {
    children: "Outline",
    variant: "outline",
  },
};

export const Ghost: Story = {
  args: {
    children: "Ghost",
    variant: "ghost",
  },
};

export const Destructive: Story = {
  args: {
    children: "삭제",
    variant: "destructive",
  },
};

// Sizes
export const Small: Story = {
  args: {
    children: "Small",
    size: "sm",
  },
};

export const Large: Story = {
  args: {
    children: "Large",
    size: "lg",
  },
};

// States
export const Disabled: Story = {
  args: {
    children: "Disabled",
    disabled: true,
  },
};

export const Loading: Story = {
  args: {
    children: "Loading...",
    disabled: true,
  },
  render: (args) => (
    <Button {...args}>
      <Spinner className="mr-2 h-4 w-4 animate-spin" />
      Loading...
    </Button>
  ),
};

// With Icon
export const WithIcon: Story = {
  args: {
    children: "설정",
  },
  render: (args) => (
    <Button {...args}>
      <SettingsIcon className="mr-2 h-4 w-4" />
      설정
    </Button>
  ),
};
```

---

## 복합 컴포넌트 스토리 (Composition)

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Sidebar } from "./Sidebar";
import { Home, Settings, Users, LogOut } from "lucide-react";

const meta: Meta<typeof Sidebar> = {
  title: "Organisms/Sidebar",
  component: Sidebar,
  tags: ["autodocs"],
  parameters: {
    layout: "fullscreen",
  },
  decorators: [
    (Story) => (
      <div className="h-screen">
        <Story />
      </div>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof Sidebar>;

export const Default: Story = {
  render: () => (
    <Sidebar defaultCollapsed={false}>
      <Sidebar.Header title="Dashboard">
        <Sidebar.CollapseButton iconOnly />
      </Sidebar.Header>

      <Sidebar.Content>
        <Sidebar.Section label="메인">
          <Sidebar.Item icon={<Home />} active>홈</Sidebar.Item>
          <Sidebar.Item icon={<Users />}>사용자</Sidebar.Item>
          <Sidebar.Item icon={<Settings />}>설정</Sidebar.Item>
        </Sidebar.Section>
      </Sidebar.Content>

      <Sidebar.Footer>
        <Sidebar.Item icon={<LogOut />}>로그아웃</Sidebar.Item>
      </Sidebar.Footer>
    </Sidebar>
  ),
};

export const Collapsed: Story = {
  render: () => (
    <Sidebar defaultCollapsed>
      {/* ... */}
    </Sidebar>
  ),
};

export const WithBadge: Story = {
  render: () => (
    <Sidebar>
      <Sidebar.Content>
        <Sidebar.Item icon={<Bell />} badge={5}>
          알림
        </Sidebar.Item>
      </Sidebar.Content>
    </Sidebar>
  ),
};
```

---

## 폼 컴포넌트 스토리

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Input } from "./Input";

const meta: Meta<typeof Input> = {
  title: "Atoms/Input",
  component: Input,
  tags: ["autodocs"],
  argTypes: {
    type: {
      control: "select",
      options: ["text", "email", "password", "number"],
    },
    disabled: { control: "boolean" },
    error: { control: "text" },
  },
};

export default meta;
type Story = StoryObj<typeof Input>;

export const Default: Story = {
  args: {
    placeholder: "입력하세요",
  },
};

export const WithLabel: Story = {
  render: () => (
    <div className="space-y-2">
      <label htmlFor="email" className="text-sm font-medium">
        이메일
      </label>
      <Input id="email" type="email" placeholder="email@example.com" />
    </div>
  ),
};

export const WithError: Story = {
  args: {
    placeholder: "이메일",
    error: "유효한 이메일을 입력하세요",
    defaultValue: "invalid-email",
  },
  render: (args) => (
    <div className="space-y-2">
      <Input {...args} aria-invalid="true" />
      <p className="text-sm text-red-500">{args.error}</p>
    </div>
  ),
};

export const Password: Story = {
  args: {
    type: "password",
    placeholder: "비밀번호",
  },
};
```

---

## 인터랙티브 스토리

```tsx
import { useState } from "react";

export const Controlled: Story = {
  render: function ControlledStory() {
    const [value, setValue] = useState("");

    return (
      <div className="space-y-4">
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="입력하세요"
        />
        <p className="text-sm text-gray-500">
          입력값: {value || "(없음)"}
        </p>
      </div>
    );
  },
};

export const WithValidation: Story = {
  render: function ValidationStory() {
    const [value, setValue] = useState("");
    const [error, setError] = useState("");

    const validate = (v: string) => {
      if (!v) setError("필수 입력입니다");
      else if (v.length < 3) setError("3자 이상 입력하세요");
      else setError("");
    };

    return (
      <div className="space-y-2">
        <Input
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            validate(e.target.value);
          }}
          aria-invalid={!!error}
        />
        {error && <p className="text-sm text-red-500">{error}</p>}
      </div>
    );
  },
};
```

---

## 실행

```bash
# Storybook 실행
pnpm storybook

# 빌드
pnpm build-storybook
```

---

## 스토리 체크리스트

- [ ] 모든 variants가 스토리로 존재
- [ ] 모든 sizes가 스토리로 존재
- [ ] disabled/loading 상태 스토리
- [ ] 에러 상태 스토리 (폼 컴포넌트)
- [ ] 인터랙티브 예제 (필요시)
- [ ] autodocs 태그 추가
- [ ] argTypes 정의 (controls)
