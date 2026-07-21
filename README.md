# MEOW Codex Pet

macOS용 [MEOW](https://github.com/CodlingDev/MEOW)의 기본 주황 고양이 에셋을 Codex용 애니메이션 펫으로 확장하는 프로젝트입니다.

원본 픽셀 아트의 얼굴, 체형, 줄무늬, 색상과 움직임을 기준으로 삼고, Codex가 작업 중이거나 사용자 응답을 기다리는 상태를 같은 캐릭터 언어로 표현합니다.

## 목표

- MEOW의 기본 품종인 `cat_orange` 정체성을 보존합니다.
- Codex Pet v2의 9개 표준 상태와 16개 시선 방향을 지원합니다.
- 생성, 조립, 검증, 설치 과정을 재현 가능하게 기록합니다.
- 최종 펫과 QA 산출물을 저장소에서 함께 관리합니다.

## Codex Pet v2 규격

| 항목 | 값 |
| --- | --- |
| 셀 크기 | `192 × 208` |
| 아틀라스 | 8열 × 11행 |
| 최종 크기 | `1536 × 2288` |
| 표준 상태 | `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review` |
| 시선 방향 | 12시 방향부터 시계 방향으로 22.5도 간격, 총 16개 |
| 매니페스트 | `spriteVersionNumber: 2` |

행별 의미와 필수 검증 기준은 [Codex Pet v2 제작 기준](docs/CODEX_PET_V2.md)에 정리합니다.

## 원본 에셋

`CatFactory.makeCat`의 기본 품종인 `.orange`를 기준 캐릭터로 사용합니다. 원본 저장소의 추적된 1x PNG 중 정체성과 대표 동작을 설명하는 프레임만 `references/cat-orange/`에 복사했습니다.

- 기준 원본: `CodlingDev/MEOW`
- 기준 커밋: `75a45c3ada731cac99e1df5a5bada598d8de64d2`
- 원본 해상도: `256 × 256`, 알파 채널 포함
- 라이선스와 체크섬: [에셋 출처](docs/ASSET_PROVENANCE.md)

## 프로젝트 구조

```text
MEOW-CodexPet/
├── docs/                    # 규격, 출처, 제작 및 검증 기록
├── references/cat-orange/   # MEOW 원본 기준 프레임
├── pets/meow/               # 배포 가능한 pet.json과 spritesheet.webp
└── qa/meow/                 # 최종 검증 결과와 시각 QA 산출물
```

생성 도중의 프롬프트, 행 스트립, 추출 프레임과 중간 아틀라스는 `.hatch/`에서 작업하며 Git에 포함하지 않습니다.

## 개발 흐름

1. `references/cat-orange/`의 프레임으로 캐릭터 정체성을 고정합니다.
2. Codex의 `hatch-pet`과 `imagegen` 워크플로로 기준 이미지와 상태별 행을 제작합니다.
3. 9개 표준 상태를 먼저 검증한 뒤 4개 방위 기준과 16개 시선 방향을 제작합니다.
4. `1536 × 2288` WebP 아틀라스를 조립하고 chroma despill, v2 구조, 시선 의미와 연속성을 검증합니다.
5. 통과한 결과만 `pets/meow/`와 `qa/meow/`에 반영합니다.

## 현재 상태

- [x] 원본 저장소 및 Git 전략 초기화
- [x] 기본 품종과 기준 에셋 선정
- [ ] 기준 캐릭터 이미지 확정
- [ ] 9개 표준 상태 제작
- [ ] 16개 시선 방향 제작
- [ ] v2 아틀라스 검증 및 패키징

## Git 전략

### 태그 컨벤션

- `init`: 가장 처음 Initial Commit에 태그를 붙일 때 사용합니다.
- `feat`: 새로운 기능을 구현할 때 사용합니다.
- `fix`: 버그나 오류를 해결할 때 사용합니다.
- `docs`: README, 템플릿 등 프로젝트 문서를 수정할 때 사용합니다.
- `setting`: 프로젝트 관련 설정을 변경할 때 사용합니다.
- `add`: 사진 등 에셋이나 라이브러리를 추가할 때 사용합니다.
- `refactor`: 기존 코드를 리팩터링하거나 수정할 때 사용합니다.
- `chore`: 중요도가 낮은 단순 수정에 사용합니다.

### 커밋 컨벤션

태그는 반드시 소문자로 작성합니다. 내용은 한글 명령조로 작성하고, 제목은 50자를 넘기지 않습니다. 설명이 필요한 경우 commit description에 작성합니다.

```text
[feat] 로그인 기능 구현
```

### 브랜치 컨벤션

```text
태그/#이슈번호-작업하는파일
```

예시:

```text
feat/#1-loginUI
```

### 브랜치 전략

- `main`: 출시(release)에 사용하는 브랜치입니다.
- `develop`: 개발된 기능을 최종적으로 합쳐 확인하는 기본 브랜치입니다.
  - 개인 브랜치의 작업이 끝나면 개인 브랜치에서 최신 `develop`을 먼저 병합합니다.
  - 충돌과 검증을 마친 뒤 `develop`을 대상으로 Pull Request를 요청합니다.
- `feature`: 태그를 붙이는 모든 작업 브랜치를 의미합니다. 기능 개발, 버그 수정, 문서와 설정 변경은 반드시 작업 브랜치에서 진행합니다.
