#!/bin/bash
set -e

echo "=== 1. Git Pull ==="
cd /home/ubuntu/naver_api/API_Test_NAVER
git fetch origin main
git reset --hard origin/main

echo "=== 2. Activate VENV ==="
source /home/ubuntu/naver_api/naverapi_pytest/bin/activate

echo "=== 3. Run Pytest ==="
pytest -v --disable-warnings

echo "=== 4. Copy Latest Report ==="
REPORT_DIR="/home/ubuntu/naver_api/API_Test_NAVER/Result"
LATEST=$(ls -t $REPORT_DIR/test_report_*.html | head -n 1)

cp "$LATEST" "linux_$(basename $LATEST)"

echo "Linux Run Complete"
