# Step 6 학습 노트 — clone과 pull 실습

> 이 문서는 [`docs/learning_checklist.md`](../learning_checklist.md)의 "7. Step 6 — clone과 pull 실습" 체크리스트를 바탕으로, 별도 디렉터리에 저장소를 복제하고 그 변경을 원본으로 가져오는 과정이 왜 이렇게 동작하는지 풀어 쓴 학습 자료입니다. [Step 0](step0_dev_environment_git_init.md) → [Step 1](step1_quiz_model.md) → [Step 2](step2_quizgame_menu.md) → [Step 3](step3_play_quiz_branch.md) → [Step 4](step4_add_list_score.md) → [Step 5](step5_state_persistence.md)에 이어지는 시리즈의 여덟 번째 문서입니다.
>
> 이 문서는 실제 `quiz-clone`/`second-project` 두 디렉터리의 상태와, 이 저장소에서 직접 확인한 명령 결과·터미널 로그를 근거로 작성했습니다. 이번 Step은 특히 지금까지의 문서들과 자연스럽게 이어집니다 — Step 0에서 배운 `git remote add`·`-u` 옵션이 `git clone`에서는 왜 필요 없는지, `.gitignore`가 clone 시점에도 그대로 효력을 발휘하는지, 그리고 사용자가 직접 남긴 학습 회고가 Step 5에서 배운 내용을 정확히 요약하고 있다는 것까지 확인합니다.

## 목차

- 7-1. 복제본 만들기
- 7-2. 복제본 변경을 원본으로 가져오기

---

## 7-1. 복제본 만들기

### 왜 하필 "상위 폴더"로 이동한 뒤 clone 하는가

체크리스트의 첫 항목은 "퀴즈 게임 개발과 핵심 push가 끝난 뒤 상위 폴더로 이동한다"입니다. 이 프로젝트에서는 `second-project`의 상위 폴더인 `~/Project`로 이동한 뒤, 그 안에 `quiz-clone`이라는 이름으로 복제본을 만들었습니다. 그 결과 `~/Project` 안에는 `quiz-clone`, `second-project`, (이 실습과 무관한) `swhs_dashboard` 세 개의 디렉터리가 형제 관계로 나란히 놓입니다.

여기서 "왜 굳이 상위 폴더로 나가야 하는가"가 중요합니다. 만약 `second-project` 내부, 예를 들어 `second-project/quiz-clone`처럼 clone을 실행했다면 어떻게 될까요? `git clone`은 대상 폴더 안에 `.git` 디렉터리를 새로 만들어 완전한 하나의 Git 저장소를 통째로 구성합니다. 그런데 `second-project` 자체가 이미 `.git`을 가진 Git 저장소이므로, 그 안에 또 다른 완전한 Git 저장소가 들어가는 **Git 저장소 안에 Git 저장소가 중첩된 구조**가 되어 버립니다. 이렇게 되면 상위 저장소 입장에서는 `quiz-clone` 폴더를 일반 파일들의 묶음으로 볼지, 서브모듈로 볼지 애매한 상태가 되고, `git status`나 `git add` 같은 기본 명령이 예상치 못하게 동작해 학습자를 혼란스럽게 만들 수 있습니다. 그래서 복제본은 원본 저장소 바깥, 즉 상위 폴더에 형제 디렉터리로 만드는 것이 올바른 습관입니다.

### clone 전에 git status와 push를 먼저 확인하는 이유

체크리스트의 두 번째 항목은 "clone 전 원본에서 git status를 확인하고, 필요한 커밋을 원격에 git push한 상태인지 확인한다"입니다. 이 순서가 중요한 이유는 `git clone`의 동작 원리 때문입니다. `git clone <URL>`은 **로컬 작업 디렉터리를 복사하는 명령이 아니라, 지정한 URL의 원격 저장소(GitHub) 안에 실제로 존재하는 내용만을 그대로 내려받는 명령**입니다. 즉 원본 폴더에 커밋되지 않은 변경 사항이 남아 있거나, 커밋은 했지만 아직 `git push`로 원격에 올리지 않은 로컬 커밋이 있다면, 그 내용은 clone 결과물에 전혀 포함되지 않습니다. clone 직전에 `git status`로 작업 디렉터리가 깨끗한지 확인하고, 최신 커밋까지 push가 끝났는지 점검하는 것은 이 원리를 실습으로 확인하는 과정입니다.

### git clone 실행과 결과 확인

```bash
cd ~/Project
git clone https://github.com/JmLeeRoom/codyssey_second_mission.git quiz-clone
cd quiz-clone
ls -al
```

복제본 안의 파일 목록을 확인하면 다음과 같이 나타납니다.

```
docs  .git  .gitignore  main.py  quiz.py  README.md  storage.py
```

여기서 눈여겨봐야 할 것은 목록에 **`state.json`이 없다**는 점입니다. `state.json`은 Step 0에서 `.gitignore`에 등록해 두었고, 그 이후로 단 한 번도 Git이 추적한 적이 없는 파일입니다. 원본 저장소(`second-project`)의 로컬 디스크에는 실제로 게임을 실행하며 생성된 `state.json`이 존재하지만, 그 파일은 커밋 이력 어디에도 기록된 적이 없으므로 clone이 가져올 대상 자체가 아닙니다. `git clone`은 "Git이 추적하는 파일과 커밋 이력"만 그대로 복제할 뿐, 무시된 파일이나 `__pycache__` 같은 캐시 디렉터리는 원본에 아무리 남아 있어도 복제본에는 나타나지 않습니다. 이는 `.gitignore`가 실제로 어떤 효과를 내는지를 clone이라는 별도의 시점에서 다시 한번 검증해 주는 셈입니다.

### git log --oneline — 이력은 "정리"되지 않고 있는 그대로 복제된다

```bash
git log --oneline
```

```
5ca7c4d (HEAD -> main, origin/main, origin/HEAD) Feat: state.json 저장 기능 구현 ...
677163a Feat: 퀴즈 추가 기능 및 입력 유효성 검사 구현 ...
0e84cc0 Merge: 퀴즈 풀기 기능 병합
1181dea (origin/feat/play-quiz) Feat: 퀴즈 출제 및 정답 채점 기능 구현 ...
5ba64a0 Feat: QuizGame 클래스 골격 및 공통 입력 검증 헬퍼 구현 ...
6868c74 Feat: Quiz 클래스 구현 (문제 출력/정답 확인/딕셔너리 변환)
9d106fd Chore: 프로젝트 초기 설정 및 .gitignore 추가
001a6ff settingfinish
ee25482 수정
b25c749 update README.md
40582bc test
d6877a1 first commit
```

원본 저장소의 12개 커밋 전체가 순서와 해시까지 그대로 복제되었습니다. 여기에는 이 시리즈 문서에서 지금까지 짚어 왔던 커밋 메시지의 흠도 예외 없이 포함되어 있습니다 — 코드 변경 없이 메시지만 남은 `677163a`, "저장 불러오기"가 "son 불러오기"로 잘린 오타가 있는 `5ca7c4d`가 그대로 보입니다. 이 부분에서 얻을 수 있는 교훈은 명확합니다. **clone은 이력을 깨끗하게 정리해 주는 기능이 아니라, 있는 그대로 완전히 복사하는 기능**입니다. 커밋 메시지를 신중하게 작성해야 하는 이유가 여기서도 다시 확인됩니다 — 한 번 원격에 올라간 이력은 clone을 거쳐도 고쳐지지 않고 계속 따라다닙니다.

또한 로그에서 `1181dea` 줄에만 `(origin/feat/play-quiz)`라는 표시가 붙어 있는 것을 눈여겨볼 필요가 있습니다. `git branch -a`로 확인해 보면 다음과 같습니다.

```
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/feat/play-quiz
  remotes/origin/main
```

로컬 브랜치는 `main` 하나뿐이고, `feat/play-quiz`는 로컬 브랜치가 아니라 `remotes/origin/feat/play-quiz`라는 **원격 추적 브랜치(remote-tracking branch)**로만 존재합니다. 즉 `git clone`은 원격 저장소가 가진 모든 브랜치의 참조 정보는 전부 가져오지만, 실제로 작업 디렉터리에 체크아웃해 두는 것은 기본 브랜치(main) 하나뿐입니다. `feat/play-quiz` 브랜치의 내용을 직접 수정하고 싶다면 `git checkout feat/play-quiz`처럼 별도로 로컬 추적 브랜치를 만들어야 합니다.

### git remote -v — origin이 자동으로 등록된다

```bash
git remote -v
```

```
origin  https://github.com/JmLeeRoom/codyssey_second_mission.git (fetch)
origin  https://github.com/JmLeeRoom/codyssey_second_mission.git (push)
```

Step 0에서는 `git init`으로 빈 저장소를 만든 뒤, `git remote add origin <URL>`이라는 명령을 손으로 직접 실행해서 원격 저장소를 연결해야 했습니다. 반면 `git clone <URL>`은 그 URL 자체를 원본 원격 저장소로 인식해 `origin`이라는 이름으로 자동 등록해 줍니다. 즉 clone은 파일과 이력뿐 아니라 원격 연결 설정까지 한 번에 준비해 주는 명령이라는 점에서, `git init` + `git remote add` 조합보다 한 단계 더 편리한 시작점을 제공합니다.

### 체크리스트는 [ ]지만, 이미 전부 검증되었다

이 섹션의 체크리스트 항목 7개는 현재 `docs/learning_checklist.md`에 모두 `[ ]`로 남아 있습니다. 하지만 위에서 인용한 실제 터미널 로그 — 상위 폴더 이동, `ls -al` 결과에서 `state.json`이 빠진 것, 12개 커밋이 그대로 담긴 `git log --oneline`, `origin`이 자동 등록된 `git remote -v` — 를 그대로 대조해 보면 이 항목들은 이미 전부 실제로 수행되었고 예상대로 동작했음이 확인됩니다. 남은 것은 체크리스트 파일에 체크 표시(`[x]`)를 반영하는 것뿐입니다.

---

## 7-2. 복제본 변경을 원본으로 가져오기

### 회고를 작성하고 복제본에서 커밋하기

7-1에서 만든 `quiz-clone`은 원본과 완전히 동일한 히스토리를 가진 별도의 작업 디렉터리입니다. 이 디렉터리 안에서 `README.md`를 직접 수정하고 커밋해도, 그 변경이 원본(`second-project`)에 자동으로 반영되지는 않습니다. Git 저장소 세 곳(로컬 복제본의 작업 디렉터리, 원격 GitHub 저장소, 로컬 원본의 작업 디렉터리)은 각자 독립된 상태를 가지고 있고, 그 사이를 이어주는 것은 오직 `push`와 `pull`이라는 명시적인 명령뿐입니다. 이번 섹션은 바로 이 "복제본 → 원격 → 원본"으로 이어지는 흐름 전체를 다룹니다.

사용자가 실제로 `quiz-clone/README.md`에 추가한 내용은 다음과 같습니다.

```markdown
## 학습 회고

`Path(__file__).resolve().parent`로 저장 경로를 계산해 실행 위치가 달라도 같은 `state.json`을 사용하도록 구현하며 상대 경로의 위험성을 배웠습니다. 또한 JSON 문법 오류나 필수 키 누락 시 파일을 `.bak`으로 백업하고 기본 데이터로 복구하는 흐름을 만들며, 예외 처리와 데이터 복구의 중요성을 경험했습니다.
```

이 문단을 눈여겨볼 필요가 있습니다. 내용을 그대로 보면, Step 5 문서에서 다뤘던 `STATE_FILE = Path(__file__).resolve().parent / "state.json"`이라는 경로 계산 방식과, JSON 손상 시 `.bak` 백업 후 기본 데이터로 복구하는 4대 복구 경로를 사용자가 스스로 요약해서 적어 놓은 것입니다. 즉 이 회고는 형식적으로 채운 문장이 아니라, 앞선 Step에서 배운 개념을 실제로 소화해 자기 언어로 다시 말할 수 있게 됐다는 증거입니다.

이 변경을 커밋한 로그는 다음과 같습니다.

```bash
$ git add .
$ git commit -m "Docs: README에 학습 회고 추가"
[main 01e3921] Docs: README에 학습 회고 추가
 1 file changed, 4 insertions(+)
```

체크리스트에는 `git add README.md`로 안내되어 있지만 실제로는 `git add .`이 실행되었습니다. 이번 경우 변경된 파일이 `README.md` 하나뿐이었기 때문에 결과는 같지만, 여러 파일을 동시에 손대는 상황이라면 의도치 않은 파일까지 스테이징될 수 있으므로 `git status`로 무엇이 올라가는지 항상 확인하는 습관이 중요합니다. 이 커밋이 체크리스트가 말하는 "커밋 #16"입니다.

### -u 없이 push해도 문제없는 이유

```bash
$ git push origin main
...
To https://github.com/JmLeeRoom/codyssey_second_mission.git
   5ca7c4d..01e3921  main -> main
```

Step 0에서는 `git init`으로 새 저장소를 만든 뒤 `git remote add origin <URL>`로 원격을 손으로 등록하고, 처음 push할 때 `git push -u origin main`처럼 `-u`(`--set-upstream`) 옵션을 줘서 로컬 `main`이 `origin/main`을 추적하도록 명시적으로 연결해야 했습니다. 이 연결이 없으면 Git은 `git push`만 입력했을 때 어디로 보내야 할지 알 수 없습니다.

반면 `quiz-clone`은 `git clone`으로 만들어졌고, FACTS 5)에서 확인했듯 `git clone`은 원격 저장소 URL을 자동으로 `origin`이라는 이름으로 등록해 줍니다. 이때 함께 만들어지는 로컬 `main` 브랜치도 `origin/main`을 추적하도록 자동으로 upstream이 설정됩니다. 그래서 `quiz-clone`에서는 `-u` 없이 `git push origin main`만 실행해도, 심지어 `origin main`도 생략한 `git push` 한 마디만으로도 문제없이 동작합니다. 즉 Step 0의 `-u`는 "처음으로 추적 관계를 만드는" 작업이었고, 이번 push는 clone 시점에 이미 그 관계가 만들어져 있었기 때문에 별도 설정이 필요 없었던 것입니다.

### 원래 작업 디렉터리로 돌아가 pull하기

push가 끝났다면 GitHub 웹의 저장소 페이지에서 커밋 이력에 `01e3921 Docs: README에 학습 회고 추가`가 올라와 있고, `README.md` 파일을 열어 보면 회고 문단이 실제로 추가돼 있는 것을 확인할 수 있습니다. 이제 `cd ..`(또는 절대 경로)로 `quiz-clone`을 빠져나와 원본 작업 디렉터리인 `second-project`로 돌아갑니다.

pull을 실행하기 전에, 원본의 `README.md`가 아직 회고를 모르는 상태라는 것을 먼저 눈으로 확인해 둡니다.

```
$ tail -n 5 README.md
## 참고 문서

- [README 작성 요구사항](docs/readme_requirements_list.md)
- [학습 가이드](docs/learning_guide.md)
- [원본 과제 명세](docs/reference.md)
```

이제 `git pull origin main`을 실행합니다.

```bash
$ git pull origin main
remote: Enumerating objects: 5, done.
...
From https://github.com/JmLeeRoom/codyssey_second_mission
 * branch            main       -> FETCH_HEAD
   5ca7c4d..01e3921  main       -> origin/main
Updating 5ca7c4d..01e3921
Fast-forward
 README.md | 4 ++++
 1 file changed, 4 insertions(+)
```

pull이 끝난 뒤 `git log -3 --oneline`과 `tail -n 5 README.md`로 다시 확인합니다.

```
$ git log -3 --oneline
01e3921 (HEAD -> main, origin/main) Docs: README에 학습 회고 추가
5ca7c4d Feat: state.json 저장 기능 구현 (UTF-8, ensure_ascii=False), son 불러오기 및 파일 부재/손상 시 자동 복구 처리
677163a Feat: 퀴즈 추가 기능 및 입력 유효성 검사 구현 퀴즈목록 조회 기능 구현 최고점수 확인 긴으 구현

$ tail -n 5 README.md
- [원본 과제 명세](docs/reference.md)

## 학습 회고

`Path(__file__).resolve().parent`로 저장 경로를 계산해 실행 위치가 달라도 같은 `state.json`을 사용하도록 구현하며 상대 경로의 위험성을 배웠습니다. 또한 JSON 문법 오류나 필수 키 누락 시 파일을 `.bak`으로 백업하고 기본 데이터로 복구하는 흐름을 만들며, 예외 처리와 데이터 복구의 중요성을 경험했습니다.
```

`quiz-clone`에서 만들었던 회고 문단이 `second-project`의 `README.md` 끝에 그대로 붙어 있고, `git log`의 최상단도 `01e3921`로 바뀌어 있습니다. `quiz-clone`이라는 완전히 다른 디렉터리에서 작성·커밋·push한 내용이, GitHub 원격 저장소를 경유해 `second-project`라는 또 다른 디렉터리로 정확히 옮겨 온 것입니다. 실제로 지금 이 저장소를 직접 확인해도 `git log -1`은 `01e3921(HEAD -> main, origin/main)`이고 `README.md`에는 위와 동일한 회고가 들어 있습니다.

### "Fast-forward"의 의미와, 이번에 나지 않은 충돌

pull 로그에 `Merge made by ...`처럼 새로운 병합 커밋을 만들었다는 메시지 대신 `Fast-forward`라고만 찍힌 이유는, `second-project`에서 `5ca7c4d` 이후로 로컬에 새 커밋을 하나도 만들지 않았기 때문입니다. 로컬 히스토리와 원격 히스토리가 갈라진 지점이 없으므로, Git은 그저 `main` 포인터를 원격이 가리키는 `01e3921`로 앞으로 밀어 넣기만 하면 됩니다. 이것이 pull이 처리할 수 있는 가장 단순한 경우입니다.

만약 `second-project`에서도 같은 기간 동안 `README.md`를 별도로 수정하고 커밋해 두었다면 상황이 달라졌을 것입니다. 두 히스토리가 `5ca7c4d`에서 갈라진 상태이므로 pull은 fast-forward 대신 두 갈래를 합치는 병합(또는 설정에 따라 rebase)을 시도했을 것이고, 만약 두 쪽이 `README.md`의 같은 줄을 건드렸다면 Git이 자동으로 합칠 수 없어 충돌(conflict)이 발생했을 것입니다. 이런 상황에서는 `git status`로 충돌이 난 파일을 확인하고, 아직 커밋하지 않은 로컬 변경이 있다면 먼저 커밋하거나 `git stash`로 잠시 치워둔 뒤 다시 `pull`을 시도하는 절차를 밟게 됩니다. 다만 이번 실습 로그에는 이런 충돌 상황이 실제로 등장하지 않았습니다 — 체크리스트의 "pull 충돌 시 git stash" 항목은 원리로만 알아 두고, 이번 실습에서 직접 시연되지는 않았다는 점을 정직하게 밝혀 둡니다.

### clone과 pull, 언제 어느 쪽을 쓰는가

이번 실습은 clone과 pull의 차이를 두 디렉터리로 정확히 대비해서 보여줍니다.

| 구분 | clone | pull |
|---|---|---|
| 이번 실습에서 사용된 곳 | `quiz-clone`을 처음 만들 때(7-1) | `second-project`를 최신 상태로 갱신할 때(7-2) |
| 로컬 상태 | 아무것도 없음(처음 한 번) | 이미 저장소가 있고 일부만 뒤처져 있음 |
| 동작 | 원격 저장소 전체(히스토리·브랜치 레퍼런스·현재 파일)를 통째로 내려받아 새 디렉터리를 만듦 | 원격의 새 커밋만 가져와 현재 로컬 브랜치에 반영함 |
| 원격 등록 | 자동으로 `origin`이 등록됨 | 이미 등록된 원격을 그대로 사용 |

정리하면, clone은 "아직 로컬에 아무것도 없을 때, 처음 한 번 저장소 전체를 그대로 내려받는 것"이고, pull은 "이미 가지고 있는 로컬 저장소를 원격의 최신 상태로 따라잡는 것"입니다. `quiz-clone`을 만든 행위(7-1)는 전자이고, `second-project`에서 방금 실행한 `git pull origin main`(7-2)은 후자입니다. 같은 원격 저장소 하나를 두고 서로 다른 시점·서로 다른 목적으로 쓰이는 명령이라는 점을 이번 실습에서 직접 확인한 셈입니다.

### 체크리스트 반영 상태

위 로그와 현재 `second-project`의 실제 상태(`git log -1`이 `01e3921`, `README.md`에 회고 포함)를 대조하면, 7-2의 모든 항목은 실제로 수행되어 성공했습니다. `docs/learning_checklist.md`에는 아직 `[ ]`로 남아 있으므로, 체크 표시만 반영하면 됩니다. 다만 체크리스트가 표기한 이번 커밋 번호 "#16"에 대해서는, 앞서 Step 5(6-5)에서 다룬 번호가 #12·#13(필수)과 #14(선택, 이 프로젝트에서는 해당 없음)였다는 것만 확인될 뿐, 그 사이의 #15가 무엇인지는 이 체크리스트 범위 안에서 등장하지 않습니다. 번호가 #14에서 #16으로 건너뛴 이유는 이 문서만으로는 알 수 없으므로, 추측하지 않고 "번호에 공백이 있다"는 사실만 그대로 남겨 둡니다.

---

## 정리 — 확인하고 넘어가면 좋은 것들

Step 6에서 실제로 검증까지 끝난 부분과, 이번 실습에서 실제로는 일어나지 않은 부분을 구분하면 다음과 같습니다.

**이미 끝난 것 (실제 로그·저장소 상태로 확인됨)**
- `~/Project` 상위 폴더에 `quiz-clone`을 형제 디렉터리로 복제하고, `state.json`처럼 `.gitignore`에 걸린 파일은 복제되지 않는다는 것을 확인함
- 복제본의 `git log --oneline`에 12개 커밋 전체(이전 Step들에서 지적한 커밋 메시지 흠까지 포함)가 그대로 복제됨을 확인함
- `feat/play-quiz`가 로컬 브랜치가 아니라 원격 추적 브랜치로만 존재한다는 것, `origin`이 clone 시점에 자동 등록된다는 것을 확인함
- 복제본에서 README에 학습 회고를 추가·커밋·push(`01e3921`)하고, 원본에서 `git pull origin main`으로 fast-forward 반영까지 실제로 검증됨(pull 전/후 `README.md`와 `git log`로 직접 대조)

**이번 실습에서 실제로는 일어나지 않은 것**
- [ ] `docs/learning_checklist.md`의 "7-1"·"7-2" 체크박스를 실제 결과에 맞게 정리하기
- [ ] pull 충돌 시나리오는 이번엔 fast-forward로 끝나 실제로 발생하지 않았음 — 원한다면 원본에서도 README를 따로 수정해 두고 pull해 충돌·해결 과정을 직접 경험해 볼 수 있음
- [ ] 커밋 번호가 #14(Step 5, 선택 항목이라 건너뜀)에서 #16(이번 Step)으로 건너뛴 이유는 문서만으로는 확인되지 않음

이 항목들을 정리한 뒤에는 [`docs/learning_checklist.md`](../learning_checklist.md)의 다음 단계로 넘어갈 수 있습니다.

## 참고 문서

- [Step 0 학습 노트](step0_dev_environment_git_init.md) — 개발 환경 설정과 Git 저장소 초기화
- [Step 1 학습 노트](step1_quiz_model.md) — Quiz 모델과 자료구조 기본 데이터
- [Step 2 학습 노트](step2_quizgame_menu.md) — QuizGame, 메뉴, 공통 입력과 안전 종료
- [Step 3 학습 노트](step3_play_quiz_branch.md) — feat/play-quiz 브랜치와 퀴즈 풀기
- [Step 4 학습 노트](step4_add_list_score.md) — 퀴즈 추가, 목록 조회, 점수 확인
- [Step 5 학습 노트](step5_state_persistence.md) — state.json 영속성과 4대 복구 경로
- [학습 체크리스트](../learning_checklist.md) — 이 문서의 원본 체크리스트
- [학습 가이드](../learning_guide.md) — 단계별 실습 코드와 커밋 힌트
- [프로젝트 README](../../README.md) — 실제로 작성된 프로젝트 설명 문서
