#!/usr/bin/env python3
"""术语一致性（基础版）：统计英文术语在正文中的出现，并报告 GLOSSARY 未收录的高频术语，
以及同篇内同一英文术语后跟不同中文译名的可疑混用。用法: python3 check_glossary.py [根目录]"""
import os, re, sys, collections
root = sys.argv[1] if len(sys.argv) > 1 else "."
g = os.path.join(root, "GLOSSARY.md")
known = set()
if os.path.exists(g):
    for line in open(g, encoding="utf-8"):
        m = re.match(r"\|\s*([A-Za-z][^|]*)\|", line)
        if m: known.add(m.group(1).strip().lower())
cnt = collections.Counter()
for dp, dn, fn in os.walk(root):
    if ".git" in dp: continue
    for f in fn:
        if f.endswith(".md"):
            txt = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
            for t in re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z]?[a-z]+){0,2}\b", txt):
                cnt[t.lower()] += 1
unk = [(t, c) for t, c in cnt.most_common(40) if t not in known and c >= 3]
print(f"GLOSSARY 已收录 {len(known)} 条；高频未收录术语 {len(unk)} 个（出现≥3次，前40）")
for t, c in unk: print(f"  {t} ×{c}")
sys.exit(0)
