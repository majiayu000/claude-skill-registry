---
name: wpf-popup-focus
description: 'WPF Popup 컨트롤의 포커스 관리 패턴 (PreviewMouseDown 이벤트 활용)'
---

# 5.7 Popup 컨트롤 사용 시 주의사항

WPF에서 Popup 컨트롤은 WPF Application에 포커스가 있을 때만 정상적으로 동작합니다. 다른 애플리케이션으로 포커스가 이동한 상태에서는 Popup이 제대로 표시되지 않거나 동작하지 않을 수 있습니다.

#### 5.7.1 포커스 관리 패턴

WPF에서 Popup 컨트롤을 사용할 경우, **PreviewMouseDown 이벤트를 통해 포커스를 강제로 가져와야 합니다.**

## 프로젝트 구조

templates 폴더에 .NET 9 WPF 프로젝트 예제가 포함되어 있습니다.

```
templates/
└── WpfPopupSample.App/                  ← WPF Application
    ├── Views/
    │   ├── MainWindow.xaml
    │   └── MainWindow.xaml.cs           ← 포커스 관리 패턴 구현
    ├── App.xaml
    ├── App.xaml.cs
    ├── GlobalUsings.cs
    └── WpfPopupSample.App.csproj
```

#### 5.7.2 핵심 원칙

- **Popup 동작 조건**: WPF Application에 포커스가 있을 때만 동작
- **PreviewMouseDown 이벤트**: 마우스 클릭 시 포커스 상태 체크
- **IsKeyboardFocused 체크**: 키보드 포커스 여부 확인
- **Activate() 호출**: 포커스가 없으면 윈도우 활성화하여 포커스 복원
- **UserControl 경우**: `Window.GetWindow(this)?.Activate()`로 부모 윈도우 활성화

#### 5.7.3 왜 필요한가?

1. **다른 앱으로 포커스 이동**: 사용자가 다른 애플리케이션을 클릭했다가 다시 돌아올 때
2. **백그라운드 실행**: WPF 앱이 백그라운드에 있을 때 Popup 동작 보장
3. **사용자 경험**: Popup이 항상 예상대로 동작하도록 보장

**⚠️ 주의사항:**

- Popup을 사용하는 모든 Window에 이 패턴을 적용해야 함

#### 5.7.4 참고 자료

- [WPF Popup 포커스 이슈 - .NET Dev 포럼](https://forum.dotnetdev.kr/t/wpf-popup/8296)
