---
name: cantonese-command-parser
description: Parse and execute commands given in Cantonese. Use when user gives instructions or requests actions in Cantonese. Translates Cantonese commands to executable actions.
---

# 粵語指令解析技能 (Cantonese Command Parser Skill)

當用戶用粵語發出指令時，使用此技能解析並執行相應操作。

## 觸發條件

當用戶輸入包含以下粵語指令模式時啟用：
- 動作請求：「幫我...」、「我想...」、「可唔可以...」
- 直接指令：「開個...」、「寫個...」、「搵下...」
- 查詢請求：「...係乜嘢」、「點樣...」、「邊度有...」

## 指令模式識別

### 文件操作
| 粵語指令 | 意圖 | 對應操作 |
|----------|------|----------|
| 開個檔案 | 打開/創建文件 | Read / Write |
| 睇下個檔 | 查看文件 | Read |
| 改下個檔 | 編輯文件 | Edit |
| 刪咗佢 | 刪除文件 | Bash rm |
| 搵個檔案 | 查找文件 | Glob / Grep |
| 寫入去 | 寫入內容 | Write / Edit |

### 代碼操作
| 粵語指令 | 意圖 | 對應操作 |
|----------|------|----------|
| 寫段 code | 編寫代碼 | Write |
| 改下段 code | 修改代碼 | Edit |
| 跑下個程式 | 運行程序 | Bash |
| 裝個 package | 安裝依賴 | Bash npm/pip |
| 測試下 | 運行測試 | Bash test |
| debug 下 | 調試 | Read / Bash |

### 搜索查詢
| 粵語指令 | 意圖 | 對應操作 |
|----------|------|----------|
| 搵下 | 搜索 | Grep / Glob |
| 有冇... | 檢查存在 | Glob / Grep |
| 喺邊度 | 定位位置 | Glob / Grep |
| 查下 | 查詢信息 | WebSearch / WebFetch |

### 系統操作
| 粵語指令 | 意圖 | 對應操作 |
|----------|------|----------|
| 開個 terminal | 執行命令 | Bash |
| 裝嘢 | 安裝 | Bash |
| 行個 command | 運行命令 | Bash |
| 睇下 status | 查看狀態 | Bash / Read |

### Git 操作
| 粵語指令 | 意圖 | 對應操作 |
|----------|------|----------|
| commit 咗佢 | 提交 | Bash git commit |
| push 上去 | 推送 | Bash git push |
| pull 返嚟 | 拉取 | Bash git pull |
| 開個 branch | 創建分支 | Bash git branch |
| merge 埋佢 | 合併 | Bash git merge |

## 常見指令句式

### 請求幫助
```
「幫我 [動作] [對象]」
例：幫我寫個 function → 請求編寫函數

「我想 [動作] [對象]」
例：我想睇下個 log → 請求查看日誌

「可唔可以 [動作]」
例：可唔可以 run 下 tests → 請求運行測試
```

### 直接指令
```
「[動作] 下 [對象]」
例：睇下個 file → 查看文件

「[動作] 咗 [對象]」
例：刪咗個 temp folder → 刪除臨時文件夾

「將 [對象] [動作]」
例：將個 bug fix 咗 → 修復 bug
```

### 查詢
```
「[對象] 係乜嘢」
例：呢個 error 係乜嘢 → 詢問錯誤含義

「點樣 [動作]」
例：點樣 deploy → 詢問如何部署

「[對象] 喺邊度」
例：config file 喺邊度 → 查找配置文件位置
```

## 解析流程

1. **識別指令類型**: 判斷是文件操作、代碼操作、搜索還是系統操作
2. **提取對象**: 識別操作的目標（文件名、代碼片段、搜索詞等）
3. **確認參數**: 如有需要，詢問缺失的參數
4. **執行操作**: 調用相應的工具執行任務
5. **粵語回應**: 用粵語報告結果

## 輸出格式

解析完成後：

```
【指令解析】
原文: [用戶原始指令]
類型: [操作類型]
動作: [具體動作]
對象: [操作目標]
參數: [額外參數]

執行: [調用的工具和參數]
```

## 示例

用戶輸入：「幫我搵下邊度用咗 deprecated API」

解析結果：
```
【指令解析】
原文: 幫我搵下邊度用咗 deprecated API
類型: 搜索查詢
動作: 搜索
對象: deprecated API 的使用位置
參數: 無

執行: Grep 工具搜索 "deprecated" 或相關模式
```

回應：「冇問題，我幫你搵下...」然後執行搜索並報告結果。
