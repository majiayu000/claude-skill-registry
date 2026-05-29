---
name: literal-string
description: "C# Literal string을 const string으로 사전 정의하여 사용하는 패턴"
---

# Literal String 처리

C# 코드에서 Literal string을 처리하는 방법에 대한 가이드입니다.

## 프로젝트 구조

templates 폴더에 .NET 9 Console Application 예제가 포함되어 있습니다.

```
templates/
└── LiteralStringSample/                ← .NET 9 Console Application
    ├── Constants/
    │   ├── Messages.cs                 ← 일반 메시지 상수
    │   └── LogMessages.cs              ← 로그 메시지 상수
    ├── Program.cs                      ← Top-Level Statement 진입점
    ├── GlobalUsings.cs
    └── LiteralStringSample.csproj
```

## 규칙

**Literal string에 대해서는 가급적 `const string`으로 사전에 정의하여 사용할 것**

## 예시

### 좋은 예

```csharp
// 좋은 예
const string ErrorMessage = "오류가 발생했습니다.";
// An error has occurred.

if (condition)
    throw new Exception(ErrorMessage);
```

### 나쁜 예

```csharp
// 나쁜 예
if (condition)
    throw new Exception("오류가 발생했습니다.");
```

## Constants 클래스 구조

메시지 유형별로 static class로 분리하여 관리:

```csharp
// Constants/Messages.cs
namespace LiteralStringSample.Constants;

public static class Messages
{
    // 오류 메시지
    // Error messages
    public const string ErrorOccurred = "오류가 발생했습니다.";
    // An error has occurred.

    public const string InvalidInput = "잘못된 입력입니다.";
    // Invalid input.

    // 성공 메시지
    // Success messages
    public const string OperationSuccess = "작업이 성공적으로 완료되었습니다.";
    // Operation completed successfully.
}
```

```csharp
// Constants/LogMessages.cs
namespace LiteralStringSample.Constants;

public static class LogMessages
{
    // 정보 로그
    // Information logs
    public const string ApplicationStarted = "애플리케이션이 시작되었습니다.";
    // Application started.

    // 포맷 문자열
    // Format strings
    public const string UserLoggedIn = "사용자가 로그인했습니다: {0}";
    // User logged in: {0}
}
```

## 사용 예시

```csharp
using LiteralStringSample.Constants;

try
{
    if (string.IsNullOrEmpty(input))
    {
        throw new ArgumentException(Messages.InvalidInput);
    }

    Console.WriteLine(Messages.OperationSuccess);
}
catch (Exception)
{
    Console.WriteLine(Messages.ErrorOccurred);
}

// 포맷 문자열 사용
// Using format strings
Console.WriteLine(string.Format(LogMessages.UserLoggedIn, userName));
```

## 이유

1. **유지보수성**: 메시지 변경 시 한 곳만 수정
2. **재사용성**: 동일한 메시지를 여러 곳에서 사용 가능
3. **타입 안전성**: 컴파일 타임에 오타 확인
4. **성능**: 문자열 리터럴 중복 제거
5. **일관성**: 한글/영문 메시지 쌍으로 관리
