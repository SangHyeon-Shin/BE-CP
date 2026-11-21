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
| 스킬 85개(명령 14개 포함) | `.agents/skills/` — `$이름`으로 호출, 요청이 맞으면 자동 선택 | `.claude/skills/`, `.claude/commands/` — `/이름` |
| 검토 에이전트 6개 | `.codex/agents/*.toml` | `.claude/agents/` |
| MCP(kordoc, korean-law) | `.codex/config.toml`(프로젝트를 신뢰해야 로드) | `.mcp.json` |

- **원본은 `.claude/`다.** `.agents/skills/`와 `.codex/agents/`는 `python tools/sync_codex.py`가 만든 생성물이므로 직접 고치지 않는다. 원본을 고친 뒤 이 스크립트를 실행한다.
- 스킬 문서에 나오는 `/이름`은 Codex에서 `$이름`이다.
- 스킬 목록과 출처: `docs/tools/archaiflow-tools.md`. archaiflow 도구는 북미 기준으로 쓰였으므로 기준값은 한국 기준표를 넣어 계산한다.
- `cad-draft`: 평면도 이미지 → DXF 초안. 작성 기준은 `.claude/skills/cad-draft/criteria.md`.

### MCP
- `kordoc`: HWP·HWPX·PDF 읽기·쓰기·양식 채우기
- `korean-law`: 법령·조례·판례 조회
- `autocad`: PC에서만, 사용자 설정에 등록

### 기타
- Python 라이브러리: ezdxf, shapely(도면), pvlib(태양광), python-hwpx, PyMuPDF.
- 시험용 도면: `samples/dwg/`. 도면 영상 스킬(axono 등) 예제: `samples/dessins/`.
- 프로젝트 폴더용 맥락 파일 견본: `templates/project/`. 바로 쓰는 프롬프트: `docs/prompts/`.
- Revit·Rhino 등 다른 프로그램 연결: `docs/tools/pc-setup.md`.

## 항상 알릴 것
- 법규·기준·도면 사이의 모순
- 확실하지 않은 내용. 추측하지 말고 모른다고 쓴다.

## 하지 말 것
- CAD·Revit 모델이나 원본 도면을 묻지 않고 수정하기
- 메일 발송, 게시, 외부 제출을 대신 하기
- 고객 도면·서류를 사용자 확인 없이 외부 서비스로 보내기
