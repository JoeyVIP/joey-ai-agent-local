# LINE 用量最佳化計畫

## 背景問題

目前每個任務會發送多則 LINE 訊息：
1. 任務建立通知 (Push)
2. 進度更新 (Push)
3. 完成通知 (Push)

LINE Messaging API 的 Push Message 有免費額度限制，超過要收費。

## 解決方案

**核心概念**：只用 Reply（免費），把後續資訊移到網頁

```
用戶傳訊息 → Agent 只回覆一則訊息（含追蹤網址）→ 用戶自己去網頁看進度
```

---

## 執行計畫

### Phase 1: 建立任務狀態頁面

**目標**：建立可以即時顯示任務狀態的網頁

**修改範圍**：
- [ ] `src/api/task_status.py` (新增) - 任務狀態 API
- [ ] `web-frontend/task/[id].html` (新增) - 任務狀態頁面

**頁面需顯示**：
- 任務建立時間
- 原始指令內容
- 目前狀態（處理中 / 已完成 / 失敗）
- 執行步驟與進度
- 最終結果或產出
- 完成時間

**技術方案**：
- 使用 SSE (Server-Sent Events) 或輪詢實現即時更新
- 頁面部署在現有的 Mac mini 服務上

**安全等級**：Level 3（web-frontend）+ Level 1（新增 API endpoint）

---

### Phase 2: 修改 LINE 回覆機制

**目標**：改用 Reply 取代 Push，只發一則訊息

**修改範圍**：
- [ ] `src/api/line_webhook.py` - 改用 reply 而非 push
- [ ] `src/services/task_processor.py` - 移除中途 LINE 通知
- [ ] `src/services/line_service.py` - 新增 reply_message 方法

**回覆格式**：
```
收到，正在處理「{任務摘要}」
追蹤進度：https://joey-agent.xxx.com/task/{task_id}
```

**安全等級**：Level 1

---

### Phase 3: 任務 ID 與狀態管理

**目標**：建立任務追蹤機制

**修改範圍**：
- [ ] `src/models/task.py` (新增) - 任務資料模型
- [ ] `src/services/task_store.py` (新增) - 任務狀態儲存

**Task ID 格式**：
- 短碼：`abc123`（6 字元，方便網址）
- 對應 Notion page ID

**狀態流轉**：
```
received → processing → completed / failed
```

**安全等級**：Level 2

---

### Phase 4: 簡單任務判斷

**目標**：極簡單任務直接回覆，不需追蹤頁面

**判斷標準**：
- Claude 分析結果為 `simple` 且預估 10 秒內完成
- 例如：「現在幾點」「今天天氣」

**修改範圍**：
- [ ] `src/services/task_processor.py` - 新增簡單任務直接回覆邏輯

**安全等級**：Level 1

---

## 執行順序

```
Day 1 上午：Phase 1 - 建立任務狀態頁面
Day 1 下午：Phase 3 - 任務 ID 與狀態管理
Day 2 上午：Phase 2 - 修改 LINE 回覆機制
Day 2 下午：Phase 4 - 簡單任務判斷 + 整合測試
```

---

## 驗證方式

1. 發送任務訊息到 LINE
2. 確認只收到一則回覆（不是 push）
3. 點擊追蹤網址，確認頁面正常顯示
4. 等待任務完成，確認網頁即時更新
5. 確認 LINE 沒有收到任何後續訊息

---

## 預期效果

| 項目 | 優化前 | 優化後 |
|------|--------|--------|
| LINE 訊息數/任務 | 2-3 則 | 1 則 |
| Push Message 用量 | 高 | 0 |
| Reply 用量 | 0 | 1 |
| 月費成本 | 可能超額 | 完全免費 |

---

## 風險與備案

**風險**：用戶可能忘記去看網頁
**備案**：重要任務完成後，仍可選擇性發送一則 Push 通知（但預設關閉）

**風險**：任務狀態頁面服務中斷
**備案**：使用 Render 或 Railway 部署獨立前端，與 Agent 服務分離
