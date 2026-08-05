# 10-2. 클래스와 객체(OOP) — 자가 점검 학습 노트

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "10. 학습 목표와 자가 점검" 아래 "10-2. 클래스와 객체(OOP)" 7개 항목을 학습 자료로 재구성한 것입니다. [10-1. Python 기초](python_basics_self_check.md)에 이어지는 자가 점검 시리즈의 두 번째 문서입니다.
>
> 모든 예시는 실제 `quiz.py`·`main.py` 코드와, 이 프로젝트 자체의 학습 가이드([`docs/learning_guide.md`](../learning_guide.md))에 이미 있는 설명을 근거로 작성했습니다. `QuizGame`에는 `self.storage` 같은 속성이 존재하지 않는 등, 실제 코드에 없는 이름은 지어내지 않았습니다.

## 목차

- 클래스·객체와 병렬 리스트의 위험
- __init__과 self
- 속성과 메서드의 차이
- 책임 분리와 to_dict/from_dict

---

## 클래스·객체와 병렬 리스트의 위험

이 두 항목은 사실 이 프로젝트의 학습 가이드(`docs/learning_guide.md`) Step 1 도입부에 이미 정리되어 있는 설명입니다. 새로 지어내는 개념이 아니라, 그 문서의 "1-1. 🧠 개념: 왜 클래스를 쓰나요?" 절에 있는 원문을 그대로 가져와서 자가 점검용으로 다시 풀어보는 것이 이 절의 목표입니다. 먼저 그 원문을 그대로 인용합니다.

```python
# ❌ 리스트 3개로 따로 관리하면?
questions = ["스택의 처리 방식은?", "큐의 처리 방식은?"]
choices   = [[...], [...]]
answers   = [2, 2]
# → questions[1]의 정답은 answers[1]... 인덱스가 어긋나면 조용히 망가집니다.

# ✅ 하나로 묶으면?
quiz = Quiz(
    "스택(Stack)의 자료 처리 방식은?",
    ["FIFO (선입선출)", "LIFO (후입선출)", "우선순위 순", "무작위 접근"],
    2,
)
quiz.question   # 문제
quiz.answer     # 정답
```

같은 문서는 이어서 다음과 같이 정의합니다.

- **클래스(class)** = 설계도 (붕어빵 틀)
- **객체/인스턴스(instance)** = 설계도로 찍어낸 실물 (붕어빵)

아래 두 항목은 이 정의와 이 비교 코드를 각각 다른 각도에서 다시 확인하는 것입니다.

### 클래스와 객체의 차이, 그리고 Quiz 클래스를 쓰는 이유를 설명할 수 있다

붕어빵 비유를 그대로 이어가 보면, **틀(클래스)** 은 "붕어빵은 이런 모양이고, 이런 재료가 들어간다"는 설계만 갖고 있을 뿐 그 자체로는 먹을 수 없습니다. 실제로 반죽을 붓고 구워서 나온 **붕어빵 한 개 한 개(객체/인스턴스)** 가 우리가 손에 쥐고 먹는 것입니다. 같은 틀에서 나온 붕어빵도 안에 든 팥의 양이나 굽기 정도는 저마다 다를 수 있는 것처럼, 같은 클래스에서 만들어진 객체도 각자 다른 데이터를 담을 수 있습니다.

이 프로젝트에서 그 틀에 해당하는 것이 `quiz.py`의 `Quiz` 클래스입니다.

```python
class Quiz:
    """문제, 선택지 4개, 정답 번호와 선택적 힌트를 관리하는 퀴즈 모델."""

    def __init__(
        self,
        question: str,
        choices: list[str],
        answer: int,
        hint: str | None = None,
    ) -> None:
        ...
        self.question = question
        self.choices = list(choices)
        self.answer = answer
        self.hint = hint
```

`Quiz`라는 틀 자체는 "퀴즈는 문제 하나, 선택지 4개, 정답 번호 하나, 힌트(선택)로 구성된다"는 **규칙**만 정의하고 있을 뿐, 이 틀 하나가 곧 어떤 특정 퀴즈는 아닙니다. 실제로 "스택의 자료 처리 방식은?"이라는 구체적인 퀴즈가 되려면 이 틀로 붕어빵을 하나 구워내야 하는데, 그게 바로 `Quiz(question, choices, answer, hint)`를 호출하는 순간입니다.

이 일이 실제로 일어나는 지점을 프로젝트 코드에서 두 군데 확인할 수 있습니다. 첫째, `quiz.py`의 `get_default_quizzes()`는 저장된 데이터가 없을 때 쓸 기본 퀴즈를 만드는 함수인데, 안을 들여다보면 `Quiz(...)`를 다섯 번 호출해서 서로 다른 문제·선택지·정답·힌트를 가진 `Quiz` 인스턴스 5개를 만들어 리스트로 돌려줍니다. 같은 틀에서 스택 문제, 큐 문제, 해시 테이블 문제가 각각 독립된 객체로 찍혀 나오는 것입니다.

둘째, `main.py`의 `add_quiz()`에서는 사용자가 직접 입력한 값으로 새 퀴즈 객체가 만들어집니다.

```python
def add_quiz(self) -> None:
    ...
    self.quizzes.append(Quiz(question, choices, answer, hint))  # 여기서 __init__ 실행됨
```

`Quiz(question, choices, answer, hint)`가 호출되는 바로 이 순간에 `Quiz.__init__`이 자동으로 실행되면서 새로운 `Quiz` 인스턴스가 태어나고, 그 결과가 `self.quizzes` 리스트에 하나 더 쌓입니다. 즉 `Quiz`는 클래스(설계도) 하나뿐이지만, 프로그램이 실행되는 동안 `self.quizzes` 안에는 그 설계도로 찍어낸 서로 다른 객체가 여러 개 들어 있게 됩니다.

그렇다면 왜 굳이 `Quiz` 클래스를 만들어서 이렇게 쓰는 걸까요? 문제·선택지·정답·힌트는 "퀴즈 한 문제"라는 하나의 개념을 이루는 항목들이라서, 이 넷을 항상 하나로 묶어 다루는 것이 자연스럽기 때문입니다. 클래스로 묶으면 `quiz.question`, `quiz.choices`, `quiz.answer`, `quiz.hint`처럼 항상 **같은 객체 안에서** 관련 데이터를 꺼내 쓸 수 있고, `display()`나 `is_correct()`처럼 그 데이터를 다루는 동작도 같은 곳에 둘 수 있습니다. 이 장점은 바로 다음 항목에서 다룰 "병렬 리스트의 위험"과 정확히 대비됩니다.

**TL;DR: 클래스는 데이터의 구성 규칙만 담은 설계도(붕어빵 틀)이고, 객체(인스턴스)는 그 규칙대로 실제 값을 채워 만든 결과물(붕어빵)이며, `Quiz`는 `get_default_quizzes()`와 `add_quiz()`에서 실제로 여러 번 호출되어 문제마다 독립된 인스턴스를 만들어낸다.**

### 리스트 3개로 문제·선택지·정답을 따로 관리할 때 인덱스가 어긋날 위험을 설명할 수 있다

위에서 인용한 학습 가이드의 `❌` 예시는 문제·선택지·정답을 `questions`, `choices`, `answers`라는 서로 다른 리스트 3개에 나눠 담는 방식입니다. 이렇게 데이터를 나눠 담으면서도 "n번째 문제와 n번째 정답은 서로 짝"이라는 약속을 인덱스만으로 유지하는 구조를 흔히 **병렬 리스트(parallel list)** 라고 부릅니다. 문제는 이 약속이 코드 어디에도 강제로 적혀 있지 않다는 점입니다. `questions[1]`이 큐 문제라면 `answers[1]`도 큐의 정답이어야 하는데, 이걸 지켜주는 것은 오직 "두 리스트를 항상 같이, 같은 순서로 건드리겠다"는 개발자의 다짐뿐입니다.

이 프로젝트를 예로 삼아 좀 더 구체적으로 살펴보겠습니다. 만약 `Quiz` 클래스 없이 이 프로젝트를 `questions`, `choices_list`, `answers` 세 리스트로 만들었다고 가정해 보겠습니다. 8-4에 해당하는 퀴즈 삭제 기능은 실제 `main.py`의 `delete_quiz()`에서 다음처럼 구현되어 있습니다.

```python
del self.quizzes[target_index]
```

`Quiz` 클래스를 쓰는 지금 구조에서는 이 한 줄로 문제·선택지·정답·힌트가 담긴 `Quiz` 객체 하나가 리스트에서 통째로 사라집니다. 그런데 만약 이걸 세 리스트 버전으로 옮겨 적었다면, 원래는 다음 세 줄을 **모두** 실행해야 삭제가 완성됩니다.

```python
# 병렬 리스트 버전이었다면 (이 프로젝트의 실제 구조가 아닌 가상의 예시)
del questions[target_index]
del choices_list[target_index]
del answers[target_index]
```

여기서 실수로 `del answers[target_index]`를 빼먹고 `del questions[target_index]`만 실행했다고 해봅시다. 예를 들어 총 5문제 중 2번째 문제(index 1, 큐 문제)를 삭제했다면, `questions` 리스트는 4개로 줄어들지만 `answers` 리스트는 여전히 5개 그대로 남습니다. 그 순간부터 `questions[1]`은 원래 3번째였던 해시 테이블 문제인데, `answers[1]`은 여전히 큐 문제의 정답인 1번을 가리키게 됩니다. index 1뿐 아니라 그 뒤에 있던 모든 문제의 정답이 한 칸씩 밀려서, 사용자가 정답을 맞혀도 프로그램은 오답 처리를 하고 오답을 골라도 정답 처리를 하는 상황이 벌어집니다. 더 무서운 점은 이 코드가 `IndexError` 하나 던지지 않고 조용히 실행된다는 것입니다. 학습 가이드의 표현대로 "인덱스가 어긋나면 조용히 망가집니다" — 에러 로그도, 경고 메시지도 없이 데이터만 틀어집니다.

`Quiz` 클래스를 쓰면 이런 위험 자체가 성립하지 않습니다. `self.quizzes.append(Quiz(question, choices, answer, hint))`로 추가하든, `del self.quizzes[target_index]`로 삭제하든, 조작 대상은 항상 "문제·선택지·정답·힌트를 한 몸으로 가진 `Quiz` 객체 하나"입니다. 리스트 하나(`self.quizzes`)만 관리하면 되기 때문에, 세 개의 리스트를 매번 같은 인덱스로 맞춰서 건드려야 한다는 부담 자체가 사라집니다. 즉 클래스는 단순히 "코드를 깔끔하게 정리하는" 취향의 문제가 아니라, 인덱스 불일치라는 조용한 버그의 발생 가능성 자체를 구조적으로 차단하는 안전장치입니다.

**TL;DR: 문제·선택지·정답을 리스트 3개로 따로 관리하면 한쪽만 수정(예: `del questions[idx]`)하고 다른 쪽(`del answers[idx]`)을 빼먹었을 때 인덱스가 어긋나 정답이 조용히 밀려버릴 수 있지만, `Quiz` 객체 하나로 묶어 `self.quizzes` 리스트 하나만 다루면 이런 어긋남이 애초에 발생할 수 없다.**

---
Source file written to: `/tmp/claude-1001/-home-jmlee-Project-second-project/80069fb6-be88-4bb0-b41b-475a5fbb3c9d/scratchpad/section_10-2_class_object_parallel_lists.md`

Facts verified directly against the repo before writing: `quiz.py`'s `Quiz` class and `get_default_quizzes()` (5 `Quiz(...)` calls), `main.py`'s `add_quiz()` and `delete_quiz()` (`del self.quizzes[target_index]`), and the exact quoted block in `docs/learning_guide.md` lines 349–364.

---

## __init__과 self

### __init__이 언제 실행되고 self가 어떤 역할을 하는지 설명할 수 있다.

`__init__`은 "괄호를 열고 닫아서 클래스를 호출하는 바로 그 순간" 파이썬이 자동으로 실행하는 메서드다. `Quiz(...)`처럼 클래스 이름 뒤에 괄호를 쓰면, 그 괄호가 실행되는 시점에 파이썬은 (1) 새 객체를 하나 만들고 (2) 그 객체를 `self`로 삼아 `__init__`을 즉시 호출한다. 우리가 따로 `__init__`을 호출하는 코드를 쓴 적이 없어도, `Quiz(question, choices, answer, hint)`라는 호출 문장 자체가 곧 `__init__` 호출이다.

이 프로젝트의 학습 가이드(docs/learning_guide.md)는 이미 이 관계를 붕어빵 틀에 비유해서 정의해 두었다: 클래스는 설계도(붕어빵 틀), 객체/인스턴스는 그 설계도로 찍어낸 실물(붕어빵), `__init__`은 객체가 태어날 때 자동 실행되는 초기화 메서드, `self`는 "지금 이 객체 자신"이다. 같은 문서에는 문제·선택지·정답을 따로따로 리스트 3개로 관리하면 인덱스가 어긋나 조용히 망가진다는 문제의식과 함께, 이렇게 하나로 묶는 예시가 있다.

```python
quiz = Quiz(
    "스택(Stack)의 자료 처리 방식은?",
    ["FIFO (선입선출)", "LIFO (후입선출)", "우선순위 순", "무작위 접근"],
    2,
)
```

이 `Quiz(...)` 호출이 실행되는 순간이 바로 `__init__`이 실행되는 순간이다. "객체를 생성할 때"라는 말을 추상적으로만 알고 넘어가지 말고, 이 프로젝트에서 실제로 그 순간이 어디인지 코드로 짚어보자.

- **`add_quiz()`에서 새 퀴즈를 추가할 때**: 사용자가 문제·선택지·정답·힌트를 입력하면, `self.quizzes.append(Quiz(question, choices, answer, hint))` 문장의 `Quiz(question, choices, answer, hint)` 부분이 실행되는 그 순간 `Quiz.__init__`이 호출되어 새 인스턴스가 만들어지고, 그 결과가 `self.quizzes` 리스트에 추가된다.
- **`get_default_quizzes()`에서 기본 퀴즈 5개를 만들 때**: 게임을 처음 시작해서 저장된 데이터가 없을 때 보여줄 기본 퀴즈 5개도 각각 `Quiz(...)` 형태로 호출되어 만들어진다. 다섯 번 호출되면 `__init__`도 다섯 번, 호출될 때마다 그때그때 실행된다.
- **`Quiz.from_dict()`의 `cls(...)` 호출에서**: `storage.py`의 `load_state()`가 저장 파일을 읽어 `[Quiz.from_dict(raw_quiz) for raw_quiz in raw_quizzes]`를 실행할 때, `from_dict` 안의 `return cls(question=..., choices=..., answer=..., hint=...)` 문장이 실행되는 순간에도 `__init__`이 호출된다. `cls`는 이 메서드가 `Quiz` 클래스에 붙어 있으므로 결국 `Quiz`를 가리키고, `cls(...)`는 `Quiz(...)`와 같은 효과를 낸다.

정리하면 이 프로젝트에서 `__init__`이 실행되는 지점은 정확히 이 세 곳(더하기, 그 세 곳 각각이 여러 번 반복 호출될 때마다)이며, 다른 어디에서도 저절로 실행되지 않는다.

그렇다면 `self`는 무엇을 하는가. `__init__` 안에서 실제로 일어나는 대입문을 보자.

```python
def __init__(
    self,
    question: str,
    choices: list[str],
    answer: int,
    hint: str | None = None,
) -> None:
    ...
    self.question = question
    self.choices = list(choices)
    self.answer = answer
    self.hint = hint
```

`self.question = question`에서 오른쪽 `question`은 이 함수가 호출될 때 잠깐 전달받은 매개변수, 즉 함수가 끝나면 사라질 임시 값이다. 왼쪽 `self.question`은 다르다. `self`는 "지금 만들어지고 있는 이 `Quiz` 인스턴스 자신"을 가리키는 이름이고, `self.question = question`은 그 임시 값을 이 인스턴스에 `question`이라는 이름의 속성으로 영구히 저장하는 것이다. `__init__` 실행이 끝나고 함수가 종료돼도 `self.question`, `self.choices`, `self.answer`, `self.hint`는 그 인스턴스 안에 계속 남아 있고, 이후 `display()`, `is_correct()`, `get_correct_text()`, `to_dict()` 같은 메서드들이 같은 `self`를 통해 이 값들을 꺼내 쓴다. `self`가 없다면 "이 값을 어느 객체에 저장할지"를 지정할 방법이 없다.

**TL;DR: `__init__`은 `Quiz(...)`(또는 `from_dict`의 `cls(...)`)처럼 클래스를 괄호로 호출하는 바로 그 순간 자동 실행되고, `self`는 그렇게 지금 만들어지는(또는 이미 만들어진) 객체 자신을 가리켜 `self.속성 = 값`으로 그 객체에 데이터를 영구 저장하는 통로다.**

### self 매개변수를 빼면 생길 오류와 이유를 설명할 수 있다.

`quiz.get_correct_text()`처럼 인스턴스를 통해 메서드를 호출하면, 파이썬은 그 호출을 내부적으로 `Quiz.get_correct_text(quiz)`로 바꿔서 실행한다. 즉 우리가 괄호 안에 아무것도 안 썼어도, 파이썬이 알아서 "이 메서드를 호출한 인스턴스 자신"을 첫 번째 인자로 몰래 끼워 넣는다. 그래서 메서드를 정의할 때 첫 번째 매개변수 자리에 `self`를 두어 그 자동으로 전달되는 인스턴스를 받아야 한다.

실제 `Quiz` 클래스의 `get_correct_text`는 이렇게 정의되어 있다.

```python
def get_correct_text(self) -> str:
    return self.choices[self.answer - 1]
```

여기서 `self`는 매개변수 1개다. `quiz.get_correct_text()`를 호출하면 파이썬은 이걸 `Quiz.get_correct_text(quiz)`로 바꿔 실행하므로, 정의된 매개변수 1개(`self`)에 전달된 인자 1개(`quiz`)가 정확히 맞아떨어져 정상적으로 `self.choices[self.answer - 1]`이 계산된다.

이제 만약 이 메서드에서 `self`를 뺀다면 어떻게 될지 보자. 아래는 **실제 코드가 아니라, self를 뺀 잘못된 가상의 예시**다.

```python
# ❌ 잘못된 예시(실제 프로젝트 코드 아님) — self를 빼고 정의했다고 가정
class Quiz:
    ...
    def get_correct_text() -> str:  # self가 없다
        return self.choices[self.answer - 1]
```

이 상태에서 기존과 똑같이 `quiz.get_correct_text()`를 호출하면, 파이썬은 여전히 인스턴스를 통한 호출이므로 자동으로 `Quiz.get_correct_text(quiz)`로 바꿔서 실행하려 한다. 그런데 방금 정의를 바꾼 `get_correct_text()`는 매개변수를 0개 받도록 되어 있다. 파이썬은 인자 1개(`quiz`)를 넘기려 하는데 정의부는 0개만 받게 생겼으니, 함수 본문(`return self.choices[...]`)이 실행되기도 전에 인자 개수가 안 맞는다는 이유로 다음과 같은 오류가 즉시 발생한다.

```
TypeError: get_correct_text() takes 0 positional arguments but 1 was given
```

여기서 중요한 점은, 이 오류가 `self.choices`나 `self.answer` 같은 본문 코드를 실행해 보기도 전에 "인자 개수 불일치" 단계에서 먼저 터진다는 것이다. `self`는 이름 자체에 무슨 마법이 있는 게 아니라(사실 `self`라는 이름은 관례일 뿐 `this` 등 다른 이름을 써도 동작은 같다), 인스턴스를 통해 메서드를 호출할 때 파이썬이 자동으로 넘기는 그 "첫 번째 자리"를 받아주는 매개변수가 반드시 있어야 한다는 것이 핵심이다. `self`를 빼면 그 자리를 받을 매개변수가 없어지므로, 인스턴스로 호출하는 모든 메서드 호출에서 인자 개수 불일치로 `TypeError`가 난다.

**TL;DR: `instance.method()` 호출은 파이썬 내부에서 `Class.method(instance)`로 바뀌어 실행되므로, 정의부에 인스턴스를 받을 `self` 자리가 없으면(예: `def get_correct_text():`처럼 self를 뺀 잘못된 정의) 인자 개수가 맞지 않아 `TypeError: get_correct_text() takes 0 positional arguments but 1 was given`이 발생한다.**

---

## 속성과 메서드의 차이

### 클래스의 속성(attribute)과 메서드(method)의 차이를 Quiz 또는 QuizGame 예로 설명할 수 있다.

이 프로젝트의 학습 가이드(`docs/learning_guide.md`)는 클래스를 붕어빵 틀에, 객체(인스턴스)를 그 틀로 찍어낸 실물 붕어빵에 비유하고, `__init__`을 "객체가 태어날 때 자동 실행되는 초기화 메서드", `self`를 "지금 이 객체 자신"이자 "속성을 저장·조회할 때의 통로"라고 정의합니다. 이 비유를 한 단계 더 밀고 나가면 속성과 메서드의 차이도 자연스럽게 설명됩니다.

- **속성(attribute)**: 붕어빵 안에 든 팥소, 크림 같은 **내용물**입니다. 그 붕어빵이 "무엇을 담고 있는지"를 나타내는 데이터·상태이며, 이름도 대체로 명사에 가깝습니다.
- **메서드(method)**: 그 내용물을 가지고 **무언가를 하는 동작**입니다. "먹는다", "자른다"처럼 이름이 동사에 가깝고, 속성값을 읽거나 바꾸거나 그 값을 이용해 판단을 내립니다.

핵심 원칙은 하나입니다. **속성은 실제로 `__init__` 등에서 `self.xxx = ...` 형태로 대입된 것만 존재합니다.** "이 클래스에는 이런 속성이 있을 것 같다"고 이름을 지어내면 안 되고, 반드시 코드에서 `self.무언가 = 무언가`로 대입되는 줄을 직접 찾아서 확인해야 합니다.

### Quiz의 속성과 메서드

`quiz.py`의 `Quiz.__init__`을 보면 대입되는 줄은 정확히 네 개입니다.

```python
self.question = question
self.choices = list(choices)
self.answer = answer
self.hint = hint
```

이 네 줄이 `Quiz`의 속성 전부입니다. 그 아래에 정의된 나머지는 전부 `def 이름(self, ...):` 형태의 메서드입니다.

| 구분 | 이름 | 무엇인가 |
|---|---|---|
| 속성 | `self.question` | 문제 문장(문자열) |
| 속성 | `self.choices` | 선택지 4개(리스트) |
| 속성 | `self.answer` | 정답 번호 1~4(정수) |
| 속성 | `self.hint` | 힌트 문자열 또는 `None` |
| 메서드 | `display(self, number=None)` | 문제와 선택지를 화면에 출력하는 동작 |
| 메서드 | `is_correct(self, user_answer)` | 입력값이 정답과 같은지 판정하는 동작 |
| 메서드 | `get_correct_text(self)` | 정답 선택지의 실제 텍스트를 꺼내는 동작 |
| 메서드 | `to_dict(self)` | 속성 4개를 JSON 저장용 딕셔너리로 바꾸는 동작 |
| 메서드 | `from_dict(cls, data)` | 딕셔너리로부터 새 `Quiz` 인스턴스를 만드는 동작(`@classmethod`) |

속성 이름이 전부 `question`, `choices`, `answer`, `hint`처럼 "이 퀴즈가 무엇을 갖고 있는가"를 답하는 명사인 반면, 메서드 이름은 `display`, `is_correct`, `get_correct_text`, `to_dict`, `from_dict`처럼 "이 퀴즈로 무엇을 하는가"를 답하는 동사(또는 동사구)라는 점이 눈에 띕니다.

### QuizGame의 속성과 메서드

`main.py`의 `QuizGame.__init__`도 같은 방식으로 확인할 수 있습니다.

```python
self.quizzes: list[Quiz] = []
self.best_score: int = 0
self.best_correct: int = 0
self.best_total: int = 0
self.history: list[dict[str, Any]] = []
```

| 구분 | 이름 | 무엇인가 |
|---|---|---|
| 속성 | `self.quizzes` | 지금까지 등록된 `Quiz` 인스턴스 목록 |
| 속성 | `self.best_score` | 지금까지의 최고 점수 |
| 속성 | `self.best_correct` | 최고 기록을 세울 때의 정답 수 |
| 속성 | `self.best_total` | 최고 기록을 세울 때의 전체 문제 수 |
| 속성 | `self.history` | 지금까지의 풀이 기록 목록 |
| 메서드 | `show_menu(self)` | 메뉴 화면을 출력하는 동작 |
| 메서드 | `run(self)` | 메뉴 선택을 반복해서 받는 실행 루프 |
| 메서드 | `ask_int(self, prompt, low, high)` | 범위를 검증하며 정수를 입력받는 동작 |
| 메서드 | `ask_text(self, prompt)` | 빈 문자열을 막으며 텍스트를 입력받는 동작 |
| 메서드 | `ask_yes_no(self, prompt)` | 예/아니오 입력을 받는 동작 |
| 메서드 | `play_quiz(self)` | 퀴즈를 출제하고 채점하는 동작 |
| 메서드 | `add_quiz(self)` | 새 `Quiz`를 만들어 `self.quizzes`에 추가하는 동작 |
| 메서드 | `show_quiz_list(self)` | 등록된 퀴즈 목록을 출력하는 동작 |
| 메서드 | `delete_quiz(self)` | 퀴즈를 목록에서 삭제하는 동작 |
| 메서드 | `show_score(self)` | 최고 점수를 출력하는 동작 |
| 메서드 | `save_state(self)` | 현재 상태를 파일에 저장하는 동작 |
| 메서드 | `load_state(self)` | 파일에서 상태를 불러와 속성에 채우는 동작 |

여기서도 `quizzes`, `best_score`, `history`처럼 속성은 "무엇을 갖고 있는가"를 답하는 명사이고, `show_menu`, `play_quiz`, `save_state`처럼 메서드는 "무엇을 하는가"를 답하는 동사(구)라는 패턴이 그대로 반복됩니다.

### "속성처럼 보이지만 존재하지 않는 이름"을 조심하기

`QuizGame`을 처음 보면 "파일 저장을 담당하니 `self.storage` 같은 속성이 있지 않을까"라고 추측하기 쉽습니다. 하지만 실제 `__init__`에는 그런 대입이 **없습니다**. `main.py` 맨 위를 보면 저장·불러오기 함수는 이렇게 모듈 함수로 직접 import됩니다.

```python
from storage import load_state as load_quiz_state
from storage import save_state as save_quiz_state
```

그리고 `QuizGame.save_state()`/`load_state()` 메서드 안에서 이 함수들을 바로 호출할 뿐, 그 결과를 `self.storage = ...`처럼 인스턴스에 저장해 두지 않습니다.

```python
def save_state(self) -> bool:
    return save_quiz_state(
        self.quizzes, self.best_score,
        best_correct=self.best_correct, best_total=self.best_total,
        history=self.history,
    )
```

즉 "저장 기능을 쓰니까 저장 객체를 속성으로 들고 있을 것"이라는 추측은 이 프로젝트의 실제 구조와 다릅니다. `QuizGame`은 `storage.py`의 함수를 **그때그때 호출**할 뿐, 그 함수(또는 어떤 "storage 객체")를 자기 속성으로 보관하지 않습니다. 속성 목록을 확인하는 유일하게 믿을 수 있는 방법은 눈으로 `__init__`을 열어서 `self.xxx = ...` 대입 줄을 직접 세어 보는 것입니다.

### 속성은 값, 메서드는 그 값으로 하는 동작

같은 `quiz` 인스턴스에서 다음 두 줄을 나란히 놓아 보면 차이가 분명해집니다.

```python
quiz.answer                # 속성: 정답 번호 그 자체 (예: 2)
quiz.is_correct(quiz.answer)  # 메서드: 그 값을 이용해 "정답인가?"라는 판정을 수행 → True
```

`quiz.answer`는 그냥 데이터입니다. 괄호도 없고, 아무 동작도 하지 않습니다. 그냥 `Quiz` 인스턴스 안에 저장된 정수값을 꺼내 올 뿐입니다. 반면 `quiz.is_correct(quiz.answer)`는 괄호와 함께 호출되고, 그 안에서 `isinstance()` 검사와 `==` 비교라는 실제 동작을 수행한 뒤 `True`/`False`라는 새로운 결과를 만들어 돌려줍니다. 하나는 "무엇을 갖고 있는가"에 대한 대답이고, 다른 하나는 "그 무엇으로 무엇을 했는가"에 대한 대답입니다. `play_quiz()` 안에서 실제로 `quiz.is_correct(user_answer)`를 호출해 정오답을 판정하는 것도 같은 이유입니다 — 정답 여부를 판단하는 로직은 `Quiz`가 가장 잘 알고 있는 자기 속성(`self.answer`)을 이용해야 하므로, `QuizGame`이 직접 비교하지 않고 `Quiz`의 메서드에게 그 동작을 맡깁니다.

**TL;DR: 속성은 `__init__`에서 `self.xxx = ...`로 실제 대입된 데이터(예: `quiz.answer`, `game.quizzes`)이고, 메서드는 그 데이터를 이용해 무언가를 수행하는 동작(예: `quiz.is_correct(...)`, `game.save_state()`)이다 — `QuizGame`에 `self.storage`가 없듯, 존재를 확인하지 않은 속성 이름은 지어내지 않는다.**


---

## 책임 분리와 to_dict/from_dict

### Quiz와 QuizGame의 책임을 왜 분리했는지 설명할 수 있다

이 프로젝트에는 클래스가 두 개 있습니다. `Quiz`와 `QuizGame`입니다. 이 둘은 이름만 다른 게 아니라, **아는 것과 알아야 할 일 자체가 다릅니다.**

- `Quiz`는 문제 **한 건**의 데이터(`question`/`choices`/`answer`/`hint`)를 검증해서 들고 있고, 그 데이터를 다루는 동작(`display()`, `is_correct()`, `get_correct_text()`, `to_dict()`, `from_dict()`)을 제공합니다. 이 퀴즈가 다른 퀴즈들과 어떻게 리스트로 묶이는지, 메뉴가 어떻게 출력되는지, 파일이 언제 저장되는지는 전혀 모릅니다.
- `QuizGame`은 여러 `Quiz` 인스턴스를 `self.quizzes` 리스트로 모아 관리하면서, 메뉴 출력·사용자 입력·게임 진행·최고 기록·히스토리·저장/불러오기 호출을 담당합니다. 대신 "문제 하나의 정답이 몇 번인지 판정하는 구체적인 방법"은 QuizGame이 직접 짜지 않습니다.

말로만 하면 추상적이니, 실제로 `play_quiz()` 안에서 정답을 확인하는 지점을 봅시다.

```python
# main.py의 QuizGame.play_quiz() 발췌
user_answer = self.ask_int("\n정답 입력 (1-4, 0: 힌트): ", 0, 4)
...
if quiz.is_correct(user_answer):
    correct += 1
    ...
    print("✅ 정답입니다! (1점 획득)")
else:
    print(
        f"❌ 오답입니다! 정답은 {quiz.answer}번 "
        f"({quiz.get_correct_text()})입니다."
    )
```

여기서 QuizGame이 아는 것은 딱 하나, **"지금 사용자가 입력한 답이 몇 번인지"**(`user_answer`)뿐입니다. "이 퀴즈의 정답이 몇 번인지, 그리고 사용자의 답과 어떻게 비교해서 맞았다고 판단하는지"는 QuizGame이 몰라도 됩니다. 그 판단 로직은 `quiz.is_correct(user_answer)`로 **Quiz에게 위임**합니다. 실제로 `Quiz.is_correct()`는 이렇게 정의돼 있습니다.

```python
def is_correct(self, user_answer: int) -> bool:
    return (
        isinstance(user_answer, int)
        and not isinstance(user_answer, bool)
        and user_answer == self.answer
    )
```

이 비교 로직(정수인지 확인하고, `bool`은 제외하고, `self.answer`와 같은지 본다)은 오직 `Quiz` 안에만 존재합니다. QuizGame은 그저 "너의 정답과 이 값을 비교해봐"라고 물어보고 `True`/`False`만 돌려받을 뿐입니다. 이게 바로 "각자 자기가 제일 잘 아는 일만 한다"는 원칙입니다. 자기 문제의 정답이 몇 번이고, 어떻게 비교해야 하는지는 그 문제(Quiz) 자신이 제일 잘 압니다. 여러 퀴즈를 순서대로 보여주고 몇 번을 맞았는지 세는 일은 진행자(QuizGame)가 제일 잘 알고요.

이렇게 나누면 좋은 점은 **변경의 영향 범위가 좁아진다**는 것으로 구체화됩니다. 예를 들어 나중에 정답 판정 규칙을 "대소문자 무시" 또는 "복수 정답 허용"으로 바꾸고 싶다고 해봅시다. 그러면 고칠 곳은 `Quiz.is_correct()` **하나**뿐입니다. QuizGame의 메뉴 출력, `ask_int()`로 입력받는 흐름, `save_state()`로 저장하는 로직은 단 한 줄도 건드릴 필요가 없습니다. 반대로 저장 파일 형식을 바꾸거나 메뉴에 새 항목을 추가하고 싶다면, 그건 QuizGame 쪽만 고치면 되고 `Quiz.is_correct()`는 그대로 둡니다. 책임이 섞여 있었다면(예: QuizGame이 `if user_answer == quiz.answer:`처럼 직접 비교했다면) 정답 판정 규칙이 하나 바뀔 때마다 QuizGame 코드 여기저기에 흩어진 비교문을 전부 찾아 고쳐야 했을 것입니다.

**TL;DR: Quiz는 문제 하나의 데이터와 그 판정 로직을, QuizGame은 여러 문제를 모아 진행하는 흐름을 맡는다 — `quiz.is_correct(user_answer)`처럼 QuizGame은 판정을 Quiz에게 위임하므로, 판정 규칙이 바뀌어도 Quiz만 고치면 된다.**

### to_dict()를 Quiz에 두는 이유와 from_dict()에 @classmethod를 쓰는 이유를 설명할 수 있다

**`to_dict()`가 왜 Quiz에 있는가.** 어떤 객체를 딕셔너리로 바꾸려면 그 객체의 속성을 정확히 알아야 합니다. `question`, `choices`, `answer`, `hint`라는 이름과 그 값을 가장 정확히 아는 존재는 다름 아닌 Quiz 자기 자신입니다. 그래서 이 변환 동작도 Quiz 안에 둡니다.

```python
def to_dict(self) -> dict[str, Any]:
    return {
        "question": self.question,
        "choices": list(self.choices),
        "answer": self.answer,
        "hint": self.hint,
    }
```

만약 이 메서드가 없다면, 저장을 담당하는 바깥 코드(storage.py)가 매번 `quiz.question`, `quiz.choices`, `quiz.answer`, `quiz.hint`를 하나하나 꺼내서 딕셔너리를 직접 조립해야 합니다. 그러면 Quiz에 속성이 하나 추가되거나 이름이 바뀔 때마다 storage.py도 함께 고쳐야 하고, 조립 코드가 여러 군데 있다면 그중 하나를 빠뜨리는 실수도 생깁니다. `quiz.to_dict()` 한 번 호출로 위임하면, "Quiz를 dict로 바꾸는 방법"은 Quiz 안에서만 관리되고 바깥에서는 그 결과만 받아쓰면 됩니다.

**`from_dict()`가 왜 `@classmethod`인가.** 이건 호출되는 시점을 보면 이유가 분명해집니다. `storage.py`의 `load_state()`에는 이런 코드가 있습니다.

```python
quizzes = [Quiz.from_dict(raw_quiz) for raw_quiz in raw_quizzes]
```

이 시점을 잘 보면, `state.json`에서 막 읽어온 `raw_quiz`(그냥 평범한 dict)만 있을 뿐, **아직 어떤 Quiz 인스턴스도 존재하지 않습니다.** 만약 `from_dict`가 일반 메서드(`def from_dict(self, data)`)였다면, 호출하려면 `무언가.from_dict(raw_quiz)`처럼 이미 만들어진 Quiz 인스턴스가 있어야 합니다. 그런데 여기서 하려는 일은 "인스턴스를 이용해서 뭔가를 하는" 게 아니라, dict로부터 **새 인스턴스를 처음부터 찍어내는 것**입니다. 인스턴스가 없는 상태에서 뭔가를 만들어야 하니, 특정 인스턴스가 아니라 **클래스 이름 자체**(`Quiz`)로 바로 호출할 수 있어야 합니다. 그래서 `@classmethod`를 쓰고, 첫 번째 매개변수로 `self`(인스턴스) 대신 `cls`(클래스 자신)를 받습니다.

```python
@classmethod
def from_dict(cls, data: dict[str, Any]) -> "Quiz":
    if not isinstance(data, dict):
        raise TypeError("퀴즈 데이터는 딕셔너리여야 합니다.")
    return cls(
        question=data["question"],
        choices=data["choices"],
        answer=data["answer"],
        hint=data.get("hint"),
    )
```

여기서 `cls(...)`가 하는 일은 결국 `Quiz(question=..., choices=..., answer=..., hint=...)`를 호출하는 것과 같습니다. `cls`는 이 메서드가 `Quiz.from_dict(...)`로 호출됐을 때 자동으로 `Quiz` 클래스 자체를 가리키므로, `cls(...)`는 곧 `Quiz(...)`이고, 이는 `Quiz.__init__`을 실행해 새 인스턴스를 만들어내는 생성 호출입니다. 그 결과로 만들어진 새 Quiz 인스턴스를 `return`하면, 리스트 컴프리헨션 `[Quiz.from_dict(raw_quiz) for raw_quiz in raw_quizzes]`이 raw dict 목록 전체를 Quiz 인스턴스 목록으로 바꿔줍니다.

정리하면, `to_dict()`는 "이미 있는 Quiz 인스턴스를 dict로 바꾸는 일"이라 인스턴스 메서드(`self`)로 충분하고, `from_dict()`는 "아직 인스턴스가 없는 상태에서 dict로부터 새 인스턴스를 만들어내는 일"이라 인스턴스가 아닌 클래스(`cls`)로 호출해야 하는 `@classmethod`가 필요합니다.

**TL;DR: to_dict()는 자기 속성을 가장 잘 아는 Quiz 자신이 dict로 변환을 맡는 것이고, from_dict()는 아직 인스턴스가 없는 상태에서 클래스 이름만으로 새 인스턴스를 만들어내야 하므로 `cls(...)`(= `Quiz(...)`)를 쓰는 @classmethod여야 한다.**

---

## 참고 문서

- [10-1. Python 기초](python_basics_self_check.md)
- [Step 0 학습 노트](step0_dev_environment_git_init.md) — 개발 환경 설정과 Git 저장소 초기화
- [Step 1 학습 노트](step1_quiz_model.md) — Quiz 모델과 자료구조 기본 데이터
- [Step 2 학습 노트](step2_quizgame_menu.md) — QuizGame, 메뉴, 공통 입력과 안전 종료
- [Step 3 학습 노트](step3_play_quiz_branch.md) — feat/play-quiz 브랜치와 퀴즈 풀기
- [Step 4 학습 노트](step4_add_list_score.md) — 퀴즈 추가, 목록 조회, 점수 확인
- [Step 5 학습 노트](step5_state_persistence.md) — state.json 영속성과 4대 복구 경로
- [Step 6 학습 노트](step6_clone_pull.md) — clone과 pull 실습
- [Step 7 학습 노트](step7_bonus_features.md) — 보너스 과제 5종
- [학습 체크리스트](../learning_checklist.md) — 이 문서의 원본 체크리스트
- [학습 가이드](../learning_guide.md) — Step별 실습 코드와 커밋 힌트
- [프로젝트 README](../../README.md) — 실제로 작성된 프로젝트 설명 문서
