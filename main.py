"""자료구조 터미널 퀴즈 게임의 실행 흐름을 관리한다."""

from __future__ import annotations

from quiz import Quiz, get_default_quizzes
from storage import load_state as load_quiz_state
from storage import save_state as save_quiz_state


class QuizGame:
    """메뉴, 게임 데이터, 각 기능 호출의 흐름을 관리하는 클래스."""

    def __init__(self) -> None:
        self.quizzes: list[Quiz] = []
        self.best_score: int = 0
        self.best_correct: int = 0
        self.best_total: int = 0

        self.load_state()

    def show_menu(self) -> None:
        """자료구조 퀴즈 게임의 1~5번 메뉴를 출력한다."""
        print("\n" + "=" * 40)
        print("      🎯 자료구조 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def run(self) -> None:
        """메뉴를 반복 표시하고 선택한 기능으로 분기한다."""
        while True:
            self.show_menu()
            choice = self.ask_int("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_score()
            else:
                self.save_state()
                print("\n👋 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
                return

    def ask_int(self, prompt: str, low: int, high: int) -> int:
        """``low``~``high`` 범위의 정수를 입력받을 때까지 재시도한다.

        ``ValueError``만 처리하여 ``KeyboardInterrupt``와 ``EOFError``는
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

    def ask_text(self, prompt: str) -> str:
        """비어 있지 않은 문자열을 입력받을 때까지 재시도한다."""
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")

    def play_quiz(self) -> None:
        """1번 메뉴: 퀴즈 풀기 기능의 자리다."""
        print("\n🚧 [퀴즈 풀기] 기능 준비 중입니다.")

    def add_quiz(self) -> None:
        """2번 메뉴: 퀴즈 추가 기능의 자리다."""
        print("\n🚧 [퀴즈 추가] 기능 준비 중입니다.")

    def show_quiz_list(self) -> None:
        """3번 메뉴: 퀴즈 목록 기능의 자리다."""
        print("\n🚧 [퀴즈 목록] 기능 준비 중입니다.")

    def show_score(self) -> None:
        """4번 메뉴: 점수 확인 기능의 자리다."""
        print("\n🚧 [점수 확인] 기능 준비 중입니다.")

    def save_state(self) -> bool:
        """현재 퀴즈 목록과 최고 점수를 JSON 파일에 저장한다."""
        return save_quiz_state(self.quizzes, self.best_score)

    def load_state(self) -> None:
        """저장된 데이터를 불러오고, 실패하면 기본 퀴즈로 복구한다."""
        self.quizzes, self.best_score = load_quiz_state()


def _save_before_exit(game: QuizGame) -> None:
    """예상하지 못한 종료 전에 가능한 범위에서 현재 상태를 저장한다."""
    if game.save_state():
        print("💾 현재 데이터를 저장하고 종료합니다.")
    else:
        print("⚠️ 데이터를 저장하지 못했지만 프로그램을 종료합니다.")


def main() -> None:
    """터미널 퀴즈 게임을 실행하고 종료 입력을 안전하게 처리한다."""
    game: QuizGame | None = None

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


if __name__ == "__main__":
    main()
