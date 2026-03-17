---
name: flutter-init
description: Use when user wants to create a new Flutter project (Todo/Habit/Note/Expense/Custom domain) with Clean Architecture, Riverpod 3.0, Drift, and modern Flutter stack
---

# Flutter Init Skill

도메인 기반 Flutter 프로젝트를 생성하고 현대적인 아키텍처로 자동 설정합니다.
Todo, Habit, Note, Expense 또는 Custom 도메인을 선택하여 Clean Architecture 기반의 완전한 CRUD 앱을 즉시 생성할 수 있습니다.

## Quick Start

스킬 실행 시 다음 정보를 입력받습니다:
- 폴더명 (예: my_habit_app)
- 프로젝트명/패키지명 (예: habit_app)
- 도메인 선택 (Todo/Habit/Note/Expense/Custom)
- 스택 프리셋 (Minimal/Essential/Full Stack/Custom)

그 후 자동으로 다음 단계가 실행됩니다:

```bash
# 1. 프로젝트 생성 (Android/Kotlin, iOS/Swift)
flutter create --platforms android,ios --android-language kotlin --org com.example [폴더명]

# 2. 패키지 설치
flutter pub get

# 3. 도메인별 Clean Architecture 코드 자동 생성
# - domain/entities/[domain].dart (Freezed 엔티티)
# - data/datasources/local/app_database.dart (Drift 테이블)
# - data/repositories/[domain]_repository_impl.dart (Repository 구현)
# - presentation/providers/[domain]_providers.dart (Riverpod 3.0)
# - presentation/screens/* (List/Detail/Form 화면)

# 4. 코드 생성 (Freezed, Drift, JSON Serializable)
dart run build_runner build --delete-conflicting-outputs

# 5. 코드 검증 및 오류 자동 수정 (필수)
flutter analyze

# 6. 앱 실행
flutter run
```

## Task Instructions

**IMPORTANT**: 이 스킬은 대화형으로 진행됩니다.

### Step 1: 도메인 및 프로젝트 설정 질문

**먼저 사용자에게 이렇게 물어보세요:**

"Flutter 앱을 생성합니다. 다음 정보를 알려주세요:

**1. 도메인(엔티티) 선택**

어떤 도메인의 앱을 만드시겠습니까?

**A) Todo (할 일 관리)**
- 필드: title, description, isCompleted, createdAt, completedAt
- 기능: CRUD, 필터링(전체/진행중/완료), 체크박스 토글

**B) Habit (습관 트래커)**
- 필드: name, description, frequency(daily/weekly/monthly), streak, lastCompletedAt, goal, isActive
- 기능: CRUD, 연속 기록 추적, 목표 달성률, 완료 체크

**C) Note (메모)**
- 필드: title, content, tags, isPinned, createdAt, updatedAt
- 기능: CRUD, 태그 필터링, 고정 메모, 검색

**D) Expense (지출 관리)**
- 필드: amount, category, description, date, paymentMethod
- 기능: CRUD, 카테고리별 집계, 월별 통계, 필터링

**E) Custom (직접 정의)**
- 엔티티명과 필드를 직접 입력

**2. 프로젝트 정보**
- **폴더명**: 프로젝트를 생성할 폴더 이름 (기본값: [도메인]_app, 예: habit_app)
  - 이 폴더에 Flutter 프로젝트가 생성됩니다
- **프로젝트명 (패키지명)**: Flutter 패키지 이름 (기본값: 폴더명과 동일)
  - pubspec.yaml의 name 필드에 사용됩니다
  - import 문에 사용됩니다 (예: package:habit_app/...)
- **조직명**: (기본값: com.example)
  - Android/iOS 패키지 식별자에 사용됩니다 (예: com.example.habit_app)

**3. 스택 프리셋 선택**

다음 중 하나를 선택해주세요:

**A) Essential (권장)**
- ✅ GoRouter (타입 안전한 라우팅)
- ✅ SharedPreferences (로컬 설정 저장)
- ✅ FPDart (함수형 에러 핸들링)
- ✅ Google Fonts
- ✅ FluentUI Icons
- ❌ Auth 시스템 제외
- ❌ Responsive Utils 제외

**B) Minimal (가장 단순)**
- ❌ GoRouter (기본 Navigator 사용)
- ✅ SharedPreferences
- ❌ FPDart 제외
- ❌ Google Fonts 제외
- ✅ 기본 FluentUI Icons
- ❌ Auth 시스템 제외
- ❌ Responsive Utils 제외

**C) Full Stack (모든 기능)**
- ✅ GoRouter
- ✅ SharedPreferences
- ✅ FPDart (함수형 에러 핸들링)
- ✅ Google Fonts
- ✅ Responsive Utils
- ✅ FluentUI Icons
- ✅ Auth 시스템 (Login/Register) - 선택 도메인에 따라

**D) Custom (직접 선택)**
- 각 기능을 개별적으로 선택

어떤 도메인과 프리셋을 선택하시겠습니까? (도메인: A/B/C/D/E, 프리셋: A/B/C/D)"

### Step 2: Custom 선택 시 추가 질문

#### 2-1. Custom 도메인 (E) 선택 시:

1. **엔티티명**: 엔티티 이름을 입력하세요 (예: Task, Event, Book)
2. **필드 정의**: 각 필드를 입력하세요 (형식: 필드명:타입, 예: title:String, amount:double, isActive:bool)
   - 지원 타입: String, int, double, bool, DateTime
   - createdAt, updatedAt은 자동 추가됨
3. **주요 기능**: 필터링/정렬 기준이 될 필드를 선택하세요

#### 2-2. Custom 스택 프리셋 (D) 선택 시:

다음 질문들을 순차적으로 하세요:

1. **네비게이션**: GoRouter를 사용하시겠습니까? (예/아니오)
2. **에러 핸들링**: FPDart를 사용하시겠습니까? (예/아니오)
3. **UI**: Google Fonts를 사용하시겠습니까? (예/아니오)
4. **반응형**: Responsive Utils를 포함하시겠습니까? (예/아니오)
5. **인증 시스템**: Auth 시스템을 포함하시겠습니까? (예/아니오)

### Step 3: 선택된 도메인과 스택에 따라 프로젝트 생성

1. **Flutter 프로젝트 생성**:
   - 사용자가 지정한 **폴더명**으로 프로젝트 생성
   - 명령어: `flutter create --platforms android,ios --android-language kotlin --org [조직명] [폴더명]`
   - 예: `flutter create --platforms android,ios --android-language kotlin --org com.example my_habit_app`
   - 폴더명과 프로젝트명(패키지명)이 다른 경우, 생성 후 pubspec.yaml의 `name` 필드를 수정
2. **Kotlin DSL 확인** (최신 Flutter는 자동으로 Kotlin DSL 사용)
3. **선택된 패키지 설치**: `pubspec.yaml` 업데이트 후 `flutter pub get`
4. **폴더 구조 생성**: Clean Architecture (core, data, domain, presentation)
5. **도메인별 보일러플레이트 생성**:

   **A) Todo**: title, description, isCompleted, createdAt, completedAt
   - Repository: getTodos, createTodo, updateTodo, toggleCompletion, deleteTodo
   - Providers: filteredTodosProvider (all/pending/completed)
   - UI: TodoListScreen (필터링), TodoDetailScreen, TodoFormDialog

   **B) Habit**: name, description, frequency, streak, lastCompletedAt, goal, isActive
   - Repository: getHabits, createHabit, updateHabit, completeHabit, deleteHabit
   - Providers: filteredHabitsProvider (active/inactive), habitStatsProvider
   - UI: HabitListScreen (통계), HabitDetailScreen, HabitFormDialog

   **C) Note**: title, content, tags, isPinned, createdAt, updatedAt
   - Repository: getNotes, createNote, updateNote, togglePin, deleteNote
   - Providers: filteredNotesProvider (pinned/all/byTag), searchProvider
   - UI: NoteListScreen (검색/태그), NoteDetailScreen, NoteFormDialog

   **D) Expense**: amount, category, description, date, paymentMethod
   - Repository: getExpenses, createExpense, updateExpense, deleteExpense
   - Providers: expensesByCategory, monthlyStats, filteredExpenses
   - UI: ExpenseListScreen (통계), ExpenseDetailScreen, ExpenseFormDialog

   **E) Custom**: 사용자 정의 필드
   - Repository: 기본 CRUD 메서드
   - Providers: 기본 list provider
   - UI: 기본 List/Detail/Form 화면

6. **설정 파일 생성** (라우팅, 스토리지, 다국어 등)
7. **Android 설정 업데이트** (CRITICAL for flutter_local_notifications):
   - `android/app/build.gradle.kts`에 core library desugaring 활성화:
     ```kotlin
     android {
         compileOptions {
             sourceCompatibility = JavaVersion.VERSION_11
             targetCompatibility = JavaVersion.VERSION_11
             isCoreLibraryDesugaringEnabled = true  // 추가
         }
     }
     dependencies {
         coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.0.4")  // 추가
     }
     ```
8. **코드 생성**: `dart run build_runner build --delete-conflicting-outputs`
9. **코드 검증 및 오류 수정**:

   a. `flutter analyze` 실행

   b. 발견된 오류 수정:
   - **Freezed 3.0 호환성** (CRITICAL): 모든 Freezed 엔티티는 `sealed class` 사용
     - ❌ `class User with _$User`
     - ✅ `sealed class User with _$User`
   - **테마 설정**: `CardTheme` → `CardThemeData` 사용 (deprecated)
   - **API Client Map 타입**: `Map<String, dynamic>` 반환 시 생성 코드 검증
     - retrofit_generator가 생성한 `dynamic.fromJson` 에러 발생 시 수정 필요
   - **import 경로 수정**: 모든 상대 경로를 `package:` 형식으로 변경
     - 예: `import '../../domain/entities/todo.dart';` → `import 'package:todo_app/domain/entities/todo.dart';`
   - **패키지 의존성 확인**: 누락된 패키지 추가 (예: `shared_preferences`)
   - **Riverpod 3.0 호환성**: `StateNotifier` → `Notifier`, `StateProvider` → `NotifierProvider`
   - **FluentUI 아이콘 이름 확인**: 존재하지 않는 아이콘은 대체
   - **타입 안전성**: switch expression 사용, null safety 준수

   c. 재검증: 모든 error 레벨 오류가 없을 때까지 반복

   d. 목표: `flutter analyze` 결과가 "0-1 issues found" (info 레벨만 허용)

   **✅ CRITICAL**: 이 단계는 필수입니다. 모든 error를 제거해야 다음 단계로 진행할 수 있습니다.

### Step 4: 최종 검증 및 안내

**✅ CRITICAL**: 이 단계는 프로젝트 완료의 필수 조건입니다.

1. **최종 분석 실행**:
   ```bash
   flutter analyze
   ```

2. **성공 기준**:
   - ✅ **성공 예시**:
     ```
     Analyzing todo_app...
     No issues found!
     ```
     또는
     ```
     Analyzing todo_app...
     1 issue found. (ran in 2.3s)
     info • Prefer using lowerCamelCase for constant names • lib/core/constants.dart:5:7 • constant_identifier_names
     ```

   - ❌ **실패 예시** (error가 있으면 반드시 수정):
     ```
     error • Target of URI doesn't exist: 'package:...' • lib/main.dart:5:8 • uri_does_not_exist
     error • The getter 'xyz' isn't defined for the type 'ABC' • lib/presentation/screens/home.dart:42:15
     ```

3. **검증 결과 요약** (성공 시):
   ```
   ✅ Flutter 프로젝트 생성 완료!
   ✅ 코드 생성 완료 (Freezed, Drift, JSON Serializable)
   ✅ Flutter analyze 통과 (0-1 issues found, info 레벨만)
   ✅ 모든 패키지 설치 완료
   ```

4. **프로젝트 정보 제공**:
   - **폴더명**: [사용자 입력값] (예: my_habit_app)
   - **프로젝트명 (패키지명)**: [사용자 입력값] (예: habit_app)
   - **조직명**: [사용자 입력값] (예: com.example)
   - **도메인**: [선택된 도메인] (Todo/Habit/Note/Expense/Custom)
   - **선택된 스택**: [프리셋명] (GoRouter, Drift, FPDart 등)
   - **주요 기능**: [도메인] CRUD, 다국어 지원, 로컬 저장소 등
   - **생성된 파일**: XX개 Dart 파일 (core, data, domain, presentation)

5. **실행 방법 안내**:
   ```bash
   cd [폴더명]
   flutter run
   ```

6. **다음 단계 제안** (선택사항, 도메인별):
   - **Todo**: 항목 추가/수정/삭제, 필터링(전체/진행중/완료), 완료 토글
   - **Habit**: 습관 기록, 연속 기록 확인, 목표 달성률, 통계 확인
   - **Note**: 메모 작성/편집, 태그 추가, 고정 메모, 검색
   - **Expense**: 지출 기록, 카테고리별 통계, 월별 집계, 필터링
   - **공통**: 언어 전환 (영어 ↔ 한국어), 다크/라이트 테마 전환

## Core Principles

- **Repository 패턴**: 데이터 레이어와 도메인 레이어 분리
- **의존성 주입**: Riverpod 3.x를 통한 의존성 관리
- **불변성**: Freezed로 불변 모델 생성
- **다국어 지원**: Easy Localization으로 i18n
- **모던 UI**: FluentUI Icons 사용

## Reference Files

[references/setup-guide.md](references/setup-guide.md) - 완전한 가이드
- 기본 셋업 (도메인별 CRUD, 다국어, FluentUI Icons)
- 선택 옵션: GoRouter, Auth, FPDart, Google Fonts, Responsive Utils, 패키지 업데이트

## Notes

- **대화형 스킬**: 사용자에게 도메인과 프리셋 선택을 통해 맞춤형 앱 구성
- **도메인 지원**: Todo, Habit, Note, Expense, Custom (사용자 정의)
- **프리셋 제공**: Full Stack, Essential, Minimal, Custom
- **선택 가능 기능**: GoRouter, Auth, FPDart, Google Fonts, Responsive Utils
- **기본 포함**: Riverpod 3.x, Easy Localization, FluentUI Icons, Drift, Dio, SharedPreferences
- **다국어**: 영어/한국어 (확장 가능)
- **플랫폼**: Android/Kotlin, iOS/Swift (웹/윈도우/리눅스 제외)
- **품질 보증**:
  - 모든 프로젝트는 `flutter analyze` 통과 필수
  - package: imports 스타일 준수
  - 타입 안전성 보장
  - 코드 생성 자동화
  - 도메인별 최적화된 UI/UX

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual
-->
