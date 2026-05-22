---
name: test-async-guardian
description: "Flutter/Dart 測試異步資源管理守護者。用於：(1) 診斷測試卡住問題，(2) 審查測試代碼中的異步資源清理，(3) 提供 tearDown 最佳實踐，(4) 掃描潛在的資源洩漏風險。觸發場景：測試卡住、撰寫新測試、Code Review 測試代碼、執行 flutter test 前自動掃描。"
---

# Test Async Guardian

測試異步資源管理守護者 - 防止測試因未清理的異步資源而卡住。

## 問題背景

Dart/Flutter 測試框架會等待所有未完成的 Future 才結束測試。如果測試啟動了長延遲的異步操作但沒有正確清理，測試會無限期卡住。

## 導致測試阻塞的異步資源類型

| 資源類型 | 問題描述 | 清理方法 |
|---------|---------|---------|
| **未完成的 Future** | 長延遲異步操作沒有等待完成或取消 | `service.clearAllQueries()` 或 `service.dispose()` |
| **Timer.periodic** | 週期性定時器未取消 | `timer.cancel()` |
| **StreamController** | 廣播流未關閉 | `controller.close()` |
| **Completer** | Completer 未完成 | `completer.complete()` |
| **網路依賴** | flutter test 啟動時需要 pub.dev DNS 解析 | 確保網路連線，或使用離線模式 |
| **testWidgets 時間** | Future.delayed 在 widget 測試中無法自動推進 | 呼叫 `tester.pump()` 或改用 `test()` |
| **MCP run_tests 大量輸出** | 全部測試輸出量過大導致 MCP 卡住 | 使用 paths 參數或改用 flutter test |

## 正確的 tearDown 模式

### 模式 A：服務清理

```dart
late BookQueryService bookQueryService;

setUp(() {
  bookQueryService = BookQueryService(apiService: mockApiService);
});

tearDown(() {
  bookQueryService.clearAllQueries();  // 清理未完成的查詢
});
```

### 模式 B：Mock 狀態重置

```dart
late MockSearchBookViewModelForBatch mockSearchViewModel;

tearDown(() {
  mockSearchViewModel.setSlowSearch(false);  // 重置慢速模式
  mockBookRepository.setSlowQuery(false);
  mockBatchEnrichBooksUseCase.setFastExecution(true);
  container.dispose();
});
```

### 模式 C：StreamController 清理

```dart
final StreamController<EnrichmentProgress> _progressController =
    StreamController<EnrichmentProgress>.broadcast();

void dispose() {
  _progressController.close();
}
```

### 模式 D：Timer 清理

```dart
Timer? _memoryMonitorTimer;

void startMonitoring() {
  _memoryMonitorTimer = Timer.periodic(interval, (_) {
    captureSnapshot();
  });
}

void dispose() {
  _memoryMonitorTimer?.cancel();
  _memoryMonitorTimer = null;
}
```

## 危險模式檢測

### 危險模式 1：長延遲沒有清理

```dart
// ❌ 危險：10 秒延遲，測試只等 10ms
when(mockApiService.queryByIsbn('xxx'))
    .thenAnswer((_) async {
  await Future.delayed(const Duration(seconds: 10));
  return data;
});
await Future.delayed(const Duration(milliseconds: 10));
// 測試結束，但 Future 還在運行！
```

**修復**：添加 tearDown 清理或縮短延遲時間。

### 危險模式 2：週期性定時器沒有取消

```dart
// ❌ 危險：Timer.periodic 未在 tearDown 中取消
Timer.periodic(Duration(seconds: 1), (timer) {
  captureSnapshot();
});
```

**修復**：保存 Timer 引用並在 dispose/tearDown 中取消。

### 危險模式 3：StreamController 未關閉

```dart
// ❌ 危險：broadcast StreamController 未關閉
final controller = StreamController<Event>.broadcast();
// 測試結束但 controller 仍在監聽
```

**修復**：在 dispose 方法中調用 `controller.close()`。

### 危險模式 4：網路斷線導致測試卡住

```bash
# ❌ 危險：網路斷線時 flutter test 卡在 Resolving dependencies
Resolving dependencies...
ClientException with SocketException: Failed host lookup: 'pub.dev'
```

**症狀**：
- 測試卡在 "Resolving dependencies..."
- 錯誤訊息包含 "Failed host lookup: 'pub.dev'"

**修復**：確認網路連線後重新執行測試。

### 危險模式 5：testWidgets 中 Future.delayed 永不完成

```dart
// ❌ 危險：testWidgets 使用虛擬時鐘，Future.delayed 永不完成
testWidgets('事件測試', (tester) async {
  await Future.delayed(Duration(milliseconds: 50));  // 永遠等待！
  expect(events.length, 3);
});
```

**症狀**：
- 測試卡在特定 testWidgets 測試
- 測試中有 Future.delayed 但沒有 tester.pump()

**修復選項**：

```dart
// 選項 A: 添加 pump（需要 Widget 環境時）
testWidgets('事件測試', (tester) async {
  await Future.delayed(Duration(milliseconds: 50));
  await tester.pump(Duration(milliseconds: 50));  // 推進虛擬時間
  expect(events.length, 3);
});

// 選項 B: 改用 test（推薦，純邏輯測試時）
test('事件測試', () async {
  await Future.delayed(Duration(milliseconds: 50));  // 正常執行
  expect(events.length, 3);
});
```

**判斷標準**：
- 需要 Widget 樹？→ 用 testWidgets + pump
- 只驗證邏輯？→ 用 test

### 危險模式 6：MCP run_tests 執行全部測試卡住

```bash
# ❌ 危險：不指定 paths 執行全部測試會卡住 20+ 分鐘
mcp__dart__run_tests (無 paths 參數)
```

**症狀**：
- 使用 MCP run_tests 執行全部測試時卡住超過 20 分鐘
- 但 `flutter test` 直接執行約 85 秒完成
- MCP 工具無回應

**根本原因**：
- MCP run_tests 是實驗性功能
- 處理大量測試輸出時存在效能問題
- 全部測試輸出量過大導致 MCP 無法處理

**修復**：

```bash
# ✅ 正確 - 必須指定 paths 參數限制測試範圍
mcp__dart__run_tests(roots: [{"root": "file:///path", "paths": ["test/domains/"]}])
mcp__dart__run_tests(roots: [{"root": "file:///path", "paths": ["test/unit/core/"]}])

# ✅ 推薦 - 全量測試使用 Bash（最穩定）
flutter test --reporter compact
./.claude/hooks/test-summary.sh
```

**適用場景對照**：
| 測試範圍 | MCP run_tests | flutter test |
|---------|---------------|--------------|
| 單一檔案 | ✅ 適用 | ✅ 適用 |
| 單一目錄 (paths) | ✅ 適用 | ✅ 適用 |
| 全部測試 | ❌ 禁止 | ✅ 推薦 |

## 掃描腳本使用

### 命令行模式

```bash
# 掃描單個測試檔案（嚴格模式）
uv run .claude/skills/test-async-guardian/scripts/async_resource_scanner.py \
  test/unit/domains/scanner/book_query_service_test.dart

# 掃描整個測試目錄
uv run .claude/skills/test-async-guardian/scripts/async_resource_scanner.py \
  test/unit/ --recursive

# 警告模式（不阻止執行）
uv run .claude/skills/test-async-guardian/scripts/async_resource_scanner.py \
  test/unit/ --warn-only
```

### Hook 模式

腳本已整合為 PreToolUse Hook，在執行 `flutter test` 或 `dart test` 前自動觸發掃描。

## 診斷流程

當測試卡住時：

0. **檢查是否使用 MCP run_tests 執行全部測試**
   ```bash
   # 如果使用 mcp__dart__run_tests 不指定 paths，會卡住 20+ 分鐘
   # 解決方案：改用 flutter test 或指定 paths 參數

   # ✅ 正確方式
   flutter test --reporter compact
   mcp__dart__run_tests(paths: ["test/domains/"])
   ```

1. **檢查網路連線**
   ```bash
   # 確認網路連線正常（排除 pub.dev DNS 問題）
   ping -c 1 pub.dev || echo "網路可能有問題"
   ```

2. **識別卡住的測試**
   ```bash
   # 使用 timeout 限制測試時間（macOS 需要安裝 coreutils）
   timeout 30 flutter test test/unit/path/to/test.dart
   # 或使用背景程序方式
   flutter test test/unit/path/to/test.dart & sleep 30 && pkill -f flutter_tester
   ```

3. **掃描異步資源問題**
   ```bash
   uv run .claude/skills/test-async-guardian/scripts/async_resource_scanner.py \
     test/unit/path/to/test.dart
   ```

4. **檢查報告中的問題**
   - 長延遲（>= 5 秒）
   - 缺少 tearDown
   - Timer.periodic 未取消
   - StreamController 未關閉
   - MCP run_tests 無 paths 參數

5. **應用修復建議**

## Resources

### scripts/

- `async_resource_scanner.py` - 異步資源掃描腳本，支援嚴格模式和 Hook 模式

### references/

- `async-cleanup-patterns.md` - 清理模式參考和真實案例

### hooks/

- `pre-test-scan.py` - PreToolUse Hook 入口腳本
