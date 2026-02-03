```
# Joey's AI Agent - 完整開發指令

## 專案目標

建立一個「手機版 Claude Code」系統。我透過 Line 傳送工作需求，Mac mini 上的 Python 服務會 24/7 運作，用 Claude API 像 Cowork 一樣自動處理任務。簡單的任務直接產出結果，複雜的任務準備好資料和 Prompt 等我開電腦用 Claude Code 處理。所有結果存在 Notion，Line 通知我去看。

## 我是誰

我是 Joey，經營營收成長顧問公司「來電司康」，同時服務多個客戶，產業包含餐廳、教育機構、電商、NGO。我習慣使用 Claude Code，偏好簡潔的輸出，不要過度格式化。我用繁體中文工作。

## 系統架構概述

Line 是輸入和通知介面。
Mac mini 運行 Python 服務，24/7 不間斷。
Claude API 是大腦，負責理解需求、判斷難度、執行任務。
Notion 是儲存和顯示介面，也是 AI 的記憶系統。

流程是這樣：我在 Line 傳送需求，Python 服務收到後呼叫 Claude API 處理，處理完把結果存到 Notion，然後 Line 通知我可以去看了。

## 資料夾結構

請建立以下結構：

```
joey-ai-agent/
├── .claude/
│   ├── settings.json
│   └── commands/
│       └── start.md
├── src/
│   ├── main.py
│   ├── line_handler.py
│   ├── notion_client.py
│   ├── claude_brain.py
│   ├── task_processor.py
│   └── config.py
├── prompts/
│   └── system_prompt.md
├── requirements.txt
├── .env.example
├── Procfile
└── README.md
```

## 環境變數設定

.env.example 內容：

```
LINE_CHANNEL_SECRET=你的_line_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=你的_line_access_token
NOTION_API_KEY=你的_notion_api_key
NOTION_INBOX_DB_ID=你的_inbox_database_id
NOTION_REVIEW_DB_ID=你的_review_database_id
NOTION_MEMORY_DB_ID=你的_memory_database_id
ANTHROPIC_API_KEY=你的_claude_api_key
JOEY_LINE_USER_ID=joey_的_line_user_id
PORT=5000
```

## Notion 資料庫設計

需要三個 Database：

第一個：Inbox
用途是暫存剛收到的任務，AI 處理中的狀態
欄位包含：
- Title 標題，類型是 title
- Status 狀態，類型是 select，選項有 received 和 processing
- Source 來源，類型是 select，選項有 line 和 manual
- RawInput 原始輸入，類型是 rich_text
- ReceivedAt 收到時間，類型是 date
- LineReplyToken，類型是 rich_text

第二個：Review 待審核
用途是 AI 處理完的任務，等我審核
欄位包含：
- Title 標題，類型是 title
- Difficulty 難度，類型是 select，選項有 simple 和 complex
- Status 狀態，類型是 select，選項有 pending_review 和 approved 和 rejected 和 need_revision
- Summary 摘要，類型是 rich_text
- Result 結果，類型是 rich_text，這是簡單任務的完整輸出
- Analysis 分析，類型是 rich_text，這是複雜任務的需求分析
- Preparation 準備資料，類型是 rich_text，這是複雜任務的前置準備
- PromptForClaudeCode 給 Claude Code 的 Prompt，類型是 rich_text
- EstimatedTime 預估時間，類型是 rich_text
- Reason 原因，類型是 rich_text，為什麼判定為複雜
- ProcessedAt 處理完成時間，類型是 date
- SourceTaskId 來源任務 ID，類型是 rich_text

第三個：Memory 記憶
用途是 AI 的長期記憶，越用越懂我
欄位包含：
- Title 標題，類型是 title
- Category 分類，類型是 select，選項有 project 和 client 和 preference 和 context
- Content 內容，類型是 rich_text
- UpdatedAt 更新時間，類型是 date
- Importance 重要性，類型是 select，選項有 high 和 medium 和 low

## Python 程式碼邏輯

main.py 是進入點，用 Flask 建立 web server，監聽 Line webhook。

line_handler.py 負責處理 Line 訊息，收到訊息後建立 Inbox 任務，然後非同步觸發處理流程，立刻回覆「收到，處理中」。

notion_client.py 封裝所有 Notion API 操作，包含：
- 建立 Inbox 任務
- 讀取 Memory
- 建立 Review 任務
- 更新任務狀態
- 刪除 Inbox 任務（處理完後）

claude_brain.py 負責呼叫 Claude API，包含：
- 載入 system prompt
- 組合 memory 內容
- 送出請求
- 解析回應

task_processor.py 是核心處理邏輯：
1. 從 Inbox 讀取任務
2. 從 Memory 讀取所有記憶
3. 組合 prompt 送給 Claude API
4. 解析 Claude 回應的 JSON
5. 根據難度建立對應的 Review 任務
6. 如果 Claude 有新的記憶要存，更新 Memory
7. 刪除 Inbox 任務
8. 透過 Line Push API 通知我

config.py 負責讀取環境變數。

## Claude API System Prompt

存在 prompts/system_prompt.md，內容如下：

```
你是 Joey 的 AI 工作代理。你的任務是獨立處理工作需求，像 Claude Code 和 Cowork 一樣能自主完成任務。

關於 Joey：
Joey 經營營收成長顧問公司「來電司康」，服務多個客戶，產業包含餐廳、教育機構、電商、NGO。他習慣使用 Claude Code，偏好簡潔的輸出格式，使用繁體中文。

你會收到兩個輸入：
1. Joey 的記憶庫（過去累積的背景資訊）
2. 新的工作需求

你的處理流程：

第一步：理解需求
分析這是什麼類型的工作，最終要產出什麼，給誰看的。

第二步：判斷難度

判定為「簡單」的條件（你能完全處理）：
- 文字內容產出，例如 email、報告、文案、回覆
- 資料整理、摘要、分析
- 簡單的規劃、建議、清單
- 資訊查詢和整理

判定為「複雜」的條件（需要 Joey 開電腦用 Claude Code）：
- 需要多輪深度對話才能完成
- 需要產出程式碼
- 需要製作檔案如簡報、試算表、PDF
- 需要存取外部系統或 API
- 需要處理大量資料
- 涉及重大決策需要人類判斷

第三步：執行

如果是簡單任務：
直接產出完整、可直接使用的結果。結果要完整到 Joey 可以直接複製貼上回覆客戶或使用。

如果是複雜任務：
完成所有前置準備工作，包含需求分析、資料整理、大綱規劃。然後產出一個完整的 Prompt，讓 Joey 開電腦後可以直接貼給 Claude Code 開始工作。

第四步：更新記憶

思考這次任務有沒有值得記住的資訊：
- 新的專案或客戶資訊
- Joey 的偏好或習慣
- 有用的背景脈絡

輸出格式：

你必須輸出合法的 JSON，格式如下：

簡單任務：
{
  "difficulty": "simple",
  "title": "任務標題，簡短描述",
  "summary": "一句話摘要，給 Line 通知用，不超過 50 字",
  "result": "完整的結果內容，這是 Joey 會直接使用的輸出",
  "memory_updates": [
    {
      "category": "project 或 client 或 preference 或 context",
      "title": "記憶標題",
      "content": "要記住的內容",
      "importance": "high 或 medium 或 low"
    }
  ]
}

複雜任務：
{
  "difficulty": "complex",
  "title": "任務標題，簡短描述",
  "summary": "一句話摘要，給 Line 通知用，不超過 50 字",
  "reason": "為什麼判定為複雜，需要開電腦",
  "analysis": "完整的需求分析",
  "preparation": "已完成的前置準備，包含收集的資料、整理的資訊、初步的規劃",
  "prompt_for_claude_code": "開電腦後直接貼給 Claude Code 的完整 prompt，要包含所有背景資訊和具體指令",
  "estimated_time": "預估開電腦後需要多少時間完成",
  "memory_updates": [
    {
      "category": "project 或 client 或 preference 或 context",
      "title": "記憶標題",
      "content": "要記住的內容",
      "importance": "high 或 medium 或 low"
    }
  ]
}

memory_updates 可以是空陣列，如果這次沒有新的記憶要存。

重要提醒：
- 輸出必須是合法 JSON，不要有其他文字
- 繁體中文
- 簡潔有力，不要廢話
- 簡單任務的 result 要完整可用
- 複雜任務的 prompt_for_claude_code 要詳細到可以直接開工
```

## Line 通知訊息格式

簡單任務完成時發送：
```
✅ 做好了

{title}

{summary}

👉 打開 Notion 看結果
```

複雜任務準備好時發送：
```
🔧 這題要開電腦

{title}

{reason}

預估時間：{estimated_time}

👉 打開 Notion 看準備好的資料和 Prompt
```

收到任務時立刻回覆：
```
📝 收到，處理中

{原始訊息的前 30 字}...

完成後會通知你
```

## 技術細節

使用 Flask 作為 web framework
使用 line-bot-sdk v3
使用 notion-client
使用 anthropic SDK
使用 python-dotenv 讀取環境變數
使用 threading 做非同步處理，讓 Line webhook 能快速回應

requirements.txt 內容：
```
flask
gunicorn
line-bot-sdk
notion-client
anthropic
python-dotenv
```

Procfile 內容：
```
web: gunicorn main:app
```

## 部署方式

這個服務會部署在我的 Mac mini 上，24/7 運作。
使用 gunicorn 執行。
可能需要用 ngrok 或 cloudflare tunnel 來取得公開的 webhook URL。

## 初始化 Memory

第一次啟動時，請在 Notion Memory 資料庫建立以下初始記憶：

標題：Joey 的基本資訊
分類：context
內容：Joey 經營來電司康營收成長顧問公司，服務餐廳、教育機構、電商、NGO 等客戶。偏好簡潔輸出，使用繁體中文，習慣用 Claude Code。
重要性：high

標題：輸出偏好
分類：preference
內容：不要過度格式化，不要太多符號，段落間適當換行，適合在 Line 或即時通訊軟體閱讀。
重要性：high

## 執行這個專案

請依照以上規格，完整建立這個專案。包含所有檔案、所有程式碼、所有設定。程式碼要完整可執行，不要留 placeholder 或 TODO。

建立完成後，告訴我：
1. 需要在 Line Developers 做什麼設定
2. 需要在 Notion 做什麼設定
3. 如何啟動服務
4. 如何測試

開始吧。
```
