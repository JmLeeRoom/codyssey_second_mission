# Step 5 학습 노트 — state.json 영속성과 4대 복구 경로

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "6. Step 5 — state.json 영속성과 4대 복구 경로" 체크리스트를 바탕으로, 저장·복구 로직이 왜 지금과 같은 모습으로 구현됐는지 풀어 쓴 학습 자료입니다. [Step 0](step0_dev_environment_git_init.md) → [Step 1](step1_quiz_model.md) → [Step 2](step2_quizgame_menu.md) → [Step 3](step3_play_quiz_branch.md) → [Step 4](step4_add_list_score.md)에 이어지는 시리즈의 여섯 번째 문서입니다.
>
> 이 문서는 실제 `storage.py`·`main.py` 코드와, 이 저장소에서 직접 실행해 확인한 명령 결과·터미널 로그를 근거로 작성했습니다. 이번 Step에서 가장 깊이 다루는 내용은 `json.JSONDecodeError`와 `UnicodeDecodeError`가 둘 다 `ValueError`의 자손 클래스라서 `except` 절의 순서 자체가 복구 메시지의 정확성을 좌우한다는 점입니다. 커밋 메시지에 남은 오타 하나까지도 숨기지 않고 그대로 짚습니다.

## 목차

- 6-1. 저장 위치와 상태 스키마
- 6-2. save_state
- 6-3. load_state와 복구
- 6-4. 호출 지점과 재시작 검증
- 6-5. Step 5 Git 체크포인트

---

## 6-1. 저장 위치와 상태 스키마

### STATE_FILE 한 줄을 뜯어보기

`storage.py` 맨 위에는 이런 코드가 있습니다.

```python
import json
from pathlib import Path
...
STATE_FILE = Path(__file__).resolve().parent / "state.json"
```

`json`은 파이썬 딕셔너리를 텍스트 파일로 저장하고 다시 읽어오는 표준 모듈이고, `pathlib.Path`는 파일 경로를 문자열이 아니라 객체로 다뤄 운영체제(윈도우/리눅스/맥)에 상관없이 안전하게 경로를 조립해 주는 도구입니다. 이 둘을 가져온 다음, `STATE_FILE`이라는 경로 하나를 딱 한 번 계산해 두고 프로그램 전체가 이 경로만 사용하도록 만든 것이 이번 섹션의 핵심입니다.

이 한 줄은 세 단계로 순서대로 실행됩니다.

1. `__file__` — 지금 이 코드가 들어 있는 파이썬 파일, 즉 `storage.py` 자신의 경로를 담고 있는 특수 변수입니다. 사용자가 어떤 명령으로 실행했는지에 따라 절대 경로일 수도, 상대 경로일 수도 있습니다.
2. `.resolve()` — `__file__`이 상대 경로거나 `..` 같은 표기, 혹은 심볼릭 링크를 포함하고 있어도 이를 모두 풀어서 완전한 절대 경로로 정규화합니다. 즉 "어디서 실행했든" 결과가 항상 같은 하나의 실제 위치를 가리키게 만드는 단계입니다.
3. `.parent` — 정규화된 경로에서 파일 이름(`storage.py`)을 떼어내고 그 파일이 들어 있는 **디렉터리**만 남깁니다.

마지막으로 그 디렉터리에 `/ "state.json"`을 이어 붙여, "`storage.py`가 실제로 위치한 폴더 안의 `state.json`"이라는 하나의 고정된 경로를 만들어 냅니다.

### 왜 open("state.json")처럼 상대 경로를 쓰면 안 되는가

만약 `STATE_FILE`을 쓰지 않고 그냥 `open("state.json")`이라고 썼다면, 이 상대 경로는 파이썬 파일이 어디 있는지가 아니라 **사용자가 `python` 명령을 실행한 시점의 현재 작업 디렉터리(cwd)**를 기준으로 해석됩니다. cwd는 코드와 무관하게 사용자가 터미널에서 `cd`로 어느 폴더에 들어가 있느냐에 따라 매번 달라지는 값입니다.

이 프로젝트에서 실제로 이를 확인한 테스트가 있습니다. 프로젝트 상위 폴더로 이동한 뒤 `python second-project/main.py`처럼 하위 경로를 지정해 실행했을 때 결과는 다음과 같았습니다.

```
✅ 저장된 데이터 로드 완료! (퀴즈: 5개, 최고 점수: 0점)
```

만약 코드가 `open("state.json")`처럼 상대 경로를 썼다면, cwd가 프로젝트 상위 폴더이므로 파이썬은 상위 폴더에서 `state.json`을 찾다가 없으면 **상위 폴더에 새로운 `state.json`을 만들어 버렸을 것**입니다. 그러면 원래 프로젝트 루트에 있던 데이터와는 완전히 다른, 엉뚱한 위치의 파일이 하나 더 생겨 데이터가 흩어지는 문제가 생깁니다. 하지만 실제 코드는 `Path(__file__).resolve().parent`를 기준으로 삼기 때문에, 실행 시점의 cwd가 어디든 상관없이 항상 `storage.py`가 실제로 놓여 있는 프로젝트 루트의 `state.json`만을 정확히 다시 읽습니다(이 시점에 0점이 나온 것은 cwd 문제가 아니라, 바로 앞서 진행한 UTF-8 손상 테스트가 파일을 기본값으로 이미 리셋해 두었기 때문입니다 — 6-3에서 다시 다룹니다). 실제로 `ls`로 확인해 보면 `state.json`은 언제나 `main.py`, `storage.py`와 같은 프로젝트 루트 폴더에 생성되어 있습니다.

### 저장되는 4개의 키

`save_state()`가 실제로 파일에 기록하는 딕셔너리는 다음 네 개의 키로 구성됩니다.

```python
data = {
    "quizzes": quiz_data,
    "best_score": best_score,
    "best_correct": best_correct,
    "best_total": best_total,
}
```

사용자가 `python3 -m json.tool --no-ensure-ascii state.json`으로 실제 파일을 열어 확인한 결과도 정확히 이 구조와 일치합니다.

```json
{
    "quizzes": [ ... 5개 문제 ... ],
    "best_score": 100,
    "best_correct": 5,
    "best_total": 5
}
```

`quizzes`는 퀴즈 목록 자체를 담고, `best_score`는 지금까지의 최고 점수(0~100)만 간단히 기록합니다. 여기에 더해 "몇 문제 중 몇 문제를 맞혀서" 그 점수가 나왔는지 상세히 남기고 싶다면 `best_correct`(맞힌 개수)와 `best_total`(전체 문제 수)을 함께 저장합니다. `quizzes` 배열의 각 항목은 `question`(문제 텍스트), `choices`(보기 목록), `answer`(정답 번호)를 가진 JSON 객체 형태를 지켜야 하며, 이 구조는 `Quiz` 클래스의 `to_dict()`/`from_dict()`와 맞물려 있습니다(자세한 검증 로직은 6-2에서 다룹니다).

### 흔한 실수와 주의사항

- 코드·README·체크리스트에서 키 이름을 다르게 적어 놓으면(`bestScore`처럼 표기를 바꾸는 등) 실제 저장 파일과 문서가 어긋나므로, 이 네 키(`quizzes`, `best_score`, `best_correct`, `best_total`)의 이름과 자료형(정수/리스트)을 문서 전체에서 그대로 유지해야 합니다.
- `STATE_FILE`을 함수 인자의 기본값(`state_file: Path | str = STATE_FILE`)으로 넘겨 테스트나 백업 시에는 다른 경로를 지정할 수 있게 열어 두었지만, 실제 실행에서는 항상 이 기본값이 프로젝트 루트를 가리킨다는 점은 변하지 않습니다.
- `Path(__file__)`은 반드시 실제 `.py` 파일 안에서만 의미가 있습니다. 대화형 인터프리터(REPL)에서 직접 입력하면 `__file__`이 정의되어 있지 않아 오류가 나므로, 이 계산은 스크립트 파일 안에서 쓰는 것을 전제로 합니다.

---

## 6-2. save_state

### 왜 quiz.to_dict()가 필요한가 — "직접 넣으면 TypeError"

`save_state()`는 현재 메모리에 있는 퀴즈 목록(`quizzes`)과 점수 정보를 `state.json` 파일에 기록하는 함수입니다. 이때 가장 먼저 나오는 코드가 이 한 줄입니다.

```python
quiz_data = [quiz.to_dict() for quiz in quizzes]
```

`json.dump()`는 파이썬의 기본 자료형(`dict`, `list`, `str`, `int`, `float`, `bool`, `None`)만 JSON으로 바꿀 줄 압니다. `Quiz`는 우리가 직접 정의한 커스텀 클래스이기 때문에, `json`이 그 안에 어떤 속성(`question`, `choices`, `answer` 등)이 있는지 알지 못합니다. 그래서 만약 `quiz_data` 변환 단계를 생략하고 바로 다음처럼 썼다면

```python
json.dump(quizzes, file, ensure_ascii=False, indent=2)  # quizzes는 Quiz 객체 리스트
```

`TypeError: Object of type Quiz is not JSON serializable`가 발생하며 프로그램이 즉시 죽습니다. `to_dict()`는 바로 이 문제를 해결하기 위해 `Quiz` 객체 각각을 `{"question": ..., "choices": [...], "answer": ...}` 같은 순수 `dict`로 변환해 주는 메서드입니다. `json.dump()` 입장에서는 더 이상 낯선 `Quiz` 객체가 아니라 익숙한 `dict`의 리스트를 받으므로 문제없이 직렬화할 수 있습니다. 실제 `storage.py`에서도 이 변환된 `quiz_data`를 다른 점수 필드들과 함께 하나의 `data` 딕셔너리로 묶은 뒤에야 파일에 씁니다.

```python
quiz_data = [quiz.to_dict() for quiz in quizzes]
data = {
    "quizzes": quiz_data,
    "best_score": best_score,
    "best_correct": best_correct,
    "best_total": best_total,
}

try:
    with Path(state_file).open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
except OSError as error:
    print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
    print("💡 프로그램은 계속 실행됩니다. 파일 저장 상태를 확인해 주세요.")
    return False

return True
```

### encoding="utf-8" 과 ensure_ascii=False — 서로 다른 두 가지 문제를 각각 담당

이 두 옵션은 이름이 비슷해 보이지만 실제로 관여하는 층이 완전히 다릅니다.

- `encoding="utf-8"`은 `open()` 쪽 옵션으로, **"이 파일을 디스크에 어떤 바이트 규칙으로 쓸 것인가"**를 정합니다. 운영체제마다(특히 Windows) 기본 인코딩이 UTF-8이 아닐 수 있는데, 이를 명시하지 않으면 같은 파일을 다른 환경에서 열었을 때 한글이 깨질 수 있습니다. `encoding="utf-8"`을 명시하면 어떤 OS에서 실행하든 항상 같은 바이트로 저장·복원됩니다.
- `ensure_ascii=False`는 `json.dump()` 쪽 옵션으로, **"문자열 안의 비-ASCII 문자(한글 등)를 `\uXXXX` 이스케이프 형태로 바꿀지, 원문 그대로 쓸지"**를 정합니다. 기본값(`True`)으로 두면 "스택"이라는 문자열이 파일 안에서 `"\uc2a4\ud0dd"`처럼 저장되어, 사람이 파일을 직접 열어봐도 내용을 알아볼 수 없습니다.

즉 `encoding`은 "바이트를 어떻게 쓸까"의 문제이고 `ensure_ascii`는 "그 문자를 이스케이프할까 말까"의 문제입니다. 둘 중 하나만 신경 써서는 사람이 읽기 좋은 한글 JSON 파일을 만들 수 없고, 이 프로젝트에서는 둘을 짝으로 지정해 `state.json`이 실제 한글 텍스트를 그대로 담도록 했습니다.

### "이스케이프되어 보인다"는 착시 — json.tool의 기본 동작일 뿐

실제로 이 프로젝트의 `state.json`을 확인해 보면, `python3 -m json.tool state.json`(옵션 없이)로 열었을 때는 한글이 `\uXXXX` 형태의 이스케이프로 보입니다. 반면 `python3 -m json.tool --no-ensure-ascii state.json`으로 열면 아래처럼 원문 한글이 그대로 보입니다.

```json
{
    "quizzes": [ ... 5개 문제 ... ],
    "best_score": 100,
    "best_correct": 5,
    "best_total": 5
}
```

이 차이만 보면 마치 저장 자체가 잘못된 것처럼 오해하기 쉽지만, 실제 원인은 파일이 아니라 `json.tool`이라는 조회용 CLI 도구에 있습니다. `save_state()`는 이미 `ensure_ascii=False`로 파일을 저장했으므로 `state.json` 안에는 처음부터 한글이 원문 그대로 들어 있습니다. 그런데 `json.tool`은 파일을 읽어 파이썬 객체로 파싱한 뒤, 그것을 다시 예쁘게(pretty-print) 출력할 때 **자기 자신의 기본 옵션**으로 `ensure_ascii=True`를 사용합니다. 그래서 옵션 없이 실행하면 "다시 이스케이프된 모습"으로 보이는 것뿐입니다. 정리하면, 저장은 이미 올바르게 되어 있고 문제처럼 보였던 것은 조회 도구의 기본 동작 차이였을 뿐입니다.

### except OSError — 저장 실패가 프로그램을 죽이지 않게 하기

파일 쓰기는 디스크 공간 부족, 권한 문제, 경로 접근 불가 등으로 실패할 수 있습니다. 이런 경우 파이썬은 `OSError`(또는 그 하위 클래스)를 발생시킵니다. `save_state()`는 파일을 여는 `with open(...)` 구문과 `json.dump()` 호출을 통째로 `try` 블록 안에 두고, `except OSError`로 이를 감쌉니다.

```python
except OSError as error:
    print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
    print("💡 프로그램은 계속 실행됩니다. 파일 저장 상태를 확인해 주세요.")
    return False
```

이 처리가 없다면 저장 실패 시 예외가 함수 밖으로 그대로 전파되어 Traceback과 함께 프로그램 전체가 비정상 종료됩니다. 사용자는 방금까지 진행하던 퀴즈 풀이 화면을 잃고 터미널에 낯선 에러 메시지만 보게 됩니다. 반면 `except OSError`로 잡아 안내 메시지를 출력하고 `False`를 반환하면, 호출한 쪽(`main.py`)은 저장이 실패했다는 사실만 알고 나머지 메뉴 루프를 계속 이어갈 수 있습니다. 즉 이 한 줄의 예외 처리가 "저장 기능 한 부분의 실패"와 "프로그램 전체의 중단"을 분리해 주는 역할을 합니다.

**흔한 실수**: `except Exception`처럼 지나치게 넓게 잡으면 저장 로직 안에 진짜 버그(예: `best_correct > best_total`처럼 이 함수 앞부분에서 의도적으로 발생시키는 `ValueError`)까지 조용히 삼켜버려 디버깅이 어려워집니다. 이 프로젝트는 그런 검증 오류들은 `save_state()` 앞부분에서 별도로 `raise`하고, `except OSError`는 오직 "파일 쓰기 자체의 실패"만 좁게 담당하도록 나눠 두었습니다. 이렇게 예외의 범위를 필요한 만큼만 좁게 잡는 습관은 다음 절(6-3)에서 다룰 `load_state()`의 예외 순서 문제와도 이어집니다.

---

## 6-3. load_state와 복구

### 예외 계층 구조부터 확인하기

`load_state()`의 except 절이 왜 지금 순서로 쌓여 있는지 이해하려면, 먼저 파이썬 표준 라이브러리의 예외 계층 구조를 직접 확인해 보는 것이 가장 확실합니다. 다음을 인터프리터에서 그대로 실행해 봅니다.

```python
>>> import json
>>> issubclass(json.JSONDecodeError, ValueError)
True
>>> issubclass(UnicodeDecodeError, ValueError)
True
```

`json.JSONDecodeError`와 `UnicodeDecodeError`는 둘 다 `ValueError`의 자손 클래스입니다. 이 사실 하나가 `storage.py`의 except 절 순서를 결정합니다.

파이썬은 `try` 블록에서 예외가 발생하면 `except` 절을 **위에서부터 순서대로** 검사해서, 발생한 예외가 해당 절이 잡는 타입(또는 그 부모 타입)과 일치하는 **첫 번째 절 하나만** 실행합니다. 나머지 절은 검사조차 하지 않습니다. 그런데 `(KeyError, TypeError, ValueError)`를 묶어 처리하는 절이 있고, `JSONDecodeError`나 `UnicodeDecodeError`는 이 `ValueError` 안에 포함되는 관계이므로, 만약 이 튜플 절이 `JSONDecodeError`나 `UnicodeDecodeError` 절보다 **위에** 있었다면 어떤 일이 벌어졌을지 생각해 보아야 합니다. JSON이 깨져서 `json.JSONDecodeError`가 발생해도, 파이썬은 그 예외가 `ValueError`의 자손이라는 이유만으로 위쪽의 일반적인 `except (KeyError, TypeError, ValueError)` 절에 먼저 걸려버립니다. 그러면 실제로는 "JSON 문법이 깨졌다"는 상황인데도 화면에는 "데이터 파일의 구조가 올바르지 않습니다"라는, 원인과 다른 메시지가 출력됩니다. 사용자 입장에서는 파일을 열어봐도 딱히 구조가 이상해 보이지 않으니 오히려 더 혼란스러운 상황이 됩니다.

그래서 실제 `storage.py`는 다음 순서를 지킵니다.

```
FileNotFoundError → json.JSONDecodeError → UnicodeDecodeError → (KeyError, TypeError, ValueError) → OSError
```

더 구체적인(자식) 예외를 먼저 검사하고, 더 일반적인(부모) 예외를 나중에 배치하는 것이 원칙입니다. `OSError`가 맨 마지막에 오는 이유도 같습니다. `FileNotFoundError` 역시 `OSError`의 자손이므로, `OSError` 절이 먼저 있었다면 파일이 없는 정상적인 첫 실행 상황까지 "읽기 실패"로 잘못 처리될 뻔했습니다.

### 손상 테스트 로그와 except 절 대응표

사용자가 실제로 세 가지 손상 파일을 만들어 재실행한 로그를 코드의 except 절과 짝지어 보면 이 순서 설계가 실제로 어떻게 동작하는지 명확해집니다.

| 손상 시나리오 | 실제 출력 로그 | 대응하는 except 절 |
|---|---|---|
| 빈 파일(JSON 문법 자체가 깨짐) | `⚠️ 데이터 파일의 JSON 형식이 손상되었습니다: Expecting value: line 1 column 1 (char 0)` | `except json.JSONDecodeError as error:` |
| `{"hello": "world"}` (JSON 문법은 맞지만 `quizzes` 키 없음) | `⚠️ 데이터 파일의 구조가 올바르지 않습니다: 'quizzes'` | `except (KeyError, TypeError, ValueError) as error:` |
| UTF-8로 디코딩 불가능한 바이트 포함 | `⚠️ 데이터 파일을 UTF-8로 읽을 수 없습니다: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte` | `except UnicodeDecodeError as error:` |

두 번째 행이 흥미로운데, `{"hello": "world"}`는 JSON 문법상 완전히 유효하므로 `json.load()` 자체는 성공합니다. 문제는 그다음 `_parse_state()` 안의 `data["quizzes"]`에서 발생합니다. `raw_quizzes = data["quizzes"]` 줄이 존재하지 않는 키에 접근하면서 `KeyError: 'quizzes'`를 일으키고, 이것이 `(KeyError, TypeError, ValueError)` 절에서 잡혀 "구조가 올바르지 않습니다"라는 정확한 메시지로 이어집니다. 세 로그 모두 원인에 맞는 메시지가 정확히 갈라져 나온 것은, 앞서 설명한 "구체적인 예외를 먼저 검사한다"는 순서 원칙이 실제로 지켜졌기 때문입니다.

### 백업이 실패해도 복구는 계속된다

JSON 손상이나 UTF-8 디코딩 실패가 감지되면 `_backup_corrupted_file()`이 손상된 파일을 `state.json.bak`으로 옮겨 둡니다.

```python
def _backup_corrupted_file(state_file: Path) -> None:
    backup_file = state_file.with_name(f"{state_file.name}.bak")
    try:
        state_file.replace(backup_file)
    except OSError:
        pass
```

여기서 주목할 부분은 `except OSError: pass`입니다. `Path.replace()`가 파일 권한 문제 등으로 `OSError`를 던지더라도, 이 함수는 그 예외를 자기 안에서 조용히 삼켜버립니다. 즉 "손상된 원본을 백업으로 남기는 작업"이 실패하더라도, 그 실패가 `load_state()`까지 다시 전파되어 복구 흐름 전체를 멈추게 하지 않습니다. 백업은 "되면 좋은 부가 기능"이고, 기본 퀴즈로 복구해서 프로그램을 계속 실행시키는 것이 더 우선순위가 높은 목표이기 때문입니다.

### best_score도 이제는 선택적 필드

이전 Step까지는 저장 파일에 `best_score` 키가 없으면 곧바로 `KeyError`가 발생하는 필수 키였습니다. 이번 `_parse_state()`에서는 `data.get("best_score", 0)`으로 바뀌어, 키가 없어도 예외 없이 `0`으로 채워집니다. `best_correct`, `best_total`도 같은 방식입니다. 옛 버전 형식의 `state.json`을 읽더라도 프로그램이 곧바로 죽지 않고 점수만 0으로 초기화된 채 정상 동작하도록 하기 위한 하위 호환성 처리입니다. 실제로 `load_state()` 성공 시 출력되는 `✅ 저장된 데이터 로드 완료! (퀴즈: 5개, 최고 점수: 100점)` 같은 안내 메시지의 점수 부분이 바로 이 `_require_nonnegative_int(data.get("best_score", 0), ...)` 값에서 나옵니다.

---

## 6-4. 호출 지점과 재시작 검증

`storage.py`의 `load_state()`/`save_state()`가 내부적으로 어떻게 동작하는지 아무리 꼼꼼히 봐도, 정작 그 함수들이 **언제 호출되는지**를 확인하지 않으면 절반짜리 이해에 그칩니다. 함수가 아무리 안전하게 짜여 있어도 호출 위치가 빠지면 "게임을 껐다 켜면 방금 추가한 퀴즈가 사라지는" 버그가 생길 수 있기 때문입니다. 이 섹션에서는 `main.py` 안에서 `save_state()`/`load_state()`가 실제로 호출되는 4개 지점을 모아서 확인하고, 이어서 재실행·복구 시나리오를 하나씩 직접 검증한 결과를 정리합니다.

### 호출 지점 4곳 한눈에 보기

커밋 `5ca7c4d`에서 `main.py`에 추가된 4줄은 전부 로직이 아니라 **설명 주석**이었습니다(실제 저장/불러오기 로직은 이전 단계에서 이미 있었고, 이번에 그 옆에 "왜 여기서 호출하는지"를 적어 넣은 것입니다). 신기하게도 이 주석 4개는 정확히 저장/불러오기가 호출되는 4개 지점 위에 하나씩 붙어 있습니다.

| # | 호출 지점 | 위치 | 주석 |
|---|---|---|---|
| 1 | `QuizGame.__init__` → `self.load_state()` | 19~20행 | `# 게임을 만들자마자 이전 퀴즈·최고 기록을 복원한다.` |
| 2 | `add_quiz()` 성공 직후 → `self.save_state()` | 140~141행 | `# 새 퀴즈는 다음 종료를 기다리지 않고 즉시 파일에 반영한다.` |
| 3 | `play_quiz()` 최고 점수 갱신 시 → `self.save_state()` | 123~124행 | `# 최고 기록을 갱신한 즉시 재시작 후에도 남도록 저장한다.` |
| 4 | `run()` 메뉴 5번 종료 + `main()`의 Ctrl+C·EOF 처리 → `save_state()` | 49~50행, 193~215행 | `# 정상 종료 전에도 현재 변경 사항을 한 번 더 저장한다.` |

4번 지점은 조금 특이합니다. 실제 코드에서 `save_state()`를 부르는 곳은 두 군데(`run()` 내부의 정상 종료 분기, 그리고 `main()`이 `KeyboardInterrupt`·`EOFError`를 잡았을 때 호출하는 `_save_before_exit()` 함수 내부)이지만, 이 둘은 "어떤 식으로 끝나든 저장 없이 종료하지 않는다"는 하나의 설계 원칙을 공유합니다. `_save_before_exit()`가 정상 종료 코드와 별도의 작은 함수로 분리되어 있는 이유도, `try`가 끝난 뒤 어디서 예외가 잡히든 같은 저장·안내 로직을 재사용하기 위해서입니다.

```python
def _save_before_exit(game: QuizGame) -> None:
    """예상하지 못한 종료 전에 가능한 범위에서 현재 상태를 저장한다."""
    if game.save_state():
        print("💾 현재 데이터를 저장하고 종료합니다.")
    else:
        print("⚠️ 데이터를 저장하지 못했지만 프로그램을 종료합니다.")
```

`load_state()`는 반대로 딱 1곳, `__init__`에서만 호출됩니다. 게임 도중에는 파일을 다시 읽어올 이유가 없기 때문입니다. 실행 중에는 메모리의 `self.quizzes`, `self.best_score` 등이 유일한 진실이고, `save_state()`가 그 스냅샷을 파일로 내보내는 역할만 합니다.

### 재실행 검증 1 — 퀴즈를 추가하고 재실행

`add_quiz()`의 저장 호출이 실제로 작동하는지는, 새 퀴즈를 추가한 뒤 프로그램을 완전히 새로 켜서 목록에 남아 있는지로 확인합니다. 실제 재실행 로그입니다.

```
✅ 저장된 데이터 로드 완료! (퀴즈: 5개, 최고 점수: 100점)
...
📋 등록된 퀴즈 목록 (총 6개)
----------------------------------------
[1] 스택(Stack)의 주요 자료 처리 방식은 무엇인가요?
[2] 큐(Queue)의 주요 특징으로 옳은 것은 무엇인가요?
[3] 해시 테이블(Hash Table)에서 해시 함수(Hash Function)의 핵심 역할은 무엇인가요?
[4] 이진 탐색 트리(BST)의 자식 노드 배치 규칙으로 옳은 것은 무엇인가요?
[5] 정렬된 N개의 배열에서 이진 탐색(Binary Search)의 시간 복잡도는 무엇인가요?
[6] 나는
```

새로 추가한 `[6] 나는` 문제가 재실행 후에도 남아 있으므로, 140~141행의 즉시 저장 호출이 의도대로 동작함을 확인했습니다. 참고로 이 시점에 `ls`를 실행했을 때 `state.json.tmp`라는 낯선 파일이 목록에 잠깐 보였는데, 이 파일은 뒤에서 따로 짚고 넘어갑니다.

### 재실행 검증 2 — 점수를 기록하고 재실행

퀴즈를 풀어 100점을 기록한 뒤 재실행했을 때도 `✅ 저장된 데이터 로드 완료! (퀴즈: 5개, 최고 점수: 100점)`처럼 100점이 그대로 로드되는 것을 확인했습니다(이 확인 자체는 6단계 문서의 3~4단계에서 이미 다룬 내용이지만, 위 "퀴즈 추가 후 재실행" 로그의 첫 줄에도 똑같이 `최고 점수: 100점`이 찍혀 있어 여러 번의 재실행에 걸쳐 최고 기록이 안정적으로 유지됨을 다시 확인할 수 있습니다). 즉 123~124행의 저장 호출과 19~20행의 불러오기 호출이 짝을 이루어 정상 동작하고 있다는 뜻입니다.

### 첫 실행 복구 3가지 — 실제 로그로 확인

| 손상 상황 | 실제 출력 |
|---|---|
| `state.json` 이름 변경/제거 | (파일 없음은 손상이 아니라 첫 실행과 동일하게 처리되어, 별도 경고 없이 조용히 기본 퀴즈 5개로 복구됩니다.) |
| 빈 파일(JSON 문법 깨짐) | `⚠️ 데이터 파일의 JSON 형식이 손상되었습니다: Expecting value: line 1 column 1 (char 0)` → `🔧 기본 퀴즈 데이터로 복구합니다.` |
| `{"hello": "world"}` (필수 키 없음) | `⚠️ 데이터 파일의 구조가 올바르지 않습니다: 'quizzes'` → `🔧 기본 퀴즈 데이터로 복구합니다.` |
| UTF-8로 디코딩 안 되는 바이트 | `⚠️ 데이터 파일을 UTF-8로 읽을 수 없습니다: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte` → `🔧 기본 퀴즈 데이터로 복구합니다.` |

세 가지 손상 상황이 각각 다른 메시지로 정확히 구분되는 이유(왜 `except` 절 순서가 중요한지)는 6-3에서 다룬 `JSONDecodeError`/`UnicodeDecodeError`가 `ValueError`의 서브클래스라는 사실과 직결됩니다. 여기서는 그 설계가 실제로 세 가지 실행 결과로 정확히 이어졌다는 점만 확인하고 넘어갑니다.

### 상위 폴더에서 실행 — "최고 점수: 0점"은 버그가 아닙니다

`second-project`의 상위 폴더에서 `python second-project/main.py`로 실행하면 다음과 같이 나옵니다.

```
✅ 저장된 데이터 로드 완료! (퀴즈: 5개, 최고 점수: 0점)
```

이걸 보고 "상위 폴더에서 실행했더니 100점 기록이 날아갔다"고 오해하기 쉽지만, 실제 원인은 다릅니다. 이 테스트 직전에 실행했던 UTF-8 손상 테스트가 이미 `_restore_default_state()`를 거쳐 `state.json`을 기본 퀴즈 5개·최고 점수 0점으로 다시 써 두었습니다. 즉 100점 기록은 상위 폴더 실행 때문에 사라진 게 아니라, 그 직전의 복구 테스트에서 이미 초기화되어 있었던 것입니다. 이 테스트에서 실제로 확인해야 할 것은 점수가 아니라 **경로**입니다. `storage.py`의 `STATE_FILE`은 `Path(__file__).resolve().parent`를 기준으로 계산되므로, 실행 시점의 현재 작업 디렉터리가 어디든 상관없이 항상 `storage.py`가 실제로 위치한 프로젝트 루트의 `state.json`만 가리킵니다. 상위 폴더에 새 `state.json`이 생기지 않고 같은 파일을 다시 읽었다는 사실이 이 항목의 진짜 검증 포인트입니다.

### python -m json.tool로 유효성 확인

```bash
python3 -m json.tool --no-ensure-ascii state.json
```

`--no-ensure-ascii` 없이 실행하면 한글이 `\uc2a4\ud0dd` 같은 유니코드 이스케이프로 보이는데, 이는 저장 파일이 잘못됐기 때문이 아니라 `json.tool`이라는 별도 CLI 도구가 재출력할 때 기본값으로 `ensure_ascii=True`를 쓰기 때문입니다. `save_state()`는 이미 `ensure_ascii=False`로 저장하므로 파일 자체에는 한글이 원문 그대로 들어 있고, `--no-ensure-ascii` 옵션은 그 원문을 도구가 다시 이스케이프하지 않도록 막아주는 역할만 합니다. 이 명령이 오류 없이 끝난다는 것 자체가 "유효한 JSON"임을 보여주는 가장 간단한 검증 방법입니다.

### 정직하게 짚고 넘어가야 할 것 — state.json.tmp

퀴즈 추가 재실행 테스트 당시 `ls` 결과에 `state.json.tmp`라는 파일이 잠깐 등장했습니다. 하지만 현재 `storage.py`의 `save_state()`/`load_state()` 코드 어디에도 `.tmp` 확장자의 임시 파일을 만드는 로직은 없습니다 — `Path(state_file).open("w", ...)`로 `state.json`을 직접 덮어쓸 뿐, 실제 서비스에서 흔히 쓰는 "임시 파일에 먼저 쓰고 `os.replace()`로 원자적으로 교체"하는 패턴은 이 프로젝트에 아직 적용되어 있지 않습니다. `.gitignore`에도 `.tmp` 파일은 등록되어 있지 않고, 지금 프로젝트 루트에도 그 파일은 존재하지 않습니다. 즉 이 파일이 정확히 어디서 왜 생겼는지는 지금 코드만 봐서는 설명할 수 없습니다 — 복구 테스트를 위해 손으로 만들었던 임시 파일일 가능성이 높아 보이지만, 이는 추측일 뿐 확정할 수 없습니다. (참고로 저장을 이 방식으로 안전하게 만드는 원자적 쓰기 패턴은 다음 단계 이후에 다뤄볼 만한 흥미로운 주제입니다.)

### 마무리 — 손상 테스트 흔적 남기지 않기

복구 테스트를 마친 뒤에는 반드시 퀴즈를 다시 풀거나 추가해 정상적인 `state.json`을 새로 만들어 두어야 합니다. 손상시켰던 테스트 파일(빈 파일, `{"hello": "world"}`, 깨진 바이트 파일 등)을 그대로 커밋하면 다음에 이 프로젝트를 여는 사람이 진짜 버그로 착각할 수 있습니다. 실제로 `git status`를 확인한 결과 현재 작업 트리는 완전히 깨끗한 상태였고, 이는 손상 테스트 파일이 남지 않았다는 뜻입니다.

---

## 6-5. Step 5 Git 체크포인트

체크리스트에는 커밋 #12(저장 기능), #13(불러오기 및 복구), 선택 커밋 #14(모듈 분리), 그리고 push까지 총 네 개의 할 일이 적혀 있습니다. 결론부터 확인하면, 이 네 가지는 이미 모두 처리되어 원격 저장소까지 반영되어 있습니다.

```bash
$ git log --oneline --graph --all --decorate
* 5ca7c4d (HEAD -> main, origin/main) Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False), son 불러오기 및 파일 부재/손상 시 자동 복구 처리
* 677163a Feat: 퀴즈 추가 기능 및 입력 유효성 검사 구현 퀴즈목록 조회 기능 구현 최고점수 확인 긴으 구현
*   0e84cc0 Merge: 퀴즈 풀기 기능 병합
...
```

`HEAD`와 `origin/main`이 동시에 `5ca7c4d`를 가리키고 있다는 것은 이 커밋이 로컬에 만들어졌을 뿐 아니라 `git push`로 원격까지 이미 올라갔다는 뜻입니다. 또한 `git status`가 완전히 깨끗한 상태이므로, 커밋에 포함되지 않고 남아 있는 변경 사항도 없습니다. 즉 이 섹션의 네 항목은 체크만 하면 되는 상태입니다.

### 커밋 안에 실제 무엇이 들어 있는지 확인하기

체크가 된 상태라고 해서 안심하고 넘어가기보다는, 그 커밋이 실제로 무슨 코드를 담고 있는지 `git show --stat`으로 확인하는 습관이 중요합니다.

```bash
$ git show --stat 5ca7c4d
 README.md                          |  26 ++-
 docs/learning_checklist.md         | 381 +++++++++++++++++++++++++++++++------
 docs/screenshots/step4.png         | Bin 0 -> 108261 bytes
 docs/study/step4_add_list_score.md | 298 +++++++++++++++++++++++++++++
 main.py                            |   4 +
 storage.py                         |  71 ++++++-
 6 files changed, 709 insertions(+), 71 deletions(-)
```

이번 Step 5의 실질적인 작업은 `storage.py`의 71줄 변경입니다. `_restore_default_state()` 함수 분리, 4가지 손상 유형(파일 없음/JSON 문법 오류/UTF-8 디코딩 실패/구조 오류)별로 나뉜 개별 `except` 절, `best_score`를 `data.get()`으로 선택적 필드화한 부분이 여기에 해당합니다. `main.py`의 4줄도 함께 포함되어 있지만, 이 4줄은 로직 변경이 아니라 "게임을 만들자마자 이전 퀴즈·최고 기록을 복원한다", "새 퀴즈는 다음 종료를 기다리지 않고 즉시 파일에 반영한다"와 같은 설명 주석입니다. 즉 커밋 메시지가 가리키는 저장/불러오기/복구 기능이 코드 diff 안에 실제로, 그것도 상당한 분량으로 들어 있다는 점을 확인할 수 있습니다.

### 커밋 메시지의 흠: "son 불러오기"

다만 커밋 메시지 자체에는 눈에 띄는 오타가 있습니다.

```
Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False), son 불러오기 및 파일 부재/손상 시 자동 복구 처리
```

체크리스트는 원래 이 작업을 커밋 #12 "Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False)"와 커밋 #13 "Feat: state.json 불러오기 및 파일 부재/손상 시 자동 복구 처리"로 나누어 커밋하도록 안내했습니다. 그런데 실제로는 이 두 메시지가 쉼표로 이어붙으며 하나의 커밋이 되었고, 그 접합부에서 "state.json 불러오기"의 앞부분("state.j")이 잘려나가 "son 불러오기"라는 어색한 문구가 남았습니다. 두 메시지를 이어붙여 편집하는 과정에서 생긴 오타로 보이며, 기능 자체와는 무관하지만 커밋 히스토리를 나중에 다시 읽을 때 혼란을 줄 수 있는 흠입니다.

이 문제를 Step 4의 `677163a`와 혼동하지 않는 것이 중요합니다. 둘 다 "계획한 여러 커밋이 하나로 합쳐졌다"는 공통점은 있지만, 문제의 성격은 다릅니다.

| 구분 | Step 4 `677163a` | Step 5 `5ca7c4d` |
|---|---|---|
| 합쳐진 계획 | 여러 기능 커밋 계획이 1개로 병합 | 커밋 #12 + #13이 1개로 병합 |
| 메시지 문제 | 메시지 자체는 멀쩡함 | 접합부에서 문구가 잘려 오타 발생("son 불러오기") |
| 코드 문제 | diff에 메시지가 가리키는 관련 코드가 실제로 없었음 | storage.py 71줄 등 관련 코드가 diff에 그대로 들어 있음 |
| 심각도 | 메시지와 코드가 어긋나는 근본적 문제 | 여러 메시지가 이어붙으며 생긴 표면적 오타 |

즉 `677163a`는 "메시지가 가리키는 코드가 없다"는 더 근본적인 문제였던 반면, `5ca7c4d`는 "코드는 제대로 들어 있지만 메시지 편집 과정에서 오타가 생겼다" 수준의 문제입니다.

### 선택 커밋 #14는 왜 필요 없는가

체크리스트의 선택 항목 "파일을 분리했다면 git commit -m "Refactor: Quiz/QuizGame/storage 모듈 분리"으로 선택 커밋 #14"는 이 프로젝트에서는 별도로 만들 필요가 없습니다. `main.py`/`quiz.py`/`storage.py`로 파일을 나누는 작업은 이미 Step 1과 Step 2 사이(`docs/study/step1_quiz_model.md`, `step2_quizgame_menu.md` 참고)에 끝나 있었기 때문입니다. Step 5 시점에는 새로 분리할 파일 구조 변경 자체가 없으므로, 이 항목은 "조건에 해당하지 않아 건너뛰는 것이 맞는" 선택 커밋입니다.

### 다섯 Step에 걸쳐 반복된 패턴

지금까지의 커밋 이력을 보면 계획한 여러 커밋이 실제로는 하나로 합쳐지는 패턴이 다섯 단계 내내 반복되었습니다.

```
6868c74 → 5ba64a0 → 1181dea → 677163a → 5ca7c4d
```

각 단계마다 여러 개의 작업 단위를 계획했지만 실제 커밋 개수는 그보다 적었고, 이번 `5ca7c4d`에서는 그 여파로 커밋 메시지 접합부에 오타까지 남았습니다. 코드 자체는 정상적으로 동작하므로 기능상의 문제는 아니지만, 나중에 `git log`나 `git blame`으로 특정 변경의 이유를 추적할 때는 메시지가 정확할수록 훨씬 도움이 됩니다.

다음 Step부터 시도해볼 수 있는 실용적인 방법은 다음과 같습니다.

- 기능 하나를 끝낼 때마다 미루지 말고 바로 커밋합니다. 여러 기능을 모아두었다가 한 번에 커밋하면 메시지를 이어붙이는 과정에서 이번처럼 오타나 누락이 생기기 쉽습니다.
- 커밋하기 직전에 `git status`와 `git diff --cached`로 무엇이 스테이징되어 있는지 한 번 더 확인합니다. 특히 `git diff --cached`는 커밋 메시지가 말하는 내용과 실제로 올라가는 코드가 일치하는지 눈으로 검증할 수 있는 가장 확실한 방법입니다.

---

## 정리 — 확인하고 넘어가면 좋은 것들

Step 5에서 실제로 구현·검증까지 끝난 부분과, 아직 남은 부분을 구분하면 다음과 같습니다.

**이미 끝난 것 (코드·실행 결과로 확인됨)**
- `STATE_FILE`이 `Path(__file__).resolve().parent` 기준으로 계산되어, 실행 위치(cwd)와 무관하게 항상 같은 `state.json`을 사용함(상위 폴더에서 실행한 테스트로 확인)
- `save_state()`가 `to_dict()`로 `Quiz` 객체를 JSON 호환 형태로 바꾸고, UTF-8·`ensure_ascii=False`·`indent=2`로 사람이 읽을 수 있는 파일을 만듦
- `load_state()`가 `FileNotFoundError`/`JSONDecodeError`/`UnicodeDecodeError`/`(KeyError, TypeError, ValueError)`/`OSError` 다섯 갈래로 나뉘어, 각 손상 유형마다 정확한 메시지로 안내하고 기본 데이터로 복구함(빈 파일, 키 누락, 잘못된 인코딩 세 가지 모두 실제 로그로 검증됨)
- 커밋 `5ca7c4d`가 실제로 만들어져 `origin/main`까지 push되고, 이번엔 실제 코드(storage.py 71줄)가 그 안에 포함됨

**다음에 정리하면 좋은 것 (계획과 실제가 갈라진 지점)**
- [ ] `docs/learning_checklist.md`의 "6-5. Step 5 Git 체크포인트" 체크박스를 실제 상황에 맞게 정리하기 — 커밋 #12/#13이 실제로는 `5ca7c4d` 하나로 합쳐졌고, 그 과정에서 커밋 메시지에 "son 불러오기"라는 편집 오타가 남았다는 것을 메모로 남기기
- [ ] `state.json.tmp`가 한 번 목격됐지만 현재 코드 어디에도 그 파일을 만드는 로직이 없다는 점을 확인하고, 필요하다면 원자적 쓰기(임시 파일 + `os.replace`)를 실제로 도입할지 결정하기
- [ ] 다섯 개 Step에 걸쳐 반복된 "계획한 여러 커밋이 하나로 합쳐지는" 패턴을 다음 기능부터는 의식적으로 깨 보기

이 항목들을 정리한 뒤에는 [`docs/learning_checklist.md`](../learning_checklist.md)의 다음 단계로 넘어갈 수 있습니다.

## 참고 문서

- [Step 0 학습 노트](step0_dev_environment_git_init.md) — 개발 환경 설정과 Git 저장소 초기화
- [Step 1 학습 노트](step1_quiz_model.md) — Quiz 모델과 자료구조 기본 데이터
- [Step 2 학습 노트](step2_quizgame_menu.md) — QuizGame, 메뉴, 공통 입력과 안전 종료
- [Step 3 학습 노트](step3_play_quiz_branch.md) — feat/play-quiz 브랜치와 퀴즈 풀기
- [Step 4 학습 노트](step4_add_list_score.md) — 퀴즈 추가, 목록 조회, 점수 확인
- [학습 체크리스트](../learning_checklist.md) — 이 문서의 원본 체크리스트
- [학습 가이드](../learning_guide.md) — 단계별 실습 코드와 커밋 힌트
- [프로젝트 README](../../README.md) — 실제로 작성된 프로젝트 설명 문서
