# 進化觸發指令：Web Frontend 自主開發

> 複製下方內容，發送到 LINE，Agent 就會開始自主進化

---

## 觸發指令（發送這段到 LINE）

```
🧬 啟動進化計畫：Web Frontend 自主開發

請執行以下自主進化任務：

1. 閱讀計畫文件
   路徑：/Users/joeyserver/joey-ai-agent/docs/web-frontend-development-plan.md
   （如果不存在，請從 GitHub 同步最新版本）

2. 分析計畫內容，理解：
   - 專案目標
   - 技術架構
   - 實作階段

3. 自主決定執行順序，從 Phase 1 開始：
   - Phase 1：後端資料庫與 API
   - Phase 2：進度回報機制
   - Phase 3：前端專案建立
   - Phase 4：整合測試
   - Phase 5：部署

4. 執行開發工作：
   - 每完成一個階段，記錄到 Notion
   - 遇到問題自行解決或記錄
   - 完成後進入下一階段

5. 最終交付：
   - GitHub repo URL
   - Render 部署 URL
   - 完整的專案文檔

注意：這是自主進化任務，請獨立完成，不需要人工介入。
```

---

## 分階段觸發（如果整個太大）

### Phase 1 觸發
```
🧬 進化任務：Web Frontend Phase 1 - 後端 API

閱讀 /Users/joeyserver/joey-ai-agent/docs/web-frontend-development-plan.md

執行 Phase 1：後端資料庫與 API
- 新增 PostgreSQL 連線設定
- 建立 SQLAlchemy models
- 實作 GitHub OAuth 端點
- 實作專案 CRUD API
- 實作 SSE 進度端點
- 實作檔案上傳 API

完成後更新 Notion 記錄。
```

### Phase 2 觸發
```
🧬 進化任務：Web Frontend Phase 2 - 進度回報

繼續 Web Frontend 開發計畫

執行 Phase 2：進度回報機制
- 修改 claude_code_service.py 支援進度回報
- 建立 web_task_processor.py
- 實作進度寫入資料庫邏輯
- 測試 SSE 連線

完成後更新 Notion 記錄。
```

### Phase 3 觸發
```
🧬 進化任務：Web Frontend Phase 3 - 前端開發

繼續 Web Frontend 開發計畫

執行 Phase 3：前端專案建立
- 初始化 Next.js 14 專案
- 設定 Tailwind CSS + shadcn/ui
- 實作 GitHub OAuth 登入
- 建立儀表板頁面
- 建立多步驟表單
- 建立即時進度監控頁面

完成後更新 Notion 記錄。
```

### Phase 4-5 觸發
```
🧬 進化任務：Web Frontend Phase 4-5 - 整合與部署

繼續 Web Frontend 開發計畫

執行 Phase 4：整合測試
執行 Phase 5：部署到 Render

完成後提供：
- GitHub repo URL
- Render 部署 URL
```

---

## 使用建議

1. **完整版**：如果你相信 Agent 能一次完成，發送完整觸發指令
2. **分階段版**：如果想更可控，一個 Phase 一個 Phase 發送
3. **監控進度**：每個任務完成後會有 Notion 記錄

---

## 前置條件

確保 Mac mini 上有這個計畫文件：
```bash
# 同步計畫文件到 Mac mini
rsync -avz "/Users/JoeyLiao/Joey-AI-Agent/docs/web-frontend-development-plan.md" macmini-remote:~/joey-ai-agent/docs/
```
