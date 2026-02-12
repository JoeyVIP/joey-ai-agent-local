# 耳朵裡的動物園 — 全 AI 開發計畫書

The Zoo Inside Your Ear
2026 世界睡眠月｜沉浸式共創策展
開發技術規劃 v1.0

---

## 一、專案現況盤點

以下是目前手上已備齊的資產清單，以及各自在開發流程中的角色定位。

心理測驗題目.pdf
已鎖定 Q1 至 Q5 共五題，每題四個選項（ABCD），涵蓋入口狀態、背景雜訊、動物接觸、隨身行李、最終願望，不需要再做內容修改，可直接轉換為前端資料結構。

提示詞.pdf
包含測驗結果頁的 AI 文案生成 Prompt，定義了角色設定（療癒繪本旁白）、語氣風格（北歐繪本風、去病理化、無說教感）、輸入解讀邏輯（五題對應五個心理維度）、寫作規則（60 到 80 字、起承合結構）以及三組 Few-Shot 範例。這份 Prompt 是後端串接 AI 文案生成的核心素材。

專案企劃規格書.pdf
完整的 Page 1 到 Page 9 頁面規格，涵蓋每一頁的視覺畫面描述、文案內容、互動邏輯與 UI 元件規格。其中首頁跑馬燈、測驗翻頁、LINE 綁定閘門、結果頁（動物卡 + 飼育員筆記 + 能量量表）、共創地圖（動物園設施 + 非語言社交 + 跨島傳送）都有詳細的設計說明。

分流機制.pdf
群島系統的技術邏輯，包含每島 2,000 人的 Soft Cap、2,200 人的 Hard Cap、序列遞補制分配規則、島嶼 HUD 介面設計、跨島搜尋與傳送的四步驟演出流程、Socket 連線只接收當前島嶼資料的效能策略、低於 500 人的島嶼優先遞補回收機制。

睡眠日提案企劃.pdf
提案簡報，包含視覺風格參考圖（首頁風格 x 3、測驗結果頁面 x 3、動物插畫風格 x 6、人物插畫風格 x 3、共創地圖風格 x 2），以及服務範疇定義（核心體驗建置、數位行銷素材、實體接觸點設計）。

---

## 二、技術架構總覽

整體系統拆成三層，每一層對應不同的開發工具與部署策略。

### 前端層 Frontend

框架選擇：Next.js 14（App Router）
理由：支援 SSR 與 SSG 混合、圖片最佳化、API Routes 可直接充當輕量後端。測驗頁面（Page 1 到 Page 6）以靜態生成為主，結果頁（Page 8）與共創地圖（Page 9）需要動態渲染。

樣式方案：Tailwind CSS + Framer Motion
理由：Tailwind 對應企劃書中「乾淨白底、低飽和度大地色系」的視覺需求，用 CSS 變數管理品牌色票。Framer Motion 處理翻頁轉場、入園降落動畫、跨島飛行的 Zoom Out / Pan / Zoom In 鏡頭語言。

畫布引擎（共創地圖）：PixiJS 或 Phaser
理由：Page 9 共創地圖需要在單一畫布上渲染數百隻動物角色、處理點擊互動與平移縮放。Canvas 渲染效能遠優於 DOM 操作。PixiJS 輕量且與 React 整合成熟（使用 @pixi/react）。

### 後端層 Backend

框架選擇：Node.js + Express（或 Next.js API Routes）
部署在 Render Web Service 上，負責以下職責：

API 端點一：測驗提交
接收使用者的五題答案（Q1 到 Q5 各一個 A/B/C/D），呼叫 AI 模型產生測驗結果文案（動物名稱、金句、Hashtags、飼育員筆記），同時呼叫 AI 圖像生成 API 產生動物插圖，將結果寫入資料庫後回傳。

API 端點二：LINE OAuth
處理 LINE Login 的 OAuth 2.0 流程（授權碼交換、取得 Profile），綁定使用者身份。

API 端點三：地圖即時資料
透過 WebSocket（Socket.io）推送當前島嶼的動物位置、互動事件（一起睡、拍拍你、照照你）。僅推送使用者所在島嶼的資料以控制頻寬。

API 端點四：島嶼分流
根據序列遞補制邏輯，為新入園者分配島嶼編號、處理跨島搜尋請求。

### 資料層 Database

主要資料庫：PostgreSQL（Render 原生支援）
儲存使用者帳號（LINE Profile）、測驗結果（答案組合、動物類型、文案內容、圖像 URL）、島嶼分配紀錄。

即時狀態：Redis（Render 原生支援）
儲存各島嶼的即時人數統計、動物當前座標位置、線上狀態。作為 Socket.io 的 Adapter 實現多 Instance 間的訊息同步。

靜態檔案：Render Static Site 或 Cloudflare R2
儲存 AI 生成的動物圖像、結果頁截圖、行銷素材。

---

## 三、AI 生成流程設計

這是本專案的核心差異化能力，需要特別拆細。

### 3A. AI 文案生成

觸發時機：使用者完成 Q1 到 Q5 送出答案後。

輸入格式：
將使用者的五題答案轉換為結構化描述，例如 Q1=D（放鬆型）、Q2=A（思緒混亂）、Q3=C（渴望陪伴）、Q4=C（責任壓力）、Q5=D（需要放鬆）。

System Prompt：
直接使用「提示詞.pdf」中的完整 Prompt，包含角色設定、語氣風格、輸入解讀邏輯、寫作規則與 Few-Shot 範例。

輸出格式要求 AI 回傳 JSON：
角色名稱（例如「已讀不回樹懶」）、動物種類（例如「樹懶」）、金句（例如「我不是不回，只是動作比較慢...」）、三個 Hashtag、飼育員筆記（60 到 80 字）、腦內噪音指數（1 到 10）、社交電力指數（1 到 10）。

模型選擇：Claude Sonnet 4 或同等級模型，溫度設定 0.7 到 0.8 以確保文案有變化但不失控。

### 3B. AI 圖像生成

觸發時機：與文案生成同步或接續觸發。

Prompt 結構：
根據企劃書定義的視覺風格——白底水彩紙紋理、手繪蠟筆質感（Crayon + Gouache）、拙趣非寫實比例、低飽和度大地色系——組裝圖像 Prompt。

範例 Prompt 模板：
「A [動物種類] drawn in clumsy crayon and gouache style on white watercolor paper texture. The animal is in a relaxed liquid-like pose, melting onto a [家具]. Warm muted earth tones, low saturation. Children's picture book illustration style similar to Rifle Paper Co. White background with visible paper grain. No text.」

模型選擇：可選用 DALL-E 3、Midjourney API、Stable Diffusion XL，或 Ideogram 等。建議優先測試 DALL-E 3（API 整合最簡單）與 Ideogram（風格一致性較好）。

品質控制：
生成後需要做風格一致性檢查。可以預先準備 10 到 15 種常見動物的 Seed Prompt，測試通過後鎖定 Prompt 模板。上線後以動物種類作為變數帶入模板即可。

### 3C. 預生成 vs 即時生成的策略選擇

考量到萬人同時在線的場景，建議採用「混合策略」：

預生成池（推薦主力方案）：
事先定義 16 到 24 種動物類型（對應 Q1 到 Q5 的主要組合群集），每種動物預先用 AI 生成 3 到 5 張風格一致的插圖，以及 5 到 8 組飼育員筆記文案。使用者完成測驗後，系統根據答案組合對應到最接近的動物類型，從預生成池中隨機抽取一組圖文。

即時生成（加分項）：
僅在使用者的答案組合落在預生成池未覆蓋的邊緣情境時觸發。或者作為 V2 版本的升級功能，讓每位使用者都得到完全獨一無二的結果。

這個策略的好處是，大幅降低即時 API 成本與回應延遲，同時維持「AI 生成」的行銷賣點。預生成的過程本身就是 AI 產出的。

---

## 四、分段開發任務拆解

以下將整個專案拆成可獨立執行的開發任務，每個任務都設計成 Claude Code Agent 可以在單次 Session 內完成的粒度。任務之間有明確的前後相依關係。

### Phase 0：專案初始化（1 個任務）

任務 0-1：Repository 建立與基礎架構
建立 Next.js 14 專案，配置 Tailwind CSS、TypeScript、ESLint，設定 GitHub Repository，建立 Render 部署 Pipeline（Web Service 連結 GitHub main branch），確認推送後能自動部署成功。產出一個顯示「耳朵裡的動物園 — 建置中」的 Hello World 頁面。

完成標準：推送至 GitHub 後 Render 自動部署，瀏覽器可見頁面。

### Phase 1：靜態頁面與測驗流程（5 個任務）

任務 1-1：設計系統建立
定義全站 CSS 變數（品牌色票、字型、間距系統），建立共用 Layout Component（Header Logo、Footer），設定字型載入（思源體或類似的繁體中文字型），建立水彩紙紋理的背景 CSS 效果（使用 CSS noise filter 或 SVG filter 模擬紙紋）。

完成標準：所有後續頁面能直接引用設計系統的 Token，背景紋理效果在行動裝置上也能流暢渲染。

任務 1-2：首頁 Page 1
實作主視覺區（貓咪佔位圖 + 主標題 + 副文案）、跑馬燈元件（模擬即時入園動態，初期用假資料驅動，後續接 API）、CTA 按鈕「躡手躡腳跟進去」。頁面需為 Mobile First 設計，行動版寬度 375px 至 428px。

完成標準：首頁在手機瀏覽器上排版正確，跑馬燈持續滾動，CTA 可點擊導向 Q1。

任務 1-3：測驗頁面 Page 2 到 Page 6
建立可復用的 QuizPage Component，接收題目文案與選項陣列作為 Props。實作翻頁式互動（使用者點選選項後自動滑到下一題），將五題的答案暫存在前端 State（React Context 或 Zustand）。最後一題送出後導向 Loading 頁。

完成標準：五題可完整作答，答案正確儲存在前端 State，翻頁動畫流暢。

任務 1-4：Loading 等待頁 Page 7 前半段
在使用者按下最後一題的選項到結果產出之間，顯示「AI 正在繪製你的動物」的等待畫面。可使用企劃書中「模糊動物剪影 + 呼吸光暈」的視覺設計。這是純前端動畫頁面。

完成標準：Loading 動畫至少能持續播放 5 到 15 秒而不卡頓，畫面質感符合品牌調性。

任務 1-5：結果頁 Page 8（靜態版）
先用假資料建立結果頁的完整版面，包含動物主視覺區、角色名稱與金句、Hashtags、能量量表（腦內噪音 + 社交電力）、飼育員筆記區、三個按鈕（驗票入園 / 下載通行證 / 分享邀請函）。此階段不串接 API，使用 Mock Data 填充所有欄位。

完成標準：結果頁視覺完整呈現，所有區塊排版正確，可做為後續 API 串接的外殼。

### Phase 2：後端核心功能（5 個任務）

任務 2-1：資料庫 Schema 設計與建立
在 Render PostgreSQL 上建立所需的 Table。users 表（line_user_id、display_name、avatar_url、created_at），quiz_results 表（user_id、answers_json、animal_type、animal_name、tagline、hashtags、note_text、noise_level、social_level、image_url、created_at），islands 表（island_id、current_count、status、created_at），island_assignments 表（user_id、island_id、position_x、position_y、assigned_at）。

完成標準：所有 Table 建立完成，可透過 SQL Client 確認結構正確。

任務 2-2：測驗結果 API
建立 POST /api/quiz/submit 端點，接收五題答案，呼叫 AI 文案生成（使用提示詞.pdf 的 Prompt），回傳結構化的測驗結果 JSON。此階段先不串圖像生成，圖像欄位回傳預設佔位圖 URL。

完成標準：透過 Postman 或 curl 送出測驗答案，能收到格式正確的 JSON 回應，文案風格符合提示詞規範。

任務 2-3：AI 圖像生成串接
在測驗結果 API 中加入圖像生成流程。根據 AI 文案回傳的動物種類，組裝圖像 Prompt，呼叫圖像生成 API，將回傳的圖像上傳至靜態儲存（Cloudflare R2 或 Render），將 URL 寫入資料庫。

完成標準：測驗提交後能回傳一張風格正確的動物圖像 URL，圖像可在瀏覽器正常載入。

任務 2-4：LINE OAuth 整合
建立 LINE Login 的 OAuth 流程。前端點擊「點亮微光」按鈕後導向 LINE 授權頁，授權回調後後端用 Authorization Code 換取 Access Token，取得使用者 Profile（userId、displayName、pictureUrl），寫入 users 表，設定 Session（JWT Cookie）。

完成標準：完整跑通 LINE 登入流程，登入後能取得使用者 LINE Profile。

任務 2-5：前後端串接
將 Phase 1 的靜態頁面與 Phase 2 的 API 串接。測驗完成後呼叫 submit API，Loading 頁面改為監聽 API 回應狀態，結果頁改為使用 API 回傳的真實資料渲染。LINE 登入閘門嵌入 Page 7 流程中（先登入再看結果，或先看結果再提示登入以「入園」）。

完成標準：使用者可完整走過「首頁 → 測驗 → LINE 登入 → 等待 → 結果頁」的全流程。

### Phase 3：共創地圖（6 個任務）

這是整個專案中技術複雜度最高的部分，需要拆得更細。

任務 3-1：Canvas 地圖基礎
使用 PixiJS 建立 Page 9 的基礎畫布，實作平移（Pan）與縮放（Pinch Zoom）的手勢控制。繪製米白色背景紋理、淡黃色遊園步道、低矮白色木柵欄等靜態地圖元素。

完成標準：可在手機上流暢地滑動與縮放地圖，靜態元素渲染正確。

任務 3-2：動物角色渲染
定義動物 Sprite 的資料結構（位置、種類、動畫狀態），實作動物角色在畫布上的渲染邏輯。點擊自己的動物顯示「📍 You」標記，點擊他人的動物跳出暱稱與金句氣泡。

完成標準：畫布上可同時渲染 50 隻以上的動物角色且不掉幀，點擊互動正常。

任務 3-3：WebSocket 即時同步
建立 Socket.io Server，實作「入園」事件（新動物降落動畫）、「移動」事件（點擊空地後動物走過去）、「互動」事件（一起睡、拍拍你、照照你）的即時廣播。僅廣播同島嶼的事件。

完成標準：開兩個瀏覽器分頁，一邊操作動物移動，另一邊能即時看到對方的移動。

任務 3-4：島嶼分流系統
實作序列遞補制的分流邏輯。新使用者入園時，系統查詢 Redis 中各島嶼的即時人數，分配到第一個未滿的島嶼。實作 HUD 懸浮欄（當前島嶼編號 + 人數 + 切換按鈕）。

完成標準：模擬 100 個使用者入園，第 1 到 2000 個分配到 Island 001，超出後自動開啟 Island 002。

任務 3-5：跨島搜尋與傳送
實作搜尋框輸入朋友 ID、系統判斷同島或不同島、不同島時執行 Zoom Out → Pan → Zoom In 的跨島飛行動畫、抵達後 HUD 更新為「訪客」狀態。

完成標準：輸入朋友 ID 後能正確跳轉到對方所在的島嶼，飛行動畫流暢。

任務 3-6：地圖裝飾與最佳化
加入園區路標（手繪風格 SVG）、設施小屋（售票亭、補給站）、家具棲息地（懶骨頭山、搖籃椅鳥巢）等裝飾元素。針對行動端做效能最佳化（視窗外的 Sprite 不渲染、遠距動物降低細節層級）。

完成標準：地圖視覺豐富度達到企劃書要求，手機端 FPS 穩定在 30 以上。

### Phase 4：美術資產生成（3 個任務）

這一階段專門處理「全 AI 美術」的產出與品控。

任務 4-1：動物預生成池
根據 Q1 到 Q5 的組合群集，定義 16 到 24 種動物類型。為每種動物撰寫圖像 Prompt 模板，批量呼叫 AI 圖像 API 生成每種動物 3 到 5 張變體。人工挑選（或用 AI 評分）風格最一致的版本入庫。

完成標準：至少 16 種動物，每種至少 3 張可用圖像，風格統一為蠟筆水彩白底。

任務 4-2：地圖靜態素材生成
用 AI 生成共創地圖所需的靜態裝飾素材，包含園區路標、設施小屋、家具棲息地、樹木花草等。統一為手繪蠟筆風格 + 透明底 PNG。

完成標準：地圖所有裝飾素材就位，風格與動物角色一致。

任務 4-3：首頁與測驗頁插畫生成
用 AI 生成企劃書中描述的各頁插畫，包含首頁的軟爛貓咪主視覺、Q1 的拱門場景、Q2 的聲音波浪線、Q3 的灌木叢小動物、Q4 的誇張背包、Q5 的舒適樹洞。

完成標準：Page 1 到 Page 6 各有一張主插畫，風格符合「拙趣、蠟筆、白底」的品牌調性。

### Phase 5：行銷素材與收尾（3 個任務）

任務 5-1：分享與下載功能
實作結果頁的「下載通行證」按鈕（使用 html2canvas 將結果頁截圖為圖片）、「分享邀請函」按鈕（Web Share API 或產生分享短連結）。圖片需包含品牌 Logo 與 QR Code。

完成標準：下載的圖片在社群平台上傳後可正常顯示，分享連結可正確導回首頁。

任務 5-2：跑馬燈與即時統計
將首頁跑馬燈從假資料改接 WebSocket 即時資料，顯示真實的入園動態與總人數統計。底部資訊欄顯示「全島嶼夢遊中：X 隻」。

完成標準：首頁即時顯示最新入園的動物暱稱，總人數持續更新。

任務 5-3：SEO、效能、無障礙最終檢查
設定 Open Graph Meta Tags（分享預覽圖與文案）、行動端 Lighthouse 跑分最佳化（目標 Performance 70 分以上）、基礎無障礙標籤（alt text、aria-label）、錯誤頁面（404、500）設計。

完成標準：社群分享預覽正確，Lighthouse 各項指標合格。

---

## 五、Claude Code Agent 自動化策略

### 任務轉譯原則

每個任務在交給 Claude Code Agent 執行時，需要包含以下結構：

Context（脈絡）：專案目前的狀態、已完成的前置任務、相關的設計規格文字。
Objective（目標）：這個任務要達成的具體產出。
Constraints（限制）：技術選型（框架、函式庫版本）、風格規範（CSS Token）、檔案命名慣例。
Acceptance Criteria（驗收標準）：可量化或可觀察的完成條件。
Reference（參考）：相關的企劃書段落或 Prompt 片段。

### 任務依賴關係圖

Phase 0 → Phase 1（全部）→ Phase 2（2-1 到 2-3 可與 Phase 1 平行）→ Phase 2-5 → Phase 3（全部）→ Phase 5
Phase 4 可與 Phase 1 到 Phase 3 完全平行執行，因為美術素材生成不依賴程式碼。

Phase 4 的產出物（圖像檔案）在 Phase 1-2（首頁主視覺）、Phase 1-3（測驗頁插畫）、Phase 3-6（地圖裝飾）時嵌入前端。如果 Phase 4 尚未完成，前端可先使用佔位圖。

### 預估自動化比例

Phase 0 → 自動化 95%（Claude Code 可獨立完成 Scaffolding）
Phase 1 → 自動化 80%（視覺微調可能需要人工確認截圖後回饋修改指令）
Phase 2 → 自動化 85%（API 邏輯 Claude Code 擅長，LINE OAuth 需要人工提供 Channel ID 等密鑰）
Phase 3 → 自動化 60%（Canvas 互動與 WebSocket 同步邏輯較複雜，需要較多的人工測試與回饋迭代）
Phase 4 → 自動化 70%（AI 圖像生成是自動的，但品質篩選需要人眼判斷）
Phase 5 → 自動化 90%

整體預估：自動化約佔 75% 至 80%，人工介入主要集中在視覺品質確認、密鑰配置與 Canvas 互動測試。

---

## 六、風險管理與替代方案

### 風險一：AI 圖像風格不一致

問題：不同次生成的動物圖像可能風格差異過大，影響品牌質感。
對策：採用預生成池策略，人工挑選風格最一致的圖像。撰寫嚴格的 Negative Prompt 排除不要的風格（如寫實、3D、動漫）。若單一模型不穩定，可交叉使用多個模型生成後挑選。

### 風險二：萬人同時在線的效能瓶頸

問題：共創地圖如果有超過 2000 人同時在同一島嶼操作，WebSocket 廣播量會很大。
對策：嚴格執行 Soft Cap 2000 人 / Hard Cap 2200 人的分流機制。在 Canvas 端做視窗裁切（Viewport Culling），只渲染可見範圍內的 Sprite。WebSocket 事件做 Throttle（每秒最多 10 次位置更新）。

### 風險三：LINE OAuth 流程中斷

問題：使用者在 LINE 授權頁面放棄或出錯，導致測驗結果遺失。
對策：在呼叫 LINE 授權前，先將測驗答案存入 LocalStorage。授權成功回調後，從 LocalStorage 取回答案再呼叫結果 API。即使使用者中途關閉，重新開啟時也能從斷點繼續。

### 風險四：Claude Code Agent 產出品質不穩定

問題：Agent 在某些複雜任務上可能產出有 Bug 的程式碼。
對策：每個任務完成後，人工執行一次 Smoke Test（打開頁面看有沒有明顯壞掉的地方）。如果有問題，將錯誤訊息與截圖作為新的 Context 餵回 Agent 要求修復。這就是「人工 Review + Agent 修復」的迭代循環。

---

## 七、建議開發時程

以每日可執行 2 到 3 個 Agent 任務為基準估算。

第 1 週：Phase 0 + Phase 1 全部 + Phase 4 啟動（美術可平行跑）
第 2 週：Phase 2 全部 + Phase 4 持續
第 3 週：Phase 3 的任務 3-1 到 3-3
第 4 週：Phase 3 的任務 3-4 到 3-6 + Phase 5 全部
第 5 週：整合測試、Bug 修復、效能最佳化

總計約 5 週，其中人工介入時間預估每天 1 到 2 小時（主要是 Review 與視覺確認）。

---

## 八、交付物清單

核心網站：首頁 + 5 題測驗 + LINE 登入 + 結果頁 + 共創地圖，部署於 Render
美術素材庫：16 到 24 種動物圖像 + 地圖裝飾素材 + 各頁插畫
AI Prompt 庫：文案生成 Prompt（已有）+ 圖像生成 Prompt 模板
技術文件：API 規格、資料庫 Schema、部署流程、環境變數清單

---

## 附錄：環境變數清單（需人工配置）

LINE_CHANNEL_ID — LINE Login Channel ID
LINE_CHANNEL_SECRET — LINE Login Channel Secret
LINE_CALLBACK_URL — OAuth 回調網址
AI_TEXT_API_KEY — 文案生成 AI 的 API Key
AI_IMAGE_API_KEY — 圖像生成 AI 的 API Key
DATABASE_URL — Render PostgreSQL 連線字串
REDIS_URL — Render Redis 連線字串
NEXT_PUBLIC_SOCKET_URL — WebSocket Server 網址
SESSION_SECRET — JWT 簽名密鑰
