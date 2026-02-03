# Joey AI Agent - Web Frontend 開發計畫

> **建立日期**：2026-02-03
> **狀態**：規劃完成，待執行
> **執行者**：Mac mini Claude Code Agent

---

## 專案概述

建立一個 Web 前端，讓使用者可以透過網頁（而非 LINE）提交網站建立需求，並即時監控 Agent 執行進度。

### 核心功能
- GitHub SSO 登入
- 豐富的網站配置選項（設計、SEO、追蹤碼）
- 檔案上傳（Logo、視覺說明書、主視覺）
- **即時進度監控**（真實顯示 Agent 執行步驟，不是假的進度條）
- 部署到 Render

---

## 使用者流程

```
1. 登入
   └─ GitHub SSO 登入
   └─ 取得使用者資訊、頭像

2. 儀表板
   └─ 顯示所有專案（進行中、已完成、失敗）
   └─ 點擊「新建網站」進入表單

3. 填寫表單（5 步驟）
   ├─ Step 1: 基本資訊
   │   └─ 專案名稱、描述、網站類型
   ├─ Step 2: 設計配置
   │   └─ 風格描述、色調選擇、字體、是否需要後台
   ├─ Step 3: 檔案上傳
   │   └─ Logo、視覺說明書、主視覺、或 Google Drive 連結
   ├─ Step 4: SEO 與追蹤
   │   └─ SEO 設定、GA4、Facebook Pixel、GTM
   └─ Step 5: 確認送出
       └─ 預覽所有設定、確認提交

4. 即時進度監控（關鍵功能）
   └─ 真實顯示 Agent 目前執行步驟
   └─ 步驟：接收 → 分析 → 下載素材 → 建立結構 →
           建立頁面 → 套用樣式 → 加入腳本 →
           推送 GitHub → 部署 Render → 驗證 → 完成
   └─ 每個步驟顯示：狀態、開始時間、錯誤訊息
   └─ 可查看詳細 log

5. 任務完成
   └─ 顯示成果：
       • 網站 URL (xxx.onrender.com)
       • GitHub repo URL
       • Notion 記錄連結
   └─ 可選：修改需求、重新部署
```

---

## 技術架構

```
┌────────────────────────────────────────────────────────────┐
│              Web Frontend (Next.js 14)                      │
│              部署在 Render (Static Site)                    │
│                                                             │
│  頁面：登入 / 儀表板 / 新建專案 / 專案詳情 / 進度監控        │
└─────────────────────────┬──────────────────────────────────┘
                          │ HTTPS API + SSE
                          ↓
┌────────────────────────────────────────────────────────────┐
│              Backend API (FastAPI)                          │
│              部署在 Render (Web Service)                    │
│                                                             │
│  端點：                                                      │
│  • /api/auth/github        - GitHub OAuth                   │
│  • /api/projects           - CRUD 專案                      │
│  • /api/projects/:id/progress - SSE 即時進度                │
│  • /api/upload             - 檔案上傳                       │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ↓
┌────────────────────────────────────────────────────────────┐
│              PostgreSQL Database                            │
│              部署在 Render                                   │
│                                                             │
│  Tables: users, projects, project_progress, uploads         │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ↓
┌────────────────────────────────────────────────────────────┐
│              Mac mini (Claude Code Agent)                   │
│              現有 joey-ai-agent                             │
│                                                             │
│  修改：支援 Web 來源 + 進度回報機制                          │
└────────────────────────────────────────────────────────────┘
```

---

## 表單欄位規格

### Step 1: 基本資訊
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| name | text | ✅ | 專案名稱 |
| description | textarea | ❌ | 網站描述 |
| site_type | select | ✅ | static / dynamic |

### Step 2: 設計配置
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| style_description | textarea | ❌ | 風格描述 |
| color_scheme.primary | color | ❌ | 主色 |
| color_scheme.secondary | color | ❌ | 次色 |
| color_scheme.accent | color | ❌ | 強調色 |
| color_scheme.background | color | ❌ | 背景色 |
| color_scheme.text | color | ❌ | 文字色 |
| font_heading | select | ❌ | 標題字體 |
| font_body | select | ❌ | 內文字體 |
| backend_type | select | ✅ | none / simple_cms / full_admin |
| pages | multiselect | ❌ | 首頁、關於、服務、作品、聯絡... |

### Step 3: 檔案上傳
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| logo | file | ❌ | Logo 圖片 |
| visual_guide | file | ❌ | 視覺說明書 / 品牌指南 |
| main_visual | file | ❌ | 主視覺圖片 |
| other_assets | files | ❌ | 其他素材 |
| google_drive_url | url | ❌ | Google Drive 連結（替代上傳）|

### Step 4: SEO 與追蹤
| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| seo_title | text | ❌ | SEO 標題 |
| seo_description | textarea | ❌ | SEO 描述 |
| seo_keywords | tags | ❌ | SEO 關鍵字 |
| og_image | file/url | ❌ | Open Graph 圖片 |
| ga4_id | text | ❌ | GA4 追蹤 ID |
| fb_pixel_id | text | ❌ | Facebook Pixel ID |
| gtm_id | text | ❌ | Google Tag Manager ID |

---

## 進度監控機制（關鍵功能）

### 進度步驟定義
```python
PROGRESS_STEPS = [
    ("task_received", "任務已接收", "📝"),
    ("analyzing", "分析需求中", "🔍"),
    ("downloading_assets", "下載素材中", "📥"),
    ("creating_structure", "建立專案結構", "📁"),
    ("building_pages", "建立頁面中", "🏗️"),
    ("styling", "套用樣式中", "🎨"),
    ("adding_scripts", "加入互動功能", "⚡"),
    ("pushing_github", "推送到 GitHub", "📤"),
    ("deploying_render", "部署到 Render", "🚀"),
    ("verifying", "驗證部署中", "✅"),
    ("completed", "完成", "🎉"),
]
```

### 實作方式：Server-Sent Events (SSE)
```
1. Agent 執行時，將進度寫入 project_progress 資料表
2. 前端透過 SSE 連線 /api/projects/:id/progress
3. 後端每 2 秒查詢資料庫，推送最新進度
4. 前端即時更新 UI
5. 任務完成或失敗時，關閉 SSE 連線
```

---

## 資料庫 Schema

```sql
-- 使用者（GitHub SSO）
CREATE TABLE users (
    id UUID PRIMARY KEY,
    github_id VARCHAR(255) UNIQUE NOT NULL,
    github_username VARCHAR(255),
    email VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 專案
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    site_type VARCHAR(50) DEFAULT 'static',
    style_description TEXT,
    color_scheme JSONB,
    font_selection JSONB,
    backend_type VARCHAR(50) DEFAULT 'none',
    pages JSONB,
    google_drive_url TEXT,

    -- SEO
    seo_title VARCHAR(255),
    seo_description TEXT,
    seo_keywords TEXT[],
    og_image TEXT,
    ga4_id VARCHAR(50),
    fb_pixel_id VARCHAR(50),
    gtm_id VARCHAR(50),

    -- 狀態
    status VARCHAR(50) DEFAULT 'pending',
    current_step VARCHAR(50),

    -- 結果
    github_url TEXT,
    deploy_url TEXT,
    notion_url TEXT,

    -- 時間
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- 進度記錄（即時監控用）
CREATE TABLE project_progress (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    step VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,  -- started / completed / failed
    message TEXT,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 上傳檔案
CREATE TABLE uploads (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    file_type VARCHAR(50),  -- logo / visual_guide / main_visual / other
    file_name VARCHAR(255),
    file_path TEXT,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 檔案結構

### 後端擴充（joey-ai-agent）
```
src/
├── database/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   └── session.py         # Database connection
├── api/
│   ├── auth.py            # GitHub OAuth 端點
│   ├── projects.py        # 專案 CRUD + SSE
│   └── uploads.py         # 檔案上傳
├── schemas/
│   └── project.py         # Pydantic schemas
├── services/
│   ├── web_task_processor.py  # Web 任務處理器
│   └── claude_code_service.py # 加入進度回報
└── config.py              # 新增 DB、OAuth 設定
```

### 前端專案（web-frontend/）
```
web-frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx                    # 首頁/登入
│   │   ├── dashboard/page.tsx          # 儀表板
│   │   ├── projects/
│   │   │   ├── new/page.tsx            # 新建專案（5 步驟表單）
│   │   │   └── [id]/
│   │   │       ├── page.tsx            # 專案詳情
│   │   │       └── progress/page.tsx   # 即時進度監控
│   │   └── settings/page.tsx           # 設定
│   ├── components/
│   │   ├── forms/                      # 表單元件
│   │   ├── progress/                   # 進度元件
│   │   └── ui/                         # 基礎 UI
│   ├── lib/
│   │   ├── api.ts                      # API client
│   │   └── hooks/useProgress.ts        # SSE hook
│   └── types/
├── package.json
├── next.config.js
└── tailwind.config.ts
```

---

## 實作階段

### Phase 1：後端資料庫與 API（2-3 天）
1. 新增 PostgreSQL 連線設定
2. 建立 SQLAlchemy models
3. 建立 Alembic migrations
4. 實作 GitHub OAuth 端點
5. 實作專案 CRUD API
6. 實作 SSE 進度端點
7. 實作檔案上傳 API

### Phase 2：進度回報機制（1-2 天）
1. 修改 claude_code_service.py 支援進度回報
2. 建立 web_task_processor.py
3. 實作進度寫入資料庫邏輯
4. 測試 SSE 連線

### Phase 3：前端專案建立（3-4 天）
1. 初始化 Next.js 專案
2. 設定 Tailwind CSS + shadcn/ui
3. 實作 GitHub OAuth 登入
4. 建立儀表板頁面
5. 建立多步驟表單
6. 建立即時進度監控頁面

### Phase 4：整合測試（1-2 天）
1. 前後端整合測試
2. 測試完整使用者流程
3. 測試進度監控
4. 修復 bugs

### Phase 5：部署（1 天）
1. 設定 Render PostgreSQL
2. 部署後端 API
3. 部署前端 Static Site
4. 設定環境變數
5. 驗證部署

---

## Agent 執行 Prompt

當要執行此計畫時，發送以下 prompt 給 Agent：

```
[AUTOMATED EXECUTION MODE - WEB FRONTEND PROJECT]

建立「Joey AI Agent Web Frontend」完整專案。

## 執行順序

1. 後端擴充
   - 新增 src/database/ 模組（models, session）
   - 新增 src/api/auth.py（GitHub OAuth）
   - 新增 src/api/projects.py（CRUD + SSE）
   - 新增 src/api/uploads.py（檔案上傳）
   - 新增 src/schemas/project.py
   - 新增 src/services/web_task_processor.py
   - 修改 src/config.py（新增 DB、OAuth 設定）
   - 修改 src/main.py（註冊新路由）

2. 前端建立
   - 在 joey-ai-agent 同層目錄建立 web-frontend/
   - 初始化 Next.js 14 專案
   - 安裝：tailwindcss, @shadcn/ui, zustand, next-auth
   - 建立所有頁面和元件

3. 部署設定
   - 建立 render.yaml（後端 + 前端）
   - 推送到 GitHub
   - 部署到 Render

## 關鍵要求

- 使用 TypeScript
- 繁體中文介面
- 響應式設計
- 真實進度監控（SSE）
- GitHub SSO 登入
- 部署到 Render

---RESULT---
PROJECT_NAME: joey-ai-frontend
GITHUB_URL: [GitHub repo]
DEPLOY_URL: [Render URL]
STATUS: SUCCESS
---END---
```

---

## 驗證方式

1. **登入測試**：GitHub SSO 可正常登入、登出
2. **表單測試**：5 步驟表單可正常填寫、上傳檔案
3. **進度測試**：提交任務後，進度頁面即時顯示 Agent 執行步驟
4. **結果測試**：任務完成後，顯示 GitHub URL 和部署 URL
5. **端到端測試**：從登入到收到成品的完整流程

---

## 關鍵檔案位置

| 檔案 | 用途 |
|------|------|
| `/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent/src/services/claude_code_service.py` | 需修改：加入進度回報 |
| `/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent/src/services/task_processor.py` | 參考：任務處理流程 |
| `/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent/src/config.py` | 需修改：新增設定 |
| `/Users/JoeyLiao/Joey's AI Agent /joey-ai-agent/src/main.py` | 需修改：註冊新路由 |

---

## 預估成本

| 項目 | 費用 |
|------|------|
| Render Web Service | ~$7/月 |
| Render PostgreSQL | ~$7/月 |
| Render Static Site | 免費 |
| **總計** | ~$14/月 |

---

*文件建立日期：2026-02-03*
*狀態：待執行*
