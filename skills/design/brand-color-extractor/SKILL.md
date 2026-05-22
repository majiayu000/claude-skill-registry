---
name: brand-color-extractor
description: 🎨 品牌配色提取專家 - 當需要為 VS Code 主題提取品牌官方配色時使用此 skill。從官方網站提取品牌配色並生成 VS Code 主題色彩方案 (project)
---

# 品牌配色提取專家

從官方網站提取品牌配色並生成 VS Code 主題色彩方案。

## 使用時機

當需要為 VS Code 主題提取品牌官方配色時使用此 skill。

## 工作流程

### 1. 取得品牌配色

使用 `WebFetch` 訪問品牌官網或設計系統頁面，提取以下資訊：

**優先來源順序：**

1. 官方 Brand Guidelines / Design System 頁面
1. 官網首頁 CSS 變數
1. 官方 Press Kit / Media Kit
1. 產品介面截圖分析

**需要提取的色彩：**

- Primary Color（主色）
- Secondary Color（輔助色）
- Accent Color（強調色）
- Background Colors（背景色系）
- Text Colors（文字色系）
- Border/Divider Colors（邊框色）
- Success/Warning/Error Colors（狀態色）

### 2. 色彩分析與轉換

**淺色主題原則：**

- 編輯器背景：不要純白 `#FFFFFF`，使用品牌淺色背景（如 `#F9FAFB`、`#FAF9F7`）
- 側邊欄背景：比編輯器稍深 2-3 階
- 對比度：文字與背景對比度 ≥ 4.5:1（WCAG AA）
- 強調色：使用品牌主色

**深色主題原則：**

- 編輯器背景：`#1A-2A` 範圍內的深色
- 側邊欄背景：比編輯器稍深或稍淺
- 文字：`#D0-F0` 範圍的淺色
- 強調色：品牌主色的亮色變體

## VS Code 主題結構

### 1. UI 色彩 (`colors`)

編輯器介面元素的顏色，必須設定以下所有類別：

#### 編輯器核心

| 屬性 | 說明 |
|------|------|
| `editor.background` | 編輯器背景 |
| `editor.foreground` | 編輯器前景（預設文字色） |
| `editor.lineHighlightBackground` | 當前行高亮背景 |
| `editor.selectionBackground` | 選取文字背景 |
| `editor.selectionHighlightBackground` | 相同選取項高亮 |
| `editor.wordHighlightBackground` | 讀取存取時單字高亮 |
| `editor.wordHighlightStrongBackground` | 寫入存取時單字高亮 |
| `editor.findMatchBackground` | 搜尋匹配項背景 |
| `editor.findMatchHighlightBackground` | 其他搜尋匹配項 |
| `editor.hoverHighlightBackground` | 懸停高亮 |
| `editor.rangeHighlightBackground` | 範圍高亮（如快速開啟） |
| `editorCursor.foreground` | 游標顏色 |
| `editorWhitespace.foreground` | 空白字元顏色 |
| `editorIndentGuide.background` | 縮排參考線 |
| `editorIndentGuide.activeBackground` | 作用中縮排線 |
| `editorRuler.foreground` | 尺規顏色 |

#### 行號與裝訂線

| 屬性 | 說明 |
|------|------|
| `editorLineNumber.foreground` | 行號顏色 |
| `editorLineNumber.activeForeground` | 當前行號顏色 |
| `editorGutter.background` | 裝訂線背景 |
| `editorGutter.modifiedBackground` | 已修改行標記 |
| `editorGutter.addedBackground` | 新增行標記 |
| `editorGutter.deletedBackground` | 刪除行標記 |

#### 括號與配對

| 屬性 | 說明 |
|------|------|
| `editorBracketMatch.background` | 配對括號背景 |
| `editorBracketMatch.border` | 配對括號邊框 |
| `editorBracketHighlight.foreground1` | 括號配對色 1 |
| `editorBracketHighlight.foreground2` | 括號配對色 2 |
| `editorBracketHighlight.foreground3` | 括號配對色 3 |
| `editorBracketHighlight.foreground4` | 括號配對色 4 |
| `editorBracketHighlight.foreground5` | 括號配對色 5 |
| `editorBracketHighlight.foreground6` | 括號配對色 6 |

#### 錯誤與警告

| 屬性 | 說明 |
|------|------|
| `editorError.foreground` | 錯誤波浪線 |
| `editorWarning.foreground` | 警告波浪線 |
| `editorInfo.foreground` | 資訊波浪線 |
| `editorHint.foreground` | 提示波浪線 |

#### 未使用程式碼

| 屬性 | 說明 | 建議值 |
|------|------|--------|
| `editorUnnecessaryCode.opacity` | 未使用程式碼透明度 | `#00000077` |
| `editorUnnecessaryCode.border` | 未使用程式碼邊框 | `#00000000` |

#### 活動欄 (Activity Bar)

| 屬性 | 說明 |
|------|------|
| `activityBar.background` | 活動欄背景 |
| `activityBar.foreground` | 活動欄前景（選中圖示） |
| `activityBar.inactiveForeground` | 未選中圖示 |
| `activityBar.border` | 活動欄邊框 |
| `activityBarBadge.background` | 徽章背景 |
| `activityBarBadge.foreground` | 徽章文字 |

#### 側邊欄 (Side Bar)

| 屬性 | 說明 |
|------|------|
| `sideBar.background` | 側邊欄背景 |
| `sideBar.foreground` | 側邊欄前景 |
| `sideBar.border` | 側邊欄邊框 |
| `sideBarTitle.foreground` | 側邊欄標題 |
| `sideBarSectionHeader.background` | 區段標題背景 |
| `sideBarSectionHeader.foreground` | 區段標題前景 |
| `sideBarSectionHeader.border` | 區段標題邊框 |

#### 標題欄 (Title Bar)

| 屬性 | 說明 |
|------|------|
| `titleBar.activeBackground` | 作用中標題背景 |
| `titleBar.activeForeground` | 作用中標題前景 |
| `titleBar.inactiveBackground` | 非作用中背景 |
| `titleBar.inactiveForeground` | 非作用中前景 |
| `titleBar.border` | 標題欄邊框 |

#### 狀態欄 (Status Bar)

| 屬性 | 說明 |
|------|------|
| `statusBar.background` | 狀態欄背景 |
| `statusBar.foreground` | 狀態欄前景 |
| `statusBar.border` | 狀態欄邊框 |
| `statusBar.debuggingBackground` | 除錯中背景 |
| `statusBar.debuggingForeground` | 除錯中前景 |
| `statusBar.noFolderBackground` | 無資料夾背景 |
| `statusBar.noFolderForeground` | 無資料夾前景 |
| `statusBarItem.hoverBackground` | 懸停背景 |
| `statusBarItem.activeBackground` | 點擊背景 |
| `statusBarItem.prominentBackground` | 醒目項目背景 |
| `statusBarItem.prominentHoverBackground` | 醒目項目懸停 |
| `statusBarItem.remoteBackground` | 遠端連線背景 |
| `statusBarItem.remoteForeground` | 遠端連線前景 |

#### 標籤 (Tabs)

| 屬性 | 說明 |
|------|------|
| `tab.activeBackground` | 作用中標籤背景 |
| `tab.activeForeground` | 作用中標籤前景 |
| `tab.inactiveBackground` | 非作用中標籤背景 |
| `tab.inactiveForeground` | 非作用中標籤前景 |
| `tab.border` | 標籤邊框 |
| `tab.activeBorder` | 作用中標籤邊框 |
| `tab.activeBorderTop` | 作用中標籤上邊框 |
| `tab.unfocusedActiveBackground` | 非焦點作用中背景 |
| `tab.unfocusedActiveForeground` | 非焦點作用中前景 |
| `tab.hoverBackground` | 懸停背景 |
| `tab.hoverForeground` | 懸停前景 |

#### 編輯器群組與標籤列

| 屬性 | 說明 |
|------|------|
| `editorGroup.border` | 編輯器群組邊框 |
| `editorGroup.dropBackground` | 拖放背景 |
| `editorGroupHeader.tabsBackground` | 標籤列背景 |
| `editorGroupHeader.tabsBorder` | 標籤列邊框 |
| `editorGroupHeader.noTabsBackground` | 無標籤時背景 |

#### 面板 (Panel)

| 屬性 | 說明 |
|------|------|
| `panel.background` | 面板背景 |
| `panel.border` | 面板邊框 |
| `panelTitle.activeBorder` | 作用中標題邊框 |
| `panelTitle.activeForeground` | 作用中標題前景 |
| `panelTitle.inactiveForeground` | 非作用中標題前景 |

#### 終端機 (Terminal)

| 屬性 | 說明 |
|------|------|
| `terminal.background` | 終端機背景 |
| `terminal.foreground` | 終端機前景 |
| `terminal.ansiBlack` | ANSI 黑 |
| `terminal.ansiRed` | ANSI 紅 |
| `terminal.ansiGreen` | ANSI 綠 |
| `terminal.ansiYellow` | ANSI 黃 |
| `terminal.ansiBlue` | ANSI 藍 |
| `terminal.ansiMagenta` | ANSI 洋紅 |
| `terminal.ansiCyan` | ANSI 青 |
| `terminal.ansiWhite` | ANSI 白 |
| `terminal.ansiBrightBlack` | ANSI 亮黑 |
| `terminal.ansiBrightRed` | ANSI 亮紅 |
| `terminal.ansiBrightGreen` | ANSI 亮綠 |
| `terminal.ansiBrightYellow` | ANSI 亮黃 |
| `terminal.ansiBrightBlue` | ANSI 亮藍 |
| `terminal.ansiBrightMagenta` | ANSI 亮洋紅 |
| `terminal.ansiBrightCyan` | ANSI 亮青 |
| `terminal.ansiBrightWhite` | ANSI 亮白 |
| `terminalCursor.foreground` | 終端機游標 |
| `terminalCursor.background` | 終端機游標背景 |

#### 輸入框與下拉選單

| 屬性 | 說明 |
|------|------|
| `input.background` | 輸入框背景 |
| `input.foreground` | 輸入框前景 |
| `input.border` | 輸入框邊框 |
| `input.placeholderForeground` | 佔位文字 |
| `inputOption.activeBackground` | 選項作用中背景 |
| `inputOption.activeBorder` | 選項作用中邊框 |
| `inputValidation.errorBackground` | 驗證錯誤背景 |
| `inputValidation.errorBorder` | 驗證錯誤邊框 |
| `inputValidation.warningBackground` | 驗證警告背景 |
| `inputValidation.warningBorder` | 驗證警告邊框 |
| `inputValidation.infoBackground` | 驗證資訊背景 |
| `inputValidation.infoBorder` | 驗證資訊邊框 |
| `dropdown.background` | 下拉選單背景 |
| `dropdown.foreground` | 下拉選單前景 |
| `dropdown.border` | 下拉選單邊框 |

#### 按鈕

| 屬性 | 說明 |
|------|------|
| `button.background` | 按鈕背景 |
| `button.foreground` | 按鈕前景 |
| `button.hoverBackground` | 按鈕懸停背景 |
| `button.secondaryBackground` | 次要按鈕背景 |
| `button.secondaryForeground` | 次要按鈕前景 |
| `button.secondaryHoverBackground` | 次要按鈕懸停 |

#### 列表與樹狀圖

| 屬性 | 說明 |
|------|------|
| `list.activeSelectionBackground` | 作用中選取背景 |
| `list.activeSelectionForeground` | 作用中選取前景 |
| `list.inactiveSelectionBackground` | 非作用中選取背景 |
| `list.inactiveSelectionForeground` | 非作用中選取前景 |
| `list.hoverBackground` | 懸停背景 |
| `list.hoverForeground` | 懸停前景 |
| `list.focusBackground` | 焦點背景 |
| `list.focusForeground` | 焦點前景 |
| `list.highlightForeground` | 搜尋匹配高亮 |
| `list.dropBackground` | 拖放背景 |
| `tree.indentGuidesStroke` | 樹狀圖縮排線 |

#### 捲軸

| 屬性 | 說明 |
|------|------|
| `scrollbar.shadow` | 捲軸陰影 |
| `scrollbarSlider.background` | 滑塊背景 |
| `scrollbarSlider.hoverBackground` | 滑塊懸停 |
| `scrollbarSlider.activeBackground` | 滑塊作用中 |

#### 迷你地圖 (Minimap)

| 屬性 | 說明 |
|------|------|
| `minimap.findMatchHighlight` | 搜尋匹配高亮 |
| `minimap.selectionHighlight` | 選取高亮 |
| `minimap.errorHighlight` | 錯誤高亮 |
| `minimap.warningHighlight` | 警告高亮 |
| `minimapSlider.background` | 滑塊背景 |
| `minimapSlider.hoverBackground` | 滑塊懸停 |
| `minimapSlider.activeBackground` | 滑塊作用中 |
| `minimapGutter.addedBackground` | 新增標記 |
| `minimapGutter.modifiedBackground` | 修改標記 |
| `minimapGutter.deletedBackground` | 刪除標記 |

#### 麵包屑 (Breadcrumb)

| 屬性 | 說明 |
|------|------|
| `breadcrumb.background` | 麵包屑背景 |
| `breadcrumb.foreground` | 麵包屑前景 |
| `breadcrumb.focusForeground` | 焦點前景 |
| `breadcrumb.activeSelectionForeground` | 選取前景 |
| `breadcrumbPicker.background` | 選擇器背景 |

#### Git 裝飾

| 屬性 | 說明 |
|------|------|
| `gitDecoration.addedResourceForeground` | 新增檔案 |
| `gitDecoration.modifiedResourceForeground` | 修改檔案 |
| `gitDecoration.deletedResourceForeground` | 刪除檔案 |
| `gitDecoration.untrackedResourceForeground` | 未追蹤檔案 |
| `gitDecoration.ignoredResourceForeground` | 忽略檔案 |
| `gitDecoration.conflictingResourceForeground` | 衝突檔案 |
| `gitDecoration.submoduleResourceForeground` | 子模組 |
| `gitDecoration.stageModifiedResourceForeground` | 暫存修改 |
| `gitDecoration.stageDeletedResourceForeground` | 暫存刪除 |

#### Diff 編輯器

| 屬性 | 說明 |
|------|------|
| `diffEditor.insertedTextBackground` | 新增文字背景 |
| `diffEditor.removedTextBackground` | 刪除文字背景 |
| `diffEditor.insertedLineBackground` | 新增行背景 |
| `diffEditor.removedLineBackground` | 刪除行背景 |
| `diffEditor.diagonalFill` | 對角線填充 |

#### 合併編輯器

| 屬性 | 說明 |
|------|------|
| `merge.currentHeaderBackground` | 當前分支標題背景 |
| `merge.currentContentBackground` | 當前分支內容背景 |
| `merge.incomingHeaderBackground` | 傳入分支標題背景 |
| `merge.incomingContentBackground` | 傳入分支內容背景 |
| `merge.border` | 合併邊框 |
| `merge.commonHeaderBackground` | 共同祖先標題背景 |
| `merge.commonContentBackground` | 共同祖先內容背景 |

#### 通知

| 屬性 | 說明 |
|------|------|
| `notificationCenter.border` | 通知中心邊框 |
| `notificationCenterHeader.background` | 通知中心標題背景 |
| `notificationCenterHeader.foreground` | 通知中心標題前景 |
| `notifications.background` | 通知背景 |
| `notifications.foreground` | 通知前景 |
| `notifications.border` | 通知邊框 |
| `notificationLink.foreground` | 通知連結 |
| `notificationsErrorIcon.foreground` | 錯誤圖示 |
| `notificationsWarningIcon.foreground` | 警告圖示 |
| `notificationsInfoIcon.foreground` | 資訊圖示 |

#### 徽章

| 屬性 | 說明 |
|------|------|
| `badge.background` | 徽章背景 |
| `badge.foreground` | 徽章前景 |

#### 進度條

| 屬性 | 說明 |
|------|------|
| `progressBar.background` | 進度條背景 |

#### 選取器與命令面板

| 屬性 | 說明 |
|------|------|
| `pickerGroup.border` | 群組邊框 |
| `pickerGroup.foreground` | 群組前景 |
| `quickInput.background` | 快速輸入背景 |
| `quickInput.foreground` | 快速輸入前景 |
| `quickInputList.focusBackground` | 焦點背景 |
| `quickInputTitle.background` | 標題背景 |

#### 編輯器小工具

| 屬性 | 說明 |
|------|------|
| `editorWidget.background` | 小工具背景 |
| `editorWidget.foreground` | 小工具前景 |
| `editorWidget.border` | 小工具邊框 |
| `editorSuggestWidget.background` | 建議小工具背景 |
| `editorSuggestWidget.border` | 建議小工具邊框 |
| `editorSuggestWidget.foreground` | 建議小工具前景 |
| `editorSuggestWidget.selectedBackground` | 選取背景 |
| `editorSuggestWidget.highlightForeground` | 匹配高亮 |
| `editorHoverWidget.background` | 懸停小工具背景 |
| `editorHoverWidget.border` | 懸停小工具邊框 |
| `editorHoverWidget.foreground` | 懸停小工具前景 |

#### Peek 檢視

| 屬性 | 說明 |
|------|------|
| `peekView.border` | Peek 邊框 |
| `peekViewEditor.background` | Peek 編輯器背景 |
| `peekViewEditor.matchHighlightBackground` | 匹配高亮背景 |
| `peekViewResult.background` | 結果背景 |
| `peekViewResult.fileForeground` | 檔案前景 |
| `peekViewResult.lineForeground` | 行前景 |
| `peekViewResult.matchHighlightBackground` | 匹配高亮 |
| `peekViewResult.selectionBackground` | 選取背景 |
| `peekViewResult.selectionForeground` | 選取前景 |
| `peekViewTitle.background` | 標題背景 |
| `peekViewTitleDescription.foreground` | 標題描述前景 |
| `peekViewTitleLabel.foreground` | 標題標籤前景 |

#### 焦點與邊框

| 屬性 | 說明 |
|------|------|
| `focusBorder` | 焦點邊框（全域） |
| `contrastBorder` | 對比邊框 |
| `contrastActiveBorder` | 作用中對比邊框 |
| `widget.shadow` | 小工具陰影 |
| `selection.background` | 選取背景（全域） |

#### 歡迎頁面

| 屬性 | 說明 |
|------|------|
| `welcomePage.background` | 歡迎頁背景 |
| `welcomePage.buttonBackground` | 按鈕背景 |
| `welcomePage.buttonHoverBackground` | 按鈕懸停 |
| `walkThrough.embeddedEditorBackground` | 嵌入編輯器背景 |

#### 設定編輯器

| 屬性 | 說明 |
|------|------|
| `settings.headerForeground` | 標題前景 |
| `settings.modifiedItemIndicator` | 已修改指示 |
| `settings.dropdownBackground` | 下拉背景 |
| `settings.dropdownForeground` | 下拉前景 |
| `settings.dropdownBorder` | 下拉邊框 |
| `settings.checkboxBackground` | 核取方塊背景 |
| `settings.checkboxForeground` | 核取方塊前景 |
| `settings.checkboxBorder` | 核取方塊邊框 |
| `settings.textInputBackground` | 文字輸入背景 |
| `settings.textInputForeground` | 文字輸入前景 |
| `settings.textInputBorder` | 文字輸入邊框 |
| `settings.numberInputBackground` | 數字輸入背景 |
| `settings.numberInputForeground` | 數字輸入前景 |
| `settings.numberInputBorder` | 數字輸入邊框 |

#### 除錯

| 屬性 | 說明 |
|------|------|
| `debugToolBar.background` | 除錯工具列背景 |
| `debugToolBar.border` | 除錯工具列邊框 |
| `debugExceptionWidget.background` | 例外小工具背景 |
| `debugExceptionWidget.border` | 例外小工具邊框 |
| `debugConsole.infoForeground` | 主控台資訊 |
| `debugConsole.warningForeground` | 主控台警告 |
| `debugConsole.errorForeground` | 主控台錯誤 |
| `debugConsole.sourceForeground` | 主控台來源 |
| `debugConsoleInputIcon.foreground` | 輸入圖示 |

#### 測試

| 屬性 | 說明 |
|------|------|
| `testing.iconFailed` | 失敗圖示 |
| `testing.iconErrored` | 錯誤圖示 |
| `testing.iconPassed` | 通過圖示 |
| `testing.iconQueued` | 排隊圖示 |
| `testing.iconUnset` | 未設定圖示 |
| `testing.iconSkipped` | 跳過圖示 |

#### 擴展

| 屬性 | 說明 |
|------|------|
| `extensionButton.prominentBackground` | 安裝按鈕背景 |
| `extensionButton.prominentForeground` | 安裝按鈕前景 |
| `extensionButton.prominentHoverBackground` | 安裝按鈕懸停 |
| `extensionBadge.remoteBackground` | 遠端徽章背景 |
| `extensionBadge.remoteForeground` | 遠端徽章前景 |

### 2. 語法高亮 (`tokenColors`)

程式碼 token 的著色，必須設定以下所有 scope：

#### 基礎

| Scope | 說明 |
|-------|------|
| `comment` | 註解 |
| `comment.line` | 單行註解 |
| `comment.block` | 區塊註解 |
| `comment.block.documentation` | 文件註解 |

#### 字串

| Scope | 說明 |
|-------|------|
| `string` | 字串 |
| `string.quoted.single` | 單引號字串 |
| `string.quoted.double` | 雙引號字串 |
| `string.template` | 模板字串 |
| `string.regexp` | 正規表達式 |

#### 常數

| Scope | 說明 |
|-------|------|
| `constant` | 常數 |
| `constant.numeric` | 數字 |
| `constant.numeric.integer` | 整數 |
| `constant.numeric.float` | 浮點數 |
| `constant.numeric.hex` | 十六進位 |
| `constant.language` | 語言常數 (true, false, null) |
| `constant.character` | 字元常數 |
| `constant.character.escape` | 跳脫字元 |
| `constant.other` | 其他常數 |

#### 變數

| Scope | 說明 |
|-------|------|
| `variable` | 變數 |
| `variable.parameter` | 參數 |
| `variable.language` | 語言變數 (this, self) |
| `variable.other` | 其他變數 |
| `variable.other.readwrite` | 讀寫變數 |
| `variable.other.constant` | 常數變數 |
| `variable.other.property` | 屬性 |

#### 關鍵字

| Scope | 說明 |
|-------|------|
| `keyword` | 關鍵字 |
| `keyword.control` | 控制關鍵字 (if, for, while) |
| `keyword.control.conditional` | 條件 (if, else) |
| `keyword.control.loop` | 迴圈 (for, while) |
| `keyword.control.import` | 匯入 (import, from) |
| `keyword.control.flow` | 流程控制 (return, break) |
| `keyword.operator` | 運算子關鍵字 (new, typeof) |
| `keyword.other` | 其他關鍵字 |

#### 儲存

| Scope | 說明 |
|-------|------|
| `storage` | 儲存 |
| `storage.type` | 型別宣告 (const, let, var, function) |
| `storage.modifier` | 修飾詞 (public, private, static) |

#### 實體名稱

| Scope | 說明 |
|-------|------|
| `entity.name` | 實體名稱 |
| `entity.name.function` | 函數名稱 |
| `entity.name.class` | 類別名稱 |
| `entity.name.type` | 型別名稱 |
| `entity.name.tag` | 標籤名稱 (HTML/XML) |
| `entity.name.section` | 區段名稱 |
| `entity.name.namespace` | 命名空間 |
| `entity.other.attribute-name` | 屬性名稱 (HTML/XML) |
| `entity.other.inherited-class` | 繼承類別 |

#### 支援

| Scope | 說明 |
|-------|------|
| `support` | 支援 |
| `support.function` | 內建函數 |
| `support.function.builtin` | 語言內建函數 |
| `support.class` | 內建類別 |
| `support.type` | 內建型別 |
| `support.type.primitive` | 原始型別 |
| `support.constant` | 內建常數 |
| `support.variable` | 內建變數 |

#### 標點符號

| Scope | 說明 |
|-------|------|
| `punctuation` | 標點符號 |
| `punctuation.definition` | 定義標點 |
| `punctuation.definition.string` | 字串引號 |
| `punctuation.definition.comment` | 註解符號 |
| `punctuation.definition.tag` | 標籤括號 |
| `punctuation.separator` | 分隔符 (逗號、分號) |
| `punctuation.accessor` | 存取器 (.) |
| `punctuation.bracket` | 括號 |

#### 運算子

| Scope | 說明 |
|-------|------|
| `keyword.operator` | 運算子 |
| `keyword.operator.assignment` | 賦值運算子 |
| `keyword.operator.arithmetic` | 算術運算子 |
| `keyword.operator.logical` | 邏輯運算子 |
| `keyword.operator.comparison` | 比較運算子 |
| `keyword.operator.ternary` | 三元運算子 |
| `keyword.operator.spread` | 展開運算子 |

#### Meta

| Scope | 說明 |
|-------|------|
| `meta.function` | 函數區塊 |
| `meta.function-call` | 函數呼叫 |
| `meta.class` | 類別區塊 |
| `meta.block` | 程式區塊 |
| `meta.brace` | 大括號 |
| `meta.bracket` | 中括號 |
| `meta.return.type` | 回傳型別 |
| `meta.type.annotation` | 型別註解 |
| `meta.object-literal.key` | 物件鍵 |
| `meta.import` | 匯入區塊 |
| `meta.export` | 匯出區塊 |

#### 無效

| Scope | 說明 |
|-------|------|
| `invalid` | 無效 |
| `invalid.illegal` | 非法語法 |
| `invalid.deprecated` | 已棄用 |

#### Markup (Markdown)

| Scope | 說明 |
|-------|------|
| `markup.heading` | 標題 |
| `markup.heading.1` | H1 |
| `markup.heading.2` | H2 |
| `markup.heading.3` | H3 |
| `markup.bold` | 粗體 |
| `markup.italic` | 斜體 |
| `markup.underline` | 底線 |
| `markup.strikethrough` | 刪除線 |
| `markup.quote` | 引用 |
| `markup.list` | 列表 |
| `markup.list.numbered` | 有序列表 |
| `markup.list.unnumbered` | 無序列表 |
| `markup.inline.raw` | 行內程式碼 |
| `markup.raw.block` | 程式碼區塊 |
| `markup.inserted` | 插入 |
| `markup.deleted` | 刪除 |
| `markup.changed` | 變更 |

#### 語言特定

**JSON**

| Scope | 說明 |
|-------|------|
| `support.type.property-name.json` | JSON 鍵名 |
| `string.json` | JSON 字串值 |

**CSS/SCSS**

| Scope | 說明 |
|-------|------|
| `entity.other.attribute-name.class.css` | CSS 類別選擇器 |
| `entity.other.attribute-name.id.css` | CSS ID 選擇器 |
| `entity.name.tag.css` | CSS 標籤選擇器 |
| `support.type.property-name.css` | CSS 屬性名 |
| `support.constant.property-value.css` | CSS 屬性值 |
| `variable.scss` | SCSS 變數 |

**HTML/JSX**

| Scope | 說明 |
|-------|------|
| `entity.name.tag.html` | HTML 標籤 |
| `entity.other.attribute-name.html` | HTML 屬性 |
| `support.class.component` | React 元件 |
| `support.class.component.jsx` | JSX 元件 |

**TypeScript**

| Scope | 說明 |
|-------|------|
| `entity.name.type.ts` | TypeScript 型別 |
| `entity.name.type.interface.ts` | TypeScript 介面 |
| `entity.name.type.enum.ts` | TypeScript 列舉 |
| `entity.name.type.alias.ts` | TypeScript 型別別名 |
| `meta.type.parameters.ts` | 泛型參數 |

**Python**

| Scope | 說明 |
|-------|------|
| `entity.name.function.decorator.python` | Python 裝飾器 |
| `support.type.python` | Python 型別 |
| `meta.function-call.arguments.python` | Python 函數參數 |

**Swift**

| Scope | 說明 |
|-------|------|
| `keyword.other.declaration-specifier.swift` | Swift 宣告修飾詞 |
| `storage.type.swift` | Swift 儲存型別 |
| `entity.name.type.swift` | Swift 型別名稱 |
| `support.type.swift` | Swift 支援型別 |

### 3. 語義高亮 (`semanticTokenColors`)

**必須啟用** `"semanticHighlighting": true`，確保變數顏色正確顯示。

**變數顏色規則（重要）**：

- 深色主題：變數使用 `#FFFFFF`（白色）
- 淺色主題：變數使用 `#1a1a1a`（近黑色）

必須設定的 token：

| Token | 說明 |
|-------|------|
| `variable` | 變數 |
| `variable.readonly` | 唯讀變數 |
| `variable.local` | 區域變數 |
| `variable.declaration` | 變數宣告 |
| `parameter` | 參數 |
| `function` | 函數 |
| `function.declaration` | 函數宣告 |
| `function.defaultLibrary` | 預設庫函數 |
| `method` | 方法 |
| `method.declaration` | 方法宣告 |
| `class` | 類別 |
| `class.declaration` | 類別宣告 |
| `interface` | 介面 |
| `interface.declaration` | 介面宣告 |
| `enum` | 列舉 |
| `enumMember` | 列舉成員 |
| `type` | 型別 |
| `type.declaration` | 型別宣告 |
| `namespace` | 命名空間 |
| `property` | 屬性 |
| `property.readonly` | 唯讀屬性 |
| `property.declaration` | 屬性宣告 |
| `macro` | 巨集 |
| `comment` | 註解 |
| `string` | 字串 |
| `number` | 數字 |
| `regexp` | 正規表達式 |
| `operator` | 運算子 |

## 品牌色彩映射

```text
品牌主色 → activityBar.foreground, statusBar.background, focusBorder, editorCursor
品牌背景 → editor.background, sideBar.background, panel.background
品牌文字 → editor.foreground, sideBar.foreground
品牌輔助 → editorLineNumber.foreground, tab.inactiveForeground
品牌強調 → activityBarBadge.background, button.background
```

## 語法高亮配色建議

**淺色主題：**

- Comment：灰色 50-60% 亮度
- String：品牌色變體或琥珀/綠色系
- Keyword：品牌主色或深藍/紫色系
- Function：品牌輔助色或橙色系
- Class：深色強調，可加 underline
- Type：斜體，品牌色變體

**深色主題：**

- 所有色彩亮度 +20-30%
- 保持色相一致性

## 輸出格式

提供完整的 VS Code 主題 JSON，包含：

1. `"semanticHighlighting": true`（必須）
2. `colors` 物件（UI 色彩）- 必須包含上述所有類別
3. `tokenColors` 陣列（語法高亮）- 必須包含上述所有 scope
4. `semanticTokenColors` 物件（語義高亮）- 必須，確保變數顏色正確

## 品牌官網參考

| 品牌 | 官網 | 設計系統 |
|------|------|----------|
| Claude (Anthropic) | claude.ai | anthropic.com |
| Microsoft Teams | teams.microsoft.com | fluent2.microsoft.design |
| macOS | apple.com/macos | developer.apple.com/design |
| iOS | apple.com/ios | developer.apple.com/design |
| Android | android.com | m3.material.io |
| Nintendo | nintendo.com | - |
| Sony | sony.com | - |
| shadcn/ui | ui.shadcn.com | - |

## 範例提取流程

```text
1. WebFetch: https://claude.ai → 提取頁面配色
2. WebFetch: https://anthropic.com/brand → 提取品牌指南
3. 分析 CSS 變數和主要色彩
4. 建立色彩映射表
5. 生成 VS Code 主題 JSON
```

## 品質檢查

- [ ] 編輯器背景非純白/純黑
- [ ] 文字可讀性（對比度 ≥ 4.5:1）
- [ ] 品牌識別度（一眼能認出品牌）
- [ ] 語法高亮區分度
- [ ] 選取/高亮狀態清晰
- [ ] 所有 UI 色彩類別都已設定
- [ ] 所有語法高亮 scope 都已設定
- [ ] `semanticHighlighting: true` 已啟用
- [ ] `semanticTokenColors` 變數顏色已設定（深色 #FFFFFF / 淺色 #1a1a1a）
- [ ] `editorUnnecessaryCode` 未使用程式碼樣式已設定
- [ ] 終端機 ANSI 色彩完整
- [ ] Git 裝飾色彩清晰區分
- [ ] 括號配對色彩明顯
