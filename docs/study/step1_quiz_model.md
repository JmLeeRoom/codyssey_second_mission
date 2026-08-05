# Step 1 학습 노트 — Quiz 모델과 자료구조 기본 데이터

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "2. Step 1 — Quiz 모델과 자료구조 기본 데이터" 체크리스트를 바탕으로, `Quiz` 클래스와 기본 퀴즈 데이터가 왜 지금과 같은 모습으로 만들어졌는지 풀어 쓴 학습 자료입니다. [Step 0 학습 노트](step0_dev_environment_git_init.md)에 이어지는 시리즈입니다.
>
> 이 문서는 실제 `main.py`·`storage.py` 코드와, 이 저장소에서 직접 실행해 확인한 명령 결과를 근거로 작성했습니다. 계획(README·체크리스트)과 실제 구현이 갈라진 지점도 숨기지 않고 그대로 짚습니다 — 계획이 실제 코드를 작성하며 자연스럽게 바뀌는 것은 흔한 일이며, 그 차이를 알아채고 다루는 법 자체가 중요한 학습 내용이기 때문입니다.

## 목차

- 2-1. Quiz 클래스 설계
- 2-2. Quiz 메서드
- 2-3. 기본 퀴즈 함수와 단위 확인
- 2-4. Step 1 Git 체크포인트

---

## 2-1. Quiz 클래스 설계

### 계획과 실제 구현이 갈라진 지점부터 짚고 갑니다

체크리스트와 README.md의 "구현 목표 파일 구조"에는 원래 `quiz.py`라는 파일이 `Quiz` 클래스를 담당하도록 계획되어 있었습니다. 하지만 지금 저장소를 열어 보면 `quiz.py` 파일은 존재하지 않고, `Quiz` 클래스와 `get_default_quizzes()` 함수는 전부 `main.py` 안에 정의되어 있습니다. 작업 초기에 `quiz.py`가 빈 스캐폴드 파일로 잠깐 있었지만, 실제 커밋에는 포함되지 않고 내용이 `main.py`로 통합된 것입니다.

이 사실은 실제로 실행 오류로 확인할 수 있습니다. `storage.py` 9번째 줄에는 다음 코드가 있습니다.

```python
from quiz import Quiz, get_default_quizzes
```

지금 상태에서 이 모듈을 직접 import해 보면 다음과 같이 깨집니다.

```bash
$ python3 -c "import storage"
ModuleNotFoundError: No module named 'quiz'
```

`quiz.py`가 없으니 당연한 결과입니다. 반면 `python3 main.py`는 문제없이 실행됩니다. `main.py`는 `storage.py`를 import하지 않고, 자기 자신 안에서 `Quiz`를 정의해서 그대로 쓰기 때문입니다.

여기서 배울 점은 "계획 문서와 실제 코드는 언제든 어긋날 수 있고, 어긋난 채로 방치하면 다른 파일이 조용히 깨진다"는 것입니다. 지금 `storage.py`는 코드 자체는 멀쩡하지만 import 대상이 사라져서 실행 불가 상태입니다. 이런 어긋남을 발견했을 때는 (1) README나 체크리스트 같은 계획 문서를 실제 구조에 맞게 고치거나, (2) `quiz.py`를 다시 만들어 `Quiz`를 분리하거나, 둘 중 하나로 맞춰야 `storage.py`가 다시 동작합니다. 지금 당장 고치지 않더라도, "왜 안 되는지"를 정확히 아는 것이 중요합니다.

### `__init__`의 검증 코드가 하는 일

`main.py`의 `Quiz.__init__`은 다음과 같이 되어 있습니다.

```python
def __init__(self, question: str, choices: list[str], answer: int) -> None:
    if not isinstance(question, str):
        raise TypeError("문제는 문자열이어야 합니다.")
    if not isinstance(choices, list):
        raise TypeError("선택지는 문자열 목록이어야 합니다.")
    if len(choices) != 4:
        raise ValueError("선택지는 정확히 4개여야 합니다.")
    if not all(isinstance(choice, str) for choice in choices):
        raise TypeError("모든 선택지는 문자열이어야 합니다.")
    if isinstance(answer, bool) or not isinstance(answer, int):
        raise TypeError("정답 번호는 정수여야 합니다.")
    if not 1 <= answer <= 4:
        raise ValueError("정답 번호는 1~4 사이여야 합니다.")

    self.question = question
    self.choices = list(choices)
    self.answer = answer
```

각 검사가 왜 필요한지 하나씩 보면 다음과 같습니다.

- `len(choices) != 4`: 이 프로젝트의 퀴즈는 선택지가 항상 4개라는 규칙을 전제로 합니다. 만약 이 검사가 없다면 `display()`가 몇 번까지 출력해야 하는지, 사용자가 몇 번까지 입력할 수 있는지가 문제마다 달라져 버립니다. 생성 시점에 4개를 강제해 두면 이후 출력·입력·저장 어디에서도 "이 퀴즈는 선택지가 4개"라는 전제가 깨지지 않습니다.
- `isinstance(answer, bool) or not isinstance(answer, int)`: 파이썬에서 `bool`은 `int`의 서브클래스라서 `isinstance(True, int)`가 `True`로 나옵니다. 이 방어 코드가 없으면 실수로 `answer=True`를 넘겼을 때 이 값이 정수 `1`처럼 취급되어 통과해 버리고, `answer=False`는 `0`처럼 취급되어 범위 검사(`1 <= answer <= 4`)에서 걸러지긴 하지만 의도와 다른 방식으로 걸러집니다. `bool`을 먼저 걸러내야 "진짜 정수인지"를 정확히 판별할 수 있습니다. 같은 방어 로직이 `is_correct()`에도 똑같이 들어가 있습니다.
- `1 <= answer <= 4`: `answer`를 리스트 인덱스(0~3)가 아니라 **사용자에게 보여줄 번호**(1~4)로 저장하기로 정했기 때문에, 이 범위를 벗어나면 애초에 잘못된 데이터입니다.

### 1-based와 0-based, 두 세계를 구분하기

이 프로젝트에서 숫자 두 종류가 섞여 쓰입니다.

| 대상 | 범위 | 쓰이는 곳 |
|---|---|---|
| 사용자가 보고 입력하는 정답 번호 | 1~4 | `display()` 출력, 사용자 입력, `answer` 저장값 |
| 파이썬 리스트 인덱스 | 0~3 | `choices[0]` ~ `choices[3]` |

`answer`는 항상 1~4 사이의 "사람이 이해하는 번호"로 저장됩니다. 하지만 실제로 정답 텍스트를 꺼낼 때는 리스트이기 때문에 인덱스가 필요합니다. 이 두 세계가 만나는 지점이 바로 `get_correct_text()`입니다.

```python
def get_correct_text(self) -> str:
    return self.choices[self.answer - 1]
```

`answer - 1`이 1-based 번호를 0-based 인덱스로 바꾸는 변환입니다. 예를 들어 정답이 2번이면 `choices[2 - 1]`, 즉 `choices[1]`을 가져와야 두 번째 선택지가 나옵니다. 만약 여기서 `choices[answer]`로 잘못 쓰면 `answer=2`일 때 `choices[2]`, 즉 세 번째 선택지를 잘못 가져오게 됩니다. 반대로 `answer`를 0부터 저장하는 실수를 하면(예: 정답이 2번인데 `answer=1`로 저장) `display()`에서 사용자에게 보여주는 번호와 실제 저장된 값이 어긋나 버립니다.

정리하면, `-1` 변환은 오직 **"choices에서 정답 텍스트를 꺼낼 때"** 한 곳에서만 일어나야 하고, `answer` 자체는 항상 1~4의 사람 기준 번호로 유지되어야 합니다. 이 경계를 흐리지 않는 것이 이 클래스 설계의 핵심입니다.

---

## 2-2. Quiz 메서드

`Quiz` 클래스는 데이터만 들고 있는 것이 아니라, 화면에 문제를 보여주고(`display`) 정답을 판정하고(`is_correct`) 저장 가능한 형태로 변환하고 복원하는(`to_dict`/`from_dict`) 네 가지 행동을 갖추고 있습니다. 이 절에서는 각 메서드가 실제로 어떻게 구현되어 있는지, 그리고 왜 그렇게 짜여 있는지를 살펴봅니다.

### display(self, number=None) — 문제를 화면에 그리기

```python
def display(self, number: int | None = None) -> None:
    if number is not None:
        print(f"[문제 {number}] {self.question}")
    else:
        print(self.question)
    for index, choice in enumerate(self.choices, start=1):
        print(f"  {index}. {choice}")
```

`number` 인자를 선택적으로 받는 이유는 이 메서드가 두 가지 문맥에서 모두 쓰이기 때문입니다. 퀴즈 목록을 번호를 매겨 순서대로 출제할 때는 `display(1)`처럼 호출해 `[문제 1]`이 앞에 붙고, 단일 문제만 보여줄 때는 인자 없이 호출해 문제 문장만 출력할 수 있습니다. 선택지를 뿌리는 `for index, choice in enumerate(self.choices, start=1)` 부분이 핵심인데, `enumerate`의 기본 시작값은 0이므로 `start=1`을 지정하지 않으면 선택지가 `0. 1. 2. 3.`으로 출력되어 사용자가 실제로 입력해야 할 번호(1~4)와 화면에 보이는 번호가 어긋나게 됩니다. 실제로 `python3 main.py`를 실행하면 다음과 같이 출력되는데,

```
[문제 1] 스택(Stack)의 주요 자료 처리 방식은 무엇인가요?
  1. FIFO (선입선출)
  2. LIFO (후입선출)
  3. LILO (후입후출)
  4. 무작위 접근
```

이 `1.`~`4.` 표시가 곧 `self.answer`에 저장되는 값의 범위와 정확히 일치합니다. 즉 `display()`가 보여주는 번호 체계와 `answer`가 저장하는 번호 체계를 1-based로 통일해 둔 것이 이후 `is_correct()`를 단순하게 만드는 전제 조건이 됩니다.

### is_correct(self, user_answer) — bool 함정 걸러내기

```python
def is_correct(self, user_answer: int) -> bool:
    return (
        isinstance(user_answer, int)
        and not isinstance(user_answer, bool)
        and user_answer == self.answer
    )
```

겉보기에는 `user_answer == self.answer` 한 줄이면 충분해 보이지만, 그 앞에 `isinstance` 검사가 두 겹으로 붙어 있습니다. 첫 번째 `isinstance(user_answer, int)`는 문자열이나 `None` 같은 엉뚱한 타입이 들어왔을 때 예외 없이 바로 `False`를 반환하기 위한 방어입니다. 두 번째 `not isinstance(user_answer, bool)`이 이 절의 핵심 포인트입니다. 파이썬에서는 `bool`이 `int`의 서브클래스로 설계되어 있어서 `isinstance(True, int)`가 `True`이고, `True == 1`, `False == 0`이 실제로 성립합니다. 만약 이 두 번째 조건이 없다면, 정답이 1번인 문제에서 `quiz.is_correct(True)`를 호출했을 때 `True == 1`이 참이 되어 `is_correct()`가 `True`를 반환해 버립니다. 사용자가 숫자 대신 참/거짓 값을 잘못 넘기는 상황은 실제로는 드물지만, 이 방어 코드는 "타입이 맞는 값만 정답으로 인정한다"는 원칙을 명시적으로 지키기 위한 안전장치입니다. 흥미롭게도 같은 방어가 `__init__`의 `answer` 검증에도 그대로 들어 있습니다(`if isinstance(answer, bool) or not isinstance(answer, int)`). 즉 이 프로젝트는 데이터가 들어오는 입구(`__init__`)와 판정이 이루어지는 지점(`is_correct`) 두 군데 모두에서 같은 함정을 동일한 패턴으로 막고 있습니다.

### get_correct_text() — 체크리스트에는 없지만 실제로 쓰이는 편의 메서드

```python
def get_correct_text(self) -> str:
    return self.choices[self.answer - 1]
```

이 메서드는 체크리스트 원문에는 이름이 등장하지 않지만, 실제 `main.py`에는 구현되어 있고 `__main__` 블록의 자체 테스트에서 "정답 번호가 가리키는 선택지 텍스트가 기대한 문자열과 같은가"를 검증하는 데 쓰입니다. `self.answer`가 1-based인 반면 파이썬 리스트 인덱스는 0-based이므로 `self.answer - 1`로 변환해 조회하는데, 이 변환을 매번 호출부에서 반복하지 않고 메서드 안에 한 번만 캡슐화해 둔 것입니다. 나중에 채점 결과를 "정답은 2번, LIFO(후입선출)입니다"처럼 사람이 읽을 문장으로 보여줘야 할 Step 2 이후 단계에서 특히 유용하게 재사용될 자리입니다.

### to_dict / from_dict — JSON과 객체 사이의 왕복

```python
def to_dict(self) -> dict:
    return {"question": self.question, "choices": list(self.choices), "answer": self.answer}

@classmethod
def from_dict(cls, data: dict) -> "Quiz":
    if not isinstance(data, dict):
        raise TypeError("퀴즈 데이터는 딕셔너리여야 합니다.")
    return cls(question=data["question"], choices=data["choices"], answer=data["answer"])
```

`to_dict()`는 `Quiz` 객체를 `question`/`choices`/`answer` 세 키만 가진 순수한 dict로 풀어내는데, 이 형태는 `json.dump()`가 그대로 직렬화할 수 있는 JSON 호환 구조입니다. `from_dict()`는 그 반대 방향으로, dict를 받아 `cls(...)`를 호출해 다시 `Quiz` 인스턴스를 만듭니다. `@classmethod`로 선언되어 있기 때문에 `Quiz.from_dict(...)`처럼 클래스 자체에서 바로 호출할 수 있고, `__init__`이 이미 갖고 있는 모든 유효성 검사(문자열 여부, 선택지 4개, 정답 범위 등)를 그대로 통과시켜 복원합니다. 이 두 메서드가 왕복 변환으로 정확히 맞아떨어져야 하는 이유는, 이후 단계에서 `state.json` 같은 파일에 진행 상태를 저장하고 다시 불러올 때 이 왕복이 그대로 저장·복구의 기반이 되기 때문입니다. 저장할 때 정보가 조금이라도 누락되거나 복구할 때 다른 값으로 재구성되면 사용자가 이전에 풀던 퀴즈가 미묘하게 달라지는 버그로 이어집니다. `main.py`의 자체 테스트는 각 기본 문제마다 `Quiz.from_dict(quiz.to_dict())`로 복원한 뒤 `to_dict()` 결과가 원본과 동일한지를 `assert`로 직접 확인하고 있고, `python3 main.py` 실행 결과에서 다섯 문제 모두 이 검증을 통과했습니다.

### get_default_quizzes() — dict 목록이 아니라 Quiz 인스턴스 목록

`get_default_quizzes()`는 `[{"question": ...}, ...]` 같은 raw dict의 리스트가 아니라, `[Quiz(...), Quiz(...), ...]`처럼 이미 `Quiz` 인스턴스로 조립된 리스트를 반환합니다. 이렇게 해 두면 호출하는 쪽에서 곧바로 `.display()`나 `.is_correct()`를 호출할 수 있고, 매번 `from_dict()`를 거칠 필요가 없습니다. 실제로 담긴 5개 문제는 각각 문자열 문제 1개, 문자열 선택지 정확히 4개, 1~4 범위의 int 정답 번호를 갖고 있으며, `__init__`의 유효성 검사를 실제로 통과했다는 사실 자체가 이 조건이 지켜졌다는 증거입니다(조건을 어겼다면 객체 생성 시점에 `TypeError`나 `ValueError`가 발생했을 것입니다). `python3 main.py` 실행 로그의 `✅ 기본 퀴즈 개수: 5개 (최소 5개 이상)`와 `✅ 해시 테이블·BST를 포함한 기본 퀴즈 검증 완료!`가 이 조건들이 실제로 통과했음을 보여줍니다.

한 가지 짚어둘 점은, 이 5문제의 실제 구성이 README.md에 처음 기획했던 5문제와 다르다는 것입니다. 계획 단계에서는 "BFS가 사용하는 자료구조"와 "해시테이블 평균 탐색 O(1)" 문제가 포함되어 있었지만, 실제 구현에서는 이 둘이 "해시 함수의 핵심 역할"과 "이진 탐색 트리(BST)의 자식 노드 배치 규칙" 문제로 바뀌었습니다. 코드를 작성하다 보면 처음 기획과 실제 결과물 사이에 이런 차이가 생기는 일은 흔하며, 잘못된 것이 아닙니다. 다만 README.md의 "2. 퀴즈 주제와 선정 이유" 표는 아직 예전 5문제 그대로 남아 있으므로, 문서와 코드가 서로 다른 이야기를 하고 있는 상태입니다. 나중에 README를 갱신할 때 실제 `main.py`의 `get_default_quizzes()` 내용을 기준으로 표를 맞추는 작업이 남아 있다는 점을 기억해 두면 좋습니다.

---

## 2-3. 기본 퀴즈 함수와 단위 확인

### get_default_quizzes()는 왜 필요한가

`Quiz` 클래스는 문제 하나를 표현하는 "틀"일 뿐, 실제 문제 내용은 어딘가에서 채워 넣어야 합니다. 이 프로젝트는 퀴즈 진행 상태를 `state.json`에 저장했다가 다음 실행 때 이어서 읽어오도록 설계되어 있는데, 파일이 아예 없거나(첫 실행) 손상되어 있으면(JSON 파싱 실패 등) 무엇으로 채워야 할지 정해 둔 곳이 있어야 합니다. `get_default_quizzes()`가 바로 그 "출처(source of truth)" 역할을 합니다. `main.py`에는 이 의도가 함수의 docstring에 그대로 적혀 있습니다.

```python
def get_default_quizzes() -> list[Quiz]:
    """기본 자료구조 퀴즈 5개를 새 목록으로 반환한다.

    이 함수는 ``state.json``이 없거나 손상되어 ``load_state()``가
    복구해야 할 때 사용하는 기본 데이터의 단일 출처다.
    """
    return [ ... ]
```

체크리스트가 요구한 "함수가 Quiz 인스턴스 5개 이상 반환"과 "각 기본 퀴즈가 자료구조 주제이며 선택지 4개·정답 번호 1~4를 가짐"은 여기서 자연스럽게 충족됩니다. `Quiz.__init__`이 이미 `len(choices) != 4`와 `1 <= answer <= 4`를 강제로 검증하기 때문에(2-2절 참고), `get_default_quizzes()` 안에서 실수로 선택지를 3개만 적거나 정답 번호를 5로 적으면 이 함수를 호출하는 순간 바로 예외가 발생합니다. 즉 데이터 자체의 정합성을 함수 바깥의 별도 검사 없이 클래스가 보장해 주는 구조입니다.

### 실제로 들어 있는 5문제

`main.py`에 실제로 작성된 5문제는 다음과 같습니다.

| 번호 | 문제 | 정답 |
|---|---|---|
| 1 | 스택(Stack)의 주요 자료 처리 방식은 무엇인가요? | 2. LIFO (후입선출) |
| 2 | 큐(Queue)의 주요 특징으로 옳은 것은 무엇인가요? | 1. 먼저 들어간 데이터가 먼저 나온다 (FIFO) |
| 3 | 해시 테이블(Hash Table)에서 해시 함수(Hash Function)의 핵심 역할은 무엇인가요? | 2. 키(Key)를 해시값 또는 인덱스로 변환한다 |
| 4 | 이진 탐색 트리(BST)의 자식 노드 배치 규칙으로 옳은 것은 무엇인가요? | 2. 왼쪽 자식은 부모보다 작고, 오른쪽 자식은 크다 |
| 5 | 정렬된 N개의 배열에서 이진 탐색(Binary Search)의 시간 복잡도는 무엇인가요? | 2. O(log n) |

체크리스트가 요구한 항목들을 하나씩 대응해 보면, 스택 문제의 정답이 LIFO(2번)와 일치하고, 큐 문제의 정답이 FIFO(1번)와 일치하며, 해시 함수 문제는 "키를 해시값/인덱스로 변환한다"(2번)가 정답으로 지정되어 해시 테이블·해시 함수의 핵심 개념을 검증하는 문제 역할을 합니다. BST 문제는 "왼쪽 자식은 부모보다 작고, 오른쪽 자식은 크다"(2번)를 정답으로 두어 이진 탐색 트리의 서브트리 규칙을 정확히 반영하고 있고, 시간 복잡도 문제는 O(log n)(2번)을 정답으로 두어 이진 탐색의 로그 시간 복잡도를 검증합니다.

### 계획했던 5문제와 실제 5문제가 다릅니다

여기서 짚고 넘어갈 점이 하나 있습니다. `README.md`의 "2. 퀴즈 주제와 선정 이유" 표에는 Step 0 단계에서 처음 기획했던 5문제가 아직 그대로 남아 있는데, 그 내용은 스택(LIFO) / 큐(FIFO) / **너비 우선 탐색(BFS)에서 사용하는 자료구조** / 이진 탐색 O(log n) / **해시 테이블 평균 탐색 O(1)** 이었습니다. 그런데 실제로 `main.py`에 구현된 5문제를 보면 BFS 문제와 해시 테이블 평균 탐색 O(1) 문제는 빠지고, 대신 **해시 함수의 역할**을 묻는 문제와 **BST 자식 노드 배치 규칙**을 묻는 문제로 바뀌어 있습니다.

이런 차이는 잘못된 것이 아니라 코드를 작성하다 보면 흔히 생기는 자연스러운 일입니다. 처음 기획할 때는 "자료구조 다섯 가지를 폭넓게 다루자"는 큰 그림만 있었고, 막상 문제를 하나하나 작성하다 보면 "BFS는 큐를 다루는 두 번째 문제와 겹치는 느낌이 든다"거나 "해시 테이블은 O(1)보다 해시 함수의 동작 원리를 묻는 게 더 기초적이고 명확하다"처럼 더 나은 선택지가 떠오르는 경우가 많습니다. 다만 이렇게 구현이 계획에서 벗어났을 때는, 나중에 문서와 코드가 서로 다른 이야기를 하지 않도록 `README.md`의 표도 실제 5문제에 맞춰 갱신해 주는 작업이 필요합니다. 지금 당장 급한 일은 아니지만, Step 1 작업을 마무리하면서 "다음에 정리하면 좋은 문서 동기화 작업" 목록에 `README.md`의 퀴즈 표 갱신을 적어 두는 것을 권합니다.

### if __name__ == "__main__": 블록으로 임시 확인하기

체크리스트는 "개수/display()/is_correct()/to_dict()를 임시로 확인하라"고 안내하는데, `main.py`는 이를 파일 맨 아래 `if __name__ == "__main__":` 블록 안에서 처리합니다.

```python
if __name__ == "__main__":
    quizzes = get_default_quizzes()
    assert len(quizzes) >= 5
    print(f"✅ 기본 퀴즈 개수: {len(quizzes)}개 (최소 5개 이상)")

    expected_answers = (2, 1, 2, 2, 2)
    expected_correct_texts = (
        "LIFO (후입선출)",
        "먼저 들어간 데이터가 먼저 나온다 (FIFO)",
        "키(Key)를 해시값 또는 인덱스로 변환한다",
        "왼쪽 자식은 부모보다 작고, 오른쪽 자식은 크다",
        "O(log n)",
    )

    for number, (quiz, expected_answer, expected_text) in enumerate(
        zip(quizzes, expected_answers, expected_correct_texts, strict=True),
        start=1,
    ):
        quiz.display(number)
        assert len(quiz.choices) == 4
        assert quiz.answer == expected_answer
        assert quiz.get_correct_text() == expected_text
        assert quiz.is_correct(quiz.answer)
        assert not quiz.is_correct(0)

        restored_quiz = Quiz.from_dict(quiz.to_dict())
        assert restored_quiz.to_dict() == quiz.to_dict()
        print(f"  └─ 정답 {quiz.answer}번 판정 및 JSON 왕복 변환 확인")

    print("✅ 해시 테이블·BST를 포함한 기본 퀴즈 검증 완료!")
```

이 블록은 문제마다 다섯 가지를 순서대로 확인합니다. 선택지가 정확히 4개인지, `answer`가 기대한 정답 번호와 같은지, `get_correct_text()`가 기대한 정답 문구를 돌려주는지, `is_correct(quiz.answer)`가 `True`이고 관계없는 값인 `is_correct(0)`은 `False`인지, 그리고 `to_dict()`로 딕셔너리로 바꿨다가 `Quiz.from_dict()`로 복원했을 때 다시 `to_dict()`를 호출하면 원본과 완전히 같은 값이 나오는지(JSON 왕복 변환)까지 `assert`로 확인합니다. 하나라도 어긋나면 `AssertionError`가 발생해 즉시 문제를 알 수 있는 구조입니다.

실제로 `python3 main.py`를 실행하면 다음과 같이 출력됩니다.

```
✅ 기본 퀴즈 개수: 5개 (최소 5개 이상)
[문제 1] 스택(Stack)의 주요 자료 처리 방식은 무엇인가요?
  1. FIFO (선입선출)
  2. LIFO (후입선출)
  3. LILO (후입후출)
  4. 무작위 접근
  └─ 정답 2번 판정 및 JSON 왕복 변환 확인
...(문제 2~5도 동일한 형식으로 출력)...
✅ 해시 테이블·BST를 포함한 기본 퀴즈 검증 완료!
```

이 실행 결과는 `docs/screenshots/quiz.png`에 스크린샷으로 남아 있고, 이미 `6868c74` 커밋에 포함되어 원격 저장소에 push되어 있습니다.

### 왜 하필 if __name__ == "__main__": 가드를 쓰는가

체크리스트의 마지막 항목은 "임시 테스트 코드가 나중에 import될 때 자동 실행되지 않는지 확인"입니다. 파이썬은 어떤 파일이 실행될 때든 import될 때든 모듈 전역 범위의 코드를 위에서 아래로 순서대로 실행합니다. 차이는 딱 하나, 직접 실행된 파일에서는 특수 변수 `__name__`이 문자열 `"__main__"`이 되고, 다른 코드가 `import`한 모듈에서는 `__name__`이 그 모듈의 이름(예: `"main"` 또는 `"quiz"`)이 된다는 점입니다. `if __name__ == "__main__":` 조건문은 바로 이 차이를 이용해서, "이 파일이 직접 실행됐을 때만" 아래 블록을 돌리도록 막아 줍니다.

만약 이 가드가 없다면 어떻게 될까요? 예를 들어 나중에 `game.py` 같은 다른 파일에서 `from main import Quiz, get_default_quizzes`처럼 가져다 쓸 때마다, 매번 5문제를 화면에 출력하고 `assert` 검증까지 실행해 버릴 것입니다. 단순히 화면이 지저분해지는 정도가 아니라, import 시점에 예상치 못한 부작용(콘솔 출력, 검증 실패로 인한 프로그램 중단)이 생길 수 있어 다른 모듈을 조합해 쓰는 것 자체가 위험해집니다. `if __name__ == "__main__":` 가드는 "이 파일을 라이브러리(부품)로 쓸 때"와 "이 파일을 직접 실행해서 자체 점검할 때"를 분리해 주는, 파이썬에서 아주 흔히 쓰이는 관용구입니다.

### storage.py와의 연결에서 드러난 문제

다만 이 지점에서 실제로 문제가 하나 드러납니다. `storage.py` 9번째 줄에는 다음과 같이 적혀 있습니다.

```python
from quiz import Quiz, get_default_quizzes
```

이는 애초에 `README.md`의 "구현 목표 파일 구조"에서 `quiz.py`가 `Quiz` 클래스와 기본 데이터를 담당하도록 계획했기 때문입니다. 그런데 실제 구현은 `Quiz` 클래스와 `get_default_quizzes()`를 모두 `main.py` 안에 넣는 방식으로 진행되었고(`quiz.py`는 작업 초기에 빈 스캐폴드 파일로 잠깐 존재했지만 실제 커밋에는 포함되지 않았습니다), 그 결과 지금 저장소에는 `quiz.py` 파일 자체가 없습니다. 그래서 `storage.py`를 단독으로 import하면 다음과 같은 오류가 그대로 발생합니다.

```bash
$ python3 -c "import storage"
ModuleNotFoundError: No module named 'quiz'
```

반면 `python3 main.py`는 `storage.py`를 import하지 않고 자기 자신 안에서 `Quiz`를 정의하기 때문에 아무 문제 없이 실행됩니다. 정리하면, 지금 상태는 "`main.py` 단독 실행은 정상, `storage.py` 단독 import는 깨짐"이라는 두 가지 사실이 동시에 성립하는 상태입니다. 이것도 앞서 살펴본 README와 실제 구현의 차이와 같은 성격의 일로, 계획(파일을 나누어 두기)과 실제 구현(파일을 합치기)이 달라지면서 아직 정리되지 않은 연결 고리입니다. 지금 당장 게임이 동작하는 데는 지장이 없지만, `storage.py`가 실제로 사용되는 시점(상태 저장/불러오기 기능을 붙이는 다음 단계)이 오면 이 import 문을 `main.py` 구조에 맞게 정리해야 한다는 점을 기억해 두면 좋습니다.

---

## 2-4. Step 1 Git 체크포인트

체크리스트의 이 항목 6개는 지금 `docs/learning_checklist.md`에서 전부 `[ ]`로 남아 있습니다. 하지만 실제로 사용자가 붙여넣은 터미널 로그와 현재 저장소의 `git log --oneline` 결과를 대조해 보면, 커밋과 push 자체는 이미 실제로 끝나 있습니다. 체크박스가 안 채워진 것과 "실제로 안 했다"는 것은 다른 이야기입니다. 이 절에서는 무엇이 실제로 일어났는지, 원래 계획과 어떤 차이가 있었는지, 그리고 그 과정에서 벌어진 실수들을 순서대로 짚어봅니다.

### 이미 끝난 일부터 확인하기

지금 이 저장소에서 `git log --oneline`을 실행하면 다음과 같이 나옵니다.

```
6868c74 (HEAD -> main, origin/main) Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)
9d106fd Chore: 프로젝트 초기 설정 및 .gitignore 추가
...
```

`6868c74` 옆에 `HEAD -> main`과 `origin/main`이 나란히 붙어 있다는 것은, 로컬 브랜치의 최신 커밋과 원격(origin)의 `main` 브랜치가 완전히 같은 지점을 가리키고 있다는 뜻입니다. 즉 fast-forward 충돌이나 push 실패 없이 정상적으로 원격 반영까지 끝난 상태입니다. 체크리스트 항목으로 보면 "commit #2를 만들었다", "commit #3을 push했다"는 문구가 아직 체크되지 않았을 뿐, 실제로 커밋하고 push하는 동작 자체는 이미 수행된 것입니다.

### 커밋 #2와 #3이 왜 하나로 합쳐졌을까

여기서 가장 중요하게 짚어야 할 부분은, 원래 계획과 실제 결과가 정확히 일치하지는 않는다는 점입니다. 체크리스트는 원래 "Quiz 클래스 구현"(커밋 #2)과 "기본 퀴즈 데이터 5개 추가"(커밋 #3)를 서로 다른 두 개의 커밋으로 나누라고 안내하고 있었습니다. 하지만 실제 터미널 로그를 보면 이렇게 진행됐습니다.

```
$ git add .
$ git commit -m "Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)
> ^C
$ git commit -m "Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)"
[main 6868c74] Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)
 6 files changed, 314 insertions(+), 71 deletions(-)
 create mode 100644 docs/screenshots/git_check_point.png
 create mode 100644 docs/screenshots/git_setting.png
 create mode 100644 docs/screenshots/quiz.png
 create mode 100644 main.py
 create mode 100644 storage.py
```

`git add .` 한 번, `git commit` 한 번으로 `main.py`(Quiz 클래스 정의 + `get_default_quizzes()`의 5문제 + 자체 검증용 `if __name__ == "__main__"` 블록), `storage.py`, 스크린샷 3장, 체크리스트 문서 수정까지 전부 하나의 커밋 `6868c74`에 합쳐졌습니다. 원래 나누려던 커밋 #2(클래스 구현)와 커밋 #3(데이터 추가)의 경계가 사라진 것입니다.

이 상황은 사실 낯선 사고가 아니라, `docs/learning_checklist.md` 맨 위 "모든 기능 커밋에 적용할 공통 규율"에서 이미 경고하고 있던 바로 그 패턴입니다.

> 코드를 모두 작성한 뒤 커밋 명령만 연속 실행하지 않는다. 첫 커밋이 변경분을 모두 가져가면 나머지 커밋은 `nothing to commit`이 된다.

Quiz 클래스와 기본 퀴즈 5개 데이터를 따로 커밋하려면, 클래스 코드만 먼저 작성해서 커밋하고, 그다음 퀴즈 데이터를 추가로 작성해서 또 커밋해야 합니다. 그런데 실제로는 클래스와 데이터를 포함한 `main.py` 전체를 다 짜고 나서 한 번에 `git add .`을 실행했기 때문에, 그 시점에 스테이징 영역에는 이미 두 변경사항이 뒤섞여 있었습니다. 첫 번째 커밋이 이 변경분을 통째로 가져가 버렸으니, 만약 이어서 커밋 #3을 만들려고 했다면 `git status`에는 아무 변경사항도 남아있지 않아 그대로 `nothing to commit`이 됐을 것입니다. 참고로 파일을 지정하지 않고 `git add .`을 쓴 것도 Step 0의 1-5에서 배운 "파일을 콕 집어 add하기" 원칙과는 다른 방식입니다. 이번에는 `.gitignore`가 잘 갖춰져 있어 원치 않는 파일이 섞여 들어가는 사고는 없었지만, 습관적으로 `.`을 쓰는 것은 여전히 위험 요소로 남습니다.

### 따옴표 하나 때문에 멈춘 터미널

로그를 자세히 보면 첫 번째 `git commit -m "..."` 시도에서 닫는 따옴표(`"`)를 빼먹은 채 Enter를 쳤습니다.

```
$ git commit -m "Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)
>
```

bash는 명령을 한 줄씩 실행하는 것이 아니라, 따옴표나 괄호 같은 "짝이 맞아야 끝나는 문법"이 열려 있으면 아직 명령이 완성되지 않았다고 판단하고 계속 다음 줄을 입력받습니다. 그 표시가 바로 `>` 프롬프트입니다. 이 상태에서는 무엇을 입력해도 명령이 실행되지 않고 계속 따옴표가 닫히기만을 기다리는데, 실제로는 `Ctrl+C`(`^C`)로 취소하고 따옴표를 제대로 닫아 다시 실행해서 정상적으로 커밋을 완료했습니다. 이 장면은 bash에서 큰따옴표든 작은따옴표든 반드시 짝을 맞춰야 한다는 것을 보여주는 실제 사례입니다. 커밋 메시지가 길어지거나 괄호·특수문자가 섞일수록 따옴표를 빼먹기 쉬우므로, 명령을 입력하기 전에 따옴표 짝을 눈으로 한 번 세어보는 습관이 도움이 됩니다. `>` 프롬프트에 갇혔을 때 당황하지 말고 `Ctrl+C`로 빠져나온 뒤 처음부터 다시 입력하면 됩니다.

### git push origin이 별도 지정 없이 동작한 이유

이어지는 로그에서 `git push origin`만으로 push가 성공했습니다.

```
$ git push origin
...
To https://github.com/JmLeeRoom/codyssey_second_mission.git
   9d106fd..6868c74  main -> main
```

브랜치 이름을 생략했는데도 정확히 `origin/main`으로 올라간 것은 우연이 아닙니다. Step 0의 1-5 체크포인트에서 `git push -u origin main`을 실행하며 로컬 `main`과 원격 `origin/main` 사이에 추적 관계(upstream)를 이미 등록해 두었기 때문입니다. `-u` 플래그로 한 번 연결해 두면 이후로는 `git push`만 입력해도 Git이 "이 로컬 브랜치는 저 원격 브랜치와 짝지어져 있다"는 것을 기억하고 알아서 목적지를 채웁니다. Step 0과 Step 1이 이렇게 이어져 있다는 것을 확인해 두면, 왜 어떤 날은 `git push -u origin main`을 쓰고 어떤 날은 그냥 `git push`만 써도 되는지 헷갈리지 않게 됩니다.

### 이미 push된 이력, 지금 쪼개야 할까

커밋 #2와 #3을 지금이라도 정확히 나누고 싶을 수 있지만, 이미 `origin/main`까지 push된 커밋 `6868c74`를 둘로 쪼개려면 `git reset`이나 `git rebase -i`로 커밋 이력을 다시 써야 합니다. 이는 원격에 이미 반영된 커밋 해시를 바꿔버리는 작업이라, 다른 협업자가 이미 그 커밋을 받아갔다면 이력 충돌을 일으킬 수 있는 위험한 조작입니다. 지금 단계에서는 이미 벌어진 일을 억지로 되돌리기보다, "다음 기능을 구현할 때는 클래스를 완성하는 시점, 데이터를 추가하는 시점마다 각각 `git add`·`git commit`을 끊어서 실행하자"는 교훈으로 삼는 편이 훨씬 안전하고 실용적입니다.

### 체크리스트 갱신하기

정리하면, `git add`·`git commit -m "Feat: Quiz 클래스 구현 ..."`·`git push`는 실제로 모두 실행되어 원격까지 반영되었으므로 이 부분은 사실에 맞게 체크할 수 있습니다. 다만 "기본 퀴즈 데이터 추가를 위한 별도의 `git add`"와 "커밋 #3"은 실제로는 독립된 이벤트로 존재하지 않고 커밋 #2에 흡수되었으므로, 이 두 항목까지 체크해버리면 실제 이력과 어긋납니다. 체크리스트를 갱신할 때는 이 차이를 숨기지 말고, "커밋 #2와 #3이 실제로는 `6868c74` 하나로 합쳐졌다"는 사실을 메모로 남겨 두는 것이 정직한 기록입니다.

---

## 정리 — 확인하고 넘어가면 좋은 것들

Step 1에서 실제로 구현·검증까지 끝난 부분과, 아직 손볼 여지가 있는 부분을 구분하면 다음과 같습니다.

**이미 끝난 것 (코드·실행 결과로 확인됨)**
- `Quiz` 클래스의 생성·검증·출력·판정·직렬화(`to_dict`/`from_dict`) 전부 구현되고 `python3 main.py`로 직접 실행 검증됨
- `get_default_quizzes()`가 자료구조 주제 5문제를 `Quiz` 인스턴스 목록으로 반환
- 커밋 `6868c74`가 실제로 만들어져 `origin/main`까지 push됨(체크리스트의 체크 표시만 아직 갱신되지 않은 상태)

**다음에 정리하면 좋은 것 (계획과 실제가 갈라진 지점)**
- [ ] `storage.py`의 `from quiz import Quiz, get_default_quizzes`를 지금 구조(main.py에 `Quiz` 정의)에 맞게 고치기 — `quiz.py`를 다시 만들어 분리하거나, import 대상을 `main`으로 바꾸기
- [ ] README.md "2. 퀴즈 주제와 선정 이유" 표를 실제 5문제(스택/큐/해시 함수 역할/BST 자식 배치 규칙/이진 탐색 복잡도)에 맞게 갱신하기
- [ ] `docs/learning_checklist.md`의 "2-4. Step 1 Git 체크포인트" 체크박스를 실제 커밋 이력에 맞게 체크하기
- [ ] 다음 기능부터는 커밋을 더 잘게 나눠, 계획한 커밋 단위와 실제 커밋 단위가 어긋나지 않도록 하기

이 항목들을 정리한 뒤에는 [`docs/learning_checklist.md`](../learning_checklist.md)의 Step 2(메뉴 시스템과 예외 처리)로 넘어갈 수 있습니다.

## 참고 문서

- [Step 0 학습 노트](step0_dev_environment_git_init.md) — 개발 환경 설정과 Git 저장소 초기화
- [학습 체크리스트](../learning_checklist.md) — 이 문서의 원본 체크리스트
- [학습 가이드](../learning_guide.md) — 단계별 실습 코드와 커밋 힌트
- [프로젝트 README](../../README.md) — 실제로 작성된 프로젝트 설명 문서
