#!/usr/bin/env sh

# Chuyển về thư mục chứa script
CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$CURRENT_DIR" || exit 1

# Kiểm tra python3 hoặc python
if command -v python3 >/dev/null 2>&1; then
    exec python3 start.py "$@"
elif command -v python >/dev/null 2>&1; then
    exec python start.py "$@"
else
    echo "[HTvideoAI] ❌ Không tìm thấy Python! Vui lòng cài đặt Python 3.11+."
    exit 1
fi

