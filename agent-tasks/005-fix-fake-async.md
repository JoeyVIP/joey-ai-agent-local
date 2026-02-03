# 進化任務：修復 Fake Async 問題

## 安全等級
Level: 1

## 目標
修復使用同步 SDK 但被定義為 async 的方法，避免阻塞事件循環。

## 問題說明
**Fake Async**：方法被定義為 `async def`，但內部沒有使用 `await`，導致：
- 阻塞 FastAPI 事件循環
- 無法同時處理多個請求
- 降低整體吞吐量

## 修改範圍
- [x] src/services/notion_service.py
- [x] src/services/claude_service.py
- [x] src/services/line_service.py

## 解決方案
使用 `asyncio.to_thread()` 將同步呼叫包裝在執行緒中。

### notion_service.py
```python
# 新增輔助方法
async def _run_sync(self, func, *args, **kwargs) -> Any:
    return await asyncio.to_thread(partial(func, *args, **kwargs))

# 使用方式
response = await self._run_sync(
    self.client.pages.create,
    parent={"database_id": self.inbox_db_id},
    properties={...}
)
```

### claude_service.py
```python
response = await asyncio.to_thread(
    self.client.messages.create,
    model=self.model,
    max_tokens=CLAUDE_MAX_TOKENS,
    ...
)
```

### line_service.py
```python
def _sync_reply_message(self, reply_token, message):
    # 同步邏輯
    ...

async def reply_message(self, reply_token, message):
    await asyncio.to_thread(self._sync_reply_message, reply_token, message)
```

## 修改的方法

### notion_service.py (15 個方法)
- create_inbox_task
- update_inbox_status
- delete_inbox_task
- create_review_task_simple
- create_review_task_complex
- update_review_task_status
- update_review_task_result
- get_all_memories
- update_memory
- create_memory
- find_memory_by_title
- create_evolution_task
- get_pending_evolution_tasks
- get_evolution_task
- update_evolution_task_status
- get_evolution_history

### claude_service.py (1 個方法)
- process_task

### line_service.py (2 個方法)
- reply_message
- push_message

## 驗證方式
- [x] python3 -m py_compile（三個檔案）
- [x] curl /health 回應 healthy
- [x] 服務重啟成功

## 效益
- 不再阻塞事件循環
- 可同時處理多個請求
- 提升整體吞吐量

## 完成狀態
- 狀態：已完成
- 完成時間：2026-02-03
- Git commit：78d7f85
