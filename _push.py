#!/usr/bin/env python3
"""通过 GitHub Contents API 推送 douyin-videos 仓库文件（token 从本地文件读取，不出现在命令行）。"""
import base64
import json
import os
import urllib.request
import urllib.error

TOKEN_FILE = r"C:/Users/66361/.workbuddy/.gh_token"
REPO_DIR = r"C:/Users/66361/WorkBuddy/douyin-videos"
OWNER, REPO = "superboy0303", "douyin-videos"
API = "https://api.github.com"

tok = open(TOKEN_FILE).read().strip()
H = {"Authorization": "Bearer " + tok, "User-Agent": "git",
     "Accept": "application/vnd.github+json", "Content-Type": "application/json"}


def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API + path, data=data, method=method, headers=H)
    try:
        resp = urllib.request.urlopen(r, timeout=120)
        raw = resp.read()
        return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


files = []
for root, _, names in os.walk(REPO_DIR):
    if ".git" in root:
        continue
    for n in names:
        full = os.path.join(root, n)
        rel = os.path.relpath(full, REPO_DIR).replace("\\", "/")
        files.append(rel)

print("files:", files)
for rel in files:
    full = os.path.join(REPO_DIR, rel)
    with open(full, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    status, d = req("PUT", f"/repos/{OWNER}/{REPO}/contents/{rel}",
                    {"message": f"add {rel}", "content": content, "branch": "main"})
    print(rel, "->", status, (d.get("commit", {}).get("sha", "")[:7] if isinstance(d, dict) else d))

# 开启 GitHub Pages
status, d = req("POST", f"/repos/{OWNER}/{REPO}/pages", {"source": {"branch": "main", "path": "/"}})
print("pages enable ->", status, json.dumps(d, ensure_ascii=False)[:300] if isinstance(d, dict) else d)
