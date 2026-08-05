# 📋 자료구조 터미널 퀴즈 게임 — 종합 학습·구현·제출 체크리스트

> 기준 문서: [과제 원문](reference.md), [학습 가이드](learning_guide.md), [README 요구사항](readme_requirements_list.md), [프로젝트 README](../README.md)
>
> 이 문서는 40시간 미션의 요구사항을 실행 가능한 최소 단위로 분해한 체크리스트입니다. 체크는 **실제 코드·명령 실행·Git 이력·스크린샷으로 확인한 뒤에만** 완료합니다. README에 적힌 “구현 목표”나 계획만으로는 완료 처리하지 않습니다.

## 0. 범위·완료 기준

- [ ] Python 3.10 이상으로 동작하는 터미널 기반 4지선다 **자료구조(Data Structure) 퀴즈 게임**을 완성한다.
- [ ] 메뉴에서 번호를 선택했을 때 퀴즈 풀기·추가·목록·점수 확인·종료 화면이 각각 동작한다.
- [ ] 자료구조 주제의 퀴즈를 5개 이상 포함하고, 각 퀴즈가 문제·선택지 4개·정답 번호를 가진다.
- [ ] 프로그램을 종료한 뒤 다시 실행해도 추가한 퀴즈와 최고 점수가 유지된다.
- [ ] 최소 두 개의 클래스(권장: `Quiz`, `QuizGame`)로 책임을 나누고, 입력·게임 진행·저장 로직을 메서드 또는 모듈로 분리한다.
- [ ] 프로젝트 루트의 `state.json`에서 UTF-8로 퀴즈와 점수를 읽고 쓴다.
- [ ] 외부 패키지 없이 Python 표준 라이브러리만 사용한다.
- [ ] 프로젝트 코드를 Public GitHub 저장소에 업로드한다.
- [ ] 기능 단위의 의미 있는 커밋을 10개 이상 남긴다.
- [ ] 기능 브랜치 생성 및 병합 이력을 1회 이상 남긴다.
- [ ] `clone`과 `pull`을 각각 1회 이상 실제로 사용한 이력을 남긴다.
- [ ] README에 프로젝트 개요, 주제 선정 이유, 실행 방법, 기능 목록, 파일 구조, 데이터 파일 설명의 6대 항목을 모두 작성한다.
- [ ] `pip install` 또는 제3자 패키지 없이 구현하고, `json`, `pathlib`, `random` 등 필요한 표준 라이브러리만 사용한다.

> [!NOTE]
> 현재 README는 실행 소스·실행 캡처가 아직 없는 상태를 “구현 목표”로 표시합니다. 이 체크리스트를 수행하면서 파일과 증빙이 실제로 생긴 경우에만 README의 상태 설명도 갱신합니다.

> [!CAUTION]
> 문서 작성 시점의 저장소에는 실행 소스(`main.py`, `quiz.py`, `quiz_game.py`, `storage.py`), `.gitignore`, `state.json`, `docs/screenshots/`가 아직 없습니다. `docs/image.png`은 개발 환경 증빙으로만 사용할 수 있습니다. 실제 파일·이력·캡처가 없으면 관련 체크를 완료 처리하지 않습니다.

### 모든 기능 커밋에 적용할 공통 규율

- [ ] 각 기능을 끝낸 **그 시점**에 `git status`로 변경 파일을 확인한다.
- [ ] 해당 기능에 필요한 파일만 `git add <파일>`로 스테이징한다.
- [ ] `git diff --cached`로 다음 커밋에 들어갈 변경을 검토한다.
- [ ] 지정된 변경 요약 메시지로 `git commit -m "..."`을 만든다.
- [ ] 코드를 모두 작성한 뒤 커밋 명령만 연속 실행하지 않는다. 첫 커밋이 변경분을 모두 가져가면 나머지 커밋은 `nothing to commit`이 된다.
- [ ] 이미 변경을 몰아 작성했다면 `git add -p`로 변경 덩어리를 나누거나 이후의 실제 기능 단위에서 커밋을 더 세분화한다.
- [ ] `git commit --allow-empty` 또는 내용 없는 커밋으로 커밋 수만 늘리지 않는다.

---

## 1. Step 0 — 개발 환경 설정과 Git 저장소 초기화

### 1-1. Python·Git 개발 환경

- [ ] macOS/Linux에서 `python3 --version`을 실행해 Python 3.10 이상인지 확인한다. 
Python 3.12.3
- [ ] `git --version`을 실행해 Git 설치를 확인한다.
git version 2.43.0
- [ ] `git config --global user.name "내이름"`으로 커밋 작성자 이름을 설정한다.
- [ ] `git config --global user.email "GitHub가입이메일"`으로 GitHub 계정과 연결할 이메일을 설정한다.
- [ ] `git config --global init.defaultBranch main`으로 기본 브랜치 이름을 `main`으로 설정한다.
- [ ] `git config --global --list`을 실행해 이름·이메일·기본 브랜치 설정을 확인한다.
- [ ] Python 버전, Git 버전, Git 전역 설정이 한 화면에 보이도록 캡처한다.
- [ ] 개발 환경 캡처를 `docs/screenshots/env_setup.png`으로 저장하거나, 기존 `docs/image.png`를 README에 연결할 때는 파일 경로와 설명이 일치하는지 확인한다.

### 1-2. 주제와 기본 문제 준비

- [ ] 퀴즈 주제를 **자료구조(Data Structure)**로 확정한다.
- [ ] README에 쓸 첫 번째 선정 이유를 메모한다: LIFO·FIFO처럼 정답이 명확해 객관적인 4지선다에 적합하다.
- [ ] README에 쓸 두 번째 선정 이유를 메모한다: 프로그램 안의 `list`·`dict`·JSON 사용과 학습 주제가 연결된다.
- [ ] README에 쓸 세 번째 선정 이유를 메모한다: 스택·큐·해시 테이블·트리·복잡도는 오래 쓰이는 CS 기초 지식이다.
- [ ] 각 문제에 문제 문장, 선택지 정확히 4개, 정답 번호 1~4를 미리 작성한다.
- [ ] 스택(Stack)의 LIFO를 검증하는 기본 문제를 준비한다.
- [ ] 큐(Queue)의 FIFO를 검증하는 기본 문제를 준비한다.
- [ ] BFS가 큐를 사용한다는 점 또는 해시 함수의 역할을 검증하는 기본 문제를 준비한다.
- [ ] 정렬된 배열의 이진 탐색 시간 복잡도 `O(log n)`을 검증하는 기본 문제를 준비한다.
- [ ] 해시 테이블 평균 탐색 또는 리스트 인덱스 접근의 `O(1)`을 검증하는 기본 문제를 준비한다.
- [ ] 선택지 순서가 바뀌면 `answer` 번호도 함께 바뀌었는지 확인한다. 예를 들어 FIFO가 1번이면 정답은 1, FIFO가 2번이면 정답은 2여야 한다.

### 1-3. GitHub·로컬 저장소

- [ ] GitHub에서 새 저장소를 생성한다.
- [ ] 저장소 공개 범위를 **Public**으로 설정한다.
- [ ] 새 저장소를 만들 때 “Add a README file”를 선택하지 않는다. 이미 로컬 README가 있으면 첫 push 전 add/add 충돌이 날 수 있다.
- [ ] 프로젝트 루트에서 `git init`을 실행한다.
- [ ] `git branch -M main`으로 로컬 기본 브랜치 이름을 `main`으로 맞춘다.
- [ ] `git status`로 현재 작업 트리 상태를 확인한다.
- [ ] `git remote add origin <저장소URL>`을 실행해 원격 저장소를 연결한다.
- [ ] `git remote -v`로 fetch·push URL이 예상한 저장소인지 확인한다.
- [ ] GitHub에서 README를 미리 만든 원격 저장소를 유지해야 한다면, 첫 push 전에 `git pull --rebase origin main`을 실행한다.
- [ ] add/add 충돌이 나면 `README.md`의 `<<<<<<<`, `=======`, `>>>>>>>` 표시를 제거하고 필요한 내용만 남긴다.
- [ ] 충돌을 해결한 뒤 `git add README.md` → `git rebase --continue` → `git push -u origin main` 순서로 진행한다.
- [ ] rebase가 꼬였을 때는 `git rebase --abort`로 rebase 시작 전 상태로 되돌린 뒤 원인을 다시 확인한다.

### 1-4. .gitignore와 README 초안

- [ ] 프로젝트 루트에 `.gitignore`를 만든다.
- [ ] `__pycache__/`, `*.py[cod]`를 `.gitignore`에 추가한다.
- [ ] `.venv/`, `venv/` 등 가상환경 경로를 `.gitignore`에 추가한다.
- [ ] `.vscode/`, `.idea/` 등 에디터 설정 파일을 `.gitignore`에 추가한다.
- [ ] `.DS_Store`, `Thumbs.db` 등 운영체제 파일을 `.gitignore`에 추가한다.
- [ ] 실행 중 변하는 `state.json`을 `.gitignore`에 추가한다.
- [ ] 손상 파일 백업본 `state.json.bak`을 `.gitignore`에 추가한다.
- [ ] `state.json`을 의도적으로 Git 추적할 선택을 했다면, 동적 실행 데이터가 커밋마다 바뀐다는 단점과 선택 이유를 README에 명시한다.
- [ ] 루트 `README.md`에 6대 필수 섹션의 제목을 먼저 만든다.
- [ ] README에 동적 실행 데이터는 Git 이력 오염을 막기 위해 추적 제외한다는 이유를 기록한다.

### 1-5. 첫 번째 Git 체크포인트

- [ ] `git add .gitignore README.md`로 초기 설정 파일만 스테이징한다.
- [ ] `git commit -m "Chore: 프로젝트 초기 설정 및 .gitignore 추가"`로 변경 이유가 드러나는 첫 커밋을 만든다.
- [ ] `git push -u origin main`으로 `main`을 원격에 연결하고 push한다.
- [ ] GitHub 웹 페이지에서 `.gitignore`와 `README.md`, 첫 번째 커밋이 보이는지 확인한다.

---

## 2. Step 1 — Quiz 모델과 자료구조 기본 데이터

### 2-1. Quiz 클래스 설계

- [ ] `Quiz` 클래스를 정의해 퀴즈 한 문제를 표현한다.
- [ ] `__init__(self, question, choices, answer)`에서 `question`을 문제 문자열로 저장한다.
- [ ] `__init__(self, question, choices, answer)`에서 `choices`를 선택지 목록으로 저장한다.
- [ ] `__init__(self, question, choices, answer)`에서 `answer`를 정답 번호로 저장한다.
- [ ] `choices`가 선택지 4개라는 규칙을 생성·입력·불러오기 전 과정에서 유지한다.
- [ ] `answer`를 사용자에게 보이는 1~4 범위의 번호로 일관되게 저장한다.
- [ ] 사용자 입력 1~4와 Python 리스트 인덱스 0~3을 혼동하지 않는다.
- [ ] 정답 선택지를 꺼낼 때만 `choices[answer - 1]`처럼 1-based 값을 0-based 인덱스로 변환한다.
- [ ] 0을 정답 번호로 저장하거나 `choices[answer]`로 잘못 접근하지 않는지 확인한다.

### 2-2. Quiz 메서드

- [ ] `display(self, number=None)`를 구현한다.
- [ ] `number`가 전달되면 `[문제 3]`처럼 문제 번호를 함께 출력한다.
- [ ] `display()`가 문제 문장을 출력한다.
- [ ] `display()`가 `enumerate(..., start=1)` 또는 동등한 방식으로 선택지를 `1. ...`부터 `4. ...`까지 출력한다.
- [ ] `is_correct(self, user_answer)`가 입력 번호와 `self.answer`를 비교한다.
- [ ] `is_correct()`가 정답이면 `True`, 오답이면 `False`를 반환한다.
- [ ] `to_dict(self)`가 `question`, `choices`, `answer` 키를 가진 JSON 호환 `dict`를 반환한다.
- [ ] `@classmethod from_dict(cls, data)`를 정의한다.
- [ ] `from_dict()`가 `data["question"]`, `data["choices"]`, `data["answer"]`를 사용해 `Quiz` 객체를 복원한다.
- [ ] `Quiz.from_dict(quiz.to_dict())` 후 문제·선택지·정답이 동일한지 확인한다.
- [ ] `get_default_quizzes()`가 raw `dict` 목록이 아니라 `Quiz(question, choices, answer)` 인스턴스의 `list`를 반환하는지 확인한다.
- [ ] 기본 퀴즈 각각에 문자열 문제 1개, 문자열 선택지 정확히 4개, `int` 정답 번호 1~4가 있는지 확인한다.

### 2-3. 기본 퀴즈 함수와 단위 확인

- [ ] `get_default_quizzes()` 함수를 작성한다.
- [ ] `state.json`이 없거나 손상됐을 때 `get_default_quizzes()`가 사용할 기본 데이터의 출처가 되게 한다.
- [ ] 함수가 `Quiz` 인스턴스 5개 이상을 반환한다.
- [ ] 각 기본 퀴즈가 자료구조 주제이며, 선택지 4개와 정답 번호 1~4를 가진다.
- [ ] 스택 문제의 정답이 LIFO와 일치하는지 확인한다.
- [ ] 큐 문제의 정답이 FIFO와 일치하는지 확인한다.
- [ ] 해시 테이블/해시 함수 문제의 정답이 선택지와 일치하는지 확인한다.
- [ ] 해시 테이블 또는 해시 함수의 핵심 개념을 검증하는 기본 문제가 최소 1개 있는지 확인한다.
- [ ] 이진 탐색 트리(BST) 문제의 정답이 왼쪽·오른쪽 서브트리 규칙과 일치하는지 확인한다.
- [ ] 시간 복잡도 문제의 정답이 `O(1)` 또는 `O(log n)` 설명과 일치하는지 확인한다.
- [ ] `if __name__ == "__main__":` 블록에서 기본 퀴즈 개수, `display()`, `is_correct()`, `to_dict()`를 임시로 확인한다.
- [ ] 임시 테스트 코드가 나중에 import될 때 자동 실행되지 않는지 확인한다.

### 2-4. Step 1 Git 체크포인트

- [ ] `git add main.py` 또는 실제 변경 파일을 스테이징한다.
- [ ] `git commit -m "Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)"`으로 커밋 #2를 만든다.
- [ ] 기본 퀴즈 5개 이상을 추가한 뒤 `git add main.py` 또는 실제 변경 파일을 스테이징한다.
- [ ] `git commit -m "Feat: 자료구조 주제 기본 퀴즈 데이터 5개 추가"`으로 커밋 #3을 만든다.
- [ ] `git push`로 커밋 #3을 원격에 반영한다.
- [ ] `git log --oneline`에서 커밋 #2와 #3이 서로 다른 의미 있는 변경으로 남았는지 확인한다.

---

## 3. Step 2 — QuizGame, 메뉴, 공통 입력과 안전 종료

### 3-1. QuizGame의 책임과 초기 상태

- [ ] `QuizGame` 클래스를 정의해 게임 전체 흐름을 관리한다.
- [ ] `__init__(self)`에서 `self.quizzes`를 기본 퀴즈 또는 불러온 퀴즈 목록으로 초기화한다.
- [ ] `__init__(self)`에서 `self.best_score`를 초기화하거나 저장 파일에서 불러온다.
- [ ] 최고 기록의 정답 수와 전체 문제 수도 보여 줄 계획이면 `best_correct`·`best_total`도 초기화한다.
- [ ] 메뉴 표시, 퀴즈 풀기, 추가, 목록, 점수 확인, 저장, 불러오기를 별도 메서드로 분리한다.
- [ ] 모든 코드를 하나의 함수에 몰아넣지 않는다.

### 3-2. ask_int: 숫자 입력 재시도 규칙

- [ ] `ask_int(self, prompt, low, high)`를 구현한다.
- [ ] `input(prompt).strip()`으로 앞뒤 공백을 제거한다.
- [ ] `"  2  "` 입력이 숫자 2로 처리되는지 확인한다.
- [ ] 공백 제거 뒤 빈 문자열이면 안내 문구를 출력하고 같은 입력 단계로 돌아간다.
- [ ] `int(raw)` 변환은 `try/except ValueError`로 감싼다.
- [ ] 유효한 숫자와 범위가 확인되면 `ask_int()`가 `int` 값을 `return`하는지 확인한다.
- [ ] `abc` 같은 문자 입력에서 `ValueError`를 안내하고 재입력받는다.
- [ ] `1.5` 같은 소수 입력에서 `ValueError`를 안내하고 재입력받는다.
- [ ] 숫자가 `low` 미만이면 허용 범위를 안내하고 재입력받는다.
- [ ] 숫자가 `high` 초과면 허용 범위를 안내하고 재입력받는다.
- [ ] 메뉴에서 0, -1, 9를 입력했을 때 프로그램이 종료·오작동하지 않고 재입력으로 돌아가는지 확인한다.
- [ ] 정답 입력에서 0 또는 5를 입력했을 때 1~4 범위를 안내하고 재입력받는지 확인한다.
- [ ] `except:` 또는 `except Exception:`으로 `KeyboardInterrupt`·`EOFError`까지 무심코 삼키지 않는다.
- [ ] `KeyboardInterrupt`와 `EOFError`는 상위 `main()`의 안전 종료 처리로 전달되게 한다.

### 3-3. ask_text, 메뉴, 실행 루프

- [ ] `ask_text(self, prompt)`를 구현한다.
- [ ] `ask_text()`가 `raw = input(prompt).strip()`으로 공백을 제거하고, 빈 문자열이면 안내 후 `continue`, 유효한 문자열이면 `return raw` 하는지 확인한다.
- [ ] `show_menu(self)`가 1. 퀴즈 풀기, 2. 퀴즈 추가, 3. 퀴즈 목록, 4. 점수 확인, 5. 종료를 모두 출력한다.
- [ ] 메뉴에 자료구조 퀴즈 게임임을 알 수 있는 제목을 출력한다.
- [ ] `run(self)`에 `while` 루프를 두어 종료 전까지 메뉴를 반복한다.
- [ ] 메뉴 선택에 `ask_int("선택: ", 1, 5)` 또는 동등한 범위 검증을 사용한다.
- [ ] 선택 1이 `play_quiz()`, 2가 `add_quiz()`, 3이 `show_quiz_list()`, 4가 `show_score()`로 분기하는지 확인한다.
- [ ] 선택 5에서 현재 상태를 저장할 수 있는 범위에서 저장하고 루프를 끝내는지 확인한다.

### 3-4. Ctrl+C·EOF 안전 종료

- [ ] 최상위 `main()` 또는 동등한 진입점에서 `KeyboardInterrupt`를 처리한다.
- [ ] Ctrl+C가 발생하면 Python Traceback 대신 안내 메시지를 출력한다.
- [ ] Ctrl+C 발생 시 가능한 범위에서 `save_state()`를 호출한 뒤 종료한다.
- [ ] 최상위에서 `EOFError`를 처리한다.
- [ ] Ctrl+D, 닫힌 표준 입력, 파이프 입력에서 무한 재입력 루프가 생기지 않는지 확인한다.
- [ ] `echo "" | python main.py` 또는 Python 3에 맞는 명령으로 EOF 종료를 직접 시험한다.

### 3-5. 입력 예외 9종 실습과 Git 체크포인트

- [ ] 메뉴 1~5 각각이 정상 분기하는지 확인한다.
- [ ] 앞뒤 공백이 있는 메뉴 입력을 확인한다.
- [ ] `abc` 입력을 확인한다.
- [ ] 9 입력을 확인한다.
- [ ] 0 입력과 -1 입력을 확인한다.
- [ ] Enter만 누른 빈 입력을 확인한다.
- [ ] `1.5` 입력을 확인한다.
- [ ] Ctrl+C 안전 종료를 확인한다.
- [ ] EOF 또는 파이프 입력 안전 종료를 확인한다.
- [ ] `git commit -m "Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현"`으로 커밋 #4를 만든다.
- [ ] `git commit -m "Feat: 메인 메뉴 루프 및 KeyboardInterrupt/EOFError 안전 종료 처리"`으로 커밋 #5를 만든다.
- [ ] 커밋 #5까지 `git push`를 실행한다.
- [ ] 필요하면 잘못된 입력 화면을 `docs/screenshots/invalid_input.png`으로 캡처한다.

---

## 4. Step 3 — feat/play-quiz 브랜치와 퀴즈 풀기

### 4-1. 브랜치 생성과 작업 분리

- [ ] 퀴즈 풀기 코드를 작성하기 **전** `git checkout -b feat/play-quiz`을 실행한다.
- [ ] 브랜치를 만들기 전 `git status`가 의도하지 않은 변경 없이 정리됐는지 확인하고, 필요한 기존 커밋을 `git push`한다.
- [ ] `git branch --show-current`으로 현재 브랜치가 `feat/play-quiz`인지 확인한다.
- [ ] 퀴즈 풀기와 최고 점수 작업을 `main`이 아닌 기능 브랜치에서 수행한다.

### 4-2. play_quiz 구현

- [ ] `play_quiz(self)`를 구현한다.
- [ ] `self.quizzes`가 비어 있으면 “등록된 퀴즈가 없습니다”와 동등한 안내를 출력하고 즉시 반환한다.
- [ ] 퀴즈가 0개일 때 `correct / total` 계산으로 ZeroDivisionError가 나지 않는지 확인한다.
- [ ] 저장된 퀴즈를 하나씩 출제하고 각 문제의 번호·문장·선택지 4개를 표시한다.
- [ ] 각 퀴즈에 `quiz.display(number)` 또는 동등한 출력을 호출한다.
- [ ] 각 문제의 답을 `ask_int(..., 1, 4)`로 입력받는다.
- [ ] `quiz.is_correct(user_answer)`로 정답을 판정한다.
- [ ] 정답일 때 즉시 정답 안내를 출력하고 `correct += 1`로 정답 수를 증가시킨다.
- [ ] 오답일 때 즉시 오답 안내와 실제 정답 선택지(예: `choices[answer - 1]`)를 출력한다.
- [ ] 모든 문제를 푼 뒤 정답 수와 전체 문제 수를 함께 출력한다.
- [ ] 점수를 `round(correct / total * 100)` 또는 프로젝트 전체에서 일관된 100점 환산식으로 계산한다.
- [ ] 결과에 “5문제 중 4문제 정답! (80점)”처럼 정답 수와 점수를 함께 표시한다.

### 4-3. 최고 점수와 결과 저장

- [ ] 새 점수가 기존 `best_score`보다 큰 경우에만 최고 점수를 갱신한다.
- [ ] 최고 기록 갱신 시 축하 메시지를 출력한다.
- [ ] 기존 최고 점수와 같거나 낮을 때는 최고 기록을 덮어쓰지 않는지 확인한다.
- [ ] 최고 기록을 상세히 표시한다면 `best_correct`와 `best_total`도 새 최고 기록일 때 함께 갱신한다.
- [ ] 점수 갱신 후 Step 5의 `save_state()`를 연결해 재시작 후에도 최고 점수가 남게 한다.

### 4-4. 브랜치 커밋·병합·증빙

- [ ] `git commit -m "Feat: 퀴즈 출제 및 정답 채점 기능 구현"`으로 커밋 #6을 만든다.
- [ ] `git commit -m "Feat: 최고 점수 비교 및 갱신 로직 추가"`으로 커밋 #7을 만든다.
- [ ] `git push -u origin feat/play-quiz`로 기능 브랜치를 원격에 push한다.
- [ ] `git checkout main`으로 `main` 브랜치로 돌아온다.
- [ ] `git merge --no-ff feat/play-quiz -m "Merge: 퀴즈 풀기 기능 병합"`으로 fast-forward가 아닌 병합 커밋 #8을 만든다.
- [ ] `git push origin main`으로 병합 결과를 원격에 올린다.
- [ ] `git log --oneline --graph --all`에서 브랜치가 갈라졌다 병합된 그래프가 보이는지 확인한다.
- [ ] 퀴즈 출제·정오답·결과·최고 점수 갱신이 한 화면에 보이도록 `docs/screenshots/play.png`을 캡처한다.

---

## 5. Step 4 — 퀴즈 추가, 목록 조회, 점수 확인

### 5-1. add_quiz

- [ ] `add_quiz(self)`를 구현한다.
- [ ] 문제 입력에 `ask_text()`를 사용한다.
- [ ] `for` 반복문으로 선택지 1~4를 입력받는다.
- [ ] 선택지 입력 코드를 4번 복사하지 않고 반복문 또는 동등한 구조로 작성한다.
- [ ] 각 선택지 입력에 `ask_text()`를 사용해 빈 선택지를 막는다.
- [ ] 정답 번호를 `ask_int(prompt, 1, 4)`로 입력받는다.
- [ ] 문제·선택지 4개·정답 번호로 `Quiz` 객체를 생성한다.
- [ ] 새 `Quiz` 객체를 `self.quizzes`에 추가한다.
- [ ] 추가 성공 메시지를 출력한다.
- [ ] 새 퀴즈를 추가한 직후 `save_state()`를 호출한다.
- [ ] 프로그램을 종료·재시작한 뒤 추가 퀴즈가 남아 있는지 확인한다.

### 5-2. show_quiz_list

- [ ] `show_quiz_list(self)`를 구현한다.
- [ ] 퀴즈가 0개면 “등록된 퀴즈가 없습니다”와 동등한 안내를 출력하고 반환한다.
- [ ] `enumerate(self.quizzes, start=1)` 또는 동등한 방식으로 퀴즈 번호와 문제를 출력한다.
- [ ] 목록 화면에서 정답 번호나 정답 선택지를 노출하지 않는다.
- [ ] 새로 추가한 퀴즈가 목록의 총개수와 항목에 반영되는지 확인한다.

### 5-3. show_score

- [ ] `show_score(self)`를 구현한다.
- [ ] 아직 한 번도 풀지 않은 상태를 명시적으로 안내한다.
- [ ] 실제로 0점을 받은 기록과 “미풀이” 상태를 혼동하지 않도록 `best_total` 또는 별도 기록 상태를 활용한다.
- [ ] 기록이 있을 때 최고 점수, 정답 수, 전체 문제 수를 표시한다.
- [ ] 퀴즈 풀이 뒤 최고 점수 확인 메뉴에서 갱신된 기록이 표시되는지 확인한다.

### 5-4. Step 4 Git·스크린샷

- [ ] `git commit -m "Feat: 퀴즈 추가 기능 및 입력 유효성 검사 구현"`으로 커밋 #9를 만든다.
- [ ] `git commit -m "Feat: 퀴즈 목록 조회 기능 구현 (빈 목록 처리 포함)"`으로 커밋 #10을 만든다.
- [ ] `git commit -m "Feat: 최고 점수 확인 기능 구현 (미기록 상태 처리)"`으로 커밋 #11을 만든다.
- [ ] 커밋 #11까지 `git push`를 실행한다.
- [ ] 문제·선택지·정답 번호 입력과 저장 성공이 보이도록 `docs/screenshots/add_quiz.png`을 캡처한다.
- [ ] 최고 점수 또는 미기록 안내가 보이도록 `docs/screenshots/score.png`을 캡처한다.
- [ ] 데이터 로딩 문구와 1~5 메뉴가 보이도록 `docs/screenshots/menu.png`을 캡처한다.

---

## 6. Step 5 — state.json 영속성과 4대 복구 경로

### 6-1. 저장 위치와 상태 스키마

- [ ] `json`과 `Path`를 필요한 모듈에서 import한다.
- [ ] `STATE_FILE = Path(__file__).resolve().parent / "state.json"` 또는 동등한 경로 계산을 사용한다.
- [ ] 상대 경로 `open("state.json")`만 사용해 실행 위치에 따라 데이터 파일이 달라지는 문제를 피한다.
- [ ] `state.json`이 프로젝트 루트에 생성되는지 확인한다.
- [ ] 저장 데이터에 `quizzes` 키를 포함한다.
- [ ] 저장 데이터에 `best_score` 키를 포함한다.
- [ ] 상세 최고 기록을 지원하면 `best_correct`와 `best_total` 키를 포함한다.
- [ ] `quizzes`의 각 항목이 `question`, `choices`, `answer`를 가진 JSON 객체인지 확인한다.
- [ ] 저장 키 이름과 자료형을 코드·README·체크리스트에서 일관되게 유지한다.

### 6-2. save_state

- [ ] `save_state(self)`를 구현한다.
- [ ] `self.quizzes`의 각 `Quiz` 객체에 `to_dict()`를 호출해 JSON 호환 목록을 만든다.
- [ ] `json.dump(self.quizzes, ...)`처럼 `Quiz` 객체를 직접 직렬화하지 않는다.
- [ ] `with open(STATE_FILE, "w", encoding="utf-8") as file:` 형태로 파일을 연다.
- [ ] `json.dump(data, file, ensure_ascii=False, indent=2)`를 사용한다.
- [ ] `encoding="utf-8"`로 운영체제 기본 인코딩 차이에서 한글이 깨지는 일을 막는다.
- [ ] `ensure_ascii=False`로 한글이 사람이 읽기 어려운 유니코드 이스케이프만으로 저장되지 않게 한다.
- [ ] `indent=2`로 `state.json`을 사람이 검토 가능한 형식으로 저장한다.
- [ ] 쓰기 실패에 대해 `except OSError`를 처리한다.
- [ ] 저장 실패 시 안내를 출력하되 프로그램이 Traceback으로 비정상 종료하지 않는지 확인한다.

### 6-3. load_state와 복구

- [ ] `load_state(self)`를 구현한다.
- [ ] 정상 파일을 `json.load()`로 읽고 각 퀴즈 dict를 `Quiz.from_dict()`로 복원한다.
- [ ] `json.load()` 결과의 최상위 값이 `dict`인지, `data["quizzes"]`가 `list`인지 검증한다.
- [ ] 정상 파일에서 `best_score` 및 선택적 상세 점수 필드를 불러온다.
- [ ] 선택적 필드는 `int(data.get("best_score", 0))` 등 일관된 기본값·형 변환 정책으로 복원한다.
- [ ] 정상 저장 데이터를 불러온 뒤 퀴즈 개수와 최고 점수를 포함한 로드 성공 안내를 출력한다.
- [ ] **① FileNotFoundError**: 첫 실행에 `FileNotFoundError`를 처리하고 `get_default_quizzes()`의 기본 퀴즈 5개 이상으로 시작한다.
- [ ] 파일이 없는 첫 실행은 정상 흐름으로 처리하며 프로그램이 중단되지 않는지 확인한다.
- [ ] **② JSONDecodeError**: 깨진 JSON에서 `json.JSONDecodeError`를 처리하고 손상 안내를 출력한다.
- [ ] JSON이 손상됐을 때 기존 `state.json`을 가능한 범위에서 `state.json.bak`으로 백업한다.
- [ ] JSON 손상 뒤 기본 퀴즈 데이터로 복구하거나 초기화한 뒤 실행을 계속한다.
- [ ] **③ KeyError·ValueError·TypeError**: 필수 키 누락, 잘못된 정답 범위, 잘못된 자료형을 각각 방어하고 안내 뒤 기본 데이터로 복구한다.
- [ ] 읽어 온 `choices`가 4개인지, `answer`가 1~4인지 검증한다.
- [ ] **④ OSError**: 권한·읽기 오류 등 `OSError`를 처리하고 안내 뒤 기본 데이터로 복구한다.
- [ ] UTF-8 읽기 실패로 생길 수 있는 `UnicodeDecodeError`도 안내·복구 경로에서 처리되는지 확인한다.
- [ ] 백업 자체가 `OSError`로 실패해도 기본 데이터 복구와 프로그램 실행이 중단되지 않는지 확인한다.
- [ ] 파일 없음·손상·구조 이상·읽기 오류로 복구할 때 `best_score`, `best_correct`, `best_total`도 일관된 초기값으로 재설정한다.
- [ ] 복구 경로 어디에서도 빨간 Traceback으로 프로그램이 끝나지 않는지 확인한다.

### 6-4. 호출 지점과 재시작 검증

- [ ] 게임 생성 시 `load_state()`를 호출한다.
- [ ] `add_quiz()` 성공 직후 `save_state()`를 호출한다.
- [ ] 최고 점수 갱신 직후 `save_state()`를 호출한다.
- [ ] 메뉴 5번 종료와 Ctrl+C·EOF 안전 종료 시 가능한 범위에서 `save_state()`를 호출한다.
- [ ] 퀴즈를 추가하고 종료한 뒤 재실행해 데이터가 유지되는지 확인한다.
- [ ] 점수를 기록하고 재실행해 최고 기록이 유지되는지 확인한다.
- [ ] `state.json`을 잠시 이름 변경하거나 제거한 뒤 첫 실행 복구가 되는지 확인한다.
- [ ] `state.json`에 임의의 잘못된 문자열을 넣은 뒤 백업·안내·기본 데이터 복구가 되는지 확인한다.
- [ ] `{"hello": "world"}`처럼 JSON 문법은 맞지만 필수 키가 빠진 파일도 안내·백업·기본 데이터 복구가 되는지 확인한다.
- [ ] 프로젝트 상위 폴더에서 `python <프로젝트폴더>/main.py`를 실행해도 같은 프로젝트 루트의 `state.json`만 사용하는지 확인한다.
- [ ] `python -m json.tool state.json`으로 저장 파일이 유효한 JSON인지, 한글이 읽기 가능한지 확인한다.
- [ ] 복구 테스트 후 정상 데이터를 다시 만들고 손상 테스트 파일을 남기지 않는다.

### 6-5. Step 5 Git 체크포인트

- [ ] `git commit -m "Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False)"`으로 커밋 #12를 만든다.
- [ ] `git commit -m "Feat: state.json 불러오기 및 파일 부재/손상 시 자동 복구 처리"`으로 커밋 #13을 만든다.
- [ ] 파일을 분리했다면 `git commit -m "Refactor: Quiz/QuizGame/storage 모듈 분리"`으로 선택 커밋 #14를 만든다.
- [ ] 파일 입출력 커밋을 원격으로 `git push`한다.

---

## 7. Step 6 — clone과 pull 실습

### 7-1. 복제본 만들기

- [ ] 퀴즈 게임 개발과 핵심 push가 끝난 뒤 상위 폴더로 이동한다.
- [ ] clone 전 원본에서 `git status`를 확인하고, 필요한 커밋을 원격에 `git push`한 상태인지 확인한다.
- [ ] `git clone <저장소URL> quiz-clone`으로 별도 복제본을 만든다.
- [ ] `cd quiz-clone`으로 복제본 디렉터리로 이동한다.
- [ ] `ls -la`로 복제본에 프로젝트 파일이 생겼는지 확인한다.
- [ ] `git log --oneline`으로 기존 커밋 이력이 복제됐는지 확인한다.
- [ ] `git remote -v`로 복제본의 `origin`이 원격 저장소를 가리키는지 확인한다.

### 7-2. 복제본 변경을 원본으로 가져오기

- [ ] `quiz-clone/README.md`에 `## 학습 회고` 섹션을 추가한다.
- [ ] 회고에 배운 점 또는 구현 중 해결한 문제를 한 줄 이상 실제 경험으로 작성한다.
- [ ] 복제본에서 `git add README.md`를 실행한다.
- [ ] `git commit -m "Docs: README에 학습 회고 추가"`으로 커밋 #16을 만든다.
- [ ] 복제본에서 `git push origin main`을 실행한다.
- [ ] GitHub 웹에서 복제본이 push한 회고 커밋과 README 변경이 보이는지 확인한다.
- [ ] 원래 작업 디렉터리로 돌아간다.
- [ ] pull 전 `tail -n 5 README.md` 또는 동등한 명령으로 회고가 아직 없는 상태를 확인한다.
- [ ] 원본에서 `git pull origin main`을 실행한다.
- [ ] 원본 `README.md`에 복제본에서 작성한 회고가 실제로 반영됐는지 확인한다.
- [ ] `git log -3 --oneline`과 `tail -n 5 README.md`로 회고 커밋·내용이 pull 뒤 반영됐는지 확인한다.
- [ ] pull 충돌이 나면 `git status`로 충돌 파일을 확인하고, 필요한 로컬 변경을 커밋하거나 `git stash`한 뒤 다시 pull한다.
- [ ] `clone`과 `pull`이 서로 다른 사용 시점(새 복제본 생성 vs 기존 복제본 동기화)임을 설명할 수 있다.

---

## 8. Step 7 — 보너스 과제 5종

> [!NOTE]
> 아래 기능은 선택 과제입니다. 구현한 기능만 메뉴·데이터 스키마·README·테스트·커밋에 함께 반영합니다.

### 8-1. 랜덤 출제

- [ ] 원본 `self.quizzes` 순서를 바꾸지 않도록 복사본을 만든다.
- [ ] `quizzes_to_play = self.quizzes[:]`로 복사한 뒤 `random.shuffle(quizzes_to_play)`를 호출하고, 실제 출제에 `quizzes_to_play`을 사용한다.
- [ ] 같은 퀴즈를 여러 번 풀어 출제 순서가 바뀌는지 확인한다.

### 8-2. 문제 수 선택

- [ ] `ask_int()`로 풀 문제 수를 입력받는다.
- [ ] 입력 범위를 현재 퀴즈 개수 이내로 제한한다.
- [ ] `quizzes[:count]` 또는 동등한 슬라이싱으로 선택한 수만 출제한다.
- [ ] 선택한 문제 수, 전체 퀴즈 수, 점수 계산 분모가 일치하는지 확인한다.

### 8-3. 힌트

- [ ] `Quiz`에 `hint=None` 또는 동등한 선택적 힌트 속성을 추가한다.
- [ ] 기존 `state.json` 데이터와 호환되도록 `data.get("hint")` 또는 동등한 기본값 처리를 한다.
- [ ] 풀이 중 정답 입력 범위를 0~4로 확장하는 등 명시한 방법으로 힌트를 볼 수 있게 한다.
- [ ] 0 입력 시 힌트를 출력하고, 힌트 사용 시 정한 점수 감점 규칙을 실제 결과 점수에 반영한다.
- [ ] `to_dict()`와 `from_dict()`에서도 `hint`를 저장·복원한다.
- [ ] 힌트를 쓰지 않은 경우와 쓴 경우를 각각 시험한다.

### 8-4. 퀴즈 삭제

- [ ] 메뉴 6번 등 삭제 진입 방법을 명시한다.
- [ ] 삭제 기능을 추가하면 메뉴 선택 범위도 1~6으로 함께 변경한다.
- [ ] 삭제할 퀴즈 번호를 범위 검증과 함께 입력받는다.
- [ ] 삭제 전 `y/n` 재확인을 받는다.
- [ ] 승인 시 `del` 또는 동등한 방식으로 올바른 퀴즈만 삭제한다.
- [ ] 삭제 직후 `save_state()`를 호출한다.
- [ ] 재실행 뒤 삭제한 퀴즈가 돌아오지 않는지 확인한다.

### 8-5. 점수 히스토리

- [ ] `history: []` 키를 상태 스키마에 추가한다.
- [ ] 각 게임마다 날짜/시간, 푼 문제 수, 정답 수, 점수를 기록한다.
- [ ] 기존 `state.json`에 `history`가 없어도 `data.get("history", [])` 또는 동등한 마이그레이션으로 불러온다.
- [ ] 최고 점수와 모든 게임 기록의 역할을 구분해 표시한다.
- [ ] 점수 확인 화면에서 최근 기록(예: 최근 5회)을 조회하는 기능을 구현했다면 실제 히스토리와 일치하는지 확인한다.

---

## 9. README.md — 6대 필수 항목과 증빙

### 9-1. 프로젝트 개요와 주제

- [ ] README 첫 부분에 Python 3.10+ 터미널 4지선다 퀴즈 게임임을 2~3줄로 설명한다.
- [ ] Python 기본 문법, OOP, JSON 영속성, Git 워크플로우를 학습 목표로 적는다.
- [ ] 퀴즈 주제가 **자료구조(Data Structure)**임을 명시한다.
- [ ] 정답의 명확성, `list`/`dict`와의 구현상 연결, CS 기초 지식 가치의 세 가지 선정 이유를 적는다.
- [ ] 기본 제공 퀴즈 5개 이상이 문제·선택지 4개·정답 번호를 가진다는 점을 적는다.

### 9-2. 실행 방법과 기능 목록

- [ ] 요구 환경으로 Python 3.10 이상, Git, 외부 라이브러리 불필요를 적는다.
- [ ] README의 저장소 URL에 맞는 `git clone https://github.com/JmLeeRoom/codyssey_second_mission.git` 명령을 적거나, 포크한 경우 자신의 URL로 바꾼다.
- [ ] `cd codyssey_second_mission` 또는 실제 저장소 디렉터리로 이동하는 명령을 적는다.
- [ ] `python main.py` 실행 명령을 적는다.
- [ ] 일부 환경에서는 `python3 main.py`를 사용해야 함을 안내한다.
- [ ] 현재 `main.py`가 없을 때는 실행 명령을 성공한 것처럼 주장하지 않고 구현 완료 후 검증 대상임을 표시한다.
- [ ] 메뉴 1 “퀴즈 풀기”의 출제·정오답·100점 환산·최고 점수 비교·빈 목록 처리를 설명한다.
- [ ] 메뉴 2 “퀴즈 추가”의 문제·선택지 4개·정답 입력·즉시 저장·유효성 검증을 설명한다.
- [ ] 메뉴 3 “퀴즈 목록”의 번호·문제 표시와 빈 목록 처리를 설명한다.
- [ ] 메뉴 4 “점수 확인”의 최고 기록 표시와 미기록 상태 처리를 설명한다.
- [ ] 메뉴 5 “종료”의 가능한 범위 저장과 안전 종료를 설명한다.

### 9-3. 파일 구조와 클래스 설계

- [ ] 프로젝트 디렉터리 트리를 Markdown 코드 블록으로 표시한다.
- [ ] `main.py`의 진입점·안전 종료 역할을 설명한다.
- [ ] `quiz.py`의 `Quiz` 모델 역할을 설명한다.
- [ ] `quiz_game.py`의 `QuizGame` 게임 흐름·입력 검증 역할을 설명한다.
- [ ] 선택적 `storage.py`의 상태 저장·불러오기·복구 역할을 설명한다.
- [ ] `state.json`, `.gitignore`, `docs/`의 역할을 설명한다.
- [ ] 아직 없는 파일을 현재 존재하는 파일처럼 표시하지 않고 “구현 목표” 또는 “추가 예정”으로 구분한다.
- [ ] 현재 문서 목록에 `docs/learning_checklist.md`를 포함할지 실제 파일 구조와 맞춰 확인한다.

### 9-4. state.json 문서화

- [ ] 데이터 경로로 `Path(__file__).resolve().parent / "state.json"`을 사용해 실행 위치와 무관함을 설명한다.
- [ ] UTF-8, `ensure_ascii=False`, `state.json`의 역할을 설명한다.
- [ ] `quizzes`, `question`, `choices`, `answer`, `best_score`, `best_correct`, `best_total`의 JSON 스키마 예시를 제공한다.
- [ ] `answer`가 1~4 번호이고 `choices`가 4개라는 규칙을 설명한다.
- [ ] 첫 실행의 `FileNotFoundError`에서는 기본 퀴즈로 시작한다고 설명한다.
- [ ] `json.JSONDecodeError`, `KeyError`, `ValueError`, `TypeError`, `OSError` 등 손상·읽기 실패를 안내하고 복구한다고 설명한다.
- [ ] 손상 파일을 `state.json.bak`으로 백업한 뒤 기본 데이터로 복구하는 동작을 설명한다.
- [ ] `state.json`과 `state.json.bak`을 `.gitignore`에 넣는 이유를 설명한다.

### 9-5. README 이미지와 Git 증빙

- [ ] Python·Git 버전과 전역 Git 설정을 보여 주는 환경 이미지를 README에서 정상 표시한다.
- [ ] `docs/screenshots/menu.png`으로 데이터 로딩 안내와 1~5 메뉴를 증빙한다.
- [ ] `docs/screenshots/play.png`으로 문제 출제, 정오답, 결과, 최고 점수 갱신을 증빙한다.
- [ ] `docs/screenshots/add_quiz.png`으로 문제·선택지·정답 입력과 저장 성공을 증빙한다.
- [ ] `docs/screenshots/score.png`으로 최고 기록 또는 미기록 상태를 증빙한다.
- [ ] `docs/screenshots/git_graph.png`으로 `git log --oneline --graph --all` 결과를 증빙한다.
- [ ] README가 참조하는 이미지 파일이 실제로 존재하고 GitHub 웹에서 깨지지 않는지 확인한다.
- [ ] 현재 존재하지 않는 런타임 스크린샷 경로를 미리 이미지로 연결해 깨진 링크를 만들지 않는다.

### 9-6. README 문서 Git 체크포인트

- [ ] README 6대 항목과 실제 캡처를 추가한 뒤 `git add README.md docs/`를 실행한다.
- [ ] `git commit -m "Docs: README 6대 항목 및 실행 화면 스크린샷 추가"`으로 커밋 #15를 만든다.
- [ ] `git push` 후 GitHub에서 README의 표·코드 블록·이미지·상대 링크가 정상 렌더링되는지 확인한다.

---

## 10. 학습 목표와 자가 점검

### 10-1. Python 기초

- [ ] 변수가 무엇이며 왜 사용하는지 설명할 수 있다.
- [ ] `int`, `str`, `bool`, `list`, `dict`의 차이와 이 프로젝트 안의 예를 각각 말할 수 있다.
- [ ] `if/elif/else`가 메뉴 선택과 정오답 분기에 어떻게 쓰이는지 설명할 수 있다.
- [ ] 메뉴 루프에 `while`, 여러 퀴즈 출제에 `for`를 쓰는 이유를 설명할 수 있다.
- [ ] 함수를 정의하고 매개변수와 반환값을 사용하는 이유를 설명할 수 있다.
- [ ] `self.quizzes`와 지역 변수 `quizzes`의 차이를 설명할 수 있다.
- [ ] `ask_int()`가 값을 `return`하지 않고 `print`만 하면 호출자에게 어떤 문제가 생기는지 설명할 수 있다.
- [ ] `if not raw:`가 참이 되는 입력을 설명할 수 있다.

### 10-2. 클래스와 객체(OOP)

- [ ] 클래스와 객체의 차이, 그리고 `Quiz` 클래스를 쓰는 이유를 설명할 수 있다.
- [ ] 리스트 3개로 문제·선택지·정답을 따로 관리할 때 인덱스가 어긋날 위험을 설명할 수 있다.
- [ ] `__init__`이 언제 실행되고 `self`가 어떤 역할을 하는지 설명할 수 있다.
- [ ] 클래스의 속성(attribute)과 메서드(method)의 차이를 `Quiz` 또는 `QuizGame` 예로 설명할 수 있다.
- [ ] `self` 매개변수를 빼면 생길 오류와 이유를 설명할 수 있다.
- [ ] `Quiz`와 `QuizGame`의 책임을 왜 분리했는지 설명할 수 있다.
- [ ] `to_dict()`를 `Quiz`에 두는 이유와 `from_dict()`에 `@classmethod`를 쓰는 이유를 설명할 수 있다.

### 10-3. 파일 입출력과 JSON

- [ ] `with open(...)`이 파일을 열고 작업 뒤 자동으로 닫는 과정을 설명할 수 있다.
- [ ] JSON의 구조와 일반 텍스트보다 퀴즈·점수 데이터를 저장하기 좋은 이유를 설명할 수 있다.
- [ ] `try/except`로 예상 가능한 예외를 구체적으로 처리해야 하는 이유를 설명할 수 있다.
- [ ] `except ValueError:` 대신 맨몸 `except:`를 썼을 때 숨겨질 수 있는 오류를 설명할 수 있다.
- [ ] `ensure_ascii=False`를 빼면 한글 데이터가 어떻게 보이는지, 프로그램 동작과 사람 가독성의 차이를 설명할 수 있다.
- [ ] 파일 부재와 파일 손상을 서로 다른 복구 경로로 처리해야 하는 이유를 설명할 수 있다.

### 10-4. Git과 GitHub

- [ ] Git이 변경 이력을 관리하는 데 왜 필요한지 설명할 수 있다.
- [ ] 작업 디렉터리, 스테이징 영역, 로컬 저장소의 3단계 흐름을 설명할 수 있다.
- [ ] `git init`, `git add`, `git commit`, `git push`, `git pull`, `git checkout`, `git clone`의 역할을 각각 설명할 수 있다.
- [ ] `add`와 `commit`, `commit`과 `push`의 차이를 설명할 수 있다.
- [ ] `git clone`과 `git pull`의 사용 시점 차이를 설명할 수 있다.
- [ ] `--no-ff` 병합이 그래프에 병합 지점을 남기는 이유를 설명할 수 있다.
- [ ] 브랜치를 나눠 작업하는 장점과 혼자 하는 프로젝트에도 필요한 이유를 설명할 수 있다.

---

## 11. 최종 검증, 제출물, 스크린샷

### 11-1. 실제 동작 검증

- [ ] Python 3.10 이상 환경에서 `python main.py` 또는 `python3 main.py`를 실행한다.
- [ ] 외부 패키지 설치 오류 없이 메뉴가 표시되는지 확인한다.
- [ ] 메뉴 1~5가 모두 동작하는지 다시 확인한다.
- [ ] 자료구조 기본 퀴즈 5개 이상, 선택지 4개, 정답 1~4 규칙을 다시 확인한다.
- [ ] 퀴즈 추가·재시작·목록·점수 확인·삭제(구현한 경우)를 연속으로 시험한다.
- [ ] 입력 공백·빈 입력·문자·소수·범위 밖 숫자·Ctrl+C·EOF를 다시 시험한다.
- [ ] `state.json` 부재·손상·읽기/쓰기 오류의 복구 경로를 다시 시험한다.

### 11-2. Git 이력과 원격 저장소 검증

- [ ] `git log --oneline | wc -l` 결과가 의미 있는 커밋 10개 이상인지 확인한다.
- [ ] 커밋 메시지가 `Feat:`, `Fix:`, `Docs:`, `Refactor:`, `Chore:`처럼 변경 내용을 드러내는 형식인지 확인한다.
- [ ] `update`, `수정`, `commit1`처럼 작업 내용을 알 수 없는 메시지만으로 커밋하지 않는다.
- [ ] `git log --oneline --graph --all`에 `feat/play-quiz`의 병합 이력이 보이는지 확인한다.
- [ ] `git log --format="%h %s"`으로 10개 이상 커밋이 실제 기능 단위의 변경 요약 메시지인지 다시 확인한다.
- [ ] `git remote -v`로 올바른 원격 저장소가 연결돼 있는지 확인한다.
- [ ] `git status`에서 제출 직전 의도하지 않은 변경이 없는지 확인한다.
- [ ] GitHub 저장소 URL을 시크릿 창 또는 로그아웃 상태에서 열어 Public 접근이 가능한지 확인한다.
- [ ] GitHub 저장소 URL을 제출한다.
- [ ] `ls -la`로 제출해야 할 소스·README·docs·스크린샷 파일이 작업 디렉터리에 실제 있는지 확인한다.

### 11-3. 제출 증빙 스크린샷 6종

- [ ] `docs/screenshots/env_setup.png` 또는 동등한 환경 화면: Python 3.10+·Git 버전·Git 전역 설정을 증빙한다.
- [ ] `docs/screenshots/menu.png`: 데이터 로딩 안내와 1~5 메뉴를 증빙한다.
- [ ] `docs/screenshots/play.png`: 출제·정오답·100점 환산·최고 점수 갱신을 증빙한다.
- [ ] `docs/screenshots/add_quiz.png`: 문제·선택지 4개·정답 번호 입력과 성공 메시지를 증빙한다.
- [ ] `docs/screenshots/score.png`: 최고 점수와 상세 정답 수 또는 미기록 안내를 증빙한다.
- [ ] `docs/screenshots/git_graph.png`: 10개 이상 커밋과 브랜치 병합 그래프를 증빙한다.
- [ ] 모든 증빙 파일이 실제 파일 경로와 README의 Markdown 이미지 링크에서 일치하는지 확인한다.

### 11-4. 최종 제출 전 마지막 확인

- [ ] README 6대 항목이 모두 있고, 실행 방법대로 실행 가능한지 확인한다.
- [ ] GitHub 웹에서 소스 코드, README, 스크린샷이 모두 push됐는지 확인한다.
- [ ] 문서의 파일 구조·기능 설명·상태 스키마가 실제 구현과 모순되지 않는지 확인한다.
- [ ] 스크린샷·Git 이력·GitHub Public 상태가 체크리스트의 주장과 일치하는지 확인한다.
- [ ] `state.json`, `state.json.bak`, 가상환경, 캐시 파일이 실수로 커밋되지 않았는지 확인한다.
- [ ] 필요한 변경을 마지막으로 커밋·push한 뒤 `git status`가 깨끗한지 확인한다.
