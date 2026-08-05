"""자료구조 터미널 퀴즈 게임의 실행 흐름을 관리한다."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

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
        self.history: list[dict[str, Any]] = []

        # 게임을 만들자마자 이전 퀴즈·최고 기록을 복원한다.
        self.load_state()

    def show_menu(self) -> None:
        """자료구조 퀴즈 게임의 1~6번 메뉴를 출력한다."""
        print("\n" + "=" * 40)
        print("      🎯 자료구조 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    def run(self) -> None:
        """메뉴를 반복 표시하고 선택한 기능으로 분기한다."""
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
                # 정상 종료 전에도 현재 변경 사항을 한 번 더 저장한다.
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

    def ask_yes_no(self, prompt: str) -> bool:
        """``y`` 또는 ``n``을 입력받아 승인 여부를 반환한다."""
        while True:
            answer = input(prompt).strip().lower()
            if answer == "y":
                return True
            if answer == "n":
                return False
            print("⚠️ y 또는 n을 입력하세요.")

    def play_quiz(self) -> None:
        """선택한 수의 퀴즈를 출제하고 점수·최고 기록·히스토리를 저장한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total_quizzes = len(self.quizzes)
        count = self.ask_int(
            f"\n풀 문제 수를 입력하세요 (1~{total_quizzes}): ",
            1,
            total_quizzes,
        )

        # 저장·목록 조회에 쓰는 원본 순서는 유지하고, 출제용 복사본만 섞는다.
        quizzes_to_play = self.quizzes[:]
        random.shuffle(quizzes_to_play)
        quizzes_to_play = quizzes_to_play[:count]

        total = len(quizzes_to_play)
        correct = 0
        earned_points = 0.0
        print(f"\n📝 자료구조 퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(quizzes_to_play, start=1):
            print("\n" + "-" * 40)
            quiz.display(number)
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

        score = round(earned_points / total * 100)
        print("\n" + "=" * 40)
        print(
            f"🏆 결과: {total}문제 중 {correct}문제 정답! "
            f"(획득 점수: {earned_points:g}/{total}점 → {score}점)"
        )

        # 최고 기록과 별개로, 완료한 모든 게임을 시간·문항 수·정답 수·점수와
        # 함께 남긴다. 힌트 감점이 반영된 최종 score를 저장한다.
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

            if has_previous_record:
                print("🎉 새로운 최고 점수입니다!")
            else:
                print("🎉 첫 기록이 저장되었습니다!")

        # 낮은 점수·동점도 히스토리에는 남아야 하므로 매 게임 종료 후 저장한다.
        self.save_state()

        print("=" * 40)

    def add_quiz(self) -> None:
        """사용자 입력으로 새 퀴즈를 추가하고 즉시 저장한다."""
        print("\n📌 새로운 자료구조 퀴즈를 추가합니다.\n")
        question = self.ask_text("문제를 입력하세요: ")

        choices: list[str] = []
        for number in range(1, 5):
            choices.append(self.ask_text(f"선택지 {number}: "))

        answer = self.ask_int("정답 번호 (1-4): ", 1, 4)
        hint = input("힌트 (선택, Enter로 건너뛰기): ").strip() or None
        self.quizzes.append(Quiz(question, choices, answer, hint))

        # 새 퀴즈는 다음 종료를 기다리지 않고 즉시 파일에 반영한다.
        if self.save_state():
            print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")
        else:
            print("\n⚠️ 퀴즈는 추가됐지만 파일 저장에 실패했습니다.")

    def show_quiz_list(self) -> None:
        """등록된 퀴즈의 번호와 문제만 출력한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def delete_quiz(self) -> None:
        """번호와 재확인을 거쳐 퀴즈 하나를 삭제하고 즉시 저장한다."""
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

    def show_score(self) -> None:
        """최고 기록과 최신 게임 히스토리 최대 5회를 구분해 출력한다."""
        print("\n" + "=" * 40)
        print("          📊 점수 및 기록 📊")
        print("=" * 40)
        print("[최고 기록]")

        if self.best_total == 0 and self.best_score == 0:
            print("🏆 최고 점수: 기록 없음")
        elif self.best_total == 0:
            print(f"🏆 최고 점수: {self.best_score}점")
            print("   (이전 저장 데이터에는 정답 수 정보가 없습니다.)")
        else:
            print(
                f"🏆 최고 점수: {self.best_score}점 "
                f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
            )

        print(f"\n[최근 게임 기록: 최근 5회 / 전체 {len(self.history)}회]")
        if not self.history:
            print("아직 진행한 게임 기록이 없습니다.")
        else:
            # 목록 끝에 새 기록을 추가하므로, 마지막 5개를 최신순으로 표시한다.
            for number, record in enumerate(reversed(self.history[-5:]), start=1):
                timestamp = record.get("timestamp", "시간 정보 없음")
                total = record.get("total", 0)
                correct = record.get("correct", 0)
                score = record.get("score", 0)
                print(
                    f"{number}. [{timestamp}] {total}문제 | "
                    f"{correct}문제 정답 | {score}점"
                )

        print("=" * 40)

    def save_state(self) -> bool:
        """현재 퀴즈 목록·상세 최고 기록·게임 히스토리를 저장한다."""
        return save_quiz_state(
            self.quizzes,
            self.best_score,
            best_correct=self.best_correct,
            best_total=self.best_total,
            history=self.history,
        )

    def load_state(self) -> None:
        """저장된 데이터를 불러오고, 실패하면 기본 퀴즈로 복구한다."""
        (
            self.quizzes,
            self.best_score,
            self.best_correct,
            self.best_total,
            self.history,
        ) = load_quiz_state(include_details=True, include_history=True)


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
