# Teddy Chatbot

Teddy Chatbot là một ứng dụng web chatbot sử dụng mô hình Gemini (Google Generative AI) với giao diện hiện đại, thân thiện. Teddy giúp bạn giải đáp mọi thắc mắc trong cuộc sống hàng ngày bằng phong cách tự nhiên, ngắn gọn, súc tích và gần gũi như người thân trong gia đình.

## Tính năng
- Chatbot AI trả lời các câu hỏi đời sống, mẹo vặt, gợi ý món ăn, v.v.
- Hỗ trợ nhận diện và trả lời thời gian/ngày thực tế.
- Giao diện đẹp, responsive, sử dụng được trên nhiều thiết bị cùng lúc.
- Header luôn hiển thị cố định trên cùng.
- Làm sạch câu trả lời, loại bỏ ký tự markdown thừa, bố cục rõ ràng.

## Công nghệ sử dụng
- Python 3, Flask
- Google Generative AI (Gemini)
- HTML, CSS, JavaScript (frontend)

## Hướng dẫn cài đặt & chạy local

1. **Clone dự án:**
   ```bash
   git clone https://github.com/hht-nghia/teddy_chatbot.git
   cd teddy_chatbot
   ```
2. **Tạo file .env** và thêm API Key:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   ```
3. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Chạy ứng dụng:**
   ```bash
   python app.py
   ```
5. **Truy cập trình duyệt:**
   - Mở [http://localhost:5000](http://localhost:5000)

## Deploy lên Render.com
- Đảm bảo đã có các file: `requirements.txt`, `Procfile`, `.env` (hoặc thêm biến môi trường trên Render).
- Kết nối repo GitHub, tạo Web Service mới trên Render, chọn branch và deploy.
- Xem hướng dẫn chi tiết trong phần Issues hoặc liên hệ tác giả.

## Đóng góp
Mọi đóng góp vui lòng tạo Pull Request hoặc Issue mới.

## Bản quyền
Teddy Chatbot © 2025 by hht-nghia. Sử dụng cho mục đích học tập, phi thương mại.
