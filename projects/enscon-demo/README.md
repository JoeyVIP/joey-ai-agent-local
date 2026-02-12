# 來電司康 — 建站測試案 #2

## 專案概述

為「來電司康股份有限公司」建立完整的建站資料，作為 Joey AI Agent 建站服務的第二個測試案例。

## 資料來源標註

### 來自簡報（主要內容來源）
> 檔案：`傳產 AI 進化專案：客戶簡報用素材V2.md`

- 核心業務定位（營收成長顧問 + AI 技術）
- 三大優勢（AI 輔助設計、標準化流程、專業團隊把關）
- 服務方案（基本 / CMS 後台 / 多語系）
- 服務流程四步驟
- 網站功能規格（SEO、響應式、高速載入、安全）
- 價格比較（傳統 30-60 萬 vs 我們個位數萬~20 萬）
- FAQ（前 4 題）
- 合作夥伴（暖色系設計）

### 來自簡報 PDF（圖片素材）
> 檔案：`傳產數位轉型簡報V4.pdf`

- 7 張高解析度簡報頁面擷取圖（5732x3200, 300dpi）
- 包含：Hero 封面、痛點人物照、傳統 vs AI 對比、價格比較、三大優勢、服務流程、CTA+QR Code

### 來自舊官網 (enscon.co)
- 公司基本資訊（公司名、統一編號、地址、Email）
- 聯絡資訊（LINE 官方帳號、Joey LINE ID）
- Logo 圖片 4 張 + LINE QR Code 1 張

### AI 生成內容
- Hero 主標語、副標語
- 品牌故事（基於簡報內容合理推敲）
- 數字統計區塊
- 補充 FAQ（第 5-8 題）
- SEO Title / Description / Keywords
- 網站設計風格需求

## 檔案結構

```
projects/enscon-demo/
├── 傳產 AI 進化專案：客戶簡報用素材V2.md  ← 原始簡報（已存在）
├── content.md          ← 結構化建站內容
├── README.md           ← 本檔案
└── images/
    ├── logo-dark.png                  (1738x666, 深色 Logo, 舊官網)
    ├── logo-light.png                 (1255x1255, 淺色 Logo, 舊官網)
    ├── logo-horizontal.png            (1738x666, 橫式組合 Logo, 舊官網)
    ├── favicon.png                    (582x590, Favicon, 舊官網)
    ├── line-qrcode.png                (592x1443, LINE QR Code, 舊官網)
    ├── slide-01-hero-cover.png        (5732x3200, 封面：齒輪→電路板, 簡報)
    ├── slide-02-pain-points.png       (5732x3200, 工廠老闆拿平板, 簡報)
    ├── slide-05-traditional-vs-ai.png (5732x3200, 傳統 vs AI 對比, 簡報)
    ├── slide-06-price-comparison.png  (5732x3200, 價格比較卡, 簡報)
    ├── slide-07-three-advantages.png  (5732x3200, 三大優勢 icon, 簡報)
    ├── slide-08-service-flow.png      (5732x3200, 四步驟流程圖, 簡報)
    └── slide-14-cta-qrcode.png        (5732x3200, CTA+QR Code, 簡報)
```

## 行業模板對應

| 項目 | 值 |
|------|------|
| 行業 | 顧問 / AI 技術服務 |
| 對應模板 | `corporate.md`（企業官網模板） |
| 風格方向 | 科技商務風，專業信賴 + 科技感 + 親和力 |
| 配色方向 | 深藍或墨綠 + 白 + 暖色強調色 |

## 注意事項

- 服務內容以簡報為主，**不使用**舊官網列出的舊服務項目
- 價格資訊已包含在 content.md 中（用戶確認要放）
- 品牌故事由 AI 基於簡報內容生成（用戶確認）
- Logo + QR Code 來自舊官網 CDN (qdm.cloud)
- 簡報頁面圖片從 `傳產數位轉型簡報V4.pdf` 擷取（300dpi 高解析度）
- 舊官網 banner 已刪除（含舊服務內容，不適用）
- 所有圖片已驗證為真實 PNG

## 建站時 LINE 訊息範本

見本檔案底部的「LINE 訊息模板」段落。

---

## Google Drive 上傳清單

上傳到 Google Drive 時，使用扁平結構（不建子資料夾）：

1. `content.md`
2. `logo-dark.png`
3. `logo-light.png`
4. `logo-horizontal.png`
5. `favicon.png`
6. `line-qrcode.png`
7. `slide-01-hero-cover.png`
8. `slide-02-pain-points.png`
9. `slide-05-traditional-vs-ai.png`
10. `slide-06-price-comparison.png`
11. `slide-07-three-advantages.png`
12. `slide-08-service-flow.png`
13. `slide-14-cta-qrcode.png`

> 設定權限為「知道連結的任何人」可查看

---

## LINE 訊息模板

上傳 Google Drive 後，複製以下訊息發送給 Joey AI Agent：

```
請幫我建立來電司康的企業官網

素材連結：https://drive.google.com/drive/folders/{替換為實際資料夾ID}?usp=sharing

請先用 gdown 下載所有素材到 ./assets 資料夾：
gdown --folder "上述連結" -O ./assets

然後讀取 content.md 了解網站內容，按照裡面的結構建站。

重點提醒：
1. 請載入 corporate.md 企業官網模板 + base-guidelines.md 共用設計原則
2. 配色用深藍或墨綠 + 白 + 暖色強調色，科技商務風但不冰冷
3. 價格比較區塊是重點，要讓「傳統 30-60 萬 vs 我們個位數萬」的差異非常醒目
4. 素材中有 7 張從簡報擷取的高解析度圖片（slide-*.png），content.md 裡有標註每張圖的對應位置
5. slide-01 是 Hero 背景、slide-02 是痛點區塊、slide-05/06 是價格對比、slide-07 是三大優勢、slide-08 是服務流程
6. 不要用 Inter / Roboto / Arial 等 generic 字體
```

---

*建立日期：2026-02-06*
