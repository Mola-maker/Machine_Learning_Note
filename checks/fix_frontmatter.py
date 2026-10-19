#!/usr/bin/env python3
"""确定性补 frontmatter：只处理内容笔记（论文精读/学习笔记/日志），不碰基础设施文件。
title 取首个一级标题（无则用文件名）；tags 按目录推断；created/updated 取 git 首次/末次提交日期；
status 一律 draft（待人工或后续流程提升）。已含 frontmatter 的跳过。用法: python3 checks/fix_frontmatter.py [根目录] [--dry]"""
import os, re, subprocess, sys
root = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
dry = "--dry" in sys.argv
SKIP_DIRS = {".git","templates","skills","checks","eval","runs","site","wiki",".opencode",".github",".obsidian"}
SKIP_FILES = {"AGENTS.md","INDEX.md","GLOSSARY.md","EXPERIENCE.md","FAILED_IDEAS.md","CHANGELOG.md","README.md","CLAUDE.md"}
TAGMAP = [("01-foundations","地基"),("02-training-toolkit","训练工具箱"),("03-vision-cnns","视觉CNN"),
          ("04-sequence-models","序列模型"),("05-transformers","Transformer"),("Git","工具"),
          ("Markdown","工具"),("html_stack_learning","工具"),("Python","Python")]
def git_date(path, fmt):
    r = subprocess.run(["git","-C",root,"log","--follow","--format=%ad","--date=short",fmt,"--",path],
                       capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    return lines[0] if lines else "2026-10-19"
fixed = 0
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in sorted(fn):
        if not f.endswith(".md") or f in SKIP_FILES: continue
        p = os.path.join(dp, f); rel = os.path.relpath(p, root)
        txt = open(p, encoding="utf-8").read()
        if txt.startswith("---"): continue
        m = re.search(r"^#\s+(.+)$", txt, flags=re.M)
        title = (m.group(1).strip() if m else f[:-3]).replace('"','\\"')
        tags = [v for k, v in TAGMAP if k in rel] or (["日志"] if re.match(r"20\d\d-\d\d-\d\d", f) else ["笔记"])
        fm = (f'---\ntitle: "{title}"\ntags: [{", ".join(tags)}]\ncreated: {git_date(rel,"--reverse")}\n'
              f'updated: {git_date(rel,"")}\nstatus: draft\n---\n\n')
        print(("DRY " if dry else "FIX ") + rel)
        if not dry: open(p, "w", encoding="utf-8").write(fm + txt)
        fixed += 1
print(f"共处理 {fixed} 篇")
