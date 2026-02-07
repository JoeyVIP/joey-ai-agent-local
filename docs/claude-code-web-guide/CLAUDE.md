# Joey 網頁專案 - Claude Code 指南

本文件定義 Joey 所有網頁專案的設計偏好、技術規範、素材流程和品質標準。
複製此檔案到新專案根目錄，Claude Code 即可自動遵循所有規範。

---

## 1. 設計偏好與禁忌

### 絕對禁止（AI Slop 特徵）

以下特徵會讓網站看起來像 AI 量產品，必須完全避免：

**字體禁忌**
- Inter、Roboto、Arial、Helvetica、system-ui
- 任何 generic 字體或 sans-serif fallback
- 全站只用一種字體

**配色禁忌**
- 紫色漸層 + 白底（最典型的 AI slop）
- 純黑 #000 + 純白 #FFF（缺乏層次）
- 彩虹色系或隨機多色
- 所有元素配色比重相同，沒有主次

**版面禁忌**
- 所有區塊等高等寬的「棋盤式」排列
- 無限重複的三欄卡片
- 沒有負空間，內容塞滿
- Cookie-cutter 樣板感

**動畫禁忌**
- 無限循環的裝飾動畫
- 過度彈跳效果
- 讓人頭暈的旋轉

### 設計核心原則

1. **選擇大膽的美學方向**，而非中庸的「安全選擇」
2. **每個網站都是獨一無二的**，根據品牌特性量身訂做
3. **先確定設計概念再寫程式碼**：用途、調性、受眾、差異點
4. **精緻度來自細節**：字距、行高、陰影、過渡效果
5. **留白是設計的一部分**，不是浪費空間

### 行業模板對應

根據客戶行業選擇對應的設計方向：

| 行業 | 風格方向 | 色調 | 字體傾向 |
|------|---------|------|---------|
| 製造/工業/倉儲 | 穩重、專業、技術實力 | 藍灰、工業橘、黑金 | Oswald、Rajdhani、Bebas Neue |
| 餐廳/咖啡 | 溫暖、氛圍感、食慾感 | 棕、金、暖色系 | Cormorant Garamond、Playfair Display |
| 品牌官網 | 質感、獨特性、品牌調性 | 依品牌定位 | Outfit、DM Serif Display |
| 企業/B2B | 穩重、信任感、專業 | 企業藍、深色調 | Plus Jakarta Sans、IBM Plex Sans |

每個行業又有子風格（如餐廳分文青咖啡、高級餐廳、活力餐廳、日式極簡），根據客戶實際定位選擇最適合的。

---

## 2. 標準技術棧

### 核心框架

```
Next.js 16+ (App Router) + TypeScript + Tailwind CSS 4
```

### 常用套件

| 套件 | 用途 |
|------|------|
| `zustand` | 輕量狀態管理 |
| `zod` | 表單驗證 + 型別安全 |
| `react-hook-form` + `@hookform/resolvers` | 表單處理 |
| `lucide-react` | Icon 圖示庫 |
| `framer-motion` | 進場動畫、頁面過渡 |
| `next-auth` | 認證（如需要） |
| `axios` | HTTP 請求 |
| `html2canvas` | 截圖功能（如需要） |

### 初始化指令

```bash
npx create-next-app@latest my-project --typescript --tailwind --app --src-dir
cd my-project
npm install zustand zod react-hook-form @hookform/resolvers lucide-react framer-motion
```

### 部署平台

**Render**（主要部署目標）

`render.yaml` 範例：
```yaml
services:
  - type: web
    name: project-name
    runtime: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
```

注意事項：
- 環境變數在 Render Dashboard 設定，不放在程式碼中
- Build 時需確保所有圖片路徑正確
- 使用 `output: 'standalone'` 可減小部署體積

---

## 3. 設計系統規範

### CSS Variables（必須使用）

所有專案都必須用 CSS Variables 建立一致配色，不可在元素上直接寫顏色值：

```css
:root {
  /* 必要的變數 */
  --color-primary: ;      /* 主色 */
  --color-secondary: ;    /* 輔色 */
  --color-accent: ;       /* 強調色 */
  --color-background: ;   /* 背景色 */
  --color-text: ;         /* 文字色 */
  --color-text-light: ;   /* 淺文字 */
  --color-light: ;        /* 淺背景 */
  --color-border: ;       /* 邊框色 */
}
```

### 配色 60-30-10 法則

- **主色 60%**：背景、大區塊
- **輔色 30%**：次要區塊、邊框、導航
- **強調色 10%**：CTA 按鈕、重點標記、連結

### 字體選擇指南

**中英文配對策略**：

```css
/* 標題 - 英文裝飾字 + 中文黑體/明體 */
.heading {
  font-family: '[英文裝飾字]', 'Noto Sans TC', serif;
}

/* 內文 - 易讀為主 */
.body {
  font-family: '[英文內文字]', 'Noto Sans TC', sans-serif;
}
```

**字體來源**：[Google Fonts](https://fonts.google.com/) - 免費、CDN 穩定

**推薦的字體組合**（按風格）：

| 風格 | 標題字體 | 內文字體 |
|------|---------|---------|
| 現代工業 | Oswald | Source Sans Pro |
| 科技精密 | Rajdhani | Open Sans |
| 經典專業 | Bebas Neue | Lato |
| 文青溫暖 | Cormorant Garamond | Lora |
| 高級優雅 | Playfair Display | Montserrat |
| 極簡高端 | Outfit | Outfit (light weight) |
| 自然有機 | DM Serif Display | Karla |
| 企業科技 | Plus Jakarta Sans | Plus Jakarta Sans |
| 專業穩重 | IBM Plex Sans | IBM Plex Sans |
| 顧問高端 | Cormorant Garamond | Work Sans |

### 排版規範

**字級層次**（使用 `clamp` 響應式）：
```css
h1 { font-size: clamp(2rem, 5vw, 3.5rem); }
h2 { font-size: clamp(1.5rem, 4vw, 2.5rem); }
h3 { font-size: clamp(1.25rem, 3vw, 1.75rem); }
p  { font-size: clamp(1rem, 2vw, 1.125rem); }
```

**行高**：
- 標題：1.2 - 1.3
- 內文：1.6 - 1.8

**負空間**：
- 區塊間距至少 60px（手機 40px）
- 內容不要塞滿，留白是設計的一部分

### 動畫規範

**推薦：Staggered Reveal（交錯入場）**
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-in { animation: fadeInUp 0.6s ease-out; }
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
```

**原則**：
- 一次精心設計的頁面入場 > 到處散落的微互動
- 用 Intersection Observer 觸發滾動入場
- Hover 效果要有驚喜感
- 使用 Framer Motion 處理複雜動畫

### 背景與紋理

增加深度感，避免純色平面：
- **漸層疊加**：圖片上加半透明漸層增加可讀性
- **Noise Texture**：微妙的噪點增加質感
- **幾何圖案**：SVG pattern 作為裝飾
- **Hero 背景範例**：
```css
.hero {
  background:
    linear-gradient(135deg, rgba(0,0,0,0.7), rgba(0,0,0,0.3)),
    url('/images/hero.jpg');
  background-size: cover;
  background-position: center;
}
```

### 按鈕設計

```css
.btn-primary {
  padding: 1rem 2rem;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
```

- 最小觸控區域：44px x 44px（手機友善）

### 響應式 Mobile First

- 以手機版為基礎向上擴展
- 斷點：`640px`（sm）、`768px`（md）、`1024px`（lg）、`1280px`（xl）
- 手機版關閉 parallax（`background-attachment: scroll`）
- Grid 在手機版降為單欄
- 圖片一律 `max-width: 100%; height: auto;`
- 使用 `loading="lazy"` 延遲載入非首屏圖片

### 圖片比例參考

- Hero：16:9 或 21:9
- 卡片：4:3 或 1:1
- 產品：1:1 或 3:4

---

## 4. 素材處理 SOP

### 圖片下載

從客戶現有官網抓圖時，**必須**加 Referer header，否則部分 CDN（如 iyp.tw）會回 403/404：

```bash
curl -H "Referer: https://客戶官網URL/" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
     -o filename.jpg "https://圖片URL"
```

### 下載後驗證

下載的每張圖片都必須用 `file` 指令驗證，確認是真圖片而非 HTML 錯誤頁：

```bash
file filename.jpg
# 正確: filename.jpg: JPEG image data, JFIF standard...
# 錯誤: filename.jpg: HTML document, ASCII text...
```

如果回傳 HTML，代表下載失敗，需要調整 header 或 URL 重新下載。

### Google Drive 素材管理

素材上傳 Google Drive 統一使用**扁平結構**（不建子資料夾），content.md 和圖片放同一層：

```
{專案名稱}/
├── content.md          # 結構化內容（必要）
├── logo.png
├── hero.jpg
├── product-1.jpg
└── ...
```

### gdown 下載指令

```bash
# 下載整個資料夾
gdown --folder "https://drive.google.com/drive/folders/xxxxxx" -O ./assets

# 下載單一檔案
gdown "https://drive.google.com/uc?id=xxxxxx" -O ./filename.png
```

**前提條件**：
- Google Drive 連結必須設為「任何人都可以查看」
- 不需要 OAuth 認證
- 需安裝 gdown：`pip install gdown`

### 檔案命名規則

- 使用英文小寫，用 `-` 連接
- 描述性命名：`product-screw-m10.jpg`、`factory-cnc.jpg`
- 避免中文檔名、空格、特殊符號

---

## 5. content.md 標準格式

每個專案都需要一份 `content.md` 作為網站內容的唯一來源。格式如下：

```markdown
# [品牌名稱] 官網內容

## 基本資訊
- **品牌名稱**：
- **公司全名**：
- **一句話描述**：

---

## 首頁

### Hero 區塊
- **主標語**：[10-20字吸引人標題]
- **副標語**：[20-40字說明價值]
- **CTA**：[按鈕文字]

### 特色區塊
1. **[特色1]** - [說明]
2. **[特色2]** - [說明]
3. **[特色3]** - [說明]

---

## 關於我們

### 品牌故事
[2-3段]

### 經營理念
[重點列表]

---

## 產品/服務介紹

### [產品/服務名稱]
- **價格**：[如有]
- **說明**：

---

## 聯絡資訊
- **電話**：
- **Email**：
- **地址**：
- **營業時間**：

### 社群
- Facebook：
- Instagram：
- LINE：

---

## FAQ

**Q: [問題]**
A: [答案]

---

## SEO
- **Title**：[50字內]
- **Description**：[150字內]
- **Keywords**：[5-10個]

---

## 網站設計需求

### 風格方向
[描述期望的視覺風格]

### 配色偏好
[指定色系或提供品牌色]

### 視覺元素
[特別想要的設計元素]

### 頁面需求
[需要哪些頁面，各頁面特殊需求]

### 參考網站
[列出喜歡的參考網站]
```

**重要**：最後一定要有「網站設計需求」區塊，為設計提供明確方向。沒有這個區塊，產出的網站容易變成 generic 模板。

---

## 6. 開源資源推薦清單

### 字型

| 資源 | 說明 |
|------|------|
| [Google Fonts](https://fonts.google.com/) | 免費字型，CDN 穩定 |
| [Noto Sans TC](https://fonts.google.com/noto/specimen/Noto+Sans+TC) | 中文黑體首選 |
| [Noto Serif TC](https://fonts.google.com/noto/specimen/Noto+Serif+TC) | 中文明體首選 |

### 動畫

| 資源 | 說明 |
|------|------|
| [Framer Motion](https://www.framer.com/motion/) | React 動畫首選 |
| CSS `@keyframes` | 簡單動畫用原生 CSS |
| Intersection Observer API | 滾動觸發動畫 |

### UI 元件

| 資源 | 說明 |
|------|------|
| [Lucide Icons](https://lucide.dev/) | 輕量 Icon 庫（已在技術棧中） |
| [shadcn/ui](https://ui.shadcn.com/) | 高品質 Tailwind 元件（按需複製） |
| [Headless UI](https://headlessui.com/) | 無樣式可存取元件 |

### 圖片與素材

| 資源 | 說明 |
|------|------|
| [Unsplash](https://unsplash.com/) | 免費高品質照片 |
| [TinyPNG](https://tinypng.com/) | 圖片壓縮（建議 500KB 以下） |
| [Squoosh](https://squoosh.app/) | Google 出品圖片壓縮 |
| [SVGOMG](https://jakearchibald.github.io/svgomg/) | SVG 最佳化 |

### 地圖整合

| 資源 | 說明 |
|------|------|
| Google Maps Embed API | 免費嵌入地圖（iframe） |
| [Leaflet](https://leafletjs.com/) | 開源互動地圖 |

---

## 7. 品質檢查清單

每個專案完成後，必須通過以下檢查：

### 設計品質

- [ ] 沒有使用禁止字體（Inter、Roboto、Arial、Helvetica）
- [ ] 沒有紫色漸層 + 白底的 AI slop 配色
- [ ] CSS Variables 建立了完整的配色系統
- [ ] 配色遵循 60-30-10 法則
- [ ] 字體有中英文配對（標題 + 內文至少兩組）
- [ ] 區塊之間有足夠的負空間
- [ ] 按鈕有 hover 效果和足夠的觸控區域
- [ ] 有入場動畫（fadeIn、staggered reveal 等）

### 手機版

- [ ] 導航在手機版可正常使用（漢堡選單或其他方案）
- [ ] 所有圖片不超出螢幕
- [ ] 文字大小可讀（最小 14px）
- [ ] 按鈕觸控區域 >= 44px
- [ ] 表單在手機上易於填寫
- [ ] Grid 在手機版降為單欄或雙欄

### 效能與 SEO

- [ ] 圖片使用 `loading="lazy"`
- [ ] 有正確的 `<title>` 和 `<meta description>`
- [ ] 所有圖片有 `alt` 屬性
- [ ] Lighthouse Performance >= 80
- [ ] Lighthouse Accessibility >= 90

### 功能完整性

- [ ] 所有連結可點擊且指向正確頁面
- [ ] 表單可正常提交（或有明確的 placeholder 行為）
- [ ] 社群連結在新分頁開啟
- [ ] 電話號碼可直接撥打（`tel:` 連結）
- [ ] Email 可直接發信（`mailto:` 連結）

### 截圖下載功能（如有）

- [ ] html2canvas 可正確截取頁面
- [ ] 產出的圖片品質可接受
- [ ] 下載按鈕在各瀏覽器可正常運作

---

## 附錄：設計思考流程

開始設計前，先回答以下問題：

1. **用途**：這個網站要解決什麼問題？誰在使用？
2. **調性**：選一個極端方向 — 極簡、奢華、復古、工業、有機、街頭、禪意...
3. **差異點**：這個網站有什麼讓人記住的特點？
4. **限制**：技術限制、素材限制、品牌規範

確定方向後才開始寫程式碼。Bold maximalism 和 refined minimalism 都可以，關鍵是**有意識的選擇**，而非預設的安全選項。
