#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "用法: $0 <项目目录> [端口]" >&2
  exit 2
fi

project_dir="$1"
port="${2:-4173}"

if [[ ! -f "$project_dir/explainer.html" ]]; then
  echo "未找到 explainer.html，请先运行构建脚本：$project_dir" >&2
  exit 1
fi

# 本地服务器只用于浏览器验收，最终交付仍是无需服务器的单文件 HTML。
echo "验收地址：http://127.0.0.1:$port/explainer.html"
python3 -m http.server "$port" --bind 127.0.0.1 --directory "$project_dir"
