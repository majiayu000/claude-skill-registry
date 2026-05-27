---
name: designing-wpf-customcontrol-architecture
description: "Designs stand-alone control styles using WPF CustomControl and ResourceDictionary. Use when creating reusable custom controls or organizing control themes in Generic.xaml."
---

# XAML Code Writing - WPF CustomControl

A guide for using CustomControl and ResourceDictionary when writing XAML code in WPF.

## Project Structure

The templates folder contains a .NET 9 WPF project example.

```
templates/
├── WpfCustomControlSample.Controls/        ← WPF Custom Control Library
│   ├── Properties/
│   │   └── AssemblyInfo.cs
│   ├── Themes/
│   │   ├── Generic.xaml                    ← MergedDictionaries hub
│   │   └── CustomButton.xaml               ← Individual control style
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

## Basic Principles

**When generating XAML code, use CustomControl with Stand-Alone Control Style Resource through ResourceDictionary**

**Purpose**: Fix the timing of StaticResource loading and minimize style dependencies

## WPF Custom Control Library Project Structure

### Default Structure When Creating Project

```
YourProject/
├── Dependencies/
├── Themes/
│   └── Generic.xaml
├── AssemblyInfo.cs
└── CustomControl1.cs
```

### Restructure to Recommended Project Structure

```
YourProject/
├── Dependencies/
├── Properties/
│   └── AssemblyInfo.cs          ← Moved
├── Themes/
│   ├── Generic.xaml             ← Use as MergedDictionaries hub
│   ├── CustomButton.xaml        ← Individual control style
│   └── CustomTextBox.xaml       ← Individual control style
├── CustomButton.cs
└── CustomTextBox.cs
```

## Step-by-Step Setup

### 1. Create Properties Folder and Move AssemblyInfo.cs

- Create Properties folder in the project
- Move AssemblyInfo.cs to the Properties folder

### 2. Configure Generic.xaml - Use as MergedDictionaries Hub

Generic.xaml does not define styles directly; it only performs the role of merging individual ResourceDictionaries:

```xml
<!-- Themes/Generic.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
    <ResourceDictionary.MergedDictionaries>
        <ResourceDictionary Source="/YourProjectName;component/Themes/CustomButton.xaml" />
        <ResourceDictionary Source="/YourProjectName;component/Themes/CustomTextBox.xaml" />
    </ResourceDictionary.MergedDictionaries>
</ResourceDictionary>
```

### 3. Define Individual Control Styles

Define styles in independent XAML files for each control:

```xml
<!-- Themes/CustomButton.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:local="clr-namespace:YourNamespace">

    <!-- Control-specific resource definitions -->
    <SolidColorBrush x:Key="ButtonBackground" Color="#FF2D5460" />
    <SolidColorBrush x:Key="ButtonBackground_MouseOver" Color="#FF1D5460" />
    <SolidColorBrush x:Key="ButtonForeground" Color="#FFFFFFFF" />

    <!-- Control style definition -->
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

## Real Project Example

### Generic.xaml Example

```xml
<!-- Themes/Generic.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
    <ResourceDictionary.MergedDictionaries>
        <ResourceDictionary Source="/GameDataTool.Controls.Popup;component/Themes/GdtBranchSelectionPopup.xaml" />
    </ResourceDictionary.MergedDictionaries>
</ResourceDictionary>
```

### Individual Control Style Example

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
                            <!-- Control content -->
                        </Grid>
                    </Border>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
</ResourceDictionary>
```

## Advantages

- Each control's style is separated into independent files for easier management
- Generic.xaml simply performs a merging role, making the structure clear
- StaticResource reference timing is clear and dependencies are minimized
- Work can be split by file for team collaboration

