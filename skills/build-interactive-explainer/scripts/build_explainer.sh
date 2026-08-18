#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "用法: $0 <项目目录>" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$1"

if [[ ! -f "$project_dir/package.json" ]]; then
  echo "未找到 package.json：$project_dir" >&2
  exit 1
fi

if command -v pnpm >/dev/null 2>&1; then
  pnpm_bin="$(command -v pnpm)"
else
  echo "未找到 pnpm，请先安装 pnpm。" >&2
  exit 1
fi

cd "$project_dir"

# 只有依赖目录缺失时才安装，重复构建保持快速且不触发网络请求。
if [[ ! -d node_modules ]]; then
  "$pnpm_bin" install --frozen-lockfile
fi

"$pnpm_bin" run build
cp dist/index.html explainer.html

node "$script_dir/validate_html.mjs" "$project_dir/explainer.html"
echo "已生成自包含文件：$project_dir/explainer.html"
