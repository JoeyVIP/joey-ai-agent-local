# 進化任務：提取 Notion Property 輔助方法

## 安全等級
Level: 1

## 目標
消除 notion_service.py 中重複的 property 建構與解析邏輯，提升程式碼可維護性。

## 修改範圍
- [x] src/services/notion_service.py

## 新增的輔助方法

### 建構方法（寫入時使用）
| 方法 | 用途 |
|------|------|
| `_build_title(value)` | 建構 Notion title 屬性 |
| `_build_rich_text(value, truncate=True)` | 建構 rich_text 屬性（自動截斷） |
| `_build_select(value)` | 建構 select 屬性 |
| `_build_date(value=None)` | 建構 date 屬性（預設現在時間） |
| `_build_number(value)` | 建構 number 屬性 |

### 解析方法（讀取時使用）
| 方法 | 用途 |
|------|------|
| `_parse_title(props, name, default="")` | 解析 title 屬性 |
| `_parse_rich_text(props, name, default="")` | 解析 rich_text 屬性 |
| `_parse_select(props, name, default="")` | 解析 select 屬性 |
| `_parse_date(props, name)` | 解析 date 屬性 |
| `_parse_number(props, name)` | 解析 number 屬性 |

## 更新的方法
- create_inbox_task
- update_inbox_status
- create_review_task_simple
- create_review_task_complex
- update_review_task_status
- update_review_task_result
- get_all_memories
- update_memory
- create_memory
- find_memory_by_title
- create_evolution_task
- _parse_evolution_task
- update_evolution_task_status

## 驗證方式
- [x] python3 -m py_compile src/services/notion_service.py
- [x] curl /health 回應 healthy
- [x] 服務重啟成功

## 效益
- 減少約 30 處重複程式碼
- 統一截斷邏輯（NOTION_MAX_TEXT_LENGTH）
- 提升可讀性和可維護性
- 新增欄位時只需呼叫輔助方法

## 完成狀態
- 狀態：已完成
- 完成時間：2026-02-03
- Git commit：0daca65
