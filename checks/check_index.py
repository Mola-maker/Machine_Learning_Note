#!/usr/bin/env python3
"""索引覆盖率：内容笔记是否被根 INDEX.md 或任一 `00 本章索引.md` 以 [[双链]] 收录。
两遍扫描：先收集全部索引文本，再核对内容笔记。跳过基础设施目录与配置文件。
用法: python3 check_index.py [根目录]"""
import os, re, sys
root = sys.argv[1] if len(sys.argv) > 1 else "."
SKIP_DIRS = {".git", "templates", "skills", "checks", "eval", "runs", "site", "wiki",
             ".opencode", ".github", ".obsidian", "node_modules"}
SKIP_FILES = {"AGENTS.md", "INDEX.md", "GLOSSARY.md", "EXPERIENCE.md", "FAILED_IDEAS.md",
              "CHANGELOG.md", "CLAUDE.md", "README.md"}
def read(p):
    return open(p, encoding="utf-8", errors="ignore").read() if os.path.exists(p) else ""
linked = set()
notes = []
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if not f.endswith(".md"): continue
        rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
        if f == "00 本章索引.md" or rel == "INDEX.md":
            linked |= set(re.findall(r"\[\[([^\]|#]+)", read(os.path.join(dp, f))))
        elif f not in SKIP_FILES:
            notes.append(rel)
missing = [r for r in notes
           if r[:-3] not in linked and os.path.basename(r)[:-3] not in linked]
print(f"内容笔记 {len(notes)} 篇，未入索引 {len(missing)} 篇")
for m in missing: print(" ", m)
sys.exit(1 if missing else 0)
