# BE&CP 저장소 설정 가이드

> **Codex·Claude에게:** 사용자가 "세팅해줘", "설치해줘", "AutoCAD 연결해줘"라고 하면 `setup-be-cp` 스킬을 실행한다(Codex `$setup-be-cp`, Claude Code `/setup-be-cp`). 이 문서가 설정의 기준이다.

## 1. 전체 그림

| 사용 도구 | 할 수 있는 일 | 설정 |
|---|---|---|
| **A. Codex(업무용 PC: Windows + 정품 AutoCAD)**, 기본 | 전부. AutoCAD 직접 조작 포함 | 2절 → 3절 |
| B. Claude Code(PC) | 전부 | 2절 → 부록 B |
| C. Claude Code 웹(claude.ai/code) | AutoCAD 직접 조작을 뺀 전부 | 부록 C |

설정이 끝나면 `python tools/check_setup.py`에서 **"필수 항목 중 빠진 것: 0개"**가 나와야 한다.

## 2. 계정 준비(공통)

| 항목 | 내용 |
|---|---|
| ChatGPT(Codex) | Codex가 포함된 ChatGPT 요금제와 로그인. 포함 요금제는 ChatGPT 요금제 안내에서 확인한다. |
| GitHub | GitHub 계정이 필요하다. 이 저장소는 **공개**라 누구나 받을 수 있고, 수정 권한은 소유자가 초대한 사람에게만 있다. 저장소 페이지의 Settings → Collaborators → Add people로 초대하고, 초대받은 사람이 메일에서 수락한다. |

## 3. Codex로 설정(Windows)

### 3-1. 프로그램 설치(한 번만)

시작 메뉴에서 **PowerShell**을 열고 한 줄씩 실행한다.

```powershell
winget install Git.Git
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
```

설치가 끝나면 PowerShell을 닫고 다시 연 뒤, Codex를 둘 중 하나로 설치한다.

| 방법 | 설치 | 비고 |
|---|---|---|
| **ChatGPT 데스크톱 앱**(Codex 포함), 권장 | `winget install --id 9PLM9XGG6VKS -s msstore` 또는 Microsoft Store에서 "ChatGPT" | Codex는 2026-07부터 ChatGPT 데스크톱 앱에 들어 있다. 입력창 아래 권한을 **"Ask for approval"**로 두면 Windows 샌드박스 보호를 받는다. |
| Codex CLI(터미널) | `npm install -g @openai/codex` | 설치 후 `codex`를 실행하고 ChatGPT 계정으로 로그인 |

### 3-2. 저장소 받기

```powershell
cd $HOME\Documents
git clone https://github.com/SangHyeon-Shin/BE-CP.git
```

- GitHub 로그인 창이 뜨면 쓸 GitHub 계정으로 로그인한다.
- 받은 폴더를 Codex에서 연다.
  - 앱: `Documents\BE-CP` 폴더를 프로젝트로 연다.
  - CLI: `cd BE-CP` 후 `codex`를 실행한다.
- 처음 열 때 이 폴더를 **신뢰(Trust)**할지 묻는다. **반드시 신뢰한다.** 신뢰해야 `.codex/config.toml`의 MCP(kordoc, korean-law)가 켜진다.

### 3-3. 자동 설정

Codex에게 입력한다.

```
$setup-be-cp
```

"BE&CP 세팅해줘"라고 써도 된다. Codex가 점검 → 빠진 것 설치 → 재점검을 진행하고, 명령마다 허용 여부를 묻는다. 설치는 인터넷을 쓰므로 네트워크 허용도 승인한다.

손으로 할 때 실행하는 명령(Codex가 하는 일과 같다):

```powershell
python -m pip install matplotlib numpy Pillow ezdxf shapely pvlib python-hwpx PyMuPDF
npm ci --ignore-scripts --prefix tools/dwg
codex mcp list
```

마지막 줄에 `kordoc`과 `korean-law`가 보이면 된다.

법령 조회 개인 키(선택):
- 키 없이도 공용 한도로 동작한다.
- 개인 한도가 필요하면 법제처 Open API(https://open.law.go.kr/LSO/openApi/guideList.do)에서 회원가입 → "Open API 사용 신청" → 인증키(OC)를 발급받는다.
- 키는 저장소에 넣지 않고 PC에만 둔다.
  1. PowerShell에서 실행: `setx LAW_OC "발급받은키"`
  2. 사용자 설정 파일 `%USERPROFILE%\.codex\config.toml`에 아래를 추가한다. 저장소 설정과 자동으로 합쳐진다.
     ```toml
     [mcp_servers.korean-law]
     env_http_headers = { apikey = "LAW_OC" }
     ```
  3. Codex를 다시 시작한다.

### 3-4. AutoCAD 연결(정품)

1. 연결 도구를 설치한다. **Python 3.11 이상**이 필요하다.
   ```powershell
   python -m pip install "autocad-mcp-pro[com]"
   ```
2. Codex가 읽고 쓸 수 있는 **폴더 하나**를 정한다. 도면을 보관하는 폴더가 좋다(예: `C:\Users\<사용자>\Documents\도면`). 비워 두면 거의 모든 폴더에 접근할 수 있으니 반드시 지정한다.
3. 등록한다(`<도면 폴더>`를 2번 폴더로 바꾼다). 사용자 설정에 저장되며 저장소 파일은 바뀌지 않는다.
   ```powershell
   codex mcp add autocad --env AUTOCAD_MCP_BACKEND=auto --env "ALLOWED_PATHS=<도면 폴더>" --env TOOL_PROFILE=full --env TOOL_PACKS=all --env DISCOVERY_MODE=search -- autocad-mcp
   ```
   "autocad-mcp를 찾을 수 없다"는 오류가 나면 아래 명령으로 나온 폴더의 `autocad-mcp.exe` 전체 경로를 마지막 `autocad-mcp` 자리에 넣는다.
   ```powershell
   python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
   ```
4. Codex를 완전히 종료하고 다시 실행한다. MCP는 다시 시작해야 반영된다.
5. AutoCAD를 켜고 도면을 연 상태에서 확인한다.
   ```
   AutoCAD에 열린 도면의 레이어 목록 보여줘
   ```

### 3-5. 최종 점검

```powershell
python tools/check_setup.py
node tools/dwg/dwgconv.mjs info samples/dwg/sample-plan.dwg
```

- 시험용 도면 `samples/dwg/sample-plan.dwg`를 AutoCAD에서 열어 본다. 이 저장소의 변환기로 만든 DWG라서, 정상으로 열리면 DWG 납품 기능이 AutoCAD와 호환된다는 확인이 된다.
- 벽, 해치, 한글 문자 "거실 LIVING", "안방 확인 필요", 치수, 블록이 보여야 한다.

## 4. 문제 해결(Codex)

| 증상 | 원인 | 해결 |
|---|---|---|
| `codex mcp list`에 kordoc·korean-law가 없음 | 폴더를 신뢰하지 않음 | Codex에서 폴더를 다시 열고 신뢰한다 |
| kordoc이 "program not found"(Windows) | `npx` 실행 방식 문제 | ① `codex mcp add kordoc-win -- cmd /c npx -y -p kordoc@4.24.80 kordoc-mcp` ② 사용자 설정에 `[mcp_servers.kordoc]` 아래 `enabled = false` 추가 ③ Codex 재시작 |
| MCP가 시작 시간 초과 | 첫 실행 때 다운로드가 길어짐 | 사용자 설정의 해당 서버 아래 `startup_timeout_sec = 120` 추가 |
| `autocad-mcp`를 찾을 수 없음 | Python Scripts 폴더가 PATH에 없음 | 3-4의 3번처럼 전체 경로로 등록 |
| AutoCAD가 응답하지 않음 | AutoCAD 미실행, 또는 대화상자가 열려 있음 | AutoCAD에서 도면을 열고, 열린 대화상자를 닫는다 |
| 스킬이 안 보임 | 세션 시작 후 추가됨 | Codex 재시작. 도면 영상 스킬(axono 등)은 자동 선택을 꺼 두었으므로 `$axono`처럼 직접 부른다 |
| pip·npm 설치가 막힘 | 샌드박스 네트워크 차단 | Codex가 묻는 네트워크 허용을 승인한다 |
| DWG 변환기 오류 | 패키지 미설치 | `npm ci --ignore-scripts --prefix tools/dwg` |
| winget이 없다고 나옴 | 오래된 Windows | Microsoft Store에서 "앱 설치 관리자" 업데이트, 또는 각 프로그램 공식 사이트에서 설치 |

## 5. 지켜야 할 것

- PC마다 다른 설정(키, 폴더 경로)은 저장소 파일에 넣지 않는다. Codex는 사용자 설정(`~/.codex/config.toml`), Claude Code는 `--scope local|user`.
- `.agents/skills/`와 `.codex/agents/`는 생성물이다. 원본(`.claude/`)을 고친 뒤 `python tools/sync_codex.py`를 실행한다.
- 원본 DWG는 덮어쓰지 않는다. 변환기도 이미 있는 파일에는 쓰지 않는다.
- 법령 조회는 MCP 제작자가 운영하는 공개 서버(mcp.gomdori.app)를 거친다. 서버를 거치지 않으려면 `npx korean-law-mcp setup`으로 PC에 직접 설치한다(OC 키 필수).
- 고객 도면과 서류를 외부 서비스로 보낼 때는 먼저 확인한다.
- Revit, Rhino, SketchUp 등 다른 프로그램 연결은 `docs/tools/pc-setup.md`에 있다(Claude 기준으로 쓰였으며, Codex에서는 `claude mcp add` 대신 `codex mcp add`를 쓴다).

---

## 부록 B. Claude Code로 설정(PC)

1. 3-1의 winget 3줄을 실행한 뒤 Claude Code를 설치한다: `irm https://claude.ai/install.ps1 | iex`. Claude Pro 이상 요금제가 필요하다.
2. 3-2처럼 저장소를 받고 `cd BE-CP` 후 `claude`를 실행한다. 폴더 신뢰와 `.mcp.json`의 MCP 사용을 묻는 창이 뜨면 둘 다 허용한다.
3. `/setup-be-cp`를 입력한다. 손으로 할 때는 3-3의 pip·npm 명령에 더해 Windows 보정 한 줄을 실행한다.
   ```powershell
   claude mcp add --scope local kordoc -- cmd /c npx -y -p kordoc@4.24.80 kordoc-mcp
   ```
4. AutoCAD 등록(3-4의 1·2번 후):
   ```powershell
   claude mcp add --scope user autocad -e AUTOCAD_MCP_BACKEND=auto -e "ALLOWED_PATHS=<도면 폴더>" -e TOOL_PROFILE=full -e TOOL_PACKS=all -e DISCOVERY_MODE=search -- autocad-mcp
   ```
5. 법령 개인 키(선택): `claude mcp add --scope local --transport http korean-law "https://mcp.gomdori.app/law?oc=발급받은키"`
6. MCP가 "승인 대기"면 대화창에서 `/mcp`로 승인한다.

## 부록 C. Claude Code 웹(클라우드)

1. https://claude.ai/code 에서 GitHub를 연결하고 이 저장소 접근을 허용한다.
2. 클라우드 환경을 만든다. 안내: https://code.claude.com/docs/en/claude-code-on-the-web
   - 네트워크: 제한(Limited), 패키지 관리자 허용, 허용 도메인에 `mcp.gomdori.app` 추가
   - 셋업 스크립트:
     ```bash
     #!/bin/bash
     pip3 install -q matplotlib numpy Pillow ezdxf shapely pvlib python-hwpx PyMuPDF
     for d in */tools/dwg; do [ -f "$d/package-lock.json" ] && (cd "$d" && npm ci --ignore-scripts --silent); done
     true
     ```
3. 이 환경과 저장소로 세션을 시작하고 `/setup-be-cp`로 점검한다. AutoCAD 직접 조작은 할 수 없고, DWG 파일을 올리면 변환·면적표·도면 점검은 할 수 있다.
