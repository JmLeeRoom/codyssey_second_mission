# 🎯 터미널 퀴즈 게임 만들기 — 학습 및 실습 가이드

> Python 기초 · 클래스(OOP) · 파일 입출력(JSON) · Git/GitHub 워크플로우를
> **하나의 완성된 프로그램**을 만들며 익히는 40시간 미션 실습서입니다.

---

## 📖 이 문서 사용법

| 표기 | 의미 |
|---|---|
| 🧠 **개념** | 코드를 쓰기 전에 반드시 이해하고 넘어가야 할 내용 |
| 🏗️ **설계 힌트** | 클래스/메서드 뼈대와 처리 흐름. **완성 코드가 아닙니다.** 직접 채우세요 |
| 💻 **직접 해보기** | 손으로 타이핑해서 구현하는 구간 |
| 🔀 **Git 체크포인트** | 지금 실행해야 할 Git 명령어와 커밋 메시지 |
| ✅ **Step 검증 체크리스트** | 다음 Step으로 넘어가기 전 통과해야 하는 조건 |

> [!IMPORTANT]
> 이 가이드는 **정답 코드를 통째로 주지 않습니다.**
> 뼈대와 흐름만 제공하고 빈칸은 여러분이 채웁니다. 막히면 아래 순서로 해결하세요.
> 1. 해당 Step의 🧠 개념 다시 읽기 → 2. 🏗️ 설계 힌트의 주석(`# TODO`) 다시 읽기 → 3. [부록 A: 자주 겪는 오류](#부록-a-자주-겪는-오류와-해결법) 확인 → 4. 그래도 안 되면 검색/질문

> [!TIP]
> **문서를 처음부터 끝까지 읽고 시작하지 마세요.** Step 0부터 순서대로, 한 Step씩 코드를 돌려보며 진행하는 것이 이 미션의 핵심입니다.
> 소요 시간 가이드: Step 0(1h) → Step 1(3h) → Step 2(5h) → Step 3(7h) → Step 4(6h) → Step 5(7h) → Step 6(2h) → 마무리/문서(3h)

---

## 목차

1. [프로젝트 개요 & 학습 목표](#1-프로젝트-개요--학습-목표)
2. [Step 0. 개발 환경 설정 & Git 저장소 초기화](#step-0-개발-환경-설정--git-저장소-초기화)
3. [Step 1. 개별 퀴즈 모델 구현 (`Quiz` 클래스)](#step-1-개별-퀴즈-모델-구현-quiz-클래스)
4. [Step 2. 메뉴 시스템 및 예외 처리 (`QuizGame` 기초)](#step-2-메뉴-시스템-및-예외-처리-quizgame-기초)
5. [Step 3. 브랜치를 활용한 퀴즈 풀기 기능](#step-3-브랜치를-활용한-퀴즈-풀기-기능)
6. [Step 4. 퀴즈 추가 · 목록 조회 · 점수 확인](#step-4-퀴즈-추가--목록-조회--점수-확인)
7. [Step 5. 데이터 영속성(`state.json`)과 파일 손상 복구](#step-5-데이터-영속성statejson과-파일-손상-복구)
8. [Step 6. 원격 저장소 복제(clone) & 가져오기(pull) 실습](#step-6-원격-저장소-복제clone--가져오기pull-실습)
9. [Step 7. 보너스 과제 (선택)](#step-7-보너스-과제-선택)
10. [최종 검증 & 제출 체크리스트](#최종-검증--제출-체크리스트)
11. [부록 A. 자주 겪는 오류와 해결법](#부록-a-자주-겪는-오류와-해결법)
12. [부록 B. Git 명령어 치트시트](#부록-b-git-명령어-치트시트)
13. [부록 C. 커밋 로드맵 전체 표](#부록-c-커밋-로드맵-전체-표)
14. [부록 D. 학습 목표 자가 점검 질문](#부록-d-학습-목표-자가-점검-질문)

---

# 1. 프로젝트 개요 & 학습 목표

## 1-1. 무엇을 만드나요?

터미널(콘솔)에서 동작하는 **나만의 주제 퀴즈 게임**을 만듭니다.

```
========================================
        🎯 나만의 퀴즈 게임 🎯
========================================
📂 저장된 데이터를 불러왔습니다. (퀴즈 6개, 최고점수 80점)
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================
선택:
```

## 1-2. 최종 제출물 2가지

| 제출물 | 만족해야 할 조건 |
|---|---|
| **Python 콘솔 프로그램 1개** | 메뉴 5종 동작 · 최소 2개 클래스(`Quiz`, `QuizGame`) · 내 주제 퀴즈 5개 이상 · 프로그램을 껐다 켜도 데이터 유지(`state.json`) |
| **GitHub 저장소 1개** | 의미 있는 커밋 10개 이상 · 브랜치 생성/병합 1회 이상 · `clone`/`pull` 각 1회 이상 · README 6대 항목 포함 |

> [!NOTE]
> **"동작하는 프로그램"과 "문법을 아는 것"은 전혀 다른 경험입니다.**
> 이 미션의 진짜 목표는 퀴즈 게임 자체가 아니라, *처음부터 끝까지 혼자 완성해 본 경험*과 *그 과정을 Git으로 기록하는 습관*입니다.

## 1-3. 학습 완료 후 스스로 설명할 수 있어야 하는 것

<details>
<summary><b>📌 Python 기초 (펼쳐보기)</b></summary>

- 변수가 무엇이고 왜 사용하는가
- `int`, `str`, `bool`, `list`, `dict`의 차이
- `if/elif/else`로 조건 분기하기
- `for`와 `while`의 차이, 그리고 언제 무엇을 고르는가
- 함수 정의, 매개변수와 반환값

</details>

<details>
<summary><b>📌 클래스와 객체 (펼쳐보기)</b></summary>

- 클래스가 무엇이고 왜 사용하는가
- `__init__` 메서드와 `self`의 역할
- 속성(attribute)과 메서드(method)의 차이

</details>

<details>
<summary><b>📌 파일 입출력 (펼쳐보기)</b></summary>

- 파일을 열고/읽고/쓰는 기본 과정 (`open`, `with`)
- JSON 형식이 무엇이고 왜 데이터 저장에 쓰는가
- `try/except`로 오류를 처리하는 방법

</details>

<details>
<summary><b>📌 Git 기초 (펼쳐보기)</b></summary>

- Git이 무엇이고 왜 필요한가
- `init` / `add` / `commit` / `push` / `pull` / `checkout` / `clone` 각각의 역할
- 브랜치를 만들고 병합하는 방법
- 원격 저장소를 clone하고 pull로 변경사항 가져오기

</details>

👉 각 항목에 대한 구체적 자가 점검 질문은 **[부록 D](#부록-d-학습-목표-자가-점검-질문)** 에 있습니다. 미션이 끝나면 반드시 풀어보세요.

## 1-4. 전체 로드맵 한눈에 보기

```
Step 0  환경설정 + git init/add/commit/push  ────────────► main
Step 1  Quiz 클래스 + 기본 퀴즈 5개          ────────────► main
Step 2  메뉴 + 공통 입력/예외 처리            ────────────► main
Step 3  퀴즈 풀기 (브랜치 작업)  ──► feat/play-quiz ──merge──► main
Step 4  퀴즈 추가 / 목록 / 점수 확인          ────────────► main
Step 5  state.json 저장·불러오기·손상 복구     ────────────► main
Step 6  clone → 수정 → push → pull 실습       ────────────► main
Step 7  (선택) 보너스 기능
```

---

# Step 0. 개발 환경 설정 & Git 저장소 초기화

> 🎯 **이 Step의 목표**: 코드를 한 줄도 쓰기 전에 "기록할 수 있는 상태"를 먼저 만든다.

## 0-1. Python 버전 확인 (3.10 이상 필수)

```bash
# macOS / Linux
python3 --version

# Windows (PowerShell 또는 cmd)
python --version
py -3 --version
```

`Python 3.10.0` 이상이 출력되어야 합니다.

> [!WARNING]
> `Python 2.7.x`가 나오거나 "명령을 찾을 수 없습니다"가 나오면 아직 설치/PATH 설정이 안 된 것입니다.
> [python.org/downloads](https://www.python.org/downloads/)에서 설치하고, Windows는 설치 화면의 **"Add python.exe to PATH"** 체크박스를 꼭 켜세요.

## 0-2. Git 설치 및 신원 설정

```bash
git --version                                   # 설치 확인
git config --global user.name  "홍길동"          # 커밋에 기록될 이름
git config --global user.email "you@example.com" # GitHub 가입 이메일과 동일하게!
git config --global init.defaultBranch main     # 기본 브랜치를 main으로
git config --global --list                      # 설정 확인
```

> [!IMPORTANT]
> `user.email`을 GitHub 계정 이메일과 다르게 설정하면 커밋이 내 프로필에 연결되지 않습니다(잔디가 안 심어집니다).
> 지금 확인하고 넘어가세요.

📸 **스크린샷 1 촬영**: `python --version` + `git --version` + `git config --global --list` 출력 화면 → `docs/screenshots/env_setup.png`

## 0-3. 퀴즈 주제 정하기 — **자료구조(Data Structure)**

README에 **"주제 선정 이유"** 를 써야 하므로, 코딩 전에 먼저 정합니다.
이 가이드는 **자료구조**를 주제로 진행합니다.

> [!NOTE]
> **왜 자료구조인가요?** (README의 "주제 선정 이유"에 그대로 쓸 수 있는 근거)
> - **정답이 하나로 딱 떨어집니다.** "스택은 LIFO다"처럼 논란의 여지가 없어 4지선다에 가장 알맞습니다.
> - **지금 만드는 프로그램 자체가 자료구조로 되어 있습니다.** 퀴즈 목록은 `list`,
>   퀴즈 한 개는 `dict`로 저장합니다. 문제를 만들면서 내 코드를 다시 보게 됩니다.
> - **오래 쓰이는 지식입니다.** 어떤 언어로 넘어가도 스택·큐·해시 테이블은 그대로 통합니다.
>
> 물론 다른 주제를 골라도 됩니다. 그때는 아래 예시의 퀴즈 내용만 바꾸면 나머지는 전부 동일합니다.

출제할 만한 세부 영역입니다. 이 중에서 **5개 이상**을 골라 문제를 만드세요.

| 세부 영역 | 물어보기 좋은 것 |
|---|---|
| 스택 / 큐 | LIFO·FIFO 동작 방식, 대표 사용 예(함수 호출 스택, 대기열) |
| 배열 / 연결 리스트 | 임의 접근 vs 중간 삽입·삭제의 장단점 |
| 해시 테이블 | 평균 탐색 속도, 파이썬 `dict`의 내부 구조 |
| 트리 / 이진 탐색 트리 | 중위 순회 결과, 루트·리프 같은 용어 |
| 힙 / 우선순위 큐 | 최소 힙의 루트에 오는 값 |
| 그래프 탐색 | DFS는 스택, BFS는 큐 |
| 시간 복잡도 | `O(1)`, `O(log n)`, `O(n)`의 의미와 대표 연산 |

> [!TIP]
> **정답이 명확하게 하나로 떨어지는 문제**를 만드세요.
> "가장 좋은 자료구조는?" 같은 주관적 문제나 "리스트는 빠른가?"처럼 조건에 따라 답이 달라지는
> 문제는 피합니다. `"파이썬 리스트에서 lst[3] 접근의 시간 복잡도는?"` 처럼 조건을 못 박으세요.
>
> 지금 메모장에 **문제 5개 + 선택지 4개씩 + 정답 번호**를 미리 적어두면 Step 1이 순식간에 끝납니다.

## 0-4. GitHub 저장소 생성

1. GitHub → **New repository**
2. Repository name: `python-quiz-game` (자유)
3. Public 선택
4. ⚠️ **"Add a README file" 체크는 해제**하세요 (아래 경고 참조)
5. **Create repository**

> [!WARNING]
> GitHub에서 README를 체크해 저장소를 만들면, 로컬에도 커밋이 있는 상태에서 첫 `push`가 거부됩니다
> (`! [rejected] main -> main (fetch first)`).
>
> **가장 쉬운 해결책은 지금 그 저장소를 삭제하고 README 체크 없이 다시 만드는 것입니다.**
> (Settings → 맨 아래 Danger Zone → Delete this repository)
>
> 저장소를 유지하고 싶다면 첫 push(0-8) 전에 아래를 실행하세요. **양쪽에 `README.md`가 따로 있어서
> 반드시 충돌(add/add)이 납니다.** 충돌 해결까지가 한 세트라는 점을 기억하세요.
> ```bash
> git pull --rebase origin main
> #   → CONFLICT (add/add): Merge conflict in README.md
> #   README.md를 열어 <<<<<<<, =======, >>>>>>> 표시 줄을 지우고
> #   내가 쓸 내용만 남긴 뒤 저장합니다.
> git add README.md
> git rebase --continue      # 편집기가 뜨면 그대로 저장하고 닫기
> git push -u origin main
> ```
> 도중에 꼬였다면 `git rebase --abort`로 언제든 되돌릴 수 있습니다.

## 0-5. 로컬 프로젝트 폴더 & `git init`

```bash
cd ~/Project/second-project     # 프로젝트 루트로 이동
git init                        # ✅ Git 명령어 1/7: init
git branch -M main              # 브랜치 이름을 main으로 통일
```

## 0-6. `.gitignore` 작성

프로젝트 루트에 `.gitignore` 파일을 만들고 아래 내용을 넣습니다.

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/

# 에디터 / OS
.vscode/
.idea/
.DS_Store
Thumbs.db

# 게임 실행 중 생성되는 데이터 (아래 [!NOTE] 참고)
state.json
state.json.bak
```

> [!NOTE]
> **`state.json`을 커밋해야 하나요?** — 둘 다 정답이며, **선택 후 README에 이유를 적으면 됩니다.**
>
> | 선택 | 장점 | 주의점 |
> |---|---|---|
> | **A. `.gitignore`에 추가 (권장)** | 실행 중 계속 바뀌는 데이터가 커밋 로그를 더럽히지 않음. 채점자가 clone 후 실행하면 **"파일이 없을 때 기본 퀴즈 5개 자동 생성"** 기능이 그대로 증명됨 | 기본 퀴즈 5개가 **반드시 코드 안에** 있어야 함 |
> | **B. 커밋한다** | 내가 추가한 퀴즈까지 저장소에 남음 | 실행할 때마다 `git status`에 변경으로 잡혀 번거로움 |
>
> 이 가이드는 **A안**을 기준으로 설명합니다.

## 0-7. `README.md` 초안 작성

지금은 뼈대만 만들고, Step 5에서 완성합니다.

````markdown
# 🎯 나만의 퀴즈 게임

## 1. 프로젝트 개요
(무엇을 만드는 프로그램인지 2~3줄)

## 2. 퀴즈 주제와 선정 이유
(주제: 자료구조 / 0-3에서 정리한 선정 이유를 내 말로 적으세요)

## 3. 실행 방법
```bash
python main.py
```

## 4. 기능 목록
- [ ] 퀴즈 풀기
- [ ] 퀴즈 추가
- [ ] 퀴즈 목록
- [ ] 점수 확인
- [ ] 종료

## 5. 파일 구조
(작성 예정)

## 6. 데이터 파일 설명 (state.json)
(작성 예정)
````

## 0-8. 첫 커밋 & 푸시

```bash
git status                       # 현재 상태 확인 (습관 들이기!)
git add .gitignore README.md     # ✅ Git 명령어 2/7: add
git commit -m "Chore: 프로젝트 초기 설정 및 .gitignore 추가"   # ✅ 3/7: commit

git remote add origin https://github.com/<내아이디>/<저장소명>.git
git remote -v                    # 연결 확인
git push -u origin main          # ✅ Git 명령어 4/7: push
```

> [!TIP]
> `-u` 옵션은 "앞으로 이 브랜치는 `origin/main`과 짝"이라고 등록하는 것입니다.
> 한 번 해두면 다음부터는 `git push`만 쳐도 됩니다.

### 🔀 Git 체크포인트

| # | 커밋 메시지 | 사용한 명령어 |
|---|---|---|
| 1 | `Chore: 프로젝트 초기 설정 및 .gitignore 추가` | `init`, `add`, `commit`, `push` |

### ✅ Step 0 검증 체크리스트

- [ ] `python --version`(또는 `python3`) 결과가 **3.10 이상**이다
- [ ] `git config --global user.email`이 GitHub 이메일과 같다
- [ ] 퀴즈 주제(자료구조)를 확인했고, 출제할 문제 5개를 메모해뒀다
- [ ] 프로젝트 루트에 `.gitignore`와 `README.md`가 있다
- [ ] GitHub 저장소 웹페이지를 새로고침하면 두 파일이 보인다
- [ ] `git log --oneline` 실행 시 커밋 1개가 보인다
- [ ] 📸 `docs/screenshots/env_setup.png` 저장 완료

---

# Step 1. 개별 퀴즈 모델 구현 (`Quiz` 클래스)

> 🎯 **이 Step의 목표**: "퀴즈 1개"라는 개념을 코드로 표현하는 설계 감각 익히기.

## 1-1. 🧠 개념: 왜 클래스를 쓰나요?

퀴즈 하나에는 **문제 · 선택지 4개 · 정답 번호**라는 정보가 항상 **세트로** 붙어 다닙니다.

```python
# ❌ 리스트 3개로 따로 관리하면?
questions = ["문제1", "문제2"]
choices   = [[...], [...]]
answers   = [3, 1]
# → questions[1]의 정답은 answers[1]... 인덱스가 어긋나면 조용히 망가집니다.

# ✅ 하나로 묶으면?
quiz = Quiz("문제1", ["A", "B", "C", "D"], 3)
quiz.question   # 문제
quiz.answer     # 정답
```

- **클래스(class)** = 설계도 (붕어빵 틀)
- **객체/인스턴스(instance)** = 설계도로 찍어낸 실물 (붕어빵)
- **`__init__`** = 객체가 태어날 때 자동 실행되는 초기화 메서드
- **`self`** = "지금 이 객체 자신". 속성을 저장·조회할 때의 통로

## 1-2. 🏗️ 설계 힌트: `Quiz` 클래스 뼈대

`main.py`를 만들고 아래 뼈대를 옮겨 적은 뒤 `# TODO`를 채우세요.

```python
class Quiz:
    """퀴즈 한 문제를 표현하는 클래스."""

    def __init__(self, question, choices, answer):
        # TODO: 전달받은 값을 self.question / self.choices / self.answer 에 저장
        pass

    def display(self, number=None):
        """문제와 선택지 4개를 보기 좋게 출력한다.
        number가 주어지면 '[문제 3]' 처럼 번호를 함께 출력한다.
        """
        # TODO: 문제 출력
        # TODO: enumerate()로 선택지를 '1. 보기내용' 형태로 출력
        pass

    def is_correct(self, user_answer):
        """사용자가 입력한 번호(1~4)가 정답이면 True를 반환한다."""
        # TODO: self.answer와 비교해서 True/False 반환
        pass

    def to_dict(self):
        """JSON으로 저장할 수 있는 dict 형태로 변환한다. (Step 5에서 사용)"""
        # TODO: {"question": ..., "choices": ..., "answer": ...} 반환
        pass

    @classmethod
    def from_dict(cls, data):
        """dict를 받아 Quiz 객체를 만들어 반환한다. (Step 5에서 사용)"""
        # TODO: cls(data["question"], data["choices"], data["answer"]) 반환
        pass
```

> [!IMPORTANT]
> **가장 많이 터지는 버그: 1-based vs 0-based 혼동**
>
> 사용자에게는 `1, 2, 3, 4`로 보여주지만, 파이썬 리스트 인덱스는 `0, 1, 2, 3`입니다.
> `answer`를 **1~4 사이의 번호**로 저장하기로 정했다면(권장), 프로그램 전체에서 그 규칙을 절대 어기지 마세요.
> ```python
> quiz = Quiz("스택(Stack)의 자료 처리 방식은?",
>             ["FIFO (선입선출)", "LIFO (후입선출)", "우선순위 순", "무작위 접근"], 2)
> quiz.choices[quiz.answer - 1]   # → "LIFO (후입선출)"   ← 꺼낼 때만 -1
> quiz.is_correct(2)              # → True
> ```

<details>
<summary>🤔 <code>@classmethod</code>가 뭔가요? (펼쳐보기)</summary>

일반 메서드는 "이미 만들어진 객체"가 호출합니다(`quiz.display()`).
`from_dict`는 아직 객체가 없는 상태에서 **객체를 만들어내야** 하므로, 객체 대신 **클래스 자신(`cls`)** 을 받는 `@classmethod`로 만듭니다.

```python
q = Quiz.from_dict({"question": "...", "choices": [...], "answer": 2})
```
지금은 "JSON dict ↔ Quiz 객체를 오가는 변환기 한 쌍"으로만 이해해도 충분합니다.

</details>

### 🔀 여기서 커밋 (커밋 #2)

```bash
git status                    # 무엇이 바뀌었는지 확인 (습관 들이기!)
git add main.py
git commit -m "Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)"
```

> [!IMPORTANT]
> **🔀 표시가 보이면 다음 절로 넘어가기 전에 그 자리에서 실행하세요.**
> 커밋은 "직전 커밋 이후 바뀐 것"만 담습니다. 여러 절을 몰아서 작성한 뒤 커밋 명령만 연달아 실행하면
> **첫 번째 커밋이 변경분을 전부 가져가고, 두 번째부터는
> `nothing to commit, working tree clean` 이 뜨며 커밋이 만들어지지 않습니다.**
> 그러면 이 미션의 필수 조건인 "의미 있는 커밋 10개 이상"을 채울 수 없습니다.
>
> 이미 몰아서 작성해버렸다면 둘 중 하나로 수습하세요.
> - 이번엔 메시지를 하나로 합쳐 한 번만 커밋하고, 대신 뒤쪽 Step에서 커밋 지점을 더 잘게 나눈다.
> - `git add -p main.py` 로 변경 덩어리를 하나씩 골라 나눠 담는다. (조금 어렵지만 정석)

## 1-3. 💻 직접 해보기: 기본 퀴즈 데이터 5개

Step 0에서 정한 **자료구조** 주제로 **5개 이상**의 퀴즈를 만드는 함수를 작성하세요.
아래에 2개를 예시로 채워뒀습니다. **나머지 3개 이상은 직접 만드세요.**

```python
def get_default_quizzes():
    """파일이 없을 때(첫 실행) 사용할 기본 퀴즈 목록을 반환한다."""
    return [
        Quiz("스택(Stack)의 자료 처리 방식은?",
             ["FIFO (선입선출)", "LIFO (후입선출)", "우선순위 순", "무작위 접근"], 2),
        Quiz("파이썬의 딕셔너리(dict)가 내부적으로 사용하는 자료구조는?",
             ["배열", "연결 리스트", "해시 테이블", "이진 탐색 트리"], 3),
        # TODO: 0-3의 세부 영역 표를 보고 자료구조 퀴즈를 3개 이상 더 추가
    ]
```

> [!IMPORTANT]
> 과제 요구사항은 **"본인이 선택한 주제의 퀴즈 5개 이상을 직접 작성한다"** 입니다.
> 예시 2개를 그대로 두고 3개만 채워도 조건은 충족되지만, 5개 모두 직접 만들어 보는 쪽이
> 훨씬 남는 게 많습니다. 문제를 만들려면 그 자료구조를 **정확히 알아야** 하기 때문입니다.

<details>
<summary>💡 <b>도저히 안 떠오를 때만 펼쳐보세요 — 자료구조 문제 은행 10선</b></summary>

먼저 직접 만들어 본 다음에 참고하세요. 그대로 베끼기보다 **선택지를 내 말로 바꿔 쓰는 것**을 권합니다.

| # | 문제 | 선택지 (1 → 4) | 정답 |
|---|---|---|---|
| 1 | 스택(Stack)의 자료 처리 방식은? | FIFO (선입선출) / LIFO (후입선출) / 우선순위 순 / 무작위 접근 | 2 |
| 2 | 큐(Queue)의 특징으로 옳은 것은? | 먼저 들어간 데이터가 먼저 나온다 / 나중에 들어간 데이터가 먼저 나온다 / 항상 가장 큰 값이 먼저 나온다 / 순서 없이 나온다 | 1 |
| 3 | 파이썬 리스트에서 `lst[3]`처럼 인덱스로 값 하나를 꺼낼 때의 시간 복잡도는? | O(1) / O(log n) / O(n) / O(n²) | 1 |
| 4 | 연결 리스트(Linked List)가 배열(Array)보다 유리한 점은? | 인덱스로 임의 접근이 빠르다 / 중간 삽입·삭제가 빠르다 / 메모리를 항상 덜 쓴다 / 캐시 효율이 좋다 | 2 |
| 5 | 이진 탐색 트리(BST)를 중위 순회(in-order)하면 값이 어떤 순서로 나오는가? | 무작위 순서 / 오름차순 정렬 / 내림차순 정렬 / 레벨 순서 | 2 |
| 6 | 해시 테이블(Hash Table)의 **평균** 탐색 시간 복잡도는? | O(1) / O(log n) / O(n) / O(n²) | 1 |
| 7 | 파이썬의 딕셔너리(dict)가 내부적으로 사용하는 자료구조는? | 배열 / 연결 리스트 / 해시 테이블 / 이진 탐색 트리 | 3 |
| 8 | 최소 힙(Min Heap)의 루트 노드에 있는 값은? | 가장 큰 값 / 가장 작은 값 / 중앙값 / 마지막에 삽입된 값 | 2 |
| 9 | 그래프 탐색에서 큐(Queue)를 사용하는 알고리즘은? | DFS (깊이 우선 탐색) / BFS (너비 우선 탐색) / 이진 탐색 / 퀵 정렬 | 2 |
| 10 | 재귀 함수의 호출 순서를 관리하는 데 쓰이는 자료구조는? | 큐 / 스택 / 힙 / 해시 테이블 | 2 |

</details>

> [!NOTE]
> 이 함수는 단순한 예시 데이터가 아니라 **요구사항입니다.**
> "`state.json`이 없거나 손상되면 기본 퀴즈 데이터를 사용한다"는 조건이 바로 이 함수로 충족됩니다.
> (`.gitignore`에 `state.json`을 넣었다면 더더욱 코드 안에 있어야 합니다.)

### 🔀 여기서 커밋 (커밋 #3)

```bash
git add main.py
git commit -m "Feat: 자료구조 주제 기본 퀴즈 데이터 5개 추가"
git push
```

## 1-4. 💻 동작 확인

파일 맨 아래에 임시 확인 코드를 넣고 실행해 보세요.

```python
if __name__ == "__main__":
    quizzes = get_default_quizzes()
    print(f"퀴즈 개수: {len(quizzes)}")
    quizzes[0].display(1)
    print(quizzes[0].is_correct(3))   # 정답 번호를 넣으면 True
    print(quizzes[0].is_correct(1))   # 오답 번호를 넣으면 False
    print(quizzes[0].to_dict())
```

```bash
python main.py
```

<details>
<summary>🤔 <code>if __name__ == "__main__":</code> 는 왜 쓰나요? (펼쳐보기)</summary>

이 파일을 **직접 실행할 때만** 아래 코드를 돌리라는 뜻입니다.
나중에 이 파일을 다른 파일에서 `import` 하면 이 블록은 실행되지 않습니다.
"테스트 코드가 남의 프로그램에서 멋대로 돌아가는 사고"를 막아줍니다.

</details>

### 🔀 Step 1 커밋 요약

이미 위에서 두 번 커밋했습니다. `git log --oneline`으로 확인하세요.

| # | 커밋 메시지 | 커밋한 시점 |
|---|---|---|
| 2 | `Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)` | 1-2 직후 |
| 3 | `Feat: 자료구조 주제 기본 퀴즈 데이터 5개 추가` | 1-3 직후 |

> [!TIP]
> **커밋 메시지 컨벤션** — `타입: 무엇을 왜 했는지 요약`
> | 타입 | 사용 시점 |
> |---|---|
> | `Feat:` | 새 기능 추가 |
> | `Fix:` | 버그 수정 |
> | `Docs:` | 문서(README 등) 변경 |
> | `Refactor:` | 동작은 그대로, 코드 구조 개선 |
> | `Chore:` | 설정 파일, 빌드 등 잡무 |
> | `Style:` | 들여쓰기/공백 등 포맷팅 |
>
> ❌ `update`, `수정`, `ㅁㄴㅇㄹ`, `commit1` → 감점 대상
> ✅ `Fix: 정답 번호가 0일 때 IndexError 발생하던 문제 수정`

### ✅ Step 1 검증 체크리스트

- [ ] `Quiz` 클래스에 `question`, `choices`, `answer` 세 속성이 있다
- [ ] `display()`가 문제와 선택지 4개를 `1. ~ 4.` 형태로 출력한다
- [ ] `is_correct()`가 정답에 `True`, 오답에 `False`를 반환한다
- [ ] `to_dict()` / `from_dict()`가 서로 왕복 변환된다 (`Quiz.from_dict(q.to_dict()).question == q.question`)
- [ ] 내 주제의 퀴즈가 **5개 이상**이고, 각각 선택지가 정확히 4개다
- [ ] 모든 `answer` 값이 **1~4 범위**다
- [ ] 커밋이 총 3개다 (`git log --oneline`)

---

# Step 2. 메뉴 시스템 및 예외 처리 (`QuizGame` 기초)

> 🎯 **이 Step의 목표**: 프로그램의 뼈대(메인 루프)를 세우고, **어떤 이상한 입력에도 죽지 않는** 입력 처리기를 만든다.

> [!IMPORTANT]
> **이번 Step이 이 미션에서 가장 배점이 큰 구간입니다.**
> 여기서 만드는 `ask_int()` 하나를 프로그램 전체(메뉴 선택, 정답 입력, 퀴즈 추가)에서 재사용합니다.
> 대충 만들고 넘어가면 Step 3, 4에서 같은 코드를 세 번 복붙하게 됩니다.

## 2-1. 🧠 개념: 두 종류의 "잘못된 입력"

| 종류 | 예시 | 올바른 처리 |
|---|---|---|
| **복구 가능** — 사용자가 잘못 침 | `abc`, `9`, `0`, 그냥 Enter, `  1  ` | 안내 메시지 출력 후 **다시 입력받기** (프로그램 계속) |
| **복구 불가** — 입력 자체가 끊김 | `Ctrl+C`(KeyboardInterrupt), `Ctrl+D`/파이프 종료(EOFError) | 안내 메시지 + **저장 후 안전 종료** |

> [!CAUTION]
> **최악의 버그: EOFError 무한 루프**
>
> ```python
> # ❌ 절대 이렇게 하지 마세요
> while True:
>     try:
>         value = int(input("선택: "))
>     except:                       # ← EOFError까지 삼켜버림
>         print("잘못된 입력입니다")
>         continue                  # ← 입력 스트림이 끝났는데 또 input() 호출
> ```
> 입력 스트림이 닫힌 뒤에는 `input()`이 **즉시 EOFError를 다시** 냅니다.
> 위 코드는 "잘못된 입력입니다"를 초당 수만 번 출력하며 터미널을 마비시킵니다.
> 👉 **규칙: `except:` (맨몸 except)나 `except Exception:`을 재입력 루프 안에서 쓰지 마세요.
> 잡을 예외를 `ValueError`처럼 정확히 지정하세요.**
>
> 직접 확인해보기: `echo "" | python main.py` (입력이 바로 끝나는 상황을 만듭니다)

## 2-2. 🏗️ 설계 힌트: 공통 입력 헬퍼

```python
class QuizGame:
    """게임 전체 흐름을 관리하는 클래스."""

    def __init__(self):
        self.quizzes = get_default_quizzes()   # Step 5에서 파일 불러오기로 교체
        self.best_score = 0

    # ------------------------------------------------------------------
    # 공통 입력 헬퍼 (프로그램 전체에서 재사용)
    # ------------------------------------------------------------------
    def ask_int(self, prompt, low, high):
        """low~high 사이의 정수를 얻을 때까지 반복해서 입력받아 반환한다.

        처리해야 할 케이스:
          1) 앞뒤 공백 제거 후 처리      "  1  " → 1
          2) 빈 입력(그냥 Enter)         → 안내 후 재입력
          3) 숫자 변환 실패("abc")       → 안내 후 재입력
          4) 허용 범위 밖(9, 0, -3)      → 안내 후 재입력
          ※ KeyboardInterrupt / EOFError 는 여기서 잡지 않고 run()까지 올려보낸다!
        """
        while True:
            raw = input(prompt).strip()          # ← 1) strip()

            if not raw:                          # ← 2) 빈 입력
                # TODO: 안내 메시지 출력 후 continue
                pass

            try:
                value = int(raw)                 # ← 3) 변환 시도
            except ValueError:                   # ← ValueError만 정확히 지정!
                # TODO: "숫자를 입력하세요" 안내 후 continue
                continue

            if low <= value <= high:             # ← 4) 범위 검사
                return value
            # TODO: f"⚠️ {low}-{high} 사이의 숫자를 입력하세요." 안내 후 반복

    def ask_text(self, prompt):
        """비어 있지 않은 문자열을 얻을 때까지 반복 입력받아 반환한다."""
        # TODO: input().strip() → 비어 있으면 안내 후 재입력, 아니면 반환
        pass
```

> [!TIP]
> **`int()`가 던지는 예외는 정확히 `ValueError` 하나입니다.**
> ```python
> int("abc")   # ValueError: invalid literal for int() with base 10: 'abc'
> int("1.5")   # ValueError  ← 소수점도 실패합니다!
> int("")      # ValueError
> int(" 1 ")   # 1 (사실 int는 공백을 자동 무시하지만, 요구사항이므로 strip()을 명시적으로 쓰세요)
> ```

### 🔀 여기서 커밋 (커밋 #4)

```bash
git add main.py
git commit -m "Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현"
```

## 2-3. 🏗️ 설계 힌트: 메뉴 출력과 메인 루프

```python
    def show_menu(self):
        """메뉴 화면을 출력한다."""
        print("\n" + "=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        # TODO: 1~5번 메뉴 항목 출력
        print("=" * 40)

    def run(self):
        """프로그램의 메인 루프. 메뉴를 반복 출력하며 선택에 따라 기능을 호출한다."""
        while True:
            self.show_menu()
            choice = self.ask_int("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()        # Step 3에서 구현
            elif choice == 2:
                self.add_quiz()         # Step 4에서 구현
            elif choice == 3:
                self.show_quiz_list()   # Step 4에서 구현
            elif choice == 4:
                self.show_score()       # Step 4에서 구현
            elif choice == 5:
                # TODO: 작별 인사 출력 + 저장(Step 5) 후 return 으로 루프 탈출
                return
```

> [!NOTE]
> **지금 당장 5개 기능을 다 만들 필요 없습니다.**
> 아직 없는 메서드는 아래처럼 "자리만" 만들어 두고(스텁), Step 3~4에서 채우세요.
> ```python
> def play_quiz(self):
>     print("🚧 준비 중입니다.")
> ```
> 이렇게 하면 **지금 바로 프로그램을 실행해서 메뉴가 도는지 확인**할 수 있습니다.
> 이것이 "작게 만들고 자주 돌려보기"라는 개발의 기본 습관입니다.

## 2-4. 🏗️ 설계 힌트: 안전 종료 (`KeyboardInterrupt` / `EOFError`)

```python
def main():
    game = QuizGame()
    try:
        game.run()
    except KeyboardInterrupt:
        # TODO: 줄바꿈 + "프로그램을 종료합니다" 안내
        # TODO: 가능한 범위에서 저장 (Step 5에서 game.save_state() 호출 추가)
        pass
    except EOFError:
        # TODO: 입력 종료 안내 + 저장
        pass


if __name__ == "__main__":
    main()
```

> [!IMPORTANT]
> **예외를 "어디서" 잡느냐가 설계의 핵심입니다.**
> ```
>  input() 에서 Ctrl+C 발생
>        │
>        ▼  (ask_int는 ValueError만 잡으므로 그냥 통과)
>     ask_int()
>        │
>        ▼  (run()도 안 잡음)
>       run()
>        │
>        ▼
>      main()  ← 여기서 딱 한 번 잡아서 "저장 후 안전 종료"
> ```
> 예외를 **가장 바깥의 한 곳**에서만 처리하면 종료 로직이 한 군데로 모여 관리하기 쉽습니다.

## 2-5. 💻 동작 확인 (아래를 전부 시도해보세요)

| 입력 | 기대 결과 |
|---|---|
| `1` ~ `5` | 해당 기능 호출 / 5는 종료 |
| `  2  ` (앞뒤 공백) | 2번 기능 정상 호출 |
| `abc` | `⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.` 후 재입력 |
| `9` | 동일한 안내 후 재입력 |
| `0`, `-1` | 동일한 안내 후 재입력 |
| 그냥 `Enter` | 안내 후 재입력 (**무한 루프 아님**) |
| `1.5` | 안내 후 재입력 |
| `Ctrl+C` | 안내 메시지 후 깔끔히 종료 (빨간 Traceback ❌) |
| `echo "" \| python main.py` | EOFError 안내 후 즉시 종료 (**폭주 ❌**) |

📸 **스크린샷 촬영**: 잘못된 입력 처리 화면 → `docs/screenshots/invalid_input.png` (선택이지만 강력 추천)

### 🔀 여기서 커밋 (커밋 #5)

2-5의 9가지 입력을 모두 확인한 뒤 커밋하세요.

```bash
git add main.py
git commit -m "Feat: 메인 메뉴 루프 및 KeyboardInterrupt/EOFError 안전 종료 처리"
git push
```

### 🔀 Step 2 커밋 요약

| # | 커밋 메시지 | 커밋한 시점 |
|---|---|---|
| 4 | `Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현` | 2-2 직후 |
| 5 | `Feat: 메인 메뉴 루프 및 KeyboardInterrupt/EOFError 안전 종료 처리` | 2-5 직후 |

### ✅ Step 2 검증 체크리스트

- [ ] 클래스가 2개 이상 존재한다 (`Quiz`, `QuizGame`)
- [ ] 메뉴 5개가 출력되고 5번으로 정상 종료된다
- [ ] 위 2-5 표의 **9가지 입력을 모두 직접 시도**했고 전부 통과했다
- [ ] `except:` 또는 `except Exception:` 을 재입력 루프 안에서 쓰지 않았다
- [ ] `Ctrl+C`를 눌렀을 때 빨간 Traceback이 뜨지 않는다
- [ ] `ask_int()`가 메뉴 선택에서 재사용되고 있다 (복붙 없음)
- [ ] 커밋이 총 5개다

---

# Step 3. 브랜치를 활용한 퀴즈 풀기 기능

> 🎯 **이 Step의 목표**: 핵심 기능을 만들면서, **브랜치에서 작업하고 main에 병합하는** 실전 Git 워크플로우를 경험한다.

## 3-1. 🧠 개념: 브랜치는 왜 필요한가?

```
main   ●───●───●───────────────●  ← 항상 "동작하는" 안정 버전
                \             /
feat/play-quiz   ●───●───●───●    ← 실험/개발용 작업 공간
```

- `main`을 망가뜨릴 걱정 없이 자유롭게 실험할 수 있습니다.
- 기능이 완성되면 `merge`로 합칩니다.
- 실무의 팀 협업은 전부 이 구조 위에서 돌아갑니다.

## 3-2. 🔀 브랜치 생성 및 이동 (**코딩 전에 먼저!**)

```bash
git status                          # 커밋 안 된 변경이 없는지 확인
git checkout -b feat/play-quiz      # ✅ Git 명령어 5/7: checkout (-b = 생성 후 이동)
git branch                          # * feat/play-quiz 로 표시되면 성공
```

> [!WARNING]
> 코드를 다 짜고 나서 브랜치를 만들면 "브랜치에서 작업한 기록"이 남지 않습니다.
> **반드시 코딩을 시작하기 전에** `checkout -b`를 하세요.

## 3-3. 🏗️ 설계 힌트: 퀴즈 출제와 채점

```
play_quiz()
   │
   ├─ 퀴즈가 0개인가? ──► "등록된 퀴즈가 없습니다" 안내 후 return   ← 잊기 쉬운 요구사항!
   │
   ├─ score = 0
   ├─ 모든 퀴즈에 대해 반복:
   │     ├─ quiz.display(번호)
   │     ├─ user = self.ask_int("정답 입력: ", 1, 4)   ← Step 2 헬퍼 재사용!
   │     ├─ quiz.is_correct(user) 이면 ✅ 출력 + score += 1
   │     └─ 아니면 ❌ 출력 + 정답이 무엇이었는지 알려주기
   │
   ├─ 100점 만점으로 환산
   ├─ 결과 출력 ("5문제 중 4문제 정답! (80점)")
   └─ 최고 점수 비교 → 갱신되면 🎉 축하 메시지 + 저장(Step 5)
```

```python
    def play_quiz(self):
        """저장된 퀴즈를 출제하고 채점한 뒤 최고 점수를 갱신한다."""
        if not self.quizzes:
            # TODO: "등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요." 안내 후 return
            return

        total = len(self.quizzes)
        correct = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for i, quiz in enumerate(self.quizzes, start=1):
            print("\n" + "-" * 40)
            quiz.display(i)
            user_answer = self.ask_int("\n정답 입력: ", 1, 4)
            # TODO: 정답 여부 판정 후 메시지 출력, 맞으면 correct += 1
            # TODO: 틀렸다면 정답 선택지도 함께 알려주기
            #       힌트: quiz.choices[quiz.answer - 1]

        # 최고 점수 처리는 3-4에서 이어서 만듭니다. 지금은 결과만 찍어 동작을 확인하세요.
        print(f"\n🏆 결과: {total}문제 중 {correct}문제 정답!")
```

여기까지 만들고 **한 번 실행해서** 끝까지 풀리는지 확인하세요.

### 🔀 여기서 커밋 (커밋 #6) — 브랜치 위에서

```bash
git branch                     # * feat/play-quiz 인지 반드시 확인!
git add main.py
git commit -m "Feat: 퀴즈 출제 및 정답 채점 기능 구현"
```

## 3-4. 🏗️ 설계 힌트: 100점 환산과 최고 점수 갱신

방금 만든 `play_quiz()`의 **끝부분**을 이어서 완성합니다.

```python
        # (위 for 반복문이 끝난 다음에 이어서)
        # TODO: score = round(correct / total * 100)
        # TODO: 결과 출력 — 예) "🏆 결과: 5문제 중 4문제 정답! (80점)"
        # TODO: score가 self.best_score보다 클 때만 갱신 + 🎉 축하 메시지
        #       best_correct / best_total 도 함께 갱신해두면 Step 4 점수 확인이 풍부해집니다
        # TODO: self.save_state()      ← Step 5에서 추가할 자리
```

> [!TIP]
> **점수는 왜 100점 만점으로 환산하나요?**
> 나중에 퀴즈를 추가하면 총 문제 수가 5개 → 6개로 바뀝니다.
> "맞힌 개수"로만 저장하면 `5문제 중 5개(만점)`보다 `6문제 중 5개`가 같은 점수로 기록되어 비교가 무의미해집니다.
> **비율(백분율)로 저장**해야 서로 다른 회차를 공정하게 비교할 수 있습니다.
> ```python
> score = round(correct / total * 100)   # 4/5 → 80
> ```
> 단, 결과 화면에는 `"5문제 중 4문제 정답! (80점)"`처럼 **원본 정보도 함께** 보여주면 더 친절합니다.
> (이를 위해 `best_correct`, `best_total`을 함께 저장해도 좋습니다 → Step 5)

## 3-5. 💻 동작 확인

- 퀴즈를 끝까지 풀고 결과가 나오는가?
- 정답 입력에 `abc`, `9`, `0`, Enter를 넣어도 재입력되는가? (`ask_int` 재사용 확인)
- 다시 풀어서 더 낮은 점수를 받으면 최고 점수가 **덮어써지지 않는가?**
- `self.quizzes = []`로 임시로 비운 뒤 실행하면 안내 메시지가 나오는가?

📸 **스크린샷 2 촬영**: 퀴즈 풀이 + 결과 화면 → `docs/screenshots/play.png`

### 🔀 여기서 커밋 (커밋 #7)

```bash
git add main.py
git commit -m "Feat: 최고 점수 비교 및 갱신 로직 추가"

# (선택) 브랜치를 원격에도 올려 작업 기록을 남기기
git push -u origin feat/play-quiz
```

## 3-6. 🔀 `main`으로 병합

```bash
git status                                                 # clean 인지 먼저 확인
git checkout main                                          # ✅ checkout (이동)
git merge --no-ff feat/play-quiz -m "Merge: 퀴즈 풀기 기능 병합"
git push origin main

# 병합 끝난 브랜치 정리 (선택)
git branch -d feat/play-quiz
```

> [!IMPORTANT]
> **`--no-ff` 옵션을 꼭 붙이세요.**
> 옵션 없이 병합하면 Git이 "빨리 감기(fast-forward)"로 처리해서 **브랜치가 갈라졌던 흔적이 사라집니다.**
> 그러면 제출용 `git log --oneline --graph` 스크린샷이 일직선으로 나와 **"브랜치 생성 및 병합 기록"을 증명할 수 없습니다.**
>
> ```
> ❌ ff 병합              ✅ --no-ff 병합
> * commit                *   Merge: 퀴즈 풀기 기능 병합
> * commit                |\
> * commit                | * Feat: 최고 점수 비교 및 갱신 로직 추가
>                         | * Feat: 퀴즈 출제 및 정답 채점 기능 구현
>                         |/
>                         * Feat: 메인 메뉴 루프 및 ...
> ```
>
> 확인: `git log --oneline --graph --all`

### 🔀 Step 3 커밋 요약

| # | 커밋 메시지 | 브랜치 | 커밋한 시점 |
|---|---|---|---|
| 6 | `Feat: 퀴즈 출제 및 정답 채점 기능 구현` | `feat/play-quiz` | 3-3 직후 |
| 7 | `Feat: 최고 점수 비교 및 갱신 로직 추가` | `feat/play-quiz` | 3-5 직후 |
| 8 | `Merge: 퀴즈 풀기 기능 병합` | `main` (merge commit) | 3-6 |

### ✅ Step 3 검증 체크리스트

- [ ] **코딩 전에** `git checkout -b feat/play-quiz`를 실행했다
- [ ] 퀴즈가 0개일 때 안내 메시지가 나오고 프로그램이 죽지 않는다
- [ ] 정답/오답 판정과 최종 결과가 출력된다
- [ ] 오답일 때 정답이 무엇이었는지 알려준다
- [ ] 최고 점수가 **더 높을 때만** 갱신된다
- [ ] 정답 입력에도 `ask_int()`가 재사용되어 잘못된 입력이 처리된다
- [ ] `git log --oneline --graph`에 **갈라졌다 합쳐지는 모양**이 보인다
- [ ] 커밋이 총 8개다
- [ ] 📸 `docs/screenshots/play.png` 저장 완료

---

# Step 4. 퀴즈 추가 · 목록 조회 · 점수 확인

> 🎯 **이 Step의 목표**: 나머지 메뉴 3개를 완성하고, **"데이터가 없을 때"** 를 빠짐없이 처리한다.

## 4-1. 🏗️ 퀴즈 추가 (`add_quiz`)

```
add_quiz()
   ├─ "📌 새로운 퀴즈를 추가합니다." 출력
   ├─ 문제 입력          → ask_text()  (빈 문자열 거부)
   ├─ 선택지 1~4 입력    → ask_text() × 4  (반복문 사용!)
   ├─ 정답 번호 입력     → ask_int(prompt, 1, 4)
   ├─ Quiz 객체 생성 → self.quizzes 에 append
   ├─ 파일 저장 (Step 5)
   └─ "✅ 퀴즈가 추가되었습니다!" 출력
```

```python
    def add_quiz(self):
        """사용자로부터 입력받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = self.ask_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            # TODO: ask_text(f"선택지 {i}: ") 로 입력받아 choices에 추가
            pass

        answer = self.ask_int("정답 번호 (1-4): ", 1, 4)

        # TODO: Quiz 객체를 만들어 self.quizzes에 추가
        # TODO: self.save_state()  ← Step 5에서 추가
        # TODO: 성공 메시지 출력
```

> [!TIP]
> **선택지 4개를 복붙하지 마세요.**
> ```python
> # ❌ 이렇게 4줄 반복하면 나중에 선택지를 5개로 바꿀 때 4군데를 고쳐야 합니다
> c1 = input("선택지 1: ")
> c2 = input("선택지 2: ")
> ...
> # ✅ for 반복문 + 리스트
> ```
> 이것이 요구사항에 있는 **"모든 코드를 한 함수에 작성하지 않고 기능별로 분리"** 의 정신입니다.

> [!NOTE]
> **추가 검증 아이디어(가산점)**: 선택지 4개 중 중복이 있으면 다시 입력받기.
> ```python
> if len(set(choices)) != 4:
>     print("⚠️ 선택지는 서로 달라야 합니다.")
> ```

### 🔀 여기서 커밋 (커밋 #9)

```bash
git add main.py
git commit -m "Feat: 퀴즈 추가 기능 및 입력 유효성 검사 구현"
```

## 4-2. 🏗️ 퀴즈 목록 (`show_quiz_list`)

```python
    def show_quiz_list(self):
        """등록된 퀴즈 목록을 번호와 함께 출력한다."""
        if not self.quizzes:
            # TODO: "등록된 퀴즈가 없습니다." 안내 후 return
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        # TODO: enumerate(self.quizzes, start=1) 로 "[1] 문제내용" 형태 출력
        print("-" * 40)
```

> [!NOTE]
> 목록에서는 **정답을 노출하지 마세요.** 문제만 보여주는 것이 자연스럽습니다.
> (정답까지 보고 싶다면 "목록 상세 보기"를 별도 기능으로 두세요.)

### 🔀 여기서 커밋 (커밋 #10)

```bash
git add main.py
git commit -m "Feat: 퀴즈 목록 조회 기능 구현 (빈 목록 처리 포함)"
```

## 4-3. 🏗️ 점수 확인 (`show_score`)

```python
    def show_score(self):
        """최고 점수를 출력한다. 아직 기록이 없으면 안내한다."""
        if self.best_score == 0:      # 또는 self.best_total == 0 등, 규칙을 정하세요
            # TODO: "아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어보세요!" 안내 후 return
            return

        # TODO: "🏆 최고 점수: 80점 (5문제 중 4문제 정답)" 형태로 출력
```

> [!IMPORTANT]
> **"아직 퀴즈를 풀지 않은 경우"는 명시적 요구사항입니다.**
> `0점`을 그냥 출력하면 "0점을 받은 것"인지 "안 푼 것"인지 구분되지 않습니다.
> 안 푼 상태를 표현할 방법을 정하세요. (예: `best_score = 0`을 미기록으로 취급하거나, `best_total = 0`으로 판별)

## 4-4. 💻 동작 확인

| 시나리오 | 기대 결과 |
|---|---|
| 2번 → 퀴즈 추가 → 3번 목록 | 방금 추가한 퀴즈가 목록에 보인다 |
| 문제 입력에서 그냥 Enter | 안내 후 재입력 |
| 정답 번호에 `5`, `0`, `abc` | 안내 후 재입력 |
| 아무것도 안 풀고 4번 | "아직 퀴즈를 풀지 않았습니다" 안내 |
| 1번으로 퀴즈 푼 뒤 4번 | 최고 점수 표시 |

📸 **스크린샷 3, 4 촬영**: `docs/screenshots/add_quiz.png`, `docs/screenshots/score.png`, `docs/screenshots/menu.png`

### 🔀 여기서 커밋 (커밋 #11)

```bash
git add main.py
git commit -m "Feat: 최고 점수 확인 기능 구현 (미기록 상태 처리)"
git push
```

### 🔀 Step 4 커밋 요약

| # | 커밋 메시지 | 커밋한 시점 |
|---|---|---|
| 9 | `Feat: 퀴즈 추가 기능 및 입력 유효성 검사 구현` | 4-1 직후 |
| 10 | `Feat: 퀴즈 목록 조회 기능 구현 (빈 목록 처리 포함)` | 4-2 직후 |
| 11 | `Feat: 최고 점수 확인 기능 구현 (미기록 상태 처리)` | 4-4 직후 |

### ✅ Step 4 검증 체크리스트

- [ ] 메뉴 5개가 **모두** 실제로 동작한다 (`🚧 준비 중` 이 하나도 없다)
- [ ] 퀴즈 추가 시 문제/선택지 4개/정답 번호를 모두 입력받는다
- [ ] 빈 입력·범위 밖·문자 입력이 세 기능 모두에서 처리된다
- [ ] 퀴즈 목록이 비었을 때 안내 메시지가 나온다
- [ ] 점수 미기록 상태가 별도로 처리된다
- [ ] 선택지 입력에 `for` 반복문을 사용했다
- [ ] 커밋이 총 11개다
- [ ] 📸 스크린샷 4종 저장 완료

---

# Step 5. 데이터 영속성(`state.json`)과 파일 손상 복구

> 🎯 **이 Step의 목표**: 프로그램을 껐다 켜도 데이터가 남게 만들고, **파일이 없거나 깨져도 절대 죽지 않게** 만든다.

> [!IMPORTANT]
> 지금까지 만든 프로그램은 종료하면 추가한 퀴즈와 점수가 **전부 사라집니다.**
> 지금 한번 확인해보세요 — 퀴즈를 추가하고 5번으로 종료한 뒤 다시 실행하면? 사라졌죠.
> 이 Step이 그것을 해결합니다.

## 5-1. 🧠 개념: JSON이 뭐고 왜 쓰나요?

**JSON(JavaScript Object Notation)** = 데이터를 사람도 읽을 수 있는 텍스트로 표현하는 표준 형식.

| Python | ↔ | JSON |
|---|---|---|
| `dict` | ↔ | `{ }` object |
| `list` | ↔ | `[ ]` array |
| `str` | ↔ | `"문자열"` |
| `int`, `float` | ↔ | number |
| `True` / `False` | ↔ | `true` / `false` |
| `None` | ↔ | `null` |

**Quiz 객체는 JSON으로 바로 저장할 수 없습니다.** 그래서 Step 1에서 `to_dict()` / `from_dict()`를 만든 것입니다.

```
[Quiz 객체] --to_dict()--> [dict] --json.dump()--> state.json 파일
[Quiz 객체] <--from_dict()-- [dict] <--json.load()-- state.json 파일
```

## 5-2. 🧠 스키마 설계

프로젝트 루트의 `state.json`:

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

| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list[dict] | 퀴즈 목록. 각 항목은 `question`(str), `choices`(str 4개), `answer`(int 1~4) |
| `best_score` | int | 최고 점수 (100점 환산) |
| `best_correct` | int | *(선택)* 최고 점수 당시 맞힌 문제 수 |
| `best_total` | int | *(선택)* 최고 점수 당시 총 문제 수 |

> [!NOTE]
> 필수는 `quizzes`와 `best_score` 두 개입니다. 나머지는 `"80점 (5문제 중 4문제 정답)"` 같은 상세 출력을 위한 선택 항목입니다.
> **어떤 키를 쓰든 프로그램 전체에서 일관되게 유지**하고, README에 정확히 문서화하세요.

## 5-3. 🏗️ 설계 힌트: 저장 (`save_state`)

```python
import json
from pathlib import Path

# 프로젝트 루트의 state.json — 어디서 실행하든 같은 파일을 가리키게 만든다
STATE_FILE = Path(__file__).resolve().parent / "state.json"
```

> [!CAUTION]
> **경로 함정**: `open("state.json", ...)` 처럼 상대 경로만 쓰면 **터미널의 현재 위치(cwd)** 기준으로 파일을 찾습니다.
> `cd ..` 후 `python second-project/main.py`로 실행하면 **엉뚱한 곳에 새 파일이 생기고 데이터가 사라진 것처럼 보입니다.**
> `Path(__file__).resolve().parent`는 "이 소스 파일이 있는 폴더"라서 실행 위치와 무관하게 항상 같은 곳을 가리킵니다.

```python
    def save_state(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],   # 리스트 컴프리헨션
            "best_score": self.best_score,
            # TODO: best_correct / best_total 도 저장한다면 여기에
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            # TODO: "저장에 실패했습니다" 안내 (프로그램은 계속 동작해야 함)
            pass
```

> [!IMPORTANT]
> **한글 저장 필수 옵션 2가지**
> | 옵션 | 없으면 생기는 일 |
> |---|---|
> | `encoding="utf-8"` | Windows에서 기본 인코딩이 cp949라 한글이 깨지거나 `UnicodeDecodeError` 발생 |
> | `ensure_ascii=False` | `"스택"` 가 `"\uc2a4\ud0dd"` 로 저장되어 사람이 못 읽음 (JSON으로는 유효하지만 열어봐도 알아볼 수 없음) |
>
> `indent=2`는 보기 좋게 줄바꿈해 주는 옵션입니다(선택이지만 권장 — 채점자가 파일을 열어봅니다).

### 🔀 여기서 커밋 (커밋 #12)

`save_state()`를 `add_quiz()` 끝과 최고 점수 갱신 직후, 그리고 5번 종료 시점에 호출하도록 연결한 뒤 커밋하세요.

```bash
git add main.py
git commit -m "Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False)"
```

## 5-4. 🏗️ 설계 힌트: 불러오기 (`load_state`) — 이 Step의 핵심

처리해야 할 상황이 **4가지**입니다.

| 상황 | 발생 예외 / 조건 | 처리 |
|---|---|---|
| ① 파일 없음 (첫 실행) | `FileNotFoundError` | 조용히 기본 퀴즈 5개 사용 (오류 아님!) |
| ② 파일이 깨진 JSON | `json.JSONDecodeError` | 안내 메시지 + 백업 + 기본 데이터로 복구 |
| ③ JSON은 맞지만 구조가 이상함 | `KeyError`, `TypeError`, `ValueError` | 동일하게 복구 |
| ④ 읽기 권한 오류 등 | `OSError` | 안내 후 기본 데이터로 진행 |

```python
    def load_state(self):
        """state.json에서 데이터를 불러온다. 실패하면 기본 데이터로 복구한다."""
        if not STATE_FILE.exists():
            # ① 첫 실행 — 정상 상황이므로 경고하지 말 것
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            print("🆕 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)          # ② 깨진 JSON이면 여기서 JSONDecodeError

            # ③ 구조 검증 — "믿지 말고 확인하라"
            if not isinstance(data, dict):
                raise ValueError("최상위 구조가 객체가 아닙니다")
            raw_quizzes = data["quizzes"]     # 없으면 KeyError
            if not isinstance(raw_quizzes, list):
                raise ValueError("quizzes가 리스트가 아닙니다")

            # TODO: Quiz.from_dict()로 변환해 self.quizzes 채우기
            # TODO: self.best_score = int(data.get("best_score", 0))
            # TODO: 불러오기 성공 메시지 출력
            #       예) 📂 저장된 데이터를 불러왔습니다. (퀴즈 6개, 최고점수 80점)

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"⚠️ 데이터 파일이 손상되었습니다: {e}")
            # TODO: 손상 파일을 state.json.bak 으로 백업 (선택이지만 추천)
            #       힌트: STATE_FILE.replace(STATE_FILE.with_suffix(".json.bak"))
            print("🔧 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
        except OSError as e:
            print(f"⚠️ 파일을 읽을 수 없습니다: {e}")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
```

> [!TIP]
> **`json.JSONDecodeError`는 `ValueError`의 하위 클래스**입니다.
> 그래서 `except ValueError:` 만 써도 잡히지만, **읽는 사람이 의도를 알 수 있도록 명시적으로 나열**하는 편이 좋습니다.

> [!NOTE]
> **`load_state()`는 언제 호출하나요?** `__init__`에서 호출합니다.
> ```python
> def __init__(self):
>     self.quizzes = []
>     self.best_score = 0
>     self.load_state()      # ← 프로그램 시작과 동시에 불러오기
> ```
> **`save_state()`는 언제 호출하나요?** (데이터가 바뀌는 모든 지점)
> - 퀴즈 추가 직후
> - 최고 점수 갱신 직후
> - 5번 메뉴로 종료할 때
> - `KeyboardInterrupt` / `EOFError`로 종료할 때 ← "가능한 범위에서 저장" 요구사항

## 5-5. 💻 동작 확인 (반드시 4가지 모두 테스트)

```bash
# ① 첫 실행 — 파일이 없는 상태
rm -f state.json          # Windows: del state.json
python main.py            # → "기본 퀴즈로 시작합니다" + 퀴즈 5개

# ② 영속성 — 껐다 켜도 유지되는가?
python main.py            # 2번으로 퀴즈 추가 → 1번으로 풀어 점수 기록 → 5번 종료
cat state.json            # Windows: type state.json  → 한글이 안 깨지고 보이는지 확인
python main.py            # → "퀴즈 6개, 최고점수 80점" 이 그대로 복원되는가?

# ③ 손상 복구 — 일부러 파일을 깨뜨려보기
echo "이건 JSON이 아님 {{{" > state.json
python main.py            # → 손상 안내 + 기본 데이터 복구 (죽으면 ❌)

# ④ 구조 이상 — JSON은 맞지만 키가 없는 경우
echo '{"hello": "world"}' > state.json
python main.py            # → 손상 안내 + 복구
```

📸 **스크린샷 촬영**: 재실행 후 데이터가 복원된 화면 → `docs/screenshots/persistence.png` (강력 추천)

### 🔀 여기서 커밋 (커밋 #13)

위 ①~④ 네 가지를 모두 통과한 뒤 커밋하세요.

```bash
git add main.py
git commit -m "Feat: state.json 불러오기 및 파일 부재/손상 시 자동 복구 처리"
git push
```

## 5-6. (선택) 모듈 분리 리팩터링

파일 하나가 길어졌다면 역할별로 나눠보세요. `Refactor:` 커밋을 남길 좋은 기회입니다.

```
second-project/
├── main.py          # 진입점: main() + 예외 처리
├── quiz.py          # Quiz 클래스
├── quiz_game.py     # QuizGame 클래스
└── storage.py       # save_state / load_state / STATE_FILE
```

```python
# main.py
from quiz_game import QuizGame
```

> [!WARNING]
> 분리 후 **반드시 다시 실행해서 동작을 확인**하세요.
> 리팩터링은 "동작은 그대로, 구조만 개선"이 원칙입니다. 동작이 바뀌었다면 그건 리팩터링이 아니라 버그입니다.
> 분리하면 `__pycache__/` 폴더가 생기는데, `.gitignore`에 이미 넣어뒀으니 걱정 마세요.

## 5-7. README 완성

Step 0의 초안을 채워 **6대 항목**을 완성합니다.

````markdown
# 🎯 나만의 퀴즈 게임

## 1. 프로젝트 개요
터미널에서 동작하는 4지선다 퀴즈 게임입니다. 퀴즈를 풀고, 직접 문제를 추가하고,
최고 점수를 기록할 수 있으며 모든 데이터는 state.json에 저장되어 프로그램을 종료해도 유지됩니다.

## 2. 퀴즈 주제와 선정 이유
- **주제**: 자료구조 (스택·큐·해시 테이블·트리·시간 복잡도)
- **선정 이유**: 정답이 하나로 명확히 떨어져 4지선다에 적합하고, 이 프로그램 자체가
  퀴즈 목록을 `list`로, 퀴즈 하나를 `dict`로 다루고 있어 문제를 만들면서
  내가 쓴 코드를 다시 들여다보게 되는 주제라서 선택했습니다.

## 3. 실행 방법
```bash
git clone https://github.com/<아이디>/<저장소>.git
cd <저장소>
python main.py     # Python 3.10 이상 필요, 외부 라이브러리 불필요
```

## 4. 기능 목록
| 번호 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 등록된 퀴즈를 순서대로 출제하고 채점, 최고 점수 갱신 |
| 2 | 퀴즈 추가 | 문제/선택지 4개/정답 번호를 입력받아 등록 후 즉시 저장 |
| 3 | 퀴즈 목록 | 등록된 퀴즈 전체를 번호와 함께 조회 |
| 4 | 점수 확인 | 최고 점수 조회 (미기록 상태 안내) |
| 5 | 종료 | 데이터를 저장하고 안전하게 종료 |

## 5. 파일 구조
```
second-project/
├── main.py                  # 프로그램 진입점
├── quiz.py                  # Quiz 클래스 (문제 1개를 표현)
├── quiz_game.py             # QuizGame 클래스 (게임 흐름 관리)
├── storage.py               # state.json 저장/불러오기
├── state.json               # 실행 시 자동 생성되는 데이터 파일 (git 제외)
├── .gitignore
├── README.md
└── docs/
    ├── reference.md
    ├── learning_guide.md
    └── screenshots/
```

## 6. 데이터 파일 설명 (state.json)
- **경로**: 프로젝트 루트 `./state.json` (`main.py`와 같은 폴더)
- **인코딩**: UTF-8 (`ensure_ascii=False`로 한글 그대로 저장)
- **역할**: 퀴즈 목록과 최고 점수를 영구 보관
- **생성 시점**: 첫 실행 시 자동 생성 (저장소에는 커밋하지 않음 — `.gitignore` 처리)
- **스키마**
  | 키 | 타입 | 설명 |
  |---|---|---|
  | `quizzes` | list[dict] | 퀴즈 목록 |
  | └ `question` | str | 문제 |
  | └ `choices` | list[str] | 선택지 4개 |
  | └ `answer` | int | 정답 번호 (1~4) |
  | `best_score` | int | 최고 점수 (100점 환산) |
  | `best_correct` | int | 최고 점수 당시 맞힌 개수 |
  | `best_total` | int | 최고 점수 당시 총 문제 수 |
- **예시**
```json
{
  "quizzes": [
    {"question": "스택(Stack)의 자료 처리 방식은?",
     "choices": ["FIFO (선입선출)", "LIFO (후입선출)", "우선순위 순", "무작위 접근"],
     "answer": 2}
  ],
  "best_score": 80,
  "best_correct": 4,
  "best_total": 5
}
```
- **없거나 손상된 경우**: 안내 메시지를 출력하고 코드에 내장된 기본 퀴즈 5개로 자동 복구합니다.
  (손상된 파일은 `state.json.bak`으로 백업됩니다.)

## 실행 화면
![메뉴](docs/screenshots/menu.png)
![퀴즈 풀기](docs/screenshots/play.png)
![퀴즈 추가](docs/screenshots/add_quiz.png)
![점수 확인](docs/screenshots/score.png)
````

### 🔀 여기서 커밋 (커밋 #14~15)

```bash
# 5-6 모듈 분리를 했다면 (새 파일이 생기므로 git add . 사용)
git add .
git commit -m "Refactor: Quiz/QuizGame/storage 모듈 분리"

# README 완성 + 스크린샷
git add README.md docs/
git commit -m "Docs: README 6대 항목 및 실행 화면 스크린샷 추가"
git push
```

### 🔀 Step 5 커밋 요약

| # | 커밋 메시지 | 커밋한 시점 |
|---|---|---|
| 12 | `Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False)` | 5-3 직후 |
| 13 | `Feat: state.json 불러오기 및 파일 부재/손상 시 자동 복구 처리` | 5-5 직후 |
| 14 | `Refactor: Quiz/QuizGame/storage 모듈 분리` *(선택)* | 5-6 직후 |
| 15 | `Docs: README 6대 항목 및 실행 화면 스크린샷 추가` | 5-7 직후 |

### ✅ Step 5 검증 체크리스트

- [ ] 퀴즈를 추가하고 종료 후 재실행하면 **그대로 남아 있다**
- [ ] 점수를 기록하고 재실행하면 최고 점수가 **그대로 남아 있다**
- [ ] `state.json`이 프로젝트 루트에 생성된다
- [ ] `state.json`을 열었을 때 **한글이 깨지지 않는다** (`\uXXXX` 아님)
- [ ] `state.json`을 지우고 실행해도 기본 퀴즈 5개로 정상 동작한다
- [ ] `state.json`에 아무 글자나 넣어 깨뜨려도 **안내 후 복구**된다 (Traceback ❌)
- [ ] README에 **6대 항목이 전부** 있다
- [ ] 스크린샷 4종이 README에서 정상적으로 보인다 (GitHub에서 확인!)
- [ ] 커밋이 총 14~15개다

---

# Step 6. 원격 저장소 복제(clone) & 가져오기(pull) 실습

> 🎯 **이 Step의 목표**: 마지막 남은 Git 명령어 `clone`과 `pull`을 실제 상황에서 사용해본다.

> [!NOTE]
> **왜 이 실습을 하나요?**
> 실무에서는 "회사 노트북 / 집 데스크톱"처럼 **같은 저장소를 여러 곳에서** 작업합니다.
> 이 실습은 그 상황을 혼자서 재현하는 것입니다.
> ```
>   GitHub (원격)
>     ↑ push        ↓ clone / pull
>   ┌────────┐    ┌──────────────┐
>   │ 원본   │    │ 복제본        │
>   │ 작업폴더│    │ quiz-clone   │
>   └────────┘    └──────────────┘
> ```

## 6-1. Step 5까지의 작업이 모두 push되었는지 먼저 확인

```bash
git status        # "nothing to commit, working tree clean" 이어야 함
git push
```

## 6-2. 다른 위치에 저장소 복제 (`clone`)

```bash
cd ~                                                          # 프로젝트 폴더 바깥으로!
git clone https://github.com/<아이디>/<저장소>.git quiz-clone   # ✅ Git 명령어 6/7: clone
cd quiz-clone
ls -la                                                        # 파일이 그대로 복제됐는지 확인
git log --oneline                                             # 커밋 히스토리까지 통째로 복제됨!
```

> [!WARNING]
> **프로젝트 폴더 안에서 clone하지 마세요.** 저장소 안에 저장소가 생겨 매우 혼란스러워집니다.
> 반드시 상위 폴더(`~` 등)로 이동한 뒤 실행하세요.

> [!TIP]
> **`clone` vs `init`**
> | | 언제 쓰나 | 하는 일 |
> |---|---|---|
> | `git init` | 저장소를 **처음 만들 때** | 빈 `.git` 폴더 생성 |
> | `git clone` | **이미 있는** 원격 저장소를 가져올 때 | 파일 + 전체 커밋 히스토리 + `origin` 연결까지 한 번에 |

## 6-3. 복제본에서 수정 → commit → push

`quiz-clone/README.md` 맨 아래에 한 줄 추가합니다.

```markdown
## 학습 회고
이 프로젝트를 통해 클래스로 역할을 나누는 법과, Git 브랜치로 안전하게 기능을 개발하는 법을 익혔습니다.
```

```bash
git add README.md
git commit -m "Docs: README에 학습 회고 추가"
git push origin main
```

📸 **스크린샷 촬영**: clone 및 push 과정 → `docs/screenshots/clone_pull.png` (선택, 추천)

## 6-4. 원본 작업 폴더에서 `pull`로 가져오기

```bash
cd ~/Project/second-project

cat README.md | tail -5     # pull 전 — "학습 회고"가 없음을 확인
git pull origin main        # ✅ Git 명령어 7/7: pull
cat README.md | tail -5     # pull 후 — "학습 회고"가 나타남!
git log --oneline -3        # 복제본에서 만든 커밋이 여기에도 들어옴
```

> [!IMPORTANT]
> **`pull`이 실패한다면?**
> ```
> error: Your local changes to the following files would be overwritten by merge
> ```
> 원본 폴더에 커밋하지 않은 변경이 남아 있다는 뜻입니다. 먼저 정리하세요.
> ```bash
> git status                    # 무엇이 변경됐는지 확인
> git add . && git commit -m "..."   # 커밋하거나
> git stash                          # 잠시 치워두거나
> git pull origin main
> ```

## 6-5. 정리 (선택)

```bash
rm -rf ~/quiz-clone      # 실습용 복제본 삭제. Windows: rmdir /s /q %USERPROFILE%\quiz-clone
```

> [!TIP]
> 제출 스크린샷을 다 찍은 뒤에 삭제하세요. 삭제해도 GitHub의 커밋 기록은 그대로 남습니다.

| # | 커밋 메시지 | 위치 |
|---|---|---|
| 16 | `Docs: README에 학습 회고 추가` | `quiz-clone` (복제본) |

### ✅ Step 6 검증 체크리스트

- [ ] 프로젝트 폴더 **바깥**에서 `git clone`을 실행했다
- [ ] 복제본에 커밋 히스토리가 그대로 따라왔다 (`git log --oneline`)
- [ ] 복제본에서 수정 → `commit` → `push` 성공
- [ ] GitHub 웹페이지에서 변경 내용이 보인다
- [ ] 원본 폴더에서 `git pull` 성공, README에 회고가 **실제로 반영**되었다
- [ ] 이제 Git 명령어 **7종을 모두** 사용했다

---

# Step 7. 보너스 과제 (선택)

> 필수 요구사항을 **모두 통과한 뒤에** 도전하세요. 각각 별도 브랜치로 작업하면 브랜치 연습도 한 번 더 됩니다.

## 7-1. 🎲 랜덤 출제 (난이도 ★☆☆)

```python
import random

quizzes = self.quizzes[:]        # ← 복사본을 만드는 것이 중요!
random.shuffle(quizzes)          # 원본 리스트를 직접 섞으면 저장 순서까지 바뀝니다
```
- 🔍 스스로 찾아보기: `random.shuffle()` vs `random.sample()`의 차이는?
- 커밋: `Feat: 퀴즈 출제 순서 랜덤 섞기 기능 추가`

## 7-2. 🔢 문제 수 선택 (난이도 ★☆☆)

- 퀴즈 시작 전 "몇 문제를 풀까요? (1~N)" 을 `ask_int(prompt, 1, len(self.quizzes))`로 입력받기
- 슬라이싱으로 개수 제한: `quizzes[:count]`
- 💡 이때 **100점 환산 방식의 진가**가 드러납니다 (3문제 중 3개 = 100점, 5문제 중 5개 = 100점)
- 커밋: `Feat: 풀 문제 수 선택 기능 추가`

## 7-3. 💡 힌트 기능 (난이도 ★★☆)

- `Quiz.__init__`에 `hint=None` 매개변수 추가 (**기본값을 주는 것이 핵심** — 기존 데이터가 깨지지 않음)
- 정답 입력 시 `0`을 누르면 힌트 표시 → `ask_int(prompt, 0, 4)`로 범위 확장
- 힌트를 쓰면 해당 문제는 0.5점만 인정하는 등 차감 로직
- ⚠️ `to_dict()` / `from_dict()`도 함께 수정해야 합니다. `from_dict`는 `data.get("hint")`로 **없어도 안 죽게** 만드세요.
- 커밋: `Feat: 힌트 기능 및 점수 차감 로직 구현`

## 7-4. 🗑️ 퀴즈 삭제 (난이도 ★★☆)

- 메뉴에 "6. 퀴즈 삭제" 추가 → `ask_int("선택: ", 1, 6)`으로 범위 수정 잊지 말기
- 목록을 보여준 뒤 삭제할 번호 입력 → `ask_int(prompt, 1, len(self.quizzes))`
- 삭제 전 "정말 삭제할까요? (y/n)" 재확인
- `del self.quizzes[번호 - 1]` 후 즉시 `save_state()`
- 커밋: `Feat: 퀴즈 삭제 기능 구현 (삭제 전 확인 절차 포함)`

## 7-5. 📊 점수 히스토리 (난이도 ★★★)

```python
from datetime import datetime

record = {
    "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "correct": correct,
    "total": total,
    "score": score,
}
```
- `state.json`에 `"history": []` 키 추가
- ⚠️ **기존 `state.json`에는 `history` 키가 없습니다.** `data.get("history", [])`로 읽어야 하위 호환이 유지됩니다.
  (이것이 실무의 "스키마 마이그레이션"의 축소판입니다.)
- 점수 확인 메뉴에서 최근 5회 기록 표시
- 커밋: `Feat: 게임 기록 히스토리 저장 및 조회 기능 구현`

---

# 최종 검증 & 제출 체크리스트

## A. Git 필수 명령어 7종 사용 확인

| # | 명령어 | 사용 시점 | 확인 방법 |
|---|---|---|---|
| 1 | `init` | Step 0-5 | `.git` 폴더 존재 (`ls -a`) |
| 2 | `add` | 매 커밋 전 | — |
| 3 | `commit` | 매 기능 완성 | `git log --oneline` |
| 4 | `push` | Step 0-8 이후 계속 | GitHub 웹에서 파일 확인 |
| 5 | `checkout` | Step 3-2, 3-6 | `git reflog` 에 checkout 기록 |
| 6 | `clone` | Step 6-2 | 복제 폴더 존재 |
| 7 | `pull` | Step 6-4 | README에 회고 문구 반영됨 |
| + | `merge` | Step 3-6 | `git log --graph`에 병합 커밋 |

## B. 최종 확인 명령어 (한 번에 실행)

```bash
cd ~/Project/second-project

echo "=== 1. 커밋 개수 (10개 이상이어야 함) ==="
git log --oneline | wc -l

echo "=== 2. 커밋 그래프 (브랜치 병합 모양 확인) ==="
git log --oneline --graph --all

echo "=== 3. 원격 저장소 연결 ==="
git remote -v

echo "=== 4. 커밋 안 된 변경 없는지 ==="
git status

echo "=== 5. 파일 구조 ==="
ls -la

echo "=== 6. Python 버전 ==="
python3 --version
```

📸 **스크린샷 5 촬영**: `git log --oneline --graph` 결과 → `docs/screenshots/git_graph.png`

> [!IMPORTANT]
> **커밋이 10개가 안 된다면** 억지로 빈 커밋을 만들지 마세요. 대신 이렇게 늘리세요.
> - 아직 안 한 리팩터링 수행 (`Refactor:`)
> - README에 트러블슈팅/회고 섹션 추가 (`Docs:`)
> - 보너스 과제 1개 구현 (`Feat:`)
> - 발견한 버그 수정 (`Fix:`)
> ❌ `git commit --allow-empty` 는 "의미 있는 커밋"이 아닙니다.

## C. 기능 요구사항 최종 점검

| 영역 | 확인 항목 | ✓ |
|---|---|---|
| **동작** | 메뉴 5개가 모두 정상 동작한다 | ☐ |
| | 자료구조 퀴즈가 5개 이상 있다 | ☐ |
| | 퀴즈를 추가하고 재실행해도 유지된다 | ☐ |
| | 최고 점수가 재실행 후에도 유지된다 | ☐ |
| **구조** | 클래스가 2개 이상 (`Quiz`, `QuizGame`) | ☐ |
| | 기능별로 메서드가 분리되어 있다 | ☐ |
| | `state.json`이 프로젝트 루트에 UTF-8로 저장된다 | ☐ |
| | 외부 라이브러리를 쓰지 않았다 (`pip install` 한 적 없음) | ☐ |
| **예외** | `abc` 입력 → 안내 후 재입력 | ☐ |
| | 범위 밖 숫자 → 안내 후 재입력 | ☐ |
| | 빈 Enter → 안내 후 재입력 | ☐ |
| | 앞뒤 공백 `" 1 "` → 정상 처리 | ☐ |
| | `Ctrl+C` → 안내 후 저장하고 안전 종료 | ☐ |
| | `EOFError` → 안내 후 안전 종료 (무한 루프 ❌) | ☐ |
| | `state.json` 없음 → 기본 데이터로 실행 | ☐ |
| | `state.json` 손상 → 안내 후 복구 | ☐ |
| | 퀴즈 0개 상태에서 풀기/목록 → 안내 | ☐ |
| | 점수 미기록 상태에서 점수 확인 → 안내 | ☐ |
| **Git** | 커밋 10개 이상, 컨벤션 준수 | ☐ |
| | 브랜치 생성 + 병합 기록 존재 | ☐ |
| | `clone`, `pull` 각 1회 이상 | ☐ |
| **README** | 프로젝트 개요 | ☐ |
| | 퀴즈 주제 선정 이유 | ☐ |
| | 실행 방법 | ☐ |
| | 기능 목록 | ☐ |
| | 파일 구조 | ☐ |
| | 데이터 파일 설명 (경로/역할/스키마) | ☐ |

## D. 제출물 최종 확인

| 제출물 | 파일/내용 | ✓ |
|---|---|---|
| GitHub 저장소 URL | Public인지 확인! (시크릿 창으로 열어보기) | ☐ |
| 📸 개발 환경 설정 | `docs/screenshots/env_setup.png` (Python 버전 + Git 설정) | ☐ |
| 📸 실행 결과 — 메뉴 | `docs/screenshots/menu.png` | ☐ |
| 📸 실행 결과 — 퀴즈 풀기 | `docs/screenshots/play.png` | ☐ |
| 📸 실행 결과 — 퀴즈 추가 | `docs/screenshots/add_quiz.png` | ☐ |
| 📸 실행 결과 — 점수 확인 | `docs/screenshots/score.png` | ☐ |
| 📸 `git log --oneline --graph` | `docs/screenshots/git_graph.png` | ☐ |
| 스크린샷이 push되었는가 | GitHub 웹에서 README 이미지가 보이는지 확인 | ☐ |

> [!CAUTION]
> **제출 전 마지막 3가지**
> 1. `git status`가 clean인가? (커밋 안 한 코드가 남아 있으면 채점자는 못 봅니다)
> 2. `git push` 했는가? (로컬에만 있으면 없는 것과 같습니다)
> 3. **시크릿 브라우저 창**으로 저장소 URL을 열어보세요. Private이면 채점자가 못 봅니다.

---

# 부록 A. 자주 겪는 오류와 해결법

## Python 오류

| 오류 메시지 | 원인 | 해결 |
|---|---|---|
| `IndentationError: unexpected indent` | 들여쓰기 불일치 (탭/스페이스 혼용) | 에디터에서 스페이스 4칸으로 통일 |
| `NameError: name 'Quiz' is not defined` | 클래스 정의보다 사용이 먼저 | 정의를 위로 옮기거나 `import` 확인 |
| `TypeError: __init__() missing 1 required positional argument` | 인자 개수 불일치 | `Quiz(q, c, a)` 3개를 넘겼는지 확인 |
| `IndexError: list index out of range` | 1-based/0-based 혼동 | `choices[answer - 1]` 인지 확인 |
| `AttributeError: 'dict' object has no attribute 'question'` | `from_dict`로 변환하지 않고 dict를 그대로 씀 | `Quiz.from_dict(d)` 로 변환 후 사용 |
| `json.decoder.JSONDecodeError` | 파일이 깨졌거나 빈 파일 | 이건 **정상** — Step 5의 except가 잡아야 함 |
| `UnicodeDecodeError: 'cp949' codec...` | Windows에서 `encoding="utf-8"` 누락 | 모든 `open()`에 `encoding="utf-8"` 추가 |
| `TypeError: Object of type Quiz is not JSON serializable` | Quiz 객체를 그대로 `json.dump` | `q.to_dict()`로 변환 후 저장 |
| 콘솔에 이모지가 `?`로 깨짐 (Windows) | 콘솔 코드페이지 문제 | `chcp 65001` 실행 또는 Windows Terminal 사용 |
| 프로그램이 메시지를 무한 출력 | `except:`가 EOFError를 삼킴 | [Step 2-1의 CAUTION](#2-1--개념-두-종류의-잘못된-입력) 참조 |
| 저장했는데 다음 실행에 안 보임 | 상대 경로 사용 + 다른 위치에서 실행 | `Path(__file__).resolve().parent` 사용 |

## Git 오류

| 오류 메시지 | 원인 | 해결 |
|---|---|---|
| `fatal: not a git repository` | `git init` 안 함 / 다른 폴더에 있음 | `pwd`로 위치 확인 후 `git init` |
| `src refspec main does not match any` | 커밋이 하나도 없음 | 먼저 `git add` → `git commit` |
| `! [rejected] main -> main (fetch first)` | 원격에 내가 없는 커밋 존재 | `git pull --rebase origin main` 후 push. **양쪽에 같은 파일이 있으면 충돌이 나므로** [Step 0-4의 WARNING](#0-4-github-저장소-생성) 절차대로 해결까지 진행 |
| `Please tell me who you are` | `user.name`/`user.email` 미설정 | Step 0-2 실행 |
| `Your local changes would be overwritten by merge` | 커밋 안 한 변경 존재 | `git commit` 또는 `git stash` 후 pull |
| `remote: Support for password authentication was removed` | 비밀번호 인증 폐지 | **Personal Access Token** 발급해서 비밀번호 자리에 입력 (GitHub → Settings → Developer settings → PAT) |
| `git log --graph`가 일직선 | fast-forward 병합됨 | 다음 병합부터 `git merge --no-ff` 사용 |
| `__pycache__`가 자꾸 커밋됨 | `.gitignore` 추가 전에 이미 추적됨 | `git rm -r --cached __pycache__` 후 커밋 |

> [!TIP]
> **커밋을 잘못했을 때 (아직 push 전이라면)**
> ```bash
> git commit --amend -m "새 메시지"   # 직전 커밋 메시지만 수정
> git reset --soft HEAD~1            # 직전 커밋 취소 (변경 내용은 유지)
> ```
> ⚠️ **이미 push한 커밋에는 사용하지 마세요.** 히스토리가 꼬입니다.

---

# 부록 B. Git 명령어 치트시트

```bash
# ── 확인 (자주 쓰세요) ────────────────────────────
git status                      # 현재 변경 상태
git log --oneline               # 커밋 목록 한 줄로
git log --oneline --graph --all # 브랜치 그래프 포함
git diff                        # 아직 add 안 한 변경 내용
git branch                      # 브랜치 목록 (* = 현재)
git remote -v                   # 원격 저장소 주소

# ── 기본 흐름 ────────────────────────────────────
git add <파일>                   # 스테이징 (git add . = 전부)
git commit -m "Feat: 설명"       # 커밋 (스냅샷 저장)
git push                        # 원격으로 업로드
git pull                        # 원격에서 다운로드 + 병합

# ── 브랜치 ───────────────────────────────────────
git checkout -b feat/기능명       # 브랜치 생성 + 이동
git checkout main               # 브랜치 이동
git merge --no-ff feat/기능명     # 병합 (기록 보존)
git branch -d feat/기능명         # 병합 끝난 브랜치 삭제

# ── 저장소 ───────────────────────────────────────
git init                        # 새 저장소 만들기
git clone <URL> [폴더명]          # 기존 저장소 복제
git remote add origin <URL>     # 원격 저장소 연결
```

### 🧠 Git의 3단계 영역

```
작업 디렉터리        스테이징 영역        저장소(.git)         원격(GitHub)
 (내가 편집)   add→   (커밋 후보)  commit→  (기록 확정)  push→  (공유)
     ↑                                                          │
     └──────────────────── pull / clone ────────────────────────┘
```

---

# 부록 C. 커밋 로드맵 전체 표

목표: **의미 있는 커밋 10개 이상.** 아래를 그대로 따라가면 16개가 됩니다.

> [!IMPORTANT]
> 이 표는 **나중에 몰아서 실행하는 목록이 아닙니다.** 각 커밋은 본문의 🔀 표시가 나온 그 자리에서
> 하나씩 실행해야 합니다. 코드를 다 짜놓고 아래 커밋 명령을 연달아 실행하면 첫 번째 커밋이
> 변경분을 전부 가져가고 나머지는 `nothing to commit`으로 만들어지지 않습니다.

| # | Step | 커밋 메시지 | 브랜치 | 사용 Git 명령어 |
|---|---|---|---|---|
| 1 | 0 | `Chore: 프로젝트 초기 설정 및 .gitignore 추가` | main | `init` `add` `commit` `push` |
| 2 | 1 | `Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)` | main | `add` `commit` |
| 3 | 1 | `Feat: 자료구조 주제 기본 퀴즈 데이터 5개 추가` | main | `add` `commit` `push` |
| 4 | 2 | `Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현` | main | `add` `commit` |
| 5 | 2 | `Feat: 메인 메뉴 루프 및 KeyboardInterrupt/EOFError 안전 종료 처리` | main | `add` `commit` `push` |
| 6 | 3 | `Feat: 퀴즈 출제 및 정답 채점 기능 구현` | feat/play-quiz | `checkout -b` `add` `commit` |
| 7 | 3 | `Feat: 최고 점수 비교 및 갱신 로직 추가` | feat/play-quiz | `add` `commit` `push` |
| 8 | 3 | `Merge: 퀴즈 풀기 기능 병합` | main | `checkout` `merge --no-ff` `push` |
| 9 | 4 | `Feat: 퀴즈 추가 기능 및 입력 유효성 검사 구현` | main | `add` `commit` |
| 10 | 4 | `Feat: 퀴즈 목록 조회 기능 구현 (빈 목록 처리 포함)` | main | `add` `commit` |
| 11 | 4 | `Feat: 최고 점수 확인 기능 구현 (미기록 상태 처리)` | main | `add` `commit` `push` |
| 12 | 5 | `Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False)` | main | `add` `commit` |
| 13 | 5 | `Feat: state.json 불러오기 및 파일 부재/손상 시 자동 복구 처리` | main | `add` `commit` |
| 14 | 5 | `Refactor: Quiz/QuizGame/storage 모듈 분리` *(선택)* | main | `add` `commit` |
| 15 | 5 | `Docs: README 6대 항목 및 실행 화면 스크린샷 추가` | main | `add` `commit` `push` |
| 16 | 6 | `Docs: README에 학습 회고 추가` | main (복제본) | `clone` `add` `commit` `push` → 원본에서 `pull` |

✅ 7종 전부 커버: `init`(1) · `add`(전체) · `commit`(전체) · `push`(1,3,5…) · `checkout`(6,8) · `clone`(16) · `pull`(16) · *보너스* `merge`(8)

---

# 부록 D. 학습 목표 자가 점검 질문

> 미션을 마친 뒤, **코드를 보지 않고** 아래 질문에 소리 내어 답해보세요.
> 막히는 질문이 있다면 그 부분을 다시 학습하면 됩니다. 이것이 진짜 완료 조건입니다.

### Python 기초
1. `self.quizzes`와 `quizzes`는 무엇이 다른가?
2. `int`, `str`, `bool`, `list`, `dict`를 이 프로젝트의 **내 코드에서** 각각 하나씩 예로 들어보시오.
3. 메뉴 루프에는 왜 `while`을 쓰고, 문제 출제에는 왜 `for`를 썼는가?
4. `ask_int()`가 값을 `return`하지 않고 `print`만 한다면 무슨 일이 생기는가?
5. `if not raw:` 는 어떤 경우에 참이 되는가?

### 클래스와 객체
6. `Quiz` 클래스를 안 쓰고 리스트 3개로 만들었다면 어떤 문제가 생겼을까?
7. `__init__`은 언제 실행되는가? 내가 직접 호출한 적이 있는가?
8. `self`를 매개변수에서 빼면 어떤 오류가 나는가? 왜인가?
9. `Quiz`와 `QuizGame`의 **책임**은 각각 무엇인가? 왜 나눴는가?
10. `to_dict()`는 왜 `Quiz` 안에 있고 `QuizGame` 안에 있지 않은가?

### 파일 입출력
11. `with open(...)`을 쓰면 무엇이 자동으로 처리되는가?
12. JSON을 쓰지 않고 그냥 텍스트로 저장했다면 무엇이 번거로웠을까?
13. `ensure_ascii=False`를 빼면 파일이 어떻게 보이는가? 프로그램은 여전히 동작하는가?
14. "파일이 없는 경우"와 "파일이 손상된 경우"의 처리가 왜 달라야 하는가?
15. `except ValueError:` 대신 `except:`를 쓰면 어떤 사고가 나는가?

### Git
16. Git이 없었다면 이 프로젝트에서 무엇이 불편했을까?
17. `add`와 `commit`은 왜 두 단계로 나뉘어 있는가?
18. `commit`과 `push`의 차이는? 커밋만 하고 push를 안 하면 어떻게 되는가?
19. `git clone`과 `git pull`은 각각 언제 쓰는가?
20. `--no-ff` 옵션을 붙인 이유를 그래프 모양으로 설명할 수 있는가?
21. 브랜치를 나눠 작업하면 무엇이 좋은가? 혼자 하는 프로젝트에도 의미가 있는가?

---

## 🎓 마치며

이 미션을 끝내고 나면 여러분은 이렇게 말할 수 있게 됩니다.

> "저는 파이썬으로 **동작하는 프로그램 하나를 처음부터 끝까지** 만들어봤습니다.
> 클래스로 역할을 나눴고, 사용자가 어떤 이상한 입력을 해도 죽지 않게 만들었고,
> 데이터를 파일에 저장해 프로그램을 껐다 켜도 유지되게 했습니다.
> 그리고 그 과정을 **16개의 커밋과 하나의 브랜치**로 기록했습니다."

문법을 아는 것과 프로그램을 완성하는 것의 차이 — 그 차이를 직접 만들어보세요. 🚀
