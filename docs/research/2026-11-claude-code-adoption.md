# BE&CP 업무와 Claude Code 활용 조사

- 작성일: **2026-11-14**
- 대상: BE&CP 사무소(건축설계, 건축물에너지평가, 녹색건축 컨설팅, 교육)
- 범위: ① 공개 자료로 확인되는 업무 ② 업무별 Claude Code 활용 방안 ③ 관련 GitHub 저장소
- 저장소 수치(★, 최근 푸시)는 2026-11-14 GitHub 검색 API 기준이다. 저장소 설명은 GitHub에 등록된 설명이고, README와 코드는 열람하지 않았다.

---

## 1. 결론

- 업무의 중심은 **설계도서 → 에너지·녹색건축 인증 자료 작성**이다. 이 과정은 반복 계산, 표 작성, 법령 대조, HWP 서류 작업이 많아 Claude Code로 자동화하기 좋다.
- 공개 저장소가 이미 있는 분야와 비어 있는 분야가 나뉜다.

| 분야 | 공개 저장소 상황 |
|---|---|
| HWP 문서 처리, 법령 조회, DXF 처리, CAD·BIM 연동(MCP), EnergyPlus 시뮬레이션 | 성숙한 저장소가 있어 바로 쓸 수 있음 |
| ECO2 입력 준비, 에너지절약계획서(EPI) 검토, G-SEED 점수 관리 | 검색 결과 **0~1건**. 직접 만들면 BE&CP 고유 자산이 됨 |

- 우선순위
  1. HWP 문서와 법령 조회 도구를 설치한다.
  2. 도면(DXF)에서 면적과 외피 수량을 뽑는 스크립트를 만든다.
  3. 그 결과로 ECO2 입력표와 EPI 검토표를 자동 작성하는 도구를 만든다.

---

## 2. 업무 조사 결과

### 2.1 확인된 사실

| 항목 | 내용 | 근거 | 확인 수준 |
|---|---|---|---|
| BE&CP 대표 | 사무소가 BE&CP로 옮겼다는 회원 소식 | [한국여성건축가협회 회원 게시판](https://www.kifaonline.com/modules/board/bd_view.html?id=member&mc_code=141510&or=bd_order&al=asc&p=6&no=40) | 공개 자료(게시일 미상) + 사용자 제공 |
| 건축물에너지평가사 | 2019년 협회 교육 공고에 "BE&CP 소속 평가사", **CAD 기초 교육** 강사(**2019-12-21**) | [건축물에너지평가사협회 2019 하반기 교육 공고](http://kibea.org/notice/?bmode=view&idx=15393513) | 공개 자료 |
| BE&CP의 협회 활동 | 같은 공고에 비이앤시피(BE&CP)가 후원사로 기재, 소속 평가사가 ECO2 기초 교육 강사 | 같은 공고 | 공개 자료 |
| 녹색건축 컨설팅 | 에너지평가사 6인 컨설팅그룹 **GREEN 6**의 건축 담당. **G-SEED ID**, **온실가스 외부사업 컨설턴트**, 설계 분야 **20년** 경력으로 소개. 공동주택 G-SEED·에너지효율등급 인증 수주 보도 | [KHARN 칸, "GREEN 6, 사회저변 녹아드는 GB실현"](https://www.kharn.kr/news/article.html?no=8984) | 공개 자료(약 2018~2019년 기사, 현재 활동은 미확인) |
| 대학 건축학과 겸임교수 | 공개 자료에서 확인되지 않음 | 없음 | 사용자 제공 |
| 건축설계사 | 건축사 등록 여부는 공개 자료로 확인하지 않음 | 없음 | 사용자 제공 |

- 동명이인이 있어 이름만으로는 인물을 특정하지 않았다.
- 조사 한계: KHARN, 여성건축가협회, 건축물에너지평가사협회, DBpia 원문은 이 환경의 네트워크 제한으로 직접 열지 못했다. 위 내용은 검색엔진이 보여준 해당 페이지 내용에 근거한다.

### 2.2 업무 영역(추론)

공개 자료와 직함에서 추론한 업무 구성이다.

| 영역 | 주요 업무 | 주요 도구·제도 |
|---|---|---|
| A. 건축설계 | 계획·인허가 도면, 면적표, 법규 검토 | AutoCAD(CAD 교육 강사 이력에서 추론), 세움터 |
| B. 에너지 평가·인증 | 에너지절약계획서(EPI), 건축물에너지효율등급·제로에너지건축물(ZEB) 인증, 1차에너지소요량·에너지자립률 계산 | ECO2(ECO2-OD), 한국에너지공단·한국부동산원 인증 체계 |
| C. 녹색건축 컨설팅 | G-SEED 항목별 점수 확보 전략, 증빙 작성 | G-SEED 인증기준 |
| D. 온실가스 외부사업 | 감축량 산정, 사업계획서·모니터링 보고서 | 엑셀, HWP |
| E. 교육 | 대학 설계·이론 수업, 평가사 실무교육 | 강의자료, 과제 평가 |
| F. 사무소 운영 | 제안서·견적·계약, 공문, 인증 신청 서류 | HWP, 엑셀 |

제도 참고(검색 결과 기준, 적용 전 원문 확인 필요):
- 한국부동산원 안내에 따르면 **2025년 1월**부터 제로에너지건축물 인증으로 통합 시행되었다.
- 한국에너지공단 안내에 따르면 ZEB 인증은 1차에너지소요량과 에너지자립률로 **ZEB Plus~5등급(6개 등급)**을 매긴다.
- 출처: [한국부동산원](https://www.reb.or.kr/reb/cm/cntnts/cntntsView.do?cntntsId=1461&mi=10090), [한국에너지공단](https://www.energy.or.kr/front/conts/105002002003000.do)

---

## 3. 업무별 Claude Code 활용 방안

표기: **자동화**(반복 작업 제거), **효율화**(시간 단축·오류 감소), **첨단화**(시뮬레이션·AI 도입), **신규**(지금까지 못 하던 일)

### A. 건축설계

| 작업 | 활용 방안 | 구분 | 관련 저장소 |
|---|---|---|---|
| 스케치·이미지 평면 → CAD 초안 | 이미 설치한 `/cad-draft` 스킬로 DXF 초안 생성 | 자동화 | ezdxf, CubiCasa5k |
| AutoCAD 직접 조작 | Claude Code가 열려 있는 AutoCAD에서 그리기·수정·검사(AutoLISP) | 효율화 | puran-water/autocad-mcp(AutoCAD LT 지원), U-C4N/Autocad-MCP |
| 도면 검수 | 레이어 표준, 치수 누락, 닫히지 않은 실 경계를 DXF에서 자동 검사 | 효율화 | ezdxf, cad-ai-agent |
| 면적표 | DXF 실 경계 → 실별·층별 면적표(엑셀) 자동 산출 | 자동화 | ezdxf, shapely |
| 법규 검토 | 건축법·시행령·조례·별표를 조문 단위로 조회하고 인용을 검증한 검토서 작성 | 효율화 | chrisryugj/korean-law-mcp |
| 대지 정보 | 건축물대장·용도지역·필지 정보 조회 | 자동화 | opendata-mcp(공공데이터포털), vworld-api-mcp |
| 3D·BIM | Rhino·SketchUp·Revit·ArchiCAD·Blender를 자연어로 조작 | 첨단화 | rhinomcp, sketchup-mcp, revit-mcp, tapir-archicad-MCP, mcp-for-blender |
| 일조 사선·높이 제한 | 대지 경계와 정북 방향으로 사선 제한 매스를 자동 생성 | 신규 | 공개 저장소 미성숙(Architectural-line ★0). 자체 개발 대상 |

### B. 에너지 평가·인증(핵심)

| 작업 | 활용 방안 | 구분 | 관련 저장소 |
|---|---|---|---|
| ECO2 입력자료 준비 | DXF에서 방위별 외벽·창 면적, 실별 면적, 층고를 추출해 ECO2 입력표 작성 | 자동화·**신규** | 공개 저장소 **0건**. ezdxf로 자체 개발 |
| ECO2 결과 교차검증 | ECO2 결과 PDF와 입력표를 대조해 면적·열관류율 입력 오류 탐지 | 효율화 | pdf 처리 + 자체 스크립트 |
| 에너지절약계획서(EPI) | 항목별 배점 자동 채점, 지역별 열관류율 기준 대조, 미달 항목과 개선안 제시 | 자동화·**신규** | 공개 저장소 **0건**. korean-law-mcp로 별표 조회 + 자체 개발 |
| 열관류율·결로 | 단면 구성 → U값, 결로 위험(Glaser법) 계산서 자동 작성 | 효율화 | GlaserMethod(EN ISO 13788), U-Value-Calculator(참고) |
| 설계 초기 대안 비교 | 창면적비·단열 두께·차양을 바꾼 수십 개 대안을 EnergyPlus로 일괄 시뮬레이션해 경향 비교 | 첨단화·**신규** | LBNL-ETA/EnergyPlus-MCP, openstudio-mcp, eppy, geomeppy, honeybee-energy |
| 에너지자립률 사전 검토 | 태양광 용량·방위·경사별 발전량을 추정해 자립률 목표 달성 여부를 미리 확인 | 첨단화 | pvlib-python |
| 기상 데이터 | 기상청 자료 → EPW 변환 | 효율화 | wjx2_kma_weather_crawler(2021, 동작 확인 필요) |

주의: 인증의 공식 계산은 ECO2 결과다. EnergyPlus와 pvlib은 설계 의사결정용 비교 도구이며 ECO2 결과를 대신하지 않는다.

### C. 녹색건축(G-SEED) 컨설팅

| 작업 | 활용 방안 | 구분 | 관련 저장소 |
|---|---|---|---|
| 점수 시뮬레이터 | 프로젝트 조건으로 항목별 취득 가능 점수와 목표 등급 달성 경로 계산 | 신규 | yuha933/G-SEED-AI-Agent(★0, 참고 수준) |
| 증빙 목록·서류 | 항목별 증빙 체크리스트와 서류 초안(HWP) 자동 생성 | 자동화 | kordoc, python-hwpx |
| 채광·일사 | 실별 주광률·일사량 시뮬레이션 | 첨단화 | honeybee-radiance, frads, rad-mcp(초기) |
| 탄소(LCA) | 물량 → 내재탄소 산정 개념 검증 | 첨단화 | IfcLCA, llm-lca-demo(유럽 DB 기준이라 국내 DB 교체 필요) |

### D. 온실가스 외부사업

| 작업 | 활용 방안 | 구분 | 관련 저장소 |
|---|---|---|---|
| 감축량 산정 | 산정식과 모니터링 데이터를 엑셀로 자동 계산하고 검증 로그 작성 | 자동화 | anthropics/skills(xlsx) |
| 보고서 | 사업계획서·모니터링 보고서 HWP 초안 작성 | 효율화 | kordoc, hwp-mcp |

### E. 교육(대학, 평가사 교육)

| 작업 | 활용 방안 | 구분 | 관련 저장소 |
|---|---|---|---|
| 강의자료 | 강의 슬라이드·실습 과제·퀴즈 생성 | 효율화 | anthropics/skills(pptx·docx) |
| 과제 검사 | 학생 제출 DXF를 자동 검사(레이어·치수·면적·실 경계)하고 개인별 피드백 초안 작성 | **신규** | ezdxf + 자체 루브릭 |
| 평가 기준 | 루브릭 설계와 채점 일관성 확인 | 효율화 | anthropics/k12-teacher-skills(K-12용이나 루브릭 구조 참고) |
| 인터랙티브 교재 | 태양 궤적·그림자·에너지 등급을 조작하며 배우는 웹 페이지 | **신규** | 이미 설치한 `/ombres`·`/axono` 스킬(위도를 한국으로 바꿔야 함) |
| 평가사 시험 대비 | 기출 유형 기반 문제·해설 생성 | 효율화 | exam-study-guide-generator(참고) |

### F. 사무소 운영

| 작업 | 활용 방안 | 구분 | 관련 저장소 |
|---|---|---|---|
| HWP 서류 | 인증 신청서·공문·계약서 양식 채우기, 신구대조, HWP↔Markdown 변환 | 자동화 | chrisryugj/kordoc, jkf87/hwp-mcp, treesoop/hwp-mcp, airmang/python-hwpx |
| 제안서·견적 | 프로젝트 조건 → 제안서(docx/pptx)·견적서(xlsx) 초안 | 효율화 | anthropics/skills |
| 법령 개정 감시 | 건축법·녹색건축법·에너지 관련 고시의 개정 사항을 주기적으로 확인해 요약 | **신규** | korean-law-mcp(신구조문대비) + 예약 작업 |
| 고객 설명 자료 | 인증 등급·에너지 절감 효과를 보여주는 웹 페이지 | 신규 | Claude Artifact |

---

## 4. 저장소 목록

성숙도 기준: ★1,000 이상 = 안정, ★100~999 = 활발, ★100 미만 = 초기·참고용

### 4.1 CAD·도면

| 저장소 | ★ | 최근 푸시 | 라이선스 | 용도 |
|---|---|---|---|---|
| [mozman/ezdxf](https://github.com/mozman/ezdxf) | 1,529 | 2026-11-14 | MIT | Python DXF 읽기·쓰기. 도면 자동화의 기반 |
| [LibreDWG/libredwg](https://github.com/LibreDWG/libredwg) | 1,674 | 2026-11-14 | GPL-3.0 | DWG 읽기·DXF 변환 |
| [puran-water/autocad-mcp](https://github.com/puran-water/autocad-mcp) | 651 | 2026-11-07 | MIT | AutoCAD LT용 MCP, AutoLISP 실행, ezdxf 백엔드 |
| [U-C4N/Autocad-MCP](https://github.com/U-C4N/Autocad-MCP) | 290 | 2026-11-06 | MIT | AutoCAD MCP, 240개 이상 도구 |
| [AnCode666/multiCAD-mcp](https://github.com/AnCode666/multiCAD-mcp) | 179 | 2026-10-31 | - | 여러 CAD 프로그램용 MCP |
| [jeremylongshore/cad-ai-agent](https://github.com/jeremylongshore/cad-ai-agent) | 55 | 2026-11-13 | Apache-2.0 | DXF·벡터 PDF 분석·편집(DWG는 ODA 변환기 필요) |
| [ajflow/pdf2takeoff](https://github.com/ajflow/pdf2takeoff) | 8 | 2026-10-29 | Apache-2.0 | PDF·DXF 물량 산출 |

### 4.2 평면도 인식

| 저장소 | ★ | 최근 푸시 | 라이선스 | 용도 |
|---|---|---|---|---|
| [CubiCasa/CubiCasa5k](https://github.com/CubiCasa/CubiCasa5k) | 631 | 2026-11-08 | 확인 필요 | 평면도 5,000장 데이터셋과 모델 |
| [Yytsi/floorplan-to-3d](https://github.com/Yytsi/floorplan-to-3d) | 39 | 2026-05-13 | MIT | 평면도 분할 → 3D 벽 |
| [OldDeLorean/rtdetr-floorplan-detector](https://github.com/OldDeLorean/rtdetr-floorplan-detector) | 6 | 2026-08-05 | - | 벽·문·창 탐지 모델 |
| [OussamaSounti/Construction-Drawing-AI-System](https://github.com/OussamaSounti/Construction-Drawing-AI-System) | 2 | 2026-09-23 | - | PDF 평면도 → 문·창·벽·실 검출, 치수 판독 |

### 4.3 3D·BIM 연동(MCP)

| 저장소 | ★ | 최근 푸시 | 라이선스 | 대상 프로그램 |
|---|---|---|---|---|
| [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) | 34,369 | 2026-11-13 | MIT | Blender |
| [pascalorg/editor](https://github.com/pascalorg/editor) | 25,502 | 2026-11-14 | MIT | 브라우저 기반 건축 3D 편집기(MCP·CLI) |
| [IfcOpenShell/IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) | 2,953 | 2026-11-14 | LGPL-3.0 | IFC 라이브러리 |
| [pyrevitlabs/pyRevit](https://github.com/pyrevitlabs/pyRevit) | 2,036 | 2026-11-14 | GPL-3.0 | Revit 스크립팅 |
| [jingcheng-chen/rhinomcp](https://github.com/jingcheng-chen/rhinomcp) | 1,214 | 2026-11-07 | MIT | Rhino |
| [specklesystems/speckle-server](https://github.com/specklesystems/speckle-server) | 862 | 2026-11-12 | 확인 필요 | CAD·BIM 데이터 교환 |
| [mhyrr/sketchup-mcp](https://github.com/mhyrr/sketchup-mcp) | 552 | 2026-04-25 | 없음 | SketchUp |
| [mcp-servers-for-revit/revit-mcp](https://github.com/mcp-servers-for-revit/revit-mcp) | 479 | 2026-02-25 | MIT | Revit |
| [LTplus-AG/ifc-lite](https://github.com/LTplus-AG/ifc-lite) | 473 | 2026-11-14 | MPL-2.0 | IFC 조회·검증·MCP |
| [mcneel/RhinoAI](https://github.com/mcneel/RhinoAI) | 409 | 2026-11-12 | MIT | Rhino 공식 AI 기능 |
| [SzamosiMate/tapir-archicad-MCP](https://github.com/SzamosiMate/tapir-archicad-MCP) | 136 | 2026-11-04 | MIT | ArchiCAD |
| [brookstalley/cordyceps](https://github.com/brookstalley/cordyceps) | 111 | 2026-11-12 | MIT | Grasshopper |
| [Show2Instruct/ifc-bonsai-mcp](https://github.com/Show2Instruct/ifc-bonsai-mcp) | 69 | 2026-07-10 | MIT | Blender + Bonsai(IFC) |

### 4.4 에너지·환경 시뮬레이션

| 저장소 | ★ | 최근 푸시 | 라이선스 | 용도 |
|---|---|---|---|---|
| [pvlib/pvlib-python](https://github.com/pvlib/pvlib-python) | 1,722 | 2026-11-03 | BSD-3-Clause | 태양광 발전량 계산 |
| [NatLabRockies/EnergyPlus](https://github.com/NatLabRockies/EnergyPlus) | 1,623 | 2026-11-14 | 확인 필요 | 건물 에너지 시뮬레이션 엔진 |
| [NatLabRockies/OpenStudio](https://github.com/NatLabRockies/OpenStudio) | 658 | 2026-11-13 | 확인 필요 | EnergyPlus 모델링 SDK |
| [CityEnergyAnalyst](https://github.com/architecture-building-systems/CityEnergyAnalyst) | 286 | 2026-11-07 | MIT | 단지·도시 단위 에너지 분석 |
| [santoshphilip/eppy](https://github.com/santoshphilip/eppy) | 202 | 2026-08-26 | MIT | EnergyPlus 입력파일(IDF) 스크립팅 |
| [LBNL-ETA/EnergyPlus-MCP](https://github.com/LBNL-ETA/EnergyPlus-MCP) | 126 | 2026-11-04 | 확인 필요 | EnergyPlus용 MCP(LBNL) |
| [NatLabRockies/openstudio-mcp](https://github.com/NatLabRockies/openstudio-mcp) | 58 | 2026-11-13 | 확인 필요 | OpenStudio용 MCP |
| [jamiebull1/geomeppy](https://github.com/jamiebull1/geomeppy) | 50 | 2026-03-15 | MIT | 형상 기반 IDF 생성 |
| [ladybug-tools/honeybee-energy](https://github.com/ladybug-tools/honeybee-energy) | 37 | 2026-11-12 | AGPL-3.0 | 에너지 모델링(Python) |
| [LBNL-ETA/frads](https://github.com/LBNL-ETA/frads) | 34 | 2026-09-29 | 확인 필요 | Radiance + EnergyPlus 연동 |
| [ladybug-tools/honeybee-radiance](https://github.com/ladybug-tools/honeybee-radiance) | 21 | 2026-11-12 | AGPL-3.0 | 채광 시뮬레이션 |
| [idfkit/idfkit-mcp](https://github.com/idfkit/idfkit-mcp) | 14 | 2026-11-13 | MIT | EnergyPlus용 MCP |
| [HuiwenZhou/Eppy-LLM-Agentic-BEM](https://github.com/HuiwenZhou/Eppy-LLM-Agentic-BEM) | 3 | 2026-04-16 | MIT | 자연어 → 에너지 모델 논문 코드 |
| [wkim300/wjx2_kma_weather_crawler](https://github.com/wkim300/wjx2_kma_weather_crawler) | 3 | 2021-11-06 | - | 기상청 자료 → EPW |
| [SustainableUrbanSystemsLab/GlaserMethod](https://github.com/SustainableUrbanSystemsLab/GlaserMethod) | 1 | 2025-10-19 | - | 내부 결로 검토(EN ISO 13788) |
| [akontadakis/rad-mcp](https://github.com/akontadakis/rad-mcp) | 0 | 2026-10-27 | MIT | Radiance용 MCP(초기) |

### 4.5 국내 문서·법령·공공데이터

| 저장소 | ★ | 최근 푸시 | 라이선스 | 용도 |
|---|---|---|---|---|
| [chrisryugj/kordoc](https://github.com/chrisryugj/kordoc) | 2,992 | 2026-11-14 | MIT | HWP·HWPX·PDF 읽기·편집·작성, 양식 채우기, 신구대조 |
| [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | 2,871 | 2026-11-03 | MIT | 법령·조문·별표·판례·해석례·조례 조회, 인용 검증 |
| [jkf87/hwp-mcp](https://github.com/jkf87/hwp-mcp) | 270 | 2026-09-27 | 없음 | HWP 처리 MCP |
| [airmang/python-hwpx](https://github.com/airmang/python-hwpx) | 123 | 2026-11-14 | Apache-2.0 | 한컴오피스 없이 HWPX 읽기·편집·생성 |
| [treesoop/hwp-mcp](https://github.com/treesoop/hwp-mcp) | 107 | 2026-11-01 | MIT | HWP·HWPX 읽기·쓰기 MCP(34개 도구) |
| [legalize-kr/agent-skills](https://github.com/legalize-kr/agent-skills) | 17 | 2026-10-16 | Apache-2.0 | 법령·행정규칙·자치법규 조회 스킬 |
| [aeriis-kr/opendata-mcp](https://github.com/aeriis-kr/opendata-mcp) | 11 | 2026-09-11 | Apache-2.0 | 공공데이터포털 API |
| [jinny-han/vworld-api-mcp](https://github.com/jinny-han/vworld-api-mcp) | 1 | 2026-05-11 | MIT | V-World 공간정보 |
| [yuha933/G-SEED-AI-Agent](https://github.com/yuha933/G-SEED-AI-Agent) | 0 | 2026-07-03 | - | G-SEED 항목 컨설팅 에이전트(참고) |
| [manminkim-eng/Architectural-line](https://github.com/manminkim-eng/Architectural-line) | 0 | 2026-11-12 | - | 건축법 일조 사선 웹(참고) |

검색 결과 **0건**인 검색어: `ECO2 에너지`, `에너지절약계획서`, `제로에너지`(건물 인증용 도구 기준)

### 4.6 Claude Code 스킬·목록

| 저장소 | ★ | 최근 푸시 | 라이선스 | 용도 |
|---|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 194,316 | 2026-11-14 | - | 공식 스킬(문서·스프레드시트·발표자료 등) |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 57,970 | 2026-11-14 | - | Claude Code 자료 모음 |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 47,244 | 2026-11-14 | Apache-2.0 | 공식 플러그인 목록 |
| [anthropics/k12-teacher-skills](https://github.com/anthropics/k12-teacher-skills) | 629 | 2026-10-14 | Apache-2.0 | 교사용 스킬·평가 루브릭 |
| [AlpacaLabsLLC/skills-for-architects](https://github.com/AlpacaLabsLLC/skills-for-architects) | 414 | 2026-11-11 | MIT | 건축·부동산용 Claude Code 스킬 |
| [osama-ata/Awesome-AECO](https://github.com/osama-ata/Awesome-AECO) | 42 | 2026-11-10 | CC0-1.0 | 건설·건축 오픈소스 도구 목록 |
| [MakeItEzzz555/Gridline](https://github.com/MakeItEzzz555/Gridline) | 41 | 2026-11-02 | MIT | 건축·AEC용 에이전트 스킬 |

---

## 5. 도입 순서

| 단계 | 내용 | 필요 조건 | 비용 |
|---|---|---|---|
| 1 | kordoc(HWP)과 korean-law-mcp(법령) 설치, 서류·법규 검토에 사용 | 법제처 Open API 키(무료 신청) | 없음 |
| 1 | DXF → 실별 면적표·방위별 외피 수량 추출 스크립트 | 실제 프로젝트 DXF 1~2건 | 없음 |
| 2 | ECO2 입력표 자동 작성 + 결과 교차검증 | 1단계 스크립트, ECO2 입력 양식 샘플 | 없음 |
| 2 | EPI 자동 채점·검토표 | 에너지절약계획서 양식(HWP/엑셀), 기준 별표 | 없음 |
| 3 | AutoCAD·Rhino·SketchUp 연동(MCP) | **사용하는 PC에서 Claude Code 실행**(Windows) | 없음(소프트웨어 라이선스는 기존 보유분) |
| 3 | EnergyPlus·pvlib 대안 비교, 태양광 자립률 사전 검토 | EnergyPlus 설치, 국내 EPW 기상파일 | 없음 |
| 3 | 수업용 과제 자동 검사·인터랙티브 교재 | 과제 양식과 평가 기준 | 없음 |

---

## 6. 주의사항

- **실행 위치:** AutoCAD·Rhino·Revit·SketchUp·ArchiCAD 연동은 해당 프로그램이 설치된 PC에서 Claude Code를 실행해야 한다. 지금 쓰는 클라우드 세션에서는 DXF·HWP·시뮬레이션 같은 파일 기반 작업만 가능하다.
- **인증 계산의 지위:** 공식 결과는 ECO2다. 자동화는 입력 준비, 검증, 대안 비교까지만 맡는다.
- **법령:** MCP 조회 결과도 시행일과 원문을 대조해야 한다. 2025년 ZEB 통합처럼 제도가 자주 바뀐다.
- **보안:** 고객 도면과 서류를 외부 API(Claude 포함)로 보낼 때는 계약상 비밀유지 조건을 확인한다.
- **라이선스:** ladybug-tools(AGPL-3.0), LibreDWG·pyRevit(GPL-3.0)은 사내 사용에는 문제가 없지만, 수정본을 배포하거나 웹 서비스로 제공하면 소스 공개 의무가 생길 수 있다.
- **성숙도:** ★100 미만 저장소, 특히 국내 건축 특화 저장소는 대부분 2025~2026년에 생긴 초기 프로젝트다. 그대로 쓰기보다 참고용으로 본다.
