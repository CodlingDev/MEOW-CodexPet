# 에셋 출처

## 기준 캐릭터

- 프로젝트: [CodlingDev/MEOW](https://github.com/CodlingDev/MEOW)
- 기준 커밋: `75a45c3ada731cac99e1df5a5bada598d8de64d2`
- 품종: `cat_orange`
- 선정 이유: `CatFactory.makeCat`의 기본 매개변수가 `.orange`이며 MEOW 앱의 기본 캐릭터 정체성을 대표합니다.
- 원본 형식: 투명 배경의 `256 × 256` PNG 픽셀 아트

이 저장소의 `references/cat-orange/`에는 최종 아틀라스 조립에 사용하는 5개 상태의 1x 프레임 전체를 보존합니다. 기준 커밋 이후 현재 로컬 MEOW 커밋 `ef5670518c396497ec6741dbce015531fdb8c612`까지 해당 파일에 변경이 없음을 확인했습니다.

## 포함 상태

| 디렉터리 | 프레임 수 | 용도 |
| --- | --- | --- |
| `idle/` | 2 | Codex `running`, `review` |
| `roll/` | 18 | Codex `running-left`, `running-right` |
| `stretch/` | 17 | Codex `waving`, `jumping` |
| `play/` | 12 | Codex `failed`, `waiting` |
| `sleep/` | 4 | Codex `idle`, 방향 고정 셀 |

각 원본 파일의 SHA-256과 실제 사용 슬롯은 [`asset-mapping.json`](../qa/meow/asset-mapping.json)에 기록합니다.

## 라이선스

원본과 이 저장소는 MIT License를 사용합니다. 원본 픽셀 아트를 포함하거나 변형한 배포물에는 저장소 루트의 `LICENSE`를 함께 유지합니다.

## 사용 원칙

- 원본의 보이는 RGBA 픽셀을 리샘플링하거나 다시 그리지 않습니다.
- 256×256 캔버스에서 고정 영역만 잘라 192×208 셀에 배치합니다.
- 사용자가 승인한 `running-right` 수평 반전 외에는 기하 변환하지 않습니다.
- 생성 이미지, 로고, 텍스트, 장식 효과를 추가하지 않습니다.
