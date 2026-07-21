# MEOW Codex Pet v2 QA 보고서

## 결론

MEOW 기본 주황 고양이로 제작한 Codex Pet v2 아틀라스가 구조 검증, chroma despill, 3인 블라인드 방향 판독과 독립 시각 QA를 통과했습니다.

## 최종 결과

| 항목 | 결과 |
| --- | --- |
| 아틀라스 크기 | `1536 × 2288` |
| 레이아웃 | 8열 × 11행, 셀 `192 × 208` |
| 스프라이트 규격 | `spriteVersionNumber: 2` |
| 표준 상태 | 9개 행 통과 |
| 시선 방향 | 16개, 시계 방향 22.5도 간격 |
| 투명 RGB 잔여 픽셀 | 0 |
| Chroma despill | `ok: true`, alpha 보존 |
| 프레임 구조 검사 | 오류 0, 경고 0 |
| 블라인드 방향 검사 | `ok: true`, 하드 게이트 4방향 통과 |
| 독립 최종 시각 QA | `pass` |
| WebP SHA-256 | `600dd9ecb88c2ac651719b908a4305c4be7841c64f9af153ef4e6065667d6f9d` |

## 방향 보정

첫 블라인드 검사에서는 270도가 뒷모습처럼 읽히고 0도와 180도의 위·아래 차이가 약해 하드 게이트를 통과하지 못했습니다. 표준 9개 상태는 유지하고 방향 2개 행만 다시 제작했습니다.

- 0도: 눈선과 주둥이를 들어 명확한 위 방향으로 보정했습니다.
- 180도: 턱과 눈을 가슴 쪽으로 내려 명확한 아래 방향으로 보정했습니다.
- 270도: 흰 볼, 한쪽 눈과 코가 보이는 완전한 왼쪽 프로필로 보정했습니다.
- 270도 주변: 꼬리와 몸통 폭을 안쪽으로 줄여 최종 셀 가장자리 검사를 통과했습니다.

보정 후 격리된 리뷰어 3명이 90도/270도와 0도/180도 하드 게이트를 모두 같은 방향으로 판독했습니다.

## 승인된 경고

얕은 중간 각도 일부는 무라벨 단일 이미지에서 수평 또는 수직 축이 모호하다는 경고가 남았습니다. 라벨이 있는 정상 크기 순환에서는 모든 프레임이 의도한 사분면을 유지하고 역전이 없었으며, 독립 최종 시각 QA도 눈에 띄는 크기 튐이나 실루엣 단절이 없다고 판정했습니다.

연속성 수치 경고도 동일한 기준으로 검토했습니다. 알파 홀, 잘림, 잘못된 방위, 캐릭터 정체성 변화는 없습니다. 승인 근거는 [`blind-review-resolution.json`](../qa/meow/blind-review-resolution.json)에 보존합니다.

## QA 산출물

- [`validation-extended.json`](../qa/meow/validation-extended.json): v2 구조와 투명도 검증
- [`chroma-despill-extended.json`](../qa/meow/chroma-despill-extended.json): 단일 despill 결과
- [`contact-sheet-extended.png`](../qa/meow/contact-sheet-extended.png): 11개 행 전체 접촉표
- [`look-directions.png`](../qa/meow/look-directions.png): 중립 상태와 16방향 비교표
- [`direction-blind-validation.json`](../qa/meow/direction-blind-validation.json): 3인 블라인드 다수결 결과
- [`direction-semantics.json`](../qa/meow/direction-semantics.json): 방향별 의미 판정
- [`look-continuity.json`](../qa/meow/look-continuity.json): 인접 방향 연속성 수치
- [`previews/`](../qa/meow/previews/): 9개 표준 상태 GIF
- [`run-summary.json`](../qa/meow/run-summary.json): 최종 실행 요약

## 설치 확인

저장소 패키지와 `/Users/don/.codex/pets/meow` 설치본의 `spritesheet.webp` SHA-256을 비교해 동일함을 확인했습니다. `pet.json`은 `id: meow`, `spriteVersionNumber: 2`, `spritesheetPath: spritesheet.webp`를 사용합니다.
