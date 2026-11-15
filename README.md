# BE&CP 업무 지원(Claude Code)

BE&CP 사무소의 업무를 Claude Code로 돕기 위한 저장소입니다. 업무 영역은 건축설계, 건축물에너지평가, 녹색건축 컨설팅, 교육입니다.

> **처음이라면:** [SETUP.md](SETUP.md)를 따르거나, 이 폴더에서 Claude Code를 열고 **`BE&CP 세팅해줘`**라고 입력하세요. 점검과 설치를 Claude가 진행합니다.

## 할 수 있는 일

Claude는 계산·서류·법규 찾기·도면 정리를 맡습니다. 최종 판단과 서명은 사람이 합니다.

| 업무 | Claude가 하는 일 |
|---|---|
| 에너지절약계획서·제로에너지 인증 | 도면에서 방위별 외벽·창 면적 정리, 창호일람표 → 엑셀(ECO2 입력 준비), 열관류율 기준 대조, 결로 검토 |
| 법규 검토 | 법령·조례를 **원문과 조문 번호**로 찾아 줌 |
| 녹색건축(G-SEED) | 항목별 점검표, 증빙 서류 목록, 내재탄소 기록 |
| 서류(한글 HWP) | 신청서·공문 양식 채우기, 보완요청 답변표, 숫자 검산 |
| 도면(AutoCAD) | DWG에서 면적표 작성, 도면 점검, 리비전 비교, 스케치 → CAD 초안, AutoCAD 직접 작도·수정(PC 연결 시) |
| 수업 | 학생 과제 도면 점검과 피드백 초안, 강의자료 |
| 사무소 운영 | 제안서·설계비 산정, 계약서 위험 조항 점검, 회의록 정리 |

## 이렇게 부탁하세요

- `이 DWG에서 실별 면적표 만들어줘`
- `이 창호일람표 PDF를 ECO2 입력용 엑셀로 정리해줘`
- `○○구 제2종일반주거지역 건폐율·용적률 조례 기준 찾아줘`
- `이 외벽 단면에 결로 생기는지 봐줘`
- `인증기관 보완요청서(HWP) 읽고 답변표 만들어줘`
- `AutoCAD에 열린 도면 레이어 정리해줘`

## 주요 명령

| 명령 | 내용 |
|---|---|
| `/setup-be-cp` | 환경 점검과 설치 |
| `/cad-draft` | 평면도 이미지 → CAD 도면(DXF) 초안 |
| `/condensation-check` | 단면 결로 검토 |
| `/schedule-extractor` | PDF 창호·마감 일람표 → CSV |
| `/climate-zone-mapper` | 지역 구분별 부위 단열 기준 점검표 |
| `/compliance-check` | 붙여넣은 조문과 도면 대조 |
| `/plan-check-response-builder` | 보완 요청 항목별 답변표 |
| `/drawing-diff` | 도면 리비전 비교 |
| `/design-critic` | 설계 크리틱(수업 피드백) |
| `/contract-review` | 계약서 위험 조항 점검 |

전체 목록(스킬 71, 명령 14, 에이전트 6)은 [docs/tools/archaiflow-tools.md](docs/tools/archaiflow-tools.md)에 있습니다.

## 폴더 구조

```
CLAUDE.md               Claude가 매번 읽는 업무 맥락과 규칙
SETUP.md                설정 가이드(PC / 웹)
.mcp.json               연결: kordoc(HWP·PDF 문서), korean-law(법령 조회)
.claude/skills/         스킬 71개(/cad-draft, 에너지·법규·도면·서류 등)
.claude/commands/       명령 14개
.claude/agents/         검토 에이전트 6개
tools/dwg/              DWG ↔ DXF 변환기(dwgconv.mjs)
tools/check_setup.py    환경 점검
templates/project/      프로젝트 폴더용 CLAUDE.md 견본
samples/                시험용 도면(dwg), 도면 영상 스킬 예제(dessins)
docs/research/          업무 조사와 도입 계획
docs/tools/             설치 도구 목록, 다른 프로그램(Revit·Rhino) 연결
docs/prompts/           바로 쓰는 프롬프트
```

## 주의

- AI 결과는 틀릴 수 있습니다. 숫자·치수·조문은 반드시 확인합니다.
- 인증의 공식 계산은 ECO2입니다. Claude는 입력 준비와 검토를 맡습니다.
- Claude는 서명·제출·메일 발송을 하지 않습니다. 원본 DWG도 덮어쓰지 않습니다.

## 출처

| 구성 | 출처 |
|---|---|
| 스킬·명령·에이전트 82개 | archaiflow.com "Claude Code for Architecture" 카탈로그 |
| 도면 영상 스킬 7개(/axono 등) | the.invest.room 키트 |
| DWG 변환 | acad-ts(MIT), LibreDWG WebAssembly(GPL-3.0). 사내 사용 기준 |
| 문서·법령 MCP | kordoc, korean-law-mcp(MIT) |
