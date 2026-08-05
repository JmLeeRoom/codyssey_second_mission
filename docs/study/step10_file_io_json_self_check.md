# 10-3. 파일 입출력과 JSON — 자가 점검 학습 노트

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "10. 학습 목표와 자가 점검" 아래 "10-3. 파일 입출력과 JSON" 6개 항목을 학습 자료로 재구성한 것입니다. [10-1. Python 기초](python_basics_self_check.md), [10-2. 클래스와 객체(OOP)](oop_self_check.md)에 이어지는 자가 점검 시리즈의 세 번째 문서입니다.
>
> 모든 예시는 실제 `storage.py` 코드에서 그대로 발췌했습니다. `load_state()`의 실제 예외 처리 절은 `FileNotFoundError` → `json.JSONDecodeError` → `UnicodeDecodeError` → `(KeyError, TypeError, ValueError)` → `OSError` 정확히 5갈래이며, 이 중 `UnicodeDecodeError`를 빠뜨리지 않고 다뤘습니다.

## 목차

- 파일을 안전하게 열고 닫기, 예외를 구체적으로 잡기
- JSON 구조와 ensure_ascii
- 예외를 좁게 잡아야 하는 이유

---

## 파일을 안전하게 열고 닫기, 예외를 구체적으로 잡기

### with open(...)이 파일을 열고 작업 뒤 자동으로 닫는 과정을 설명할 수 있다.

파일을 다루는 코드에는 항상 "연다 → 읽거나 쓴다 → 닫는다"라는 세 단계가 있다. 문제는 세 번째 단계인 "닫는다"가 사람이 직접 챙겨야 하는 일이라는 점이다. `with` 문은 바로 이 마지막 단계를 파이썬이 대신 챙겨주게 만드는 문법이다. `with 무언가.open(...) as file:` 블록 안으로 들어가는 순간 파일이 열리고, 그 블록을 벗어나는 순간 — 정상적으로 코드를 다 실행하고 빠져나가든, 블록 안에서 예외가 터져서 빠져나가든 — 파이썬이 자동으로 파일을 닫아준다. "정상 종료든 예외든 상관없이 닫아준다"는 부분이 핵심이다. 사람이 매번 `close()`를 손으로 호출할 필요가 없을 뿐 아니라, `close()`를 깜빡할 걱정 자체를 할 필요가 없어진다.

이 프로젝트의 `storage.py`에는 실제로 이 패턴이 두 곳에 쓰여 있다. 첫 번째는 `load_state()`에서 저장된 파일을 읽는 부분이다.

```python
with path.open("r", encoding="utf-8") as file:
    data = json.load(file)
```

두 번째는 `save_state()`에서 현재 상태를 파일에 쓰는 부분이다.

```python
with Path(state_file).open("w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
```

두 코드 모두 `storage.py` 전체 어디를 봐도 `file.close()`를 명시적으로 호출하는 줄이 없다. 그런데도 파일이 안전하게 닫히는 이유는, `with` 블록을 벗어나는 순간 파이썬이 알아서 닫기 때문이다.

여기서 "블록 안에서 예외가 나도 닫힌다"는 부분을 이 프로젝트의 실제 흐름으로 확인해 보자. `load_state()`의 `with` 블록 안에서는 `json.load(file)`이 실행되는데, 만약 `state.json`의 JSON 문법이 깨져 있다면 이 줄에서 `json.JSONDecodeError`가 발생한다. 이 예외는 `with` 블록 **안에서** 일어난 예외다. 이때도 파이썬은 "예외를 먼저 바깥으로 던지고 파일은 그냥 열어둔 채 방치"하지 않는다. 파일을 먼저 안전하게 닫은 다음에, 그 예외를 `with` 블록 바깥으로 계속 전달한다. 그래서 이 예외가 결국 `load_state()`의 `except json.JSONDecodeError as error:` 절에 도착했을 때는, `state.json` 파일은 이미 닫혀 있는 상태다. `_backup_corrupted_file(path)`가 바로 이어서 `state_file.replace(backup_file)`로 파일 이름을 바꿔야 하는데, 만약 그 파일이 아직 열린 채로 남아 있었다면 이 이름 변경 작업 자체가 방해받을 수 있었을 것이다. `with` 덕분에 이런 걱정 없이 곧바로 백업 작업으로 넘어갈 수 있다.

이제 `with` 없이 직접 여닫는 경우와 비교해 보자. 아래는 이 프로젝트의 실제 코드가 아니라, `with`를 안 쓰고 흉내만 낸 잘못된 예시다.

```python
# ❌ 잘못된 예시(실제 프로젝트 코드 아님) — with 없이 열고, close()를 깜빡했다고 가정
file = open(state_file, "r", encoding="utf-8")
data = json.load(file)  # 여기서 JSONDecodeError가 나면?
file.close()            # 이 줄까지 도달하지 못하고 함수가 예외로 빠져나간다
```

`json.load(file)`에서 예외가 발생하면 그 아래에 있는 `file.close()`는 아예 실행되지 못한 채 함수가 빠져나가 버린다. 이렇게 파일을 닫지 않고 방치하면 크게 두 가지 문제가 생길 수 있다. 하나는 그 파일을 다른 프로세스나 다른 코드가 건드리기 어려워지는 것이다. 예를 들어 이 프로젝트의 `_backup_corrupted_file()`이 `state_file.replace(backup_file)`로 파일 이름을 바꾸려 할 때, 같은 파일이 어딘가에서 열린 채로 남아 있으면 이름 변경이나 삭제가 막힐 수 있다. 다른 하나는 프로그램이 오래 실행될수록 문제가 누적된다는 점이다. 열어놓고 안 닫은 파일 핸들이 하나씩 쌓이면, 운영체제가 프로세스 하나에 허용하는 "동시에 열 수 있는 파일 개수" 한도에 결국 닿게 되고, 그 이후로는 새 파일을 여는 것 자체가 실패하기 시작한다. `with`를 쓰면 이런 누적이 애초에 일어나지 않는다 — 블록을 벗어나는 즉시 그 파일 핸들은 반납되기 때문이다.

**TL;DR: `with path.open(...) as file:`로 열면 그 블록을 정상적으로 빠져나가든 블록 안에서 예외(예: `json.JSONDecodeError`)가 나서 빠져나가든 파이썬이 파일을 자동으로 닫아 주지만, `file = open(...)`으로 열고 `close()`를 깜빡하면 다른 코드가 그 파일에 접근하기 어려워지거나 열린 파일 핸들이 계속 쌓이는 문제가 생긴다.**

### try/except로 예상 가능한 예외를 구체적으로 처리해야 하는 이유를 설명할 수 있다.

`state.json`을 읽어 들이는 과정에는 망가질 수 있는 지점이 여러 곳 있고, 각각 망가지는 이유가 다르다. 이 프로젝트의 `_parse_state()`를 보면 그 차이가 코드 수준에서 드러난다.

```python
def _parse_state(data: Any) -> State:
    if not isinstance(data, dict):
        raise ValueError("state.json의 최상위 값은 객체(dict)여야 합니다.")
    raw_quizzes = data["quizzes"]
    if not isinstance(raw_quizzes, list):
        raise TypeError("state.json의 quizzes는 리스트여야 합니다.")
    quizzes = [Quiz.from_dict(raw_quiz) for raw_quiz in raw_quizzes]
    best_score = _require_nonnegative_int(data.get("best_score", 0), "best_score")
    if best_score > 100:
        raise ValueError("state.json의 best_score는 100 이하여야 합니다.")
    ...
```

`data["quizzes"]`처럼 대괄호로 직접 키를 꺼내는 부분은, 만약 `state.json`에 `"quizzes"`라는 키 자체가 없다면 `KeyError`를 낸다. 그 값이 리스트가 아니라면 `isinstance` 검사에 걸려 `TypeError`를 낸다. 값은 있고 타입도 맞는데 범위가 잘못됐다면(`best_score`가 100을 넘는 경우 등) `ValueError`를 낸다. 이 셋은 서로 다른 종류의 손상을 나타내도록 **의도적으로** 다르게 설계돼 있다.

`load_state()`는 이 차이를 그대로 받아서 각각 다른 `except` 절로 나눠 잡는다. 실제 코드에서 이 함수의 예외 처리 절은 정확히 5개이고, 순서는 다음과 같다.

```python
except FileNotFoundError:
    ...
except json.JSONDecodeError as error:
    ...
except UnicodeDecodeError as error:
    ...
except (KeyError, TypeError, ValueError) as error:
    ...
except OSError as error:
    ...
```

이렇게 다섯 갈래로 나눠 잡기 때문에 가능한 일들을 하나씩 짚어보자. `FileNotFoundError`는 아예 경고 메시지를 출력하지 않는다. 첫 실행이라 파일이 없는 것은 오류가 아니라 정상적인 상황이므로, 곧바로 `_restore_default_state(path)`를 불러 조용히 기본 데이터로 시작한다. 반면 `json.JSONDecodeError`, `UnicodeDecodeError`, `(KeyError, TypeError, ValueError)` 이 세 갈래는 공통적으로 `_backup_corrupted_file(path)`를 먼저 호출해 손상된 파일을 `state.json.bak`으로 옮긴 뒤 복구하지만, 사용자에게 보여주는 메시지는 각각 다르다.

```python
print(f"⚠️ 데이터 파일의 JSON 형식이 손상되었습니다: {error}")   # JSONDecodeError
print(f"⚠️ 데이터 파일을 UTF-8로 읽을 수 없습니다: {error}")      # UnicodeDecodeError
print(f"⚠️ 데이터 파일의 구조가 올바르지 않습니다: {error}")      # KeyError/TypeError/ValueError
```

그리고 마지막 `OSError`는 앞의 셋과 아예 다른 조치를 취한다. 권한이 없거나 장치에 문제가 있어서 파일을 읽는 것 자체가 실패한 상황이므로, 백업을 시도하지도 않고 파일도 건드리지 않은 채 `_default_state()`로 메모리에서만 복구한다. 접근조차 안 되는 파일을 상대로 `replace()`를 시도해 봤자 그 역시 실패할 가능성이 높기 때문에, 여기서는 아예 파일 쪽을 건드리지 않는 게 더 안전한 선택이다.

이제 이걸 하나로 뭉뚱그렸다면 어떻게 됐을지 생각해 보자. 아래는 실제 코드가 아니라, 다섯 갈래를 하나로 합친 잘못된 가상의 예시다.

```python
# ❌ 잘못된 예시(실제 프로젝트 코드 아님) — 5개 except를 하나로 뭉뚱그렸다고 가정
try:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    state = _parse_state(data)
    ...
except Exception as error:
    print(f"⚠️ 오류가 발생했습니다: {error}")
    _backup_corrupted_file(path)  # OSError(권한 문제)여도 무조건 백업을 시도한다
    return _select_state_values(_restore_default_state(path), ...)
```

이렇게 하나로 합치면 당장 두 가지를 할 수 없게 된다. 첫째, 사용자에게 "JSON 문법이 깨졌다"와 "필수 키가 없다"와 "UTF-8로 못 읽는다"를 구분해서 알려줄 방법이 사라진다. 세 경우 모두 `{error}` 하나로 뭉뚱그려 찍히는 메시지만 보고는, 사용자가 `state.json`을 텍스트 에디터로 열어서 무엇을 어떻게 고쳐야 할지 가늠하기 어렵다. 둘째, 손상 원인에 따라 다른 조치를 취할 수 없게 된다. 실제 코드에서는 `OSError`일 때만 백업을 건너뛰는데(파일에 접근 자체가 안 되니 백업도 실패할 가능성이 높기 때문), 하나로 합친 버전에서는 권한 문제로 못 읽은 경우까지 무작정 `_backup_corrupted_file(path)`를 호출하게 되어, 원래는 건드리지 않았어야 할 파일에 불필요한 `replace()` 시도를 하게 된다. 예상 가능한 예외를 구체적으로 잡는다는 것은 결국 "무슨 일이 일어났는지 정확히 알아야, 그에 맞는 정확한 대응을 할 수 있다"는 원칙을 코드로 옮긴 것이다.

이 원칙은 `main.py`의 `ask_int()`에서도 똑같이 확인할 수 있다.

```python
def ask_int(self, prompt: str, low: int, high: int) -> int:
    """``low``~``high`` 범위의 정수를 입력받을 때까지 재시도한다.

    ``ValueError``만 처리하여 ``KeyboardInterrupt``와 ``EOFError``는
    상위 실행 흐름에서 안전하게 처리할 수 있도록 그대로 전달한다.
    """
    while True:
        raw = input(prompt).strip()
        ...
        try:
            value = int(raw)
        except ValueError:
            print("⚠️ 숫자를 입력하세요.")
            continue
```

`int(raw)`는 사용자가 숫자가 아닌 문자열을 입력했을 때 `ValueError`를 낸다는 것이 충분히 예상 가능하므로, 딱 그 예외만 좁게 잡아서 "숫자를 입력하세요"라는 안내와 함께 재시도시킨다. 만약 여기서 `except ValueError:` 대신 아무 종류나 다 잡는 `except:`를 썼다면 어떻게 될까. 사용자가 `Ctrl+C`를 눌러서 발생시키는 `KeyboardInterrupt`나 입력 스트림이 끊겨서 발생하는 `EOFError`까지 이 좁은 `except` 안에서 조용히 삼켜지고, 다시 `input(prompt)`를 호출하며 루프를 돈다. 그런데 이 두 예외는 이 프로젝트의 `main()`이 `_save_before_exit(game)`으로 안전하게 저장하고 종료하기 위해 일부러 잡아서 처리하도록 설계해 둔 것들이다.

```python
try:
    game = QuizGame()
    game.run()
except KeyboardInterrupt:
    print("\n⚠️ 사용자에 의해 프로그램이 중단되었습니다. (Ctrl+C)")
    if game is not None:
        _save_before_exit(game)
except EOFError:
    print("\n⚠️ 입력 스트림이 종료되었습니다. (EOF)")
    if game is not None:
        _save_before_exit(game)
```

`ask_int()`가 `ValueError`만 좁게 잡고 그 외의 모든 예외(`KeyboardInterrupt`, `EOFError` 포함)는 자기가 처리하지 않고 그대로 위로 흘려보내기 때문에, 이 예외들이 결국 `main()`의 `except KeyboardInterrupt:`와 `except EOFError:`까지 살아서 도달할 수 있다. 만약 `ask_int()` 안에서 뭉뚱그린 `except:`를 썼다면, `Ctrl+C`를 눌러도 그저 다시 입력을 받는 루프로 삼켜져 버릴 뿐 `main()`의 안전 종료 로직까지 도달하지 못했을 것이다. 예상 가능한 예외를 구체적으로 잡아야 하는 이유는 결국 하나로 모인다 — 잡을 예외의 범위를 좁게 정해 두어야, 그 범위 밖의 신호(다른 계층에서 처리하기로 되어 있는 예외)를 실수로 가로채지 않는다.

**TL;DR: `_parse_state()`는 `data["quizzes"]` 키가 없으면 `KeyError`, 타입이 틀리면 `TypeError`, 범위를 벗어나면 `ValueError`를 내도록 설계돼 있고, `load_state()`는 이를 포함해 정확히 5개(`FileNotFoundError` → `json.JSONDecodeError` → `UnicodeDecodeError` → `(KeyError, TypeError, ValueError)` → `OSError`)의 `except`로 나눠 잡아 서로 다른 메시지와 서로 다른 조치(예: `OSError`만 백업을 건너뜀)를 취한다 — 이걸 하나로 뭉뚱그리면 원인 구분도, 원인별 대응도 불가능해지며, `ask_int()`가 `ValueError`만 좁게 잡아 `KeyboardInterrupt`/`EOFError`를 `main()`의 안전 종료 로직까지 그대로 흘려보내는 것도 같은 원리다.**

---

## JSON 구조와 ensure_ascii

### JSON의 구조와 일반 텍스트보다 퀴즈·점수 데이터를 저장하기 좋은 이유를 설명할 수 있다

이 프로젝트의 `state.json`은 겉보기엔 그냥 텍스트 파일이지만, 그 안의 값들은 절대 평평(flat)하지 않다. `_parse_state()`가 실제로 읽어 들이는 최상위 구조를 보면 이렇다.

```json
{
  "quizzes": [
    {
      "question": "스택(Stack)의 주요 자료 처리 방식은 무엇인가요?",
      "choices": ["FIFO (선입선출)", "LIFO (후입선출)", "LILO (후입후출)", "무작위 접근"],
      "answer": 2
    }
  ],
  "best_score": 100,
  "best_correct": 5,
  "best_total": 5,
  "history": [
    {"timestamp": "2026-08-05T10:00:00", "total": 5, "correct": 5, "score": 100}
  ]
}
```

여기엔 세 겹의 계층이 겹쳐 있다. 가장 바깥은 "게임 전체 상태"를 나타내는 객체(`{}`) 하나, 그 안에 "퀴즈 목록"과 "게임 기록 목록"이라는 배열(`[]`) 두 개, 그리고 배열 각 항목이 다시 "문제 하나"를 나타내는 객체다. 문제 객체 안에는 또 "선택지 4개"라는 배열이 들어 있다. 즉 `{}`는 "이름 붙은 값들의 묶음"(question이라는 이름에는 문자열, answer라는 이름에는 정수), `[]`는 "순서가 있는 값들의 나열"(선택지 4개, 게임 기록 여러 회)을 표현한다. 이 프로젝트가 다루는 데이터가 원래부터 이런 모양—"문제 하나"는 여러 필드를 가진 객체이고, "선택지"는 그 안에 들어간 배열이고, "퀴즈 전체"는 그런 객체들의 배열—이기 때문에 JSON의 `{}`/`[]` 조합이 별다른 변환 없이 그대로 들어맞는다.

이걸 만약 평범한 한 줄짜리 텍스트로 저장했다면 어떻게 될지 생각해 보면 이 적합성이 더 잘 보인다. 예를 들어 파이프(`|`)로 구분한 텍스트 줄로 흉내 내 본다면 이렇게 될 것이다.

```
스택(Stack)의 주요 자료 처리 방식은 무엇인가요?|FIFO (선입선출)|LIFO (후입선출)|LILO (후입후출)|무작위 접근|2
```

당장 두 가지 문제가 생긴다. 첫째, 선택지 안에 구분자로 쓴 `|` 문자가 실제로 들어가면(예를 들어 "A|B 중 하나"라는 선택지) 몇 번째 칸이 문제 문장이고 몇 번째가 선택지인지 파싱이 깨진다. 둘째, `hint`처럼 있을 수도 없을 수도 있는 선택적 필드를 넣으려면 "6번째 칸이 있으면 힌트, 없으면 힌트 없음"이라는 직접 만든 규칙이 필요하고, 그 규칙을 읽는 쪽과 쓰는 쪽이 항상 정확히 같은 버전으로 맞아야 한다. 필드 순서를 하나만 밀려 써도 프로그램은 조용히 잘못된 값을 정답 번호로 읽어버릴 수 있다. JSON은 이런 파싱 규칙을 직접 설계할 필요가 없다—`data["question"]`, `data["choices"]`, `data.get("hint")`처럼 이름으로 값을 꺼내면 되고, 필드가 없으면 그냥 없는 것으로(파이썬에서는 `KeyError`나 `.get()`의 기본값으로) 명확하게 드러난다. 실제로 `_parse_state()`는 `raw_quizzes = data["quizzes"]`처럼 이름으로 직접 접근하고, `history`는 `data.get("history", [])`로 없으면 빈 리스트로 처리하는 식으로 이 장점을 그대로 쓰고 있다.

**TL;DR: JSON의 객체(`{}`)와 배열(`[]`)은 "문제 하나(객체)에 선택지 4개(배열)가 들어 있고, 그런 문제들이 다시 배열로 모여 있는" 이 프로젝트의 실제 데이터 모양과 그대로 맞아떨어져서, 직접 파싱 규칙을 설계하지 않고도 계층 구조와 가변 필드(힌트 등)를 안전하게 표현할 수 있다.**

### ensure_ascii=False를 빼면 한글 데이터가 어떻게 보이는지, 프로그램 동작과 사람 가독성의 차이를 설명할 수 있다

`json.dumps()`(그리고 `json.dump()`)의 `ensure_ascii` 옵션은 기본값이 `True`다. 이 프로젝트의 실제 문제 문장으로 직접 확인해 보면 차이가 뚜렷하다.

```python
>>> import json
>>> d = {"question": "스택(Stack)의 주요 자료 처리 방식은 무엇인가요?", "answer": 2}
>>> print(json.dumps(d, ensure_ascii=True, indent=2))   # 기본값
{
  "question": "\uc2a4\ud0dd(Stack)\uc758 \uc8fc\uc694 \uc790\ub8cc \ucc98\ub9ac \ubc29\uc2dd\uc740 \ubb34\uc5c7\uc778\uac00\uc694?",
  "answer": 2
}
>>> print(json.dumps(d, ensure_ascii=False, indent=2))  # 이 프로젝트가 실제로 쓰는 옵션
{
  "question": "스택(Stack)의 주요 자료 처리 방식은 무엇인가요?",
  "answer": 2
}
```

코드 한 줄, 정확히는 `ensure_ascii` 값 하나만 바뀌었을 뿐인데 파일에 실제로 쓰이는 바이트는 완전히 다른 모습이 된다. `ensure_ascii=True`(기본값)일 때는 아스키 범위 밖의 모든 문자를 `\uXXXX` 형태의 유니코드 이스케이프 시퀀스로 바꿔 써버린다. `ensure_ascii=False`일 때는 한글 문자를 그대로, 사람이 읽을 수 있는 형태로 쓴다.

여기서 중요한 건, 이 둘이 "다른 데이터"가 아니라는 점이다. `\uc2a4\ud0dd`는 "스택"이라는 두 글자를 나타내는 또 다른 표기법일 뿐이다. 그래서 어느 쪽으로 저장했든 `json.load()`로 다시 읽으면 파이썬 프로그램 입장에서는 완전히 동일한 문자열 `"스택(Stack)의 주요 자료 처리 방식은 무엇인가요?"`로 복원된다. `quiz.question == "스택..."` 같은 비교, 화면에 `print()`로 출력하는 동작, `Quiz.from_dict()`가 이 값을 받아 객체를 만드는 과정—프로그램이 하는 모든 일에 이 옵션은 아무런 차이를 만들지 않는다. 즉 **프로그램 동작에는 차이가 없다.**

차이가 실감나는 순간은 딱 하나, 사람이 텍스트 에디터나 `cat`으로 `state.json` 파일을 직접 열어볼 때다. `ensure_ascii=True`로 저장된 파일을 열면 문제 문장이 온통 `\uXXXX`의 나열로 보여서, 어떤 퀴즈가 들어 있는지 파일만 봐서는 알아볼 수 없다. 커밋 diff를 봐도 무슨 내용이 바뀌었는지 짐작하기 어렵다. `ensure_ascii=False`로 저장된 파일은 열자마자 "스택(Stack)의 주요 자료 처리 방식은 무엇인가요?"라는 문장이 그대로 보인다. **사람 가독성**의 차이는 오직 여기, 파일을 직접 열어보는 순간에만 있다.

이 프로젝트의 `save_state()`는 실제로 다음과 같이 파일을 쓴다.

```python
with Path(state_file).open("w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
```

그리고 `load_state()`의 정상 읽기 경로는 다음과 같이 대응한다.

```python
with path.open("r", encoding="utf-8") as file:
    data = json.load(file)
```

세 옵션은 각각 서로 다른 역할을 맡고 있으며, 하나로 뭉뚱그려 이해하면 안 된다.

| 옵션 | 역할 | 빠지면 생기는 문제 |
|---|---|---|
| `encoding="utf-8"` | 파일을 열 때 바이트를 어떤 문자 인코딩으로 해석·기록할지 지정 | 운영체제 기본 인코딩이 UTF-8이 아닌 환경에서 한글이 깨지거나, 읽을 때 `UnicodeDecodeError`가 날 수 있다 |
| `ensure_ascii=False` | 아스키 범위 밖 문자(한글 등)를 이스케이프할지 그대로 쓸지 결정 | 기본값(`True`)이면 한글이 전부 `\uXXXX`로 바뀌어 저장되어, 프로그램은 똑같이 동작해도 사람이 파일을 직접 열었을 때 알아볼 수 없다 |
| `indent=2` | 출력 JSON을 2칸 들여쓰기로 줄바꿈해 정렬 | 빠지면(또는 `indent=None`) 모든 내용이 한 줄로 뭉쳐 저장되어, 파일을 열어 구조를 눈으로 훑어보기 어렵다 |

세 옵션 모두 "파일을 열었을 때"의 문제를 다룬다는 공통점이 있지만 층위가 다르다. `encoding`은 바이트 수준(어떤 바이트로 저장·해석할지), `ensure_ascii`는 문자 표현 수준(한글을 이스케이프할지), `indent`는 레이아웃 수준(사람이 훑어보기 좋게 줄바꿈할지)의 결정이다. 이 셋이 함께 있어야 `state.json`이 "프로그램도 정확히 읽고, 사람도 열어서 바로 검토할 수 있는" 파일이 된다. 실제로 `save_state()` 코드의 주석도 "UTF-8과 ensure_ascii=False로 한글을 그대로 보존하고, indent=2로 사람이 state.json 내용을 쉽게 검토할 수 있게 한다"고 이 세 역할을 명시적으로 구분해 설명하고 있다.

**TL;DR: `ensure_ascii=False`가 빠지면 한글이 `\uXXXX` 이스케이프로 저장되지만 `json.load()`로 복원하면 프로그램 입장에서는 완전히 같은 문자열이 되므로—프로그램 동작에는 차이가 없고, 사람이 파일을 직접 열어볼 때의 가독성만 달라진다.**

---

## 예외를 좁게 잡아야 하는 이유

### except ValueError: 대신 맨몸 except:를 썼을 때 숨겨질 수 있는 오류를 설명할 수 있다

`storage.py`의 `load_state()`를 다시 보면, 이 함수는 예외를 딱 하나로 뭉뚱그리지 않는다. 실제 코드에는 순서대로 다섯 개의 `except` 절이 나란히 있다.

```python
except FileNotFoundError:
    ...
except json.JSONDecodeError as error:
    ...
except UnicodeDecodeError as error:
    ...
except (KeyError, TypeError, ValueError) as error:
    ...
except OSError as error:
    ...
```

파일이 없는 경우, JSON 문법이 깨진 경우, 인코딩이 UTF-8이 아닌 경우, `_parse_state()`가 데이터 구조를 검증하다 실패한 경우, 그리고 권한 등으로 아예 읽기 자체가 실패한 경우—이 다섯 가지는 원인도 다르고 사용자에게 보여줄 메시지도 다르다. 코드를 작성한 사람은 "여기서 발생할 수 있는 오류는 이 다섯 종류뿐이고, 각각 이렇게 대응하겠다"라고 미리 선언해 둔 셈이다.

**비유하자면** 이건 병원 응급실의 분류(트리아지)와 같다. 의사가 환자를 볼 때 "아픈 사람"이라고만 뭉뚱그리지 않고 골절, 화상, 감염처럼 원인별로 나눠서 각기 다른 처치를 준비하는 것처럼, `load_state()`도 문제의 종류마다 다른 "처방"(백업 여부, 출력 메시지, 복구 방식)을 준비해 둔 것이다. 만약 응급실 접수대에서 모든 환자를 "아픈 사람"이라는 팻말 하나로만 분류한다면, 화상 환자에게 깁스를 하는 식의 엉뚱한 처치가 나올 수도 있고, 정말 위급한 환자가 뒤로 밀릴 수도 있다.

이제 이걸 맨몸 `except:`(또는 `except Exception:`) 하나로 바꾸면 어떤 일이 벌어지는지 살펴보자.

```python
# 잘못된 예시 — 실제 코드가 아니라 대조를 위한 가정
try:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    state = _parse_state(data)
    ...
except:  # 무슨 예외든 다 여기로 들어온다
    print("⚠️ 뭔가 문제가 생겼습니다.")
    return _select_state_values(_default_state(), include_details, include_history)
```

이 프로젝트 맥락에서 가장 직접적인 위험은 **KeyboardInterrupt**와 **EOFError**다. `main.py`의 `main()`은 이 두 예외를 특별히 잡아서 안전 종료 메시지를 보여주도록 설계되어 있다.

```python
try:
    game = QuizGame()
    game.run()
except KeyboardInterrupt:
    print("\n⚠️ 사용자에 의해 프로그램이 중단되었습니다. (Ctrl+C)")
    if game is not None:
        _save_before_exit(game)
except EOFError:
    print("\n⚠️ 입력 스트림이 종료되었습니다. (EOF)")
    if game is not None:
        _save_before_exit(game)
```

그런데 `KeyboardInterrupt`는 파이썬 예외 계층에서 `Exception`이 아니라 `BaseException`을 직접 상속한다. 콜론만 있는 맨몸 `except:`는 클래스를 지정하지 않으므로 `BaseException` 계열까지 전부, 즉 `KeyboardInterrupt`도 그대로 걸려든다. 만약 `load_state()` 안에서 데이터를 읽는 도중 사용자가 Ctrl+C를 눌렀는데 이 코드가 맨몸 `except:`였다면, 그 신호는 `load_state()` 안에서 조용히 삼켜지고 "기본 데이터로 복구합니다" 같은 무관한 메시지만 찍힌 채 프로그램은 아무 일 없다는 듯 계속 실행된다. `main()`까지 신호가 전달되지 않으니 "Ctrl+C로 중단되었습니다"라는 정상적인 안내도 뜨지 않고, 사용자는 왜 종료가 안 되는지 알 수 없는 이상한 상태에 빠진다. (참고로 `except Exception:`으로 바꿨다면 `KeyboardInterrupt`는 통과시키지만, `Exception`의 하위 클래스인 `EOFError`는 여전히 삼켜버린다—그러니 "그냥 조금 더 좁히면 되지 않냐"는 접근도 완전한 해법은 아니다.)

같은 원리가 `main.py`의 `ask_int()`에도 그대로 적용된다. 실제 코드는 `int(raw)` 변환에서 발생할 수 있는 `ValueError`만 정확히 잡는다.

```python
try:
    value = int(raw)
except ValueError:
    print("⚠️ 숫자를 입력하세요.")
    continue
```

이 함수의 docstring에는 "`ValueError`만 처리하여 `KeyboardInterrupt`와 `EOFError`는 상위 실행 흐름에서 안전하게 처리할 수 있도록 그대로 전달한다"라고 명시되어 있다. 만약 여기서도 맨몸 `except:`를 썼다면 사용자가 숫자를 입력하는 도중 Ctrl+C를 눌러도 "숫자를 입력하세요"라는 엉뚱한 메시지만 반복되고 프로그램을 끝낼 방법이 사라졌을 것이다.

두 번째 문제는 **진짜 버그를 숨긴다**는 점이다. 예를 들어 개발자가 `_parse_state()` 안에서 오타로 `quizzse` 같은 존재하지 않는 변수를 참조했다면 `NameError`가, 존재하지 않는 메서드를 호출했다면 `AttributeError`가 발생한다. 이런 예외는 "예상한 이상 상황"이 아니라 "코드 자체의 결함"이다. 지정된 다섯 개의 `except` 절 어디에도 걸리지 않으므로 이런 예외는 그대로 위로 전파되어 개발자가 즉시 알아차리고 고칠 수 있다. 하지만 맨몸 `except:`가 있었다면 이런 진짜 버그마저 "⚠️ 데이터 파일의 구조가 올바르지 않습니다" 같은 무관한 메시지와 함께 조용히 기본 데이터로 덮이고 넘어간다. 프로그램은 겉으로는 멀쩡히 동작하는 것처럼 보이지만, 실제로는 코드에 명백한 오류가 있어도 아무도 눈치채지 못하는 상태가 된다.

**TL;DR: 맨몸 `except:`는 예상한 문제(JSON 손상 등)뿐 아니라 사용자의 Ctrl+C(`KeyboardInterrupt`)와 개발자의 오타로 인한 진짜 버그(`AttributeError`, `NameError`)까지 전부 삼켜버려서, 안전 종료도 안 되고 버그도 숨겨진다—그래서 `load_state()`는 정확히 다섯 개의 구체적인 예외 타입만 잡는다.**

### 파일 부재와 파일 손상을 서로 다른 복구 경로로 처리해야 하는 이유를 설명할 수 있다

`load_state()`를 자세히 보면 "파일이 아예 없는 상황"과 "파일은 있는데 내용이 망가진 상황"을 완전히 다르게 처리한다.

파일이 없을 때(`FileNotFoundError`)는 경고 메시지를 전혀 출력하지 않는다.

```python
except FileNotFoundError:
    # 첫 실행은 오류가 아니라 기본 상태 파일을 만드는 정상 흐름이다.
    return _select_state_values(
        _restore_default_state(path), include_details, include_history
    )
```

반면 파일 내용이 망가져 있을 때(`JSONDecodeError`, `UnicodeDecodeError`, `(KeyError, TypeError, ValueError)`)는 셋 다 공통적으로 먼저 기존 파일을 백업한 뒤 경고 메시지를 출력한다.

```python
except json.JSONDecodeError as error:
    # JSON 문법이 깨진 파일은 보관할 수 있으면 백업한 뒤 다시 만든다.
    _backup_corrupted_file(path)
    print(f"⚠️ 데이터 파일의 JSON 형식이 손상되었습니다: {error}")
    print("🔧 기본 퀴즈 데이터로 복구합니다.")
    return _select_state_values(
        _restore_default_state(path), include_details, include_history
    )
```

**비유하자면** 이건 "이사 온 새집에 가구가 하나도 없는 것"과 "원래 있던 가구가 부서져 있는 것"의 차이다. 새집에 가구가 없는 건 당연한 일이라 놀랄 필요가 없다—그냥 새로 채우면 된다. 하지만 원래 있던 가구가 부서져 있다면, 뭔가 잘못됐다는 신호이므로 사진을 찍어 증거를 남기고("백업"), 무슨 일이 있었는지 알려야("경고 메시지") 한다. 프로그램을 처음 실행하는 사용자에게 `state.json`이 없는 것은 지극히 정상적인 상황이고, 반대로 어제까지 잘 저장되던 파일이 갑자기 JSON 문법 오류를 일으킨다면 그건 정말 뭔가 비정상적인 일(디스크 오류, 수동 편집 실수 등)이 벌어졌다는 신호다.

만약 이 두 상황을 하나로 뭉쳐서 처리했다면 두 가지 구체적인 문제가 생겼을 것이다.

첫째, 정상적인 첫 실행마다 사용자를 놀라게 했을 것이다. 이 프로젝트를 처음 내려받아 실행하는 사람은 아직 `state.json`이 없는 게 당연한데, 만약 `FileNotFoundError`도 손상 처리 경로로 합쳐졌다면 시작하자마자 "⚠️ 데이터 파일이 손상되었습니다"라는 무서운 경고가 뜬다. 아무 문제도 없는데 사용자는 "내가 뭘 잘못했나?"하고 불안해하며, 심지어 존재하지도 않았던 파일을 `.bak`으로 "백업"하려는 시도까지 벌어졌을 수 있다.

둘째, 반대로 손상 경로를 파일 부재 경로처럼 조용히 처리했다면, 진짜로 파일이 손상됐을 때 사용자는 아무것도 알 수 없게 된다. 예를 들어 `state.json`이 텍스트 편집기 실수로 중간에 깨졌는데도 프로그램이 아무 말 없이 기본 데이터로 조용히 시작해 버린다면, 사용자는 자신의 퀴즈 기록과 최고 점수가 사라졌다는 사실도, 원본이 `state.json.bak`으로 보존되어 있어서 복구할 수 있다는 사실도 전혀 알 방법이 없다. `_backup_corrupted_file(path)` 호출과 경고 출력이야말로 "데이터를 잃어버릴 뻔했지만 원본은 안전하게 보관해 두었다"는 유일한 단서인데, 그게 사라지는 것이다.

참고로 `OSError`(권한 문제 등으로 읽기 자체가 실패하는 경우)는 앞의 세 손상 상황과도 또 다르게 처리된다. 백업 시도조차 하지 않고 `_default_state()`로 메모리에서만 복구한다.

```python
except OSError as error:
    # 권한·장치 등 읽기 실패 시에는 파일을 덮어쓰지 않고 메모리에서만 복구한다.
    print(f"⚠️ 데이터 파일을 읽을 수 없습니다: {error}")
    print("🔧 기본 퀴즈 데이터로 복구합니다.")
    return _select_state_values(_default_state(), include_details, include_history)
```

이건 파일에 접근조차 못 하는 상황에서 백업을 시도하면 그 시도마저 같은 이유로 실패할 가능성이 높기 때문이다. 이렇게 네 가지 상황(부재, JSON 손상, 인코딩 손상, 구조 오류, 접근 실패)이 각자 다른 원인 메시지와 다른 복구 절차를 갖는 것은 우연이 아니라, "무엇이 문제였는지"와 "그래서 어떻게 복구했는지"를 사용자에게 정확히 전달하려는 의도적인 설계다.

**TL;DR: 파일이 "없는 것"은 정상(조용히 기본값으로 시작)이고, 파일이 "있는데 망가진 것"은 비정상(백업 후 경고)이므로, 이 둘을 하나로 합치면 정상 상황에 헛경고가 뜨거나 진짜 손상 상황이 조용히 묻혀 복구 단서(백업 파일)를 잃게 된다.**

---

## 참고 문서

- [10-1. Python 기초](python_basics_self_check.md)
- [10-2. 클래스와 객체(OOP)](oop_self_check.md)
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
