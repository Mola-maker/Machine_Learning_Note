#!/usr/bin/env python3
"""死链检查：按 Obsidian [[目标]] / [[目标|别名]] / [[目标#小节]] 规则解析。
目标按笔记名（去 .md）或相对路径匹配。用法: python3 check_deadlinks.py [根目录]"""
import os, re, subprocess, sys
root = sys.argv[1] if len(sys.argv) > 1 else "."
notes = {}
# 目标集合以 git 追踪清单为准（稀疏检出下磁盘不全）；无 git 时退回磁盘遍历
tracked = []
try:
    r = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True, text=True, timeout=20)
    if r.returncode == 0: tracked = [l for l in r.stdout.splitlines() if l.strip()]
except Exception:
    tracked = []
for rel in tracked:
    f = os.path.basename(rel)
    notes[f] = rel
    notes[os.path.splitext(f)[0]] = rel
    notes[rel] = rel
    notes[rel[:-3] if rel.endswith(".md") else rel] = rel
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in {".git", "node_modules", ".opencode"}]
    for f in fn:
        # Obsidian 链接目标可以是任意文件（笔记、图片、附件）：按全名、无扩展名、相对路径三种键登记
        rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
        stem = rel[:-3] if rel.endswith(".md") else rel
        notes[f] = rel
        notes[os.path.splitext(f)[0]] = rel
        notes[rel] = rel
        notes[stem] = rel
pat = re.compile(r"\[\[([^\]|#]+)")
bad = []
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in {".git", "node_modules", ".opencode"}]
    for f in fn:
        if not f.endswith(".md"): continue
        p = os.path.join(dp, f)
        for i, line in enumerate(open(p, encoding="utf-8", errors="ignore"), 1):
            for m in pat.finditer(line):
                t = m.group(1).strip()
                if t and t not in notes:
                    bad.append(f"{os.path.relpath(p, root)}:{i}: [[{t}]]")
print(f"死链 {len(bad)} 处")
for b in bad: print(" ", b)
sys.exit(1 if bad else 0)
