# 10-1. Python 기초 — 자가 점검 학습 노트

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "10. 학습 목표와 자가 점검" 아래 "10-1. Python 기초" 8개 항목을 학습 자료로 재구성한 것입니다. Step 0~7 구현 체크리스트([step0](step0_dev_environment_git_init.md)~[step7](step7_bonus_features.md))가 "무엇을 만들었는가"를 다뤘다면, 이 자가 점검 시리즈는 "왜 그렇게 코드를 짰는지 스스로 설명할 수 있는가"를 확인하는 문서입니다.
>
> 모든 예시는 실제 `main.py`·`quiz.py` 코드에서 그대로 발췌했습니다. 변수명·메서드명은 이 프로젝트에 실제로 존재하는 것만 사용했습니다(예: 선택지는 `options`가 아니라 `choices`, 점수는 `score += 10`이 아니라 `round(earned_points / total * 100)`로 계산됩니다).

## 목차

- 변수와 자료형
- 조건문과 반복문
- 함수와 변수의 유효 범위
- return의 의미와 빈 입력 판별

---

## 변수와 자료형

### 변수가 무엇이며 왜 사용하는지 설명할 수 있다.

변수는 값에 붙이는 "이름표가 붙은 상자"입니다. 상자 안에는 숫자든 글자든 목록이든 무언가가 들어 있고, 코드는 상자 안의 실제 값 대신 이름표만 보고 그 값을 다룹니다. 이렇게 이름을 붙여 두면 나중에 상자 안 내용물이 바뀌어도(예: 사용자가 다른 숫자를 입력해도) 코드를 고칠 필요 없이 이름표만 그대로 참조하면 됩니다.

이 프로젝트에서 가장 먼저 만나는 상자는 `ask_int()` 안의 `raw`입니다.

```python
def ask_int(self, prompt: str, low: int, high: int) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("⚠️ 숫자를 입력하세요.")
            continue
        if low <= value <= high:
            return value
        print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")
```

`raw`라는 상자에 사용자가 입력한 문자열을 잠깐 담아 두었다가, 검증을 통과하면 `value`라는 새 상자에 정수로 변환해 담습니다. 변수가 없다면 "방금 입력받은 문자열"과 "그걸 정수로 바꾼 값"을 구분해서 가리킬 방법이 없습니다.

변수를 쓰는 이유는 크게 세 가지로 정리할 수 있고, 이 프로젝트 코드 곳곳에서 실제 근거를 찾을 수 있습니다.

**① 재사용성** — 같은 로직을 값만 바꿔서 여러 번 쓸 수 있게 해 줍니다. `ask_int()`는 `prompt`, `low`, `high`라는 세 개의 상자(매개변수)를 받도록 만들어졌기 때문에, 메뉴 선택에도 정답 입력에도 문제 수 입력에도 똑같은 함수를 재사용할 수 있습니다.

```python
choice = self.ask_int("선택: ", 1, 6)
...
user_answer = self.ask_int("\n정답 입력 (1-4, 0: 힌트): ", 0, 4)
...
count = self.ask_int(
    f"\n풀 문제 수를 입력하세요 (1~{total_quizzes}): ", 1, total_quizzes,
)
```

만약 `low`·`high`가 변수가 아니라 함수 안에 숫자 `1`, `6`으로 고정 박혀 있었다면, 정답 입력 범위(0~4)나 문제 수 입력 범위(1~total_quizzes)마다 함수를 따로 만들어야 했을 것입니다. 변수 덕분에 함수 하나로 세 가지 다른 상황을 모두 처리합니다.

**② 가독성** — 계산 과정에 이름이 붙으면 코드를 읽는 사람이 각 값의 의미를 바로 알 수 있습니다. `play_quiz()`의 점수 계산 부분을 보면:

```python
total = len(quizzes_to_play)
correct = 0
earned_points = 0.0
...
score = round(earned_points / total * 100)
```

`len(quizzes_to_play)`를 매번 다시 쓰는 대신 `total`이라는 이름을 한 번 붙여 두면, `earned_points / total * 100`이라는 수식이 "얻은 점수를 전체 문제 수로 나눠 100점 만점으로 환산한다"는 의미로 곧바로 읽힙니다. 이름 없이 숫자와 함수 호출만 나열했다면 같은 코드라도 훨씬 해석하기 어려웠을 것입니다.

**③ 상태 관리** — 프로그램이 실행되는 동안(또는 재시작 후에도) 어떤 값을 계속 기억해야 할 때 변수가 그 역할을 합니다. `QuizGame.__init__`을 보면:

```python
def __init__(self) -> None:
    self.quizzes: list[Quiz] = []
    self.best_score: int = 0
    self.best_correct: int = 0
    self.best_total: int = 0
    self.history: list[dict[str, Any]] = []
    self.load_state()
```

`self.best_score`는 `__init__`이 끝난 뒤에도, 메뉴를 몇 번을 오가고 퀴즈를 몇 번을 풀어도 `QuizGame` 인스턴스가 살아 있는 한 계속 유지되는 "상태"입니다. 더 짧은 생명 주기를 가진 상태 변수도 있습니다. `play_quiz()` 안의 `used_hint`가 그 예입니다.

```python
used_hint = False
while True:
    user_answer = self.ask_int("\n정답 입력 (1-4, 0: 힌트): ", 0, 4)
    if user_answer != 0:
        break
    ...
    if not used_hint:
        used_hint = True
        print("⚠️ 힌트 사용으로 이 문제는 맞혀도 0.5점만 인정됩니다.")
```

`used_hint`는 한 문제를 푸는 동안만 "이 문제에서 힌트를 봤는지"를 기억했다가, 채점 시점에 `earned_points`에 1.0을 더할지 0.5를 더할지를 결정하는 데 쓰입니다. `self.best_score`처럼 프로그램 전체 수명을 갖는 상태와, `used_hint`처럼 한 문제 동안만 사는 상태를 구분할 수 있으면 "변수가 값을 담아 시간이 지나도 기억하게 해 준다"는 것이 무슨 뜻인지 실감할 수 있습니다.

변수가 왜 필요한지는 반대로 "return 없이 print만 하면 어떻게 되는가"를 생각해 보면 더 분명해집니다. 실제 `ask_int()`는 검증을 통과한 값을 `return value`로 돌려줍니다. 만약 이 부분을 다음과 같이 바꿨다고 가정해 봅시다.

```python
# 실제 코드 (정상)
if low <= value <= high:
    return value

# 잘못된 코드 (대조군) — return 대신 print만 하면?
if low <= value <= high:
    print(value)
```

`return`이 없으면 함수는 암묵적으로 `None`을 돌려줍니다. 그러면 `choice = self.ask_int("선택: ", 1, 6)`에서 `choice`라는 상자에는 화면에 이미 출력하고 지나간 숫자가 아니라 `None`이 담기고, 이후 `if choice == 1:` 같은 분기는 전부 실패합니다. `value`라는 지역 변수는 함수 안에서만 존재하다가 함수가 끝나면 사라지므로, `return`으로 그 값을 호출자의 변수(`choice`)에 "전달"해 주지 않으면 화면에 찍힌 숫자와 프로그램이 실제로 아는 값이 서로 어긋나 버립니다. 이것이 변수가 단순한 "이름"이 아니라, 프로그램의 서로 다른 부분 사이에서 값을 옮기고 기억하는 통로라는 사실을 보여 줍니다.

**TL;DR: 변수는 값에 이름을 붙인 상자이며, 이 프로젝트에서는 함수 재사용(`ask_int`의 `low`/`high`), 계산식 가독성(`total`), 상태 유지(`self.best_score`, `used_hint`)라는 세 가지 이유로 곳곳에 쓰인다.**

### int, str, bool, list, dict의 차이와 이 프로젝트 안의 예를 각각 말할 수 있다.

Python의 기본 자료형은 "상자 안에 어떤 종류의 값이 들어 있는가"를 나타냅니다. 다섯 가지 자료형과 이 프로젝트의 실제 예를 짝지으면 다음과 같습니다.

| 자료형 | 의미 | 이 프로젝트의 실제 예 | 근거 코드 |
|---|---|---|---|
| `int` | 정수 | `self.best_score`, `quiz.answer` | `self.best_score: int = 0` / `answer: int` |
| `str` | 문자열 | `question`, `hint`, `prompt` | `def __init__(self, question: str, ...)` / `def ask_text(self, prompt: str) -> str:` |
| `bool` | 참/거짓 | `used_hint`, `is_correct()`의 반환값, `ask_yes_no()`의 반환값 | `used_hint = False` / `def is_correct(self, user_answer: int) -> bool:` / `def ask_yes_no(self, prompt: str) -> bool:` |
| `list` | 순서 있는 값의 모음 | `self.quizzes`, `choices` | `self.quizzes: list[Quiz] = []` / `choices: list[str] = []` |
| `dict` | 이름(key)과 값(value)의 짝 | `Quiz.to_dict()`의 반환값, `self.history`의 각 원소 | `def to_dict(self) -> dict[str, Any]:` / `self.history: list[dict[str, Any]] = []` |

각각을 코드로 조금 더 들여다보겠습니다.

**int** — `self.best_score`는 지금까지 기록한 최고 점수를 정수로 담습니다. `Quiz.answer`도 정답 번호(1~4)를 담는 `int`입니다. 정수는 사칙연산과 크기 비교(`score > self.best_score`)에 바로 쓸 수 있다는 점이 문자열과 다릅니다.

**str** — `Quiz.__init__`의 `question`은 문제 문장을 담는 문자열이고, `hint`는 힌트 문장(또는 `None`)을 담습니다. `ask_text(self, prompt: str) -> str:`의 `prompt`는 "문제를 입력하세요: "처럼 화면에 보여줄 안내 문구를 담는 문자열 매개변수입니다. 문자열은 `+`로 이어 붙이거나 `f"..."`처럼 다른 값을 끼워 넣을 수 있다는 점에서 숫자와 다르게 쓰입니다.

**bool** — `used_hint = False`는 참/거짓 두 값만 가질 수 있는 상자로, 힌트를 봤는지 여부를 기억합니다. `is_correct()`는 아예 `bool`을 반환하도록 설계돼 있습니다.

```python
def is_correct(self, user_answer: int) -> bool:
    return (
        isinstance(user_answer, int)
        and not isinstance(user_answer, bool)
        and user_answer == self.answer
    )
```

`ask_yes_no()`도 마찬가지로 `y`/`n` 입력을 받아 `True`/`False`로 변환해 돌려줍니다.

```python
def ask_yes_no(self, prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("⚠️ y 또는 n을 입력하세요.")
```

두 함수 모두 호출한 쪽에서 `if quiz.is_correct(user_answer):`, `if self.ask_yes_no(...):`처럼 `if` 조건에 곧바로 넣어 쓸 수 있다는 것이 `bool` 반환값의 쓸모입니다.

**list** — `self.quizzes: list[Quiz] = []`는 여러 개의 `Quiz` 객체를 순서대로 담는 목록입니다. `add_quiz()` 안의 `choices`도 리스트입니다.

```python
choices: list[str] = []
for number in range(1, 5):
    choices.append(self.ask_text(f"선택지 {number}: "))
```

여기서 눈여겨볼 대조가 있습니다. `add_quiz()`의 지역 변수 `choices`는 이 함수가 실행되는 동안만 존재하며, 방금 입력받은 선택지 4개만 담았다가 `Quiz(question, choices, answer, hint)`로 전달되고 나면 역할이 끝납니다. 반면 `Quiz` 클래스 안의 `self.choices`는 그 `Quiz` 객체가 살아 있는 동안(즉 `self.quizzes` 목록에 남아 있는 한) 계속 유지되는 인스턴스 속성입니다. 이름은 같지만 하나는 잠깐 쓰고 버리는 지역 변수, 하나는 객체와 함께 오래 사는 속성이라는 점이 다릅니다.

**dict** — 이름(key)과 값(value)을 짝지어 담는 자료형으로, 이 프로젝트에서는 저장용 데이터를 표현할 때 등장합니다. `Quiz.to_dict()`가 대표적입니다.

```python
def to_dict(self) -> dict[str, Any]:
    return {
        "question": self.question,
        "choices": list(self.choices),
        "answer": self.answer,
        "hint": self.hint,
    }
```

이 메서드가 반환한 `dict`가 그대로 `state.json`에 저장되는 형태와 일치합니다.

```json
{
  "question": "스택(Stack)의 주요 자료 처리 방식은 무엇인가요?",
  "choices": ["FIFO (선입선출)", "LIFO (후입선출)", "LILO (후입후출)", "무작위 접근"],
  "answer": 2,
  "hint": null
}
```

`"question"`, `"choices"`, `"answer"`, `"hint"`라는 이름표가 각각 문자열, 리스트, 정수, 문자열(또는 `null`) 값과 짝지어져 있는 것이 `dict`의 형태입니다. 리스트가 "순서로만 값을 구분"하는 반면 `dict`는 "이름으로 값을 구분"한다는 점이 핵심적인 차이입니다. `self.history`도 이와 비슷하게 `list[dict[str, Any]]`로 선언되어 있어서, 목록의 각 원소 하나하나가 "이번 판 결과를 나타내는 `dict`"가 되는 구조입니다.

정리하면, `int`와 `bool`은 계산과 판단에, `str`은 사람이 읽는 문장에, `list`는 같은 종류의 값을 순서대로 여러 개 모을 때, `dict`는 서로 다른 종류의 값을 이름을 붙여 하나의 묶음으로 표현할 때(그리고 JSON으로 저장할 때) 쓰인다는 것을 이 프로젝트의 실제 코드에서 확인할 수 있습니다.

**TL;DR: int는 점수·정답 번호처럼 계산 가능한 정수(`self.best_score`, `answer`), str은 문제·힌트·안내 문구 같은 텍스트(`question`, `hint`, `prompt`), bool은 참/거짓 판단(`used_hint`, `is_correct()`, `ask_yes_no()`), list는 같은 종류를 순서대로 모은 목록(`self.quizzes`, `choices`), dict는 이름-값 짝의 묶음(`Quiz.to_dict()`, `self.history`의 각 원소이자 `state.json`의 저장 형태)이다.**

---

## 조건문과 반복문

### if/elif/else가 메뉴 선택과 정오답 분기에 어떻게 쓰이는지 설명할 수 있다.

`if/elif/else`는 "여러 갈래 길 중 딱 하나만 골라서 들어간다"는 비유로 이해하면 쉽습니다. 갈림길 표지판이 1번부터 순서대로 붙어 있고, 조건에 맞는 표지판을 처음 만나는 순간 그 길로 들어가고 나머지 표지판은 쳐다보지도 않는 것과 같습니다.

`run()` 메서드는 사용자가 고른 메뉴 번호(`choice`)에 따라 서로 다른 메서드를 호출하는 전형적인 다중 분기입니다.

```python
if choice == 1:
    self.play_quiz()
elif choice == 2:
    self.add_quiz()
elif choice == 3:
    self.show_quiz_list()
elif choice == 4:
    self.show_score()
elif choice == 5:
    self.delete_quiz()
else:
    self.save_state()
    print("\n👋 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
    return
```

여기서 주목할 점은 `choice`가 `ask_int("선택: ", 1, 6)`으로 이미 1~6 사이의 정수임이 보장된 상태로 들어온다는 것입니다. 그래서 마지막 `else`는 "1~5도 아니라면 무조건 6"이라는 뜻이 되고, 굳이 `elif choice == 6:`이라고 쓰지 않아도 안전합니다. 즉 `if/elif/.../else`는 위에서부터 조건을 하나씩 검사하다가 처음으로 참(True)이 되는 블록만 실행하고, 마지막 `else`는 "그 외 나머지 모든 경우"를 담당하는 안전망 역할을 합니다.

정오답을 나누는 분기는 `play_quiz()` 안에 있는 다음 코드입니다.

```python
if quiz.is_correct(user_answer):
    correct += 1
    if used_hint:
        earned_points += 0.5
        print("✅ 정답입니다! (힌트 사용: 0.5점 획득)")
    else:
        earned_points += 1.0
        print("✅ 정답입니다! (1점 획득)")
else:
    print(
        f"❌ 오답입니다! 정답은 {quiz.answer}번 "
        f"({quiz.get_correct_text()})입니다."
    )
```

`quiz.is_correct(user_answer)`가 `True`면 정답 블록으로 들어가 `correct`를 늘리고 점수를 더하며 ✅ 메시지를 출력합니다. `False`면 `else` 블록으로 가서 ❌ 메시지와 함께 정답 번호(`quiz.answer`)와 정답 텍스트(`quiz.get_correct_text()`)를 보여줍니다. 그리고 그 정답 블록 안에 `if used_hint: ... else: ...`라는 또 다른 분기가 중첩되어 있어서, "맞혔는가"와 "힌트를 썼는가"라는 두 가지 조건을 따로따로 판단하고 있다는 점도 눈여겨볼 만합니다.

**TL;DR: `if/elif/else`는 조건을 위에서부터 순서대로 검사해 맨 처음 참인 블록 하나만 실행하며, 메뉴 번호 분기(`run()`)와 정오답 분기(`play_quiz()`의 `is_correct`)가 그 실제 예다.**

### 메뉴 루프에 while, 여러 퀴즈 출제에 for를 쓰는 이유를 설명할 수 있다.

`while`과 `for`는 둘 다 "반복"을 하지만, 반복을 멈추는 기준이 다릅니다. `while`은 "조건이 거짓이 될 때까지" 계속 도는 반면, `for`는 "정해진 목록/횟수를 다 소진할 때까지"만 돕니다. 비유하자면 `while`은 "손님이 그만 오라고 할 때까지 문을 여는 가게"이고, `for`는 "미리 뽑아 둔 번호표 5장을 순서대로 다 부를 때까지 진행하는 안내 창구"입니다.

`run()` 메서드는 `while True:`로 감싸져 있습니다.

```python
def run(self) -> None:
    while True:
        self.show_menu()
        choice = self.ask_int("선택: ", 1, 6)
        ...
        else:
            self.save_state()
            print("\n👋 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            return
```

메뉴는 사용자가 몇 번이나 항목을 고를지 프로그램 작성 시점에는 전혀 알 수 없습니다. 한 번 퀴즈를 풀고 바로 종료할 수도 있고, 퀴즈 추가→풀기→점수 확인을 열 번 반복할 수도 있습니다. "반복 횟수"가 아니라 "사용자가 6번(종료)을 선택할 때까지"라는 조건 자체가 종료 기준이므로, 반복 횟수를 미리 셀 수 있는 `for`가 아니라 조건 기반으로 도는 `while True:`를 쓰고, 조건을 만족하면(`else` 분기에서) `return`으로 빠져나옵니다.

`ask_int`, `ask_text`, `ask_yes_no`의 입력 재시도 루프도 같은 이유로 `while True:`를 씁니다.

```python
def ask_int(self, prompt: str, low: int, high: int) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("⚠️ 숫자를 입력하세요.")
            continue
        if low <= value <= high:
            return value
        print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")
```

사용자가 몇 번 만에 유효한 숫자를 입력할지는 아무도 예측할 수 없습니다. 첫 시도에 맞을 수도 있고, 열 번을 틀릴 수도 있습니다. "유효한 값이 나올 때까지"라는 조건 자체가 반복을 멈추는 기준이므로 여기서도 `while True:`가 자연스럽고, 유효한 값을 얻는 순간 `return value`로 함수를 끝냅니다.

반대로 `play_quiz()`에서 여러 문제를 차례로 출제하는 부분은 `for`를 씁니다.

```python
for number, quiz in enumerate(quizzes_to_play, start=1):
    print("\n" + "-" * 40)
    quiz.display(number)
    ...
```

`quizzes_to_play`는 이미 `self.quizzes[:]`로 복사하고 `random.shuffle()`로 섞은 뒤 `[:count]`로 잘라낸, 길이가 정확히 정해진 리스트입니다(예: 사용자가 3문제를 선택했다면 정확히 3개). "몇 번 반복될지" 자체가 이 리스트의 길이로 이미 확정되어 있으므로, 조건을 매번 판단하는 `while`보다 "이 리스트를 처음부터 끝까지 순회한다"는 의도를 그대로 드러내는 `for`가 더 적합합니다. `enumerate(quizzes_to_play, start=1)`을 쓰면 리스트를 순회하면서 동시에 1부터 시작하는 문제 번호(`number`)도 함께 얻을 수 있어, `quiz.display(number)`처럼 "몇 번째 문제인지" 화면에 보여줄 때 유용합니다.

`add_quiz()`에서 선택지 4개를 입력받는 부분도 정해진 횟수만큼 반복하는 `for`의 좋은 예입니다.

```python
choices: list[str] = []
for number in range(1, 5):
    choices.append(self.ask_text(f"선택지 {number}: "))
```

`range(1, 5)`는 1, 2, 3, 4라는 정확히 4개의 숫자를 만들어내므로, 이 반복은 "선택지를 몇 개 받을지 모르니 조건으로 멈춘다"가 아니라 "사지선다이므로 무조건 4번 반복한다"는 확정된 요구사항을 코드로 그대로 옮긴 것입니다. 만약 이 부분을 `while`로 짰다면 별도의 카운터 변수를 만들고 매번 증가시키고 조건을 검사해야 해서 코드가 더 길고 실수하기 쉬워집니다. 이렇게 "반복 횟수가 미리 정해져 있는가"를 기준으로 `for`와 `while` 중 하나를 고르면 됩니다.

| 상황 | 반복 종료 기준 | 선택 |
|---|---|---|
| 메뉴 루프(`run`) | 사용자가 종료(6)를 고를 때까지 | `while True:` |
| 입력 재시도(`ask_int` 등) | 유효한 값이 들어올 때까지 | `while True:` |
| 퀴즈 여러 개 출제(`play_quiz`) | `quizzes_to_play`의 길이만큼 | `for ... in enumerate(...)` |
| 선택지 4개 입력(`add_quiz`) | 정확히 4번 | `for number in range(1, 5):` |

**TL;DR: 몇 번 반복될지 미리 알 수 없고 "조건을 만족할 때까지"가 기준이면 `while True:`(메뉴 루프, 입력 재시도), 반복 횟수가 리스트 길이나 4개처럼 미리 정해져 있으면 `for`(`enumerate(quizzes_to_play, ...)`, `range(1, 5)`)를 쓴다.**

---

## 함수와 변수의 유효 범위

### 함수를 정의하고 매개변수와 반환값을 사용하는 이유를 설명할 수 있다.

함수는 "반복해서 쓸 코드 뭉치에 이름을 붙여 놓은 것"이다. 그런데 이름만 붙여서는 부족하다. 매번 똑같은 동작만 한다면 재사용할 이유가 별로 없기 때문이다. 그래서 함수는 **매개변수(parameter)**로 "이번엔 무엇을 다르게 할지"를 입력받고, **반환값(return value)**으로 "그래서 결과가 뭔지"를 돌려준다. 이 프로젝트의 `ask_int`가 그 예시를 정확히 보여준다.

```python
def ask_int(self, prompt: str, low: int, high: int) -> int:
    """low~high 범위의 정수를 입력받을 때까지 재시도한다.

    ValueError만 처리하여 KeyboardInterrupt와 EOFError는
    상위 실행 흐름에서 안전하게 처리할 수 있도록 그대로 전달한다.
    """
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("⚠️ 숫자를 입력하세요.")
            continue
        if low <= value <= high:
            return value
        print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")
```

여기서 `prompt`, `low`, `high`는 매개변수다. 함수를 호출할 때마다 다른 값을 넘겨줄 수 있기 때문에, `run()`에서 메뉴 번호를 받을 때는

```python
choice = self.ask_int("선택: ", 1, 6)
```

처럼 1~6 범위로 호출하고, `play_quiz()`에서 정답을 받을 때는

```python
user_answer = self.ask_int("\n정답 입력 (1-4, 0: 힌트): ", 0, 4)
```

처럼 0~4 범위로 호출한다. "입력이 비었는지 검사하고, 숫자로 변환되는지 검사하고, 범위 안에 있는지 검사한다"는 로직 자체는 완전히 동일하지만, `prompt`/`low`/`high`라는 매개변수 덕분에 이 로직 하나를 메뉴 선택에도, 정답 입력에도, 정답 번호 입력(`self.ask_int("정답 번호 (1-4): ", 1, 4)`)에도 재사용할 수 있다. 매개변수가 없었다면 "메뉴용 입력 함수", "정답용 입력 함수"를 따로따로 만들어야 했을 것이다.

그리고 함수 마지막의 `return value`가 **반환값**이다. `ask_int`는 검증이 끝난 정수를 화면에 출력하고 끝내는 게 아니라, `return value`로 호출한 쪽에 그 값을 "돌려준다". 그래서 `choice = self.ask_int(...)`처럼 반환값을 변수에 담아 `if choice == 1:` 같은 이후 로직에서 계속 사용할 수 있다. 만약 반환값이 없었다면 `ask_int` 함수 안에서 값을 검증만 하고 그 값을 밖에서는 전혀 쓸 수 없는, "검증만 하고 사라지는" 함수가 됐을 것이다.

이걸 실감하려면 일부러 잘못된 버전과 비교해보면 좋다.

```python
# 실제 코드 - 검증된 값을 반환값으로 돌려준다
if low <= value <= high:
    return value

# 잘못된 버전 - 반환값 대신 출력만 하고 끝낸다
if low <= value <= high:
    print(value)   # 화면에만 보여주고, 호출한 쪽은 이 값을 받을 방법이 없다
```

`print(value)`로 바꾼 잘못된 버전에서는 `choice = self.ask_int("선택: ", 1, 6)`이라고 써도 `choice`에는 아무 값도 담기지 않는다(정확히는 `None`이 담긴다). 함수 안에서 아무리 열심히 검증해도, 그 결과를 밖으로 "돌려주지" 않으면 호출한 코드는 그 값을 활용할 수 없다. 매개변수는 함수에 "정보를 넣는" 통로이고, 반환값은 함수에서 "결과를 꺼내는" 통로라는 걸 기억하면 된다.

### self.quizzes와 지역 변수 quizzes의 차이를 설명할 수 있다.

`self.quizzes`와 `play_quiz()` 안의 `quizzes_to_play`는 얼핏 비슷해 보이지만 **생명주기가 완전히 다르다.**

```python
class QuizGame:
    def __init__(self) -> None:
        self.quizzes: list[Quiz] = []
        ...
```

`self.quizzes`는 `QuizGame.__init__`에서 만들어지는 **인스턴스 속성**이다. `self.`이 붙어 있다는 것 자체가 "이 객체에 딸린 데이터"라는 뜻이고, `QuizGame` 인스턴스가 살아 있는 한(프로그램이 종료되기 전까지) 계속 유지된다. `run()`, `add_quiz()`, `show_quiz_list()`, `play_quiz()` 등 어느 메서드에서든 `self.quizzes`라고 쓰면 언제나 같은 리스트에 접근하게 된다.

반면 `play_quiz()` 내부를 보자.

```python
def play_quiz(self) -> None:
    ...
    # 저장·목록 조회에 쓰는 원본 순서는 유지하고, 출제용 복사본만 섞는다.
    quizzes_to_play = self.quizzes[:]
    random.shuffle(quizzes_to_play)
    quizzes_to_play = quizzes_to_play[:count]
    ...
```

`quizzes_to_play`는 `self.`이 붙지 않은 **지역 변수**다. `self.quizzes[:]`로 원본 리스트를 통째로 복사해서 만들어졌기 때문에 처음에는 `self.quizzes`와 똑같은 `Quiz` 객체들을 담고 있다. 하지만 그 다음 줄의 `random.shuffle(quizzes_to_play)`는 `quizzes_to_play`만 섞을 뿐, `self.quizzes`는 전혀 건드리지 않는다. 그래서 `play_quiz()`가 실행되는 동안 두 변수는 같은 퀴즈들을 가리키면서도 순서가 달라진다 — `quizzes_to_play`는 뒤섞인 채로 문제를 출제하는 데 쓰이고, `self.quizzes`는 원래 등록 순서 그대로 유지되어 `show_quiz_list()`나 저장(`save_state`)에서 계속 그 순서로 쓰인다. `play_quiz()`가 끝나면 `quizzes_to_play`는 사라지지만, `self.quizzes`는 다음 메뉴 선택에서도, 다음번 `play_quiz()` 호출에서도 그대로 남아 있다. 이게 바로 "속성은 객체가 사는 동안 오래 유지되고, 지역 변수는 그 함수 실행 중에만 산다"는 차이다.

같은 대비를 `add_quiz()`에서도 볼 수 있다.

```python
def add_quiz(self) -> None:
    ...
    choices: list[str] = []
    for number in range(1, 5):
        choices.append(self.ask_text(f"선택지 {number}: "))

    answer = self.ask_int("정답 번호 (1-4): ", 1, 4)
    hint = input("힌트 (선택, Enter로 건너뛰기): ").strip() or None
    self.quizzes.append(Quiz(question, choices, answer, hint))
```

여기서 `choices`는 `add_quiz()` 안에서만 존재하는 지역 변수로, 이번에 사용자가 입력한 4개의 선택지만 잠깐 담아뒀다가 `Quiz(question, choices, answer, hint)`를 만드는 데 쓰이고 함수가 끝나면 사라진다. 반면 `Quiz.__init__`에서 만들어지는 `self.choices`

```python
self.choices = list(choices)
```

는 그 `Quiz` 인스턴스가 존재하는 한(즉 `self.quizzes` 리스트 안에 남아 있는 한) 계속 유지되는 속성이다. `add_quiz()`의 `choices`는 재료를 잠깐 담는 그릇이고, `Quiz` 인스턴스의 `self.choices`는 그 재료로 완성해서 오래 보관하는 결과물인 셈이다.

**TL;DR:** 매개변수(`prompt`/`low`/`high`)는 함수를 여러 상황에 재사용하게 해주고 반환값(`return value`)은 함수 안에서 검증된 결과를 호출한 쪽으로 돌려주며, `self.quizzes`처럼 `self.`이 붙은 속성은 인스턴스가 사는 동안 오래 유지되는 반면 `quizzes_to_play`·`choices` 같은 지역 변수는 해당 함수가 실행되는 동안만 잠깐 존재했다가 사라진다.

---

## return의 의미와 빈 입력 판별

### ask_int()가 값을 return하지 않고 print만 하면 호출자에게 어떤 문제가 생기는지 설명할 수 있다.

`return`은 함수가 계산한 결과를 "호출한 곳으로 돌려주는" 통로다. 함수 안에서 `print()`로 화면에 무언가를 보여주는 것과, `return`으로 값을 함수 밖으로 넘겨주는 것은 완전히 다른 일이다. `print()`는 사람이 눈으로 보라고 화면에 출력하는 것이고, `return`은 다른 코드(호출자)가 그 값을 변수에 담아 계속 사용할 수 있게 해주는 것이다. 편지에 비유하면 `print()`는 편지를 그냥 낭독하고 마는 것이고, `return`은 그 편지를 봉투에 넣어 상대방 손에 쥐여주는 것이다.

`main.py`의 실제 `ask_int()`는 유효한 정수를 입력받으면 `return value`로 그 값을 호출자에게 돌려준다.

```python
# 실제 코드 (main.py)
def ask_int(self, prompt: str, low: int, high: int) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("⚠️ 숫자를 입력하세요.")
            continue
        if low <= value <= high:
            return value
        print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")
```

만약 마지막 `return value` 줄을 아래처럼 `print(value)`로 바꿔버렸다고 가정해보자.

```python
# 잘못된 버전 (가정) — return을 print로 바꿈
def ask_int(self, prompt: str, low: int, high: int) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("⚠️ 숫자를 입력하세요.")
            continue
        if low <= value <= high:
            print(value)   # return value 대신 print(value)로 바뀜
        print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")
```

이 잘못된 버전은 화면에 숫자를 출력하긴 하지만, 함수를 명시적으로 종료(return)하지 않는다. 파이썬에서는 함수 끝까지 실행되도록 `return`을 아예 만나지 못하거나, `return` 뒤에 값을 쓰지 않으면(단독 `return`) **자동으로 `None`을 반환**한다는 규칙이 있다. 위 잘못된 버전은 `if low <= value <= high:` 블록 안에서 `print(value)`만 하고 `return`을 쓰지 않았으므로, while 루프가 다음 줄인 `print(f"⚠️ ...")`까지 실행한 뒤 다시 루프 맨 위로 돌아가 버린다(심지어 정상 입력을 했는데도 경고 메시지가 뜨는 이상한 동작까지 생긴다). 그리고 만에 하나 루프를 벗어나는 경로가 있었다 해도, 함수가 `return value` 없이 끝나면 호출자가 받는 값은 언제나 `None`이다.

이게 왜 문제인지는 `run()`의 실제 코드를 보면 바로 드러난다.

```python
# 실제 코드 (main.py, run())
choice = self.ask_int("선택: ", 1, 6)
if choice == 1:
    self.play_quiz()
elif choice == 2:
    self.add_quiz()
elif choice == 3:
    self.show_quiz_list()
elif choice == 4:
    self.show_score()
elif choice == 5:
    self.delete_quiz()
else:
    self.save_state()
    print("\n👋 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
    return
```

`ask_int()`가 `None`을 반환하게 되면 `choice`에는 `None`이 담긴다. 그러면 `choice == 1`, `choice == 2`, …, `choice == 5` 모든 비교가 `False`가 되어 `if`/`elif` 체인을 전부 통과해버리고, 결국 마지막 `else` 블록으로 빠진다. 이 `else`는 "종료" 처리를 담당하는 분기다. 즉 사용자가 메뉴에서 분명히 `1`을 정확히 입력해서 퀴즈를 풀려고 했는데도, `ask_int()`가 값을 돌려주지 않는 순간 프로그램은 아무 문제 없이 조용히 종료돼버린다. 에러 메시지도 뜨지 않고 예외도 발생하지 않기 때문에, 이런 버그는 겉으로는 "그냥 프로그램이 이상하게 바로 꺼진다"는 증상으로만 나타나서 원인을 찾기 까다롭다. `return`을 빠뜨리는 실수가 왜 조용하고 치명적인지 보여주는 좋은 예다.

**TL;DR**: `return`이 없거나 값 없이 끝나는 함수는 파이썬이 자동으로 `None`을 돌려주므로, `ask_int()`가 `print`만 하고 `return`하지 않으면 `choice`가 `None`이 되어 `if choice == 1:` 이하 모든 분기가 거짓이 되고 프로그램은 곧장 종료 분기(`else`)로 빠진다.

### if not raw:가 참이 되는 입력을 설명할 수 있다.

`ask_int()`의 두 번째 줄은 이렇게 시작한다.

```python
raw = input(prompt).strip()
if not raw:
    print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
    continue
```

여기서 `raw`는 사용자가 입력한 문자열을 `.strip()`으로 앞뒤 공백까지 제거한 결과다. `if not raw:`가 참(`True`)이 되는 경우는 정확히 두 가지다.

1. **사용자가 아무것도 입력하지 않고 Enter만 친 경우**: `input()`이 곧바로 빈 문자열 `""`을 돌려주고, `"".strip()`도 여전히 `""`이다.
2. **공백 문자만 입력한 경우**: 예를 들어 `"   "`(스페이스 세 칸)를 입력하면 `input()`은 `"   "`을 돌려주지만, `.strip()`이 앞뒤 공백을 모두 걷어내면서 `"   ".strip() == ""`가 되어 결국 빈 문자열로 바뀐다.

두 경우 모두 최종적으로 `raw`가 빈 문자열 `""`이 된다는 점이 핵심이다. 파이썬에는 "Falsy(거짓처럼 취급되는 값)"라는 규칙이 있는데, 빈 문자열 `""`은 그 대표적인 예다. 그래서 `not ""`은 `True`가 된다. `not raw`는 결국 `raw`가 Falsy인지, 즉 빈 문자열인지를 검사하는 것과 같다.

```python
>>> not ""
True
>>> not "   ".strip()
True
>>> not "1"
False
```

동일한 검사를 `raw == ""`로 써도 이 두 경우(빈 입력, 공백만 입력)에 대해서는 결과가 완전히 같다. 즉 `if not raw:`와 `if raw == "":`는 이 함수의 문맥에서 동일하게 동작한다. 다만 파이썬 커뮤니티에서는 문자열이나 리스트 같은 값이 "비어 있는지"를 검사할 때 `== ""`나 `== []`처럼 값을 직접 비교하기보다, Falsy 규칙을 이용한 `not raw`, `not some_list` 형태를 더 자주 쓰는 관용구로 취급한다. 짧고, "raw에 유효한 내용이 없다"는 의도를 더 직접적으로 드러내기 때문이다. 두 표현이 같은 결과를 내는 상황에서는 어느 쪽을 써도 틀리지 않지만, 프로젝트 코드 스타일을 읽거나 맞출 때는 `not raw` 쪽이 더 널리 쓰인다는 점을 알아두면 된다.

**TL;DR**: `if not raw:`는 `raw = input(prompt).strip()` 이후이므로, 사용자가 Enter만 친 빈 문자열(`""`)과 공백만 입력해 `strip()` 후 빈 문자열이 된 경우(`"   ".strip() == ""`) 둘 다를 걸러내며, 이는 파이썬에서 빈 문자열이 Falsy로 취급되기 때문이다.

---

## 참고 문서

- [Step 0 학습 노트](step0_dev_environment_git_init.md) — 개발 환경 설정과 Git 저장소 초기화
- [Step 1 학습 노트](step1_quiz_model.md) — Quiz 모델과 자료구조 기본 데이터
- [Step 2 학습 노트](step2_quizgame_menu.md) — QuizGame, 메뉴, 공통 입력과 안전 종료
- [Step 3 학습 노트](step3_play_quiz_branch.md) — feat/play-quiz 브랜치와 퀴즈 풀기
- [Step 4 학습 노트](step4_add_list_score.md) — 퀴즈 추가, 목록 조회, 점수 확인
- [Step 5 학습 노트](step5_state_persistence.md) — state.json 영속성과 4대 복구 경로
- [Step 6 학습 노트](step6_clone_pull.md) — clone과 pull 실습
- [Step 7 학습 노트](step7_bonus_features.md) — 보너스 과제 5종
- [학습 체크리스트](../learning_checklist.md) — 이 문서의 원본 체크리스트
- [프로젝트 README](../../README.md) — 실제로 작성된 프로젝트 설명 문서
