#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTvideoAI - Auto Environment Setup & Launcher Script
Tác giả / Nâng cấp: Lưu Trọng Hiếu

Tác dụng:
- Tự động kiểm tra phiên bản Python (khuyến nghị >= 3.10, tốt nhất 3.11+).
- Tự động tạo môi trường ảo (.venv) nếu chưa có.
- Tự động cài đặt & đồng bộ dependencies (requirements.txt).
- Tự động sao chép file cấu hình config.toml từ config.example.toml nếu thiếu.
- Tự động dò tìm cổng (port) trống khả dụng (8501-8599).
- Tự động khởi chạy WebUI (Streamlit) hoặc API (FastAPI) trong môi trường .venv.
- Tự động mở trình duyệt web khi ứng dụng đã sẵn sàng.
- Hỗ trợ mượt mà trên tất cả hệ điều hành: Windows, Linux, macOS.
"""

import argparse
import os
import platform
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Thư mục gốc dự án
PROJECT_ROOT = Path(__file__).resolve().parent

# ANSI Colors for Terminal Output
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    @classmethod
    def disable_on_windows(cls):
        # Kích hoạt ANSI trên Windows Console nếu cần
        if platform.system() == "Windows":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except Exception:
                pass


def log_info(msg: str):
    print(f"{Colors.CYAN}[HTvideoAI] ℹ️  {msg}{Colors.END}")


def log_success(msg: str):
    print(f"{Colors.GREEN}[HTvideoAI] ✅ {msg}{Colors.END}")


def log_warning(msg: str):
    print(f"{Colors.YELLOW}[HTvideoAI] ⚠️  {msg}{Colors.END}")


def log_error(msg: str):
    print(f"{Colors.RED}[HTvideoAI] ❌ {msg}{Colors.END}")


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
========================================================================
   🎬 HTvideoAI - Công cụ Tạo Video AI Tự Động Toàn Diện 🎬
   Phát triển & Nâng cấp bởi: Lưu Trọng Hiếu
   Hệ điều hành: {platform.system()} ({platform.machine()}) | Python: {platform.python_version()}
========================================================================
{Colors.END}"""
    print(banner)


def check_python_version():
    """Kiểm tra phiên bản Python."""
    major = sys.version_info.major
    minor = sys.version_info.minor
    if major < 3 or (major == 3 and minor < 10):
        log_error(f"Phiên bản Python hiện tại ({major}.{minor}) không được hỗ trợ!")
        log_error("Vui lòng cài đặt Python 3.10 trở lên (khuyến nghị Python 3.11 hoặc 3.12).")
        sys.exit(1)
    log_success(f"Kiểm tra Python: v{major}.{minor}.{sys.version_info.micro} (Đạt yêu cầu)")


def get_venv_paths():
    """Lấy đường dẫn python và pip trong .venv tùy theo hệ điều hành."""
    venv_dir = PROJECT_ROOT / ".venv"
    if platform.system() == "Windows":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
        venv_streamlit = venv_dir / "Scripts" / "streamlit.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"
        venv_streamlit = venv_dir / "bin" / "streamlit"

    return venv_dir, venv_python, venv_pip, venv_streamlit


def is_running_inside_target_venv(venv_python: Path) -> bool:
    """Kiểm tra xem script hiện tại có đang chạy bằng Python của .venv này không."""
    try:
        current_py = Path(sys.executable).resolve()
        target_py = venv_python.resolve()
        return current_py == target_py
    except Exception:
        return False


def ensure_config_file():
    """Tự động sao chép config.toml nếu chưa tồn tại."""
    config_file = PROJECT_ROOT / "config.toml"
    config_example = PROJECT_ROOT / "config.example.toml"

    if not config_file.exists():
        if config_example.exists():
            log_warning("Chưa tìm thấy file config.toml, đang tự động tạo từ config.example.toml...")
            shutil.copy(config_example, config_file)
            log_success("Đã tạo file config.toml mặc định thành công.")
        else:
            log_warning("Không tìm thấy cả config.toml và config.example.toml.")
    else:
        log_success("Kiểm tra file cấu hình: config.toml đã sẵn sàng.")


def create_virtual_environment(venv_dir: Path):
    """Tự động tạo môi trường ảo .venv."""
    log_info(f"Đang tạo môi trường ảo venv tại: {venv_dir}...")
    try:
        # Sử dụng module venv tích hợp sẵn
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        log_success("Tạo môi trường ảo (.venv) thành công!")
    except subprocess.CalledProcessError as e:
        log_error(f"Không thể tạo môi trường ảo: {e}")
        log_error("Hãy đảm bảo bạn đã cài đặt python3-venv (đối với Linux: sudo apt install python3-venv).")
        sys.exit(1)


def check_and_install_dependencies(venv_python: Path, venv_pip: Path, force_reinstall: bool = False):
    """Kiểm tra các thư viện bắt buộc và tự động cài đặt nếu thiếu."""
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.exists():
        log_warning("Không tìm thấy file requirements.txt, bỏ qua bước kiểm tra thư viện.")
        return

    # Danh sách các gói quan trọng cần có
    essential_packages = [
        "streamlit",
        "moviepy",
        "edge_tts",
        "fastapi",
        "uvicorn",
        "openai",
        "loguru",
        "google-genai",
        "requests",
    ]

    needs_install = force_reinstall

    if not needs_install:
        # Kiểm tra nhanh xem các gói cốt lõi đã được cài trong venv chưa
        check_script = (
            "import sys\n"
            "missing = []\n"
            "for pkg in ['streamlit', 'moviepy', 'edge_tts', 'fastapi', 'uvicorn', 'loguru', 'requests']:\n"
            "    try:\n"
            "        __import__(pkg)\n"
            "    except ImportError:\n"
            "        missing.append(pkg)\n"
            "if missing:\n"
            "    print(','.join(missing))\n"
            "    sys.exit(1)\n"
            "sys.exit(0)\n"
        )
        try:
            res = subprocess.run(
                [str(venv_python), "-c", check_script],
                capture_output=True,
                text=True,
                check=False
            )
            if res.returncode != 0:
                missing = res.stdout.strip()
                log_warning(f"Phát hiện còn thiếu thư viện trong .venv ({missing}). Sẽ tiến hành cài đặt...")
                needs_install = True
            else:
                log_success("Tất cả các thư viện bắt buộc đã được cài đặt đầy đủ.")
        except Exception:
            needs_install = True

    if needs_install:
        log_info("Đang nâng cấp pip và cài đặt dependencies từ requirements.txt...")
        try:
            # Nâng cấp pip trước
            subprocess.run(
                [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Cài đặt requirements
            log_info("Đang cài đặt các thư viện (quá trình này có thể mất 1-3 phút lần đầu)...")
            cmd = [str(venv_python), "-m", "pip", "install", "-r", str(req_file)]
            subprocess.run(cmd, check=True)
            log_success("Cài đặt toàn bộ thư viện dependencies thành công!")
        except subprocess.CalledProcessError as e:
            log_error(f"Lỗi khi cài đặt dependencies: {e}")
            log_error(f"Bạn có thể thử cài thủ công bằng: {venv_pip} install -r requirements.txt")
            sys.exit(1)


def find_available_port(host: str, preferred_port: int, max_scan: int = 100) -> int:
    """Dò tìm port khả dụng bắt đầu từ preferred_port."""
    candidates = [preferred_port] + [
        port for port in range(preferred_port + 1, preferred_port + max_scan)
    ]
    for port in candidates:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            try:
                # Thử bind vào host và port
                sock.bind((host, port))
                return port
            except OSError:
                continue
    return preferred_port


def wait_and_open_browser(url: str, check_host: str, check_port: int, timeout: int = 40):
    """Đợi server khởi động xong và tự động mở trình duyệt web."""
    start_time = time.time()
    server_ready = False

    while time.time() - start_time < timeout:
        time.sleep(0.5)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1.0)
                # Thử kết nối đến port của web server
                target_host = "127.0.0.1" if check_host in ["0.0.0.0", ""] else check_host
                res = sock.connect_ex((target_host, check_port))
                if res == 0:
                    server_ready = True
                    break
        except Exception:
            pass

    if server_ready:
        log_info(f"Ứng dụng đã sẵn sàng! Đang mở trình duyệt: {url}")
        time.sleep(0.5)
        webbrowser.open(url)
    else:
        log_warning(f"Chưa thể kết nối tự động đến server sau {timeout}s. Vui lòng mở thủ công: {url}")


def run_webui(venv_python: Path, venv_streamlit: Path, host: str, port: int, auto_browser: bool):
    """Khởi chạy Streamlit WebUI."""
    webui_script = PROJECT_ROOT / "webui" / "Main.py"
    if not webui_script.exists():
        log_error(f"Không tìm thấy file WebUI tại: {webui_script}")
        sys.exit(1)

    display_host = "127.0.0.1" if host in ["0.0.0.0", ""] else host
    app_url = f"http://{display_host}:{port}"

    log_success(f"Khởi động WebUI tại: {Colors.BOLD}{Colors.UNDERLINE}{app_url}{Colors.END}")

    # Khởi động thread mở trình duyệt
    if auto_browser:
        threading.Thread(
            target=wait_and_open_browser,
            args=(app_url, host, port),
            daemon=True
        ).start()

    # Thiết lập biến môi trường
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT) + (os.pathsep + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")
    env["MPT_WEBUI_HOST"] = str(host)
    env["MPT_WEBUI_PORT"] = str(port)

    # Lệnh chạy streamlit qua python của venv
    cmd = [
        str(venv_python),
        "-m",
        "streamlit",
        "run",
        str(webui_script),
        f"--server.address={host}",
        f"--server.port={port}",
        f"--browser.serverAddress={display_host}",
        "--browser.gatherUsageStats=False",
        "--client.toolbarMode=minimal",
        "--logger.hideWelcomeMessage=True",
        "--server.showEmailPrompt=False",
        "--server.enableCORS=True",
    ]

    try:
        subprocess.run(cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\n")
        log_info("Đã nhận lệnh dừng từ người dùng. Tạm biệt!")
    except subprocess.CalledProcessError as e:
        log_error(f"Tiến trình WebUI kết thúc với lỗi: {e}")


def run_api(venv_python: Path):
    """Khởi chạy FastAPI Backend Server."""
    main_script = PROJECT_ROOT / "main.py"
    if not main_script.exists():
        log_error(f"Không tìm thấy file main.py tại: {main_script}")
        sys.exit(1)

    log_success("Khởi động FastAPI Backend Server...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT) + (os.pathsep + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")

    cmd = [str(venv_python), str(main_script)]
    try:
        subprocess.run(cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\n")
        log_info("Đã nhận lệnh dừng từ người dùng. Tạm biệt!")
    except subprocess.CalledProcessError as e:
        log_error(f"Tiến trình API kết thúc với lỗi: {e}")


def main():
    Colors.disable_on_windows()
    print_banner()

    parser = argparse.ArgumentParser(description="HTvideoAI - Script Tự Động Kiểm Tra, Cài Đặt Môi Trường & Khởi Chạy")
    parser.add_argument("--host", type=str, default=os.environ.get("MPT_WEBUI_HOST", "127.0.0.1"), help="Địa chỉ Host để chạy WebUI (mặc định: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=int(os.environ.get("MPT_WEBUI_PORT", "8501")), help="Cổng Port chạy WebUI (mặc định: 8501)")
    parser.add_argument("--no-browser", action="store_true", help="Không tự động mở trình duyệt web sau khi khởi động")
    parser.add_argument("--api", action="store_true", help="Chạy API Backend FastAPI thay vì giao diện WebUI")
    parser.add_argument("--reinstall", action="store_true", help="Cài đặt lại toàn bộ dependencies trong requirements.txt")
    parser.add_argument("--check-only", action="store_true", help="Chỉ kiểm tra môi trường và cài đặt, không khởi chạy web")

    args = parser.parse_args()

    # 1. Kiểm tra Python
    check_python_version()

    # 2. Kiểm tra file cấu hình
    ensure_config_file()

    # 3. Kiểm tra Virtualenv
    venv_dir, venv_python, venv_pip, venv_streamlit = get_venv_paths()

    if not venv_dir.exists() or not venv_python.exists():
        log_warning("Chưa phát hiện môi trường ảo (.venv). Đang tự động tạo...")
        create_virtual_environment(venv_dir)

    # 4. Kiểm tra & Cài đặt Dependencies
    check_and_install_dependencies(venv_python, venv_pip, force_reinstall=args.reinstall)

    if args.check_only:
        log_success("Kiểm tra và thiết lập môi trường hoàn tất thành công!")
        sys.exit(0)

    # 5. Nếu đang chạy bằng Python ngoài venv, tự chuyển sang gọi bằng Python trong venv
    if not is_running_inside_target_venv(venv_python):
        log_info(f"Đang chuyển tiếp thực thi sang Python trong môi trường ảo: {venv_python}")
        # Chạy lại chính file này nhưng với venv_python
        cmd = [str(venv_python), str(__file__)] + sys.argv[1:]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT) + (os.pathsep + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")
        try:
            subprocess.run(cmd, env=env, check=True)
        except KeyboardInterrupt:
            pass
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)
        sys.exit(0)

    # 6. Khởi chạy WebUI hoặc API
    if args.api:
        run_api(venv_python)
    else:
        # Tìm port trống khả dụng
        selected_port = find_available_port(args.host, args.port)
        if selected_port != args.port:
            log_warning(f"Port {args.port} đang bận, tự động chuyển sang Port trống: {selected_port}")

        auto_open = not args.no_browser
        run_webui(venv_python, venv_streamlit, args.host, selected_port, auto_open)


if __name__ == "__main__":
    main()
