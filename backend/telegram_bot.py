"""
Telegram bot dùng chung logic trả lời với web widget (ask_claude trong main.py).
Chạy theo kiểu webhook, gắn vào FastAPI app (xem main.py).

Thiết lập webhook sau khi deploy (chạy 1 lần):
  curl -F "url=https://<your-domain>/telegram/webhook/<TELEGRAM_WEBHOOK_SECRET>" \\
       https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook
"""

import os
import httpx
from fastapi import APIRouter, Request, HTTPException

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "change-me")

router = APIRouter()

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


async def send_telegram_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": text, "disable_web_page_preview": True},
            timeout=20,
        )


@router.post("/telegram/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if not TELEGRAM_BOT_TOKEN:
        raise HTTPException(500, "Thiếu TELEGRAM_BOT_TOKEN")
    if secret != TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(403, "Sai webhook secret")

    update = await request.json()
    message = update.get("message") or update.get("edited_message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    if not text:
        await send_telegram_message(chat_id, "Xin lỗi, mình chỉ xử lý được tin nhắn văn bản 🙏")
        return {"ok": True}

    # dùng chính Telegram chat_id làm session_id để giữ lịch sử hội thoại riêng từng khách
    from main import ask_groq  # import trễ để tránh vòng lặp import

    session_id = f"tg-{chat_id}"
    try:
        reply = ask_groq(session_id, text)
    except Exception as e:
        reply = f"Xin lỗi, hệ thống đang gặp sự cố. Vui lòng liên hệ trực tiếp @Clickbuy_ru. ({e})"

    await send_telegram_message(chat_id, reply)
    return {"ok": True}
