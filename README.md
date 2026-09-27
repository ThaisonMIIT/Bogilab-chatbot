# Chatbot Bogilab — Telegram + Web

Một backend duy nhất (FastAPI + Google Gemini API, miễn phí), phục vụ cả Telegram bot và widget chat nhúng vào web.

## Cấu trúc
```
backend/
  main.py            # API /chat cho web widget + gắn Telegram webhook
  telegram_bot.py     # xử lý webhook Telegram
  knowledge_base.py   # toàn bộ dữ liệu sản phẩm/giá/chính sách Bogilab (sửa ở đây khi giá đổi)
  requirements.txt
  .env.example
widget/
  bogilab-chat-widget.js   # nhúng vào web tự code
```

## Bước 1 — Lấy API key Gemini (miễn phí)
1. Vào https://aistudio.google.com/apikey (đăng nhập bằng tài khoản Google).
2. Bấm **Create API key** → chọn hoặc tạo 1 Google Cloud project → copy key dạng `AIzaSy...`.
3. Copy vào biến `GEMINI_API_KEY`.

Free tier hiện tại của `gemini-2.0-flash` đủ dùng cho quy mô 1 cửa hàng (giới hạn theo phút/ngày,
không tốn phí — nếu sau này lượng khách tăng nhiều, chỉ cần đổi sang gói trả phí của Google mà
không phải sửa code).

## Bước 2 — Tạo Telegram bot (2 phút)
1. Mở Telegram, tìm **@BotFather**.
2. Gửi `/newbot`, đặt tên và username cho bot (vd `BogilabSupportBot`).
3. BotFather trả về **token** dạng `123456:AAxxxxx...` → copy vào `TELEGRAM_BOT_TOKEN`.
4. Tự chọn một chuỗi bí mật bất kỳ cho `TELEGRAM_WEBHOOK_SECRET` (để bảo vệ webhook).

## Bước 3 — Chạy thử local
```bash
cd backend
cp .env.example .env   # rồi điền các giá trị thật vào .env
pip install -r requirements.txt --break-system-packages
export $(cat .env | xargs)
uvicorn main:app --reload --port 8000
```
Test web: `curl -X POST localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"giá màn hình iphone 13 pro max bao nhiêu"}'`

## Bước 4 — Deploy backend (miễn phí/giá rẻ)
Khuyên dùng **Railway** hoặc **Render** (không cần quản lý server):

### Railway (khuyên dùng, nhanh nhất)
1. Push thư mục `backend/` lên 1 GitHub repo.
2. Vào https://railway.app → New Project → Deploy from GitHub repo.
3. Vào tab Variables, thêm các biến trong `.env.example` với giá trị thật.
4. Railway tự build & cho bạn 1 domain dạng `https://xxx.up.railway.app`.

### Render
1. New → Web Service → connect GitHub repo (thư mục backend).
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Thêm Environment Variables giống `.env.example`.

## Bước 5 — Kích hoạt Telegram webhook
Sau khi có domain backend (vd `https://bogilab-bot.up.railway.app`), chạy:
```bash
curl -F "url=https://bogilab-bot.up.railway.app/telegram/webhook/<TELEGRAM_WEBHOOK_SECRET>" \
     https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook
```
Kiểm tra: nhắn tin cho bot trên Telegram, bot sẽ trả lời tự động.

## Bước 6 — Nhúng widget vào web
1. Mở `widget/bogilab-chat-widget.js`, sửa dòng:
   ```js
   const API_URL = "https://bogilab-bot.up.railway.app/chat";
   ```
2. Copy file này vào project web của bạn, hoặc host trên CDN/S3.
3. Dán trước thẻ `</body>` của trang:
   ```html
   <script src="bogilab-chat-widget.js"></script>
   ```
4. Nút chat bong bóng sẽ xuất hiện góc dưới phải mọi trang có nhúng script này.

## Cập nhật dữ liệu (giá, chính sách...)
Sửa trực tiếp trong `backend/knowledge_base.py` rồi deploy lại — không cần sửa code logic.
Khuyên định kỳ (vd hàng tuần) đối chiếu lại với bogilab.ru để cập nhật giá mới.

## Giới hạn hiện tại (có thể nâng cấp sau)
- Lịch sử hội thoại lưu trong RAM — nếu backend restart, lịch sử mất (không ảnh hưởng dữ liệu sản phẩm).
- Bot không tự chốt đơn/thanh toán — luôn dẫn khách sang Telegram @Clickbuy_ru hoặc WhatsApp để hoàn tất.
- Giá lấy từ 1 lần crawl web (26/09/2026) — cần cập nhật định kỳ thủ công.
