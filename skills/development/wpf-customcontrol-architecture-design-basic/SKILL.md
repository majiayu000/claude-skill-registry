---
name: wpf-customcontrol-architecture-design-basic
description: 'WPF CustomControl과 ResourceDictionary를 통한 Stand-Alone Control Style 작성'
---

# XAML 코드 작성 - WPF CustomControl

WPF에서 XAML 코드 작성 시 CustomControl과 ResourceDictionary 사용 가이드입니다.

## 프로젝트 구조

templates 폴더에 .NET 9 WPF 프로젝트 예제가 포함되어 있습니다.

```
templates/
├── WpfCustomControlSample.Controls/        ← WPF Custom Control Library
│   ├── Properties/
│   │   └── AssemblyInfo.cs
│   ├── Themes/
│   │   ├── Generic.xaml                    ← MergedDictionaries 허브
│   │   └── CustomButton.xaml               ← 개별 컨트롤 스타일
│   ├── CustomButton.cs
│   ├── GlobalUsings.cs
│   └── WpfCustomControlSample.Controls.csproj
└── WpfCustomControlSample.App/             ← WPF Application
    ├── Views/
    │   ├── MainWindow.xaml
    │   └── MainWindow.xaml.cs
    ├── App.xaml
    ├── App.xaml.cs
    ├── GlobalUsings.cs
    └── WpfCustomControlSample.App.csproj
```

## 기본 원칙

**XAML 코드를 생성할 때는 CustomControl을 사용하여 ResourceDictionary를 통한 Stand-Alone Control Style Resource를 사용**

**목적**: StaticResource 불러올 때 시점 고정 및 스타일 의존성 최소화

## WPF Custom Control Library 프로젝트 구조

### 프로젝트 생성 시 기본 구조

```
YourProject/
├── Dependencies/
├── Themes/
│   └── Generic.xaml
├── AssemblyInfo.cs
└── CustomControl1.cs
```

### 권장 프로젝트 구조로 재구성

```
YourProject/
├── Dependencies/
├── Properties/
│   └── AssemblyInfo.cs          ← 이동
├── Themes/
│   ├── Generic.xaml             ← MergedDictionaries 허브로 사용
│   ├── CustomButton.xaml        ← 개별 컨트롤 스타일
│   └── CustomTextBox.xaml       ← 개별 컨트롤 스타일
├── CustomButton.cs
└── CustomTextBox.cs
```

## 단계별 설정

### 1. Properties 폴더 생성 및 AssemblyInfo.cs 이동

- 프로젝트에 Properties 폴더 생성
- AssemblyInfo.cs를 Properties 폴더로 이동

### 2. Generic.xaml 구성 - MergedDictionaries 허브로 사용

Generic.xaml은 직접 스타일을 정의하지 않고, 개별 ResourceDictionary들을 병합하는 역할만 수행:

```xml
<!-- Themes/Generic.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
    <ResourceDictionary.MergedDictionaries>
        <ResourceDictionary Source="/YourProjectName;component/Themes/CustomButton.xaml" />
        <ResourceDictionary Source="/YourProjectName;component/Themes/CustomTextBox.xaml" />
    </ResourceDictionary.MergedDictionaries>
</ResourceDictionary>
```

### 3. 개별 컨트롤 스타일 정의

각 컨트롤마다 독립적인 XAML 파일에 스타일 정의:

```xml
<!-- Themes/CustomButton.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:local="clr-namespace:YourNamespace">

    <!-- 컨트롤 전용 리소스 정의 -->
    <SolidColorBrush x:Key="ButtonBackground" Color="#FF2D5460" />
    <SolidColorBrush x:Key="ButtonBackground_MouseOver" Color="#FF1D5460" />
    <SolidColorBrush x:Key="ButtonForeground" Color="#FFFFFFFF" />

    <!-- 컨트롤 스타일 정의 -->
    <Style TargetType="{x:Type local:CustomButton}">
        <Setter Property="Background" Value="{StaticResource ButtonBackground}" />
        <Setter Property="Foreground" Value="{StaticResource ButtonForeground}" />
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="{x:Type local:CustomButton}">
                    <Border Background="{TemplateBinding Background}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            BorderThickness="{TemplateBinding BorderThickness}">
                        <ContentPresenter HorizontalAlignment="Center"
                                        VerticalAlignment="Center"/>
                    </Border>
                    <ControlTemplate.Triggers>
                        <Trigger Property="IsMouseOver" Value="True">
                            <Setter Property="Background"
                                    Value="{StaticResource ButtonBackground_MouseOver}" />
                        </Trigger>
                    </ControlTemplate.Triggers>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
</ResourceDictionary>
```

## 실제 프로젝트 예시

### Generic.xaml 예시

```xml
<!-- Themes/Generic.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
    <ResourceDictionary.MergedDictionaries>
        <ResourceDictionary Source="/GameDataTool.Controls.Popup;component/Themes/GdtBranchSelectionPopup.xaml" />
    </ResourceDictionary.MergedDictionaries>
</ResourceDictionary>
```

### 개별 컨트롤 스타일 예시

```xml
<!-- Themes/GdtBranchSelectionPopup.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:local="clr-namespace:GameDataTool.Controls.Popup"
                    xmlns:ui="clr-namespace:GameDataTool.Controls.GdtCore.UI;assembly=GameDataTool.Controls.GdtCore"
                    xmlns:unit="clr-namespace:GameDataTool.Controls.GdtUnits;assembly=GameDataTool.Controls.GdtUnits">

    <SolidColorBrush x:Key="ApplyButtonBackground" Color="{DynamicResource Theme_PopupConfirmButtonColor}" />
    <SolidColorBrush x:Key="ApplyButtonBackground_MouseOver" Color="#FF1D5460" />
    <SolidColorBrush x:Key="ApplyButtonForeground" Color="{DynamicResource Theme_PopupConfirmButtonTextColor}" />
    <SolidColorBrush x:Key="CancelButtonBackground" Color="#FFE8EBED" />
    <SolidColorBrush x:Key="CancelButtonBackground_MouseOver" Color="#FFC9CDD2" />
    <SolidColorBrush x:Key="CancelButtonForeground" Color="#FF323334" />

    <Style TargetType="{x:Type local:GdtBranchSelectionPopup}">
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="{x:Type local:GdtBranchSelectionPopup}">
                    <Border Width="{DynamicResource BranchSelectionPopupWidthSize}"
                            Height="{DynamicResource BranchSelectionPopupHeightSize}"
                            Background="{TemplateBinding Background}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            BorderThickness="{TemplateBinding BorderThickness}">
                        <Grid>
                            <!-- 컨트롤 내용 -->
                        </Grid>
                    </Border>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
</ResourceDictionary>
```

## 장점

- 각 컨트롤의 스타일이 독립적인 파일로 분리되어 관리 용이
- Generic.xaml은 단순히 병합 역할만 수행하여 구조가 명확함
- StaticResource 참조 시점이 명확하고 의존성 최소화
- 팀 작업 시 파일 단위로 작업 분리 가능
