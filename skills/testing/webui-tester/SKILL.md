---
name: webui-tester
description: Test, debug, and modify Majsoul WebUI (Laya engine) within the Naki app. Use when the user asks to adjust "the screen" or "UI" - clarify whether they mean Naki's SwiftUI app or Majsoul's WebUI. This skill handles WebUI JavaScript execution, tile manipulation, and visual debugging.
allowed-tools: Read, Glob, Grep, Task
---

<IMPORTANT>
**MCP 調用規則**: 所有 Naki MCP 工具必須透過 `/naki-mcp-proxy` skill 調用，禁止直接調用 `mcp__naki__*` 工具。
</IMPORTANT>

# WebUI Tester Skill

This skill helps test and modify Majsoul's WebUI (game interface) running inside Naki's WKWebView.

## 🆕 NakiCoordinator - 統一協調器 (推薦)

Naki 提供了統一的 JavaScript 協調器，**優先使用**它而非直接訪問遊戲物件：

```javascript
// 快捷訪問
window.naki === window.NakiCoordinator

// 遊戲狀態 (取代直接訪問 DesktopMgr)
naki.state.isInGame()           // 是否在遊戲中
naki.state.canExecuteAction()   // 是否可執行操作
naki.state.getFullState()       // 完整狀態
naki.state.getHandInfo()        // 手牌資訊
naki.state.getAvailableOps()    // 可用操作

// 遊戲操作 (安全封裝，含驗證)
naki.action.discard(tileIndex, {verify: true})  // 打牌並驗證
naki.action.pass({useBuiltin: true})            // 使用內建 auto-nofulu
naki.action.chi(combIndex)      // 吃
naki.action.pon()               // 碰
naki.action.hora({useBuiltin: true})            // 使用內建 auto-hule
naki.action.execute('pass', {}) // 通用執行

// 自動設定控制
naki.auto.setHule(true)         // 自動和牌
naki.auto.setNoFulu(true)       // 自動 pass
naki.auto.setMoqie(true)        // 自動摸切

// 診斷
naki.debug.getDiagnostics()     // 完整診斷
naki.debug.listMethods()        // 列出所有方法
```

**完整 API**: 見 [references/api-architecture.md](references/api-architecture.md)

## Critical Distinction: WebUI vs App UI

When the user says "adjust the screen" or "modify UI", ALWAYS clarify:

| Term | Meaning | Technology | How to Modify |
|------|---------|------------|---------------|
| **WebUI** | Majsoul game interface | Laya 3D Engine (JavaScript) | `mcp__naki__execute_js` |
| **App UI** | Naki application interface | SwiftUI | Edit Swift files |

**Ask the user**: "Do you mean the Majsoul game screen (WebUI) or the Naki app interface (App UI)?"

## MCP Tool Pitfalls

### 1. execute_js MUST use `return` statement

**CRITICAL**: When using `mcp__naki__execute_js`, the JavaScript code MUST include a `return` statement to get results back.

```javascript
// ❌ WRONG - returns undefined
mcp__naki__execute_js({ code: "document.title" })

// ✅ CORRECT - returns the actual value
mcp__naki__execute_js({ code: "return document.title" })
```

**Why**: The code is wrapped in a function, so without `return`, the result is lost.

### 2. Tile Index Mapping - Critical Pitfall

**NEVER use Swift's `tehai` array index to find tiles in WebUI!**

The Problem:
- Swift's `tehai` array is sorted: `tehai.sort { $0.index < $1.index }`
- Majsoul's UI displays tiles in visual order (NOT sorted by index)
- Using `tehai[i]` index will click the WRONG tile

**Correct Approach** (from `WebViewModel.swift:226-266`):
```javascript
// 1. Parse tile MJAI name (e.g., "7m", "5mr", "W")
// 2. Convert to Majsoul type mapping:
const typeMap = {'m': 1, 'p': 0, 's': 2};
const honorMap = {
  'E': [3,1], 'S': [3,2], 'W': [3,3], 'N': [3,4],
  'P': [3,5], 'F': [3,6], 'C': [3,7]
};

// 3. Iterate through mr.hand[i] in JavaScript
// 4. Match by tile.val.type and tile.val.index
// 5. For red dora (e.g., "5mr"), also check tile.val.dora flag
```

## WebUI Object Reference

Key Majsoul/Laya objects accessible via JavaScript:

```javascript
// Game manager (main entry point)
window.view.DesktopMgr.Inst

// Main player role
const mr = window.view.DesktopMgr.Inst.mainrole

// Hand tiles (14 tile objects)
mr.hand[]  // Array of tile objects

// Each tile object has:
tile.val.type   // 0=pinzu, 1=manzu, 2=souzu, 3=honor
tile.val.index  // 1-9 for suited, 1-7 for honors
tile.val.dora   // true if red dora (5mr, 5pr, 5sr)

// Visual effects
tile._doraeffect           // Dora glow effect
tile._recommendeffect      // AI recommendation highlight
tile.effect_recommend      // Recommendation control (.active)
```

See `@docs/majsoul-webui-objects-reference.md` for complete reference.

## Common WebUI Debugging Commands

### Check Game State
```javascript
// Get current round info
return JSON.stringify({
  bakaze: window.view.DesktopMgr.Inst.gameing_state?.bakaze,
  kyoku: window.view.DesktopMgr.Inst.gameing_state?.kyoku
});
```

### Get Hand Tiles
```javascript
const mr = window.view.DesktopMgr.Inst.mainrole;
const tiles = mr.hand.map((t, i) => ({
  index: i,
  type: t.val?.type,
  num: t.val?.index,
  dora: t.val?.dora
}));
return JSON.stringify(tiles);
```

### Find Specific Tile Position
```javascript
// Find tile "5m" (manzu 5)
const mr = window.view.DesktopMgr.Inst.mainrole;
for (let i = 0; i < mr.hand.length; i++) {
  const t = mr.hand[i];
  if (t.val?.type === 1 && t.val?.index === 5) {
    return JSON.stringify({found: true, index: i, pos: t.transform?.position});
  }
}
return JSON.stringify({found: false});
```

### Check Player Names
```javascript
const dm = window.view.DesktopMgr.Inst;
const names = dm.players?.map(p => p.character?.charid) || [];
return JSON.stringify(names);
```

### Toggle Visual Effect
```javascript
// Toggle recommendation highlight on first tile
const mr = window.view.DesktopMgr.Inst.mainrole;
if (mr.hand[0]?.effect_recommend) {
  mr.hand[0].effect_recommend.active = !mr.hand[0].effect_recommend.active;
}
return "toggled";
```

## Workflow for WebUI Testing

1. **Verify game is running**:
   ```
   mcp__naki__game_state
   ```

2. **Get current hand info**:
   ```
   mcp__naki__game_hand
   ```

3. **Execute test JavaScript** (always use return!):
   ```
   mcp__naki__execute_js({ code: "return ..." })
   ```

4. **Check logs for errors**:
   ```
   mcp__naki__get_logs
   ```

## Checklist Before WebUI Modification

- [ ] Confirmed user wants WebUI (not App UI)
- [ ] Game is active (`mcp__naki__game_state` shows valid state)
- [ ] JavaScript includes `return` statement
- [ ] NOT using Swift tehai index for tile lookup
- [ ] Tested in safe scenario first

## Error Handling

If `execute_js` returns null or undefined:
1. Check if game page is loaded
2. Verify JavaScript has `return` statement
3. Check for JavaScript errors in logs
4. Ensure object path exists (use optional chaining `?.`)

## Reference Documentation

For complete Majsoul WebUI object documentation, see:
- [API Architecture](references/api-architecture.md) - **完整 API 架構** (NakiCoordinator, NetAgent, 配置系統, 音效系統等)
- [WebUI Objects Reference](references/reference.md) - Laya Sprite3D 屬性, 牌編碼, 效果機制

### NakiCoordinator 優先使用指南

| 任務 | 舊方法 | 新方法 (推薦) |
|------|--------|---------------|
| 檢查遊戲狀態 | `view.DesktopMgr.Inst.gameing` | `naki.state.isInGame()` |
| 獲取手牌 | `dm.mainrole.hand` | `naki.state.getHandInfo()` |
| 執行打牌 | `mr.setChoosePai(); mr.DoDiscardTile()` | `naki.action.discard(idx)` |
| 執行 pass | 手動發送網路請求 | `naki.action.pass()` |
| 驗證動作 | 自己寫輪詢 | `naki.action.execute('pass', {verify: true})` |
