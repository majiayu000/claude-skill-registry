---
name: component-usage
description: 동구라미 앱 컴포넌트 라이브러리 사용 가이드. UI 컴포넌트 구현, 스타일 커스터마이징, 위젯 활용법 안내. Keywords: component, widget, ui, style, button, dialog, text field, chip, app bar, drawer
---

# 동구라미 컴포넌트 라이브러리

## 개요

동구라미 앱의 재사용 가능한 UI 컴포넌트 라이브러리입니다.
모든 컴포넌트는 `lib/widgets/{component_name}/` 폴더에 위치하며, 스타일 분리 패턴을 따릅니다.

## 컴포넌트 아키텍처

### 폴더 구조
```
lib/widgets/
├── {component_name}/
│   ├── {component_name}.dart        # 컴포넌트 구현
│   └── {component_name}_styles.dart # 스타일 클래스
```

### 스타일 패턴
```dart
// 1. 기본 스타일 사용
MyComponent()

// 2. 커스텀 스타일 사용
MyComponent(
  style: MyComponentStyle.defaultStyle.copyWith(
    backgroundColor: Colors.blue,
  ),
)
```

---

## 컴포넌트 목록

### 네비게이션 & 레이아웃

| 컴포넌트 | 설명 | 문서 |
|----------|------|------|
| AppBar | 메인 화면용 커스텀 앱바 | [app-bar.md](app-bar.md) |
| DetailAppBar | 상세 화면용 앱바 (뒤로가기 + 제목) | [detail-app-bar.md](detail-app-bar.md) |
| DrawerMenu | 드로어 메뉴 (로그인/비로그인 통합) | [drawer-menu.md](drawer-menu.md) |
| DrawerItem | 드로어 메뉴 아이템 | [drawer-item.md](drawer-item.md) |
| DrawerEventItem | 드로어 이벤트 아이템 | [drawer-event-item.md](drawer-event-item.md) |

### 필터 & 선택

| 컴포넌트 | 설명 | 문서 |
|----------|------|------|
| FilterTabBar | 전체/모집중 필터 탭 | [filter-tab-bar.md](filter-tab-bar.md) |
| CategoryFilterButton | 카테고리 필터 버튼 | [category-filter-button.md](category-filter-button.md) |
| CategoryPicker | 카테고리 선택 다이얼로그 | [category-picker.md](category-picker.md) |
| RemovableChip | 삭제 가능한 칩 | [removable-chip.md](removable-chip.md) |
| SelectedCategoryChipList | 선택된 카테고리 칩 목록 | [selected-category-chip-list.md](selected-category-chip-list.md) |

### 입력 필드

| 컴포넌트 | 설명 | 문서 |
|----------|------|------|
| RoundedTextField | 둥근 텍스트 필드 | [rounded-text-field.md](rounded-text-field.md) |
| RoundedEmailField | 둥근 이메일 필드 | [rounded-email-field.md](rounded-email-field.md) |
| EmailTextField | 이메일 텍스트 필드 | [email-text-field.md](email-text-field.md) |
| EmailTextFieldWithButton | 버튼 포함 이메일 필드 | [email-text-field-with-button.md](email-text-field-with-button.md) |
| RoundedDropdown | 둥근 드롭다운 | [rounded-dropdown.md](rounded-dropdown.md) |

### 다이얼로그 & 오버레이

| 컴포넌트 | 설명 | 문서 |
|----------|------|------|
| AlertTextDialog | 알림 다이얼로그 | [alert-text-dialog.md](alert-text-dialog.md) |
| CircleCertificateDialog | 인증 코드 다이얼로그 | [circle-certificate-dialog.md](circle-certificate-dialog.md) |
| MajorPickerDialog | 학과 선택 다이얼로그 | [major-picker-dialog.md](major-picker-dialog.md) |
| PolicyDialog | 약관 다이얼로그 | [policy-dialog.md](policy-dialog.md) |
| NotificationOverlay | 알림 오버레이 | [notification-overlay.md](notification-overlay.md) |
| CircleDetailOverlay | 동아리 상세 오버레이 | [circle-detail-overlay.md](circle-detail-overlay.md) |

### 동아리 관련

| 컴포넌트 | 설명 | 문서 |
|----------|------|------|
| CircleList | 동아리 목록 | [circle-list.md](circle-list.md) |
| CircleItem | 동아리 아이템 | [circle-item.md](circle-item.md) |
| CircleGroup | 동아리 그룹 | [circle-group.md](circle-group.md) |
| CircleDetailItem | 동아리 상세 아이템 | [circle-detail-item.md](circle-detail-item.md) |

### 기타

| 컴포넌트 | 설명 | 문서 |
|----------|------|------|
| TextFontWidget | 텍스트 폰트 헬퍼 | [text-font-widget.md](text-font-widget.md) |
| NoticeList | 공지사항 목록 | [notice-list.md](notice-list.md) |
| CloudMessaging | FCM 메시징 위젯 | [cloud-messaging.md](cloud-messaging.md) |

---

## 테마 색상

| 용도 | 색상 코드 | 설명 |
|------|-----------|------|
| Primary | `#FFB052` | 브랜드 주 색상 (오렌지) |
| Primary Dark | `#FF9A21` | 브랜드 진한 색상 |
| Background | `#F0F2F5` | 배경 회색 |
| Text Primary | `#000000` | 주 텍스트 색상 |
| Text Secondary | `#767676` | 보조 텍스트 색상 |
| Text Tertiary | `#A8A8A8` | 연한 텍스트 색상 |
| Border | `#DBDBDB` | 기본 테두리 색상 |
| Divider | `#CECECE` | 구분선 색상 |

---

## 새 컴포넌트 추가 가이드

### 1. 폴더 생성
```bash
mkdir lib/widgets/{new_component}
```

### 2. 스타일 파일 생성
```dart
// lib/widgets/{new_component}/{new_component}_styles.dart
import 'package:flutter/material.dart';

class NewComponentStyle {
  final Color backgroundColor;

  const NewComponentStyle({
    this.backgroundColor = Colors.white,
  });

  static const NewComponentStyle defaultStyle = NewComponentStyle();

  NewComponentStyle copyWith({Color? backgroundColor}) {
    return NewComponentStyle(
      backgroundColor: backgroundColor ?? this.backgroundColor,
    );
  }
}
```

### 3. 컴포넌트 파일 생성
```dart
// lib/widgets/{new_component}/{new_component}.dart
import 'package:flutter/material.dart';
import '{new_component}_styles.dart';

class NewComponent extends StatelessWidget {
  final NewComponentStyle style;

  const NewComponent({
    super.key,
    this.style = NewComponentStyle.defaultStyle,
  });

  @override
  Widget build(BuildContext context) {
    return Container(color: style.backgroundColor);
  }
}
```
