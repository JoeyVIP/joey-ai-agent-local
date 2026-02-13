# Joey AI Agent - Claude Code 指南

> **⚠️ 語言規定：所有輸出一律使用繁體中文。** 包含對話、文件、註解、commit message 說明等，除非是程式碼變數名稱或技術專有名詞。

## 專案目的

Joey AI Agent 是一套「AI 自動化建站服務」系統，核心功能：

1. **接收客戶建站需求**（透過 LINE）→ 自動呼叫 Claude Code 生成網站
2. **管理客戶專案**（`projects/` 資料夾）→ 每個客戶一個獨立專案目錄
3. **自體進化**（進化協議）→ Agent 可以在安全框架下自我升級

---

## 架構決策：本 repo 與客戶網站的關係

### 兩層架構

| 層級 | 位置 | 內容 | 範例 |
|------|------|------|------|
| **管理層** | 本 repo `projects/` | 需求文件、content.md、備份、進度追蹤 | `projects/rayter/docs/` |
| **程式碼層** | Mac mini 各自的 repo | 網站實際原始碼 | Mac mini 上的獨立 Git repo |

### `projects/` 收錄範圍

`projects/` 是**專案管理檔案櫃**，不限於 Agent 自動生成的網站。以下兩種專案都放這裡：

| 類型 | 說明 | 範例 |
|------|------|------|
| **Agent 自動生成** | 透過 LINE → Agent 自動建站，之後在此管理後續修改 | 巨領企業、來電司康 |
| **手動管理** | 非 Agent 生成，但透過 Claude Code 對話協作的建站/改版專案 | Rayter 醫材（WordPress 改版） |

### 工作流程

1. **Agent 自動建站**：客戶透過 LINE 發需求 → Agent 在 Mac mini 生成網站 → `projects/` 記錄管理資料
2. **對話協作**：Joey 在 Claude Code 對話中指示 → 讀取 `projects/` 了解背景 → SSH 到 Mac mini 操作網站 repo
3. **進度追蹤**：所有專案的文件、備份、進度統一在 `projects/` 管理

### 目前客戶專案

| 專案 | 類型 | 狀態 |
|------|------|------|
| **Rayter 醫材** | 手動管理（WordPress 改版） | Phase 1 備份完成，等待 Phase 0 前置作業 |
| **來電司康** | Agent 生成測試案 | 內容準備完成 |
| **巨領企業** | Agent 生成測試案 | 已完成（80+ 分） |
| **酷思迪亞** | 手動管理（活動頁開發） | 開發計畫階段 |

---

## 特殊觸發詞

### 「啟動進化計劃！」
當用戶說這句話時，代表要對 Joey AI Agent 進行功能升級或改進。
- 進入進化任務模式
- 遵循自體進化協議
- 根據安全分級制度執行修改

---

## Hostinger 預覽站（客戶網站部署平台）

> **⚠️ 敏感資訊（API Token、Order ID、帳號）存放在 `.env`，不要寫在這裡。**

### 環境變數（在 `.env` 中設定）

```
HOSTINGER_API_TOKEN=（API Token）
HOSTINGER_ORDER_ID=（主機方案 ID）
HOSTINGER_USERNAME=（主機帳號）
```

### API 使用方式

```bash
# 基本呼叫格式（Token 從環境變數讀取）：
curl -H "Authorization: Bearer $HOSTINGER_API_TOKEN" \
  "https://developers.hostinger.com/api/hosting/v1/websites"
```

- API 文件：https://developers.hostinger.com/
- MCP Server：`hostinger-api-mcp@latest`

### 常用 API 端點

| 操作 | 方法 | 端點 |
|------|------|------|
| 列出所有網站 | GET | `/api/hosting/v1/websites` |
| 建立新網站 | POST | `/api/hosting/v1/websites`（需帶 domain + order_id） |
| 生成免費子網域 | POST | `/api/hosting/v1/domains/free-subdomains`（需帶 order_id） |
| 列出資料中心 | GET | `/api/hosting/v1/datacenters?order_id=` |

### 建立預覽站流程

1. 生成免費子網域：`POST /api/hosting/v1/domains/free-subdomains`
2. 在子網域上建立網站：`POST /api/hosting/v1/websites`
3. 手動到 hPanel 安裝 WordPress（API 目前無此功能）
4. 匯入 All-in-One WP Migration 備份

### 注意事項

- API Token 是敏感資訊，**只存在 `.env` 裡，不進 git**
- WordPress 安裝目前需手動到 hPanel 操作（API 不支援自動安裝 WP）
- 免費子網域名稱是隨機生成的，無法自訂
- 主機位置建議選亞洲（新加坡或馬來西亞）

---

## 素材下載方式（統一使用 Google Drive）

### 重要說明

所有專案素材統一存放於 **Google Drive 公開資料夾**，使用 `gdown` 工具下載。

> ⚠️ **不使用 GitHub 素材庫**（`joey-agent-assets` 已棄用）

### 下載方法

```bash
# 下載整個資料夾
gdown --folder "https://drive.google.com/drive/folders/xxxxxx" -O ./assets

# 下載單一檔案
gdown "https://drive.google.com/uc?id=xxxxxx" -O ./filename.png
```

### 成功條件

| 項目 | 說明 |
|------|------|
| 工具 | `gdown` (Python 包，Mac mini 已安裝 v5.2.1) |
| 認證 | **不需要** OAuth 認證 |
| 必要條件 | Google Drive 連結必須設為「**任何人都可以查看**」 |

### 成功案例

- **space-cat-cafe-v5** (2026-02-03)：成功下載 3 個素材檔案
  - catcoffeelogo.png (1MB)
  - catcoffeemainv.png (8.5MB)
  - catcoffee店內裝潢.png (2.8MB)

### 撰寫提示詞時的素材引用

當協助用戶撰寫要給 Joey AI Agent 執行的 `.md` 提示詞檔案時：

**正確做法**
```markdown
## 素材來源
Google Drive：https://drive.google.com/drive/folders/xxxxxx?usp=sharing

請使用 gdown 下載素材到 ./assets 資料夾：
gdown --folder "上述連結" -O ./assets
```

### 注意事項

- Google Drive MCP 目前**尚未成功配置授權**
- 如需下載私有檔案，需另外設定 OAuth（待研究）
- 公開連結是目前最可靠的方式

---

## 專案架構

```
joey-ai-agent/
│
├── projects/                      # ★ 客戶專案（每個客戶一個資料夾）
│   ├── rayter/                    #   Rayter 醫材官網改版
│   │   ├── docs/                  #     需求文件、content.md、進度追蹤
│   │   ├── backup/                #     REST API JSON、截圖、媒體檔
│   │   └── scripts/               #     備份腳本
│   ├── enscon/                    #   來電司康原始素材
│   ├── enscon-demo/               #   來電司康建站簡報/測試案
│   ├── jiuhliing-cold-storage/    #   巨領企業建站測試案
│   └── acousdea-sleep-fest/       #   酷思迪亞睡眠日活動
│
├── src/                           # ★ Agent 核心程式碼（運行於 Mac mini）
│   ├── main.py                    #   FastAPI 入口 (Level 0)
│   ├── config.py                  #   環境變數設定 (Level 0)
│   ├── api/
│   │   ├── line_webhook.py        #   LINE Webhook (Level 1)
│   │   └── health.py              #   健康檢查
│   ├── services/
│   │   ├── notion_service.py      #   Notion 整合 (Level 1)
│   │   ├── task_processor.py      #   任務處理核心 (Level 1)
│   │   ├── claude_service.py      #   Claude API (Level 2)
│   │   ├── claude_code_service.py #   Claude Code 執行 (Level 1)
│   │   └── line_service.py        #   LINE 推送 (Level 2)
│   ├── models/
│   │   └── claude_response.py     #   資料模型
│   └── prompts/
│       └── system_prompt.md       #   系統提示詞 (Level 2)
│
├── skills/                        # ★ 建站設計系統（三合一）
│   ├── frontend-design/
│   │   └── SKILL.md               #   官方前端設計 Skill (Level 3)
│   ├── ui-ux-pro-max/             #   BM25 設計系統生成器 (Level 3)
│   │   ├── SKILL.md               #     使用說明
│   │   ├── scripts/               #     search.py, design_system.py, core.py
│   │   └── data/                  #     50+ 風格、97 色盤、57 字體組合資料
│   └── templates/
│       ├── base-guidelines.md     #   共用設計原則 (Level 3)
│       ├── manufacturing.md       #   製造業模板 (Level 3)
│       ├── restaurant.md          #   餐廳模板 (Level 3)
│       ├── brand.md               #   品牌官網模板 (Level 3)
│       └── corporate.md           #   企業官網模板 (Level 3)
│
├── docs/                          # ★ 系統級文件（不放客戶專案）
│   ├── 架構說明.md
│   ├── 官網專案資料準備指南.md
│   ├── 建站測試案製作流程（範例參考）.md
│   └── ...
│
├── scripts/                       # 進化控制器等系統腳本
│   ├── evolution_controller.py
│   └── create_evolution_task.py
├── agent-tasks/                   # 進化任務提交
│   ├── submit_evolution.sh
│   └── templates/
│       └── evolution-template.md
├── web-frontend/                  # 前端程式碼 (Level 3)
└── tasks/                         # 任務輸出 (Level 3)
```

### 資料夾分工原則

| 資料夾 | 放什麼 | 不放什麼 |
|--------|--------|----------|
| `projects/` | 客戶專案素材、文件、備份 | 系統程式碼 |
| `docs/` | 系統級指南、架構說明、開發紀錄 | 客戶專案資料 |
| `src/` | Agent 核心程式碼 | 文件、素材 |
| `skills/templates/` | 行業建站模板 | 客戶資料 |

## 建站設計系統（三合一）

建站時使用的設計規範、自動生成工具和品質驗證方法，避免 generic AI 風格。

### 三個 Skill 的角色

| Skill | 功能 | 在 Agent 中的作用 |
|-------|------|-----------------|
| **Frontend Design** | 設計哲學與美學規範 | 避免 AI Slop，確保大膽、有個性的設計 |
| **UI/UX Pro Max** | BM25 設計系統生成器 | 根據專案類型自動生成配色、字體、風格方案 |
| **Superpowers** | 開發最佳實踐（TDD、除錯、驗證） | 系統化驗證流程，提升網站品質 |

### 檔案結構
```
skills/
├── frontend-design/
│   └── SKILL.md              # Claude 官方前端設計 Skill（禁止 generic 美學）
├── ui-ux-pro-max/
│   ├── SKILL.md              # BM25 設計系統生成器使用說明
│   ├── scripts/
│   │   ├── search.py         # 主程式：搜尋風格 + 生成設計系統
│   │   ├── design_system.py  # 設計系統生成邏輯
│   │   └── core.py           # BM25 搜尋核心
│   └── data/                 # 50+ 風格、97 色盤、57 字體組合資料
└── templates/
    ├── base-guidelines.md    # 共用設計原則（字體、配色、排版、動畫）
    ├── manufacturing.md      # 代工廠/製造業模板
    ├── restaurant.md         # 餐廳/咖啡廳模板
    ├── brand.md              # 品牌官網模板
    └── corporate.md          # 企業官網模板
```

### 使用方式
1. `claude_code_service.py` 的 Prompt 已包含指示，會自動要求 Agent：
   - 載入 Frontend Design Skill 設計哲學
   - 執行 UI/UX Pro Max `search.py` 生成設計系統
   - 根據行業選擇對應模板
   - 完成後使用 Superpowers 方法論驗證品質
2. Prompt 中使用 `{SKILLS_DIR}` 佔位符，在執行時替換為 skills/ 的絕對路徑
3. Superpowers plugin 已安裝在 `~/.claude/plugins/repos/superpowers/`

### 核心原則
- **禁止 generic 字體**：Inter、Roboto、Arial、Helvetica
- **禁止 AI slop 配色**：紫色漸層 + 白底
- **必須使用 CSS Variables** 建立一致配色
- **必須選擇大膽的美學方向**，而非中庸的「安全選擇」
- **必須先生成設計系統**再開始建站（UI/UX Pro Max）
- **完成後必須系統化驗證**（Superpowers 方法論）

---

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
| **Level 3** | 自由修改 | web-frontend/, tasks/, agent-tasks/, docs/, projects/ |

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
rsync -avz "/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent/skills/" macmini-remote:~/joey-ai-agent/skills/
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
rsync -avz "/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent/skills/" macmini-remote:~/joey-ai-agent/skills/ && \
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
