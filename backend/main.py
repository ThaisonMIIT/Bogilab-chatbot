"""
Backend chung cho chatbot Bogilab.
- POST /chat        -> dùng cho widget web
- Telegram webhook  -> dùng cho bot Telegram (chạy trong cùng app, xem telegram_bot.py)

AI: Google Gemini (free tier) qua REST API.

Chạy local:  uvicorn main:app --reload --port 8000
Deploy:      xem README.md (Railway / Render / VPS)
"""

import os
import uuid
from typing import Dict, List

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from knowledge_base import build_system_prompt

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Thiếu biến môi trường GEMINI_API_KEY")

# Model free tier của Google. Có thể đổi qua biến môi trường GEMINI_MODEL.
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
)

SYSTEM_PROMPT = build_system_prompt()

app = FastAPI(title="Bogilab Chatbot API")

# CORS: cho phép widget nhúng trên web của bạn gọi API này.
# Đổi "*" thành domain thật của bạn khi deploy production, vd ["https://bogilab.ru"]
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lưu lịch sử hội thoại tạm trong RAM theo session_id.
# Đủ dùng cho quy mô nhỏ; nếu cần bền vững/nhiều instance thì thay bằng Redis.
SESSIONS: Dict[str, List[dict]] = {}
MAX_HISTORY_MESSAGES = 20  # giới hạn để không phình context


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str


def ask_gemini(session_id: str, user_message: str) -> str:
    """
    Gọi Gemini API (REST) với lịch sử hội thoại của session này.
    Định dạng Gemini: contents = [{role: "user"|"model", parts: [{text: ...}]}]
    System prompt truyền riêng qua "system_instruction".
    """
    history = SESSIONS.setdefault(session_id, [])
    history.append({"role": "user", "parts": [{"text": user_message}]})
    history[:] = history[-MAX_HISTORY_MESSAGES:]

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": history,
        "generationConfig": {"maxOutputTokens": 800, "temperature": 0.4},
    }

    with httpx.Client(timeout=30) as client:
        resp = client.post(GEMINI_URL, json=payload)

    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API lỗi {resp.status_code}: {resp.text[:300]}")

    data = resp.json()
    try:
        candidate = data["candidates"][0]
        reply_text = "".join(
            part.get("text", "") for part in candidate["content"]["parts"]
        ).strip()
    except (KeyError, IndexError):
        reply_text = (
            "Xin lỗi, mình chưa trả lời được câu này. "
            "Vui lòng liên hệ trực tiếp Telegram @Clickbuy_ru."
        )

    history.append({"role": "model", "parts": [{"text": reply_text}]})
    history[:] = history[-MAX_HISTORY_MESSAGES:]
    return reply_text


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(400, "message không được để trống")

    session_id = req.session_id or str(uuid.uuid4())
    try:
        reply = ask_gemini(session_id, req.message.strip())
    except Exception as e:
        raise HTTPException(500, f"Lỗi khi gọi Gemini API: {e}")

    return ChatResponse(reply=reply, session_id=session_id)


# --- Gắn Telegram webhook vào cùng app FastAPI ---
from telegram_bot import router as telegram_router  # noqa: E402

app.include_router(telegram_router)
