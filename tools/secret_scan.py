#!/usr/bin/env python3
"""저장소 유출 검사: 비밀유지 대상 이름, 비밀번호, 키, 토큰이 저장소 파일·기록에 들어가지 않았는지 본다.

  python tools/secret_scan.py              추적 중인 파일 + 아직 커밋 안 한 새 파일(무시 목록 제외)
  python tools/secret_scan.py --history    모든 커밋의 파일과 커밋 메시지까지
  python tools/secret_scan.py --files A B  지정한 파일만

검사 항목
  1. 비밀유지 대상 이름: tools/private_terms.sha256 에 SHA-256 해시로만 저장(원문 없음).
     문서의 낱말 1~3개 조합을 해시해 비교한다.
  2. 이 PC에만 둔 추가 목록: local/private-terms.txt (한 줄에 하나, 원문, GitHub 제외 폴더)
  3. 비밀번호·키·토큰 형태: 개인키 머리말, GitHub·OpenAI·AWS 토큰, JWT, "비밀번호: 값" 같은 대입

찾으면 파일·줄·종류만 출력하고 값은 출력하지 않는다. 하나라도 있으면 종료 코드 1.
해시 목록에 이름을 더할 때: python tools/secret_scan.py --hash "이름"  (비밀번호는 절대 넣지 않는다)
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
HASH_FILE = ROOT / "tools" / "private_terms.sha256"
LOCAL_TERMS = ROOT / "local" / "private-terms.txt"
SKIP_SUFFIX = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".mp4", ".dwg", ".ecl2", ".eco", ".ecox", ".tpl", ".tplx",
               ".xls", ".xlsx", ".zip", ".wasm", ".ico", ".woff", ".woff2")
TOKEN = re.compile(r"[0-9a-z가-힣]+")
PATTERNS = [
    ("개인키", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub 토큰", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}")),
    ("OpenAI·Anthropic 키", re.compile(r"\bsk-(ant-)?[A-Za-z0-9_-]{20,}")),
    ("AWS 키", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("JWT 토큰", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("비밀번호 대입", re.compile(r"(?i)(password|passwd|pwd|비밀번호|비번|암호)\s*[:=]\s*['\"]?[^\s'\"<>`|]{3,}")),
    ("아이디·비밀번호 쌍", re.compile(r"(?i)(아이디|id|user(name)?)\s*[:=]?\s*\S+\s*[,/]\s*(비밀번호|비번|password|pw)\s*[:=]?\s*\S+")),
]
# 문서에 쓰는 자리표시자는 비밀번호로 보지 않는다.
PLACEHOLDER = re.compile(r"(?i)[:=]\s*['\"]?(<[^>]*>|\$\{?[A-Z_]+\}?|\*+|x{3,}|\.\.\.|입력|본인키|발급받은키|none|null|false|true)")


def norm(text: str) -> str:
    return " ".join(TOKEN.findall(text.lower()))


def sha(text: str) -> str:
    return hashlib.sha256(norm(text).encode("utf-8")).hexdigest()


def load_hashes() -> set[str]:
    if not HASH_FILE.is_file():
        return set()
    return {line.strip() for line in HASH_FILE.read_text("utf-8").splitlines()
            if line.strip() and not line.startswith("#")}


def load_local_terms() -> list[str]:
    if not LOCAL_TERMS.is_file():
        return []
    return [t.strip().lower() for t in LOCAL_TERMS.read_text("utf-8").splitlines() if t.strip() and not t.startswith("#")]


def candidates(line: str) -> set[str]:
    toks = TOKEN.findall(line.lower())
    out = set()
    for n in (1, 2, 3):
        for i in range(len(toks) - n + 1):
            grp = toks[i:i + n]
            out.add(" ".join(grp))
            if n > 1:
                out.add("".join(grp))
    return out


def scan_text(text: str, where: str, hashes: set[str], terms: list[str]) -> list[str]:
    hits = []
    for no, line in enumerate(text.splitlines(), 1):
        if hashes and any(hashlib.sha256(c.encode("utf-8")).hexdigest() in hashes for c in candidates(line)):
            hits.append(f"{where}:{no}  비밀유지 대상 이름")
        low = line.lower()
        if any(t in low for t in terms):
            hits.append(f"{where}:{no}  이 PC 목록(local/private-terms.txt)의 이름")
        for label, pat in PATTERNS:
            m = pat.search(line)
            if m and not (label in ("비밀번호 대입", "아이디·비밀번호 쌍") and PLACEHOLDER.search(line[m.start():])):
                hits.append(f"{where}:{no}  {label}")
    return hits


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", check=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser(description="저장소 유출 검사")
    ap.add_argument("--history", action="store_true", help="모든 커밋과 커밋 메시지까지 검사")
    ap.add_argument("--files", nargs="+", type=Path, help="지정한 파일만 검사")
    ap.add_argument("--hash", metavar="이름", help="이름의 해시를 출력(목록에 더할 때). 비밀번호는 넣지 않는다")
    args = ap.parse_args()

    if args.hash:
        print(sha(args.hash))
        return 0

    hashes, terms = load_hashes(), load_local_terms()
    hits: list[str] = []
    skip = {HASH_FILE.relative_to(ROOT).as_posix()}

    if args.files:
        for f in args.files:
            hits += scan_text(f.read_text("utf-8", "replace"), str(f), hashes, terms)
    elif args.history:
        for commit in git("rev-list", "--all").split():
            short = commit[:7]
            hits += [h.replace(":", " 커밋 메시지:", 1) for h in
                     scan_text(git("log", "-1", "--format=%B", commit), short, hashes, terms)]
            for path in git("ls-tree", "-r", "--name-only", commit).splitlines():
                if path in skip or path.lower().endswith(SKIP_SUFFIX):
                    continue
                try:
                    blob = git("show", f"{commit}:{path}")
                except subprocess.CalledProcessError:
                    continue
                hits += scan_text(blob, f"{short}:{path}", hashes, terms)
        hits = sorted(set(hits))
    else:
        paths = git("ls-files").splitlines() + git("ls-files", "--others", "--exclude-standard").splitlines()
        for path in sorted(set(paths)):
            p = ROOT / path
            if path in skip or path.lower().endswith(SKIP_SUFFIX) or not p.is_file():
                continue
            hits += scan_text(p.read_text("utf-8", "replace"), path, hashes, terms)

    if hits:
        print(f"유출 의심 {len(hits)}건(값은 표시하지 않음):")
        for h in hits[:200]:
            print("  - " + h)
        return 1
    scope = "모든 커밋·메시지" if args.history else ("지정 파일" if args.files else "현재 파일")
    print(f"유출 검사 통과({scope}). 비밀유지 이름 해시 {len(hashes)}개, 이 PC 목록 {len(terms)}개, 키·토큰·비밀번호 형태 {len(PATTERNS)}종 확인.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
