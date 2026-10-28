#!/bin/sh
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if [ ! -x "venv/bin/python" ]; then
    python3 -m venv venv || exit 1
fi

. venv/bin/activate
python -m pip install -r requirements.txt || exit 1
python gen_sample_image.py || exit 1
python app.py
