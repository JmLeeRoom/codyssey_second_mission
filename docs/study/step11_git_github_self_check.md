# 10-4. Git과 GitHub — 자가 점검 학습 노트

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "10. 학습 목표와 자가 점검" 아래 "10-4. Git과 GitHub" 7개 항목을 학습 자료로 재구성한 것입니다. [10-1. Python 기초](python_basics_self_check.md), [10-2. 클래스와 객체(OOP)](oop_self_check.md), [10-3. 파일 입출력과 JSON](file_io_json_self_check.md)에 이어지는 자가 점검 시리즈의 마지막 문서입니다.
>
> 모든 커밋 해시·메시지·병합 그래프는 이 저장소에서 `git log`로 직접 확인한 실제 값입니다. `--no-ff` 병합 그래프는 이 프로젝트의 실제 `0e84cc0`/`1181dea`/`5ba64a0` 병합 이력을 그대로 사용했습니다.

## 목차

- Git이 필요한 이유와 3단계 흐름
- 7개 명령어의 역할과 add·commit·push의 차이
- git clone과 git pull의 사용 시점
- --no-ff 병합과 브랜치 분리 작업

---

## Git이 필요한 이유와 3단계 흐름

### Git이 변경 이력을 관리하는 데 왜 필요한지 설명할 수 있다.

Git을 배우기 전에 흔히 쓰는 방식은 이런 식이다. `quiz.py`를 고치다가 혹시 몰라 `quiz_final.py`로 복사해두고, 또 고치다가 `quiz_final_진짜.py`를 만들고, 다음날 다시 손대면서 `quiz_final_진짜_수정.py`가 생긴다. 이 방식의 문제는 세 가지다.

1. **어떤 게 최신인지 파일 이름만으로는 알 수 없다.** `final`, `진짜`, `최종`이 세 번 겹치면 사람의 기억에 의존할 수밖에 없다.
2. **무엇이 왜 바뀌었는지 기록이 없다.** 두 파일을 열어서 한 줄씩 비교(diff)하지 않는 한, "이 버전에서 무슨 기능이 추가됐는지"는 알 도리가 없다.
3. **저장소 용량과 협업이 무너진다.** 파일마다 버전이 늘어날수록 폴더는 지저분해지고, 여러 사람이 동시에 작업하면 누구의 `final`이 진짜 최종인지 다툼이 생긴다.

Git은 이 문제를 "파일을 복사해서 버전을 남기는" 대신 "매 순간의 변경 내용을 하나의 스냅샷(커밋)으로 기록"하는 방식으로 해결한다. 실제로 이 프로젝트는 지금까지 아래처럼 **15개의 커밋**으로 시작부터 지금까지의 변경 이력을 하나도 잃지 않고 남겼다.

```text
* 8fa57e9 Docs: README 6대 항목 및 실행 화면 스크린샷 추가
* 2ce41a5 보너스 과제 5종
* 01e3921 Docs: README에 학습 회고 추가
* 5ca7c4d Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False), json 불러오기 및 파일 부재/손상 시 자동 복구 처리
* 677163a Feat: 퀴즈 추가 기능 및 입력 유효성 검사 구현, 퀴즈목록 조회 기능 구현, 최고점수 확인 기능 구현
*   0e84cc0 Merge: 퀴즈 풀기 기능 병합
|\
| * 1181dea Feat: 퀴즈 출제 및 정답 채점 기능 구현, 최고 점수 비교 및 갱신 로직 추가
|/
* 5ba64a0 Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현, 메인 루프 및 안전 종료 처리
* 6868c74 Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)
* 9d106fd Chore: 프로젝트 초기 설정 및 .gitignore 추가
* 001a6ff settingfinish
* ee25482 수정
* b25c749 update README.md
* 40582bc test
* d6877a1 first commit
```

파일 이름은 계속 `quiz.py`, `storage.py`, `README.md`로 **똑같다.** 대신 "6868c74에서 `Quiz` 클래스를 만들었고, 5ba64a0에서 `QuizGame` 골격을 얹었고, 677163a에서 유효성 검사를 추가했다"는 식으로 각 시점의 변화가 커밋 메시지와 함께 순서대로 남는다. 이러면 다음이 모두 가능해진다.

- 언제 어떤 기능이 들어왔는지 `git log`로 즉시 확인
- 특정 커밋 시점의 코드로 돌아가 비교(`git diff`)하거나 되돌리기
- `final_진짜.py` 같은 파일을 두지 않고도, 필요하면 과거 어느 시점의 상태든 재현

즉 Git은 "파일 여러 벌을 만들어 사람이 기억으로 버전을 관리하던 일"을, "커밋이라는 이력 단위로 기계가 정확하게 기록"하는 일로 바꿔준다. 이 프로젝트의 15개 커밋 하나하나가 바로 그 증거다.

**TL;DR: Git은 `final.py`, `final_진짜.py`식 파일 복사 대신, 이 프로젝트가 남긴 15개의 커밋처럼 "언제 무엇이 왜 바뀌었는지"를 스냅샷으로 정확히 기록해 이력 관리 문제를 해결한다.**

### 작업 디렉터리, 스테이징 영역, 로컬 저장소의 3단계 흐름을 설명할 수 있다.

Git으로 커밋 하나가 만들어지기까지, 변경 내용은 세 곳을 순서대로 거친다. 이걸 "원고 제출" 비유로 보면 이해가 쉽다.

| 단계 | 비유 | 실제 위치 | 상태 |
|---|---|---|---|
| ① 작업 디렉터리 (Working Directory) | 책상 위에서 원고를 고치는 중 | 프로젝트 폴더 자체 (`quiz.py`, `storage.py` 등) | 아직 아무것도 Git에 알리지 않은, 그냥 수정된 파일 |
| ② 스테이징 영역 (Staging Area) | "이번에 제출할 원고만" 봉투에 골라 담기 | `.git` 내부의 임시 색인(index) | `git add`로 선택된, 다음 커밋에 포함될 목록 |
| ③ 로컬 저장소 (Local Repository) | 봉투를 봉인하고 서랍(캐비닛)에 도장 찍어 보관 | `.git` 디렉터리 | `git commit`으로 확정된, 되돌릴 수 없는 이력 스냅샷 |

이 흐름을 이 프로젝트의 Step 0(프로젝트 초기 설정)에서 실제로 실행된 명령으로 그대로 따라가 보자.

```bash
git add .gitignore README.md
git commit -m "Chore: 프로젝트 초기 설정 및 .gitignore 추가"
git push -u origin main
```

**① 작업 디렉터리 — 파일을 고친다.** `.gitignore`를 새로 작성하고 `README.md`를 정리하는 작업 자체는 순수하게 프로젝트 폴더 안에서 일어난다. 이 시점에서는 아직 Git에게 "이걸 기록해줘"라고 말한 게 아니다. 그냥 텍스트 에디터로 파일을 고친 상태일 뿐이다.

**② 스테이징 영역 — `git add`로 골라 담는다.** `git add .gitignore README.md`는 폴더 안의 모든 변경을 무작정 다 넣는 게 아니라, **딱 이 두 파일만** 콕 집어서 스테이징 영역에 올리는 동작이다. 만약 그 시점에 다른 파일도 함께 수정 중이었다면(예: 아직 완성되지 않은 코드), 그 파일은 스테이징되지 않으므로 다음 커밋에 섞여 들어가지 않는다. 즉 `git add`는 "작업 디렉터리에 있는 모든 변경 중 이번 커밋에 포함시킬 것만 선별"하는 단계다.

**③ 로컬 저장소 — `git commit`으로 스냅샷을 확정한다.** `git commit -m "Chore: 프로젝트 초기 설정 및 .gitignore 추가"`는 방금 스테이징 영역에 올라온 내용(`.gitignore`, `README.md`의 변경분)을 하나의 커밋 객체로 묶어 `.git` 디렉터리에 영구히 기록한다. 이 커밋이 바로 커밋 그래프의 `9d106fd`다. 한번 커밋되면 그 시점의 스냅샷은 이후 작업 디렉터리에서 파일이 아무리 바뀌어도 그대로 보존된다.

정리하면 순서는 항상 **작업 디렉터리(수정) → 스테이징 영역(`git add`로 선별) → 로컬 저장소(`git commit`으로 확정)** 다. 참고로 `git push -u origin main`은 이 로컬 저장소의 커밋을 원격 저장소(GitHub)로 내보내는 그다음 단계이며, 3단계 흐름 자체(작업 디렉터리·스테이징·로컬 저장소)와는 별개로 로컬 저장소 이후에 선택적으로 이어지는 과정이다.

**TL;DR: 파일을 고치면 작업 디렉터리, `git add`로 이번 커밋에 포함할 것만 선별하면 스테이징 영역, `git commit`으로 그 내용을 하나의 스냅샷으로 확정하면 로컬 저장소(`.git`) — 이 프로젝트의 `git add .gitignore README.md` → `git commit -m "Chore: 프로젝트 초기 설정 및 .gitignore 추가"`가 그 순서를 그대로 보여준다.**

---

## 7개 명령어의 역할과 add·commit·push의 차이

### 7개 명령어 각각이 하는 일

Git 명령어를 처음 배우면 이름만 보고는 뭐가 뭔지 헷갈리기 쉽다. 이 7개를 하나의 비유로 묶어서 보면 이렇다: **git은 "버전이 기록되는 일기장"이고, 각 명령어는 그 일기장을 쓰고 공유하는 과정의 한 단계다.**

- `git init` — 새 폴더를 "이제부터 이 폴더의 변경 이력을 기록할게"라고 선언하는 것. 빈 노트를 사서 표지에 "일기장"이라고 적는 것과 같다.
- `git add` — 다음 기록에 무엇을 남길지 고르는 것. 오늘 있었던 일 중 일기에 쓸 내용을 메모지에 골라 옮겨두는 단계다. 아직 일기장(이력)에 적힌 건 아니다.
- `git commit` — 골라둔 내용을 실제로 펜으로 일기장에 적어넣는 것. 이 순간부터 그 변경사항은 로컬 이력에 영구히 남는다.
- `git push` — 내가 쓴 일기장을 통째로 복사해서 클라우드(GitHub)에 업로드하는 것. 내 컴퓨터 안에서만 존재하던 기록이 비로소 원격 저장소에도 남는다.
- `git pull` — 클라우드에 올라온 최신 내용을 내 컴퓨터로 받아와 합치는 것. push의 반대 방향이다.
- `git checkout` — 여러 갈래(브랜치)의 이야기 중 하나를 골라 그 버전으로 이동하는 것.
- `git clone` — 남의 일기장(원격 저장소) 전체를 통째로 복사해서 내 로컬 저장소로 만드는 것. `git init` + `git remote add origin` + 첫 `git pull`을 한 번에 해주는 셈이다.

이걸 이 프로젝트 로그에서 실제로 쓰인 형태로 정리하면 다음과 같다.

| 명령어 | 역할 | 이 프로젝트에서 실제로 쓰인 형태 |
|---|---|---|
| `git init` | 폴더를 Git 저장소로 초기화 | 이 저장소의 커밋 로그(`d6877a1 first commit` 이후)만으로는 `git init`이 정확히 언제 실행됐는지 직접 확인되지 않는다. 저장소가 이미 만들어진 뒤부터 로그가 남아있기 때문이다. 이 항목은 지어내지 않고 정직하게 "로그로는 직접 확인 불가"라고 밝혀둔다. |
| `git add` | 다음 커밋에 포함할 파일을 스테이징 | `git add .gitignore README.md` |
| `git commit` | 스테이징된 내용을 로컬 이력에 기록 | `git commit -m "Chore: 프로젝트 초기 설정 및 .gitignore 추가"` |
| `git push` | 로컬 커밋을 원격(GitHub)으로 전송 | `git push -u origin main` (최초 push), `git push origin main` (이후 push) |
| `git pull` | 원격의 새 커밋을 로컬로 가져와 병합 | `git pull origin main` → `Updating 5ca7c4d..01e3921` `Fast-forward` |
| `git checkout` | 브랜치 전환 | `git checkout main` → `Switched to branch 'main'` |
| `git clone` | 원격 저장소를 통째로 복제 | `git clone https://github.com/JmLeeRoom/codyssey_second_mission.git quiz-clone` |

여기서 `git init`을 특히 정직하게 짚어야 하는 이유가 있다. 체크리스트가 요구하는 절차이고 실제로 이 저장소도 어딘가에서 반드시 `git init`을 거쳤겠지만, `git log`에 남는 건 "커밋"뿐이지 "초기화 명령을 실행했다"는 사실 자체는 아니다. 로그의 첫 커밋이 `d6877a1 first commit`이라는 것과 `git init`이 몇 시에 실행됐는지는 별개 정보다. 다만 `git remote -v` 결과 `origin`이 `https://github.com/JmLeeRoom/codyssey_second_mission.git`으로 정확히 연결되어 있다는 것은 확인되므로, `git init` 이후 어느 시점에 `git remote add origin <URL>`도 실행됐을 것이다 — 이 역시 정확한 실행 시점이 로그에 직접 남아있지는 않다. 반면 `git clone`으로 만든 `quiz-clone`은 `origin`이 자동으로 등록되어 있었다(`git remote -v` 결과 동일한 URL). 이것이 clone과 init+remote add의 실질적 차이다: clone은 원격 연결까지 한 번에 끝내주지만, init으로 새로 시작한 저장소는 원격 연결을 별도로 걸어줘야 한다.

`git checkout`도 실제 로그로 짚어보자. `feat/play-quiz` 브랜치에서 작업을 마친 뒤 `git checkout main`을 실행하자 `Switched to branch 'main'` / `Your branch is up to date with 'origin/main'.`이 출력됐다. 이렇게 브랜치를 옮긴 뒤 `git merge --no-ff feat/play-quiz`를 실행해 병합 커밋 `0e84cc0`을 만들었고, 그 결과가 `git log --oneline --graph`에서 `|\` `|/`로 갈라졌다 합쳐지는 모양으로 보인다.

**TL;DR: `git init`이 저장소를 만들고, `add`가 다음 커밋 내용을 고르고, `commit`이 로컬 이력에 기록하고, `push`/`pull`이 원격과 주고받고, `checkout`이 브랜치를 옮기고, `clone`이 원격 저장소를 통째로 복제해온다 — 단, 이 저장소에서 `git init` 실행 시점 자체는 로그로 직접 확인되지 않는다.**

### add·commit·push는 왜 세 단계로 나뉘어 있을까

세 명령어를 하나로 합치지 않고 굳이 나눠둔 이유는 "책임 범위"가 다르기 때문이다.

- **add vs commit**: `add`는 "다음 커밋에 무엇을 넣을지 고르는 것"이고, `commit`은 "그걸 실제로 이력에 남기는 것"이다. 장바구니에 물건을 담는 것(add)과 결제를 눌러서 주문을 확정하는 것(commit)의 차이라고 생각하면 된다. 담기만 하고 결제 안 하면 주문 기록에 안 남듯이, `add`만 하고 `commit`을 안 하면 그 변경사항은 아직 이력에 존재하지 않는다.
- **commit vs push**: `commit`은 "내 컴퓨터의 `.git` 폴더 안에만 기록되는 것"이고, `push`는 "그걸 실제로 `origin`(GitHub)까지 전송하는 것"이다. 일기장에 적는 것(commit)과 그 일기장을 클라우드에 업로드하는 것(push)의 차이다. commit까지만 하고 push를 안 하면, 그 기록은 내 컴퓨터에만 있고 GitHub에는 아직 존재하지 않는다.

이 프로젝트의 실제 로그로 두 경계를 각각 확인할 수 있다. 먼저 add와 commit의 경계다.

```bash
git add .gitignore README.md
git commit -m "Chore: 프로젝트 초기 설정 및 .gitignore 추가"
```

`git add`는 `.gitignore`와 `README.md`를 "다음 커밋 후보"로 올려놓았을 뿐이고, 그 다음 줄의 `git commit -m "..."`이 실행되고 나서야 `9d106fd`라는 실제 커밋 해시가 이력에 생겼다. `git log --oneline`에서 `9d106fd Chore: 프로젝트 초기 설정 및 .gitignore 추가`로 남아있는 게 바로 이 commit의 결과다.

commit과 push의 경계는 브랜치 병합 과정에서 더 뚜렷하게 드러난다.

```bash
$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

$ git merge --no-ff feat/play-quiz -m "Merge: 퀴즈 풀기 기능 병합"
Merge made by the 'ort' strategy.
 5 files changed, 650 insertions(+), 74 deletions(-)

$ git push origin main
...
   5ba64a0..0e84cc0  main -> main
```

`git merge --no-ff`가 실행되는 순간, 병합 커밋 `0e84cc0`은 이미 **내 로컬 `.git`에만** 만들어졌다. 이 시점에는 GitHub의 `origin/main`은 아직 옛날 상태(`5ba64a0`) 그대로다. 그다음 줄의 `git push origin main`이 실행되고 나서야 `5ba64a0..0e84cc0`라는 범위가 실제로 원격에 전송됐고, 그 결과가 `main -> main`으로 출력됐다. 즉 로컬에 커밋이 생기는 시점과 그 커밋이 GitHub에 반영되는 시점은 명백히 서로 다른 두 단계이며, 그 사이에는 얼마든지 시간차가 있을 수 있다(push를 깜빡하면 로컬 커밋은 존재해도 GitHub에는 영원히 안 올라간다).

같은 원리가 `git pull`에서도 반대 방향으로 나타난다. `quiz-clone`에서 커밋하고 push한 `01e3921`을 원본 저장소(`second-project`)에서 받아올 때는:

```bash
$ git pull origin main
Updating 5ca7c4d..01e3921
Fast-forward
 README.md | 4 ++++
 1 file changed, 4 insertions(+)
```

여기서도 "원격에 이미 존재하는 커밋"과 "내 로컬에 반영되는 시점"이 분리되어 있다는 걸 확인할 수 있다.

**TL;DR: add는 다음 커밋 후보를 고르는 것, commit은 로컬 `.git`에 역사로 남기는 것, push는 그 역사를 origin(GitHub)까지 실제로 전송하는 것 — 세 단계는 각각 별도로 실행해야 하며, 실제 로그의 `5ba64a0..0e84cc0` 전송 시점이 그 commit(로컬)과 push(원격) 사이의 경계를 그대로 보여준다.**

---

## git clone과 git pull의 사용 시점

### git clone과 git pull의 사용 시점 차이를 설명할 수 있다.

`git clone`과 `git pull`은 둘 다 "원격 저장소의 내용을 로컬로 가져온다"는 점에서는 비슷해 보이지만, 정확히 언제 쓰는 명령인지를 가르는 기준은 단 하나입니다 — **로컬에 그 저장소가 이미 있는가, 없는가**입니다. 이사에 비유하면 이해하기 쉽습니다. `git clone`은 아직 살아본 적 없는 동네에 처음 이삿짐을 통째로 옮기는 것이고, `git pull`은 이미 살고 있는 집에 택배로 새로 온 물건만 받아 채워 넣는 것입니다. 처음 살 집에 굳이 "어제 도착한 택배만" 받으러 갈 수는 없고(아직 그 집 자체가 없으므로), 이미 살고 있는 집을 매번 통째로 다시 지을 필요도 없습니다.

이 프로젝트의 Step 6 실습이 이 차이를 정확히 보여줍니다. `~/Project`(second-project의 상위 폴더)에는 아직 `quiz-clone`이라는 디렉터리 자체가 존재하지 않는 상태였습니다. 이 상태에서 실행한 명령이 `git clone`입니다.

```bash
$ git clone https://github.com/JmLeeRoom/codyssey_second_mission.git quiz-clone
$ cd quiz-clone
$ git log --oneline
5ca7c4d (HEAD -> main, origin/main, origin/HEAD) Feat: state.json 저장 기능 구현 ...
...
d6877a1 first commit
```

`git clone`은 `quiz-clone`이라는 디렉터리를 새로 만들면서, 원격 저장소가 가진 커밋 이력 전체(`d6877a1`부터 `5ca7c4d`까지, `main` 브랜치에 있던 12개 이상의 커밋)를 한꺼번에 받아옵니다. 심지어 원격 연결(`origin`)까지 자동으로 준비해 줍니다.

```bash
$ git remote -v
origin  https://github.com/JmLeeRoom/codyssey_second_mission.git (fetch)
origin  https://github.com/JmLeeRoom/codyssey_second_mission.git (push)
```

즉 `git clone`은 "빈 폴더 → 완전한 저장소(파일 + 전체 이력 + 원격 연결)"를 한 번에 만드는, **처음 한 번만 쓰는** 명령입니다.

반면 `git pull`은 정반대 상황에서 씁니다. `quiz-clone`에서 회고를 추가해 커밋하고 push한 뒤(`5ca7c4d..01e3921 main -> main`), 원래 작업하던 `second-project` 디렉터리로 돌아왔을 때를 생각해 보겠습니다. `second-project`는 이미 완전한 저장소이고, 로컬 `main`은 여전히 `5ca7c4d`를 가리키고 있는데 원격(`origin/main`)에는 그보다 한 커밋 앞선 `01e3921`이 이미 올라와 있는 상태입니다. 이럴 때 저장소를 통째로 다시 받을 필요는 없고, "달라진 부분만" 반영하면 됩니다. 그래서 실행한 명령이 `git pull`입니다.

```bash
$ git pull origin main
...
Updating 5ca7c4d..01e3921
Fast-forward
 README.md | 4 ++++
 1 file changed, 4 insertions(+)
```

로그의 `Updating 5ca7c4d..01e3921`이라는 표현이 핵심입니다. 저장소 전체를 다시 만든 것이 아니라, 로컬이 이미 갖고 있던 `5ca7c4d`를 기준점 삼아 그 뒤에 새로 생긴 `01e3921` 구간의 차이(이 경우 `README.md`에 4줄 추가)만 반영했습니다. `Fast-forward`라는 표시는 로컬 `main`이 그 사이에 독자적으로 앞서 나간 커밋이 하나도 없어서, 그저 포인터를 `01e3921`로 밀어 올리기만 하면 충돌 없이 이력이 이어진다는 뜻입니다. `git clone`이 "0에서 통째로 시작"이라면, `git pull`은 "이미 아는 지점 이후의 차이만 갱신"인 셈입니다.

이 대비는 원격 연결이 언제, 어떻게 만들어지는지에서도 드러납니다. Step 0에서 `second-project`를 처음 GitHub에 올릴 때는 저장소를 만든 뒤 원격을 손으로 연결하는 절차(`git remote add origin <URL>`)가 필요했고, 로컬 `main`과 `origin/main` 사이의 추적(upstream) 관계도 저절로 생기지 않았습니다. 그래서 최초 push는 `-u`(`--set-upstream`) 옵션을 반드시 함께 써야 했습니다.

```bash
git push -u origin main
```

이 `-u` 덕분에 로컬 `main`이 `origin/main`을 추적하도록 한 번 등록되고 나면, 그 뒤로는 옵션 없이 `git push`나 `git pull`만 써도 Git이 어디로 보내고 어디서 받아야 할지 스스로 압니다. `quiz-clone`은 처음부터 `git clone`으로 만들어졌으므로 이 추적 관계가 clone 시점에 자동으로 이미 설정되어 있었습니다. 그래서 Step 6에서 `quiz-clone`이 push할 때는

```bash
git push origin main
```

처럼 `-u` 없이도 곧바로 동작했습니다. `git remote add`와 `-u`를 손으로 챙겨야 했던 Step 0의 최초 push와, 그런 절차 없이 바로 push가 된 Step 6의 차이는 결국 "저장소를 어떻게 시작했는가"(직접 `init` vs `clone`)의 차이에서 비롯된 것입니다.

마지막으로 짚어야 할 것은, `git clone`을 반복해서 쓰면 안 되는 이유입니다. `quiz-clone`에 이미 반영된 변경 사항을 다시 최신 상태로 맞추고 싶다고 해서 그 자리에서 또 `git clone`을 실행하는 것은 좋은 습관이 아닙니다. `git clone`은 실행할 때마다 새 디렉터리를 만들며 이력 전체를 처음부터 다시 내려받기 때문에 비효율적일 뿐 아니라, 같은 이름의 디렉터리에 다시 clone을 시도하면 이미 그 안에서 작업 중이던 내용(아직 커밋하지 않은 변경 등)과 충돌하거나 덮어써질 위험도 있습니다. `quiz-clone`처럼 이미 만들어진 저장소 안에서 원격의 새 커밋을 따라잡고 싶을 때는, `second-project`에서 그랬듯 그 디렉터리 안에서 `git pull`만 반복해서 쓰면 됩니다. 정리하면 **`git clone`은 저장소당 딱 한 번, `git pull`은 그 뒤로 필요할 때마다** 쓰는 명령입니다.

**TL;DR: `git clone`은 로컬에 저장소가 아예 없을 때 딱 한 번 실행해 전체 이력과 origin 연결까지 한꺼번에 새로 만드는 명령(`quiz-clone` 생성, `d6877a1`~`5ca7c4d` 전체 이력 + upstream 자동 설정으로 이후 push에 `-u` 불필요)이고, `git pull`은 이미 있는 저장소에서 원격에 새로 생긴 커밋과의 차이만 반영하는 명령(`second-project`의 `git pull origin main` → `Updating 5ca7c4d..01e3921` Fast-forward)이며, 이미 만들어진 저장소를 다시 받을 때 `clone`을 반복하면 비효율적이고 덮어쓰기 위험도 있으므로 그 안에서는 `pull`만 반복해서 쓴다.**

---

## --no-ff 병합과 브랜치 분리 작업

### --no-ff 병합이 그래프에 병합 지점을 남기는 이유를 설명할 수 있다.

이 프로젝트의 실제 커밋 그래프(`git log --oneline --graph --all --decorate`)를 보면 다음 부분이 눈에 띈다.

```
* 0e84cc0   Merge: 퀴즈 풀기 기능 병합
|\
| * 1181dea (origin/feat/play-quiz, feat/play-quiz) Feat: 퀴즈 출제 및 정답 채점 기능 구현 ...
|/
* 5ba64a0 Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현 ...
```

`5ba64a0`에서 그래프가 `|\` 모양으로 갈라졌다가 `|/` 모양으로 다시 합쳐지는 이 마름모꼴이, `--no-ff` 병합이 만들어내는 시각적 흔적이다. 실제로 이 병합을 만든 명령은 다음과 같았다.

```bash
$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

$ git merge --no-ff feat/play-quiz -m "Merge: 퀴즈 풀기 기능 병합"
Merge made by the 'ort' strategy.
 5 files changed, 650 insertions(+), 74 deletions(-)
```

`--no-ff`는 "no fast-forward"의 줄임말로, 직역하면 "빨리 감기 금지"다. 이걸 이해하려면 먼저 fast-forward(줄여서 ff) 병합이 무엇인지 알아야 한다. `feat/play-quiz` 브랜치는 `5ba64a0`에서 갈라져 나가 `1181dea` 커밋 하나만 추가로 쌓은 상태였다. 이때 `main`은 `feat/play-quiz`가 갈라진 뒤로 새 커밋이 하나도 없었다(`main`도 여전히 `5ba64a0`에 머물러 있었다). 이런 상황에서는 사실 병합이랄 것도 없이, `main`이라는 이름표(포인터)를 `5ba64a0`에서 `1181dea`로 그냥 옮기기만 해도 두 브랜치의 내용이 완전히 일치하게 된다. 이게 바로 fast-forward다 — 새로운 커밋을 만들지 않고 포인터만 앞으로 "빨리 감는" 것이다. 만약 `--no-ff` 없이 그냥 `git merge feat/play-quiz`를 실행했다면, Git은 이 조건(중간에 새 커밋 없음)을 확인하고 자동으로 fast-forward를 선택했을 것이고, 그 결과 그래프는 `5ba64a0 → 1181dea`로 이어지는 일직선이 되어 `0e84cc0`이라는 병합 커밋 자체가 아예 생기지 않았을 것이다.

여기서 붕어빵 틀 비유를 다시 빌려오면 이해하기 쉽다. fast-forward는 책갈피(브랜치 포인터)를 페이지만 넘겨서 다음 장으로 옮기는 것과 같다 — 책 내용에는 아무 변화도, 표시도 남지 않는다. 반면 `--no-ff`는 "여기서 다른 이야기 갈래가 하나 있었고, 지금 이 지점에서 본편과 합쳐졌다"는 것을 책 속에 굵은 글씨로 못박아 두는 것과 같다. `--no-ff`는 fast-forward가 가능한 상황이어도 그 지름길을 쓰지 않고, 강제로 부모가 둘인 새로운 커밋(`0e84cc0`)을 만든다. `git log --graph`가 `0e84cc0`에 부모 커밋 두 개(`main` 쪽의 `5ba64a0`와 `feat/play-quiz` 쪽의 `1181dea`)를 모두 연결해서 그리기 때문에, 그래프에는 자연히 갈라졌다 합쳐지는 마름모 모양이 남는다. 즉 병합 지점이 그래프에 남는 이유는 "병합 커밋이 부모를 두 개 가지고 있고, `--no-ff`가 그 병합 커밋의 생성 자체를 강제하기 때문"이다.

이 흔적이 왜 유용한가 하면, `0e84cc0`이라는 커밋 하나만 보면 "언젠가 `feat/play-quiz`라는 이름의 작업이 여기서 `main`에 합류했다"는 사실을 그래프만으로 영구히 확인할 수 있기 때문이다. 만약 fast-forward로 처리됐다면 `1181dea`는 그냥 `main` 위에 찍힌 평범한 커밋 하나로만 보였을 것이고, "이게 별도 브랜치에서 작업된 기능이었다"는 맥락은 커밋 메시지를 일일이 읽지 않는 한 그래프에서 사라졌을 것이다.

**TL;DR: `main`에 그 사이 새 커밋이 없어 사실은 fast-forward(포인터만 이동, 일직선 그래프)로도 처리될 수 있었던 상황을, `--no-ff`가 강제로 막고 부모가 둘인 병합 커밋 `0e84cc0`을 만들어서 "`feat/play-quiz`에서 작업이 있었다"는 사실이 `|\ ... |/` 모양으로 그래프에 영구히 남는다.**

### 브랜치를 나눠 작업하는 장점과 혼자 하는 프로젝트에도 필요한 이유를 설명할 수 있다.

이 프로젝트에서 실제로 있었던 시나리오를 그대로 따라가 보자. 퀴즈 출제와 정답 채점 기능을 만들 때, 곧바로 `main`에서 작업하지 않고 `feat/play-quiz`라는 별도 브랜치를 만들어 그 위에서 작업했다.

```bash
$ git push -u origin feat/play-quiz
...
 * [new branch]      feat/play-quiz -> feat/play-quiz
branch 'feat/play-quiz' set up to track 'origin/feat/play-quiz'.
```

이 브랜치 위에서 `1181dea`(퀴즈 출제 및 정답 채점 기능 구현, 최고 점수 비교 및 갱신 로직 추가) 커밋이 쌓이는 동안, `main`은 계속 `5ba64a0` 상태 그대로 안정적으로 유지됐다. 새 기능이 절반쯤 완성된 불안정한 코드가 `main`에 섞여 들어갈 일이 없었다는 뜻이다. 작업이 끝난 뒤에야 `git checkout main` → `git merge --no-ff feat/play-quiz`로 한 번에, 완성된 형태로만 `main`에 합류시켰다. 이것이 브랜치를 나눠 작업하는 핵심 장점이다 — **"만들고 있는 중"인 상태와 "완성돼서 믿고 써도 되는" 상태를 물리적으로 분리할 수 있다.**

그렇다면 협업자가 없는 혼자만의 프로젝트에서도 이게 왜 필요할까? 두 가지 이유를 이 프로젝트 자체에서 찾을 수 있다.

첫째는 **안전망(되돌리기 쉬움)** 이다. 만약 `feat/play-quiz`에서 시도한 채점 로직이 잘못됐거나 마음에 들지 않았다면, `main`은 여전히 `5ba64a0` 그대로 멀쩡했을 것이므로 `feat/play-quiz` 브랜치만 지워버리고 처음부터 다시 시도할 수 있었다. 협업자가 없어도 "지금의 나"와 "실험 중인 나"를 분리해두면, 실험이 실패해도 본체(`main`)는 다치지 않는다. 브랜치를 나누지 않고 `main`에서 바로 이것저것 시도했다면, 실패한 시도의 흔적을 되돌리기 위해 커밋을 하나하나 되짚거나 `git reset` 같은 더 위험한 명령을 써야 했을 것이다.

둘째는 **이력 관리(나중에 한눈에 파악하기)** 이다. `git log --graph --all`로 전체 이력을 보면, `0e84cc0`이 갈라졌다 합쳐지는 지점 덕분에 "퀴즈 풀기 기능이 정확히 어디서 시작해서 어디서 끝났는지"가 그래프만 보고도 파악된다. 몇 달 뒤 이 프로젝트를 다시 열어봤을 때 "퀴즈 출제/채점 기능이 언제, 얼마만큼의 작업 범위로 만들어졌는가"를 기억에 의존하지 않고 그래프에서 바로 확인할 수 있다는 것은, 혼자 하는 프로젝트라도 무시할 수 없는 이점이다.

여기에 더해 흥미로운 사례가 하나 있다. 저장소를 새로 clone한 `quiz-clone`에서 `git branch -a`를 실행하면, 로컬 브랜치는 `main` 하나뿐이고 `feat/play-quiz`는 `remotes/origin/feat/play-quiz`라는 **원격 추적 브랜치**로만 존재했다(로컬로 체크아웃된 `feat/play-quiz`는 없었다). 이미 `main`에 병합이 끝난 기능 브랜치는, 다른 사람(또는 다른 clone)의 입장에서는 굳이 직접 작업할 대상이 아니라 "이런 이름의 작업이 있었다"는 **참고용 이력**으로만 남는다는 것을 잘 보여준다. clone은 원격의 모든 브랜치 레퍼런스를 가져오지만, 그중 실제로 체크아웃해서 작업할 브랜치는 기본 브랜치(`main`) 하나뿐이라는 점도 이와 맞닿아 있다.

**TL;DR: `feat/play-quiz`처럼 기능을 별도 브랜치에서 작업하면 완성 전까지 `main`을 안정 상태로 유지할 수 있고, 혼자 하는 프로젝트에서도 실패한 시도를 브랜치째 버릴 수 있는 안전망과 `git log --graph --all`로 작업 범위를 한눈에 되짚어볼 수 있는 이력 관리 이점을 동시에 얻을 수 있으며, 병합이 끝난 기능 브랜치는 `quiz-clone`의 사례처럼 다른 clone에서는 원격 추적 브랜치로만 남는 참고용 이력이 된다.**

---

## 참고 문서

- [10-1. Python 기초](python_basics_self_check.md)
- [10-2. 클래스와 객체(OOP)](oop_self_check.md)
- [10-3. 파일 입출력과 JSON](file_io_json_self_check.md)
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
