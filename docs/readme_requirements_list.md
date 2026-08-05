# 📋 README.md 작성 및 포함 요구사항 종합 명세서

> 본 문서는 [reference.md](file:///home/jmlee/Project/second-project/docs/reference.md) 및 [learning_guide.md](file:///home/jmlee/Project/second-project/docs/learning_guide.md)를 바탕으로, 학습자가 **`README.md`에 반드시 작성하고 증명해야 하는 모든 요구항목**을 객관적 근거(원문 라인 참조)와 함께 완벽히 리스트업한 문서입니다.

---

## 1. README.md 6대 필수 작성 항목 (Mandatory Sections)

`docs/reference.md` (Lines 50-56, 158-166, 323-329) 및 `docs/learning_guide.md` (Step 5-7)에서 요구하는 `README.md` 핵심 6대 항목 명세입니다.

### ① 프로젝트 개요 (Project Overview)
- **근거**: `reference.md` Line 51, 160 / `learning_guide.md` Line 1342-1344
- **작성 내용**:
  - 무엇을 만드는 프로그램인지 2~3줄 요약 (Python 3.10+ 기반 터미널 콘솔 4지선다 퀴즈 게임).
  - 학습 목표: Python 기본 문법, OOP(클래스), 파일 입출력(JSON 영속성), Git 워크플로우를 실제 작동하는 완성형 프로그램으로 대변함.

### ② 퀴즈 주제 및 선정 이유 (Quiz Subject & Selection Rationale)
- **근거**: `reference.md` Line 39, 52, 116-118, 161 / `learning_guide.md` Line 176-206, 1346-1350
- **작성 내용**:
  - 학습자가 직접 선택한 주제 명시 (가이드 기준: **자료구조 - Data Structure**).
  - 주제 선정 이유를 명확한 근거와 함께 서술:
    1. 4지선다에 적합한 명확하고 객관적인 정답 체계.
    2. 프로그램 내부 자료구조(`list`, `dict`)와 주제(스택, 큐, 해시 테이블 등) 간의 상호 연결성.
    3. 기초 컴퓨터 과학 지식으로서의 영속적 가치.
  - 기본 제공 퀴즈 최소 5개 이상 명시 (문제, 선택지 4개, 정답 1~4).

### ③ 실행 방법 (Execution Guide)
- **근거**: `reference.md` Line 53, 162, 191-192 / `learning_guide.md` Line 289-293, 1352-1357
- **작성 내용**:
  - 시스템 요구사항: **Python 3.10 이상** (외부 라이브러리 설치 불필요, 파이썬 표준 라이브러리만 활용).
  - 저장소 클론 및 실행 명령:
    ```bash
    git clone https://github.com/<사용자ID>/<저장소명>.git
    cd <저장소명>
    python main.py
    ```

### ④ 기능 목록 (Feature List)
- **근거**: `reference.md` Line 36-40, 54, 83-157, 163 / `learning_guide.md` Line 1359-1366
- **작성 내용**:
  - 프로그램 메뉴 5종 및 동작 설명 표:
    1. **퀴즈 풀기**: 저장된 퀴즈 출제, 정답/오답 판정 및 해설, 100점 만점 환산, 최고 점수 비교 및 갱신. (퀴즈 0개 시 예외 처리)
    2. **퀴즈 추가**: 문제, 선택지 4개, 정답 번호 유효성 입력받아 추가 후 즉시 `state.json` 파일 저장.
    3. **퀴즈 목록**: 등록된 전체 퀴즈 번호 및 문제 조회. (퀴즈 0개 시 예외 처리)
    4. **점수 확인**: 최고 점수 조회. (미풀이/미기록 상태 구분 안내)
    5. **종료**: 현재 상태 저장 후 프로그램 안전 종료.

### ⑤ 파일 구조 및 클래스 설계 (File Structure & Class Architecture)
- **근거**: `reference.md` Line 41-44, 55, 108-114, 144-148, 164, 198-200 / `learning_guide.md` Line 1368-1382
- **작성 내용**:
  - 프로젝트 전체 디렉토리 트리 시각화:
    ```
    second-project/
    ├── main.py                  # 진입점 및 안전 종료(KeyboardInterrupt/EOFError)
    ├── quiz.py                  # Quiz 클래스 (문제 1개 표현 및 dict 변환)
    ├── quiz_game.py             # QuizGame 클래스 (게임 흐름 및 입력 검증)
    ├── storage.py               # state.json 파일 입출력 및 복구 (또는 main.py 통합)
    ├── state.json               # 데이터 파일 (git 제외/포함 선택 사유 기재)
    ├── .gitignore               # 추적 제외 설정
    ├── README.md                # 종합 안내 문서
    └── docs/                    # 참고 문서 및 스크린샷
        ├── reference.md
        ├── learning_guide.md
        └── screenshots/
    ```
  - **최소 2개 이상의 클래스 역할 명시**:
    - `Quiz`: 문제(question), 선택지 4개(choices), 정답 번호(answer) 속성을 관리하고, JSON ↔ 객체 간 `to_dict()`/`from_dict()` 변환 제공.
    - `QuizGame`: 퀴즈 목록, 최고 점수 관리, 메뉴 루프, 입력 예외 처리(`ask_int`, `ask_text`), 파일 저장/불러오기 통합 관리.

### ⑥ 데이터 파일 설명 (`state.json` Specification)
- **근거**: `reference.md` Line 40, 44, 56, 149-157, 165, 195-197, 310-322 / `learning_guide.md` Line 1384-1414
- **작성 내용**:
  - **파일 경로**: 프로젝트 루트 `./state.json` (`Path(__file__).resolve().parent / "state.json"` 활용으로 실행 위치 독립성 보장)
  - **인코딩**: UTF-8 (`ensure_ascii=False` 설정으로 한글 원본 저장)
  - **데이터 스키마 JSON 예시 및 필드 설명**:
    ```json
    {
      "quizzes": [
        {
          "question": "스택(Stack)의 자료 처리 방식은?",
          "choices": ["FIFO (선입선출)", "LIFO (후입선출)", "우선순위 순", "무작위 접근"],
          "answer": 2
        }
      ],
      "best_score": 80,
      "best_correct": 4,
      "best_total": 5
    }
    ```
  - **예외 처리 및 자동 복구 메커니즘 설명**:
    - **첫 실행 (파일 없음)**: `FileNotFoundError` 시 코드 내 내장된 기본 퀴즈 5개로 자동 생성 및 로딩.
    - **파일 손상 / 읽기 실패**: `json.JSONDecodeError`, `KeyError`, `ValueError`, `OSError` 발생 시 사용자 안내 메시지 출력 후 `state.json.bak` 백업 및 기본 퀴즈 데이터로 안전 복구.
  - **.gitignore 처리 여부 및 이유**: `state.json`을 `.gitignore`에 등록하여 동적 실행 데이터가 Git 변경 이력을 더럽히지 않도록 조치함 (또는 커밋 선택 시 이유 명시).

---

## 2. README.md에 포함되어야 하는 시각적 증빙 (Screenshots Checklist)

`reference.md` (Lines 212-214, 330-334) 및 `learning_guide.md` (Line 1415-1419, 1665)에 따른 마크다운 이미지 링크(`![alt](docs/screenshots/...)`) 포함 목록입니다.

| 스크린샷 파일명 | 증명해야 하는 문제 및 내용 | 위치 / 비고 |
|---|---|---|
| `docs/screenshots/env_setup.png` | **개발 환경 설정**: Python 3.10+ 버전 확인(`python --version`), Git 설치 및 `git config --global user.email` 설정 화면 | 제출 필수 |
| `docs/screenshots/menu.png` | **메인 메뉴 화면**: 1~5번 메뉴 출력 및 저정 데이터 로딩 안내 문구 | README 이미지 링크 |
| `docs/screenshots/play.png` | **퀴즈 풀기 및 결과**: 문제출제, 사용자 정답 입력, 정/오답 판정, 100점 환산 결과 및 최고 점수 갱신 축하 문구 | README 이미지 링크 |
| `docs/screenshots/add_quiz.png` | **퀴즈 추가**: 새로운 문제, 선택지 4개, 정답 번호 입력 및 성공 메시지 | README 이미지 링크 |
| `docs/screenshots/score.png` | **점수 확인**: 저장된 최고 점수 및 상세 정답 문제 수 표시 (또는 미풀이 안내) | README 이미지 링크 |
| `docs/screenshots/git_graph.png` | **Git 히스토리 검증**: `git log --oneline --graph --all` 명령어 실행 결과 (최소 10개 이상의 의미 있는 커밋, 기능 브랜치 생성 및 `--no-ff` 병합 그래프) | 제출/증빙 필수 |

---

## 3. README.md 및 저장소에서 입증해야 하는 기능 및 예외 처리 항목 (Verification Grid)

`README.md` 내의 "기능 목록" 및 "트러블슈팅/특징" 란에 반드시 포함되어 입증되어야 하는 세부 문제/조건들입니다.

### A. 공통 입력 및 예외 처리 검증 항목 (`reference.md` Lines 97-107)
1. **공백 자동 제거**: `"  1  "` 입력 시 공백 제거 후 정상 1번 처리.
2. **숫자 변환 실패**: `"abc"`, `"1.5"` 입력 시 경고 메시지 출력 후 재입력 루프 복귀.
3. **허용 범위 밖 입력**: 메뉴 `9`, `0`, `-1` 등 입력 시 안내 메시지 후 재입력 루프 복귀.
4. **빈 입력 (Enter)**: 입력 없이 Enter 입력 시 안내 메시지 후 재입력 루프 복귀.
5. **강제 종료 신호 안전 처리**: `Ctrl+C`(`KeyboardInterrupt`), `EOFError` 발생 시 파이썬 에러 트레이스백 없이 "안전 종료 메시지 + 가능한 범위 저장" 수행.
6. **데이터 파일 손상/부재 대응**: 파일 없거나 손상 시 프로그램이 비정상 종료하지 않고 기본 데이터로 복구 실행.

### B. Git 워크플로우 요구사항 (`reference.md` Lines 45-49, 77-83, 201-209, 209)
1. **필수 7종 Git 명령어 사용 기록**: `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone` (및 `merge`) 1회 이상 사용.
2. **커밋 수 및 컨벤션**: 최소 **10개 이상**의 의미 있는 커밋 (`Feat:`, `Fix:`, `Docs:`, `Refactor:`, `Chore:`).
3. **브랜치 전략**: `main` 외 기능 브랜치(`feat/play-quiz` 등) 생성 후 `--no-ff` 옵션으로 merge 한 이력 그래프.
4. **원격 저장소 동기화**: `clone` 및 `pull` 실습을 통한 복제본과 원본 디렉토리 간 변경 사항 반영 증명.

---

## 4. 선택 구현 (보너스 과제) 명시 항목 (Bonus Tasks if Implemented)

보너스 기능(Lines 173-188)을 구현한 경우 `README.md` 기능 목록에 추가 기재해야 하는 항목입니다.
- **랜덤 출제**: `random.shuffle()` 활용 출제 순서 섞기.
- **문제 수 선택**: 푼 문제 개수 지정 풀기.
- **힌트 기능**: 힌트 보기 옵션 및 점수 감점 로직.
- **퀴즈 삭제**: 기존 퀴즈 삭제 및 `state.json` 즉시 반영.
- **점수 기록 히스토리**: 날짜/시간, 푼 문제 수, 점수 다중 기록 (`history` 키 스키마 마이그레이션).

---

## 5. README.md 제출 전 최종 체크리스트 (Submission Checklist)

- [ ] GitHub 저장소가 **Public** 상태로 공개되어 있는가?
- [ ] README.md의 6대 필수 영역이 빠짐없이 작성되었는가?
- [ ] 실행 방법 안내대로 `python main.py` 실행 시 외부 패키지 오류 없이 작동하는가?
- [ ] `state.json` 스키마 및 예외 복구(파일 없음/손상) 설명이 서술되어 있는가?
- [ ] 이미지 4종 이상의 스크린샷 마크다운 링크가 GitHub 웹페이지에서 정상 표시되는가?
- [ ] `git log --oneline --graph` 결과에서 10개 이상의 커밋과 브랜치 병합 흔적이 보이는가?
