#!/usr/bin/env bash
set -euo pipefail

SERVER="${1:-ubuntu@www.geneflow.online}"
REMOTE_DIR="/home/ubuntu/web_app"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> 上传至 $SERVER:$REMOTE_DIR ..."

rsync -avz --delete \
    --exclude '.git/' \
    --exclude '.env' \
    --exclude '.superpowers/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.DS_Store' \
    --exclude '*.db' \
    --exclude '收件箱/' \
    "$LOCAL_DIR/" "$SERVER:$REMOTE_DIR/"

echo "==> 安装/更新 Python 依赖 ..."
ssh "$SERVER" "cd $REMOTE_DIR && pip install -r requirements.txt --quiet"

echo "==> 重启 geneflow 服务 ..."
ssh "$SERVER" "sudo systemctl restart geneflow"

echo "==> 完成！检查状态："
ssh "$SERVER" "sudo systemctl status geneflow --no-pager | head -5"
