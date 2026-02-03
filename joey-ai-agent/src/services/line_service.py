import asyncio
import logging

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
)
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from src.config import settings

logger = logging.getLogger(__name__)


class LineService:
    """LINE Messaging API 服務"""
    def __init__(self):
        self.handler = WebhookHandler(settings.line_channel_secret)
        self.configuration = Configuration(
            access_token=settings.line_channel_access_token
        )
        self.joey_user_id = settings.joey_line_user_id

    def verify_signature(self, body: str, signature: str) -> bool:
        """Verify LINE webhook signature."""
        try:
            self.handler.handle(body, signature)
            return True
        except InvalidSignatureError:
            logger.warning("LINE 簽名驗證失敗")
            return False

    def _sync_reply_message(self, reply_token: str, message: str) -> None:
        """同步回覆 LINE 訊息（內部使用）"""
        with ApiClient(self.configuration) as api_client:
            api = MessagingApi(api_client)
            api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=message)]
                )
            )

    async def reply_message(self, reply_token: str, message: str) -> None:
        """Reply to a LINE message."""
        try:
            await asyncio.to_thread(self._sync_reply_message, reply_token, message)
            logger.debug(f"LINE 回覆訊息成功: {message[:50]}...")
        except Exception as e:
            logger.error(f"LINE 回覆訊息失敗: {e}")
            raise

    def _sync_push_message(self, user_id: str, message: str) -> None:
        """同步推送 LINE 訊息（內部使用）"""
        with ApiClient(self.configuration) as api_client:
            api = MessagingApi(api_client)
            api.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=[TextMessage(text=message)]
                )
            )

    async def push_message(self, user_id: str, message: str) -> None:
        """Push a message to a user."""
        try:
            await asyncio.to_thread(self._sync_push_message, user_id, message)
            logger.debug(f"LINE 推送訊息成功至 {user_id[:8]}...: {message[:50]}...")
        except Exception as e:
            logger.error(f"LINE 推送訊息失敗至 {user_id[:8]}...: {e}")
            raise

    async def push_to_joey(self, message: str) -> None:
        """Push a message to Joey."""
        logger.info(f"推送訊息給 Joey: {message[:50]}...")
        await self.push_message(self.joey_user_id, message)

    def get_handler(self) -> WebhookHandler:
        """Get the webhook handler for registering event handlers."""
        return self.handler

    def _sync_get_message_content(self, message_id: str) -> bytes:
        """同步下載 LINE 訊息內容（檔案、圖片等）"""
        with ApiClient(self.configuration) as api_client:
            api_blob = MessagingApiBlob(api_client)
            response = api_blob.get_message_content(message_id)
            return response

    async def get_message_content(self, message_id: str) -> bytes:
        """下載 LINE 訊息內容（檔案、圖片等）"""
        try:
            content = await asyncio.to_thread(self._sync_get_message_content, message_id)
            logger.debug(f"成功下載訊息內容: {message_id}")
            return content
        except Exception as e:
            logger.error(f"下載訊息內容失敗: {e}")
            raise


line_service = LineService()
