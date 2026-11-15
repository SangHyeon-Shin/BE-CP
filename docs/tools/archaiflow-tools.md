# archaiflow 도구 설치 기록

- 설치일: **2026-11-15**
- 출처: archaiflow.com "Claude Code for Architecture" 카탈로그(전체 **321개**: 스킬 163, 명령 54, 에이전트 47, MCP 57)
- 설치 위치: 이 저장소의 `.claude/skills/`, `.claude/agents/`, `.claude/commands/`
- 설치 수량: 스킬 **62**, 명령 **14**, 에이전트 **6**(총 82). MCP는 이 클라우드 환경에서 쓸 수 없어 설치하지 않았다(5절 참고).

## 1. 설치 방식과 검사

- 사이트의 공식 설치 도구 `npx archtmpl@latest`(v0.6.0) 코드를 먼저 읽었다. 이 도구는 `archaiflow.com/f/`에서 파일을 받아 `.claude/` 아래에 쓰고, 설치 횟수를 사이트에 보낸다.
- 이번 설치는 npx를 실행하지 않고 같은 파일을 직접 내려받았다. 내용을 검사한 뒤 복사했고, 설치 횟수 전송은 하지 않았다.
- 검사 결과
  - 압축 파일: 경로 조작(`..`, 절대경로)이나 링크 없음
  - 동봉 Python 스크립트 24개: 로컬 파일 작업만 함(작업 폴더 생성, 색인 파일 기록, PDF 비교, CSV 정리). 네트워크 호출, 외부 명령 실행, 파일 삭제 없음.
  - 마크다운 127개: 내장 셸 명령, 키·토큰, 외부 전송 지시 없음. 외부 링크는 기준·코드 출처(phius.org, passiv.de, iccsafe.org 등)뿐.
  - 에이전트 6개는 읽기 도구만 사용. `doc-finder`만 Bash가 있으며 로컬 검색 용도.
- 추가 설치: `PyMuPDF`(drawing-diff, schedule-extractor의 PDF 처리용)

## 2. 설치한 도구(업무별)

`/이름`으로 실행한다. 스킬은 대화 내용이 맞으면 자동으로도 실행된다. 에이전트는 Claude가 하위 검토자로 부른다.

### 에너지·외피(에너지평가사 업무 핵심)

| 종류 | 이름 | 용도 |
|---|---|---|
| 스킬 | condensation-check | 단면 구성의 온도 분포와 이슬점으로 결로 위치 판정 |
| 스킬 | assembly-review | 남이 만든 단면 구성의 제어층(공기·물·증기·단열) 검토 |
| 스킬 | air-barrier-trace | 단면을 따라 기밀·방수·방습·단열층 연속성 추적 |
| 스킬 | design-envelope | 외피 유형과 접합부 구분, 성능 목표 정리 |
| 스킬 | design-wall-assembly / design-roof-assembly / design-below-grade-assembly | 외벽·지붕·지하 구성 설계 |
| 스킬 | design-window-perimeter / design-balcony / design-parapet | 창호 주변, 발코니(열교), 파라펫 상세 |
| 스킬 | envelope-checklist / envelope-diff | 단계별 외피 점검표, 두 단면 버전 비교 |
| 스킬 | airtightness-tracker | 기밀 목표의 사양·시공·시험 기록 |
| 스킬 | passive-house-tracker | 패시브하우스 인증 기준 대비 성능 추적 |
| 스킬 | embodied-carbon-tracker | 내재탄소 단계별 기록(G-SEED LCA 준비) |
| 스킬 | decarbonization-strategist | 5~15년 탈탄소 로드맵(그린리모델링 제안) |
| 명령 | compare-assembly / explain-u-value / lookup-r-value / explain-vapor-retarder | 단면 비교, 열관류율 확인, 방습층 설명 |
| 명령 | test-energy / test-glazing | 부위·창호를 지역별 기준표와 대조 |
| 에이전트 | enclosure-architect / energy-modeler | 외피 전문가, 에너지 모델러 관점 검토 |

### 법규·인허가

| 종류 | 이름 | 용도 |
|---|---|---|
| 스킬 | code-reader / applicability-check / cite-check | 조문 분해, 적용 여부 판단, 인용 검증 |
| 스킬 | compliance-check | 붙여넣은 조문과 도면을 항목별로 대조 |
| 스킬 | jurisdiction-profile | 법규 한계값을 근거와 함께 한 번 기록해 재사용 |
| 스킬 | climate-zone-mapper | 지역 구분과 부위별 단열 기준 점검표(CSV) |
| 스킬 | zoning-summary | 필지 조회 결과 → 계획 초기 법규 요약 |
| 스킬 | plan-check-response-builder / submission-reader | 보완 요청에 대한 항목별 답변표, 기관 회신 해석 |
| 스킬 | permit-tracker | 인허가·심의·검사 일정 기록 |
| 명령 | explain-code / test-far / draft-letter | 조문 쉬운 설명, 건폐율·용적률·높이 확인, 기관 공문 |
| 에이전트 | senior-plan-examiner | 심사자 관점 도면 검토 |

### 설계·교육

| 종류 | 이름 | 용도 |
|---|---|---|
| 스킬 | design-critic / precedent-critique | 구조화된 설계 크리틱(수업 피드백) |
| 스킬 | plan-review / section-review | 평면·단면 검토 |
| 스킬 | daylight-study / shadow-study | 실 깊이별 채광, 일조·그림자 |
| 스킬 | site-analysis / test-fit / space-program / area-measurement | 대지 분석, 배치 가능성, 실 면적표, 면적 산정 기준 |
| 스킬 | option-compare / design-narrative | 대안 비교표, 설계 설명문 |
| 스킬 | existing-conditions-survey | 기존 건물 현황 조사(그린리모델링) |
| 명령 | test-massing | 매스 대안의 연면적·높이 비교 |
| 에이전트 | senior-architect | 경력 25년 건축가 관점 점검 |

### 도면·문서

| 종류 | 이름 | 용도 |
|---|---|---|
| 스킬 | drawing-reader / set-reader / doc-reader | 도면·도서 PDF 읽기 |
| 스킬 | drawing-diff / document-diff | 도면 리비전 비교, 문서 버전 비교 |
| 스킬 | drawing-standards-audit / markup-reader | 도면 표기 일관성 점검, 수정 표시 → 할 일 목록 |
| 스킬 | schedule-builder / schedule-extractor | 창호·마감 일람표 작성, PDF 일람표 → CSV(ECO2 창호 입력 준비) |
| 명령 | create-site-visit-report | 현장 방문 보고서 |
| 에이전트 | doc-finder | 프로젝트 파일에서 근거와 함께 답 찾기 |

### 설비(에너지 입력 관련)

| 종류 | 이름 | 용도 |
|---|---|---|
| 스킬 | equipment-reader / schedule-reader | 장비 사양서·설비 일람표 해석(ECO2 설비 입력 준비) |
| 스킬 | mep-review / design-ventilation | 설비 도면 검토, 환기량 계산 |
| 에이전트 | senior-mep-engineer | 설비 엔지니어 관점 점검 |

### 사무소 운영

| 종류 | 이름 | 용도 |
|---|---|---|
| 스킬 | aec-doc-gen | Markdown → Word·Excel·PDF |
| 스킬 | fee-estimator / rfp-response-builder | 설계비 산정, 제안서 |
| 스킬 | contract-review | 발주자 계약서의 위험 조항 검토 |
| 스킬 | project-tracker / meeting-notes-cleaner / thread-reader / lessons-learned | 프로젝트 기록, 회의록 정리, 메일 스레드 결정사항, 교훈 기록 |
| 스킬 | client-translator / file-organizer | 고객용 쉬운 설명, 폴더 정리(승인 후 이동) |
| 명령 | draft-proposal / draft-email / draft-additional-services | 용역 제안서, 메일, 추가 업무 요청 |

## 3. 설치하지 않은 것과 이유

| 구분 | 예 | 이유 |
|---|---|---|
| 미국 제도 전용 | ada-tracker, test-ada, nyc-zoning-lookup, lookup-flood-zone, sf330-builder, explain-aia, lookup-csi, lookup-cost, census-mcp, draft-payment-application | 미국 법규·양식·데이터 기준 |
| 인증 체계 불일치 | leed-tracker | LEED 전용. G-SEED에는 맞지 않음 |
| 업무 범위 밖 | 구조 계산(design-beam·column·footing), 시공사 관리(bid-review, change-order·RFI·submittal 계열), 건물 유형별 전문가 에이전트 대부분 | 소규모 설계·에너지 컨설팅 업무와 관련이 낮음 |
| 그래픽·기타 소프트웨어 | Adobe, Cinema 4D, Unreal, SolidWorks 등 MCP | 업무 관련성 낮음 |

필요하면 같은 방식으로 추가할 수 있다: `npx archtmpl@latest --skill <이름>` (사이트 공식 방법) 또는 Claude에게 요청.

## 4. 한국 업무에 쓸 때 주의

- 도구는 영어로 쓰였고 북미 실무를 기준으로 한다. 한국어로 요청하면 답변은 한국어로 받을 수 있지만, 스킬이 만드는 기록 파일의 양식(표 머리글 등)과 `doc-finder` 에이전트의 중간 보고는 영어다.
- 대부분의 도구는 기준값을 내장하지 않는다. 사용자가 붙여넣은 표와 조문으로 계산한다. 따라서 건축물의 에너지절약설계기준 별표, 건축법·조례 조문, 녹색건축 인증기준 등 **한국 기준 원문을 함께 제공해야** 한다.
- 단위: 일부 도구는 R값(ft²·°F·h/Btu)을 기본으로 설명한다. 열관류율 W/m²K로 계산하도록 요청에 명시한다.
- 지역 구분: `climate-zone-mapper`, `test-energy`, `test-glazing`은 기후대를 사용자에게 받는다. 중부1·중부2·남부·제주 구분과 해당 기준표를 넣으면 된다.
- 스킬 수가 많아 Claude Code가 세션 시작 시 보여주는 스킬 설명 일부가 생략된다. 자동 실행이 잘 안 되면 `/이름`으로 직접 실행한다.

## 5. MCP: 업무용 PC에서 설치

Revit, Rhino, 법령·HWP MCP의 Windows 설정까지 포함한 전체 절차는 `docs/tools/pc-setup.md`에 있다. 담당자는 **AutoCAD**를 쓰므로 그 문서 3절만 따르면 된다. 아래 `npx archtmpl` 명령은 등록 단계에서 `--global` 옵션 때문에 실패할 수 있다(pc-setup.md 6절 주의 참고).

MCP는 AutoCAD·SketchUp 같은 데스크톱 프로그램을 Claude가 직접 조작하게 하는 연결 도구다. 프로그램이 설치된 PC에서 Claude Code를 실행해야 하므로 이 클라우드 저장소에는 설치하지 않았다.

| 상황 | MCP | PC에서 실행할 명령 | 조건 |
|---|---|---|---|
| AutoCAD(정품) 사용 | autocad-mcp-pro | `npx archtmpl@latest --mcp autocad-mcp-pro` | Windows, Python 3.11+. 설치 후 `ALLOWED_PATHS`를 작업 폴더 하나로 지정 |
| AutoCAD LT 사용 | autocad-mcp | `npx archtmpl@latest --mcp autocad-mcp` | git, uv 필요. AutoCAD에서 `mcp_dispatch.lsp`를 APPLOAD |
| ZWCAD·GstarCAD 사용 | cad-mcp | `npx archtmpl@latest --mcp cad-mcp` | Windows 전용. `src/config.json`에서 프로그램 선택 |
| 엑셀 계산서 | excel-mcp | `npx archtmpl@latest --mcp excel-mcp` | uv 필요. 엑셀 설치 불필요 |
| SketchUp 사용 | sketchup-mcp | 설치 없음. claude.ai 커넥터 디렉터리에서 Trimble ID로 연결 | 새 모델 생성만 가능(기존 .skp 편집 불가) |
| Rhino 8 사용 | rhino-mcp-mcneel | Rhino PackageManager에서 Rhino-MCP-Platform 설치 후 MCPConnect | McNeel 공식 |
| 에너지 시뮬레이션(선택) | energyplus-mcp, openstudio-mcp | `npx archtmpl@latest --mcp energyplus-mcp` 등 | Docker Desktop 필요. 공식 인증 계산(ECO2)을 대신하지 않음 |

주의: MCP 설치 명령은 설치 과정에서 git clone, pip, docker 같은 셸 명령을 실행한다. 사용하는 CAD 프로그램에 해당하는 것만 설치한다.
