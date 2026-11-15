#!/usr/bin/env python3
"""BE&CP 저장소 환경 점검.

무엇이 준비됐고 무엇이 빠졌는지 표로 보여 준다. 아무것도 설치하거나 바꾸지 않는다.
실행: python tools/check_setup.py   (Windows는 py tools/check_setup.py 도 가능)
빠진 항목의 "해결" 열에 있는 명령을 실행하거나, Claude에게 "BE&CP 세팅해줘"라고 하면 된다.
"""
from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
WIN = os.name == "nt"
LAW_URL = "https://mcp.gomdori.app/law"
PIP_PKGS = "matplotlib numpy Pillow ezdxf shapely pvlib python-hwpx PyMuPDF"

rows: list[tuple[str, str, str, str, str]] = []  # 구분, 항목, 상태, 내용, 해결


def add(group, item, ok, detail="", fix="", required=True):
    status = "OK" if ok else ("없음" if required else "선택")
    rows.append((group, item, status, detail, "" if ok else fix))


def run(args, timeout=60):
    exe = shutil.which(args[0])
    if not exe:
        return None
    try:
        p = subprocess.run([exe, *args[1:]], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout, cwd=ROOT)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:  # timeout, permission
        return -1, str(e)


# ── 기본 ─────────────────────────────────────────────
v = sys.version_info
need = (3, 11) if WIN else (3, 10)
add("기본", "Python", v >= need, f"{v.major}.{v.minor}.{v.micro}",
    "winget install Python.Python.3.12" if WIN else "Python 3.10 이상 설치")

mods = {"ezdxf": "ezdxf", "shapely": "shapely", "pvlib": "pvlib", "python-hwpx": "hwpx",
        "PyMuPDF": "pymupdf", "matplotlib": "matplotlib", "numpy": "numpy", "Pillow": "PIL"}
missing = [k for k, m in mods.items() if importlib.util.find_spec(m) is None
           and not (m == "pymupdf" and importlib.util.find_spec("fitz"))]
add("기본", "Python 라이브러리", not missing, "모두 있음" if not missing else "없음: " + ", ".join(missing),
    f"python -m pip install {PIP_PKGS}")

r = run(["node", "--version"])
node_ok = bool(r and r[0] == 0 and int(r[1].strip().lstrip("v").split(".")[0]) >= 18)
add("기본", "Node.js 18+", node_ok, r[1].strip() if r else "설치 안 됨",
    "winget install OpenJS.NodeJS.LTS" if WIN else "Node.js 18 이상 설치")

r = run(["git", "--version"])
add("기본", "Git", bool(r and r[0] == 0), r[1].strip() if r else "설치 안 됨",
    "winget install Git.Git" if WIN else "git 설치")

dwg_mod = (ROOT / "tools/dwg/node_modules/@node-projects/acad-ts").exists() and \
          (ROOT / "tools/dwg/node_modules/@mlightcad/libredwg-web").exists()
r = run(["node", str(ROOT / "tools/dwg/dwgconv.mjs")]) if dwg_mod else None
add("기본", "DWG 변환기(tools/dwg)", bool(r and r[0] == 0), "작동" if r and r[0] == 0 else "패키지 미설치",
    "npm ci --ignore-scripts --prefix tools/dwg")

add("기본", "ffmpeg(도면 영상 스킬용)", shutil.which("ffmpeg") is not None,
    "있음" if shutil.which("ffmpeg") else "없음",
    "winget install Gyan.FFmpeg" if WIN else "ffmpeg 설치", required=False)

# ── Claude Code ─────────────────────────────────────
r = run(["claude", "--version"])
add("Claude", "Claude Code", bool(r and r[0] == 0), r[1].strip().splitlines()[0] if r and r[1] else "설치 안 됨",
    "irm https://claude.ai/install.ps1 | iex" if WIN else "curl -fsSL https://claude.ai/install.sh | bash")

mcp_out = ""
if r and r[0] == 0:
    m = run(["claude", "mcp", "list"], timeout=120)
    mcp_out = m[1] if m else ""


def mcp_line(name):
    for line in mcp_out.splitlines():
        if line.strip().startswith(name + ":"):
            return line.strip()
    return ""


for name, desc in (("kordoc", "HWP·PDF 문서"), ("korean-law", "법령 조회")):
    line = mcp_line(name)
    ok = bool(line) and ("Connected" in line or "✓" in line)
    if name == "kordoc" and WIN and "cmd" not in line:
        add("Claude", f"MCP {name} ({desc})", False, "Windows 보정 없음",
            "claude mcp add --scope local kordoc -- cmd /c npx -y -p kordoc@4.24.80 kordoc-mcp")
    elif "Pending approval" in line:
        # A separate `claude` process cannot see approvals given in a running session,
        # so this is a reminder, not a failure.
        rows.append(("Claude", f"MCP {name} ({desc})", "확인",
                     "승인 필요할 수 있음: Claude Code 대화창에서 /mcp 로 연결 상태 확인·승인", ""))
    else:
        add("Claude", f"MCP {name} ({desc})", ok,
            line[len(name) + 1:].strip()[:70] if line else "목록에 없음", "SETUP.md 3-3절")

# ── 네트워크 ─────────────────────────────────────────
try:
    req = urllib.request.Request(LAW_URL, method="POST", data=json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "check", "version": "0"}},
    }).encode(), headers={"content-type": "application/json", "accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        law_ok, law_detail = resp.status == 200, f"HTTP {resp.status}"
except Exception as e:
    law_ok, law_detail = False, str(e)[:60]
add("네트워크", "법령 서버(mcp.gomdori.app)", law_ok, law_detail,
    "회사 방화벽 확인" if WIN else "클라우드 환경 설정에서 허용 도메인에 mcp.gomdori.app 추가(SETUP.md 4절)")

# ── AutoCAD (Windows PC 전용) ────────────────────────
if WIN:
    add("AutoCAD", "autocad-mcp-pro", shutil.which("autocad-mcp") is not None,
        "설치됨" if shutil.which("autocad-mcp") else "설치 안 됨", 'python -m pip install "autocad-mcp-pro[com]"')
    add("AutoCAD", "pywin32(AutoCAD 연결)", importlib.util.find_spec("win32com") is not None, "",
        'python -m pip install "autocad-mcp-pro[com]"')
    line = mcp_line("autocad")
    g = run(["claude", "mcp", "get", "autocad"], timeout=60) if line else None
    has_paths = bool(g and "ALLOWED_PATHS" in g[1])
    add("AutoCAD", "MCP autocad 등록", bool(line), line[8:].strip()[:70] if line else "등록 안 됨", "SETUP.md 3-4절")
    if line:
        add("AutoCAD", "ALLOWED_PATHS(접근 폴더 제한)", has_paths, "설정됨" if has_paths else "설정 안 됨",
            "SETUP.md 3-4절: 도면 폴더 하나로 지정")
else:
    rows.append(("AutoCAD", "AutoCAD 연결", "해당 없음",
                 f"{platform.system()}: AutoCAD 직접 조작은 Windows PC에서만", ""))

# ── 출력 ─────────────────────────────────────────────
print(f"BE&CP 환경 점검  ({platform.system()} {platform.release()}, 저장소: {ROOT})\n")
w = [max(len(str(r[i])) for r in rows) for i in range(4)]
for g, item, st, detail, fix in rows:
    mark = {"OK": "[OK]  ", "없음": "[없음]", "선택": "[선택]", "확인": "[확인]", "해당 없음": "[ - ] "}[st]
    print(f"{mark} {g:<{w[0]}}  {item:<{w[1]}}  {detail}")
    if fix:
        print(f"        해결: {fix}")
req_missing = [r for r in rows if r[2] == "없음"]
print(f"\n필수 항목 중 빠진 것: {len(req_missing)}개" + ("" if req_missing else "  → 준비 완료"))
sys.exit(1 if req_missing else 0)
