#!/usr/bin/env bash

# 将仓库中的一级 Skill 目录同步为 Codex 全局目录的软链接，供本地开发时即时加载。
# 仅处理包含 SKILL.md 的目录；遇到同名的实体文件或目录时保留原内容并失败退出，避免覆盖用户已安装的 Skill。
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_skills_dir="$project_root/skills"
codex_skills_dir="${CODEX_HOME:-"$HOME/.codex"}/skills"

mkdir -p "$codex_skills_dir"

linked_count=0
unchanged_count=0
conflict_count=0

for skill_dir in "$source_skills_dir"/*; do
  [ -d "$skill_dir" ] || continue
  [ -f "$skill_dir/SKILL.md" ] || continue

  skill_name="$(basename "$skill_dir")"
  link_path="$codex_skills_dir/$skill_name"

  if [ -L "$link_path" ]; then
    current_target="$(readlink "$link_path")"
    if [ "$current_target" = "$skill_dir" ]; then
      printf '保持：%s\n' "$skill_name"
      unchanged_count=$((unchanged_count + 1))
      continue
    fi

    ln -sfn "$skill_dir" "$link_path"
    printf '已更新：%s\n' "$skill_name"
    linked_count=$((linked_count + 1))
    continue
  fi

  if [ -e "$link_path" ]; then
    printf '冲突：%s 已存在且不是软链接，未修改：%s\n' "$skill_name" "$link_path" >&2
    conflict_count=$((conflict_count + 1))
    continue
  fi

  ln -s "$skill_dir" "$link_path"
  printf '已链接：%s\n' "$skill_name"
  linked_count=$((linked_count + 1))
done

printf '完成：新增或更新 %d 个，保持 %d 个。\n' "$linked_count" "$unchanged_count"

if [ "$conflict_count" -gt 0 ]; then
  printf '存在 %d 个同名冲突，请手动处理后重新执行。\n' "$conflict_count" >&2
  exit 1
fi
