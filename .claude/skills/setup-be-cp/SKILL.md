---
name: setup-be-cp
description: BE&CP 저장소를 새 PC나 새 계정에서 처음 쓸 때 설치와 연결(Python 라이브러리, DWG 변환기, HWP·법령 MCP, 정품 AutoCAD 연결)을 점검하고 진행한다. Codex와 Claude Code 모두에서 쓴다. "세팅해줘", "설치해줘", "처음 설정", "환경 점검", "AutoCAD 연결해줘", 또는 도구나 MCP가 없다는 오류가 날 때 사용.
---

# BE&CP 설정

기준 문서는 저장소 루트의 `SETUP.md`다. 먼저 읽는다. 사용자는 개발자가 아니므로 쉬운 한국어로 짧게 말한다.

## 0. 지금 어느 도구인지 확인

| 지금 도구 | SETUP.md에서 따를 곳 | MCP 등록 명령 | MCP 상태 보기 |
|---|---|---|---|
| **Codex**(ChatGPT 앱 또는 Codex CLI) | 3절 | `codex mcp add ...` → 사용자 설정 `~/.codex/config.toml` | `codex mcp list`, 대화창 `/mcp` |
| Claude Code | 부록 B | `claude mcp add --scope local|user ...` | 대화창 `/mcp` |

## 1. 점검

`python tools/check_setup.py`를 실행한다. Windows에서 `python`이 없으면 `py`를 쓴다. 결과를 "준비됨 / 빠짐 / 해당 없음" 표로 요약한다.

## 2. 빠진 항목 해결

하나씩 처리한다. 각 명령 전에 무엇을 왜 하는지 한 줄로 말한다.

- 설치 명령은 `SETUP.md`에 있는 것만 쓴다. 그 밖의 설치가 필요하면 먼저 묻는다.
- 설치에는 인터넷이 필요하다. Codex가 네트워크 허용을 물으면 승인해 달라고 안내한다.
- Python, Node.js, Git 자체가 없으면 winget 명령(`SETUP.md` 3-1)을 안내한다. 설치 후 PowerShell과 Codex(또는 Claude)를 다시 열어야 한다고 알린다.
- Python 라이브러리, DWG 변환기: `SETUP.md` 3-3의 명령.
- MCP `kordoc`·`korean-law`가 안 보일 때:
  - Codex: 이 폴더를 "신뢰(trust)"했는지 확인한다. 신뢰하지 않으면 `.codex/config.toml`을 읽지 않는다.
  - Claude Code: `/mcp`에서 승인한다.
- Windows에서 kordoc이 "program not found"로 실패할 때: `SETUP.md` 4절의 kordoc 보정을 적용한다.
- AutoCAD(Windows, 정품):
  1. `python -m pip install "autocad-mcp-pro[com]"`
  2. `ALLOWED_PATHS`로 쓸 폴더를 사용자에게 묻는다. 도면 보관 폴더를 권한다. 드라이브 전체(`C:\`)나 사용자 폴더 전체는 쓰지 않는다. 폴더가 실제로 있는지 확인한다.
  3. `where autocad-mcp`로 경로를 확인한다. 없으면 `python -c "import sysconfig; print(sysconfig.get_path('scripts'))"`로 나온 폴더의 `autocad-mcp.exe` 전체 경로를 쓴다.
  4. 등록 명령을 실행한다. Codex는 `SETUP.md` 3-4, Claude Code는 부록 B.
  5. MCP는 다시 시작해야 반영된다고 알린다. 다시 시작한 뒤 "AutoCAD 연결 확인해줘"라고 하면 4단계부터 이어간다.
- 법령 개인 키는 선택이다. 사용자가 원할 때만 `SETUP.md` 3-3의 방법을 안내하고, 키는 사용자가 직접 입력하게 한다.

## 3. 재점검

`python tools/check_setup.py`가 "필수 항목 중 빠진 것: 0개"가 될 때까지 반복한다.

## 4. 동작 시험

- `node tools/dwg/dwgconv.mjs info samples/dwg/sample-plan.dwg`
- korean-law: "건축물의 에너지절약설계기준"을 검색해 결과가 나오는지 본다.
- kordoc: 사용자가 가진 HWP나 PDF가 있으면 하나 읽어 본다. 없으면 건너뛴다.
- AutoCAD(Windows):
  - 사용자에게 AutoCAD에서 `samples/dwg/sample-plan.dwg`를 열게 한다. 변환기로 만든 DWG가 AutoCAD에서 열리는지 확인하는 단계다.
  - 그다음 레이어 목록을 조회한다.

## 5. 보고

항목별 상태 표와 남은 일을 짧게 쓴다.

## 하지 말 것

- 저장소 파일(`AGENTS.md`, `CLAUDE.md`, `.codex/config.toml`, `.mcp.json`)에 PC별 경로나 키를 쓰지 않는다. 사용자 설정에만 넣는다.
- `.agents/skills/`, `.codex/agents/`를 직접 고치지 않는다. `tools/sync_codex.py`가 만든 생성물이다.
- 관리자 권한이 필요한 작업이나 시스템 설정 변경을 사용자 확인 없이 하지 않는다.
- 키와 비밀번호를 대화에 붙여넣으라고 요청하지 않는다.
- 설치가 실패하면 실패한 그대로 보고한다. 된 것처럼 쓰지 않는다.
