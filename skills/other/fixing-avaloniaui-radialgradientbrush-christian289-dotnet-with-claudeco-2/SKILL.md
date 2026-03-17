---
name: fixing-avaloniaui-radialgradientbrush
description: Fixes RadialGradientBrush compatibility issues in AvaloniaUI due to Issue #19888 where GradientOrigin and Center must be identical. Use when converting WPF RadialGradientBrush to AvaloniaUI, resolving gradient rendering issues, or GradientOrigin/Center value mismatch problems.
---

# AvaloniaUI RadialGradientBrush 호환성 수정

## 문제 배경

AvaloniaUI에서 RadialGradientBrush는 WPF와 달리 GradientOrigin과 Center 값이 다르면 정상 동작하지 않음.

**관련 이슈**: [AvaloniaUI/Avalonia#19888](https://github.com/AvaloniaUI/Avalonia/issues/19888)

- RadialGradientBrush doesn't work when the GradientOrigin is different than the Center and the first Stop is Transparent

## 변환 절차

### 1. RadialGradientBrush 감지

WPF XAML에서 `<RadialGradientBrush>` 요소를 찾고 GradientOrigin과 Center 속성값을 비교.

### 2. 불일치 시 사용자에게 선택 요청

GradientOrigin ≠ Center인 경우 **반드시** 사용자에게 다음 선택지를 제시:

```
RadialGradientBrush의 GradientOrigin과 Center 값이 다릅니다.
- GradientOrigin: {현재값}
- Center: {현재값}

AvaloniaUI에서는 두 값이 동일해야 정상 동작합니다.
어느 쪽 값으로 통일하시겠습니까?

1. GradientOrigin 값으로 통일 → 결과: GradientOrigin="{GO값}" Center="{GO값}"
2. Center 값으로 통일 → 결과: GradientOrigin="{C값}" Center="{C값}"
```

### 3. 변환 예시

**WPF 원본**:

```xml
<RadialGradientBrush GradientOrigin="20%,20%" Center="28%,28%" RadiusX="75%" RadiusY="75%">
    <GradientStop Color="White" Offset="0"/>
    <GradientStop Color="Black" Offset="1"/>
</RadialGradientBrush>
```

**AvaloniaUI 변환 (GradientOrigin 선택 시)**:

```xml
<RadialGradientBrush GradientOrigin="20%,20%" Center="20%,20%" RadiusX="75%" RadiusY="75%">
    <GradientStop Color="White" Offset="0"/>
    <GradientStop Color="Black" Offset="1"/>
</RadialGradientBrush>
```

**AvaloniaUI 변환 (Center 선택 시)**:

```xml
<RadialGradientBrush GradientOrigin="28%,28%" Center="28%,28%" RadiusX="75%" RadiusY="75%">
    <GradientStop Color="White" Offset="0"/>
    <GradientStop Color="Black" Offset="1"/>
</RadialGradientBrush>
```

## 주의사항

- 사용자가 선택하기 전까지 **임의로 값을 변경하지 말 것**
- GradientOrigin 또는 Center 중 하나만 명시된 경우, 명시되지 않은 속성은 명시된 값으로 자동 설정
- GradientOrigin과 Center가 이미 동일한 경우 수정 불필요

```

```
