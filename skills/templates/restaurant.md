# 餐廳/咖啡廳網站模板

專為餐廳、咖啡廳、甜點店、酒吧設計的網站模板。

## 美學方向

根據餐廳類型選擇：

### A. 文青咖啡廳 (Artisan Cafe)
- 溫暖、手作感、質樸
- 木質紋理、手繪元素
- 米色、棕色、綠色系

### B. 高級餐廳 (Fine Dining)
- 優雅、精緻、奢華
- 大量留白、精美排版
- 黑、金、白配色

### C. 活力餐廳 (Casual Dining)
- 活潑、親切、食慾感
- 大圖片、明亮色彩
- 橘、紅、黃暖色系

### D. 日式/極簡 (Zen Minimal)
- 寧靜、乾淨、禪意
- 大量負空間
- 白、淺灰、原木色

## 字體推薦

### 文青咖啡廳
```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Lora:wght@400;500&display=swap');

h1, h2, h3 {
  font-family: 'Cormorant Garamond', 'Noto Serif TC', serif;
  font-weight: 400;
}

body, p {
  font-family: 'Lora', 'Noto Serif TC', serif;
}
```

### 高級餐廳
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Montserrat:wght@300;400&display=swap');

h1, h2, h3 {
  font-family: 'Playfair Display', 'Noto Serif TC', serif;
  font-style: italic;
}

body, p {
  font-family: 'Montserrat', 'Noto Sans TC', sans-serif;
  font-weight: 300;
  letter-spacing: 0.05em;
}
```

### 活力餐廳
```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

h1, h2, h3 {
  font-family: 'Poppins', 'Noto Sans TC', sans-serif;
  font-weight: 700;
}
```

### 日式極簡
```css
@import url('https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@300;500&display=swap');

body {
  font-family: 'Zen Kaku Gothic New', 'Noto Sans TC', sans-serif;
  font-weight: 300;
}
```

## 配色方案

### 文青咖啡（Warm Earth）
```css
:root {
  --color-primary: #5D4037;      /* 咖啡棕 */
  --color-secondary: #8D6E63;    /* 淺棕 */
  --color-accent: #2E7D32;       /* 植物綠 */
  --color-background: #FFF8E1;   /* 米白 */
  --color-text: #3E2723;         /* 深棕 */
  --color-cream: #EFEBE9;        /* 奶油色 */
}
```

### 高級餐廳（Elegant Dark）
```css
:root {
  --color-primary: #1A1A1A;      /* 純黑 */
  --color-secondary: #2D2D2D;    /* 深灰 */
  --color-accent: #C9A961;       /* 香檳金 */
  --color-background: #FFFFFF;   /* 純白 */
  --color-text: #1A1A1A;         /* 黑 */
  --color-light: #F5F5F5;        /* 淺灰 */
}
```

### 活力餐廳（Appetizing）
```css
:root {
  --color-primary: #D84315;      /* 番茄紅 */
  --color-secondary: #FF8A65;    /* 珊瑚橘 */
  --color-accent: #FFC107;       /* 芥末黃 */
  --color-background: #FFFDE7;   /* 淺黃 */
  --color-text: #37474F;         /* 深灰 */
  --color-green: #689F38;        /* 蔬菜綠 */
}
```

### 日式極簡（Zen）
```css
:root {
  --color-primary: #424242;      /* 墨灰 */
  --color-secondary: #9E9E9E;    /* 淺灰 */
  --color-accent: #8D6E63;       /* 木質色 */
  --color-background: #FAFAFA;   /* 米白 */
  --color-text: #212121;         /* 黑 */
}
```

## 必要頁面結構

### 首頁

1. **Hero 區塊**
   - 全幅美食/店內照片
   - 店名 + Slogan
   - CTA：「線上訂位」「查看菜單」

2. **關於區塊**
   - 故事/理念（左右圖文）
   - 主廚介紹（可選）

3. **招牌菜展示**
   - 3-4 道精選菜品
   - 大圖 + 名稱 + 簡述
   - 點擊進入完整菜單

4. **用餐資訊**
   - 營業時間
   - 地址 + 地圖
   - 訂位電話

5. **Instagram Feed**（可選）
   - 嵌入或靜態圖片牆

### 菜單頁
- 分類標籤（前菜、主餐、甜點、飲料）
- 菜品卡片：圖片 + 名稱 + 描述 + 價格
- 過敏原標示（可選）

### 關於我們
- 品牌故事
- 店內環境照
- 團隊/主廚介紹

### 聯絡/訂位
- 線上訂位表單
- 營業時間
- 地圖嵌入
- 社群連結

## 設計細節

### Hero 處理（全幅美食照）
```css
.hero {
  position: relative;
  height: 100vh;
  min-height: 600px;
  background:
    linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.5)),
    url('/images/hero-food.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero h1 {
  color: white;
  font-size: clamp(2.5rem, 6vw, 5rem);
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
```

### 菜品卡片
```css
.menu-item {
  display: grid;
  grid-template-columns: 120px 1fr auto;
  gap: 1.5rem;
  padding: 1.5rem 0;
  border-bottom: 1px solid var(--color-border);
  align-items: center;
}

.menu-item img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
}

.menu-item .price {
  font-weight: 600;
  color: var(--color-primary);
}
```

### 營業時間區塊
```css
.hours {
  background: var(--color-cream);
  padding: 3rem;
  text-align: center;
}

.hours-table {
  display: inline-grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 2rem;
  text-align: left;
}
```

## 圖片建議

### 必要圖片
1. Hero - 招牌菜或店內氛圍
2. 菜品照 - 每道菜獨立照片
3. 店內環境 - 座位區、裝潢
4. 主廚/團隊（可選）

### 攝影風格
- **食物**：近拍、淺景深、自然光
- **環境**：廣角、展現氛圍
- **暖色調濾鏡增加食慾感**

## 特殊效果

### Parallax 滾動（Hero）
```css
.hero {
  background-attachment: fixed;
}

@media (max-width: 768px) {
  .hero {
    background-attachment: scroll; /* 手機關閉 parallax */
  }
}
```

### 圖片 Hover 效果
```css
.menu-item img {
  transition: transform 0.3s ease;
}

.menu-item:hover img {
  transform: scale(1.05);
}
```

## 參考網站

1. [Blue Bottle Coffee](https://bluebottlecoffee.com/) - 極簡咖啡廳
2. [Noma](https://noma.dk/) - 高級餐廳標竿
3. [Shake Shack](https://shakeshack.com/) - 活力速食
4. [% Arabica](https://arabica.coffee/) - 日式極簡咖啡
