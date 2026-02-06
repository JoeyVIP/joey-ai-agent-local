# 企業官網模板

專為 B2B 企業、科技公司、顧問公司、服務業公司設計的網站模板。

## 美學方向

根據企業類型選擇：

### A. 科技現代 (Tech Modern)
- 創新、前瞻、數位化
- 漸層、動態元素
- 藍、紫科技色系

### B. 專業穩重 (Professional)
- 信賴、專業、權威
- 乾淨版面、商業攝影
- 藍、灰、白色系

### C. 創意活力 (Creative Agency)
- 創意、活力、獨特
- 不規則版面、大膽用色
- 多彩、對比強烈

### D. 顧問高端 (Consulting)
- 高端、精英、品質
- 大量留白、精緻排版
- 深色調、金色點綴

## 字體推薦

### 科技現代
```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700&display=swap');

body {
  font-family: 'Plus Jakarta Sans', 'Noto Sans TC', sans-serif;
}
```

### 專業穩重
```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap');

body {
  font-family: 'IBM Plex Sans', 'Noto Sans TC', sans-serif;
}
```

### 創意活力
```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700&display=swap');

h1, h2, h3 {
  font-family: 'Syne', 'Noto Sans TC', sans-serif;
  font-weight: 700;
}
```

### 顧問高端
```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&family=Work+Sans:wght@300;400;500&display=swap');

h1, h2, h3 {
  font-family: 'Cormorant Garamond', 'Noto Serif TC', serif;
}

body, p {
  font-family: 'Work Sans', 'Noto Sans TC', sans-serif;
  font-weight: 300;
}
```

## 配色方案

### 科技現代（Tech Blue）
```css
:root {
  --color-primary: #0F172A;      /* 深海藍 */
  --color-secondary: #1E293B;    /* 次深藍 */
  --color-accent: #3B82F6;       /* 亮藍 */
  --color-gradient-start: #6366F1; /* 紫藍 */
  --color-gradient-end: #3B82F6;   /* 亮藍 */
  --color-background: #FFFFFF;   /* 白 */
  --color-text: #1E293B;         /* 深藍灰 */
  --color-light: #F1F5F9;        /* 淺灰藍 */
}
```

### 專業穩重（Corporate Blue）
```css
:root {
  --color-primary: #1E3A8A;      /* 企業藍 */
  --color-secondary: #3B82F6;    /* 亮藍 */
  --color-accent: #10B981;       /* 成功綠 */
  --color-background: #FFFFFF;   /* 白 */
  --color-text: #1F2937;         /* 深灰 */
  --color-light: #F3F4F6;        /* 淺灰 */
}
```

### 創意活力（Creative Bold）
```css
:root {
  --color-primary: #7C3AED;      /* 亮紫 */
  --color-secondary: #EC4899;    /* 桃紅 */
  --color-accent: #F59E0B;       /* 橘黃 */
  --color-background: #FAFAFA;   /* 淺灰 */
  --color-text: #18181B;         /* 近黑 */
  --color-dark: #18181B;         /* 暗背景 */
}
```

### 顧問高端（Premium Dark）
```css
:root {
  --color-primary: #1C1917;      /* 深棕黑 */
  --color-secondary: #292524;    /* 棕灰 */
  --color-accent: #A78BFA;       /* 淡紫 */
  --color-gold: #D4AF37;         /* 金色 */
  --color-background: #FAFAF9;   /* 米白 */
  --color-text: #1C1917;         /* 深棕黑 */
}
```

## 必要頁面結構

### 首頁

1. **Hero 區塊**
   - 價值主張標題
   - 副標說明（1-2 句）
   - 雙 CTA：「預約諮詢」「了解更多」
   - 背景：漸層/圖片/動畫

2. **服務/解決方案**
   - 3-4 個核心服務卡片
   - 圖標 + 標題 + 描述
   - 連結到詳情頁

3. **為什麼選擇我們**
   - 3-4 個差異化優勢
   - 數據佐證

4. **案例/客戶**
   - 成功案例輪播
   - 客戶 Logo 牆
   - 客戶見證引用

5. **CTA 區塊**
   - 行動呼籲
   - 表單或按鈕

### 服務頁
- 服務列表
- 各服務詳情
- 流程說明
- 定價（可選）

### 關於我們
- 公司簡介
- 歷史/里程碑
- 團隊介紹
- 企業文化

### 案例/作品
- 案例分類
- 案例卡片
- 詳情頁：挑戰、解決方案、成果

### 聯絡
- 聯絡表單
- 辦公室資訊
- 社群連結

## 設計細節

### Hero（漸層背景）
```css
.hero {
  min-height: 90vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg,
    var(--color-gradient-start) 0%,
    var(--color-gradient-end) 100%
  );
  position: relative;
  overflow: hidden;
}

/* 裝飾圓形 */
.hero::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  top: -200px;
  right: -200px;
}
```

### 服務卡片
```css
.service-card {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}

.service-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
  color: var(--color-accent);
}
```

### 客戶 Logo 牆
```css
.clients {
  padding: 4rem 0;
  background: var(--color-light);
}

.client-logos {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  flex-wrap: wrap;
}

.client-logo {
  filter: grayscale(100%);
  opacity: 0.6;
  transition: all 0.3s ease;
  max-height: 40px;
}

.client-logo:hover {
  filter: grayscale(0%);
  opacity: 1;
}
```

### 數據統計
```css
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  padding: 4rem 0;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: var(--color-accent);
  margin-bottom: 0.5rem;
}

.stat-label {
  color: var(--color-text);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

### 客戶見證
```css
.testimonial {
  max-width: 700px;
  margin: 0 auto;
  text-align: center;
  padding: 4rem 2rem;
}

.testimonial-quote {
  font-size: 1.5rem;
  line-height: 1.8;
  font-style: italic;
  color: var(--color-text);
  margin-bottom: 2rem;
}

.testimonial-quote::before {
  content: '"';
  font-size: 4rem;
  color: var(--color-accent);
  display: block;
  line-height: 1;
}
```

## 特殊效果

### 計數動畫
```javascript
function animateValue(element, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    element.innerHTML = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}
```

### 滾動進場
```css
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease;
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}
```

## 參考網站

1. [Stripe](https://stripe.com/) - 科技現代
2. [Deloitte](https://deloitte.com/) - 專業穩重
3. [IDEO](https://ideo.com/) - 創意活力
4. [McKinsey](https://mckinsey.com/) - 顧問高端
5. [Notion](https://notion.so/) - 科技簡約
