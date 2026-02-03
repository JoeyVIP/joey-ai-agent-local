# 進化任務：為服務加入 Logging 支援

## 安全等級
Level: 2

## 目標
為缺少 logging 的服務加入日誌記錄，改善錯誤追蹤和偵錯能力。

## 修改範圍
- [x] src/services/notion_service.py
- [x] src/services/claude_service.py
- [x] src/services/line_service.py

## 新增的 Logging

### notion_service.py
| 方法 | 日誌級別 | 內容 |
|------|----------|------|
| create_inbox_task | info | 建立任務標題 |
| create_review_task_* | info | 建立任務標題和類型 |
| create_memory | info | 記憶標題、分類、重要性 |
| create_evolution_task | info | 任務標題、類型、等級 |
| 所有 CRUD | debug | 操作成功的 page_id |
| 所有錯誤 | error | 例外訊息和堆疊追蹤 |

### claude_service.py
| 方法 | 日誌級別 | 內容 |
|------|----------|------|
| process_task | info | 模型名稱、回應長度 |
| process_task | debug | 使用者輸入預覽 |
| _parse_json_response | debug | JSON 提取來源、難度 |
| _parse_json_response | warning | JSON 解析失敗 |

### line_service.py
| 方法 | 日誌級別 | 內容 |
|------|----------|------|
| verify_signature | warning | 簽名驗證失敗 |
| reply_message | debug | 回覆成功 |
| push_message | debug | 推送成功 |
| push_to_joey | info | 推送給 Joey |
| 所有錯誤 | error | 例外訊息 |

## 驗證方式
- [x] python3 -m py_compile（三個檔案）
- [x] curl /health 回應 healthy
- [x] 服務重啟成功

## 效益
- 可追蹤所有 Notion 操作
- 可追蹤 Claude API 呼叫
- 可追蹤 LINE 訊息發送
- 錯誤發生時有完整堆疊追蹤

## 完成狀態
- 狀態：已完成
- 完成時間：2026-02-03
- Git commit：f5ca8cb
