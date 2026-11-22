---
name: eco2
description: ECO2·ECO2-OD 프로젝트 파일(.eco, .ecox, .tpl, .tplx, .ECL2)을 읽어 입력값(외피 면적·방위·열관류율·재료층, 냉난방·조명 설비, 신재생)을 표로 정리하고 도면·창호일람표·기준과 대조한다. 외벽·창 U값과 SHGC를 바꾼 대안 파일을 만들고, ECO2 계산 결과 리포트를 집계해 대안별로 비교한다. "ECO2 파일 검토", "에코2 입력값 확인", "ECL2", "1차에너지소요량 결과 정리", "단열 대안 비교" 요청에 사용.
---

# ECO2 파일 다루기

## 원칙
- **공식 계산은 ECO2 프로그램에서 한다.** 이 스킬은 입력 검토, 대안 파일 준비, 결과 정리만 한다.
- **원본 파일은 덮어쓰지 않는다.**
  - 사본을 쓴다.
  - 새 파일은 별도 폴더에 `<원본이름>_대안N_<바꾼내용>.<확장자>`로 저장한다.
- **대안 파일은 비교용이다. 인증 제출에 쓰지 않는다.** U값을 바꾸면 기존 재료층이 같은 성능의 단일층 하나로 바뀐다.
- 값이 확실하지 않으면 "확인 필요"로 표시한다. 기준값은 `korean-law` MCP나 원문에서 인용한다.

## 도구

| 도구 | 용도 | 필요 조건 |
|---|---|---|
| `python tools/eco2/eco2_table.py list|show|export <파일>` | 입력값을 표·CSV로 보기(읽기 전용). `--section 외피`처럼 구역 지정 | ECO2-OD(.ECL2)는 바로 됨. ECO2(.eco 등)는 eco2 패키지 필요 |
| `eco2 decrypt <파일>` | ECO2 저장 파일을 XML(+헤더 json)로 풀기 | eco2 패키지(beskep/ECO2, MIT) |
| `eco2 encrypt <xml> --extension eco` | XML을 ECO2 저장 파일로 되돌리기 | 〃 |
| `eco2 prune <파일>` | 기상자료 등 공용 정보를 빼고 설계 정보만 추출 | 〃 |
| Python `eco2.editor.Eco2Editor` | U값·SHGC 대안 파일 생성 | 〃 |
| Python `eco2.report` | 결과 리포트(엑셀, batchreport.tab) 집계 | eco2 패키지 + dataframe 추가 설치 |

참고자료(woo-seung/BEM-semantic-debugging, MIT. `references/NOTICE.md`):
- `references/eco2od-modeling-manual.md`: ECO2-OD 부문별 입력 규칙과 흔한 실수
- `references/eco2od-fields.json`: XML 테이블·필드와 화면 이름의 대응

압축 형식(`.ecox`, `.tplx`)을 풀려면 별도 프로그램(MiniLZO.exe)이 필요하다. 그 프로그램이 없으면, 가능한 경우 ECO2에서 압축하지 않은 `.eco` 형식으로 저장한 사본을 쓰게 한다.

## 작업 1. 입력 검토(가장 자주 씀)

1. 파일 경로와 종류를 확인한다. ECO2(주거·비주거 효율등급)인지, ECO2-OD(에너지절약계획서·업무용)인지 확인한다.
2. `eco2_table.py list`로 테이블 목록을 본다. 이어서 `show`로 다음 구역을 표로 정리한다.
   - 외피(면적·방위·부위), 형별성능내역(열관류율·SHGC), 재료층
   - 냉난방·공조·조명 설비, 신재생
3. 근거 자료와 대조한다.
   - 면적: 도면에서 잰다. DWG는 `node tools/dwg/dwgconv.mjs dwg2dxf` 후 측정하고, PC에서는 AutoCAD MCP를 쓴다.
   - 창: 창호일람표(`schedule-extractor` 스킬).
   - 열관류율 기준: 「건축물의 에너지절약설계기준」 별표(지역·부위별)를 `korean-law`로 확인한다.
4. `references/eco2od-modeling-manual.md`의 해당 부문 "주의사항"과 흔한 실수를 하나씩 점검한다.
5. 결과는 이 표로 보고한다.

| 항목 | ECO2 입력값 | 근거 자료 값(출처) | 차이 | 판단(일치·불일치·확인 필요) |
|---|---|---|---|---|

## 작업 2. 대안 파일 만들기(비교용)

사용자가 바꿀 값(예: 외벽 U값 0.15, 창 U값 1.0·SHGC 0.4)을 정하면 다음처럼 만든다.

```python
from eco2.editor import Eco2Editor
ed = Eco2Editor("<원본 사본 경로>")
ed.xml.set_walls(0.15, "외벽(벽체)")              # 대상 부위의 모든 벽체 U값
ed.xml.set_windows(uvalue=1.0, shgc=0.4)         # 외부창 U값과 SHGC
ed.write("<새 폴더>/<원본이름>_대안1_외벽0.15_창1.0.eco", dsr=False)  # 결과부 없이 저장
```

- 부위 이름: `외벽(벽체)`, `외벽(지붕)`, `외벽(바닥)`, `내벽(벽체)`, `내벽(지붕)`, `내벽(바닥)`, `간벽`, `외부창`, `내부창`, `지중벽`
- 결과부를 포함해 저장하면 ECO2에서 불러올 때 오류가 날 수 있다(도구 작성자 안내). `dsr=False`로 저장한다.
- 이 편집기는 ECO2(.eco) 기준으로 만들어졌다. ECO2-OD(.ECL2)에서 쓸 때는 첫 사용 때 결과 파일을 ECO2-OD에서 열어 확인한다.
- 만든 파일은 사용자가 ECO2에서 열어 계산한다. 계산 결과를 저장하면 작업 3으로 집계한다.

## 작업 3. 결과 집계

```python
from eco2.report import GraphReport, BatchReport
g = GraphReport("<ECO2 결과 그래프 엑셀 경로>")
g.yearly      # 연간 요약
g.monthly     # 월별
```

- 대안이 여러 개면 대안별 1차에너지소요량, 등급 관련 값, 항목별(난방·냉방·급탕·조명·환기) 소요량을 한 표로 만든다.
- 리포트 형식이 맞지 않아 오류가 나면 엑셀을 직접 읽어 정리하고, 그 사실을 보고한다.

## 하지 말 것
- 원본 ECO2 파일 덮어쓰기
- 대안 파일을 인증 제출용으로 안내하기
- 계산을 ECO2 없이 했다고 말하기. 이 도구는 계산 엔진이 아니다.
