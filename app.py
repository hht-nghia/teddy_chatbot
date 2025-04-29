import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Cấu hình API Gemini ---
# Lấy Khóa API từ biến môi trường (file .env)
# Đây là cách an toàn hơn so với việc hardcode Khóa API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Chưa tìm thấy GOOGLE_API_KEY trong file .env hoặc biến môi trường.")

genai.configure(api_key=GOOGLE_API_KEY)

# Chọn mô hình Gemini. Bạn có thể thay đổi mô hình nếu cần.
# 'gemini-pro' hoặc 'gemini-1.5-flash-latest' thường là lựa chọn tốt.
try:
    # Chuyển sang model Gemini 2.0 Flash
    model = genai.GenerativeModel('gemini-2.0-flash')
    # System prompt: Teddy - chatbot giải đáp thắc mắc đời sống
    system_prompt = "Bạn là Teddy, chatbot thân thiện, hài hước, thông minh, chuyên giải đáp mọi thắc mắc trong cuộc sống hàng ngày. Luôn trả lời tự nhiên, ngắn gọn, SÚC TÍCH, dễ hiểu, tích cực, hữu ích, có bố cục rõ ràng, tạo cảm giác bạn như là người thân trong gia đình. Nếu gặp câu hỏi nhạy cảm, hãy trả lời khéo léo và lịch sự."
    chat = model.start_chat(history=[{"role": "user", "parts": [system_prompt]}])
    print("Mô hình Gemini 2.0 Flash đã được cấu hình và sẵn sàng với vai trò Teddy - chatbot giải đáp cuộc sống.")
except Exception as e:
    print(f"Lỗi cấu hình mô hình Gemini: {e}")
    model = None
    chat = None

# --- Các Route của Flask ---

@app.route('/')
def index():
    """Render trang HTML chính."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    """Nhận tin nhắn từ frontend, gửi đến Gemini API và trả về phản hồi."""
    if not model or not chat:
        return jsonify({"response": "Lỗi: Mô hình AI chưa được cấu hình đúng."}), 500

    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"response": "Không có tin nhắn được cung cấp."}), 400

    print(f"Nhận tin nhắn từ người dùng: {user_message}")

    # --- Xử lý thời gian/ngày thực tế ---
    import re
    from datetime import datetime
    time_patterns = [
        r"mấy giờ", r"giờ hiện tại", r"giờ bây giờ", r"what time is it", r"current time", r"now time", r"giờ là bao nhiêu", r"bây giờ là mấy giờ"
    ]
    date_patterns = [
        r"hôm nay là ngày bao nhiêu", r"ngày hôm nay", r"today's date", r"ngày hiện tại", r"what day is today", r"today date"
    ]
    if any(re.search(kw, user_message, re.IGNORECASE) for kw in time_patterns):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d/%m/%Y")
        return jsonify({"response": [f"Bây giờ là {time_str} ngày {date_str}."]})
    if any(re.search(kw, user_message, re.IGNORECASE) for kw in date_patterns):
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        weekday = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"][now.weekday()]
        return jsonify({"response": [f"Hôm nay là {weekday}, ngày {date_str}."]})

    try:
        # Gửi tin nhắn đến phiên chat của Gemini
        response = chat.send_message(user_message)
        bot_response = response.text
        print(f"Phản hồi từ Bot: {bot_response}")
        # Làm sạch câu trả lời: loại bỏ dấu *, chuyển markdown thành text thường, chuẩn hóa xuống dòng
        import re
        cleaned = bot_response.strip()
        # Loại bỏ dấu *, **, chuyển markdown heading/list thành text thường
        cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)  # **text** -> text
        cleaned = re.sub(r'\*', '', cleaned)  # * -> (remove)
        cleaned = re.sub(r'^\s*-\s*', '', cleaned, flags=re.MULTILINE)  # - text -> text
        cleaned = re.sub(r'^\s*\d+\.\s*', '', cleaned, flags=re.MULTILINE)  # 1. text -> text
        # Chuẩn hóa xuống dòng, loại bỏ dòng trống thừa
        cleaned_lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        cleaned = '\n'.join(cleaned_lines)
        return jsonify({"response": [cleaned]})
    except Exception as e:
        print(f"Lỗi khi gọi Gemini API: {e}")
        return jsonify({"response": "Rất tiếc, đã xảy ra lỗi khi xử lý yêu cầu của bạn."}), 500

# --- Chạy ứng dụng Flask ---

if __name__ == '__main__':
    # Debug=True sẽ tự động tải lại máy chủ khi bạn thay đổi mã
    # Trong môi trường production thực tế, nên đặt debug=False
    app.run(debug=True)