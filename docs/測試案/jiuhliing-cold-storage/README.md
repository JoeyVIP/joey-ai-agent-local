# 測試案：巨領企業有限公司 — 冷凍冷藏倉儲官網

## 用途

這是 Joey AI Agent 建站功能的測試案資料，模擬一個真實企業完成業主訪談後的建站素材產出。用於測試 Agent 能否依據 `content.md` 自動生成完整的企業官網。

## 公司簡介

巨領企業有限公司成立於 2000 年，位於屏東市工業區，是南台灣專業的冷凍冷藏倉儲服務商。擁有雙廠區，採用德國 Bitzer、Guntner 及義大利 ICAM 等歐洲進口設備，提供冷凍庫出租、冷藏庫出租、低溫倉儲及代客理貨等服務。

## 資料來源

| 內容 | 來源 | 說明 |
|------|------|------|
| 公司名稱、地址、電話、Email、LINE | 真實資料 | 來自官網 jiuhliing.com.tw |
| 創辦人背景、設備規格、廠區介紹 | 真實資料 | 來自官網內容 |
| 知名客戶（富統食品、瓜瓜園） | 真實資料 | 來自官網 |
| 經營理念（誠信、積極、熱誠、效率、責任） | 真實資料 | 來自官網 |
| Hero 主標語、副標語 | 生成 | 基於真實定位潤飾 |
| 品牌故事（擴寫版） | 生成 | 以真實創辦背景為基礎擴寫 |
| 服務詳細說明、適用對象 | 生成 | 基於行業常識補充 |
| FAQ 問答 | 生成 | 基於行業常識生成 |
| SEO Title / Description / Keywords | 生成 | 基於服務內容生成 |
| 數字統計區塊 | 真實 + 生成 | 數據真實，呈現方式生成 |
| 網站設計需求 | 模擬 | 模擬業主訪談時的設計偏好 |

## 圖片素材

所有圖片從巨領企業官網（jiuhliing.com.tw）下載，共 16 張：

- `logo.png` — 公司 Logo
- `hero-banner.jpg` — 首頁橫幅大圖
- `company-profile.jpg` — 公司外觀
- `factory2-exterior.png` — 二廠外觀
- `equipment-*.jpg` — 設備照片（6 張）
- `icon-*.png` — 經營理念圖示（5 張）

## 對應模板

此測試案屬於 **製造業/工業服務業** 類型，建站時應參考：
- `skills/templates/manufacturing.md` — 代工廠/製造業模板
- `skills/templates/base-guidelines.md` — 共用設計原則

## 檔案結構

```
jiuhliing-cold-storage/
├── content.md          # 結構化建站內容（主要產出）
├── README.md           # 本檔案
└── images/             # 圖片素材（16 張）
    ├── logo.png
    ├── hero-banner.jpg
    ├── company-profile.jpg
    ├── factory2-exterior.png
    ├── equipment-guntner-evaporator.jpg
    ├── equipment-temp-control.jpg
    ├── equipment-bitzer-compressor.jpg
    ├── equipment-icam-shelving.jpg
    ├── equipment-dock-1.jpg
    ├── equipment-dock-2.jpg
    ├── equipment-dock-3.jpg
    ├── icon-integrity.png
    ├── icon-proactivity.png
    ├── icon-enthusiasm.png
    ├── icon-efficiency.png
    └── icon-responsibility.png
```
