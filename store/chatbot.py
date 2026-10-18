"""
Chatbot AI tư vấn bán hàng cho Shop Hồng Loan.
Tích hợp Google Generative AI (Gemini) kèm cơ chế Fallback thông minh.
"""
import os
import re
import logging
from django.conf import settings
from .models import Product, ShopSetting

logger = logging.getLogger(__name__)

STANDARD_SIZE_GUIDE = """
BẢNG SIZE CHUẨN THỜI TRANG TRUNG NIÊN SHOP HỒNG LOAN:
- Size M: 45 - 50 kg (Chiều cao khoảng 150 - 158 cm)
- Size L: 50 - 55 kg (Chiều cao khoảng 155 - 162 cm)
- Size XL: 55 - 62 kg (Chiều cao khoảng 158 - 165 cm)
- Size 2XL: 62 - 70 kg (Chiều cao khoảng 160 - 168 cm)
- Size 3XL: 70 - 80 kg (Chiều cao khoảng 162 - 170 cm)
* Khuyên khách có vòng eo hoặc bắp tay lớn nên chọn tăng thêm 1 size để mặc thoải mái, dễ chịu.
"""


def get_product_catalog_context():
    """Lấy danh sách các sản phẩm đang bán để nạp vào ngữ cảnh AI."""
    products = Product.objects.filter(is_active=True).prefetch_related('sizes', 'category')
    lines = []
    for idx, p in enumerate(products, 1):
        cat_name = p.category.name if p.category else 'Thời trang'
        price_str = p.formatted_display_price
        fabric_str = p.get_fabric_display_name()
        sizes = [f"{s.size} ({s.weight_hint})" if s.weight_hint else s.size for s in p.sizes.filter(is_available=True)]
        sizes_str = ", ".join(sizes) if sizes else "M, L, XL, 2XL"
        lines.append(f"{idx}. {p.name} | Danh mục: {cat_name} | Giá: {price_str} | Vải: {fabric_str} | Size: {sizes_str} | Link: /san-pham/{p.slug}/")
    return "\n".join(lines)


def build_system_prompt(setting=None):
    if not setting:
        setting = ShopSetting.get_settings()

    catalog_text = get_product_catalog_context()

    prompt = f"""Bạn là Trợ lý tư vấn bán hàng AI của thương hiệu thời trang trung niên cao cấp "{setting.shop_name}".
Địa chỉ cửa hàng: {setting.address}
Số Hotline hỗ trợ: {setting.hotline}
Số Zalo tư vấn: {setting.zalo_phone}
Giờ mở cửa: {setting.open_hours}

{STANDARD_SIZE_GUIDE}

DANH SÁCH SẢN PHẨM HIỆN CÓ TẠI SHOP:
{catalog_text}

QUY TẮC BẮT BUỘC TRONG TƯ VẤN:
1. XƯNG HÔ VÀ THÁI ĐỘ:
   - Giọng điệu luôn lễ phép, ấm áp, nhã nhặn, chu đáo với khách hàng độ tuổi U40 - U70.
   - Luôn dùng từ "dạ", "em", "chúng em" để xưng hô.
   - Gọi khách hàng là "cô", "chú", "chị" hoặc "quý khách".
2. TƯ VẤN SẢN PHẨM & GIÁ TIỀN:
   - TUYỆT ĐỐI KHÔNG dùng từ "chính hãng". Hãy dùng: "cao cấp", "chất lượng loại 1", "thiết kế chuẩn phom dáng trung niên", "tỉ mỉ từng đường kim mũi chỉ".
   - Giá tiền BẮT BUỘC có dấu chấm phân cách hàng nghìn và kèm chữ 'đ' (ví dụ: 360.000 đ, 590.000 đ, 420.000 đ). Tuyệt đối không viết 360000 hay 360k.
   - Khi giới thiệu mẫu, có thể kèm theo link đường dẫn dạng: [Tên sản phẩm](/san-pham/slug/).
3. TƯ VẤN KÍCH CỠ (SIZE):
   - Khi khách hỏi chọn size theo cân nặng, chiều cao, hãy đối chiếu chính xác bảng size trên để tư vấn.
   - Giải thích form dáng trung niên thoải mái, khéo léo che khuyết điểm vòng 2 và bắp tay.
4. ĐẶT HÀNG & CHÍNH SÁCH:
   - Được mở hàng kiểm tra vải và đường may trước khi thanh toán.
   - Hỗ trợ đổi size miễn phí trong 7 ngày nếu không vừa.
   - Hướng dẫn khách để lại Số điện thoại + Địa chỉ ngay trong chat, hoặc nhấn nút Gọi Hotline ({setting.hotline}) / Chat Zalo ({setting.zalo_phone}) trên màn hình để được hỗ trợ nhanh nhất.
5. CÁCH TRÌNH BÀY:
   - Trình bày ngắn gọn, gạch đầu dòng rõ ràng, font chữ dễ đọc cho người lớn tuổi. Dùng các icon nhẹ nhàng (🌸, 👗, 🧵, ✨, 📞).
"""
    return prompt


def call_gemini_api(user_message, history=None):
    """Gọi Google Gemini API nếu có cấu hình GEMINI_API_KEY hợp lệ."""
    api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')
    if not api_key or 'YOUR_GEMINI_API_KEY' in api_key or len(api_key.strip()) < 10:
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key.strip())
        setting = ShopSetting.get_settings()
        system_instruction = build_system_prompt(setting)

        # Danh sách model thử nghiệm theo thứ tự ưu tiên
        candidate_models = ['gemini-1.5-flash', 'gemini-2.0-flash', 'gemini-1.5-pro']
        
        for model_name in candidate_models:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction
                )

                gemini_history = []
                if history and isinstance(history, list):
                    for h in history[-8:]:
                        role = 'user' if h.get('sender') == 'user' or h.get('role') == 'user' else 'model'
                        content = h.get('text') or h.get('content') or ''
                        if content:
                            gemini_history.append({'role': role, 'parts': [str(content)]})

                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(user_message)
                if response and response.text:
                    return response.text.strip()
            except Exception as model_err:
                logger.warning(f"Thử model {model_name} thất bại: {model_err}")
                continue

    except Exception as e:
        logger.error(f"Lỗi khi kết nối Google Generative AI: {e}")

    return None


def generate_fallback_response(user_message):
    """Cơ chế Fallback thông minh phản hồi chuẩn xác theo persona khi chưa có API Key hoặc mất kết nối."""
    setting = ShopSetting.get_settings()
    msg_lower = user_message.lower().strip()

    # 1. Câu hỏi về Cân nặng / Chọn Size
    # Tìm kiếm số cân nặng (ví dụ: 52kg, 52 kg, 65 ký, 70 cân, nặng 58...)
    weight_match = re.search(r'(\d{2,3})\s*(kg|kí|ký|cân)?', msg_lower)
    is_size_query = any(w in msg_lower for w in ['size', 'kích cỡ', 'cân nặng', 'nặng', 'chiều cao', 'vừa không', 'mặc số mấy', 'bảng size'])

    if weight_match and (is_size_query or 'kg' in msg_lower or 'kí' in msg_lower or 'cân' in msg_lower):
        try:
            w = int(weight_match.group(1))
            if w < 40 or w > 120:
                suggested_size = "XL"
            elif w <= 50:
                suggested_size = "M (45 - 50 kg)"
            elif w <= 55:
                suggested_size = "L (50 - 55 kg)"
            elif w <= 62:
                suggested_size = "XL (55 - 62 kg)"
            elif w <= 70:
                suggested_size = "2XL (62 - 70 kg)"
            elif w <= 80:
                suggested_size = "3XL (70 - 80 kg)"
            else:
                suggested_size = "3XL form rộng hoặc liên hệ shop tư vấn may đo"

            return (
                f"Dạ em chào cô/chú/chị ạ! 🌸\n\n"
                f"Với cân nặng khoảng **{w} kg**, cô/chú/chị mặc chuẩn nhất là **Size {suggested_size}** bên em nhé ạ.\n\n"
                f"• Phom dáng trung niên của {setting.shop_name} được may suông nhẹ, khéo léo che khuyết điểm vòng bụng và bắp tay.\n"
                f"• Chất liệu vải đũi tơ tằm mềm mại, co giãn nhẹ và thoáng mát, mặc cả ngày rất dễ chịu.\n\n"
                f"👉 Cô/chú/chị có thể cho em xin thêm chiều cao hoặc Số điện thoại để em gọi hỗ trợ chọn mẫu ưng ý nhất nhé ạ! 📞"
            )
        except Exception:
            pass

    if is_size_query:
        return (
            f"Dạ em gửi cô/chú/chị **Bảng chọn size chuẩn trung niên** của {setting.shop_name} ạ: 📏\n\n"
            f"• **Size M:** 45 - 50 kg (Cao 150 - 158 cm)\n"
            f"• **Size L:** 50 - 55 kg (Cao 155 - 162 cm)\n"
            f"• **Size XL:** 55 - 62 kg (Cao 158 - 165 cm)\n"
            f"• **Size 2XL:** 62 - 70 kg (Cao 160 - 168 cm)\n"
            f"• **Size 3XL:** 70 - 80 kg (Cao 162 - 170 cm)\n\n"
            f"*Nếu vòng bụng hoặc bắp tay hơi tròn, cô/chú/chị có thể tăng lên 1 size để mặc thoải mái nhất ạ. "
            f"Cô/chú/chị hiện nặng bao nhiêu kg để em tư vấn size chuẩn cho mình nhé ạ? 🌸"
        )

    # 2. Câu hỏi về Mẫu mới / Mẫu áo / Đầm váy / Giá cả
    if any(w in msg_lower for w in ['mẫu mới', 'mẫu áo', 'đầm', 'váy', 'áo kiểu', 'đồ bộ', 'bộ sưu tập', 'sản phẩm', 'giá', 'bao nhiêu']):
        products = Product.objects.filter(is_active=True).select_related('category')[:4]
        items_text = []
        for p in products:
            items_text.append(f"🌸 **[{p.name}](/san-pham/{p.slug}/)** — Giá: **{p.formatted_display_price}**\n  *Chất liệu: {p.get_fabric_display_name()} cao cấp, phom suông trang nhã.*")

        list_str = "\n\n".join(items_text)
        return (
            f"Dạ {setting.shop_name} xin giới thiệu đến cô/chú/chị các mẫu thời trang trung niên cao cấp mới về rất được yêu thích ạ:\n\n"
            f"{list_str}\n\n"
            f"👉 Tất cả các mẫu đều có sẵn size từ M đến 3XL. Cô/chú/chị ưng ý mẫu nào hãy nhắn cho em hoặc để lại Số điện thoại để bên em gửi thêm hình ảnh thực tế qua Zalo nhé ạ! 💖"
        )

    # 3. Câu hỏi về Đặt hàng / Giao hàng / Đổi trả / Vận chuyển
    if any(w in msg_lower for w in ['đặt hàng', 'mua hàng', 'giao hàng', 'ship', 'đổi trả', 'thanh toán', 'chốt đơn']):
        return (
            f"Dạ cách thức đặt hàng tại {setting.shop_name} vô cùng nhanh chóng và an tâm ạ: ✨\n\n"
            f"1. **Đặt trực tiếp qua chat:** Cô/chú/chị chỉ cần để lại **[Tên + Số điện thoại + Địa chỉ]** ngay tại đây, nhân viên bên em sẽ gọi lại hỗ trợ ngay.\n"
            f"2. **Gọi Hotline:** Bấm gọi số **{setting.hotline}** để được nhân viên tư vấn trực tiếp.\n"
            f"3. **Nhắn Zalo:** Nhắn tin tới Zalo **{setting.zalo_phone}** để nhận ảnh chi tiết mẫu vải.\n\n"
            f"🎁 **Chính sách an tâm mua sắm:**\n"
            f"• Giao hàng tận nơi trên toàn quốc.\n"
            f"• **Được mở bưu phẩm kiểm tra đúng mẫu, đúng chất vải rồi mới thanh toán tiền.**\n"
            f"• Miễn phí đổi size trong 7 ngày nếu mặc không vừa vặn ạ! 🌸"
        )

    # 4. Câu hỏi về Địa chỉ / Giờ mở cửa / Hotline / Liên hệ
    if any(w in msg_lower for w in ['địa chỉ', 'ở đâu', 'hotline', 'số điện thoại', 'zalo', 'giờ mở cửa', 'mở cửa']):
        return (
            f"Dạ {setting.shop_name} xin gửi thông tin liên hệ của cửa hàng đến cô/chú/chị ạ: 🏡\n\n"
            f"• 📍 **Địa chỉ:** {setting.address}\n"
            f"• 🕐 **Giờ mở cửa:** {setting.open_hours}\n"
            f"• 📞 **Hotline tư vấn:** {setting.hotline}\n"
            f"• 💬 **Zalo:** {setting.zalo_phone}\n\n"
            f"Cửa hàng rất hân hạnh được phục vụ cô/chú/chị bất cứ lúc nào ạ! 🌸"
        )

    # 5. Phản hồi chào hỏi mặc định
    return (
        f"Dạ {setting.shop_name} xin chào cô/chú/chị ạ! 🌸\n\n"
        f"Em là Trợ lý tư vấn bán hàng của shop. Em rất vui được hỗ trợ cô/chú/chị:\n"
        f"• 📏 **Tư vấn chọn size chuẩn** theo chiều cao & cân nặng\n"
        f"• 👗 **Gợi ý các mẫu đầm, áo kiểu, đồ bộ** trung niên cao cấp mới nhất\n"
        f"• 🛒 **Hỗ trợ đặt hàng nhanh & giải đáp chính sách giao hàng**\n\n"
        f"Dạ cô/chú/chị đang quan tâm đến kiểu trang phục nào hay cần em tư vấn cân nặng bao nhiêu kg ạ?"
    )


def ask_chatbot(user_message, history=None):
    """
    Hàm giao tiếp chính: Thử Gemini AI trước,
    nếu chưa có API key hoặc lỗi sẽ tự động chuyển sang Fallback.
    """
    if not user_message or not user_message.strip():
        return "Dạ em có thể giúp gì cho cô/chú/chị về trang phục và kích cỡ ạ? 🌸"

    ai_reply = call_gemini_api(user_message, history=history)
    if ai_reply:
        return ai_reply

    return generate_fallback_response(user_message)
