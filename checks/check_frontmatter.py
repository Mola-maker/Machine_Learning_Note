#!/usr/bin/env python3
"""Frontmatter 完整性：每篇笔记须有 YAML frontmatter 且含 title/tags/created/updated/status。
跳过根目录治理文件与模板。用法: python3 check_frontmatter.py [根目录]"""
import os, sys
root = sys.argv[1] if len(sys.argv) > 1 else "."
SKIP = {"AGENTS.md","INDEX.md","GLOSSARY.md","EXPERIENCE.md","FAILED_IDEAS.md","CHANGELOG.md","README.md"}
REQ = ["title","tags","created","updated","status"]
bad = []
for dp, dn, fn in os.walk(root):
    if any(s in dp for s in (".git","templates","eval","runs","skills","wiki","site","node_modules",".opencode")): continue
    for f in fn:
        if not f.endswith(".md") or f in SKIP or f in ("CLAUDE.md", "AGENTS.md"): continue
        p = os.path.join(dp, f); txt = open(p, encoding="utf-8", errors="ignore").read()
        rel = os.path.relpath(p, root)
        if not txt.startswith("---"):
            bad.append(f"{rel}: 无 frontmatter"); continue
        head = txt[3:txt.find("\n---", 3)] if "\n---" in txt[3:] else ""
        miss = [k for k in REQ if f"{k}:" not in head]
        if miss: bad.append(f"{rel}: 缺字段 {','.join(miss)}")
print(f"frontmatter 问题 {len(bad)} 篇")
for b in bad: print(" ", b)
sys.exit(1 if bad else 0)
