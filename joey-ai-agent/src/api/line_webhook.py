import logging
import json
import hashlib
import hmac
import base64
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks

from src.services.line_service import line_service
from src.services.task_processor import task_processor
from src.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["line"])

# 授權使用者清單（ID -> 名稱）
# 只有在這個清單中的使用者才能使用此 Bot
AUTHORIZED_USERS = {
    settings.joey_line_user_id: "Joey",
    "U07923894d7eb396901da0796ee96d0c6": "Cindy",
}


async def process_message_background(user_input: str, user_id: str, user_name: str):
    """Background task to process LINE message."""
    try:
        logger.info(f"Processing task for {user_name} ({user_id})")
        await task_processor.process_task(
            user_input=user_input,
            source="line"
        )
    except Exception as e:
        logger.error(f"Background task failed for {user_name}: {e}", exc_info=True)


@router.post("/webhook/line")
async def line_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    LINE Webhook endpoint.

    Flow:
    1. Verify signature
    2. Parse events
    3. Reply immediately with "收到，處理中"
    4. Process task in background
    """
    # Get signature from header
    signature = request.headers.get("X-Line-Signature", "")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    # Get request body
    body = await request.body()
    body_str = body.decode("utf-8")

    # Parse the webhook body manually to extract events
    try:
        body_json = json.loads(body_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Verify signature
    try:
        channel_secret = settings.line_channel_secret
        hash_value = hmac.new(
            channel_secret.encode("utf-8"),
            body_str.encode("utf-8"),
            hashlib.sha256
        ).digest()
        computed_signature = base64.b64encode(hash_value).decode("utf-8")

        if signature != computed_signature:
            raise HTTPException(status_code=400, detail="Invalid signature")

    except Exception as e:
        logger.error(f"Signature verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Process events
    events = body_json.get("events", [])

    for event in events:
        # Only handle text messages
        if event.get("type") != "message":
            continue
        if event.get("message", {}).get("type") != "text":
            continue

        reply_token = event.get("replyToken")
        user_id = event.get("source", {}).get("userId")
        user_input = event.get("message", {}).get("text", "")

        if not user_input:
            continue

        logger.info(f"Received message from {user_id}: {user_input[:50]}...")

        # 檢查使用者是否授權
        if user_id not in AUTHORIZED_USERS:
            logger.warning(f"Unauthorized user attempted access: {user_id}")
            try:
                await line_service.reply_message(
                    reply_token=reply_token,
                    message="抱歉，你目前沒有使用權限。請聯繫管理員。"
                )
            except Exception as e:
                logger.error(f"Failed to send unauthorized reply: {e}")
            continue

        # 取得使用者名稱
        user_name = AUTHORIZED_USERS[user_id]
        logger.info(f"Authorized user: {user_name} ({user_id})")

        # 回覆確認訊息（個人化）
        try:
            await line_service.reply_message(
                reply_token=reply_token,
                message=f"📝 收到，{user_name}！處理中..."
            )
        except Exception as e:
            logger.error(f"Failed to send reply to {user_name}: {e}")

        # 加入背景任務處理
        background_tasks.add_task(
            process_message_background,
            user_input=user_input,
            user_id=user_id,
            user_name=user_name
        )

    return {"status": "ok"}
