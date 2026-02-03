# Joey AI Agent - Claude Code 指南

這是 Joey 的個人 AI Agent 系統，運行於 Mac mini 上。

## 特殊觸發詞

### 「啟動進化計劃！」
當用戶說這句話時，代表要對 Joey AI Agent 進行功能升級或改進。
- 進入進化任務模式
- 遵循自體進化協議
- 根據安全分級制度執行修改

---

## GitHub 素材庫使用方式

### 素材庫位置
所有專案素材統一存放於 GitHub：
`https://github.com/JoeyVIP/joey-agent-assets`

### 下載方式
使用 `gh` CLI 下載專案資料夾：
```bash
# 下載整個素材庫
gh repo clone JoeyVIP/joey-agent-assets

# 或只下載特定專案資料夾
# 先 clone，再進入對應資料夾
```

### 撰寫提示詞時的素材引用

當協助用戶撰寫要給 Joey AI Agent 執行的 `.md` 提示詞檔案時：

**正確做法**
```markdown
## 參考資料

所有專案素材請從 GitHub 下載：
https://github.com/JoeyVIP/joey-agent-assets/tree/main/{專案名稱}

請下載資料夾內的所有檔案作為建站參考。
```

---

## 專案架構

```
joey-ai-agent/
├── src/
│   ├── main.py              # FastAPI 入口 (Level 0)
│   ├── config.py            # 環境變數設定 (Level 0)
│   ├── api/
│   │   ├── line_webhook.py  # LINE Webhook (Level 1)
│   │   └── health.py        # 健康檢查
│   ├── services/
│   │   ├── notion_service.py      # Notion 整合 (Level 1)
│   │   ├── task_processor.py      # 任務處理核心 (Level 1)
│   │   ├── claude_service.py      # Claude API (Level 2)
│   │   ├── claude_code_service.py # Claude Code 執行 (Level 1)
│   │   └── line_service.py        # LINE 推送 (Level 2)
│   ├── models/
│   │   └── claude_response.py     # 資料模型
│   └── prompts/
│       └── system_prompt.md       # 系統提示詞 (Level 2)
├── scripts/
│   ├── evolution_controller.py    # 進化控制器
│   └── create_evolution_task.py   # 建立進化任務
├── agent-tasks/
│   ├── submit_evolution.sh        # 提交進化任務
│   └── templates/
│       └── evolution-template.md  # 任務模板
├── web-frontend/                  # 前端程式碼 (Level 3)
└── tasks/                         # 任務輸出 (Level 3)
```

## 進化前置步驟：先找現成工具

**重要**：這應該成為所有進化任務的第一步！

### 執行順序

1. **搜尋** - 先在 GitHub、npm、PyPI 搜尋是否有現成解決方案
2. **評估** - 比較自己做 vs 用現成工具的成本
3. **採用** - 優先使用經過驗證的工具
4. **客製** - 只在必要時才自己開發

### 搜尋關鍵字範例

- `Claude Code plugin {功能}`
- `MCP server {功能}`
- `GitHub {語言} {功能} tool`
- `awesome-{技術} {功能}`

### 為什麼這很重要？

- 節省開發時間
- 使用經過測試的解決方案
- 減少維護負擔
- 學習業界最佳實踐

### 評估採用 vs 自建

在決定是否使用現成工具時，考慮：

| 因素 | 採用現成工具 | 自己開發 |
|------|-------------|----------|
| 功能符合度 | > 80% 需求 | < 50% 需求 |
| 維護狀態 | 活躍維護 | 已棄用或無人維護 |
| 學習曲線 | 文件完整 | 文件不足 |
| 客製化需求 | 可擴展 | 完全客製 |

### 記錄決策

每次進化任務應記錄：
- 搜尋了哪些工具
- 為什麼選擇/不選擇現成工具
- 採用的工具來源（如有）

---

## 自體進化協議

### 安全分級制度

| 等級 | 說明 | 檔案範圍 |
|------|------|----------|
| **Level 0** | 禁止自動修改 | config.py, main.py, .env, plist |
| **Level 1** | 核心邏輯，需快照 + 完整驗證 | line_webhook.py, task_processor.py, notion_service.py, claude_code_service.py |
| **Level 2** | 安全修改，需快照 | system_prompt.md, claude_service.py, line_service.py |
| **Level 3** | 自由修改 | web-frontend/, tasks/, agent-tasks/, docs/ |

### 進化流程

當收到進化任務時，必須按照以下流程執行：

1. **讀取任務的安全等級**
   - 檢查任務中指定的檔案
   - 自動判斷最高限制等級

2. **Level 0 任務處理**
   - 拒絕執行
   - 回報需要人工介入
   - 更新 Notion 狀態為 `failed`

3. **Level 1-3 任務處理**
   ```
   a. 呼叫 evolution_controller.pre_evolution_check()
      - 檢查 /health 端點
      - 建立 Git 快照 (tag: pre-evolution-{task_id}-{timestamp})
      - 記錄開始時間到 Notion

   b. 執行修改
      - 根據任務描述進行程式碼修改
      - 遵循任務中的執行步驟

   c. 呼叫 evolution_controller.post_evolution_verify()
      - 檢查 /health 端點
      - 執行任務定義的驗證步驟

   d. 如驗證失敗
      - 呼叫 evolution_controller.rollback()
      - 回滾到快照
      - 重啟服務
      - 更新 Notion 狀態為 rolled_back
   ```

4. **將結果記錄到 Notion Evolution Database**
   - 更新狀態（completed / failed / rolled_back）
   - 記錄執行時間、Git tag、錯誤訊息

### 進化任務格式

使用 `agent-tasks/templates/evolution-template.md` 模板：

```markdown
# 進化任務：{標題}

## 安全等級
Level: {0-3}

## 目標
{描述要達成什麼}

## 修改範圍
- [ ] 檔案1: {路徑}
- [ ] 檔案2: {路徑}

## 執行步驟
1. ...
2. ...

## 驗證方式
- [ ] /health 回應 healthy
- [ ] {其他驗證項目}

## 回滾條件
- 如果 {條件} 則回滾
```

### 使用方式

**方式一：透過腳本提交任務**
```bash
# 建立任務（不執行）
./agent-tasks/submit_evolution.sh task.md

# 建立並執行任務
./agent-tasks/submit_evolution.sh task.md --execute
```

**方式二：檢查並執行 pending 任務**
```bash
python3 scripts/evolution_controller.py --check-pending
```

**方式三：直接執行指定任務**
```bash
python3 scripts/evolution_controller.py --task-id <notion_task_id>
```

## Notion 資料庫

### Evolution Database 欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| Name | Title | 進化標題 |
| Status | Select | pending / executing / verifying / completed / failed / rolled_back |
| Type | Select | prompt / code / frontend / config |
| Level | Select | Level 0 / Level 1 / Level 2 / Level 3 |
| Description | Rich Text | 變更描述與目標 |
| FilesModified | Rich Text | 修改的檔案列表 |
| VerificationSteps | Rich Text | 驗證步驟清單 |
| CreatedAt | Date | 任務建立時間 |
| StartedAt | Date | 開始執行時間 |
| CompletedAt | Date | 完成時間 |
| Duration | Number | 執行耗時（秒） |
| GitTagPre | Text | 進化前快照 tag |
| GitTagPost | Text | 進化後快照 tag |
| GitCommitHash | Text | 最終 commit hash |
| VerificationResult | Rich Text | 驗證結果詳情 |
| ErrorMessage | Rich Text | 錯誤訊息 |
| RollbackReason | Rich Text | 回滾原因 |
| AgentOutput | Rich Text | Agent 執行輸出摘要 |

### 狀態流轉

```
pending → executing → verifying → completed
              ↓           ↓
           failed    rolled_back
```

## 開發注意事項

1. **永遠不要直接修改 Level 0 檔案**
   - 這些檔案的變更需要人工審核

2. **修改 Level 1 檔案前務必備份**
   - 使用 evolution_controller 自動建立快照
   - 確保 /health 檢查通過後才算成功

3. **測試新功能時**
   - 先在 Level 3 區域（如 web-frontend）測試
   - 確認無誤後再考慮整合到核心

4. **查看進化歷史**
   - 到 Notion Evolution Database 查看所有進化記錄
   - 可追蹤失敗原因和回滾歷史

## 部署流程（重要！必須完整執行）

當完成進化任務後，**必須按照以下完整流程部署**：

### 完整部署步驟

#### Step 1: 推送到 GitHub
```bash
cd "/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent"
git add <修改的檔案>
git commit -m "feat: 功能描述

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push origin main
```

#### Step 2: 同步到 Mac mini
```bash
rsync -avz "/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent/src/" macmini-remote:~/joey-ai-agent/src/
```

#### Step 3: 清除 Python 緩存（關鍵！）
```bash
ssh macmini-remote "find ~/joey-ai-agent -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null; find ~/joey-ai-agent -name '*.pyc' -delete 2>/dev/null"
```

> ⚠️ **這步非常重要！** Python 會緩存 .pyc 檔案，不清除的話服務可能繼續使用舊代碼。

#### Step 4: 重啟服務
```bash
ssh macmini-remote "lsof -ti :8000 | xargs kill -9 2>/dev/null; sleep 3; cd ~/joey-ai-agent && /usr/bin/python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000 >> ~/joey-ai-agent.log 2>> ~/joey-ai-agent.error.log &"
```

#### Step 5: 驗證部署
```bash
ssh macmini-remote "sleep 4; curl -s http://localhost:8000/health"
# 應該返回: {"status":"healthy"}
```

### 一鍵部署指令（合併 Step 2-5）
```bash
rsync -avz "/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent/src/" macmini-remote:~/joey-ai-agent/src/ && \
ssh macmini-remote "find ~/joey-ai-agent -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null; find ~/joey-ai-agent -name '*.pyc' -delete 2>/dev/null; lsof -ti :8000 | xargs kill -9 2>/dev/null; sleep 3; cd ~/joey-ai-agent && /usr/bin/python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000 >> ~/joey-ai-agent.log 2>> ~/joey-ai-agent.error.log & sleep 4; curl -s http://localhost:8000/health"
```

### SSH 連線資訊
- **別名**: `macmini-remote`（Tailscale）
- **IP**: 100.116.178.96
- **用戶**: joeyserver
- **專案路徑**: `~/joey-ai-agent`
- **日誌位置**: `~/joey-ai-agent.log` 和 `~/joey-ai-agent.error.log`

### 注意事項
- 本地 repo: `joey-ai-agent-local.git`
- Mac mini repo: `joey-ai-agent.git`
- 兩個 repo 歷史不同步，使用 rsync 同步檔案更可靠
- Mac mini 有自動重啟機制（透過 .zshrc），殺掉進程後會自動重啟
- 如果服務異常，查看日誌：`ssh macmini-remote "tail -50 ~/joey-ai-agent.error.log"`

### 常見問題

#### 問題：部署後代碼沒有更新
**原因**：Python 緩存（.pyc）沒有清除
**解決**：執行 Step 3 清除緩存後重啟

#### 問題：端口被佔用
**解決**：`ssh macmini-remote "lsof -ti :8000 | xargs kill -9"`

#### 問題：服務已讀不回
**排查步驟**：
1. 檢查健康狀態：`ssh macmini-remote "curl -s http://localhost:8000/health"`
2. 查看錯誤日誌：`ssh macmini-remote "tail -30 ~/joey-ai-agent.error.log"`
3. 確認進程存在：`ssh macmini-remote "ps aux | grep uvicorn | grep -v grep"`

---

## 相關指令

```bash
# 健康檢查
curl http://localhost:8000/health

# 查看服務狀態
launchctl list | grep joey

# 重啟服務
launchctl kickstart -k gui/$(id -u)/com.joey.ai-agent

# 查看 Git 快照
git tag -l "pre-evolution-*"
git tag -l "post-evolution-*"

# 回滾到特定快照
git reset --hard pre-evolution-{tag}
```
