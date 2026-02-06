# 製造業/代工廠網站模板

專為 OEM/ODM 代工廠、製造業、工業公司設計的網站模板。

## 美學方向

**Industrial Professional** - 專業、信賴、技術實力

### 設計關鍵詞
- 穩重、可靠、技術導向
- 乾淨俐落的線條
- 強調品質與認證
- 工廠實景展示

## 字體推薦

### 組合 1：現代工業
```css
/* 標題 - 粗壯有力 */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Source+Sans+Pro:wght@400;600&display=swap');

h1, h2, h3 {
  font-family: 'Oswald', 'Noto Sans TC', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

body, p {
  font-family: 'Source Sans Pro', 'Noto Sans TC', sans-serif;
}
```

### 組合 2：科技精密
```css
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Open+Sans:wght@400;600&display=swap');

h1, h2, h3 {
  font-family: 'Rajdhani', 'Noto Sans TC', sans-serif;
}
```

### 組合 3：經典專業
```css
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Lato:wght@400;700&display=swap');

h1, h2, h3 {
  font-family: 'Bebas Neue', 'Noto Sans TC', sans-serif;
  letter-spacing: 0.1em;
}
```

## 配色方案

### 方案 1：藍灰專業（信賴感）
```css
:root {
  --color-primary: #1E3A5F;      /* 深海軍藍 */
  --color-secondary: #64748B;    /* 工業灰 */
  --color-accent: #2563EB;       /* 科技藍 */
  --color-background: #F8FAFC;   /* 淺灰白 */
  --color-text: #1E293B;         /* 深灰 */
  --color-border: #E2E8F0;       /* 淺邊框 */
}
```

### 方案 2：工業橘（活力、效率）
```css
:root {
  --color-primary: #37474F;      /* 石墨灰 */
  --color-secondary: #607D8B;    /* 鋼鐵灰 */
  --color-accent: #E65100;       /* 工業橘 */
  --color-background: #ECEFF1;   /* 淺灰 */
  --color-text: #263238;         /* 深灰 */
}
```

### 方案 3：黑金高端（精密製造）
```css
:root {
  --color-primary: #1A1A1A;      /* 純黑 */
  --color-secondary: #333333;    /* 深灰 */
  --color-accent: #D4AF37;       /* 金色 */
  --color-background: #FAFAFA;   /* 極淺灰 */
  --color-text: #1A1A1A;         /* 黑 */
}
```

## 必要頁面結構

### 首頁
1. **Hero 區塊**
   - 全幅工廠/產線照片
   - 大標：公司核心價值（如「30 年專業代工經驗」）
   - CTA：「取得報價」「了解更多」

2. **核心能力展示**
   - 3-4 個服務/能力卡片
   - 圖標 + 標題 + 簡述
   - Grid 佈局

3. **數字成就**
   - 客戶數、產能、年資、認證數
   - 大數字 + 單位 + 說明
   - 計數動畫效果

4. **認證標章區**
   - ISO 9001、ISO 14001、CE、UL 等
   - 灰階或單色 Logo 排列

5. **聯絡 CTA**
   - 背景色區塊
   - 簡單表單或聯絡資訊

### 關於我們
- 公司歷史時間軸
- 工廠照片輪播
- 團隊介紹（可選）
- 企業理念

### 產品/服務
- 分類導航
- 產品卡片（圖片 + 規格摘要）
- 詳細規格表（可展開）

### 品質認證
- 認證證書展示
- 品管流程說明
- 測試設備照片

### 聯絡我們
- 表單：姓名、Email、電話、需求描述
- 地圖嵌入
- 工廠地址、電話、傳真

## 設計細節

### Hero 處理
```css
.hero {
  position: relative;
  height: 80vh;
  min-height: 500px;
  background:
    linear-gradient(135deg, rgba(30, 58, 95, 0.9), rgba(30, 58, 95, 0.6)),
    url('/images/factory.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
}
```

### 數字統計區
```css
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  padding: 4rem 0;
  background: var(--color-primary);
  color: white;
}

.stat-number {
  font-family: 'Oswald', sans-serif;
  font-size: 3rem;
  font-weight: 700;
}
```

### 認證標章
```css
.certifications {
  display: flex;
  justify-content: center;
  gap: 3rem;
  padding: 3rem 0;
  background: var(--color-background);
}

.cert-logo {
  filter: grayscale(100%);
  opacity: 0.7;
  transition: all 0.3s ease;
}

.cert-logo:hover {
  filter: grayscale(0%);
  opacity: 1;
}
```

## 圖片建議

### 必要圖片
1. Hero 背景 - 工廠全景或產線
2. 產品/設備 - 高清產品照
3. 工廠內部 - 整潔的生產環境
4. 團隊 - 專業形象照（可選）

### 圖片風格
- 色調統一（建議偏冷色調）
- 避免手機隨拍感
- 展現專業與規模

## 參考網站

1. [Foxconn](https://www.foxconn.com/) - 大型代工廠標竿
2. [Flex](https://flex.com/) - 現代工業設計
3. [Jabil](https://www.jabil.com/) - 科技製造業
