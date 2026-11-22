# BE&CP 업무 지원 저장소

BE&CP 사무소의 업무를 돕는 작업 공간이다. 이 파일은 Codex와 Claude Code가 함께 읽는 공통 지침이다(Claude Code는 `CLAUDE.md`에서 이 파일을 불러온다).

업무 영역:
- 건축설계
- 건축물에너지평가(에너지절약계획서, 제로에너지건축물 인증)
- 녹색건축(G-SEED) 컨설팅
- 온실가스 외부사업 컨설팅
- 대학 건축학과 겸임교수로서의 교육

## 처음 사용할 때
- 사용자가 세팅을 요청하거나, 도구·MCP가 없다는 오류가 나면 `setup-be-cp` 스킬을 따른다(Codex `$setup-be-cp`, Claude Code `/setup-be-cp`). 기준 문서는 `SETUP.md`다.
- 환경 점검: `python tools/check_setup.py`
- PC마다 다른 설정(키, 폴더 경로)은 저장소 파일에 쓰지 않는다. Codex는 `codex mcp add`(사용자 설정 `~/.codex/config.toml`), Claude Code는 `claude mcp add --scope local|user`로 등록한다.

## 작업 원칙
- 한국어로 답한다. 단위는 SI(mm, m², W/m²K, kWh/m²·년)를 쓴다.
- 짧게 쓰고, 문단보다 표와 목록을 쓴다.
- 사용자는 개발자가 아니다. 명령이나 코드를 실행하기 전에 무엇을 왜 하는지 한 줄로 쉽게 말한다.

## 적용 기준
- 건축법, 녹색건축물 조성 지원법, 건축물의 에너지절약설계기준, 제로에너지건축물 인증 기준, G-SEED 인증기준, 해당 지자체 조례.
- 조문과 기준값은 `korean-law` MCP나 사용자가 준 원문 PDF에서 인용한다. 조문 번호와 원문을 함께 쓰고, 기억으로 쓰지 않는다.
- 인증의 공식 계산은 ECO2 결과다. EnergyPlus·pvlib 등의 결과는 비교용으로만 제시한다.

## 도구

### AutoCAD(정품, LT 아님)
- 원본은 DWG다.
- PC에서는 MCP `autocad`(autocad-mcp-pro)로 실행 중인 AutoCAD를 조작한다(`SETUP.md` 3-4).
  - 사용자가 연 도면에서, 요청받은 범위만 작업한다.
  - 지우기·덮어쓰기 전에는 묻는다.
- DWG 읽기: `node tools/dwg/dwgconv.mjs dwg2dxf <파일.dwg>`로 DXF로 바꾼 뒤 ezdxf로 처리한다.
- DWG 납품: DXF로 작업한 뒤 `dxf2dwg`로 변환한다.
  - 기본은 AutoCAD 2018 형식이고, `--version 2013` 등으로 지정할 수 있다.
  - 변환기가 다시 읽어 엔티티 수를 검증한다. 최종 확인은 AutoCAD에서 한다.
- 원본 DWG는 덮어쓰지 않는다. 변환기는 이미 있는 파일에 쓰지 않는다.
- 처음 한 번 설치: `npm ci --ignore-scripts --prefix tools/dwg`

### 스킬·명령·에이전트
| 도구 | Codex | Claude Code |
|---|---|---|
| 스킬 87개(명령 14개 포함) | `.agents/skills/` — `$이름`으로 호출, 요청이 맞으면 자동 선택 | `.claude/skills/`, `.claude/commands/` — `/이름` |
| 검토 에이전트 6개 | `.codex/agents/*.toml` | `.claude/agents/` |
| MCP(kordoc, korean-law) | `.codex/config.toml`(프로젝트를 신뢰해야 로드) | `.mcp.json` |

- **원본은 `.claude/`다.** `.agents/skills/`와 `.codex/agents/`는 `python tools/sync_codex.py`가 만든 생성물이므로 직접 고치지 않는다. 원본을 고친 뒤 이 스크립트를 실행한다.
- 스킬 문서에 나오는 `/이름`은 Codex에서 `$이름`이다.
- 스킬 목록과 출처: `docs/tools/archaiflow-tools.md`. archaiflow 도구는 북미 기준으로 쓰였으므로 기준값은 한국 기준표를 넣어 계산한다.
- `cad-draft`: 평면도 이미지 → DXF 초안. 작성 기준은 `.claude/skills/cad-draft/criteria.md`.

### ECO2·ECO2-OD
- `eco2` 스킬을 따른다. 입력값 표: `python tools/eco2/eco2_table.py show <파일>`. ECO2-OD(.ECL2)는 바로 읽고, ECO2(.eco 등)는 eco2 패키지(beskep/ECO2)가 필요하다.
- 원본 ECO2 파일은 덮어쓰지 않는다. 대안 파일(U값·SHGC 변경)은 비교용이며 인증 제출에 쓰지 않는다.
- ECO2 계산 자체는 ECO2 프로그램에서만 한다. 이 도구들은 계산 엔진이 아니다.

### MCP
- `kordoc`: HWP·HWPX·PDF 읽기·쓰기·양식 채우기
- `korean-law`: 법령·조례·판례 조회
- `autocad`: PC에서만, 사용자 설정에 등록
- `playwright`(선택, PC): 웹 서비스를 페이지 구조로 읽어 조작한다. 스크린샷 기반 컴퓨터 사용보다 우선한다(`SETUP.md` 3-5).
  - 로그인은 사용자가 직접 한다. 비밀번호를 묻거나 입력하지 않는다.
  - 저장·제출·결제·삭제 버튼은 누르기 전에 무엇을 누르는지 말하고 확인을 받는다.
  - 같은 화면 흐름을 반복하면 Playwright 스크립트로 만들어 재사용할지 제안한다.

### 기타
- Python 라이브러리: ezdxf, shapely(도면), pvlib(태양광), python-hwpx, PyMuPDF.
- 시험용 도면: `samples/dwg/`. 도면 영상 스킬(axono 등) 예제: `samples/dessins/`.
- 프로젝트 폴더용 맥락 파일 견본: `templates/project/`. 바로 쓰는 프롬프트: `docs/prompts/`.
- 시연 시나리오(효과 확인용): `docs/demo/demo-script.md`. "시연 N번 진행해줘"라고 하면 이 문서대로 한다.
- Revit·Rhino 등 다른 프로그램 연결: `docs/tools/pc-setup.md`.

## 항상 알릴 것
- 법규·기준·도면 사이의 모순
- 확실하지 않은 내용. 추측하지 말고 모른다고 쓴다.

## 저장소와 자료 관리
- 이 저장소는 GitHub **비공개** 저장소다. 업무용 PC는 GitHub 계정 없이 읽기 전용 접근키로 받는다(`SETUP.md` 3-2). 업데이트는 `git pull`.
- 업무용 PC에서는 저장소 파일을 고치지 않는다. 고치면 다음 `git pull`이 충돌한다. 고칠 점은 사용자에게 알려 저장소 관리자가 반영하게 한다.
- 고객 도면·서류, 프로젝트 값, 시연 결과, 웹 서비스 탐색 기록, 로그인 세션 파일은 `local/` 폴더(`.gitignore`로 제외)에만 두고 커밋하지 않는다.
- 커밋 전에 새 파일에 고객·프로젝트 정보가 없는지 확인한다.

## 비밀유지(NDA) 대상 서비스·자료
사용자가 비밀유지 대상이라고 한 서비스·자료(시범 사용 중인 웹 서비스 등)에 적용한다.
- **어디에도 남기지 않는다:** 서비스 이름, 주소, 화면 구조, 파일 형식, 계정 정보를 저장소 파일·커밋 메시지·이슈·외부 서비스에 쓰지 않는다. 관련 기록과 개인 스킬은 이 PC의 `local/private/`, 또는 사용자 개인 스킬 폴더(Codex `~/.agents/skills/`)에만 둔다. `private-web-service` 스킬을 따른다.
- **계정 정보:** 로그인은 사용자가 브라우저 창에서 직접 한다.
  - 아이디·비밀번호를 묻지 않는다. 대화창·파일·명령에 쓰지 않는다.
  - 대화에 비밀번호가 보이면 즉시 그 값을 쓰지 말라고 하고, 비밀번호 변경을 권한다.
- **브라우저:** Playwright는 기록이 남지 않는 격리 모드(`--isolated`)로 쓴다. 로그인 세션 파일을 저장하지 않는다(`--save-storage` 금지).
- **AI 사용 범위:** 비밀유지 각서가 AI 서비스 사용을 허용하는지 사용자가 확인한 범위에서만 화면·파일을 읽는다. 확인되지 않았으면 먼저 묻는다.
- **커밋 전 검사:** `python tools/secret_scan.py`. 비밀유지 이름은 `tools/private_terms.sha256`에 해시로만 둔다.

## 하지 말 것
- CAD·Revit 모델이나 원본 도면을 묻지 않고 수정하기
- 메일 발송, 게시, 외부 제출을 대신 하기
- 고객 도면·서류를 사용자 확인 없이 외부 서비스로 보내기
- 비밀유지 대상 정보를 저장소에 커밋하거나, 계정 정보를 묻거나 기록하기
