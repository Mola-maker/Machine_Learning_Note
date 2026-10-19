#!/usr/bin/env python3
"""笔记价值特征抽取（确定性）：输出 JSON 到 stdout。
用法: python3 checks/value_features.py [根目录] > features.json"""
import os, re, sys, json, collections
root = sys.argv[1] if len(sys.argv) > 1 else "."
SKIP_DIRS = {".git", "templates", "skills", "checks", "eval", "runs", "site", "wiki", ".opencode"}
GOV = {"AGENTS.md","INDEX.md","GLOSSARY.md","EXPERIENCE.md","FAILED_IDEAS.md","CHANGELOG.md"}
files = []
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if f.endswith(".md") and f not in GOV:
            files.append(os.path.join(dp, f))
inbound = collections.Counter()
texts = {}
for p in files:
    txt = open(p, encoding="utf-8", errors="ignore").read()
    texts[p] = txt
    for t in re.findall(r"\[\[([^\]|#]+)", txt):
        inbound[t.strip()] += 1
out = []
for p in files:
    txt = texts[p]
    body = re.sub(r"^---.*?---", "", txt, flags=re.S)
    out.append({
        "path": os.path.relpath(p, root),
        "title": os.path.basename(p)[:-3],
        "chars": len(body),
        "formulas": txt.count("$"),
        "examples": len(re.findall(r"例题|例\s*\d|Example", txt)),
        "images": len(re.findall(r"!\[|!\[\[|\.png|\.jpg|\.excalidraw|\.canvas", txt)),
        "sections": len(re.findall(r"^#{2,3}\s", txt, flags=re.M)),
        "outlinks": len(re.findall(r"\[\[", txt)),
        "inlinks": inbound.get(os.path.basename(p)[:-3], 0),
        "has_frontmatter": txt.startswith("---"),
    })
print(json.dumps(out, ensure_ascii=False, indent=1))
