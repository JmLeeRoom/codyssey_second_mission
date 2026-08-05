# Step 3 학습 노트 — feat/play-quiz 브랜치와 퀴즈 풀기

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "4. Step 3 — feat/play-quiz 브랜치와 퀴즈 풀기" 체크리스트를 바탕으로, 기능 브랜치 분리와 퀴즈 채점·최고 점수 로직이 왜 지금과 같은 모습으로 구현됐는지 풀어 쓴 학습 자료입니다. [Step 0](step0_dev_environment_git_init.md) → [Step 1](step1_quiz_model.md) → [Step 2](step2_quizgame_menu.md)에 이어지는 시리즈의 네 번째 문서입니다.
>
> 이 문서는 실제 `main.py`·`storage.py` 코드와, 이 저장소에서 직접 실행해 확인한 명령 결과·터미널 로그를 근거로 작성했습니다. Step 2 학습 노트가 남겨뒀던 숙제(`best_correct`/`best_total` 미저장 문제)가 이번에 실제로 풀린 지점, 그리고 Step 1·2에서 반복됐던 "커밋이 계획대로 나뉘지 않는" 패턴이 이번에 세 번째로 반복된 지점까지 숨기지 않고 그대로 짚습니다.

## 목차

- 4-1. 브랜치 생성과 작업 분리
- 4-2. play_quiz 구현
- 4-3. 최고 점수와 결과 저장
- 4-4. 브랜치 커밋·병합·증빙

---

## 4-1. 브랜치 생성과 작업 분리

### 기능 브랜치가 필요한 이유

Step 2까지는 `main` 브랜치 위에서 바로 작업을 이어왔지만, Step 3부터는 사정이 달라집니다. `play_quiz()`처럼 사용자와 직접 상호작용하며 최고 점수를 갱신하는, 코드량과 위험도가 모두 큰 기능을 다루기 때문입니다. 이런 작업을 `main`에서 곧바로 하지 않고 `feat/play-quiz`라는 별도 브랜치를 만들어 진행해야 하는 이유는 크게 세 가지입니다.

첫째, **작업 중인 코드가 `main`을 오염시키지 않습니다.** `main`은 언제 봐도 "지금 당장 실행해도 안전한 상태"를 유지해야 하는 브랜치입니다. 퀴즈 채점 로직을 만들다 보면 당연히 중간중간 문법 오류나 로직 버그가 섞인 커밋이 생기는데, 이런 커밋들이 `main`에 바로 올라가면 다른 사람(또는 미래의 나 자신)이 `main`을 내려받았을 때 실행되지 않는 상태를 마주치게 됩니다. 기능 브랜치에서 작업하면 이런 불안정한 중간 상태는 전부 `feat/play-quiz` 안에만 머물고, `main`은 항상 깨끗하게 유지됩니다.

둘째, **문제가 생기면 브랜치째 버릴 수 있습니다.** 예를 들어 최고 점수 갱신 로직을 짜다가 설계가 완전히 잘못됐다는 걸 깨달았다고 해봅시다. `main`에서 바로 작업했다면 되돌리기 위해 커밋을 하나하나 되짚어야 하지만, 별도 브랜치였다면 그냥 그 브랜치를 지우고 `main`에서 다시 새 브랜치를 파면 끝입니다. 실패의 비용이 훨씬 낮아지는 것입니다.

셋째, **나중에 리뷰·병합 단위가 명확해집니다.** `feat/play-quiz` 브랜치 하나가 곧 "퀴즈 풀기 기능 추가"라는 하나의 작업 단위가 되므로, 이 브랜치를 병합할 때 "이번에 무엇이 들어왔는지"가 커밋 그래프에 고스란히 남습니다. 실제로 이 프로젝트의 `git log --oneline --graph --all` 결과를 보면 이 구조가 그대로 드러납니다.

```
*   0e84cc0 (HEAD -> main, origin/main) Merge: 퀴즈 풀기 기능 병합
|\
| * 1181dea (origin/feat/play-quiz, feat/play-quiz) Feat: 퀴즈 출제 및 정답 채점 기능 구현 최고 점수 비교 및 갱신 로직 추가
|/
* 5ba64a0 Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현 메인 루프 및 안전 종료 처리
```

`|\`와 `|/`로 갈라졌다가 다시 합쳐지는 모양이 보이시나요? 이게 바로 `feat/play-quiz`에서 작업한 커밋 `1181dea`가 `main`과 분리된 채로 만들어졌다가, 이후 병합 커밋 `0e84cc0`으로 다시 합쳐진 흔적입니다.

### `git checkout -b`는 무엇을 축약한 명령인가

체크리스트의 첫 항목은 `git checkout -b feat/play-quiz`를 실행하라고 안내합니다. 이 명령은 사실 두 단계를 한 번에 처리하는 축약형입니다.

```bash
# git checkout -b feat/play-quiz 는 아래 두 줄과 동일합니다
git branch feat/play-quiz      # 1. 새 브랜치를 만든다
git checkout feat/play-quiz    # 2. 그 브랜치로 이동한다
```

최신 Git(2.23 이상)에서는 `checkout`이 브랜치 이동과 파일 복원이라는 서로 다른 역할을 동시에 맡고 있어 혼동을 준다는 이유로, 브랜치 전환 전용 명령인 `switch`가 도입되었습니다. 같은 일을 다음처럼 표현할 수도 있습니다.

```bash
git switch -c feat/play-quiz
```

`-c`는 `--create`의 줄임말로, `checkout -b`의 `-b`와 같은 역할을 합니다. 둘 중 무엇을 써도 결과는 동일하니, 팀이나 강의 자료가 어느 쪽을 쓰든 당황하지 않아도 됩니다.

### 이 프로젝트에서 실제로 확인되는 것과 확인되지 않는 것

체크리스트의 4개 항목은 모두 `[ ]`로 비어 있지만, 실제 git 이력을 보면 이야기가 조금 다릅니다. `git branch -a`를 실행해 보면 다음과 같이 나옵니다.

```bash
$ git branch -a
  feat/play-quiz
* main
  remotes/origin/feat/play-quiz
  remotes/origin/main
```

`feat/play-quiz` 브랜치가 로컬과 원격(origin) 모두에 실제로 존재합니다. 그리고 위에서 본 `git log --oneline --graph --all` 결과에서 커밋 `1181dea`가 `main`이 아니라 `feat/play-quiz` 브랜치 위에서 만들어졌다는 것도 확인됩니다. 즉 **"퀴즈 풀기와 최고 점수 작업을 `main`이 아닌 기능 브랜치에서 수행한다"는 마지막 항목은, 체크박스는 비어 있어도 실제로는 이미 지켜진 상태**입니다. 이는 단지 체크리스트의 표시가 아직 갱신되지 않았을 뿐입니다.

다만 정직하게 짚어야 할 부분도 있습니다. 사용자가 붙여넣은 터미널 로그는 `git add .`와 `git commit`부터 시작하고 있어서, 그 앞에 실제로 `git checkout -b feat/play-quiz`를 실행했는지, 또는 브랜치를 만든 뒤 `git branch --show-current`로 현재 브랜치가 `feat/play-quiz`인지 확인했는지는 이 로그 범위 밖이라 직접 확인할 수 없습니다. 로그가 시작되는 시점에 이미 커밋 배너가 `[feat/play-quiz 1181dea]`로 찍혀 있었다는 사실만으로, 그 순간 현재 브랜치가 `feat/play-quiz`였다는 것을 간접적으로 알 수 있을 뿐입니다.

한 가지 정황은 더 있습니다. `docs/screenshots/git_branch.png` 파일이 실제로 존재하고(9,418바이트) 이미 커밋 `1181dea`에 포함되어 있습니다. 체크리스트가 이 섹션 뒤에 이 이미지를 캡처 자료로 요구하고 있다는 점을 생각하면, 브랜치 확인 작업 자체는 어떤 형태로든 화면에 캡처되어 남아 있다고 볼 수 있습니다. 다만 그 캡처가 정확히 `git branch --show-current` 명령의 결과인지, 다른 방식(예: 터미널 프롬프트에 표시된 브랜치명)으로 확인한 것인지는 이미지 내용을 직접 열어보기 전까지는 단정할 수 없습니다.

정리하면, 이 4개 항목 중 "기능 브랜치에서 작업했다"는 결과는 git 이력으로 명확히 검증되지만, "그 과정에서 정확히 어떤 명령을 어떤 순서로 실행했는가"는 로그에 남지 않은 부분이라 추측이 아니라 "확인 불가"로 남겨두는 것이 정직한 태도입니다. 체크리스트를 갱신할 때는 실제 브랜치 구조를 근거로 마지막 항목(기능 브랜치에서 작업)에 체크하고, 나머지는 스크린샷을 열어 실제로 어떤 명령 결과가 찍혀 있는지 확인한 뒤 체크하는 것을 권합니다.

---

## 4-2. play_quiz 구현

체크리스트의 `play_quiz(self) 구현` 항목은 이미 `[x]`로 표시되어 있고, 실제 `main.py`에 구현된 코드로 확인할 수 있습니다. 이 메서드는 저장된 퀴즈를 순서대로 출제하고, 채점하고, 최고 기록까지 갱신하는 이 프로젝트의 핵심 로직입니다. 전체 코드를 위에서부터 흐름대로 따라가 보겠습니다.

```python
def play_quiz(self) -> None:
    """저장된 퀴즈를 순서대로 출제하고 최고 기록을 갱신한다."""
    if not self.quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return

    total = len(self.quizzes)
    correct = 0
    print(f"\n📝 자료구조 퀴즈를 시작합니다! (총 {total}문제)")

    for number, quiz in enumerate(self.quizzes, start=1):
        print("\n" + "-" * 40)
        quiz.display(number)
        user_answer = self.ask_int("\n정답 입력 (1-4): ", 1, 4)

        if quiz.is_correct(user_answer):
            correct += 1
            print("✅ 정답입니다!")
        else:
            print(
                f"❌ 오답입니다! 정답은 {quiz.answer}번 "
                f"({quiz.get_correct_text()})입니다."
            )

    score = round(correct / total * 100)
    ...
```

가장 먼저 나오는 것은 빈 퀴즈 목록 가드입니다. `if not self.quizzes: print(...); return`으로, 등록된 퀴즈가 하나도 없으면 안내 메시지만 출력하고 함수를 즉시 끝냅니다. 이 가드가 왜 중요한지는 뒤에서 나오는 `score = round(correct / total * 100)` 계산과 직접 연결됩니다. 가드를 통과했다는 것은 `total = len(self.quizzes)`가 최소 1 이상이라는 뜻이므로, 함수 뒷부분의 나눗셈이 `ZeroDivisionError`를 일으킬 걱정 없이 항상 안전합니다. 즉 "퀴즈가 0개일 때 ZeroDivisionError가 나지 않는지 확인"이라는 체크리스트 항목은 별도의 방어 코드를 추가한 게 아니라, 맨 위의 이 한 줄짜리 조기 반환(early return)이 그 역할을 전부 맡고 있는 것입니다.

가드를 통과하면 `for number, quiz in enumerate(self.quizzes, start=1):` 루프가 시작됩니다. `enumerate(..., start=1)`을 쓴 이유는 화면에 "문제 1", "문제 2"처럼 사람이 읽기 좋은 1부터 시작하는 번호를 보여주기 위해서입니다(파이썬 인덱스는 0부터 시작하지만 사용자에게 0번 문제라고 보여주면 어색하겠죠). 루프 안에서는 `print("\n" + "-" * 40)`으로 문제 사이 구분선을 찍고, `quiz.display(number)`를 호출해 문제 번호·문장·선택지 4개를 출력합니다. 실제 실행 로그를 보면 이 두 줄이 정확히 어떻게 찍히는지 확인할 수 있습니다.

```
----------------------------------------
[문제 1] 스택(Stack)의 주요 자료 처리 방식은 무엇인가요?
  1. FIFO (선입선출)
  2. LIFO (후입선출)
  3. LILO (후입후출)
  4. 무작위 접근

정답 입력 (1-4): 2
✅ 정답입니다!
```

`"-" * 40`으로 만든 구분선이 각 문제 시작 전에 한 번씩 찍히고, 그 아래 `[문제 1] ...`부터가 `quiz.display(number)`의 출력입니다. 그다음 `정답 입력 (1-4):` 프롬프트는 `self.ask_int("\n정답 입력 (1-4): ", 1, 4)` 호출이 그대로 화면에 나타난 것으로, `ask_int`에 넘긴 `1, 4`가 사용자 입력을 1~4 범위로 제한하는 역할을 합니다. 사용자가 `2`를 입력하면 `quiz.is_correct(user_answer)`가 정답 여부를 판정하고, 맞았을 때는 `correct += 1`과 함께 `✅ 정답입니다!`를 즉시 출력합니다.

오답일 때는 `f"❌ 오답입니다! 정답은 {quiz.answer}번 ({quiz.get_correct_text()})입니다."`처럼 두 정보를 함께 보여줍니다. `quiz.answer`는 사람이 보는 1~4 번호이고, `quiz.get_correct_text()`는 그 번호에 해당하는 실제 선택지 문장입니다. 번호만 알려주면 사용자가 다시 위로 스크롤해서 선택지를 확인해야 하지만, 텍스트까지 함께 보여주면 그 자리에서 바로 "아, 정답이 이거였구나"를 알 수 있습니다. 흥미로운 점은 `get_correct_text()`가 체크리스트에는 등장하지 않는 메서드라는 것입니다 — Step 1 학습 노트에서 "체크리스트에는 이름이 없지만 실제로 쓰이는 편의 메서드"로 처음 소개됐던 바로 그 메서드로, 그때는 `Quiz` 클래스 자체 테스트(`__main__` 블록)에서만 호출됐습니다. 이번 Step 3에서 오답 안내라는 실제 사용자 대면 기능에 재사용되면서, 미리 만들어둔 편의 메서드가 나중에 실전에서 값어치를 하는 좋은 예가 되었습니다.

루프가 모두 끝나면 `score = round(correct / total * 100)`으로 점수를 계산합니다. `round()`는 소수점을 반올림하는 함수이므로, 예를 들어 5문제 중 4문제를 맞히면 `4/5*100 = 80.0`으로 정확히 나누어떨어져 `80점`이 되지만, 3문제 중 2문제를 맞히면 `2/3*100 = 66.666...`이 `67점`으로 반올림됩니다. 체크리스트가 예시로 든 "5문제 중 4문제 정답! (80점)"은 이 계산식이 어떻게 동작하는지 보여주는 가상의 예시이고, 실제 사용자가 5문제를 모두 맞힌 로그에서는 `5/5*100 = 100.0`이 그대로 반올림 없이 `100점`으로 출력되었습니다.

```
========================================
🏆 결과: 5문제 중 5문제 정답! (100점)
🎉 첫 기록이 저장되었습니다!
========================================
```

정답 수와 점수를 함께 보여주는 이 결과 줄(`f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)"`)이 체크리스트의 마지막 두 항목 — "정답 수와 전체 문제 수를 함께 출력", "정답 수와 점수를 함께 표시" — 을 그대로 만족시킵니다. 최고 기록 갱신 로직(`has_previous_record`, `best_score`/`best_correct`/`best_total` 저장)은 이어지는 4-3 섹션에서 다루지만, 이 결과 줄까지가 문제를 출제하고 채점하는 `play_quiz`의 본 임무이고, 나머지는 그 결과를 기록으로 남기는 후처리에 해당합니다.

---

## 4-3. 최고 점수와 결과 저장

Step 2 학습 노트(`step2_quizgame_menu.md`)에서 지적했던 문제를 기억하시나요? 당시 `storage.py`의 `load_state()`/`save_state()`는 `best_correct`와 `best_total`을 전혀 다루지 않아서, `QuizGame.__init__`에서 초기화한 이 두 값이 프로그램을 다시 실행할 때마다 항상 0으로 리셋되는 문제가 있었습니다. 이번 Step 3에서 이 문제가 실제로 해결되었습니다. `storage.py`의 `load_state()`에는 `include_details`라는 키워드 전용 인자가 추가되어, `True`로 넘기면 `(quizzes, best_score, best_correct, best_total)` 네 값을 한꺼번에 돌려받을 수 있게 됐습니다. `save_state()`에도 `best_correct`/`best_total` 키워드 인자가 추가되어 이 값들이 JSON 파일에 함께 저장됩니다. Step 2에서 남겨둔 숙제가 Step 3에서 실제로 마무리된 셈이니, 이전 문서와 이어서 읽고 계셨다면 이 대목을 꼭 기억해 두시기 바랍니다.

이제 핵심 로직인 `play_quiz()`의 최고 점수 갱신 부분을 살펴보겠습니다.

```python
has_previous_record = self.best_total > 0 or self.best_score > 0
if not has_previous_record or score > self.best_score:
    self.best_score = score
    self.best_correct = correct
    self.best_total = total

    if has_previous_record:
        print("🎉 새로운 최고 점수입니다!")
    else:
        print("🎉 첫 기록이 저장되었습니다!")
    self.save_state()
```

`has_previous_record`는 "이전에 저장된 기록이 하나라도 있는가"를 나타냅니다. `best_total`이나 `best_score` 둘 중 하나라도 0보다 크면 이전 기록이 있다는 뜻입니다. 그리고 그 아래 `if` 조건문은 다음 두 가지 경우를 `or`로 하나의 조건에 묶은 것입니다.

- `not has_previous_record`: 이전 기록이 아예 없다면 — 이번 점수가 몇 점이든 무조건 저장합니다(첫 기록이므로 비교할 대상이 없습니다).
- `score > self.best_score`: 이전 기록이 있더라도, 이번 점수가 기존 최고 점수보다 높다면 갱신합니다.

이 두 조건 중 하나라도 참이면 `if` 블록 안으로 들어가 `best_score`, `best_correct`, `best_total`을 한꺼번에 새 값으로 덮어씁니다. 반대로 두 조건이 모두 거짓인 경우, 즉 이전 기록이 있으면서 이번 점수가 기존 최고 점수와 같거나 낮은 경우에는 이 `if` 블록 자체에 들어가지 않습니다. 여기서 중요한 점은 "같거나 낮을 때 최고 기록을 덮어쓰지 않는다"는 체크리스트 요구사항이 별도의 방어 코드 없이도 자연스럽게 지켜진다는 것입니다. `self.best_score`, `self.best_correct`, `self.best_total`에 값을 대입하는 코드가 이 `if` 블록 안에만 존재하기 때문에, 조건이 거짓이면 이 세 변수는 손도 대지 않고 그대로 남습니다. "건드리지 않는 코드가 없다"는 사실 자체가 곧 "덮어쓰지 않는다"는 보장입니다.

실제 실행 로그로 이 조건을 검증해 보겠습니다. 사용자가 `python3 main.py`로 퀴즈 5문제를 모두 맞혔을 때 다음과 같이 출력되었습니다.

```
🏆 결과: 5문제 중 5문제 정답! (100점)
🎉 첫 기록이 저장되었습니다!
```

"첫 기록이 저장되었습니다!"라는 메시지가 뜬 것은 `has_previous_record`가 `False`였기 때문입니다. 즉 이 실행 이전의 `state.json`에는 `best_score`와 `best_total`이 모두 0으로 저장되어 있었던 상태였다는 뜻입니다. 실행 이후 `state.json` 파일을 직접 확인하면 끝부분이 다음과 같이 바뀌어 있습니다.

```json
  "best_score": 100,
  "best_correct": 5,
  "best_total": 5
```

`best_score`뿐 아니라 `best_correct`와 `best_total`까지 함께 저장된 것을 볼 수 있습니다. 이는 앞서 언급한 `storage.py`의 스키마 확장 덕분입니다. `QuizGame`의 `save_state()`/`load_state()` 메서드는 다음과 같이 이 새 시그니처를 사용하도록 이미 갱신되어 있습니다.

```python
def save_state(self) -> bool:
    return save_quiz_state(
        self.quizzes,
        self.best_score,
        best_correct=self.best_correct,
        best_total=self.best_total,
    )

def load_state(self) -> None:
    (
        self.quizzes,
        self.best_score,
        self.best_correct,
        self.best_total,
    ) = load_quiz_state(include_details=True)
```

여기서 흥미로운 지점이 하나 있습니다. 체크리스트 문구는 "점수 갱신 후 **Step 5**의 `save_state()`를 연결해 재시작 후에도 최고 점수가 남게 함"이라고 되어 있지만, 실제로는 이 연결이 **Step 3인 지금 이 코드**에 이미 배선되어 있습니다. `play_quiz()`가 최고 기록을 갱신한 직후 `self.save_state()`를 바로 호출하고 있으니까요. 체크리스트에 적힌 단계 번호와 실제 구현이 이루어진 시점이 항상 정확히 일치하지는 않는다는 것을 보여주는 좋은 예입니다. 문서상의 "Step 5"라는 표현에 얽매이기보다, 지금 코드가 실제로 무엇을 하고 있는지를 기준으로 이해하는 습관을 들이는 것이 중요합니다.

마지막으로 흔히 헷갈리는 부분을 짚어 보겠습니다. `has_previous_record`를 `self.best_score > 0`만으로 판단하면 어떻게 될까요? 만약 예전 방식으로 저장된 `state.json`(즉 `best_correct`/`best_total` 키가 아예 없던 옛 파일)을 불러왔다면, `storage.py`의 `_parse_state()`는 `data.get("best_correct", 0)`처럼 기본값 0으로 복원하므로 `best_total`은 0인데 `best_score`만 0보다 큰 상태가 생길 수 있습니다. 이런 경우까지 고려해서 `or` 조건으로 `best_total`과 `best_score` 둘 다 확인하도록 만든 것은, 데이터 마이그레이션 상황까지 염두에 둔 신중한 설계라고 볼 수 있습니다.

---

## 4-4. 브랜치 커밋·병합·증빙

이 섹션은 커밋 2개, 원격 push, main 복귀, `--no-ff` 병합, 병합 결과 push, 그래프 확인, 스크린샷 캡처까지 총 8개 항목으로 이루어져 있습니다. 체크리스트 파일을 열어 보면 8개 모두 `[ ]`로 표시되어 있지만, 먼저 분명히 짚고 넘어갈 사실이 있습니다 — **이 중 앞의 6개 항목은 실제로 이미 전부 실행되어 성공했습니다.** 근거는 `git log --oneline --graph --all`의 실제 출력입니다.

```
*   0e84cc0 (HEAD -> main, origin/main) Merge: 퀴즈 풀기 기능 병합
|\
| * 1181dea (origin/feat/play-quiz, feat/play-quiz) Feat: 퀴즈 출제 및 정답 채점 기능 구현 최고 점수 비교 및 갱신 로직 추가
|/
* 5ba64a0 Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현 메인 루프 및 안전 종료 처리
```

`HEAD -> main`과 `origin/main`이 같은 커밋 `0e84cc0`을 가리키고 있다는 것은, 병합 커밋을 만든 뒤 원격까지 push가 끝났다는 뜻입니다. 즉 체크리스트의 네모 칸은 아직 비어 있지만, 실제 작업은 이미 끝나 있는 상태입니다. 이런 경우 체크리스트를 "다시 실행"할 필요는 없고, 체크 표시만 채워 넣으면 됩니다.

### 명령어별로 로그 따라가기

실제 터미널 로그를 순서대로 인용하면 다음과 같습니다.

```bash
$ git add .
$ git commit -m "Feat: 퀴즈 출제 및 정답 채점 기능 구현 최고 점수 비교 및 갱신 로직 추가"
[feat/play-quiz 1181dea] Feat: 퀴즈 출제 및 정답 채점 기능 구현 최고 점수 비교 및 갱신 로직 추가
 5 files changed, 650 insertions(+), 74 deletions(-)
 create mode 100644 docs/screenshots/git_branch.png
 create mode 100644 docs/study/step2_quizgame_menu.md

$ git push -u origin feat/play-quiz
 * [new branch]      feat/play-quiz -> feat/play-quiz
branch 'feat/play-quiz' set up to track 'origin/feat/play-quiz'.

$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

$ git merge --no-ff feat/play-quiz -m "Merge: 퀴즈 풀기 기능 병합"
Merge made by the 'ort' strategy.
 5 files changed, 650 insertions(+), 74 deletions(-)

$ git push origin main
   5ba64a0..0e84cc0  main -> main
```

`add` → `commit` → `push -u` → `checkout main` → `merge --no-ff` → `push origin main`까지 한 줄도 빠짐없이 실행되었고, 각 명령의 출력 메시지(`[new branch]`, `Switched to branch`, `Merge made by the 'ort' strategy`, `5ba64a0..0e84cc0`)가 모두 성공을 나타내고 있습니다.

참고로 이 로그 범위 안에는 `git branch --show-current`나 `feat/play-quiz`를 처음 만든 `git checkout -b feat/play-quiz` 명령 자체는 등장하지 않습니다. 로그가 시작될 때 이미 `[feat/play-quiz 1181dea]`라는 커밋 배너로 "현재 브랜치가 feat/play-quiz였다"는 사실만 간접적으로 확인할 수 있을 뿐입니다. 확인되지 않은 것을 확인된 것처럼 말하지 않는 것이 중요하므로, 이 부분은 "로그 범위 밖이라 확인 불가"로 남겨둡니다. 다만 `docs/screenshots/git_branch.png`(9,418바이트) 파일이 이미 커밋에 포함되어 있으므로, 브랜치 확인 자체는 어떤 형태로든 캡처된 것으로 보입니다.

### 세 번째로 반복되는 "커밋 2개 → 1개" 패턴

체크리스트 4-4는 커밋 #6("퀴즈 출제 및 정답 채점 기능 구현")과 커밋 #7("최고 점수 비교 및 갱신 로직 추가")을 나누어 커밋하라고 안내했습니다. 하지만 실제로는 `git add .` 한 번, `git commit` 한 번으로 두 메시지가 이어붙어 커밋 `1181dea` 하나로 합쳐졌습니다. 그런데 이 현상은 이번이 처음이 아닙니다.

| Step | 계획된 커밋 | 실제 커밋 | 결과 |
|------|------------|-----------|------|
| Step 1 | 2개로 분리 예정 | `6868c74` | 1개로 합쳐짐 |
| Step 2 | 2개로 분리 예정 | `5ba64a0` | 1개로 합쳐짐 |
| Step 3 (이번) | 커밋 #6, #7 (2개) | `1181dea` | 1개로 합쳐짐 |

Step 1, Step 2에 이어 Step 3까지 정확히 같은 패턴이 **세 번 연속** 반복된 것입니다. 이걸 "실패"로 볼 필요는 없습니다. 코드 자체는 정상적으로 커밋되고 push까지 잘 되었고, `1181dea`에는 `main.py`/`storage.py` 변경 외에도 `docs/study/step2_quizgame_menu.md`(신규), `docs/screenshots/git_branch.png`(신규), `docs/learning_checklist.md` 갱신까지 총 5개 파일, 650줄 추가/74줄 삭제가 함께 잘 담겨 있습니다. 다만 패턴이 이렇게 세 번이나 뚜렷하게 반복된다면, 그 자체가 "다음 Step부터는 의식적으로 한 번 다르게 시도해볼 좋은 실험 대상"이라는 신호입니다. 예를 들어 다음 기능 브랜치에서는 `git add -p`로 변경분을 나눠서 스테이징하거나, 첫 번째 기능을 커밋한 뒤 두 번째 기능을 작업하기 전에 한 번 멈춰서 `git status`를 확인해보는 습관을 시도해볼 수 있습니다.

### `--no-ff`와 `ort` 전략을 쓴 이유

`git merge --no-ff feat/play-quiz`는 `Merge made by the 'ort' strategy.`라는 메시지를 출력했습니다. `ort`는 Git 2.34부터 기본 병합 전략이 된 것으로, 예전의 `recursive` 전략을 대체합니다. 여기서 중요한 것은 `--no-ff` 옵션입니다. `feat/play-quiz`가 `main`에서 갈라진 뒤 `main`에는 새로운 커밋이 없었기 때문에, 사실 이 병합은 fast-forward(단순히 포인터만 이동)로도 처리될 수 있는 상황이었습니다. 하지만 `--no-ff`를 주었기 때문에 Git은 fast-forward를 하지 않고 **병합 커밋 `0e84cc0`을 강제로 새로 생성**했습니다. 그 결과 `git log --oneline --graph --all`에서 `|\`, `|/`처럼 브랜치가 갈라졌다가 다시 합쳐지는 모양이 시각적으로 남게 되었습니다. fast-forward 병합을 했다면 이 그래프는 그냥 일직선으로 보였을 것이므로, "feat/play-quiz라는 기능 브랜치에서 작업했다"는 이력 자체가 사라졌을 것입니다.

### 스크린샷 파일명 정직하게 확인하기

체크리스트는 `docs/screenshots/play.png`로 캡처하라고 안내하고 있습니다. 하지만 실제로 존재하는 파일은 `docs/screenshots/step3.png`(141,812바이트)이며, `git status`에는 아직 `??`로 표시되어 커밋되지 않은 상태로 남아 있습니다. 파일명이 체크리스트 문구와 다른 것은 이번이 처음이 아니라, Step 0에서도 있었던 "체크리스트가 제안한 이름과 실제 캡처 파일명이 다른" 상황과 같은 종류입니다. 체크리스트를 그대로 맞추려면 파일명을 `play.png`로 바꾸거나 체크리스트 문구를 `step3.png`에 맞게 수정한 뒤, `git add docs/screenshots/step3.png`로 스테이징하고 커밋해야 이 항목이 실제로 마무리됩니다.

### 병합 후 남아 있는 feat/play-quiz 브랜치

`git branch -a`로 확인하면 `feat/play-quiz`는 병합이 끝난 뒤에도 로컬과 원격(`remotes/origin/feat/play-quiz`) 양쪽에 그대로 남아 있습니다. 이는 잘못된 상태가 아니라, Git이 병합 후 브랜치를 자동으로 지우지 않기 때문에 생기는 자연스러운 결과입니다. 더 이상 필요 없다고 판단되면 로컬은 `git branch -d feat/play-quiz`(병합이 확인된 경우) 또는 `-D`(강제 삭제), 원격은 `git push origin --delete feat/play-quiz`로 정리할 수 있습니다. 다만 이 프로젝트가 실제로 그렇게 정리했는지는 지금까지의 로그로는 확인되지 않으므로, 이는 "정리해야 한다"가 아니라 "정리할 수도 있는 선택지"로만 남겨둡니다.

---

## 정리 — 확인하고 넘어가면 좋은 것들

Step 3에서 실제로 구현·검증까지 끝난 부분과, 아직 남은 부분을 구분하면 다음과 같습니다.

**이미 끝난 것 (코드·실행 결과로 확인됨)**
- `play_quiz()`가 빈 퀴즈 목록 가드, 문제 출제·채점, 점수 계산, 최고 기록 갱신까지 전부 구현되고 `python3 main.py`로 직접 실행 검증됨 (5문제 만점 시나리오로 확인)
- `storage.py`가 `include_details`/`best_correct`/`best_total`을 지원하도록 확장되어, Step 2에서 지적했던 "재실행하면 최고 기록이 리셋되는" 문제가 실제로 해결됨
- `feat/play-quiz` 브랜치가 실제로 만들어져 그 위에서 작업이 진행되고, `--no-ff` 병합(`0e84cc0`)으로 `main`에 합쳐진 뒤 원격까지 push됨(체크리스트 체크 표시만 아직 갱신되지 않은 상태)

**다음에 정리하면 좋은 것 (계획과 실제가 갈라진 지점)**
- [ ] `docs/learning_checklist.md`의 "4-1. 브랜치 생성과 작업 분리"와 "4-4. 브랜치 커밋·병합·증빙" 체크박스를 실제 git 이력에 맞게 정리하기 — 커밋 #6/#7이 실제로는 `1181dea` 하나로 합쳐졌다는 사실을 메모로 남기기
- [ ] 잘못된 입력 화면과 마찬가지로, 결과 화면 캡처 파일명이 계획(`play.png`)과 실제(`step3.png`)가 다르다는 점을 문서에서 정리하고, 아직 커밋되지 않은 `docs/screenshots/step3.png`를 커밋하기
- [ ] 병합이 끝난 `feat/play-quiz` 브랜치를 계속 보관할지, `git branch -d`/`git push origin --delete`로 정리할지 결정하기
- [ ] 커밋을 계획대로 나누는 패턴이 세 번 연속 깨졌으므로, 다음 기능부터는 의식적으로 작은 단위 커밋을 실험해 보기

이 항목들을 정리한 뒤에는 [`docs/learning_checklist.md`](../learning_checklist.md)의 다음 단계로 넘어갈 수 있습니다.

## 참고 문서

- [Step 0 학습 노트](step0_dev_environment_git_init.md) — 개발 환경 설정과 Git 저장소 초기화
- [Step 1 학습 노트](step1_quiz_model.md) — Quiz 모델과 자료구조 기본 데이터
- [Step 2 학습 노트](step2_quizgame_menu.md) — QuizGame, 메뉴, 공통 입력과 안전 종료
- [학습 체크리스트](../learning_checklist.md) — 이 문서의 원본 체크리스트
- [학습 가이드](../learning_guide.md) — 단계별 실습 코드와 커밋 힌트
- [프로젝트 README](../../README.md) — 실제로 작성된 프로젝트 설명 문서
