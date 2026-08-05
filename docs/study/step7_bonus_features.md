# Step 7 학습 노트 — 보너스 과제 5종

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "8. Step 7 — 보너스 과제 5종" 체크리스트를 바탕으로, 랜덤 출제·문제 수 선택·힌트·퀴즈 삭제·점수 히스토리 다섯 가지 선택 기능이 왜 이렇게 구현됐는지 풀어 쓴 학습 자료입니다. [Step 0](step0_dev_environment_git_init.md) → [Step 1](step1_quiz_model.md) → [Step 2](step2_quizgame_menu.md) → [Step 3](step3_play_quiz_branch.md) → [Step 4](step4_add_list_score.md) → [Step 5](step5_state_persistence.md) → [Step 6](step6_clone_pull.md)에 이어지는 시리즈의 아홉 번째 문서입니다.
>
> 이 문서는 실제 `main.py`·`quiz.py`·`storage.py` 코드와, 이 저장소에서 직접 확인한 명령 결과·터미널 로그를 근거로 작성했습니다. 이번 Step은 시리즈에서 처음으로 코드 구현과 체크리스트 체크 표시가 이미 함께 맞춰진 상태로 발견되었습니다 — 다만 그 결과물은 아직 커밋되지 않았습니다.

## 목차

- 8-1. 랜덤 출제
- 8-2. 문제 수 선택
- 8-3. 힌트
- 8-4. 퀴즈 삭제
- 8-5. 점수 히스토리

---

## 8-1. 랜덤 출제

이번 Step 7 보너스 과제는 지금까지의 시리즈와 살짝 다른 지점에서 출발합니다. `docs/learning_checklist.md`의 "8. Step 7 — 보너스 과제 5종" 아래 8-1~8-5 항목을 직접 grep으로 확인해 보면 전부 `[x]`로 체크되어 있습니다. Step 1~6에서는 코드가 먼저 완성되고 체크리스트 체크 표시가 한참 뒤에 따라오는 패턴이 반복됐는데, 이번엔 코드 구현과 체크리스트 갱신이 함께 이루어진 것입니다. 다만 `git status`를 보면 `main.py`, `quiz.py`, `storage.py`, `README.md`, `docs/learning_checklist.md`가 모두 `M`(수정, 미커밋) 상태입니다. 즉 "코드와 체크리스트는 이미 일치하는데, 그 결과물이 아직 하나도 커밋되지 않은" 상태에서 이 문서를 작성하고 있다는 점을 먼저 짚고 넘어가겠습니다. 커밋은 8-1~8-5를 모두 학습하고 정리한 뒤에 진행해도 늦지 않습니다.

### 체크리스트가 요구하는 것

8-1의 체크리스트 항목은 세 가지입니다.

- 원본 `self.quizzes` 순서를 바꾸지 않도록 복사본을 만든다.
- `quizzes_to_play = self.quizzes[:]`로 복사한 뒤 `random.shuffle(quizzes_to_play)`를 호출하고, 실제 출제에 `quizzes_to_play`를 사용한다.
- 같은 퀴즈를 여러 번 풀어 출제 순서가 바뀌는지 확인한다.

세 항목 모두 결국 하나의 질문으로 수렴합니다. "왜 `self.quizzes`를 직접 섞지 않고, 굳이 복사본을 만들어서 그걸 섞는가?"

### `[:]` 슬라이싱은 얕은 복사(shallow copy)를 만듭니다

실제 `main.py`의 `play_quiz()` 안에서 이 부분은 다음과 같이 구현되어 있습니다.

```python
# 저장·목록 조회에 쓰는 원본 순서는 유지하고, 출제용 복사본만 섞는다.
quizzes_to_play = self.quizzes[:]
random.shuffle(quizzes_to_play)
quizzes_to_play = quizzes_to_play[:count]
```

`self.quizzes[:]`는 리스트 전체를 슬라이싱하는 문법입니다. 시작 인덱스와 끝 인덱스를 생략했기 때문에 처음부터 끝까지 전체 범위를 잘라내는 셈이고, 그 결과로 `self.quizzes`와 **원소는 같지만 껍데기(리스트 객체)는 별개인** 새 리스트가 만들어집니다. 이것이 "얕은 복사"입니다. 얕다고 하는 이유는, 리스트라는 그릇 자체는 새로 만들어지지만 그 안에 담긴 `Quiz` 객체들은 복사되지 않고 원본과 같은 객체를 그대로 참조하기 때문입니다. 그래서 `quizzes_to_play`와 `self.quizzes`는 서로 다른 리스트이지만, `quizzes_to_play[0]`과 `self.quizzes`에서 같은 퀴즈를 가리키는 항목은 완전히 동일한 `Quiz` 객체입니다. 이번 8-1에서 중요한 건 딱 이 정도입니다 — **리스트의 순서(그릇)만 독립적으로 바꿀 수 있으면 충분**하고, `Quiz` 객체 내부까지 복제할 필요는 없습니다.

### 왜 `self.quizzes`를 직접 섞으면 안 되는가

만약 `random.shuffle(self.quizzes)`처럼 원본 리스트를 그대로 넘겼다면 어떻게 될까요? `random.shuffle()`은 리스트를 **제자리에서(in-place)** 섞습니다. 즉 새 리스트를 반환하는 게 아니라, 넘겨받은 리스트 객체 자체의 내부 순서를 바꿔버립니다. `self.quizzes`를 직접 넘기면 `self.quizzes`의 순서 자체가 영구적으로 뒤섞이게 되는 것입니다.

이게 왜 문제가 되냐면, `self.quizzes`는 퀴즈 출제에만 쓰이는 게 아니기 때문입니다. 메뉴 3번 "퀴즈 목록"은 `self.quizzes`를 그대로 순회하며 보여주고, `save_state()`로 저장할 때도 `self.quizzes`의 현재 순서 그대로 `state.json`에 기록됩니다. 사용자가 퀴즈를 등록한 순서, 예를 들어 "1번 스택, 2번 큐, 3번 배열..."처럼 자신이 입력한 순서를 기대하고 있는데, 퀴즈 한 판을 풀 때마다 그 순서가 계속 랜덤하게 뒤바뀐다면 사용자는 "내가 등록한 순서"를 완전히 잃어버리게 됩니다. 삭제할 때 번호로 지정하는 8-4 기능이나, 점수 확인 시 참조하는 순서 감각도 덩달아 신뢰할 수 없게 됩니다. 그래서 저장·목록 조회용 원본(`self.quizzes`)과 출제용 사본(`quizzes_to_play`)을 분리하는 것이 핵심입니다.

### 흔한 실수: `random.shuffle()`의 반환값

또 하나 자주 걸려 넘어지는 지점은 `random.shuffle()`의 반환값입니다. 이 함수는 리스트를 제자리에서 섞고 **`None`을 반환**합니다. 즉 다음처럼 쓰면 안 됩니다.

```python
# 잘못된 예시 — quizzes_to_play가 None이 되어버립니다
quizzes_to_play = random.shuffle(quizzes_to_play)
```

이렇게 쓰면 `quizzes_to_play`에는 섞인 리스트가 아니라 `None`이 대입되고, 이후 `quizzes_to_play`를 순회하려는 순간 `TypeError`가 발생합니다. 올바른 순서는 실제 코드처럼 셔플을 호출문 하나로 독립시키는 것입니다.

```python
quizzes_to_play = self.quizzes[:]  # 1. 복사
random.shuffle(quizzes_to_play)    # 2. 복사본을 제자리에서 섞는다 (반환값은 버림)
```

### 실제로 순서가 바뀌는지 확인한 로그

체크리스트 세 번째 항목인 "같은 퀴즈를 여러 번 풀어 출제 순서가 바뀌는지 확인한다"는 실제로 두 차례 실행해서 검증되었습니다. 첫 실행에서는 `[문제 1]`이 "큐(Queue)..."로 시작했고, 프로그램을 재실행한 뒤 같은 5문제를 다시 풀었을 때는 `[문제 1]`이 "스택(Stack)..."으로 바뀌어 시작했습니다. 등록된 퀴즈 목록 자체는 변하지 않았는데(3번 메뉴로 확인하면 순서가 그대로입니다) 출제되는 순서만 매번 달라진다는 것은, `quizzes_to_play`가 매 실행마다 새로 셔플된 사본이라는 것을 실제 동작으로 보여주는 증거입니다.

### 8-2로 이어지는 지점

바로 다음 줄인 `quizzes_to_play = quizzes_to_play[:count]`가 8-2(문제 수 선택)에서 다룰 부분입니다. 여기서 미리 짚어둘 점은, 이 슬라이싱이 **이미 섞인 뒤의 리스트**에서 앞쪽 `count`개를 잘라낸다는 것입니다. 셔플이 먼저 일어나고 자르기가 나중에 일어나기 때문에, 사용자가 문제 수를 5문제 중 2문제로 줄이더라도 그 2문제는 매번 다른 조합으로 뽑히게 됩니다. 만약 순서가 반대였다면(자르고 나서 섞는다면) 애초에 항상 같은 앞부분 문제들만 후보에 오르게 되므로, "섞은 뒤에 자른다"는 순서 자체가 랜덤 출제와 문제 수 제한이라는 두 요구사항을 동시에 만족시키는 핵심 설계입니다.

---

## 8-2. 문제 수 선택

### 왜 필요한가 — 항상 전체 문제를 다 풀 필요는 없다

8-1에서 매번 출제 순서를 무작위로 섞는 기능을 넣었다면, 8-2는 그 위에 "몇 문제를 풀지"를 사용자가 직접 정할 수 있게 해 주는 기능입니다. 등록된 퀴즈가 5개든 50개든, 시간이 부족하면 2~3문제만 빠르게 풀어보고 싶을 수 있습니다. 이걸 코드로 구현하려면 세 가지를 정확히 맞춰야 합니다.

1. 사용자에게 몇 문제를 풀지 물어본다.
2. 그 입력값이 "현재 등록된 퀴즈 개수"를 넘지 않도록 제한한다.
3. 실제로 그 수만큼만 출제하고, 점수 계산도 그 수를 기준으로 한다.

이 세 단계 중 하나라도 어긋나면 "3문제를 골랐는데 5문제가 나온다"거나 "2문제 중 1문제를 맞혔는데 점수가 20점으로 나온다" 같은 버그가 생깁니다. 이 프로젝트의 `play_quiz()` 메서드가 이 세 단계를 어떻게 연결하는지 순서대로 살펴보겠습니다.

### ask_int()로 입력받되, 범위는 항상 "지금" 계산한다

```python
total_quizzes = len(self.quizzes)
count = self.ask_int(
    f"\n풀 문제 수를 입력하세요 (1~{total_quizzes}): ",
    1,
    total_quizzes,
)
```

여기서 눈여겨봐야 할 부분은 `1`이나 `5` 같은 숫자를 코드에 직접 박아 넣지 않았다는 점입니다. `low=1`은 고정값이지만, `high`에 해당하는 상한선은 `total_quizzes`라는 변수, 즉 `len(self.quizzes)`를 그대로 넘깁니다. 이 한 줄 덕분에 퀴즈를 추가하거나 삭제해서 `self.quizzes`의 길이가 바뀌면, 다음에 `play_quiz()`를 실행할 때 `ask_int()`에 넘어가는 범위도 자동으로 따라 바뀝니다. 별도로 범위를 갱신하는 코드를 추가할 필요가 없습니다 — `len(self.quizzes)`를 호출하는 시점이 바로 "지금 이 순간의 퀴즈 개수"이기 때문입니다.

실제로 이 프로젝트에서 8-4(퀴즈 삭제) 기능을 시연하는 과정에서 이 동작이 그대로 확인되었습니다. 퀴즈를 하나 추가해 총 6개가 되었을 때는 안내 문구가 `풀 문제 수를 입력하세요 (1~6):`으로 바뀌었고, 이후 6번 퀴즈를 삭제해서 다시 5개로 돌아오자 문구도 `풀 문제 수를 입력하세요 (1~5):`로 다시 줄어들었습니다. 코드 어디에도 "삭제하면 범위를 5로 되돌려라" 같은 로직은 없습니다. `total_quizzes = len(self.quizzes)`가 매번 새로 계산되기 때문에 자연스럽게 따라온 결과입니다. 만약 이 값을 `__init__`에서 한 번만 계산해 두고 재사용했다면, 퀴즈를 추가하거나 삭제해도 입력 범위가 처음 상태로 굳어 있는 버그가 생겼을 것입니다.

### quizzes_to_play[:count] — 8-1과 맞물려 "무작위 부분집합"이 된다

문제 수를 입력받은 다음에는 그 수만큼만 잘라서 출제합니다.

```python
quizzes_to_play = self.quizzes[:]
random.shuffle(quizzes_to_play)
quizzes_to_play = quizzes_to_play[:count]
```

여기서 슬라이싱 `[:count]` 자체는 단순히 "리스트 앞에서부터 count개"를 가져오는 동작일 뿐입니다. 그런데 이 코드가 특별한 이유는 슬라이싱 대상이 `self.quizzes`의 원본 순서가 아니라, 바로 앞줄에서 `random.shuffle()`로 이미 섞어 놓은 복사본이라는 점입니다. 즉 8-2의 "문제 수 줄이기"는 8-1의 "무작위 섞기"와 항상 함께 동작합니다. 그 결과 "문제 수를 3개로 줄인다"는 것은 원래 등록 순서상 앞쪽 3문제를 고정으로 뽑는 게 아니라, 매번 실행할 때마다 다른 3문제가 무작위로 선택되는 것을 의미합니다. 두 기능이 각자 독립적으로 동작하는 게 아니라, 셔플 이후에 자르는 순서 덕분에 자연스럽게 결합되는 구조입니다.

### total = len(quizzes_to_play) — 점수 계산 분모를 다시 맞춘다

문제를 줄였다면 점수도 그 줄어든 수를 기준으로 계산되어야 합니다. 이 부분이 8-2 체크리스트의 마지막 항목("선택한 문제 수, 전체 퀴즈 수, 점수 계산 분모가 일치")입니다.

```python
total = len(quizzes_to_play)
...
score = round(earned_points / total * 100)
```

핵심은 `total`이 `len(self.quizzes)`(전체 등록된 퀴즈 수)가 아니라 `len(quizzes_to_play)`(실제로 이번에 출제된 문제 수)로 계산된다는 점입니다. 만약 실수로 `len(self.quizzes)`를 그대로 분모에 썼다면, 5문제 중 1문제만 골라 풀었을 때 1문제를 다 맞혀도 `1/5*100 = 20점`으로 나오는 잘못된 결과가 나왔을 것입니다.

실제 시연 로그에서 이 계산이 정확히 맞아떨어지는 것을 두 번 확인할 수 있었습니다. 먼저 `풀 문제 수를 입력하세요 (1~5): 1`로 1문제만 선택했을 때 결과는 `1문제 중 0문제 정답! (0점)`으로, 분모가 1로 정확히 표시되었습니다. 이후 퀴즈를 하나 추가해 총 6개가 된 상태에서 `풀 문제 수를 입력하세요 (1~6): 2`로 2문제를 선택했을 때는 `2문제 중 1문제 정답! (50점)`이 나왔습니다. 6개 중 2개를 뽑았지만 분모는 전체 개수인 6이 아니라 실제로 푼 2로 계산되어 `1/2*100 = 50`이 정확히 나온 것입니다.

### 흔한 실수

- 상한값을 `len(self.quizzes)`처럼 매번 계산하지 않고 변수에 캐싱해 두면, 퀴즈를 추가·삭제해도 입력 범위가 갱신되지 않는 문제가 생길 수 있습니다.
- 셔플하기 전에 슬라이싱부터 하면(`self.quizzes[:count]` 후 셔플), 무작위 부분집합이 아니라 "원본 순서 앞쪽 count개를 뽑은 뒤 그 안에서만 섞는" 것이 되어 버립니다. 전체 퀴즈 중 다양한 조합이 나오지 않고 항상 같은 앞부분 후보군에서만 골라지는 문제가 생깁니다.
- 점수 계산의 분모로 `len(self.quizzes)`를 그대로 쓰면, 문제 수를 줄여서 풀었을 때 점수가 실제보다 낮게 계산되는 버그가 생깁니다. 반드시 실제로 출제된 리스트의 길이(`len(quizzes_to_play)`)를 사용해야 합니다.

---

## 8-3. 힌트

퀴즈를 풀다가 막히면 힌트를 보고 싶어지는 것은 자연스러운 일입니다. 하지만 힌트를 공짜로 주면 문제 자체가 의미 없어지므로, "힌트를 볼 수는 있지만 그만큼 점수를 깎는다"는 규칙이 필요합니다. 이번 8-3에서는 이 규칙을 `Quiz` 클래스와 `play_quiz()` 양쪽에 걸쳐 구현합니다.

### Quiz에 hint 속성 추가하기

`quiz.py`의 `Quiz.__init__`은 이제 `hint`라는 네 번째 매개변수를 선택적으로 받습니다.

```python
def __init__(self, question, choices, answer, hint: str | None = None) -> None:
    ...
    if hint is not None and not isinstance(hint, str):
        raise TypeError("힌트는 문자열 또는 None이어야 합니다.")
    self.question = question
    self.choices = list(choices)
    self.answer = answer
    self.hint = hint
```

`hint: str | None = None`이라는 타입 힌트(type hint, 여기서 "힌트"라는 단어가 두 가지 뜻으로 겹쳐 나오는 점은 주의하세요 — 하나는 파이썬 타입 애너테이션, 하나는 이번 기능인 퀴즈 힌트입니다)는 "hint는 문자열이거나 아예 없어도(None) 된다"는 뜻입니다. 기본값이 `None`이므로 기존 코드에서 `Quiz("질문", ["A", "B", "C", "D"], 1)`처럼 힌트 없이 호출하던 곳은 전혀 수정할 필요가 없습니다. 대신 `if hint is not None and not isinstance(hint, str):` 검증으로 "None이 아닌데 문자열도 아닌" 값(숫자나 리스트 등)이 들어오면 즉시 `TypeError`를 던져, 잘못된 데이터가 조용히 저장되는 것을 막습니다. `get_default_quizzes()`의 기본 5문제에도 이제 실제 힌트 문장이 채워져 있는데, 예를 들어 스택 문제에는 "접시를 쌓아 올린 뒤 가장 위의 접시부터 꺼내는 상황을 떠올려 보세요."라는 힌트가 들어 있습니다.

### to_dict / from_dict와 storage.py의 마이그레이션 패턴

`to_dict()`는 `hint`를 항상 딕셔너리에 포함시킵니다.

```python
def to_dict(self):
    return {"question": self.question, "choices": list(self.choices), "answer": self.answer, "hint": self.hint}
```

반대로 `from_dict()`는 `data["hint"]`가 아니라 `data.get("hint")`를 씁니다.

```python
@classmethod
def from_dict(cls, data):
    return cls(
        question=data["question"], choices=data["choices"], answer=data["answer"],
        hint=data.get("hint"),  # 기존 state.json에 hint 키가 없어도 None으로 안전하게 복원
    )
```

이 차이가 핵심입니다. `data["hint"]`처럼 대괄호로 접근하면 키가 없을 때 `KeyError`가 나서, hint 기능이 생기기 전에 저장된 옛날 `state.json`(문제, 보기, 정답만 있고 hint 키 자체가 없는 파일)을 불러오는 순간 프로그램이 죽어버립니다. 반면 `data.get("hint")`는 키가 없으면 조용히 `None`을 돌려주므로, 옛날 데이터도 "힌트가 등록되지 않은 문제"로 자연스럽게 해석됩니다. 이 패턴은 처음 쓰는 것이 아닙니다. `storage.py`에서 `best_correct`·`best_total`을 불러올 때, 그리고 `history`를 불러올 때(`history = _parse_history(data.get("history", []))`) 이미 같은 `data.get(key, 기본값)` 방식으로 이전 Step의 state.json을 마이그레이션했습니다. hint도 정확히 같은 원리로, 스키마가 바뀌어도 옛 데이터를 깨뜨리지 않고 받아들이는 것입니다.

### 0을 입력해 힌트 보기

`play_quiz()`에서 정답을 입력받는 부분이 `while True` 루프로 바뀌었습니다.

```python
used_hint = False
while True:
    user_answer = self.ask_int("\n정답 입력 (1-4, 0: 힌트): ", 0, 4)
    if user_answer != 0:
        break

    if quiz.hint:
        print(f"💡 힌트: {quiz.hint}")
    else:
        print("💡 등록된 힌트가 없습니다.")

    if not used_hint:
        used_hint = True
        print("⚠️ 힌트 사용으로 이 문제는 맞혀도 0.5점만 인정됩니다.")
```

먼저 `ask_int`의 허용 범위가 기존 `(1, 4)`에서 `(0, 4)`로 넓어졌습니다. 0은 원래 보기 번호가 아니지만, "힌트를 보고 싶다"는 의사 표시로 0을 정답 입력 범위 안에 끼워 넣은 것입니다. 사용자가 0을 입력하면 `user_answer != 0` 조건이 거짓이 되어 `break`가 실행되지 않으므로, 루프가 끝나지 않고 다시 `while True`의 맨 위로 돌아가 같은 문제에 대해 다시 입력을 받습니다. 즉 0은 "답을 확정하지 않고 힌트만 확인한 뒤 같은 문제를 계속 풀겠다"는 신호입니다. 1~4를 입력해야만 `break`로 루프를 빠져나가 채점 단계로 넘어갑니다.

`quiz.hint`가 `None`인지 실제 문자열인지는 `if quiz.hint:`로 구분합니다. `None`은 거짓(falsy)이므로 힌트가 없는 문제라면 else 분기의 "💡 등록된 힌트가 없습니다."가 출력되고, 힌트 문자열이 있으면 그 내용이 그대로 출력됩니다.

`used_hint`는 `while` 루프 밖, `for` 루프 안에서 문제마다 `False`로 새로 선언되는 지역 변수입니다. 그래서 한 문제 안에서 0을 여러 번 눌러 힌트를 반복해서 봐도 `if not used_hint:` 조건 덕분에 "0.5점만 인정됩니다" 경고는 딱 한 번만 뜨고, `used_hint`는 그 문제가 끝날 때까지 `True`로 유지됩니다. 다음 문제로 넘어가면 다시 `False`로 초기화되어 힌트 사용 여부가 문제별로 독립적으로 관리됩니다.

### 점수 반영: earned_points와 :g 포맷

채점 단계에서는 정수 `correct` 대신 실수 `earned_points`가 실제 점수 계산에 쓰입니다.

```python
if quiz.is_correct(user_answer):
    correct += 1
    if used_hint:
        earned_points += 0.5
        print("✅ 정답입니다! (힌트 사용: 0.5점 획득)")
    else:
        earned_points += 1.0
        print("✅ 정답입니다! (1점 획득)")
```

`earned_points`는 `0.0`에서 시작해 힌트 없이 맞히면 `1.0`씩, 힌트를 쓰고 맞히면 `0.5`씩 늘어납니다. `correct`는 여전히 "몇 문제를 맞혔는가"를 세는 정수 카운터로 별도로 유지되고, 최종 점수는 `score = round(earned_points / total * 100)`처럼 `earned_points`를 기준으로 계산됩니다. 결과 출력에는 `f"{earned_points:g}"` 포맷이 쓰이는데, `:g`는 불필요한 소수점 0을 정리해 줍니다. 힌트를 한 번도 안 써서 `earned_points`가 `1.0`이면 `1`로, 절반짜리 점수가 섞여 `1.5`가 되면 `1.5` 그대로 보여 줍니다.

### 실제 실행 로그

사용자가 직접 추가한, 힌트 없이 등록한 퀴즈를 풀며 0을 입력했을 때의 실제 로그입니다.

```text
정답 입력 (1-4, 0: 힌트): 0
💡 등록된 힌트가 없습니다.
⚠️ 힌트 사용으로 이 문제는 맞혀도 0.5점만 인정됩니다.
```

이 문제는 사용자가 8-2에서 직접 추가한 퀴즈였고, 추가할 때 힌트를 입력하지 않았기 때문에 `quiz.hint`가 `None`으로 저장되어 있었습니다. 그래서 `if quiz.hint:` 분기가 아니라 else 분기가 실행되어 "등록된 힌트가 없습니다"가 출력된 것입니다. 힌트가 없어도 0을 누르면 감점 경고는 동일하게 뜬다는 점, 즉 "힌트 내용이 있든 없든 0을 눌러 힌트 확인을 시도한 행위 자체"가 감점 기준이라는 점을 이 로그가 보여 줍니다.

### 흔한 실수와 주의사항

`data["hint"]`처럼 대괄호로 직접 접근하면 옛 `state.json`을 불러올 때 `KeyError`가 나므로 반드시 `data.get("hint")`를 써야 합니다. 또한 `ask_int`의 범위를 `(0, 4)`로 넓히지 않고 그대로 `(1, 4)`에 0을 억지로 처리하려 하면 애초에 0을 입력할 수 없으므로 힌트 기능 자체가 동작하지 않습니다. `used_hint`를 `for` 루프 바깥(문제 전체에 걸쳐 한 번만 선언)에 두면 이전 문제에서 힌트를 썼다는 상태가 다음 문제까지 이어져 감점 로직이 뒤섞이므로, 반드시 문제마다 새로 초기화되어야 합니다. 마지막으로 힌트를 쓰지 않은 경우(1.0점씩 누적, `:g`로 정수처럼 표시)와 쓴 경우(0.5점 섞임, `:g`로 소수점까지 표시)를 각각 실행해 보며 `earned_points`와 최종 `score`가 의도대로 계산되는지 직접 확인하는 것이 이 기능을 검증하는 가장 확실한 방법입니다.

---

## 8-4. 퀴즈 삭제

### 메뉴가 5개에서 6개로 늘어날 때 반드시 함께 바꿔야 하는 것

퀴즈 삭제 기능은 단순히 새 메서드 하나를 추가하는 것으로 끝나지 않습니다. 메뉴 항목이 5개(풀기·추가·목록·점수·종료)에서 6개(풀기·추가·목록·점수·**삭제**·종료)로 늘어나면서, `show_menu()`와 `run()`도 함께 바뀌었습니다.

```python
def show_menu(self) -> None:
    ...
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 퀴즈 삭제")
    print("6. 종료")
    ...

def run(self) -> None:
    while True:
        self.show_menu()
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

여기서 눈여겨봐야 할 부분은 `ask_int("선택: ", 1, 6)`과 마지막 `else` 분기의 관계입니다. Step 2~4 문서에서 반복해서 짚었던 설계 원칙이 바로 "`ask_int`가 값의 범위를 이미 보장해 주기 때문에, `run()`의 마지막 `else`는 별도의 조건문 없이도 안전하게 '나머지 하나의 값'을 의미할 수 있다"는 것이었습니다. 메뉴가 5개였을 때는 `ask_int(..., 1, 5)`였고 `else`는 "5번(종료)"를 뜻했습니다. 이번에 메뉴가 6개로 늘어나면서 `ask_int`의 상한도 `5`에서 `6`으로 함께 바뀌었고, 그 결과 `else`가 이제는 "6번(종료)"를 의미하게 되었습니다. 만약 삭제 기능은 추가했는데 `ask_int`의 범위를 `1, 5`로 그대로 두었다면 사용자는 6번을 입력할 방법 자체가 없었을 것이고, 반대로 범위만 `1, 6`으로 늘리고 `elif choice == 5`를 추가하지 않았다면 5번을 눌러도 아무 일도 일어나지 않고 `else`(종료)로 빠져 버렸을 것입니다. 즉 "메뉴 항목 수 · `ask_int` 호출 범위 · `else`가 가리키는 마지막 번호" 세 가지는 항상 한 세트로 맞춰야 하며, 이번 8-4가 그 원칙이 실제 코드 변경으로 드러난 첫 사례입니다.

### ask_yes_no() — ask_int/ask_text와 같은 패턴, 다른 허용값

삭제 전 재확인을 위해 새로 추가된 `ask_yes_no()`는 지금까지 써 온 `ask_int()`, `ask_text()`와 똑같은 골격을 따릅니다.

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

`while True`로 감싸고 유효한 값이 나올 때까지 반복해서 `input()`을 받는 구조는 동일하되, 허용하는 값의 종류만 다릅니다. `ask_int`는 지정한 정수 범위 안의 숫자를, `ask_text`는 비어 있지 않은 문자열을 요구했다면, `ask_yes_no`는 `.strip().lower()`로 다듬은 뒤 오직 `"y"`와 `"n"` 두 값만 정답으로 인정합니다. "잘못된 입력이면 안내 메시지를 출력하고 다시 묻는다"는 이 반복 검증 패턴이 입력값의 종류가 달라져도 그대로 재사용된다는 점이 이 헬퍼의 핵심입니다.

### delete_quiz() 단계별로 읽기

```python
def delete_quiz(self) -> None:
    if not self.quizzes:
        print("\n⚠️ 삭제할 퀴즈가 없습니다.")
        return

    self.show_quiz_list()
    total = len(self.quizzes)
    target_number = self.ask_int(
        f"\n삭제할 퀴즈 번호를 선택하세요 (1~{total}): ", 1, total
    )
    target_index = target_number - 1
    target_quiz = self.quizzes[target_index]

    if not self.ask_yes_no(
        f"\n❓ [{target_number}] {target_quiz.question!r} 퀴즈를 삭제하시겠습니까? (y/n): "
    ):
        print("\n❌ 퀴즈 삭제가 취소되었습니다.")
        return

    del self.quizzes[target_index]
    if self.save_state():
        print(f"\n✅ [{target_number}]번 퀴즈가 삭제되었습니다.")
    else:
        print("\n⚠️ 퀴즈는 삭제되었지만 파일 저장에 실패했습니다.")
```

1. **빈 목록 가드**: `self.quizzes`가 비어 있으면 아예 진입하지 않고 곧바로 돌아갑니다. 지울 대상이 없는 상태에서 번호를 묻는 것 자체가 의미 없기 때문입니다.
2. **`show_quiz_list()` 재사용**: 삭제할 대상을 고르려면 먼저 무엇이 있는지 보여줘야 하는데, 이를 위해 새 출력 로직을 만들지 않고 4장에서 이미 만들어 둔 `show_quiz_list()`를 그대로 호출합니다. 같은 목적(퀴즈 목록 보여주기)의 코드를 두 번 작성하지 않는 재사용의 예입니다.
3. **`ask_int`로 번호 검증**: `1~total` 범위를 지정해 호출하므로, 존재하지 않는 번호를 입력할 방법 자체가 차단됩니다.
4. **`target_index = target_number - 1`**: 사용자에게 보여주는 번호는 1부터 시작하지만 파이썬 리스트의 인덱스는 0부터 시작합니다. 이 1-based → 0-based 변환은 Step 1의 퀴즈 모델을 다룰 때부터 이 시리즈 전반에서 계속 등장해 온 패턴입니다.
5. **`{target_quiz.question!r}`**: 문자열 포맷에서 `!r`은 `repr()`을 적용하라는 지시자입니다. 일반 `str()` 변환과 달리 `!r`은 문자열 양쪽에 따옴표를 그대로 남기므로, 출력 결과가 `'1'`처럼 나와 "지금 지우려는 값이 정확히 무엇인지"를 눈으로 바로 확인할 수 있게 해 줍니다.
6. **`ask_yes_no`로 재확인**: `n`을 입력하면 아무것도 지우지 않고 함수가 종료됩니다.
7. **`del self.quizzes[target_index]`**: 승인된 경우에만 실제로 리스트에서 항목을 제거합니다.
8. **`save_state()` 즉시 호출**: 삭제 직후 바로 저장해, 메모리상의 `self.quizzes`와 `state.json` 파일 내용이 어긋나지 않도록 합니다.

### 실제 실행 로그로 확인한 삭제 반영

```
삭제할 퀴즈 번호를 선택하세요 (1~6): 6
❓ [6] '1' 퀴즈를 삭제하시겠습니까? (y/n): y
✅ [6]번 퀴즈가 삭제되었습니다.
```

이 로그는 6개짜리 목록에서 6번(직접 추가했던 `'1'`이라는 질문의 퀴즈)을 골라 `y`로 확인한 뒤 삭제된 상황입니다. 이어서 메뉴로 돌아와 다시 문제 수를 물으면 `"풀 문제 수를 입력하세요 (1~5): "`처럼 범위가 6에서 5로 줄어들어 있습니다. 이는 삭제가 메모리와 파일 양쪽에 실제로 반영되어, 재실행 후에도 삭제한 퀴즈가 되돌아오지 않는다는 체크리스트 마지막 항목을 그대로 뒷받침하는 근거입니다.

### del vs remove() — 흔히 헷갈리는 부분

`del self.quizzes[target_index]`의 `del`은 리스트의 **인덱스 위치**를 지정해 그 자리의 항목을 제거하는 파이썬 문법입니다. 반면 리스트에는 `list.remove(value)`라는 메서드도 있는데, 이는 인덱스가 아니라 **값**을 기준으로 찾아 제거합니다. 만약 같은 값이 리스트 안에 여러 번 들어 있다면 `remove()`는 앞에서부터 처음 발견한 항목 하나만 지우고 나머지는 그대로 둡니다. 이번 `delete_quiz()`에서는 사용자가 화면에 표시된 번호로 대상을 고르고, 그 번호를 인덱스로 변환해 정확한 위치를 지정하고 있으므로 `del self.quizzes[target_index]`처럼 인덱스 기반으로 지우는 것이 맞습니다. 만약 실수로 `self.quizzes.remove(target_quiz)`처럼 값 기반 삭제를 썼다면, 질문 내용이 우연히 같은 퀴즈가 두 개 이상 등록되어 있을 때 사용자가 고른 것과 다른(먼저 나온) 항목이 지워질 위험이 있습니다.

---

## 8-5. 점수 히스토리

### `self.history`와 `self.best_*`는 서로 다른 역할을 맡습니다

`QuizGame`은 지금까지 `best_score`, `best_correct`, `best_total` 세 값만으로 "잘한 기록"을 표현해 왔습니다. 이번 Step에서는 여기에 `history: list[dict[str, Any]] = []`라는 상태를 하나 더 추가했는데, 이 둘은 겉보기엔 비슷해 보여도 완전히 다른 일을 합니다.

| 상태 | 담는 것 | 개수 |
|---|---|---|
| `best_score` / `best_correct` / `best_total` | 지금까지 게임 중 **가장 점수가 높았던 단 한 번**의 요약값 | 항상 최대 1세트 |
| `history` | **풀었던 모든 게임**을 하나도 빠짐없이 남긴 로그 | 게임을 할 때마다 계속 늘어남 |

`best_*`는 "역대 최고 기록판"이고, `history`는 "매 게임을 빠짐없이 적는 일지"입니다. 이 차이는 `play_quiz()`의 코드 위치에도 그대로 드러납니다.

```python
self.history.append(
    {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": total,
        "correct": correct,
        "score": score,
    }
)

has_previous_record = self.best_total > 0 or self.best_score > 0
if not has_previous_record or score > self.best_score:
    self.best_score = score
    self.best_correct = correct
    self.best_total = total
```

`self.history.append(...)`는 `if not has_previous_record or score > self.best_score:` 조건문 **바깥**에 있습니다. 즉 이번 게임 점수가 0점이든 100점이든, 최고 기록을 갱신하든 못 하든 관계없이 **매 게임 종료 후 무조건 한 번씩 실행**됩니다. 반면 `best_score`/`best_correct`/`best_total`의 갱신은 조건문 **안**에서만, 즉 "이전 기록이 없거나 이번 점수가 최고 기록보다 높을 때"만 일어납니다. 이 위치 차이가 곧 "요약값 vs 전체 로그"라는 역할 차이를 코드로 보여주는 부분입니다.

### 타임스탬프를 문자열로 남기는 이유

`datetime.now().strftime("%Y-%m-%d %H:%M:%S")`는 현재 시각을 `"2026-08-05 07:28:57"` 같은 문자열로 바꿔줍니다. 굳이 문자열로 변환하는 이유는 JSON 포맷 자체에 날짜/시간을 나타내는 전용 타입이 없기 때문입니다. JSON이 표현할 수 있는 값은 문자열, 숫자, 불리언, null, 배열, 객체뿐이므로, `datetime` 객체를 그대로 저장하려 하면 `json.dump()`가 직렬화 오류를 냅니다. 사람이 읽기도 쉽고 정렬도 자연스러운 `"YYYY-MM-DD HH:MM:SS"` 문자열로 남기는 것이 가장 단순한 해법입니다.

### storage.py는 기록 하나하나를 꼼꼼히 검증합니다

`storage.py`의 `_parse_history()`는 `history` 리스트의 각 항목을 다음 순서로 검사합니다.

```python
timestamp = record["timestamp"]
if not isinstance(timestamp, str) or not timestamp.strip():
    raise TypeError(f"history의 {number}번째 timestamp는 비어 있지 않은 문자열이어야 합니다.")
total = _require_nonnegative_int(record["total"], f"history[{number}].total")
if total == 0:
    raise ValueError(f"history의 {number}번째 total은 1 이상이어야 합니다.")
correct = _require_nonnegative_int(record["correct"], f"history[{number}].correct")
if correct > total:
    raise ValueError(f"history의 {number}번째 correct는 total보다 클 수 없습니다.")
score = _require_nonnegative_int(record["score"], f"history[{number}].score")
if score > 100:
    raise ValueError(f"history의 {number}번째 score는 100 이하여야 합니다.")
```

`timestamp`는 빈 문자열이 아닌 문자열이어야 하고, `total`은 1 이상, `correct`는 `total` 이하, `score`는 100 이하여야 합니다. 특히 `total == 0`을 허용하지 않는 이유를 눈여겨볼 만합니다. `play_quiz()`는 애초에 `total = len(quizzes_to_play)`가 1 이상일 때만 실행되고 기록을 남기므로, 문제를 하나도 풀지 않은 게임은 처음부터 `history`에 들어올 이유가 없습니다. `total == 0`인 기록이 파일에 있다면 그것은 정상적인 게임 결과가 아니라 손상되었거나 조작된 데이터라고 보는 것이 맞고, `_parse_history()`는 이를 즉시 오류로 걸러냅니다.

### 옛 state.json도 자연스럽게 불러옵니다

`_parse_state()`는 `history = _parse_history(data.get("history", []))`로 `history`를 읽어옵니다. `history` 키가 아예 없던 옛 `state.json` 파일이라도 `data.get("history", [])`는 예외 없이 빈 리스트를 돌려주므로, 히스토리가 없던 시절의 저장 파일도 "빈 기록에서 시작"하는 상태로 자연스럽게 이어집니다. 이는 Step 5에서 `best_correct`/`best_total`이 없는 옛 파일을 마이그레이션했던 것과 같은 패턴으로, 이 프로젝트에서 "새 필드를 추가할 때는 `data.get(키, 기본값)`으로 옛 파일과의 호환을 보장한다"는 원칙이 반복적으로 쓰이고 있음을 보여줍니다.

### `show_score()`의 최근 5회 조회 한 줄 뜯어보기

```python
for number, record in enumerate(reversed(self.history[-5:]), start=1):
```

이 줄은 안쪽부터 바깥쪽으로 읽으면 이해하기 쉽습니다.

1. `self.history[-5:]` — 리스트 끝에서부터 최대 5개를 잘라냅니다. 기록이 5개 미만이어도 오류 없이 있는 만큼만 가져옵니다.
2. `reversed(...)` — 순서를 뒤집습니다. `append()`로 쌓인 리스트는 가장 최근 게임이 맨 끝에 있으므로, 뒤집으면 가장 최근 기록이 맨 앞으로 옵니다.
3. `enumerate(..., start=1)` — 화면에 1번부터 번호를 매깁니다.

실제 실행 로그가 이 순서를 그대로 확인해 줍니다. 사용자가 1문제(0점) → 2문제(100점) 순서로 두 번 플레이한 뒤 점수 확인 화면에는 다음과 같이 표시되었습니다.

```
[최근 게임 기록: 최근 5회 / 전체 N회]
1. [2026-08-05 07:28:57] 2문제 | 2문제 정답 | 100점
2. [2026-08-05 07:28:48] 1문제 | 0문제 정답 | 0점
```

더 나중에 플레이한 2문제 100점 게임이 1번으로, 더 먼저 플레이한 1문제 0점 게임이 2번으로 표시되어, `self.history[-5:]` → `reversed(...)` → `enumerate(..., start=1)`이 실제로 "최신 기록이 위로 오는" 순서로 동작함을 확인할 수 있습니다. 흔한 실수는 `reversed()`를 빼먹고 `self.history[-5:]`만 순서대로 출력하는 것인데, 이렇게 하면 가장 오래된 기록이 1번으로 표시되어 "최근" 기록을 보여준다는 화면 문구와 어긋나게 됩니다.

---

## 정리 — 확인하고 넘어가면 좋은 것들

Step 7에서 실제로 구현·검증까지 끝난 부분과, 아직 남은 부분을 구분하면 다음과 같습니다.

**이미 끝난 것 (코드·체크리스트·실행 결과 모두 확인됨)**
- 랜덤 출제: `self.quizzes[:]`로 얕은 복사를 만들고 `random.shuffle()`로 출제용 사본만 섞어, 저장·목록 조회용 원본 순서는 그대로 유지함(재실행 로그로 순서가 바뀌는 것 확인)
- 문제 수 선택: `ask_int()`의 상한을 `len(self.quizzes)`로 매번 다시 계산해 퀴즈 추가·삭제에 자동으로 따라가고, 점수 분모도 실제 출제 수(`len(quizzes_to_play)`)로 정확히 맞춰짐
- 힌트: `Quiz.hint`가 선택적 필드로 추가되고, 0 입력으로 힌트를 보면 0.5점 감점이 실제 결과에 반영됨
- 퀴즈 삭제: 메뉴가 1~6으로 확장되고, 번호 검증·`y/n` 재확인·`del`·즉시 저장까지 전부 구현되어 재실행 후에도 삭제가 유지됨
- 점수 히스토리: `best_*`(최고 한 번)와 `history`(모든 게임 기록)의 역할이 명확히 분리되고, 최근 5회를 최신순으로 보여줌

**다음에 정리하면 좋은 것**
- [ ] `main.py`, `quiz.py`, `storage.py`, `README.md`, `docs/learning_checklist.md`의 미커밋 변경 사항을 의미 단위로 나누어 커밋하고 원격에 push하기
- [ ] 이번 보너스 기능들의 실행 화면(메뉴 1~6, 힌트 사용, 삭제, 히스토리 조회)을 스크린샷으로 남기기

이 항목들을 정리한 뒤에는 [`docs/learning_checklist.md`](../learning_checklist.md)의 다음 단계로 넘어갈 수 있습니다.

## 참고 문서

- [Step 0 학습 노트](step0_dev_environment_git_init.md) — 개발 환경 설정과 Git 저장소 초기화
- [Step 1 학습 노트](step1_quiz_model.md) — Quiz 모델과 자료구조 기본 데이터
- [Step 2 학습 노트](step2_quizgame_menu.md) — QuizGame, 메뉴, 공통 입력과 안전 종료
- [Step 3 학습 노트](step3_play_quiz_branch.md) — feat/play-quiz 브랜치와 퀴즈 풀기
- [Step 4 학습 노트](step4_add_list_score.md) — 퀴즈 추가, 목록 조회, 점수 확인
- [Step 5 학습 노트](step5_state_persistence.md) — state.json 영속성과 4대 복구 경로
- [Step 6 학습 노트](step6_clone_pull.md) — clone과 pull 실습
- [학습 체크리스트](../learning_checklist.md) — 이 문서의 원본 체크리스트
- [학습 가이드](../learning_guide.md) — 단계별 실습 코드와 커밋 힌트
- [프로젝트 README](../../README.md) — 실제로 작성된 프로젝트 설명 문서
