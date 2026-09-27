"""
Backend chung cho chatbot Bogilab.
- POST /chat        -> dùng cho widget web
- Telegram webhook  -> dùng cho bot Telegram (chạy trong cùng app, xem telegram_bot.py)

AI: Groq (free tier, chuẩn API tương thích OpenAI). Không bị giới hạn vùng miền
như Google Gemini AI Studio.

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

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Thiếu biến môi trường GROQ_API_KEY")

# Model free tier của Groq. Có thể đổi qua biến môi trường GROQ_MODEL.
# llama-3.3-70b-versatile: chất lượng tốt, đủ nhanh, free tier hào phóng.
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

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


def ask_groq(session_id: str, user_message: str) -> str:
    """
    Gọi Groq API (chuẩn OpenAI chat completions) với lịch sử hội thoại của session này.
    """
    history = SESSIONS.setdefault(session_id, [])
    history.append({"role": "user", "content": user_message})
    history[:] = history[-MAX_HISTORY_MESSAGES:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.4,
    }
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    with httpx.Client(timeout=30) as client:
        resp = client.post(GROQ_URL, json=payload, headers=headers)

    if resp.status_code != 200:
        raise RuntimeError(f"Groq API lỗi {resp.status_code}: {resp.text[:300]}")

    data = resp.json()
    try:
        reply_text = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        reply_text = (
            "Xin lỗi, mình chưa trả lời được câu này. "
            "Vui lòng liên hệ trực tiếp Telegram @Clickbuy_ru."
        )

    history.append({"role": "assistant", "content": reply_text})
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
        reply = ask_groq(session_id, req.message.strip())
    except Exception as e:
        raise HTTPException(500, f"Lỗi khi gọi Groq API: {e}")

    return ChatResponse(reply=reply, session_id=session_id)


# --- Gắn Telegram webhook vào cùng app FastAPI ---
from telegram_bot import router as telegram_router  # noqa: E402

app.include_router(telegram_router)
