"""퀴즈 게임의 state.json 불러오기와 안전한 기본 데이터 복구를 담당한다."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from quiz import Quiz, get_default_quizzes


STATE_FILE = Path(__file__).resolve().parent / "state.json"


def _default_state() -> tuple[list[Quiz], int]:
    """복구에 사용할 새 기본 퀴즈 목록과 초기 최고 점수를 반환한다."""
    return get_default_quizzes(), 0


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


def _parse_state(data: Any) -> tuple[list[Quiz], int]:
    """JSON으로 읽은 값을 프로젝트의 state.json 스키마로 검증한다."""
    if not isinstance(data, dict):
        raise ValueError("state.json의 최상위 값은 객체(dict)여야 합니다.")

    raw_quizzes = data["quizzes"]
    if not isinstance(raw_quizzes, list):
        raise TypeError("state.json의 quizzes는 리스트여야 합니다.")

    quizzes = [Quiz.from_dict(raw_quiz) for raw_quiz in raw_quizzes]

    best_score = data["best_score"]
    if isinstance(best_score, bool) or not isinstance(best_score, int):
        raise TypeError("state.json의 best_score는 정수여야 합니다.")
    if best_score < 0:
        raise ValueError("state.json의 best_score는 0 이상이어야 합니다.")

    return quizzes, best_score


def load_state(state_file: Path | str = STATE_FILE) -> tuple[list[Quiz], int]:
    """저장된 퀴즈와 최고 점수를 불러오고, 실패하면 기본값으로 복구한다.

    이후 ``QuizGame.__init__()``에서 ``self.quizzes, self.best_score =
    load_state()``처럼 호출할 수 있다. 파일 없음은 첫 실행의 정상 상태로
    처리하며, JSON 또는 스키마가 손상된 파일은 가능한 경우 ``.bak``으로
    보관한 뒤 :func:`get_default_quizzes`의 데이터로 복구한다.
    """
    path = Path(state_file)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return _parse_state(data)
    except FileNotFoundError:
        return _default_state()
    except (json.JSONDecodeError, KeyError, TypeError, ValueError, UnicodeDecodeError) as error:
        _backup_corrupted_file(path)
        print(f"⚠️ 데이터 파일이 손상되었습니다: {error}")
        print("🔧 기본 퀴즈 데이터로 복구합니다.")
        return _default_state()
    except OSError as error:
        print(f"⚠️ 데이터 파일을 읽을 수 없습니다: {error}")
        print("🔧 기본 퀴즈 데이터로 복구합니다.")
        return _default_state()


def save_state(
    quizzes: list[Quiz], best_score: int, state_file: Path | str = STATE_FILE
) -> bool:
    """퀴즈 목록과 최고 점수를 UTF-8 JSON 파일로 저장한다.

    저장 실패는 게임 종료나 메뉴 흐름을 막지 않도록 안내 후 ``False``를
    반환한다. 성공하면 ``True``를 반환한다.
    """
    if isinstance(best_score, bool) or not isinstance(best_score, int):
        raise TypeError("최고 점수는 정수여야 합니다.")
    if best_score < 0:
        raise ValueError("최고 점수는 0 이상이어야 합니다.")
    if not all(isinstance(quiz, Quiz) for quiz in quizzes):
        raise TypeError("저장할 모든 항목은 Quiz 객체여야 합니다.")

    data = {
        "quizzes": [quiz.to_dict() for quiz in quizzes],
        "best_score": best_score,
    }

    try:
        with Path(state_file).open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
        return False

    return True
