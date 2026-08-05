"""퀴즈 한 문제를 표현하는 도메인 모델."""

from __future__ import annotations

from typing import Any


class Quiz:
    """문제, 선택지 4개, 1-based 정답 번호를 관리하는 퀴즈 모델."""

    def __init__(self, question: str, choices: list[str], answer: int) -> None:
        """유효한 퀴즈 데이터를 저장한다.

        ``answer``는 사용자가 보는 번호와 동일하게 1~4로 저장한다.
        리스트 인덱스로 선택지를 조회할 때만 ``answer - 1``을 사용한다.
        """
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

    def display(self, number: int | None = None) -> None:
        """문제와 선택지 4개를 사용자에게 출력한다."""
        if number is not None:
            print(f"[문제 {number}] {self.question}")
        else:
            print(self.question)

        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        """사용자 입력이 1-based 정답 번호와 일치하는지 반환한다."""
        return (
            isinstance(user_answer, int)
            and not isinstance(user_answer, bool)
            and user_answer == self.answer
        )

    def get_correct_text(self) -> str:
        """정답 선택지 텍스트를 안전하게 반환한다."""
        return self.choices[self.answer - 1]

    def to_dict(self) -> dict[str, Any]:
        """JSON으로 저장할 수 있는 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quiz":
        """JSON에서 읽은 딕셔너리로부터 Quiz 객체를 복원한다."""
        if not isinstance(data, dict):
            raise TypeError("퀴즈 데이터는 딕셔너리여야 합니다.")

        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
        )


def get_default_quizzes() -> list[Quiz]:
    """기본 자료구조 퀴즈 5개를 새 목록으로 반환한다.

    이 함수는 ``state.json``이 없거나 손상되어 ``load_state()``가
    복구해야 할 때 사용하는 기본 데이터의 단일 출처다.
    """
    return [
        Quiz(
            "스택(Stack)의 주요 자료 처리 방식은 무엇인가요?",
            [
                "FIFO (선입선출)",
                "LIFO (후입선출)",
                "LILO (후입후출)",
                "무작위 접근",
            ],
            2,
        ),
        Quiz(
            "큐(Queue)의 주요 특징으로 옳은 것은 무엇인가요?",
            [
                "먼저 들어간 데이터가 먼저 나온다 (FIFO)",
                "나중에 들어간 데이터가 먼저 나온다 (LIFO)",
                "항상 가장 큰 값이 먼저 나온다",
                "순서와 관계없이 무작위로 나온다",
            ],
            1,
        ),
        Quiz(
            "해시 테이블(Hash Table)에서 해시 함수(Hash Function)의 핵심 역할은 무엇인가요?",
            [
                "데이터를 오름차순으로 정렬한다",
                "키(Key)를 해시값 또는 인덱스로 변환한다",
                "데이터를 후입선출 구조로 저장한다",
                "트리의 높이를 자동으로 균형 있게 맞춘다",
            ],
            2,
        ),
        Quiz(
            "이진 탐색 트리(BST)의 자식 노드 배치 규칙으로 옳은 것은 무엇인가요?",
            [
                "왼쪽 자식은 부모보다 크고, 오른쪽 자식은 작다",
                "왼쪽 자식은 부모보다 작고, 오른쪽 자식은 크다",
                "모든 자식 노드는 부모보다 무조건 크다",
                "노드의 크기와 관계없이 무작위로 배치한다",
            ],
            2,
        ),
        Quiz(
            "정렬된 N개의 배열에서 이진 탐색(Binary Search)의 시간 복잡도는 무엇인가요?",
            [
                "O(1)",
                "O(log n)",
                "O(n)",
                "O(n²)",
            ],
            2,
        ),
    ]


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
