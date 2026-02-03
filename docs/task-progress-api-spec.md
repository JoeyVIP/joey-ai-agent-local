# 任務進度監控 API 規格

> 未來網頁版「功能進度顯示頁面」的開發規格

## 監控方法概覽

| 項目 | 資料來源 | 用途 |
|------|----------|------|
| 任務接收記錄 | 錯誤日誌 | 確認檔案/訊息已收到 |
| 任務分析結果 | 錯誤日誌 | 查看 Claude API 判定（simple/complex）|
| Claude Code 執行狀態 | 進程列表 | 確認是否正在執行 |
| 任務輸出檔案 | tasks/ 資料夾 | 查看已產出的檔案 |
| Notion 任務狀態 | Notion API | Review Database 狀態 |

---

## 資料來源與查詢方式

### 1. 查看任務日誌

```bash
# 查看最新任務處理記錄
ssh macmini-remote "tail -50 ~/joey-ai-agent.error.log | grep -E 'Received|task|Task|Claude|完成|Error'"
```

**關鍵日誌關鍵字**：
| 關鍵字 | 意義 |
|--------|------|
| `Received file from` | 收到檔案 |
| `Creating inbox task` | 建立 Inbox 任務 |
| `Claude response - difficulty:` | 任務難度判定 |
| `Creating review task` | 建立 Review 任務 |
| `Executing complex task with Claude Code` | 開始執行 Claude Code |
| `Ralph Loop: Attempt X/10` | 執行嘗試次數 |

### 2. 查看 Claude Code 執行狀態

```bash
# 檢查 Claude 進程是否在運行
ssh macmini-remote "ps aux | grep claude | grep -v grep"

# 輸出範例：
# joeyserver 56229 0.4 1.7 429499008 279904 ?? S 10:32下午 0:03.62 claude
# → PID: 56229, 啟動時間: 10:32下午, 執行中
```

### 3. 查看任務輸出資料夾

```bash
# 列出所有任務資料夾
ssh macmini-remote "ls -la ~/joey-ai-agent/tasks/"

# 查看特定任務的檔案結構
ssh macmini-remote "ls -laR ~/joey-ai-agent/tasks/{任務資料夾}/"

# 任務資料夾命名格式：{日期}_{任務名稱}_attempt{次數}
# 範例：2026-02-03_來電司康官網製作_attempt1
```

### 4. 查看任務內容

```bash
# 查看任務描述
ssh macmini-remote "cat ~/joey-ai-agent/tasks/{任務資料夾}/task.md"

# 查看產出的程式碼（以網站為例）
ssh macmini-remote "head -50 ~/joey-ai-agent/tasks/{任務資料夾}/{專案名稱}/index.html"
```

---

## 日誌時間線解讀

典型的複雜任務執行流程：

```
22:31:45 - Received file from U445... (收到檔案)
22:31:45 - Creating inbox task... (建立 Inbox)
22:31:47 - Inbox task created: {id} (Inbox 建立完成)
22:31:49 - Reading memories... (讀取記憶)
22:31:49 - Stage 1: Calling Claude API... (呼叫 Claude 分析)
22:32:03 - Claude response - difficulty: complex (判定為複雜)
22:32:03 - Creating review task... (建立 Review)
22:32:04 - 推送訊息給 Joey... (LINE 通知)
22:32:05 - Stage 2: Executing complex task... (開始 Claude Code)
22:32:05 - Ralph Loop: Attempt 1/10 (第 1 次嘗試)
22:32:05 - Created task folder: /path/to/task (建立任務資料夾)
... (執行中)
XX:XX:XX - Task completed successfully (完成)
```

---

## API 設計規格

### GET /api/tasks/progress/{task_id}

查詢特定任務的執行進度。

**回傳格式**：

```json
{
    "task_id": "2fc6fb7a-...",
    "title": "來電司康官網製作",
    "status": "executing",
    "difficulty": "complex",
    "started_at": "2026-02-03T22:31:45",
    "current_attempt": 1,
    "max_attempts": 10,
    "output_folder": "/tasks/2026-02-03_來電司康官網製作_attempt1",
    "files_created": [
        "leicall-scone-website/index.html",
        "leicall-scone-website/services.html",
        "leicall-scone-website/css/style.css"
    ],
    "claude_process": {
        "pid": 56229,
        "running": true,
        "started_at": "22:32:05"
    },
    "logs": [
        {"time": "22:31:45", "event": "file_received", "message": "收到檔案"},
        {"time": "22:32:03", "event": "analysis_complete", "message": "判定為複雜任務"},
        {"time": "22:32:05", "event": "execution_started", "message": "開始執行 Claude Code"}
    ]
}
```

**狀態值 (status)**：
| 值 | 說明 |
|----|------|
| `received` | 已收到任務 |
| `analyzing` | Claude API 分析中 |
| `executing` | Claude Code 執行中 |
| `completed` | 任務完成 |
| `failed` | 任務失敗 |

---

## 實作建議

### 後端實作

1. **日誌解析器**：解析 `~/joey-ai-agent.error.log` 提取任務事件
2. **進程監控**：定期檢查 Claude 進程狀態
3. **檔案掃描**：掃描 tasks/ 資料夾取得產出檔案列表
4. **Notion 整合**：從 Review Database 取得任務狀態

### 前端實作

1. **輪詢機制**：每 5-10 秒查詢一次進度
2. **時間線顯示**：以時間線方式顯示任務事件
3. **檔案樹狀圖**：顯示已產出的檔案結構
4. **即時日誌**：顯示最新的執行日誌

---

## 相關檔案

- 日誌位置：`~/joey-ai-agent.error.log`
- 任務資料夾：`~/joey-ai-agent/tasks/`
- Notion Review Database：詳見 `架構說明.md`
