# BE&CP 저장소 설정 가이드

> **Claude에게:** 사용자가 "세팅해줘", "설치해줘", "AutoCAD 연결해줘"라고 하면 `/setup-be-cp` 스킬을 실행한다. 이 문서가 설정의 기준이다.

## 1. 전체 그림

| 사용 방식 | 할 수 있는 일 | 설정 |
|---|---|---|
| **A. 업무용 PC(Windows + 정품 AutoCAD)**, 권장 | 전부. AutoCAD 직접 조작 포함 | 2절 → 3절 |
| B. Claude Code 웹(claude.ai/code) | AutoCAD 직접 조작을 뺀 전부. DWG 파일을 올리면 처리 가능 | 2절 → 4절 |

설정이 끝나면 `python tools/check_setup.py`에서 **"필수 항목 중 빠진 것: 0개"**가 나와야 한다.

## 2. 계정 준비(공통)

| 항목 | 내용 |
|---|---|
| Claude | **Pro 이상** 요금제. 무료 요금제에는 Claude Code가 없다. |
| GitHub | GitHub 계정이 필요하다. 이 저장소는 **공개**라 누구나 받을 수 있고, 수정 권한은 소유자가 초대한 사람에게만 있다. 저장소 페이지의 Settings → Collaborators → Add people로 초대하고, 초대받은 사람이 메일에서 수락한다. |

## 3. 경로 A: 업무용 PC(Windows)

### 3-1. 프로그램 설치(한 번만)

시작 메뉴에서 **PowerShell**을 열고 한 줄씩 실행한다.

```powershell
winget install Git.Git
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
```

설치가 끝나면 PowerShell을 닫고 다시 연 뒤 Claude Code를 설치한다.

```powershell
irm https://claude.ai/install.ps1 | iex
```

다시 PowerShell을 열고 `claude --version`으로 설치를 확인한다. 처음 `claude`를 실행하면 Claude 계정 로그인 창이 뜬다.

### 3-2. 저장소 받기

```powershell
cd $HOME\Documents
git clone https://github.com/SangHyeon-Shin/BE-CP.git
cd BE-CP
claude
```

- GitHub 로그인 창이 뜨면 쓸 GitHub 계정으로 로그인한다.
- `claude`를 처음 실행하면 두 가지를 묻는다. 둘 다 허용한다.
  1. 이 폴더를 신뢰하는지
  2. `.mcp.json`의 MCP 서버(kordoc, korean-law)를 사용할지

### 3-3. 자동 설정

Claude에게 입력한다.

```
BE&CP 세팅해줘
```

Claude가 점검 → 빠진 것 설치 → 재점검을 진행한다. 명령을 실행할 때마다 허용 여부를 묻는다.

손으로 할 때 실행하는 명령(Claude가 하는 일과 같다):

```powershell
python -m pip install matplotlib numpy Pillow ezdxf shapely pvlib python-hwpx PyMuPDF
npm ci --ignore-scripts --prefix tools/dwg
claude mcp add --scope local kordoc -- cmd /c npx -y -p kordoc@4.24.80 kordoc-mcp
```

마지막 줄은 Windows에서 `npx`로 실행하는 MCP 서버에 필요한 보정이다. 같은 이름의 local 설정이 저장소 설정보다 우선한다.

법령 조회 개인 키(선택):
- 키 없이도 공용 한도로 동작한다.
- 개인 한도가 필요하면 법제처 Open API(https://open.law.go.kr/LSO/openApi/guideList.do)에서 회원가입 → "Open API 사용 신청" → 인증키(OC)를 발급받는다.
- 이 폴더에서 실행한다. 키는 저장소 파일에 넣지 않는다.

```powershell
claude mcp add --scope local --transport http korean-law "https://mcp.gomdori.app/law?oc=발급받은키"
```

### 3-4. AutoCAD 연결(정품)

1. 연결 도구를 설치한다. **Python 3.11 이상**이 필요하다.
   ```powershell
   python -m pip install "autocad-mcp-pro[com]"
   ```
2. Claude가 읽고 쓸 수 있는 **폴더 하나**를 정한다. 도면을 보관하는 폴더가 좋다(예: `C:\Users\<사용자>\Documents\도면`). 비워 두면 거의 모든 폴더에 접근할 수 있으니 반드시 지정한다.
3. 등록한다(`<도면 폴더>`를 2번 폴더로 바꾼다).
   ```powershell
   claude mcp add --scope user autocad -e AUTOCAD_MCP_BACKEND=auto -e "ALLOWED_PATHS=<도면 폴더>" -e TOOL_PROFILE=full -e TOOL_PACKS=all -e DISCOVERY_MODE=search -- autocad-mcp
   ```
   "autocad-mcp를 찾을 수 없다"는 오류가 나면 아래 명령으로 나온 폴더의 `autocad-mcp.exe` 전체 경로를 마지막 `autocad-mcp` 자리에 넣는다.
   ```powershell
   python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
   ```
4. Claude Code를 완전히 종료하고 다시 실행한다. MCP는 다시 시작해야 반영된다.
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

## 4. 경로 B: Claude Code 웹(클라우드)

1. https://claude.ai/code 에서 GitHub를 연결하고 이 저장소 접근을 허용한다.
2. 클라우드 환경을 만든다(세션 제목 표시줄의 환경 메뉴 → 새 환경). 안내: https://code.claude.com/docs/en/claude-code-on-the-web
   - 이름: `BE-CP`
   - 네트워크: 제한(Limited), 패키지 관리자 허용, 허용 도메인에 `mcp.gomdori.app` 추가(법령 조회용)
   - 셋업 스크립트:
     ```bash
     #!/bin/bash
     pip3 install -q matplotlib numpy Pillow ezdxf shapely pvlib python-hwpx PyMuPDF
     for d in */tools/dwg; do [ -f "$d/package-lock.json" ] && (cd "$d" && npm ci --ignore-scripts --silent); done
     true
     ```
3. 이 환경과 저장소로 세션을 시작하고 "BE&CP 세팅해줘"로 점검한다.

웹에서는 AutoCAD를 직접 조작할 수 없다. DWG 파일을 세션에 올리면 변환, 면적표, 도면 점검은 할 수 있다.

## 5. 문제 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| kordoc 연결 실패(Windows) | `npx` 실행 보정 없음 | 3-3의 마지막 명령 |
| kordoc·korean-law가 "승인 대기" | MCP 사용 승인 전 | Claude Code에서 `/mcp` → 해당 서버 승인 |
| korean-law 연결 실패 | 네트워크 차단 | PC: 회사 방화벽 확인 / 웹: 허용 도메인에 `mcp.gomdori.app` |
| `autocad-mcp`를 찾을 수 없음 | Python Scripts 폴더가 PATH에 없음 | 3-4의 3번처럼 전체 경로로 등록 |
| AutoCAD가 응답하지 않음 | AutoCAD 미실행, 또는 대화상자가 열려 있음 | AutoCAD에서 도면을 열고, 열린 대화상자를 닫는다 |
| DWG 변환기 오류 | 패키지 미설치 | `npm ci --ignore-scripts --prefix tools/dwg` |
| winget이 없다고 나옴 | 오래된 Windows | Microsoft Store에서 "앱 설치 관리자" 업데이트, 또는 각 프로그램 공식 사이트에서 설치 |

## 6. 지켜야 할 것

- PC마다 다른 설정(키, 폴더 경로)은 저장소 파일에 넣지 않는다. `--scope local` 또는 `--scope user`로 등록한다.
- 원본 DWG는 덮어쓰지 않는다. 변환기도 이미 있는 파일에는 쓰지 않는다.
- 법령 조회는 MCP 제작자가 운영하는 공개 서버(mcp.gomdori.app)를 거친다. 서버를 거치지 않으려면 `npx korean-law-mcp setup`으로 PC에 직접 설치한다(OC 키 필수).
- 고객 도면과 서류를 외부 서비스로 보낼 때는 먼저 확인한다.
- Revit, Rhino, SketchUp 등 다른 프로그램 연결은 `docs/tools/pc-setup.md`에 있다.
