# 基礎設計原則

所有行業模板的共用設計規範。

## 字體選擇原則

### 禁止使用的字體（AI Slop）
- Inter、Roboto、Arial、Helvetica
- System fonts、sans-serif fallback
- 任何 generic 字體

### 推薦來源
- [Google Fonts](https://fonts.google.com/) - 免費，CDN 穩定
- 優先選擇有個性的字體，避免「安全選擇」

### 中英文配對策略
```css
/* 標題 - 英文裝飾字 + 中文黑體 */
.heading {
  font-family: 'Playfair Display', 'Noto Sans TC', serif;
}

/* 內文 - 易讀為主 */
.body {
  font-family: 'Source Sans Pro', 'Noto Sans TC', sans-serif;
}
```

## 配色原則

### CSS Variables（必須使用）
```css
:root {
  --color-primary: #1a1a2e;
  --color-secondary: #16213e;
  --color-accent: #e94560;
  --color-background: #f5f5f5;
  --color-text: #333333;
  --color-text-light: #666666;
}
```

### 配色比例
- 主色 60%：背景、大區塊
- 輔色 30%：次要區塊、邊框
- 強調色 10%：CTA 按鈕、重點標記

### 避免的配色
- 紫色漸層 + 白底（AI slop 典型）
- 純黑 + 純白（缺乏層次）
- 彩虹色系（過於花俏）

## 排版原則

### 負空間
- 區塊間距至少 60px（手機 40px）
- 內容不要塞滿，留白是設計的一部分

### 層次結構
```css
h1 { font-size: clamp(2rem, 5vw, 3.5rem); }
h2 { font-size: clamp(1.5rem, 4vw, 2.5rem); }
h3 { font-size: clamp(1.25rem, 3vw, 1.75rem); }
p  { font-size: clamp(1rem, 2vw, 1.125rem); }
```

### 行高
- 標題：1.2 - 1.3
- 內文：1.6 - 1.8

## 動畫原則

### 入場動畫
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: fadeInUp 0.6s ease-out;
}
```

### Staggered Reveal（推薦）
```css
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
.stagger-3 { animation-delay: 0.3s; }
```

### 避免的動畫
- 無限循環的裝飾動畫
- 過度彈跳效果
- 讓人頭暈的旋轉

## 背景處理

### 推薦技巧
- **漸層疊加**：圖片上加半透明漸層增加可讀性
- **紋理**：微妙的 noise texture 增加質感
- **幾何圖案**：SVG pattern 作為裝飾

### 範例
```css
.hero {
  background:
    linear-gradient(135deg, rgba(0,0,0,0.7), rgba(0,0,0,0.3)),
    url('/images/hero.jpg');
  background-size: cover;
  background-position: center;
}
```

## 按鈕設計

### 主要按鈕
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

### 最小觸控區域
- 寬高至少 44px x 44px（手機友善）

## 圖片處理

### 響應式圖片
```html
<img
  src="image.jpg"
  alt="描述文字"
  loading="lazy"
  style="max-width: 100%; height: auto;"
>
```

### 圖片比例
- Hero: 16:9 或 21:9
- 卡片: 4:3 或 1:1
- 產品: 1:1 或 3:4
