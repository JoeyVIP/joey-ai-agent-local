# 品牌官網模板

專為產品品牌、生活風格品牌、設計師品牌設計的網站模板。

## 美學方向

根據品牌定位選擇：

### A. 極簡高端 (Minimal Luxury)
- Apple 風格、大量留白
- 產品英雄展示
- 黑白灰 + 單一強調色

### B. 潮流街頭 (Street Culture)
- 大膽、衝突、打破規則
- 不對稱版面、粗體字
- 高對比、螢光色

### C. 自然有機 (Organic Natural)
- 環保、永續、自然
- 柔和曲線、手繪元素
- 大地色系、植物元素

### D. 復古懷舊 (Retro Vintage)
- 復刻、工藝、故事性
- 紋理背景、襯線字體
- 棕、金、深紅色系

## 字體推薦

### 極簡高端
```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

body {
  font-family: 'Outfit', 'Noto Sans TC', sans-serif;
  font-weight: 300;
  letter-spacing: 0.02em;
}

h1, h2 {
  font-weight: 400;
  letter-spacing: 0.1em;
}
```

### 潮流街頭
```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap');

/* 注意：Space Grotesk 雖被列為常見選擇，在街頭風格仍適用 */
/* 替代選擇：Archivo Black, Anton */

h1, h2, h3 {
  font-family: 'Space Grotesk', 'Noto Sans TC', sans-serif;
  font-weight: 700;
  text-transform: uppercase;
}
```

### 自然有機
```css
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Karla:wght@400;500&display=swap');

h1, h2, h3 {
  font-family: 'DM Serif Display', 'Noto Serif TC', serif;
}

body, p {
  font-family: 'Karla', 'Noto Sans TC', sans-serif;
}
```

### 復古懷舊
```css
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Crimson+Text:wght@400;600&display=swap');

h1, h2, h3 {
  font-family: 'Libre Baskerville', 'Noto Serif TC', serif;
}
```

## 配色方案

### 極簡高端（Monochrome）
```css
:root {
  --color-primary: #000000;      /* 純黑 */
  --color-secondary: #666666;    /* 中灰 */
  --color-accent: #0066FF;       /* 科技藍（可替換） */
  --color-background: #FFFFFF;   /* 純白 */
  --color-text: #1A1A1A;         /* 近黑 */
  --color-light: #F5F5F5;        /* 淺灰 */
}
```

### 潮流街頭（Bold Contrast）
```css
:root {
  --color-primary: #000000;      /* 黑 */
  --color-secondary: #1A1A1A;    /* 深灰 */
  --color-accent: #00FF88;       /* 螢光綠 */
  --color-highlight: #FF3366;    /* 螢光桃 */
  --color-background: #0A0A0A;   /* 近黑 */
  --color-text: #FFFFFF;         /* 白 */
}
```

### 自然有機（Earth Tones）
```css
:root {
  --color-primary: #4A5D4E;      /* 森林綠 */
  --color-secondary: #8B7355;    /* 土棕 */
  --color-accent: #D4A574;       /* 陶土橘 */
  --color-background: #FAF6F1;   /* 米白 */
  --color-text: #2D3830;         /* 深綠灰 */
  --color-cream: #F5EDE4;        /* 奶油 */
}
```

### 復古懷舊（Vintage Warm）
```css
:root {
  --color-primary: #8B0000;      /* 深紅 */
  --color-secondary: #4A3C31;    /* 深棕 */
  --color-accent: #C9A961;       /* 金色 */
  --color-background: #FDF5E6;   /* 老紙色 */
  --color-text: #2C2416;         /* 深棕 */
}
```

## 必要頁面結構

### 首頁

1. **Hero 區塊**
   - 產品全幅展示或品牌視覺
   - 品牌 Slogan
   - CTA：「探索系列」「立即購買」

2. **品牌宣言**
   - 一句話品牌精神
   - 配合動態視覺或影片

3. **產品系列**
   - 2-4 個系列入口
   - 大圖 + 系列名 + 簡述
   - Hover 效果

4. **品牌故事**
   - 左右交錯圖文
   - 創辦人/品牌歷程

5. **社群/新聞**
   - Instagram 嵌入
   - 最新消息

### 產品頁
- 產品分類
- 產品列表（Grid）
- 產品詳情：多角度圖片、規格、購買

### 關於品牌
- 品牌故事
- 理念與價值
- 團隊介紹（可選）
- 新聞報導（可選）

### 聯絡
- 客服表單
- 社群連結
- 實體店位置（如有）

## 設計細節

### Hero 產品展示
```css
.hero {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background);
}

.hero-product {
  max-width: 60%;
  animation: floatIn 1s ease-out;
}

@keyframes floatIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 產品卡片
```css
.product-card {
  position: relative;
  overflow: hidden;
}

.product-card img {
  transition: transform 0.5s ease;
}

.product-card:hover img {
  transform: scale(1.05);
}

.product-info {
  padding: 1.5rem 0;
}

.product-name {
  font-size: 1rem;
  letter-spacing: 0.05em;
}

.product-price {
  color: var(--color-secondary);
}
```

### 左右交錯版面
```css
.story-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  min-height: 80vh;
}

.story-section:nth-child(even) {
  direction: rtl;
}

.story-section:nth-child(even) > * {
  direction: ltr;
}

.story-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.story-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 4rem;
}
```

### 視差滾動標語
```css
.manifesto {
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  color: white;
}

.manifesto h2 {
  font-size: clamp(2rem, 5vw, 4rem);
  text-align: center;
  max-width: 800px;
  line-height: 1.4;
}
```

## 特殊效果

### 滑鼠追蹤效果（潮流風格）
```javascript
document.addEventListener('mousemove', (e) => {
  const cursor = document.querySelector('.cursor');
  cursor.style.left = e.clientX + 'px';
  cursor.style.top = e.clientY + 'px';
});
```

### 滾動淡入
```css
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}
```

## 參考網站

1. [Apple](https://apple.com/) - 極簡科技
2. [Aesop](https://aesop.com/) - 極簡自然
3. [Supreme](https://supremenewyork.com/) - 街頭潮流
4. [Patagonia](https://patagonia.com/) - 自然環保
5. [Diptyque](https://diptyqueparis.com/) - 復古奢華
