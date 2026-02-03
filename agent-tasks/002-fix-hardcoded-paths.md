# 進化任務：修復硬編碼路徑

## 安全等級
Level: 1

## 目標
移除硬編碼路徑，使用動態路徑計算，提升專案的可移植性。

## 修改範圍
- [x] src/constants.py（新增常數）
- [x] src/api/line_webhook.py（修復硬編碼路徑）

## 執行步驟
1. 在 constants.py 新增 USER_IDS_LOG_FILENAME 常數
2. 在 line_webhook.py 中：
   - 匯入 pathlib 和常數
   - 定義 PROJECT_ROOT 使用相對路徑計算
   - 將 `/Users/joeyserver/joey-ai-agent/user_ids.log` 替換為 `PROJECT_ROOT / USER_IDS_LOG_FILENAME`
   - 將 `[:200]`、`[:100]`、`[:50]` 替換為對應常數

## 驗證方式
- [x] python3 -m py_compile src/constants.py
- [x] python3 -m py_compile src/api/line_webhook.py
- [x] curl /health 回應 healthy
- [x] 服務重啟成功

## 完成狀態
- 狀態：已完成
- 完成時間：2026-02-03
- Git commit：e411381
