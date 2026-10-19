#!/usr/bin/env bash
# 全套检查：死链 / frontmatter / 索引覆盖 / 术语 / 密钥。仓库根目录执行：bash checks/run_all.sh
set -u; cd "$(dirname "$0")/.."
fail=0
for s in check_deadlinks check_frontmatter check_index check_glossary check_secrets; do
  echo "===== $s ====="
  python3 "checks/$s.py" . || fail=1
done
echo "===== 汇总：$( [ $fail -eq 0 ] && echo 全部通过 || echo 有检查未通过 ) ====="
exit $fail
