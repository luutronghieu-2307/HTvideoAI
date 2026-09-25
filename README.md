<div align="center">

# HTvideoAI 🎬 (Enhanced Edition)

### An All-in-One AI Short & Long Video Generator
**Developed & Enhanced by: Lưu Trọng Hiếu**

Simply provide a video **Topic** or **Keyword**, and HTvideoAI will automatically research web sources, generate AI scripts, match copyright-free footage, synthesize speech narration, create subtitles, and produce high-definition (HD) short & long videos.

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://python.org)

</div>

---

## 🌟 Developer & Upgrade Notice

This project has been extensively enhanced and modernized by **Lưu Trọng Hiếu** under the project name **HTvideoAI** (upgraded from MoneyPrinterTurbo). This enhanced version introduces breakthrough features for long-form video creation, automated web research fact-grounding, and customizable voice style prompting.

---

## 🚀 Key Upgrades & New Features (by Lưu Trọng Hiếu)

- 🔍 **Research Pipeline (SearXNG Integration)**: Automatically searches web sources and retrieves evidence excerpts (Evidence Map) to help AI write grounded, fact-checked scripts.
- 🎙️ **Custom Voice Style Prompting**: Tailor voice style (`voice_style`), tone (`tone`), and target audience (`audience`) to give speech narration distinct personality and emotion.
- 🎬 **Long Video Pipeline**: Support script generation up to **50 paragraphs** and flexible target video duration control from **3 to 15 minutes**.
- 📝 **Script Critique Service**: Automatically evaluates, scores, and provides revision suggestions for AI-generated scripts before video rendering.
- 🔊 **Standalone Edge TTS Module**: Prioritizes high-quality Vietnamese neural voices (`vi-VN-HoaiMyNeural`, `vi-VN-NamMinhNeural`) with an enforced 300-second (5 minutes) timeout safety for long narration synthesis.
- 🎛️ **Enhanced WebUI Controls**: Integrated research toggles, paragraph sliders, and voice style controls directly into the main WebUI panel.

---

## 🎯 Full Feature Overview

- [x] Multiple workflow options: **WebUI**, **API**, **CLI**, and **AI Agent**
- [x] AI automatic script generation or custom script input
- [x] Supports various HD video formats:
  - 📱 Portrait 9:16 (`1080x1920`) - TikTok, Shorts, Reels
  - 💻 Landscape 16:9 (`1920x1080`) - YouTube, Facebook
- [x] Supports **Batch Video Generation**
- [x] Configurable transition duration and clip speed
- [x] Multilingual speech synthesis: **Edge TTS**, **Azure Speech**, **Google Gemini TTS**, **SiliconFlow**, **Xiaomi MiMo**, **ElevenLabs**, **Chatterbox**
- [x] Professional subtitle customization (font, color, position, stroke, background)
- [x] Background music (BGM) integration from built-in library or custom upload
- [x] Copyright-free stock video retrieval from **Pexels**, **Pixabay**, **Coverr**, or **Local Video Folders**
- [x] Seamless connection with leading AI providers: **Google Gemini**, **Groq**, **OpenAI**, **DeepSeek**, **Kimi/Moonshot**, **Qwen**, **MiniMax**, **Ollama**, **LiteLLM**, etc.

---

## 💻 Installation & Quick Start

### Prerequisites
- **Python 3.11+** (Python 3.10+ supported)
- Supported OS: **Windows**, **macOS**, or **Linux**

### 1. Clone Repository:
```shell
git clone https://github.com/tronghieu/HTvideoAI.git
cd HTvideoAI
```

---

### 🚀 1-Click Auto Setup & Launcher (Recommended)

The project includes a smart, cross-platform Python script `start.py` that handles everything automatically:
- ✅ Verifies Python version compatibility.
- ✅ Automatically creates a virtual environment (`.venv`) if not present.
- ✅ Automatically installs missing dependencies from `requirements.txt`.
- ✅ Automatically creates `config.toml` from `config.example.toml` if absent.
- ✅ Automatically finds an available network port (8501-8599).
- ✅ Automatically launches the WebUI and **opens your default web browser**.
- ✅ Eliminates traditional `.bat` / `.sh` script execution errors across different OS.

#### 📌 Quickest Launch (Cross-platform):
```shell
python start.py
```
*(On Linux/macOS, use `python3 start.py`)*

#### Or run via platform launchers:
- **Windows**: Double-click `webui.bat`
- **Linux / macOS**: Run `sh webui.sh`

---

### ⚙️ Command Line Options with `start.py`:

| Command | Description |
| :--- | :--- |
| `python start.py` | Auto-verify, auto-setup all dependencies, start WebUI & open browser |
| `python start.py --reinstall` | Force reinstallation of all dependencies in `requirements.txt` |
| `python start.py --port 8505` | Specify custom port for the WebUI |
| `python start.py --no-browser` | Launch WebUI server without auto-opening the browser |
| `python start.py --api` | Launch FastAPI Backend Server (`main.py`) instead of WebUI |
| `python start.py --check-only` | Verify environment, setup `.venv` and exit without launching |

---

### 🛠️ Manual Installation (Optional):

If you prefer to manage the virtual environment manually:
```shell
# 1. Create and activate virtualenv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install requirements
pip install -r requirements.txt

# 3. Launch WebUI
streamlit run webui/Main.py
```

After starting, navigate to **http://127.0.0.1:8501** in your browser.

---

## 📚 Documentation

- 📄 [Research Pipeline (SearXNG) Setup Guide](docs/research.md)
- 🎙️ [Custom Voice Style & Long Video Guide](docs/custom_voice_prompt.md)

---

## 📜 License

This open-source project is licensed under the MIT License.
