# MEOW Codex Pet v2 QA 보고서

## 결론

MEOW 기본 주황 고양이의 원본 1x PNG만으로 조립한 Codex Pet v2 아틀라스가 lossless 픽셀 왕복과 구조 검증을 통과했습니다.

## 최종 결과

| 항목 | 결과 |
| --- | --- |
| 아틀라스 크기 | `1536 × 2288` |
| 레이아웃 | 8열 × 11행, 셀 `192 × 208` |
| 스프라이트 규격 | `spriteVersionNumber: 2` |
| 원본 에셋 | MEOW `cat_orange` 1x PNG 53장 |
| 새 그림 생성 | 없음 |
| 리사이즈 | 없음 |
| 기하 변환 | `running-right` 수평 반전만 적용 |
| `idle` 체감 속도 | 3개 자세 장기 유지, 자세 변경 절반 수준 |
| `roll` 체감 속도 | 주기당 자세 변경 8회 → 5회, 약 1.6배 감소 |
| 앉은 `idle` 체감 속도 | 두 자세를 각각 3칸 유지해 빠른 교차 출력 제거 |
| `stretch` 반복 노출 | 완전히 늘어난 구간의 미세 동작으로 반복 폭 축소 |
| 방향 반응 | 없음, 16개 셀 모두 `sleep_0` |
| WebP 픽셀 왕복 | 통과 |
| 투명 RGB 잔여 픽셀 | 0 |
| 프레임 구조 검사 | 오류 0, 경고 0 |
| 독립 최종 시각 QA | `pass`, findings 없음 |
| WebP SHA-256 | `890e4a5c19156c8a0235dc23bc88d2976d9e8839f8195af1ae54fcb2c9b1e3d7` |

## 프레임 구성

- `sleep`: `idle`과 방향 고정 셀
- `roll`: 왼쪽 원본, 오른쪽 수평 반전
- `stretch`: `waving`, `jumping`
- `play`: 사용자 상호작용이 필요한 `failed`, `waiting`
- `idle`: `running`, `review`

각 행의 선택 인덱스와 원본 체크섬은 [`asset-mapping.json`](../qa/meow/asset-mapping.json)에 기록했습니다. 재생속도 조정은 Codex 앱 런타임을 변조하지 않고 원본 프레임을 중복하는 방식이며, 실제 상태 지속시간은 바뀌지 않습니다.

## 검증 명령

```bash
make PYTHON=/Users/don/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 qa
```

결과:

- `scripts/build_pet_atlas.py`: 성공
- `validate_atlas.py --require-v2`: `ok: true`
- `make_contact_sheet.py`: 성공
- `make_direction_qa_sheet.py`: 성공
- `render_animation_previews.py`: 9개 GIF 생성 성공

## QA 산출물

- [`asset-mapping.json`](../qa/meow/asset-mapping.json): 원본 상태, 선택 인덱스, 체크섬과 반전 여부
- [`validation-extended.json`](../qa/meow/validation-extended.json): v2 구조와 투명도 검증
- [`transparency.json`](../qa/meow/transparency.json): 원본 알파 보존과 hidden RGB 정리 결과
- [`contact-sheet-extended.png`](../qa/meow/contact-sheet-extended.png): 11개 행 전체 contact sheet
- [`look-directions.png`](../qa/meow/look-directions.png): 방향 16칸이 동일한 프레임인지 확인
- [`previews/`](../qa/meow/previews/): 9개 표준 상태 GIF
- [`review.json`](../qa/meow/review.json): 원본 및 조립 불변식 검사
- [`final-visual-qa.txt`](../qa/meow/final-visual-qa.txt): 독립 시각 검토 결과
