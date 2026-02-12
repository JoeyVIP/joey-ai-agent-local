# 耳朵裡的動物園 — 全 AI 開發計畫書（v2.0）

The Zoo Inside Your Ear
2026 世界睡眠月｜沉浸式共創策展
開發技術規劃 v2.0（整合 Claude Code Agent Teams）

---

## 版本更新說明

v2.0 相較 v1.0 的核心變更：
引入 Claude Code Agent Teams（研究預覽版），將原本的「單一 Agent 序列執行」改為「多 Agent 平行協作」。
原計畫 23 個任務需要依序執行，預估 5 週。新計畫透過 Agent Teams 平行化，壓縮至 3 週。

---

## 一、什麼是 Agent Teams，跟原來的做法差在哪

### 原本的做法（v1.0）

一個 Claude Code Session 依序處理任務。
做完任務 A 才能做任務 B，即使 A 和 B 完全不相干。
就像一個超強的工程師，但他一次只能坐在一張桌子前面。

### Agent Teams 的做法（v2.0）

一個 Team Lead（主控 Agent）負責拆解任務、分派工作、彙整結果。
多個 Teammate（平行 Agent）各自有獨立的 Context Window，可以同時開工。
Teammate 之間可以直接互相溝通、共享任務清單、互相 Review。
就像你突然有了一整個開發小組，每個人各自負責一塊，做完會自己對齊。

### 啟用方式

在 Claude Code 的 settings.json 中加入：
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = 1

或者直接在環境變數中設定：
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

### 重要限制與注意事項

目前是 Research Preview，有已知的 Session 恢復與關閉行為問題
每個 Teammate 是獨立的 Claude 實例，Token 費用分開計算，成本會明顯上升
兩個 Teammate 編輯同一個檔案會造成覆寫衝突，必須確保每個 Teammate 負責不同的檔案範圍
不建議讓 Team 長時間無人看管，需要定期 Check-in 確認方向對不對
最適合的場景是「可以明確切分成獨立區塊」的任務

---

## 二、技術架構（與 v1.0 相同）

前端層：Next.js 14 + Tailwind CSS + Framer Motion + PixiJS
後端層：Node.js + Express / Next.js API Routes，部署在 Render
資料層：PostgreSQL + Redis（都在 Render 上）
版本控制：GitHub，main branch 自動部署到 Render

（架構選型的理由已在 v1.0 詳述，此處不重複。）

---

## 三、Agent Teams 的團隊編制設計

整個專案的 Agent Teams 不是一次開到底，而是分階段組建不同編制的 Team。
每個 Phase 根據任務性質，啟動一組 Team，完成後解散，再啟動下一組。

### Phase 0 Team：基礎建設組（1 Lead + 0 Teammate）

不需要 Agent Teams，單一 Session 即可完成。
任務：建立 Next.js 專案、配置 Tailwind、設定 GitHub + Render 部署 Pipeline。
預估時間：半天。

### Phase 1 Team：前端介面組（1 Lead + 3 Teammates）

Lead 負責：建立設計系統（CSS 變數、共用 Layout、字型、背景紋理），這是所有 Teammate 的共用基礎，必須先完成。

Lead 完成設計系統後，啟動三個 Teammate 平行開工：

Teammate A — 首頁工程師
負責檔案：app/page.tsx、components/landing/ 資料夾下所有檔案
工作內容：首頁主視覺區、跑馬燈元件、CTA 按鈕、Mobile First 排版

Teammate B — 測驗流程工程師
負責檔案：app/quiz/ 資料夾下所有檔案、components/quiz/ 資料夾下所有檔案
工作內容：QuizPage 共用元件、五題測驗的翻頁互動、答案暫存 State、Loading 等待頁

Teammate C — 結果頁工程師
負責檔案：app/result/ 資料夾下所有檔案、components/result/ 資料夾下所有檔案
工作內容：結果頁完整版面（Mock Data 版）、動物卡、能量量表、飼育員筆記、下載與分享按鈕

三個 Teammate 的檔案範圍完全不重疊，不會有衝突。
Lead 在三人開工期間負責 Review 進度、確保設計系統的 Token 被正確引用。
預估時間：2 天（Lead 半天建設計系統 + Teammates 平行 1.5 天）。

### Phase 2 Team：後端功能組（1 Lead + 3 Teammates）

Lead 負責：資料庫 Schema 設計與建表（PostgreSQL），這是所有 API 的基礎，必須先完成。

Lead 完成建表後，啟動三個 Teammate 平行開工：

Teammate D — 測驗 API 工程師
負責檔案：app/api/quiz/ 資料夾、lib/ai-text.ts、lib/ai-image.ts
工作內容：POST /api/quiz/submit 端點、AI 文案生成串接（使用提示詞.pdf 的 Prompt）、AI 圖像生成串接、結果寫入資料庫

Teammate E — 認證工程師
負責檔案：app/api/auth/ 資料夾、lib/line-oauth.ts、lib/session.ts
工作內容：LINE OAuth 流程（授權、回調、Token 交換、Profile 取得）、JWT Session 管理、使用者資料寫入

Teammate F — 整合工程師
負責檔案：app/api/islands/ 資料夾、lib/island-routing.ts
工作內容：島嶼分流 API（序列遞補制邏輯）、島嶼狀態查詢 API、Redis 即時人數統計

三個 Teammate 的 API 路由完全獨立。
Lead 在三人完成後，負責前後端串接（將 Phase 1 的靜態頁面接上 Phase 2 的 API）。
預估時間：3 天（Lead 半天建表 + Teammates 平行 2 天 + Lead 半天串接）。

### Phase 3 Team：共創地圖組（1 Lead + 2 Teammates）

共創地圖是技術最複雜的部分，但 Canvas 渲染和 WebSocket 通訊可以平行開發。

Teammate G — Canvas 工程師
負責檔案：components/map/ 資料夾、lib/pixi/ 資料夾
工作內容：PixiJS 畫布初始化、地圖底圖渲染（步道 + 柵欄 + 路標）、動物 Sprite 渲染與點擊互動、平移縮放手勢、視窗裁切效能最佳化

Teammate H — 即時通訊工程師
負責檔案：app/api/socket/ 資料夾、lib/socket-server.ts、lib/socket-client.ts
工作內容：Socket.io Server 建立、入園事件廣播、移動事件同步、互動事件（一起睡 / 拍拍你 / 照照你）、僅推送當前島嶼資料

Lead 負責：在兩個 Teammate 完成後，將 Canvas 渲染層與 WebSocket 資料層對接。然後 Lead 自己處理跨島搜尋飛行動畫（這個功能同時依賴 Canvas 和 Socket，不適合拆給 Teammate）。
預估時間：5 天（Teammates 平行 3 天 + Lead 整合 + 跨島功能 2 天）。

### Phase 4：美術資產生成（獨立平行，不需 Agent Teams）

美術生成不是 Claude Code 的任務，而是透過 AI 圖像生成 API 批量產出。
這個 Phase 可以在 Phase 1 啟動的同一天就開始跑，完全不卡主流程。
產出的圖片在各 Phase 需要時嵌入即可，之前先用佔位圖。

工作內容：
16 到 24 種動物的預生成圖庫（每種 3 到 5 張變體）
共創地圖的裝飾素材（路標、小屋、家具、植物）
首頁與測驗頁的場景插畫（Page 1 到 Page 6 各一張）

預估時間：持續進行，約 3 到 5 天完成全部素材。

### Phase 5 Team：收尾整合組（1 Lead + 2 Teammates）

Teammate I — 社交功能工程師
負責檔案：components/share/ 資料夾、lib/screenshot.ts
工作內容：html2canvas 截圖下載、Web Share API 分享、OG Meta Tags、分享短連結

Teammate J — 即時數據工程師
負責檔案：修改 components/landing/ticker.tsx、components/map/hud.tsx
工作內容：首頁跑馬燈接 WebSocket 真實資料、地圖 HUD 即時人數、底部資訊欄

Lead 負責：Lighthouse 效能最佳化、無障礙檢查、錯誤頁面（404 / 500）、最終部署確認。
預估時間：2 天。

---

## 四、Agent Teams 的 Prompt 範本

以下是每個 Phase 啟動 Agent Team 時，給 Team Lead 的指令範本。
你只需要在 Claude Code 中貼入這段話，Lead 就會自動建立 Team 並分派任務。

### Phase 1 啟動指令範本

---

我正在開發「耳朵裡的動物園」心理測驗網站，使用 Next.js 14 + Tailwind CSS + TypeScript。

請建立一個 Agent Team 來平行開發前端介面：

在開始分派之前，你（Lead）先完成設計系統的建立：
建立 app/globals.css 中的 CSS 變數（品牌色票：米白底色 #FDFAF5、暖棕文字 #5C4B3A、淡黃步道 #F5E6C8、低飽和大地色系）
建立 components/layout/ 中的共用 Layout（Header 含 Logo、Footer）
設定繁體中文字型載入
建立水彩紙紋理的背景 CSS 效果

完成後，啟動三個 Teammate：

Teammate A — 首頁工程師
只負責 app/page.tsx 和 components/landing/ 資料夾
實作首頁主視覺區（貓咪佔位圖 + 主標題「The Zoo Inside Your Ear 耳朵裡的動物園」+ 副文案 + 跑馬燈 + CTA 按鈕「躡手躡腳跟進去」）
Mobile First，支援 375px 到 428px

Teammate B — 測驗流程工程師
只負責 app/quiz/ 和 components/quiz/ 資料夾
建立可復用的 QuizPage Component，五題測驗翻頁互動，答案暫存在 Zustand Store
最後一題送出後導向 /loading
Loading 頁面顯示「AI 正在繪製你的動物」動畫（模糊剪影 + 呼吸光暈）

Teammate C — 結果頁工程師
只負責 app/result/ 和 components/result/ 資料夾
使用 Mock Data 建立完整結果頁：動物主視覺、角色名稱、金句、Hashtags、能量量表（腦內噪音 + 社交電力滑桿）、飼育員筆記區、三個按鈕

請確保三個 Teammate 不碰彼此的檔案範圍，避免衝突。

---

### Phase 2 啟動指令範本

---

前端介面已完成。現在建立後端功能。

你（Lead）先完成資料庫建表：
連線到 PostgreSQL（DATABASE_URL 在 .env 中）
建立 users、quiz_results、islands、island_assignments 四張表

完成後，啟動三個 Teammate：

Teammate D — 測驗 API 工程師
只負責 app/api/quiz/ 和 lib/ai-text.ts、lib/ai-image.ts
實作 POST /api/quiz/submit
System Prompt 使用以下內容（貼入提示詞.pdf 的完整 Prompt）
AI 回傳 JSON 格式：animal_type、animal_name、tagline、hashtags（陣列）、note_text、noise_level（1-10）、social_level（1-10）
串接圖像生成 API，將結果存入 quiz_results 表

Teammate E — 認證工程師
只負責 app/api/auth/ 和 lib/line-oauth.ts、lib/session.ts
實作 LINE Login OAuth 2.0 全流程
環境變數：LINE_CHANNEL_ID、LINE_CHANNEL_SECRET、LINE_CALLBACK_URL
授權成功後寫入 users 表，設定 JWT Cookie

Teammate F — 島嶼分流工程師
只負責 app/api/islands/ 和 lib/island-routing.ts
實作序列遞補制分流邏輯（Soft Cap 2000、Hard Cap 2200）
Redis 儲存各島即時人數
API：POST /api/islands/assign（分配島嶼）、GET /api/islands/search（搜尋朋友所在島嶼）

三個 Teammate 完成後，你（Lead）負責將前端頁面的 Mock Data 替換為真實 API 呼叫。

---

### Phase 3 啟動指令範本

---

前後端基礎功能已完成。現在開發共創地圖。

啟動兩個 Teammate：

Teammate G — Canvas 工程師
只負責 components/map/ 和 lib/pixi/
使用 PixiJS（@pixi/react）建立 Page 9 共創地圖
實作：畫布初始化、米白色底圖、淡黃步道、白色柵欄、手繪風路標（SVG）
動物 Sprite 渲染（接收座標陣列，每隻動物顯示為對應種類的小圖示）
點擊自己的動物顯示 📍 You，點擊他人跳出暱稱與金句氣泡
支援平移（Pan）和捏合縮放（Pinch Zoom）
視窗裁切：只渲染可見範圍內的 Sprite

Teammate H — 即時通訊工程師
只負責 app/api/socket/ 和 lib/socket-server.ts、lib/socket-client.ts
建立 Socket.io Server
事件類型：animal:join（入園）、animal:move（移動）、animal:interact（互動）、island:stats（人數更新）
只推送當前島嶼的事件，使用 Socket.io Room 隔離
Redis Adapter 處理多 Instance 同步

兩個 Teammate 完成後，你（Lead）負責：
將 Canvas 層與 Socket 層對接（Socket 收到事件後更新 PixiJS Sprite 位置）
實作跨島搜尋與飛行動畫（Zoom Out → Pan → Zoom In）
實作 HUD 懸浮欄（島嶼編號 + 人數 + 切換按鈕）

---

## 五、修訂版時程

### 第 1 週

Day 1：Phase 0（專案初始化）+ Phase 4 啟動（美術素材開始批量生成）
Day 2-3：Phase 1 Team 執行（前端介面，Lead + 3 Teammates 平行）
Day 4-5：Phase 2 Team 執行（後端功能，Lead + 3 Teammates 平行）

### 第 2 週

Day 6-10：Phase 3 Team 執行（共創地圖，Lead + 2 Teammates 平行 + Lead 整合）
Phase 4 持續進行，素材陸續到位後替換佔位圖

### 第 3 週

Day 11-12：Phase 5 Team 執行（收尾整合，Lead + 2 Teammates 平行）
Day 13-15：整合測試、Bug 修復、效能最佳化、最終部署

總計 3 週，相比 v1.0 的 5 週縮短了 40%。

---

## 六、Token 成本預估

Agent Teams 的每個 Teammate 都是獨立的 Claude 實例，Token 分開計費。
以下是粗略的成本預估（以 Opus 4.6 定價 $5/$25 per M tokens 計算）。

Phase 1：Lead + 3 Teammates = 4 個實例 x 約 2 小時 Session
Phase 2：Lead + 3 Teammates = 4 個實例 x 約 3 小時 Session
Phase 3：Lead + 2 Teammates = 3 個實例 x 約 5 小時 Session
Phase 5：Lead + 2 Teammates = 3 個實例 x 約 2 小時 Session

如果要控制成本，可以讓 Teammates 使用 Sonnet 4.5（較便宜），只有 Lead 使用 Opus 4.6。
在 Team 啟動指令中可以指定：「Use Sonnet for each teammate.」

另一個省錢策略：Phase 1 和 Phase 5 的任務相對單純，可以不用 Agent Teams，改回單一 Session 依序處理。只在 Phase 2（後端三條 API 完全獨立）和 Phase 3（Canvas + Socket 完全獨立）使用 Agent Teams，這樣只增加兩次 Team 的成本，但仍然能拿到大部分的時間壓縮效益。

---

## 七、v1.0 vs v2.0 對比

### 開發時間

v1.0：5 週（23 個任務序列執行）
v2.0：3 週（同樣 23 個任務，但透過 Agent Teams 平行化）

### 自動化比例

v1.0：75% 到 80%
v2.0：80% 到 85%（Agent Teams 的 Lead 自動協調減少人工調度時間）

### 人工介入頻率

v1.0：每完成一個任務需要人工 Review 再啟動下一個
v2.0：每完成一個 Phase 才需要人工 Review，Phase 內部由 Lead 自動協調

### Token 成本

v1.0：較低（一次只跑一個 Session）
v2.0：約為 v1.0 的 2 到 3 倍（多個平行 Session）

### 風險

v1.0：風險較低，每步可控
v2.0：檔案衝突風險（需嚴格切分 Teammate 的檔案範圍）、Lead 協調失誤風險（需明確的 Prompt）

---

## 八、建議的混合策略（推薦方案）

不是每個 Phase 都需要用 Agent Teams。
根據「任務是否可平行 + 成本效益」來決定。

Phase 0 → 單一 Session（任務太簡單，不值得開 Team）
Phase 1 → Agent Teams（三個頁面完全獨立，平行效益高）
Phase 2 → Agent Teams（三條 API 完全獨立，平行效益最高）
Phase 3 → Agent Teams（Canvas + Socket 獨立，但 Lead 整合工作量大）
Phase 4 → 不用 Claude Code（美術用圖像 API 批量生成）
Phase 5 → 單一 Session 或小型 Team（任務量不大）

這樣可以在「時間壓縮」和「成本控制」之間取得最佳平衡。

---

## 九、操作流程 SOP

以下是你每天實際操作的步驟。

Step 1：開啟 Claude Code，確認 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 已啟用
Step 2：貼入該 Phase 的啟動指令範本（本文件第四節）
Step 3：確認 Lead 建立的 Team 結構合理，按確認啟動
Step 4：用 Shift+Up/Down 在 Teammates 之間切換，觀察進度
Step 5：如果某個 Teammate 卡住或方向偏了，直接傳訊息給它修正
Step 6：Team 完成後，推送到 GitHub，等 Render 自動部署
Step 7：開手機瀏覽器做 Smoke Test（頁面有沒有壞、功能有沒有通）
Step 8：如果有問題，開新的 Session 把錯誤訊息貼進去要求修復
Step 9：進入下一個 Phase，重複 Step 2

每天預估操作時間：1 到 2 小時（主要是 Step 4 的觀察和 Step 7 的測試）。

---

## 十、環境變數清單（需人工配置，與 v1.0 相同）

CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = 1
LINE_CHANNEL_ID
LINE_CHANNEL_SECRET
LINE_CALLBACK_URL
AI_TEXT_API_KEY
AI_IMAGE_API_KEY
DATABASE_URL
REDIS_URL
NEXT_PUBLIC_SOCKET_URL
SESSION_SECRET
