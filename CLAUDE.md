# BE&CP 업무 지원 저장소

BE&CP 사무소의 업무를 돕는 작업 공간이다. 업무 영역은 다음과 같다.
- 건축설계
- 건축물에너지평가(에너지절약계획서, 제로에너지건축물 인증)
- 녹색건축(G-SEED) 컨설팅
- 온실가스 외부사업 컨설팅
- 대학 건축학과 겸임교수로서의 교육

## 작업 원칙
- 한국어로 답한다. 단위는 SI(mm, m², W/m²K, kWh/m²·년)를 쓴다.
- 짧게 쓰고, 문단보다 표와 목록을 쓴다.

## 적용 기준
- 건축법, 녹색건축물 조성 지원법, 건축물의 에너지절약설계기준, 제로에너지건축물 인증 기준, G-SEED 인증기준, 해당 지자체 조례.
- 조문과 기준값은 `korean-law` MCP나 사용자가 준 원문 PDF에서 인용한다. 조문 번호와 원문을 함께 쓰고, 기억으로 쓰지 않는다.
- 인증의 공식 계산은 ECO2 결과다. EnergyPlus·pvlib 등의 결과는 비교용으로만 제시한다.

## 도구
- CAD는 **AutoCAD 정품**을 쓴다(LT 아님). 원본은 DWG다. PC 연결은 autocad-mcp-pro(`docs/tools/pc-setup.md` 3절 "정품 AutoCAD").
  - DWG 읽기: `node tools/dwg/dwgconv.mjs dwg2dxf <파일.dwg>` → DXF로 바꿔 ezdxf로 처리
  - DWG 납품: DXF로 작업한 뒤 `dxf2dwg`로 변환(기본 AutoCAD 2018 형식, `--version 2013` 등 지정 가능). 변환기가 다시 읽어 엔티티 수를 검증한다. 최종 확인은 AutoCAD에서 한다.
  - 원본 DWG는 덮어쓰지 않는다. 변환기는 이미 있는 파일에 쓰지 않는다.
  - 처음 한 번 설치: `npm ci --ignore-scripts --prefix tools/dwg`
- `.claude/skills/`, `.claude/commands/`, `.claude/agents/`: 설치한 스킬·명령·에이전트. 목록과 출처는 `docs/tools/archaiflow-tools.md`.
  - archaiflow 도구는 북미 기준으로 쓰였다. 기준값은 한국 기준표를 넣어 계산한다.
- `/cad-draft`: 평면도 이미지 → DXF 초안. 작성 기준은 `.claude/skills/cad-draft/criteria.md`.
- MCP(`.mcp.json`): `kordoc`(HWP·HWPX·PDF 읽기·쓰기·양식 채우기), `korean-law`(법령·조례·판례 조회).
- Python: ezdxf, shapely(도면), pvlib(태양광), python-hwpx, PyMuPDF.
- PC에서 CAD·Revit을 연결하는 방법: `docs/tools/pc-setup.md`.

## 항상 알릴 것
- 법규·기준·도면 사이의 모순
- 확실하지 않은 내용. 추측하지 말고 모른다고 쓴다.

## 하지 말 것
- CAD·Revit 모델이나 원본 도면을 묻지 않고 수정하기
- 메일 발송, 게시, 외부 제출을 대신 하기
- 고객 도면·서류를 사용자 확인 없이 외부 서비스로 보내기
