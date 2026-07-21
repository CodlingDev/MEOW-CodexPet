# 에셋 출처

## 기준 캐릭터

- 프로젝트: [CodlingDev/MEOW](https://github.com/CodlingDev/MEOW)
- 기준 커밋: `75a45c3ada731cac99e1df5a5bada598d8de64d2`
- 품종: `cat_orange`
- 선정 이유: `CatFactory.makeCat`의 기본 매개변수가 `.orange`이며 MEOW 앱의 기본 캐릭터 정체성을 대표합니다.
- 원본 형식: 투명 배경의 `256 × 256` PNG 픽셀 아트

이 저장소의 `references/cat-orange/`에는 전체 원본 세트 대신 캐릭터의 얼굴, 체형, 줄무늬, 방향성과 대표 동작을 설명하는 최소 프레임만 보존합니다.

## 포함 파일

| 파일 | 용도 | SHA-256 |
| --- | --- | --- |
| `cat_orange_idle_0.png` | 정면 기본 자세 | `403dc3df5741bf2fe9ca67a7eed5bc399be52d7f39a0130c22f85cef3502d828` |
| `cat_orange_idle_1.png` | idle 미세 변화 | `a32f9cec8146216810ac3d6c5ace271ef87e4333bb36019c3aa544901da2503f` |
| `cat_orange_run_0.png` | 오른쪽 이동 실루엣 | `d2a94a938a8675d8aa111490e1ccf204ee9cad4a6907ee1fc93192a3e4c7180d` |
| `cat_orange_run_2.png` | 달리기 보폭 변화 | `b64005909a289021be8017553e67ba89170e5e1576d41907a03db4e7a4bc987b` |
| `cat_orange_jump_3.png` | 점프 자세 | `2bf5a5015179206939282920f2a57252cb23157b4b3c004d392491dd1b57d2db` |
| `cat_orange_play_04.png` | 장난감 상호작용 | `f7b65a9ad1b35f7479a2a299f97f299e3c11f7da333346ea148029ea272843e8` |
| `cat_orange_scratch_2.png` | 앞발 동작과 측면 비율 | `eed8a191fe8a3b97353e5f1f28b07a41e956dcb66b81b1cbef20901eb13b9091` |
| `cat_orange_sleep_0.png` | 낮은 자세와 휴식 표현 | `51c6fe875f20bcc6ff3882a2e29f69e627f747a332d84873933c7365001a09d2` |

## 라이선스

원본과 이 저장소는 MIT License를 사용합니다. 원본 픽셀 아트를 포함하거나 변형한 배포물에는 저장소 루트의 `LICENSE`를 함께 유지합니다.

## 사용 원칙

- 얼굴의 흰색 영역, 주황색 줄무늬, 흰 발, 긴 꼬리와 픽셀 아트 질감을 정체성 고정 요소로 취급합니다.
- Codex 상태를 설명하기 위해 필요한 자세만 확장하며, 로고나 텍스트를 캐릭터에 추가하지 않습니다.
- 생성 결과가 원본 캐릭터와 다른 품종이나 비픽셀 스타일로 변하면 실패로 처리합니다.
