#!/usr/bin/env python3
"""BE&CP 저장소 환경 점검(Codex·Claude Code 공용).

무엇이 준비됐고 무엇이 빠졌는지 표로 보여 준다. 아무것도 설치하거나 바꾸지 않는다.
실행: python tools/check_setup.py   (Windows는 py tools/check_setup.py 도 가능)
빠진 항목의 "해결" 열에 있는 명령을 실행하거나, Codex에 "$setup-be-cp"(Claude Code는 "/setup-be-cp")라고 하면 된다.
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

try:
    import tomllib
except ImportError:  # Python < 3.11
    tomllib = None

ROOT = Path(__file__).resolve().parent.parent
WIN = os.name == "nt"
LAW_URL = "https://mcp.gomdori.app/law"
PIP_PKGS = "matplotlib numpy Pillow ezdxf shapely pvlib python-hwpx PyMuPDF"
ECO2_PKG = "ECO2[dataframe,edit] @ git+https://github.com/beskep/eco2@97049bfa8e629c5e1c6ba117eecf05ce33b44f4c"
CODEX_HOME = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")

rows: list[tuple[str, str, str, str, str]] = []  # 구분, 항목, 상태, 내용, 해결


def add(group, item, ok, detail="", fix="", required=True):
    status = "OK" if ok else ("없음" if required else "선택")
    rows.append((group, item, status, detail, "" if ok else fix))


def note(group, item, detail, fix=""):
    rows.append((group, item, "확인", detail, fix))


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


def load_toml(path: Path):
    if tomllib is None or not path.is_file():
        return None
    try:
        return tomllib.loads(path.read_text("utf-8"))
    except Exception:
        return None


def same_path(a: str, b: Path) -> bool:
    def norm(p):
        p = str(p).replace("\\\\?\\", "").replace("\\", "/").rstrip("/")
        return p.lower() if WIN else p
    try:
        return norm(Path(a).resolve()) == norm(b.resolve())
    except Exception:
        return norm(a) == norm(b)


# ── 기본 ─────────────────────────────────────────────
v = sys.version_info
need = (3, 12)  # eco2 패키지(beskep/ECO2)가 3.12 이상 필요
add("기본", "Python", v >= need, f"{v.major}.{v.minor}.{v.micro}",
    "winget install Python.Python.3.12" if WIN else "Python 3.10 이상 설치")

mods = {"ezdxf": "ezdxf", "shapely": "shapely", "pvlib": "pvlib", "python-hwpx": "hwpx",
        "PyMuPDF": "pymupdf", "matplotlib": "matplotlib", "numpy": "numpy", "Pillow": "PIL"}
missing = [k for k, m in mods.items() if importlib.util.find_spec(m) is None
           and not (m == "pymupdf" and importlib.util.find_spec("fitz"))]
add("기본", "Python 라이브러리", not missing, "모두 있음" if not missing else "없음: " + ", ".join(missing),
    f"python -m pip install {PIP_PKGS}")

eco2_ok = importlib.util.find_spec("eco2") is not None and importlib.util.find_spec("polars") is not None
add("기본", "ECO2 파일 도구(eco2)", eco2_ok, "설치됨" if eco2_ok else "없음(.ECL2 읽기는 없어도 됨)",
    f'python -m pip install "{ECO2_PKG}"', required=False)

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

try:
    s = subprocess.run([sys.executable, str(ROOT / "tools/sync_codex.py"), "--check"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    add("기본", "Codex용 생성물 동기화", s.returncode == 0,
        "원본과 일치" if s.returncode == 0 else "원본(.claude/)과 다름", "python tools/sync_codex.py")
except Exception as e:
    add("기본", "Codex용 생성물 동기화", False, str(e)[:60], "python tools/sync_codex.py")

r = run(["git", "ls-remote", "--exit-code", "origin", "HEAD"], timeout=30)
add("기본", "저장소 업데이트 접근(git pull)", bool(r and r[0] == 0),
    "접근 가능" if r and r[0] == 0 else "접근 안 됨(접근키 미등록이거나 인터넷 문제)",
    "SETUP.md 3-2: 읽기 전용 접근키", required=False)

# ── AI 도구 ──────────────────────────────────────────
r_codex = run(["codex", "--version"])
r_claude = run(["claude", "--version"])
has_codex_cli = bool(r_codex and r_codex[0] == 0)
has_claude = bool(r_claude and r_claude[0] == 0)
has_codex = has_codex_cli or CODEX_HOME.is_dir()

if not (has_codex or has_claude):
    add("AI 도구", "Codex 또는 Claude Code", False, "찾지 못함",
        "SETUP.md 3-1(ChatGPT 앱 또는 npm install -g @openai/codex)")
if has_codex:
    version = next((line.strip() for line in r_codex[1].splitlines() if line.lower().startswith("codex")),
                   "버전 확인 불가") if has_codex_cli else ""
    add("AI 도구", "Codex", True,
        version if has_codex_cli else f"설정 폴더 있음({CODEX_HOME}), CLI 없음(앱만 쓰면 정상)")
if has_claude:
    add("AI 도구", "Claude Code", True, r_claude[1].strip().splitlines()[0])

# Codex: 프로젝트 MCP 설정, 폴더 신뢰
project_cfg = load_toml(ROOT / ".codex/config.toml")
user_cfg = load_toml(CODEX_HOME / "config.toml") or {}
if has_codex:
    servers = (project_cfg or {}).get("mcp_servers", {})
    ok = {"kordoc", "korean-law"} <= set(servers)
    add("AI 도구", "Codex 프로젝트 MCP(.codex/config.toml)", ok,
        "kordoc, korean-law" if ok else "파일 없음 또는 항목 누락", "저장소를 다시 받는다(git pull)")
    projects = user_cfg.get("projects", {}) if isinstance(user_cfg, dict) else {}
    trusted = any(same_path(k, ROOT) and str(v.get("trust_level", "")).lower() == "trusted"
                  for k, v in projects.items() if isinstance(v, dict))
    if trusted:
        add("AI 도구", "Codex 폴더 신뢰", True, "신뢰됨")
    else:
        note("AI 도구", "Codex 폴더 신뢰", "사용자 설정에서 신뢰 기록을 찾지 못함",
             "Codex에서 이 폴더를 열 때 '신뢰(Trust)'를 선택(SETUP.md 3-2). 신뢰해야 MCP가 켜짐")

# Claude Code: MCP 상태
claude_out = ""
if has_claude:
    m = run(["claude", "mcp", "list"], timeout=120)
    claude_out = m[1] if m else ""


def claude_line(name):
    for line in claude_out.splitlines():
        if line.strip().startswith(name + ":"):
            return line.strip()
    return ""


if has_claude:
    for name in ("kordoc", "korean-law"):
        line = claude_line(name)
        if name == "kordoc" and WIN and "cmd" not in line:
            add("AI 도구", "Claude MCP kordoc", False, "Windows 보정 없음",
                "claude mcp add --scope local kordoc -- cmd /c npx -y -p kordoc@4.24.80 kordoc-mcp")
        elif "Pending approval" in line:
            # A separate `claude` process cannot see approvals given in a running session.
            note("AI 도구", f"Claude MCP {name}", "승인 필요할 수 있음", "Claude Code 대화창에서 /mcp")
        else:
            add("AI 도구", f"Claude MCP {name}", "Connected" in line or "✓" in line,
                line[len(name) + 1:].strip()[:60] if line else "목록에 없음", "SETUP.md 부록 B")

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
    "회사 방화벽 확인" if WIN else "클라우드 환경 허용 도메인에 mcp.gomdori.app 추가(SETUP.md 부록 C)")

# ── AutoCAD (Windows PC 전용) ────────────────────────
if WIN:
    add("AutoCAD", "autocad-mcp-pro", shutil.which("autocad-mcp") is not None,
        "설치됨" if shutil.which("autocad-mcp") else "PATH에서 못 찾음(전체 경로로 등록했으면 무시)",
        'python -m pip install "autocad-mcp-pro[com]"')
    add("AutoCAD", "pywin32(AutoCAD 연결)", importlib.util.find_spec("win32com") is not None, "",
        'python -m pip install "autocad-mcp-pro[com]"')
    codex_ac = (user_cfg.get("mcp_servers", {}) or {}).get("autocad") if isinstance(user_cfg, dict) else None
    claude_ac = claude_line("autocad")
    where = [n for n, hit in (("Codex", codex_ac), ("Claude", claude_ac)) if hit]
    add("AutoCAD", "MCP autocad 등록", bool(where), ", ".join(where) if where else "등록 안 됨",
        "SETUP.md 3-4(Codex) 또는 부록 B(Claude)")
    if codex_ac:
        paths = ((codex_ac.get("env") or {}).get("ALLOWED_PATHS") or "").strip()
        add("AutoCAD", "Codex ALLOWED_PATHS", bool(paths), paths or "설정 안 됨", "SETUP.md 3-4: 도면 폴더 하나로 지정")
    if claude_ac:
        g = run(["claude", "mcp", "get", "autocad"], timeout=60)
        add("AutoCAD", "Claude ALLOWED_PATHS", bool(g and "ALLOWED_PATHS" in g[1]), "",
            "SETUP.md 부록 B: 도면 폴더 하나로 지정")
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
