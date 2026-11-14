# plan.json 형식

평면도 판독 결과다. 도면화는 이 파일과 샘플 CAD만 입력으로 받는다.
좌표는 `[x, y]` mm이고, x는 오른쪽, y는 위쪽이 양수다.

모든 요소에 공통으로 붙는 필드:

| 필드 | 값 |
|---|---|
| `source` | `"이미지"` \| `"샘플"` \| `"가정"` |
| `evidence` | 근거. 예: `"하단 치수 3,600"`, `"축척으로 측정"`, `"가정: 내벽 두께 표기 없음"` |
| `confirm` | `null` 또는 `"확인 필요: 사유"` |

## 구조

```json
{
  "meta": {
    "name": "도면명",
    "image": "plan.png",
    "units": "mm",
    "origin": "좌하단 외벽 중심선 교점",
    "scale": {
      "px_per_mm": 0.1234,
      "checks": [{ "dim": "D1", "px": 444.2, "label": 3600, "px_per_mm": 0.1234 }]
    },
    "north_deg": null,
    "unread": ["이미지에서 읽지 못한 것"]
  },
  "dimensions": [
    { "id": "D1", "label": 3600, "p1": [0, 0], "p2": [3600, 0], "ref": "벽 중심선",
      "chain": "하단-1", "offset": -1200, "source": "이미지", "evidence": "하단 치수 3,600", "confirm": null }
  ],
  "walls": [
    { "id": "W1", "start": [0, 0], "end": [3600, 0], "thickness": 200, "type": "외벽",
      "source": "이미지", "evidence": "외벽 두께 200 표기", "confirm": null }
  ],
  "openings": [
    { "id": "O1", "kind": "door", "type": "외여닫이", "wall": "W1", "offset": 600, "width": 900,
      "hinge": "left", "swing_into": "R1", "block": "DOOR_900",
      "source": "이미지", "evidence": "호 기호, 좌측 경첩", "confirm": null }
  ],
  "rooms": [
    { "id": "R1", "name": "거실", "polygon": [[0, 0], [3600, 0], [3600, 4200], [0, 4200]],
      "area_basis": "벽 중심선", "source": "이미지", "evidence": "방 이름 표기", "confirm": null }
  ],
  "fixtures": [
    { "id": "F1", "category": "양변기", "block": "WC_01", "insert": [1200, 300], "rotation": 90,
      "mirror": false, "against_wall": "W5",
      "source": "샘플", "evidence": "위치·방향은 이미지 기호", "confirm": null }
  ],
  "uncertain": [
    { "target": "O3", "reason": "문 기호가 흐려 열림 방향을 판별할 수 없음" }
  ]
}
```

## 필드 정의

| 필드 | 정의 |
|---|---|
| `dimensions[].label` | 이미지에 적힌 숫자(mm). 형상에서 잰 값이 아니다. |
| `dimensions[].ref` | 치수선 끝점이 가리키는 기준: `"벽 중심선"` \| `"벽 외곽"` \| `"내측 마감"` |
| `dimensions[].chain` | 연속 치수 묶음 id. 같은 묶음의 합은 그 방향의 전체 치수와 같아야 한다. |
| `openings[].offset` | 벽 `start`에서 개구부 시작 모서리까지의 거리 |
| `openings[].hinge` | 벽 start→end 방향으로 볼 때 경첩 쪽: `"left"` \| `"right"` \| `null`(미닫이 등) |
| `openings[].swing_into` | 문이 열리는 쪽 방의 id. 외부면 `"외부"`. |
| `openings[].block`, `fixtures[].block` | `sample_inventory.json`의 블록 이름. 샘플에 없으면 `null`이고 `evidence`에 `"샘플 없음"`. |
| `fixtures[].rotation` | 블록 정의의 정면 방향 기준 반시계 회전각(도) |
| `fixtures[].against_wall` | 붙어 있는 벽 id. 떨어져 있으면 `null`. |
| `uncertain` | `confirm`이 있는 요소의 요약 목록. `report.md`와 도면 `확인필요` 레이어의 개수와 같아야 한다. |
