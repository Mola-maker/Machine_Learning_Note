#!/usr/bin/env python3
"""密钥/隐私扫描：常见 token 前缀、私钥块、密码赋值。用法: python3 check_secrets.py [根目录]"""
import os, re, sys
root = sys.argv[1] if len(sys.argv) > 1 else "."
PATS = [r"sk-[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}",
        r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", r"(?i)(api[_-]?key|password|passwd)\s*[:=]\s*\S{8,}"]
hits = []
for dp, dn, fn in os.walk(root):
    if any(s in dp for s in (".git","node_modules","dist",".opencode")): continue
    for f in fn:
        p = os.path.join(dp, f)
        try: lines = open(p, encoding="utf-8", errors="ignore").read().splitlines()
        except Exception: continue
        for i, line in enumerate(lines, 1):
            for pat in PATS:
                if re.search(pat, line):
                    hits.append(f"{os.path.relpath(p, root)}:{i}: 命中 {pat[:24]}…")
                    break
print(f"疑似密钥/隐私 {len(hits)} 处")
for h in hits: print(" ", h)
sys.exit(1 if hits else 0)
