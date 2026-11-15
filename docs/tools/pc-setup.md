# PC 설치 가이드(Windows)

CAD·Revit 같은 데스크톱 프로그램은 클라우드 세션에서 조작할 수 없다. 프로그램이 설치된 PC에서 Claude를 실행해야 한다.

| 작업 | 클라우드 세션(지금 이 저장소) | PC |
|---|---|---|
| DXF·PDF·HWP 파일 처리, 법령 조회, 스킬 실행 | 가능 | 가능 |
| AutoCAD·ZWCAD·Revit·Rhino를 Claude가 직접 조작 | 불가 | 가능(이 문서의 3~5절) |
| EnergyPlus 시뮬레이션(Docker) | 불가 | 가능(6절) |

## 1. 준비

- Claude 유료 요금제(**Pro 이상**). 무료 요금제에는 Claude Code가 없다.
- Claude 설치는 둘 중 하나를 고른다.
  - 데스크톱 앱(https://claude.com/download): Revit·Rhino 연결은 이 앱에서 동작한다.
  - 터미널: PowerShell에서 `irm https://claude.ai/install.ps1 | iex`. 설치 후 `claude --version`으로 확인한다.
- Node.js 18 이상(MCP 실행용 `npx`), Git for Windows, Python 3.11 이상
- 이 저장소 받기: `git clone https://github.com/SangHyeon-Shin/BE-CP.git` (공개 저장소)
- Python 라이브러리: `pip install matplotlib numpy Pillow ezdxf shapely pvlib python-hwpx PyMuPDF`

## 2. 저장소에 이미 설정된 MCP(Windows 보정)

`.mcp.json`에 두 서버가 있다. 저장소 폴더에서 처음 `claude`를 실행하면 사용 여부를 묻는다.

| 서버 | 용도 | Windows에서 할 일 |
|---|---|---|
| kordoc | HWP·HWPX·PDF 읽기·쓰기·양식 채우기·서류 검수 | Windows에서는 `npx` 앞에 `cmd /c`가 필요하다. 저장소 폴더에서 한 번 실행: `claude mcp add --scope local kordoc -- cmd /c npx -y -p kordoc@4.24.80 kordoc-mcp` (같은 이름의 local 설정이 저장소 설정보다 우선한다) |
| korean-law | 법령·조례·행정규칙·판례 조회 | 키 없이 공용 한도로 동작한다. 본인 키는 아래 참고 |

법령 MCP 본인 키(선택):
1. 법제처 Open API(https://open.law.go.kr/LSO/openApi/guideList.do)에서 회원가입 → "Open API 사용 신청" → 인증키(OC) 발급
2. 저장소 폴더에서 실행: `claude mcp add --scope local --transport http korean-law "https://mcp.gomdori.app/law?oc=발급받은키"`

참고: 이 설정은 MCP 제작자가 운영하는 공개 서버(mcp.gomdori.app)를 거쳐 법제처를 조회한다. 서버를 거치지 않으려면 `npx korean-law-mcp setup`으로 PC에 직접 설치한다(OC 키 필수).

## 3. AutoCAD 연결

업무용 PC는 **정품 AutoCAD**다(2026-11-15 확인). 아래 "정품 AutoCAD" 절차를 따른다.

참고: AutoCAD 제목 표시줄이나 도움말 > 정보에 **"AutoCAD LT"**라고 나오면 LT, 아니면 정품(AutoCAD 또는 AutoCAD Architecture 등)이다.

| 종류 | 연결 도구 | 방식 |
|---|---|---|
| AutoCAD(정품) | autocad-mcp-pro | Windows COM으로 실행 중인 AutoCAD를 직접 조작. 240개 이상 도구(작도·수정·실·일람표·치수·시트) |
| AutoCAD LT 2024 이상 | autocad-mcp | AutoLISP 파일 연동으로 조작. LT 2023 이하는 AutoLISP가 없어 연결할 수 없다 |

### 정품 AutoCAD

1. 저장소 폴더의 터미널에서 실행: `pip install "autocad-mcp-pro[com]"`
2. 읽고 쓸 폴더를 하나로 제한해 등록한다(예: 프로젝트 도면 폴더). 비워 두면 거의 모든 폴더에 접근할 수 있다.
   ```
   claude mcp add --scope user autocad -e AUTOCAD_MCP_BACKEND=auto -e "ALLOWED_PATHS=C:\Users\<사용자>\Documents\BE-CP-도면" -- autocad-mcp
   ```
3. AutoCAD를 켜고 도면을 연 뒤 Claude에서 "AutoCAD에 열린 도면의 레이어 목록 보여줘"로 연결을 확인한다.

### AutoCAD LT 2024 이상

git과 uv가 필요하다. PowerShell에서 순서대로 실행한다.
1. `git clone https://github.com/puran-water/autocad-mcp "$env:USERPROFILE\.claude-arch\autocad-mcp"`
2. `cd "$env:USERPROFILE\.claude-arch\autocad-mcp"; uv sync`
3. `claude mcp add --scope user autocad-mcp -e AUTOCAD_MCP_BACKEND=auto -- "$env:USERPROFILE\.claude-arch\autocad-mcp\.venv\Scripts\python.exe" -m autocad_mcp`
4. AutoCAD LT에서 `APPLOAD`로 `lisp-code\mcp_dispatch.lsp`(1단계 폴더 안)를 불러온다.

### 클라우드 세션에서 DWG 다루기(AutoCAD 연결 없이)

PC 연결 없이도 DWG 파일을 이 저장소에 올리면 처리할 수 있다.
- `node tools/dwg/dwgconv.mjs dwg2dxf 도면.dwg` → DXF로 읽어 면적표, 창호 수량, 도면 검사
- `node tools/dwg/dwgconv.mjs dxf2dwg 결과.dxf` → AutoCAD 2018 형식 DWG(검증 포함)

## 4. Revit(Revit을 쓰는 경우)

출처: Architecture AI Starter Kit의 "Revit x Claude: MCP Connection Guide", Revit × Claude 무료 핸드북

조건
- **정품 Revit 2024~2027, Windows**(Revit LT는 애드인을 쓸 수 없어 불가)
- 같은 PC에 Claude 데스크톱 앱
- 작업용 사본(공동 작업 파일은 File > Open에서 Detach from Central)

설치
1. pyRevit을 설치하고, pyRevit Settings에서 **Routes**를 켠다(로컬 포트 48884).
2. Revit의 pyRevit 탭 > Extensions에서 **MCP Server for Revit Python Extension**을 설치하고 다시 불러온다. 브라우저에서 `http://localhost:48884/revit_mcp/status/`를 열어 `"status": "active"`인지 확인한다.
3. uv를 설치하고, Claude 앱의 Settings > Developer > Edit Config에 아래를 추가한다. `main.py` 경로는 `%APPDATA%\pyRevit\Extensions` 안 확장 폴더에 있으며, 경로는 `/`로 쓴다.
   ```json
   {
     "mcpServers": {
       "Revit Connector": {
         "command": "uv",
         "args": ["run", "--with", "mcp[cli]", "mcp", "run", "C:/Users/<사용자>/AppData/Roaming/pyRevit/Extensions/<확장폴더>/main.py"]
       }
     }
   }
   ```
4. Claude 앱을 완전히 종료한 뒤 다시 열고, Revit에서 프로젝트를 연 상태로 "Revit 상태 확인해줘"라고 요청한다. 연결되면 모델 이름을 답한다.

2~3단계는 Claude Code에 맡길 수 있다. 터미널에서 `claude`를 실행하고 붙여넣는다.
```
Install the Revit MCP server from https://github.com/mcp-servers-for-revit/mcp-server-for-revit-python
for use with Claude Desktop on Windows:
1. Clone the repo into %APPDATA%\pyRevit\Extensions, renaming the folder to end in ".extension".
2. Install uv if it isn't already on PATH.
3. Add a "Revit Connector" entry to mcpServers in my claude_desktop_config.json that runs
   the repo's main.py with uv (the README's "Connecting to Claude Desktop" section has the JSON).
4. Tell me what I still need to do by hand in Revit and Claude Desktop.
```

버전: Revit 2025에서 시험됐다. 2024~2026은 최신 pyRevit에서 동작한다. 2027은 pyRevit 6.4.0 이상이 필요하고 아직 불안정하다.

Revit 스킬(선택)
- 무료 체험 3종: 분해 액소노메트릭, 실 하나에 섹션 박스, 일람표를 엑셀로. Gumroad(https://architex484.gumroad.com/l/revit_claude)의 Start here 페이지에서 `revit-skills-free.zip`을 받는다. 계정이 필요해 이 저장소에서는 대신 받을 수 없다.
- 설치: Claude 앱에 zip을 끌어다 놓고 다음 문장과 함께 보낸 뒤, 나온 카드에서 Save plugin을 누른다.
  `Build the plugin from this zip and give me the card to install it. Leave the skills as they are.`
- 첫 실행은 읽기만 하는 작업으로 한다(모델을 바꾸지 않음).
  `Use my Revit skills for this. Put the schedules in this model into Excel.`
- 전체 44종은 유료다. 사용 팁은 `docs/prompts/starter-kit-prompts.md` 5절.

## 5. 기타 프로그램

| 프로그램 | 방법 |
|---|---|
| Rhino 8 | Rhino에서 PackageManager → **Rhino-MCP-Platform**(McNeel 공식) 설치 → 재시작 → `MCPConnect` 실행 후 안내된 명령을 Claude 설정에 추가 |
| SketchUp | 설치 없음. claude.ai 커넥터 디렉터리에서 SketchUp(Trimble)을 Trimble ID로 연결. 새 모델 생성만 가능하고 기존 .skp 편집은 불가 |
| Archicad | 무료 Tapir 애드온 + MCP. Starter Kit의 Archicad 가이드 참고 |
| Notion·Gmail·Drive | Claude 앱 메시지 창의 + → Connectors → Add connector → 검색 → Connect. 승인한 계정이 볼 수 있는 범위만 Claude도 본다 |

## 6. 에너지 시뮬레이션(선택)

Docker Desktop을 설치·실행한 뒤 다음 명령을 실행한다.
- `npx archtmpl@latest --mcp energyplus-mcp`(LBNL 공식)
- `npx archtmpl@latest --mcp openstudio-mcp`

설계 대안 비교용이다. 인증 계산은 ECO2로 한다.

`npx archtmpl` 주의: 이 도구는 마지막에 `claude mcp add --global ...`로 등록하는데, 현재 Claude Code에는 `--global` 옵션이 없어 등록 단계가 실패할 수 있다. 실패 메시지가 나오면 출력된 명령에서 `--global`을 `--scope user`로 바꿔 다시 실행한다.
