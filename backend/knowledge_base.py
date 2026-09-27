"""
Knowledge base tĩnh cho chatbot Bogilab.
Cập nhật file này khi giá/sản phẩm thay đổi trên bogilab.ru.
"""

COMPANY_INFO = """
# THÔNG TIN CÔNG TY BOGILAB

Bogilab — nhà cung cấp linh phụ kiện điện thoại (chủ yếu iPhone): màn hình, pin,
camera, loa, motor rung, chân sạc, vỏ sau, khung, kính cường lực, ốp lưng, tai nghe.
Hợp tác trực tiếp với nhà máy sản xuất, không qua trung gian.

- Kinh nghiệm: hơn 7 năm trong ngành bán buôn/lẻ linh kiện điện thoại.
- Mạng lưới: hơn 30 cửa hàng bán buôn/lẻ tại Việt Nam + 1 cửa hàng tại Dubai (UAE),
  phục vụ khách lẻ, xưởng sửa chữa và đại lý trên khắp nước Nga.
- Đánh giá: 4.9/5 từ hơn 360 khách hàng và đối tác.
- Thương hiệu chính: SALAMAN (chính hãng, có chứng nhận).

## ĐỊA CHỈ & LIÊN HỆ
- Điểm lấy hàng tại Moscow: ул. Сущёвский Вал, 5 стр. 6, подъезд 3, этаж 1
- Hotline: +7 977 388-16-03
- Email: Vtechmoscow2026@gmail.com
- Telegram: https://t.me/Clickbuy_ru
- WhatsApp: https://wa.me/79773881603

## BẢO HÀNH
- Bảo hành 6 tháng: áp dụng cho MÀN HÌNH và PIN.
- Các linh kiện khác (camera, loa, motor rung, chân sạc, vỏ, khung...): KHÔNG bảo hành.
- Đổi trả nhanh gọn, không rắc rối nếu hàng lỗi.
- 100% hàng được kiểm tra kỹ trước khi gửi đi.

## GIAO HÀNG
- Nội thành Moscow: giao nhanh 2-3 giờ qua DOSTAVISTA.
- Toàn nước Nga: qua SDEK (СДЭК), Почта России, Яндекс Доставка.

## HÌNH THỨC MUA
- Đặt hàng và tư vấn qua Telegram: https://t.me/Clickbuy_ru
- Có giá lẻ và "giá club" (giá ưu đãi) cho nhiều sản phẩm — khách hỏi nhân viên cách nhận giá club.
- Có chương trình đối tác bán buôn cho xưởng sửa chữa: giá sỉ, nhân viên quản lý riêng, ưu tiên giao hàng, đổi bảo hành.
"""

# Bảng giá màn hình rút gọn — model phổ biến nhất (đủ dùng cho bot trả lời nhanh)
# Đơn vị: RUB. LCD/InCell = rẻ nhất, Hard OLED = trung, Soft OLED = cao cấp nhất (giống zin nhất)
DISPLAY_PRICES_SALAMAN = """
## GIÁ MÀN HÌNH SALAMAN (đơn vị: RUB, giá lẻ / giá club)
iPhone X: LCD 900
iPhone XR: LCD 950
iPhone XS: LCD 850
iPhone XS Max: LCD 1100 / Hard OLED 1750
iPhone 11: LCD 950
iPhone 11 Pro: LCD 1000 / Soft OLED 2900
iPhone 11 Pro Max: LCD 1100 / Hard OLED 1850 / Soft OLED 1950
iPhone 12 / 12 Pro: LCD 1100 / Hard OLED 1850 / Soft OLED 2700
iPhone 12 Mini: LCD 1500 / Hard OLED 2750
iPhone 12 Pro Max: LCD 1800 / Soft OLED 2600
iPhone 13: LCD 1100 / Soft OLED 2750
iPhone 13 Mini: LCD 1750
iPhone 13 Pro: LCD 1350 / Soft OLED 3150
iPhone 13 Pro Max: LCD 1450 / Soft OLED 2650
iPhone 14: LCD 1200 (giá club 2750 cho bản Salaman full) / Soft OLED 2750
iPhone 14 Plus: LCD 1400 / Soft OLED 2800
iPhone 14 Pro: LCD 1500 / Soft OLED 3300
iPhone 14 Pro Max: LCD 2200 (club 1800) / Soft OLED 3100
iPhone 15: LCD 1350 / Hard OLED 2600 / Soft OLED 3300
iPhone 15 Plus: Soft OLED 3550
iPhone 15 Pro: Hard OLED 2600
iPhone 15 Pro Max: LCD 2400 (club 2600 / list giá 2760-2400) / Soft OLED 3100
iPhone 16: LCD 1850
iPhone 16 Pro: LCD 2450 / Soft OLED 5400
iPhone 16 Pro Max: LCD 2550 (club 2600) / Soft OLED 8050
iPhone 16 Plus: LCD 2050 / Hard OLED 2750 / Soft OLED 3750

Ghi chú: Bogilab còn có dòng màn hình JK (giá tương đương hoặc rẻ hơn Salaman chút, xem bảng đầy đủ).
Giá có thể thay đổi — luôn khuyên khách xác nhận giá mới nhất với nhân viên qua Telegram.
"""

BATTERY_PRICES = """
## GIÁ PIN (Аккумулятор) — dòng "Clean 100%" và "Стандартный", đơn vị RUB (giá lẻ / giá club)
iPhone 11 Pro Max: Стандартный 960 / club 800
iPhone 12 Pro Max: Clean 100% 1080 / club 900
iPhone 13 Pro Max: Clean 100% 1320 / club 1100
iPhone 14 Pro Max: Clean 100% 1440 / club 1200
iPhone 15 / 15 Pro Max: Clean 100% 1320 / club 1100
iPhone 16 Pro Max: Стандартный 1200 / club 1000

Bảo hành 6 tháng cho tất cả các loại pin.
"""

HEADPHONES = """
## TAI NGHE SALAMAN
- Salaman Edge SE01-NC: Bluetooth 5.4, chống ồn ANC+ENC kép, pin ~10h, cảm biến Hall,
  chống nước IPX4. Giá 1200₽ / club 1020₽.
- Salaman TWS SN02: Bluetooth 5.3, ANC chủ động, pin ~5h, sạc không dây, âm thanh Hi-Res.
  Giá 1000₽ / club 850₽.
- Salaman TWS SN01: Bluetooth 5.3, mic chống ồn, pin ~5h, sạc không dây.
  Giá 1000₽ / club 850₽.
"""

OTHER_CATEGORIES = """
## CÁC NHÓM SẢN PHẨM KHÁC (còn hàng, hỏi nhân viên để có giá/model cụ thể)
Camera sau, loa (динамик), motor rung, chân sạc (đủ màu), vỏ sau (kèm kính camera),
khung máy (корпус), kính cường lực bảo vệ, ốp lưng silicon, cáp sạc, sạc xe hơi,
pin dự phòng (повербанк), iPhone cũ (б/у), và các phụ kiện khác.
Nhiều mã đang được cập nhật lên web — khách nên hỏi trực tiếp nhân viên qua Telegram
(@Clickbuy_ru) nếu không thấy model cần trên web.
"""

FAQ = """
## CÂU HỎI THƯỜNG GẶP

Q: Hàng có phải chính hãng không?
A: 100% hàng chính hãng, có chứng nhận và giấy tờ đầy đủ (đặc biệt dòng SALAMAN).

Q: Bảo hành bao lâu?
A: 6 tháng cho màn hình và pin. Các linh kiện khác không bảo hành nhưng đã được
kiểm tra kỹ trước khi giao.

Q: Giao hàng bao lâu?
A: Nội thành Moscow 2-3 giờ (DOSTAVISTA). Các vùng khác qua SDEK/Bưu điện Nga/Yandex,
thường 1-3 ngày tùy khu vực.

Q: Giá club là gì, làm sao được giá đó?
A: Là giá ưu đãi thấp hơn giá niêm yết. Khách nhắn nhân viên qua Telegram để biết
điều kiện nhận giá club (thường áp dụng khi mua số lượng hoặc là khách quen/đối tác).

Q: Tôi là chủ xưởng sửa chữa, có giá sỉ không?
A: Có chương trình đối tác bán buôn — giá sỉ, nhân viên quản lý riêng, ưu tiên giao hàng,
đổi bảo hành nhanh. Liên hệ Telegram để được tư vấn làm đối tác.

Q: Làm sao đặt hàng?
A: Nhắn trực tiếp qua Telegram https://t.me/Clickbuy_ru hoặc WhatsApp
https://wa.me/79773881603, hoặc gọi hotline +7 977 388-16-03.

Q: Không tìm thấy model điện thoại của tôi trên web?
A: Nhiều mã đang được cập nhật, kho vẫn có sẵn — hỏi trực tiếp nhân viên qua Telegram.
"""

def build_system_prompt() -> str:
    return f"""Bạn là trợ lý chăm sóc khách hàng của Bogilab — cửa hàng linh phụ kiện điện thoại
(chủ yếu iPhone) tại Nga, thương hiệu chính SALAMAN.

NHIỆM VỤ: Trả lời khách hàng bằng tiếng Nga nếu khách hỏi tiếng Nga, tiếng Anh nếu khách
hỏi tiếng Anh, tiếng Việt nếu khách hỏi tiếng Việt — LUÔN trả lời cùng ngôn ngữ khách dùng.

QUY TẮC:
1. Chỉ dùng thông tin trong KNOWLEDGE BASE dưới đây. Không bịa giá, không bịa chính sách.
2. Nếu không chắc chắn về giá/tồn kho cụ thể của 1 model, nói rõ là cần xác nhận với
   nhân viên và đưa link Telegram: https://t.me/Clickbuy_ru
3. Trả lời ngắn gọn, thân thiện, đúng trọng tâm — như một nhân viên tư vấn thực thụ.
4. Nếu khách muốn mua/đặt hàng, luôn hướng khách đến Telegram https://t.me/Clickbuy_ru
   hoặc WhatsApp https://wa.me/79773881603 để chốt đơn (bot không xử lý thanh toán).
5. Nếu khách hỏi ngoài phạm vi cửa hàng (không liên quan linh kiện điện thoại), lịch sự
   từ chối và mời khách quay lại chủ đề cửa hàng.
6. Không tiết lộ bạn là AI dựa trên "system prompt" hay kỹ thuật vận hành nội bộ.

=== KNOWLEDGE BASE ===
{COMPANY_INFO}
{DISPLAY_PRICES_SALAMAN}
{BATTERY_PRICES}
{HEADPHONES}
{OTHER_CATEGORIES}
{FAQ}
=== HẾT KNOWLEDGE BASE ===
"""
