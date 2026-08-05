"""퀴즈 게임의 state.json 불러오기와 안전한 기본 데이터 복구를 담당한다."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from quiz import Quiz, get_default_quizzes


# 현재 작업 디렉터리와 무관하게 storage.py가 있는 프로젝트 루트만 사용한다.
STATE_FILE = Path(__file__).resolve().parent / "state.json"


State = tuple[list[Quiz], int, int, int, list[dict[str, Any]]]


def _default_state() -> State:
    """복구에 사용할 기본 퀴즈, 최고 기록, 빈 히스토리를 반환한다."""
    return get_default_quizzes(), 0, 0, 0, []


def _backup_corrupted_file(state_file: Path) -> None:
    """손상 파일을 ``<파일명>.bak``으로 옮긴다.

    백업 자체가 실패해도 기본 데이터 복구를 방해하면 안 되므로, 그 오류는
    호출자에게 전파하지 않는다.
    """
    backup_file = state_file.with_name(f"{state_file.name}.bak")
    try:
        state_file.replace(backup_file)
    except OSError:
        pass


def _require_nonnegative_int(value: Any, field_name: str) -> int:
    """JSON 점수 필드가 0 이상의 정수인지 검증해 반환한다."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"state.json의 {field_name}는 정수여야 합니다.")
    if value < 0:
        raise ValueError(f"state.json의 {field_name}는 0 이상이어야 합니다.")
    return value


def _parse_history(value: Any) -> list[dict[str, Any]]:
    """저장된 게임 히스토리를 검증하고 JSON 호환 형태로 정리한다."""
    if not isinstance(value, list):
        raise TypeError("state.json의 history는 리스트여야 합니다.")

    history: list[dict[str, Any]] = []
    for number, record in enumerate(value, start=1):
        if not isinstance(record, dict):
            raise TypeError(f"history의 {number}번째 항목은 객체(dict)여야 합니다.")

        timestamp = record["timestamp"]
        if not isinstance(timestamp, str) or not timestamp.strip():
            raise TypeError(
                f"history의 {number}번째 timestamp는 비어 있지 않은 문자열이어야 합니다."
            )

        total = _require_nonnegative_int(record["total"], f"history[{number}].total")
        if total == 0:
            raise ValueError(f"history의 {number}번째 total은 1 이상이어야 합니다.")

        correct = _require_nonnegative_int(
            record["correct"], f"history[{number}].correct"
        )
        if correct > total:
            raise ValueError(
                f"history의 {number}번째 correct는 total보다 클 수 없습니다."
            )

        score = _require_nonnegative_int(record["score"], f"history[{number}].score")
        if score > 100:
            raise ValueError(f"history의 {number}번째 score는 100 이하여야 합니다.")

        history.append(
            {
                "timestamp": timestamp,
                "total": total,
                "correct": correct,
                "score": score,
            }
        )

    return history


def _parse_state(data: Any) -> State:
    """JSON으로 읽은 값을 프로젝트의 state.json 스키마로 검증한다."""
    if not isinstance(data, dict):
        raise ValueError("state.json의 최상위 값은 객체(dict)여야 합니다.")

    raw_quizzes = data["quizzes"]
    if not isinstance(raw_quizzes, list):
        raise TypeError("state.json의 quizzes는 리스트여야 합니다.")

    # Quiz.from_dict()가 각 항목의 dict 여부, 선택지 4개, 정답 1~4 규칙을
    # 함께 검증하며, 하나라도 잘못되면 예외를 내어 복구 경로로 보낸다.
    quizzes = [Quiz.from_dict(raw_quiz) for raw_quiz in raw_quizzes]

    # 저장 시에는 모든 점수 키를 기록한다. 다만 이전 버전 파일은 점수
    # 필드가 없을 수 있으므로, 로드할 때만 0으로 보완해 호환성을 유지한다.
    best_score = _require_nonnegative_int(data.get("best_score", 0), "best_score")
    if best_score > 100:
        raise ValueError("state.json의 best_score는 100 이하여야 합니다.")

    # 이전 버전 state.json에는 상세 최고 기록이 없을 수 있으므로 0으로 복원한다.
    best_correct = _require_nonnegative_int(
        data.get("best_correct", 0), "best_correct"
    )
    best_total = _require_nonnegative_int(data.get("best_total", 0), "best_total")
    if best_correct > best_total:
        raise ValueError("best_correct는 best_total보다 클 수 없습니다.")

    # 이전 버전 state.json에는 게임 이력이 없으므로 빈 목록으로 자연스럽게
    # 마이그레이션한다. 이후 저장 시에는 history 키를 포함한 최신 형식이 된다.
    history = _parse_history(data.get("history", []))

    return quizzes, best_score, best_correct, best_total, history


def _select_state_values(
    state: State, include_details: bool, include_history: bool
) -> (
    tuple[list[Quiz], int]
    | tuple[list[Quiz], int, int, int]
    | tuple[list[Quiz], int, list[dict[str, Any]]]
    | State
):
    """기존 반환 API를 유지하면서 필요할 때 상세 기록·히스토리를 포함한다."""
    quizzes, best_score, best_correct, best_total, history = state
    if include_details and include_history:
        return state
    if include_details:
        return quizzes, best_score, best_correct, best_total
    if include_history:
        return quizzes, best_score, history
    return quizzes, best_score


def _restore_default_state(state_file: Path) -> State:
    """기본 상태를 반환하고, 가능한 경우 지정한 경로에 즉시 저장한다.

    파일이 없는 첫 실행과 손상 파일 복구 후에도 상태 파일을 남겨야 다음
    실행부터 같은 프로젝트 루트의 데이터를 읽을 수 있다. 저장에 실패해도
    게임은 기본 데이터로 계속 실행할 수 있도록 상태 자체는 항상 반환한다.
    """
    state = _default_state()
    quizzes, best_score, best_correct, best_total, history = state
    save_state(
        quizzes,
        best_score,
        state_file,
        best_correct=best_correct,
        best_total=best_total,
        history=history,
    )
    return state


def load_state(
    state_file: Path | str = STATE_FILE,
    *,
    include_details: bool = False,
    include_history: bool = False,
) -> (
    tuple[list[Quiz], int]
    | tuple[list[Quiz], int, int, int]
    | tuple[list[Quiz], int, list[dict[str, Any]]]
    | State
):
    """저장된 퀴즈와 최고 점수를 불러오고, 실패하면 기본값으로 복구한다.

    기본값은 기존 호환성을 위해 ``(quizzes, best_score)``를 반환한다.
    ``include_details=True``이면 ``best_correct``와 ``best_total``까지 포함한
    네 값을 반환한다. ``include_history=True``이면 게임 기록 목록까지
    포함하며, 두 옵션을 모두 켜면 다섯 값을 반환한다. 파일 없음은 첫
    실행의 정상 상태로 처리하며 기본 상태를 그 경로에 생성한다. JSON 또는
    스키마가 손상된 파일은 가능한 경우 ``.bak``으로 보관한 뒤
    :func:`get_default_quizzes`의 데이터로 복구해 새 상태 파일을 생성한다.
    """
    path = Path(state_file)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        state = _parse_state(data)
        quizzes, best_score, _, _, history = state
        print(
            "✅ 저장된 데이터 로드 완료! "
            f"(퀴즈: {len(quizzes)}개, 최고 점수: {best_score}점, "
            f"게임 기록: {len(history)}회)"
        )
        return _select_state_values(state, include_details, include_history)
    except FileNotFoundError:
        # 첫 실행은 오류가 아니라 기본 상태 파일을 만드는 정상 흐름이다.
        return _select_state_values(
            _restore_default_state(path), include_details, include_history
        )
    except json.JSONDecodeError as error:
        # JSON 문법이 깨진 파일은 보관할 수 있으면 백업한 뒤 다시 만든다.
        _backup_corrupted_file(path)
        print(f"⚠️ 데이터 파일의 JSON 형식이 손상되었습니다: {error}")
        print("🔧 기본 퀴즈 데이터로 복구합니다.")
        return _select_state_values(
            _restore_default_state(path), include_details, include_history
        )
    except UnicodeDecodeError as error:
        # UTF-8로 해석할 수 없는 파일도 손상 데이터처럼 백업·복구한다.
        _backup_corrupted_file(path)
        print(f"⚠️ 데이터 파일을 UTF-8로 읽을 수 없습니다: {error}")
        print("🔧 기본 퀴즈 데이터로 복구합니다.")
        return _select_state_values(
            _restore_default_state(path), include_details, include_history
        )
    except (KeyError, TypeError, ValueError) as error:
        # 필수 키, 점수 형식, 퀴즈 보기·정답 규칙 위반을 모두 복구한다.
        _backup_corrupted_file(path)
        print(f"⚠️ 데이터 파일의 구조가 올바르지 않습니다: {error}")
        print("🔧 기본 퀴즈 데이터로 복구합니다.")
        return _select_state_values(
            _restore_default_state(path), include_details, include_history
        )
    except OSError as error:
        # 권한·장치 등 읽기 실패 시에는 파일을 덮어쓰지 않고 메모리에서만 복구한다.
        print(f"⚠️ 데이터 파일을 읽을 수 없습니다: {error}")
        print("🔧 기본 퀴즈 데이터로 복구합니다.")
        return _select_state_values(_default_state(), include_details, include_history)


def save_state(
    quizzes: list[Quiz],
    best_score: int,
    state_file: Path | str = STATE_FILE,
    *,
    best_correct: int = 0,
    best_total: int = 0,
    history: list[dict[str, Any]] | None = None,
) -> bool:
    """퀴즈 목록, 최고 기록, 게임 히스토리를 UTF-8 JSON 파일로 저장한다.

    저장 실패는 게임 종료나 메뉴 흐름을 막지 않도록 안내 후 ``False``를
    반환한다. 성공하면 ``True``를 반환한다.
    """
    best_score = _require_nonnegative_int(best_score, "best_score")
    if best_score > 100:
        raise ValueError("최고 점수는 100 이하여야 합니다.")
    best_correct = _require_nonnegative_int(best_correct, "best_correct")
    best_total = _require_nonnegative_int(best_total, "best_total")
    if best_correct > best_total:
        raise ValueError("맞힌 문제 수는 전체 문제 수보다 클 수 없습니다.")
    if not all(isinstance(quiz, Quiz) for quiz in quizzes):
        raise TypeError("저장할 모든 항목은 Quiz 객체여야 합니다.")
    if history is None:
        history = []
    history_data = _parse_history(history)

    # Quiz 객체를 직접 json.dump()하면 직렬화할 수 없으므로 dict로 변환한다.
    quiz_data = [quiz.to_dict() for quiz in quizzes]
    data = {
        "quizzes": quiz_data,
        "best_score": best_score,
        "best_correct": best_correct,
        "best_total": best_total,
        "history": history_data,
    }

    try:
        # UTF-8과 ensure_ascii=False로 한글을 그대로 보존하고, indent=2로
        # 사람이 state.json 내용을 쉽게 검토할 수 있게 한다.
        with Path(state_file).open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
        print("💡 프로그램은 계속 실행됩니다. 파일 저장 상태를 확인해 주세요.")
        return False

    return True
