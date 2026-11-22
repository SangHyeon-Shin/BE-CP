#!/usr/bin/env python3
"""ECO2-OD(.ECL2) 또는 ECO2 XML을 사람이 읽는 표로 바꾼다. 원본 파일은 바꾸지 않는다.

입력:
  - .ECL2                      ECO2-OD 프로젝트(그대로 읽음)
  - .xml                       `eco2 decrypt`로 푼 ECO2 파일(.eco, .ecox, .tpl, .tplx)
  - .eco .ecox .tpl .tplx      eco2 패키지(beskep/ECO2)가 설치돼 있으면 바로 읽음

명령:
  python tools/eco2/eco2_table.py list   <파일>                   표(테이블) 목록과 행 수
  python tools/eco2/eco2_table.py show   <파일> [--section 외피]   주요 항목을 Markdown 표로
  python tools/eco2/eco2_table.py export <파일> --out <새 폴더>     항목별 CSV(엑셀용 UTF-8 BOM)

옵션:
  --all   기본값 행(code 0, "(없음)")도 포함
  --raw   대응표에 없는 테이블과 필드도 전부 표시

필드 이름 대응표: .claude/skills/eco2/references/eco2od-fields.json
(woo-seung/BEM-semantic-debugging, MIT. NOTICE.md 참고)
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent.parent
FIELDS = ROOT / ".claude" / "skills" / "eco2" / "references" / "eco2od-fields.json"
SKIP_PREFIX = ("weather_", "tbl_weather", "tbl_common", "tbl_profile")  # 공용 기상·프로필 자료


def _parse(text: str, tag: str) -> ET.Element:
    text = re.sub(rf'<{tag} xmlns="[^"]*"', f"<{tag}", text, count=1)
    try:
        return ET.fromstring(text)
    except ET.ParseError:
        try:
            from lxml import etree  # 손상된 XML 복구 시도
        except ImportError:
            raise
        el = etree.fromstring(text.encode("utf-8"), parser=etree.XMLParser(recover=True))
        return ET.fromstring(etree.tostring(el, encoding="unicode"))


def load(path: Path) -> tuple[ET.Element, ET.Element | None]:
    """(DS: 설계 정보, DSR: 계산 결과 또는 None)"""
    suffix = path.suffix.lower()
    if suffix in (".eco", ".ecox", ".tpl", ".tplx"):
        try:
            from eco2.core.data import Eco2
        except ImportError:
            sys.exit("이 형식은 eco2 패키지가 필요합니다. SETUP.md 3-3의 설치 명령을 실행하거나, "
                     "`eco2 decrypt <파일>`로 만든 .xml을 넣으세요.")
        eco = Eco2.read(path)
        ds_text, dsr_text = eco.ds, eco.dsr
    else:
        raw = path.read_bytes()
        start = raw.find(b"<DS")
        end = raw.find(b"</DS>")
        if start < 0 or end < 0:
            sys.exit("ECO2 설계 정보(<DS>)를 찾지 못했습니다. ECO2-OD(.ECL2) 또는 `eco2 decrypt`로 만든 .xml인지 확인하세요.")
        ds_text = raw[start:end + len(b"</DS>")].decode("utf-8", "replace")
        r_start = raw.find(b"<DSR", end)
        r_end = raw.find(b"</DSR>", end)
        dsr_text = raw[r_start:r_end + len(b"</DSR>")].decode("utf-8", "replace") if r_start >= 0 and r_end >= 0 else None
    ds = _parse(ds_text, "DS")
    dsr = _parse(dsr_text, "DSR") if dsr_text and "<DSR" in dsr_text else None
    return ds, dsr


def field_map() -> dict[str, list[tuple[str, dict[str, str]]]]:
    """XML 테이블 태그 → [(구역 이름, {XML 필드: 화면 이름})]"""
    out: dict[str, list[tuple[str, dict[str, str]]]] = {}
    if FIELDS.is_file():
        for section, spec in json.loads(FIELDS.read_text("utf-8")).items():
            out.setdefault(spec["key"], []).append((section, spec["columns"]))
    return out


def is_default(row: ET.Element) -> bool:
    return (row.findtext("code") or "").strip() == "0" and (row.findtext("설명") or "").strip() in ("(없음)", "")


def tables(ds: ET.Element, *, include_all: bool, raw: bool, section: str | None):
    """(구역 이름, 열 이름 목록, 행 목록) 생성"""
    fmap = field_map()
    tags: list[str] = []
    for child in ds:
        if child.tag not in tags:
            tags.append(child.tag)
    for tag in tags:
        if tag.startswith(SKIP_PREFIX) and not raw:
            continue
        rows = [r for r in ds.findall(tag) if include_all or not is_default(r)]
        specs = fmap.get(tag) or ([] if not raw else [(tag, {})])
        if not specs and raw:
            specs = [(tag, {})]
        for name, columns in specs:
            if section and section not in name and section != tag:
                continue
            if columns:
                header = list(columns.values())
                data = [[(r.findtext(k) or "").strip() for k in columns] for r in rows]
            else:
                keys: list[str] = []
                for r in rows:
                    keys += [c.tag for c in r if c.tag not in keys]
                header, data = keys, [[(r.findtext(k) or "").strip() for k in keys] for r in rows]
            yield name, tag, header, data


def md_table(header: list[str], data: list[list[str]]) -> str:
    esc = lambda s: s.replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(map(esc, header)) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(esc(c) for c in row) + " |" for row in data]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="ECO2-OD/ECO2 파일을 표로 보기(읽기 전용)")
    ap.add_argument("command", choices=["list", "show", "export"])
    ap.add_argument("file", type=Path)
    ap.add_argument("--section", help="구역 이름 일부(예: 외피, 난방) 또는 XML 태그(예: tbl_myoun)")
    ap.add_argument("--out", type=Path, help="export 결과를 저장할 새 폴더")
    ap.add_argument("--all", action="store_true", help="기본값 행도 포함")
    ap.add_argument("--raw", action="store_true", help="대응표에 없는 테이블·필드도 표시")
    args = ap.parse_args()

    if not args.file.is_file():
        sys.exit(f"파일이 없습니다: {args.file}")
    ds, dsr = load(args.file)

    if args.command == "list":
        fmap = field_map()
        counts: dict[str, int] = {}
        for child in ds:
            counts[child.tag] = counts.get(child.tag, 0) + 1
        print(f"설계 정보(DS) 테이블 {len(counts)}개. 계산 결과(DSR): {'있음' if dsr is not None else '없음'}\n")
        print("| XML 테이블 | 행 수 | 대응 구역 |\n|---|---|---|")
        for tag, n in counts.items():
            names = ", ".join(s for s, _ in fmap.get(tag, [])) or ("(공용 자료)" if tag.startswith(SKIP_PREFIX) else "")
            print(f"| {tag} | {n} | {names} |")
        if dsr is not None:
            r_counts: dict[str, int] = {}
            for child in dsr:
                r_counts[child.tag] = r_counts.get(child.tag, 0) + 1
            print("\n계산 결과(DSR) 테이블: " + ", ".join(f"{t}({n})" for t, n in r_counts.items()))
        return 0

    found = list(tables(ds, include_all=args.all, raw=args.raw, section=args.section))
    if not found:
        sys.exit("해당하는 구역이 없습니다. `list`로 테이블 목록을 확인하세요.")

    if args.command == "show":
        for name, tag, header, data in found:
            print(f"\n### {name} (`{tag}`, {len(data)}행)\n")
            print(md_table(header, data) if data else "(값이 있는 행 없음)")
        return 0

    if not args.out:
        sys.exit("export에는 --out <새 폴더>가 필요합니다.")
    args.out.mkdir(parents=True, exist_ok=True)
    written = []
    for name, tag, header, data in found:
        target = args.out / f"{name}.csv"
        if target.exists():
            sys.exit(f"이미 있는 파일은 덮어쓰지 않습니다: {target}")
        with target.open("w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(data)
        written.append(f"{target.name}({len(data)}행)")
    print(f"저장: {args.out}\n" + "\n".join("  - " + x for x in written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
