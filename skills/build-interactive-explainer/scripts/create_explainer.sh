#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "用法: $0 <输出目录>" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
target_dir="$1"

if [[ -e "$target_dir" ]] && [[ -n "$(find "$target_dir" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
  echo "目标目录不是空目录，已停止：$target_dir" >&2
  exit 1
fi

mkdir -p "$target_dir"

# 复制可运行源码与评审模板，避免生成结果依赖 Skill 安装目录。
cp -R "$skill_dir/assets/vue-template/." "$target_dir/"
cp "$skill_dir/assets/research-notes-template.md" "$target_dir/research-notes.md"
cp "$skill_dir/assets/novice-review-template.md" "$target_dir/novice-review.md"

echo "已创建交互解释项目：$target_dir"
