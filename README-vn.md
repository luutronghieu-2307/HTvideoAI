<div align="center">

# HTvideoAI 🎬 (Phiên bản Nâng cấp)

### Công cụ Tạo Video AI Tự động All-in-One
**Được phát triển & Nâng cấp bởi: Lưu Trọng Hiếu**

Chỉ cần nhập **Chủ đề** hoặc **Từ khóa**, HTvideoAI sẽ tự động nghiên cứu tài liệu, viết kịch bản AI, khớp video bản quyền, tạo giọng đọc thuyết minh, chèn phụ đề & nhạc nền để xuất video chất lượng cao (HD).

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://python.org)

</div>

---

## 🌟 Thông tin Người Nâng cấp & Phát triển

Dự án này được **Lưu Trọng Hiếu** phát triển và nâng cấp chuyên sâu dưới tên gọi **HTvideoAI** (nền tảng nâng cấp từ MoneyPrinterTurbo). Phiên bản này bổ sung hàng loạt tính năng đột phá phục vụ sáng tạo nội dung video dài, nghiên cứu thông tin tự động trên web và tùy chỉnh giọng đọc phong phú.

---

## 🚀 Các Tính Năng Nâng Cấp Nổi Bật (bởi Lưu Trọng Hiếu)

- 🔍 **Research Pipeline (SearXNG Integration)**: Tự động tìm kiếm tài liệu trên Web, trích xuất dữ liệu thực tế (Evidence Map) giúp AI viết kịch bản có căn cứ khoa học và chính xác.
- 🎙️ **Custom Voice Style Prompting**: Tự do tùy chỉnh phong cách giọng đọc (`voice_style`), giọng điệu (`tone`), đối tượng khán giả (`audience`) giúp kịch bản và lời thoại thuyết minh mang cá tính riêng.
- 🎬 **Tạo Video Dài (Long Video Pipeline)**: Hỗ trợ kịch bản lên tới **50 đoạn văn** và tùy chỉnh thời lượng video linh hoạt từ **3 đến 15 phút**.
- 📝 **Dịch vụ Đánh giá Kịch bản (Script Critique Service)**: Tự động chấm điểm, phân tích và đưa ra gợi ý chỉnh sửa kịch bản AI trước khi dựng video.
- 🔊 **Mô-đun Edge TTS Độc Lập**: Đưa các giọng đọc Tiếng Việt chuẩn (`vi-VN-HoaiMyNeural`, `vi-VN-NamMinhNeural`) lên ưu tiên hàng đầu, thiết lập mức Timeout an toàn 300 giây (5 phút) cho video dài.
- 🎛️ **Giao diện WebUI Nâng Cấp**: Tích hợp các bộ điều khiển nghiên cứu tài liệu, tùy chỉnh số đoạn kịch bản và phong cách đọc trực tiếp trên trang chủ WebUI.

---

## 🎯 Tính Năng Tổng Thể

- [x] Đa dạng phương thức sử dụng: **WebUI**, **API**, **CLI** và **AI Agent**
- [x] Tự động viết kịch bản bằng AI hoặc nhập kịch bản thủ công
- [x] Hỗ trợ các định dạng video HD:
  - 📱 Video Dọc 9:16 (`1080x1920`) - TikTok, Shorts, Reels
  - 💻 Video Ngang 16:9 (`1920x1080`) - YouTube, Facebook
- [x] Hỗ trợ **Tạo video hàng loạt (Batch Generation)**
- [x] Tùy chỉnh thời lượng chuyển cảnh và tốc độ clip
- [x] Hỗ trợ giọng đọc đa ngôn ngữ: **Edge TTS**, **Azure Speech**, **Google Gemini TTS**, **SiliconFlow**, **Xiaomi MiMo**, **ElevenLabs**, **Chatterbox**
- [x] Tùy chỉnh phụ đề chuyên nghiệp (font chữ, màu sắc, vị trí, viền chữ, nền phụ đề)
- [x] Tùy chỉnh nhạc nền (BGM) từ thư viện hoặc file riêng
- [x] Tìm kiếm video stock bản quyền từ **Pexels**, **Pixabay**, **Coverr** hoặc dùng **Thư mục video Local**
- [x] Kết nối linh hoạt với nhiều nhà cung cấp AI: **Google Gemini**, **Groq**, **OpenAI**, **DeepSeek**, **Kimi/Moonshot**, **Qwen**, **MiniMax**, **Ollama**, **LiteLLM**, v.v.

---

## 💻 Hướng Dẫn Cài Đặt & Chạy Dự Án

### Yêu cầu hệ thống:
- Python 3.11+
- Hệ điều hành: Windows, macOS, hoặc Linux

### 1. Tải Mã Nguồn:
```shell
git clone https://github.com/tronghieu/HTvideoAI.git
cd HTvideoAI
```

### 2. Cài Đặt Môi Trường:
```shell
python -m venv .venv
source .venv/bin/activate  # Trên Windows dùng: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Khởi Động Giao Diện WebUI:

- **Trên Linux / macOS**:
  ```shell
  sh webui.sh
  ```

- **Trên Windows**:
  ```cmd
  webui.bat
  ```

Sau khi chạy, truy cập đường dẫn: **http://127.0.0.1:8501** trên trình duyệt.

---

## 📚 Tài Liệu Hướng Dẫn

- 📄 [Hướng dẫn Cấu hình Research Pipeline (SearXNG)](docs/research.md)
- 🎙️ [Hướng dẫn Tùy chỉnh Phong cách Giọng đọc & Video Dài](docs/custom_voice_prompt.md)

---

## 📜 Giấy Phép (License)

Dự án phát triển mã nguồn mở tuân thủ theo giấy phép MIT License.
