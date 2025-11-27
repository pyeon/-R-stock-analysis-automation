# 배포 가이드

외국인 순매수 + 주가 분석 시스템을 GitHub에 배포하는 단계별 가이드입니다.

## 📋 배포 전 체크리스트

- [ ] GitHub 계정 및 Repository 준비
- [ ] Telegram Bot Token 발급
- [ ] Telegram Chat ID 확인
- [ ] 필요한 파일 다운로드 완료

## 📁 필요한 파일 목록

### 필수 파일 (7개)

1. **`.github/workflows/foreign_investment_analysis.yml`**
   - GitHub Actions workflow 설정 파일

2. **`foreign_investment_analysis.py`**
   - 메인 Python 실행 스크립트

3. **`requirements.txt`**
   - Python 패키지 의존성

4. **`.gitignore`**
   - Git 제외 파일 설정

5. **`README.md`**
   - 프로젝트 메인 문서

6. **`FOLDER_STRUCTURE.md`** (선택)
   - 폴더 구조 상세 설명

7. **`DEPLOYMENT.md`** (이 파일, 선택)
   - 배포 가이드

## 🚀 배포 단계

### 1단계: Telegram Bot 준비

#### 1.1 Bot 생성
```
1. Telegram 앱 열기
2. @BotFather 검색하여 대화 시작
3. /newbot 명령어 입력
4. Bot 이름 입력 (예: "Stock Analysis Bot")
5. Bot username 입력 (예: "my_stock_bot")
6. Bot Token 복사 (예: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)
```

#### 1.2 Chat ID 확인
```
1. 생성한 Bot과 대화 시작
2. 아무 메시지나 전송 (예: "Hello")
3. 웹 브라우저에서 아래 URL 접속:
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   
4. 응답에서 "chat":{"id": 숫자 부분 찾기
   예: "chat":{"id":123456789,...
   
5. Chat ID 복사 (예: 123456789)
```

### 2단계: GitHub Repository 준비

#### 2.1 새 Repository 생성
```
1. GitHub 로그인
2. 우측 상단 '+' → 'New repository'
3. Repository 이름 입력 (예: foreign-investment-analysis)
4. Public 또는 Private 선택
5. 'Create repository' 클릭
```

#### 2.2 로컬에서 초기화 (선택적)
```bash
# 새 디렉토리 생성
mkdir foreign-investment-analysis
cd foreign-investment-analysis

# Git 초기화
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### 3단계: 파일 업로드

#### 방법 A: GitHub 웹 인터페이스 사용 (권장)

```
1. GitHub Repository 페이지 접속
2. 'Add file' → 'Upload files' 클릭
3. 다음 파일들을 드래그 앤 드롭:
   - foreign_investment_analysis.py
   - requirements.txt
   - .gitignore
   - README.md
   - FOLDER_STRUCTURE.md (선택)
   - DEPLOYMENT.md (선택)
   
4. 'Commit changes' 클릭

5. '.github/workflows' 폴더 생성:
   - Repository 메인 페이지에서 'Add file' → 'Create new file'
   - 파일명에 '.github/workflows/foreign_investment_analysis.yml' 입력
   - foreign_investment_analysis.yml 내용 붙여넣기
   - 'Commit new file' 클릭
```

#### 방법 B: Git 명령어 사용

```bash
# 파일들을 로컬 디렉토리에 복사한 후

# .github/workflows 디렉토리 생성
mkdir -p .github/workflows

# foreign_investment_analysis.yml을 .github/workflows/에 복사
cp foreign_investment_analysis.yml .github/workflows/

# Git에 추가
git add .
git commit -m "Initial commit: Foreign investment analysis system"

# GitHub에 push
git branch -M main
git push -u origin main
```

### 4단계: GitHub Secrets 설정

```
1. Repository 페이지에서 'Settings' 클릭
2. 왼쪽 메뉴에서 'Secrets and variables' → 'Actions' 클릭
3. 'New repository secret' 클릭

4. 첫 번째 Secret 추가:
   Name: TELEGRAM_BOT_TOKEN
   Secret: (1단계에서 복사한 Bot Token 붙여넣기)
   'Add secret' 클릭

5. 두 번째 Secret 추가:
   Name: TELEGRAM_CHAT_ID
   Secret: (1단계에서 복사한 Chat ID 붙여넣기)
   'Add secret' 클릭
```

### 5단계: GitHub Actions 권한 설정

```
1. Repository 'Settings' → 'Actions' → 'General'
2. 'Workflow permissions' 섹션에서:
   ✅ 'Read and write permissions' 선택
   ✅ 'Allow GitHub Actions to create and approve pull requests' 체크
3. 'Save' 클릭
```

### 6단계: 첫 실행 테스트

#### 수동 실행으로 테스트
```
1. Repository 페이지에서 'Actions' 탭 클릭
2. 왼쪽에서 'Foreign Investment Analysis' workflow 선택
3. 우측 'Run workflow' 버튼 클릭
4. 'Run workflow' 확인 클릭
5. 실행 상태 확인:
   - 노란색 원: 실행 중
   - 초록색 체크: 성공
   - 빨간색 X: 실패
```

#### 실행 로그 확인
```
1. 실행된 workflow 클릭
2. 'analyze' job 클릭
3. 각 단계별 로그 확인:
   - Run Foreign Investment Analysis
   - Commit and Push Data
```

### 7단계: 결과 확인

#### Telegram 확인
- Bot에서 분석 요약 메시지가 도착했는지 확인

#### GitHub Repository 확인
```
1. Repository 메인 페이지 새로고침
2. 새로 생성된 디렉토리 확인:
   - market_data/foreign_investment/
   - analysis_reports/foreign_investment/
3. 생성된 파일 확인:
   - foreign_analysis_YYYYMMDD.json
   - foreign_analysis_YYYYMMDD.xlsx
   - foreign_analysis_YYYYMMDD.md
```

## ✅ 배포 완료 확인

다음 사항들이 모두 확인되면 배포 완료:

- [ ] GitHub Actions workflow가 성공적으로 실행됨
- [ ] `market_data/foreign_investment/` 디렉토리에 JSON, Excel 파일 생성
- [ ] `analysis_reports/foreign_investment/` 디렉토리에 Markdown 파일 생성
- [ ] Telegram Bot으로 알림 수신
- [ ] Git commit이 자동으로 푸시됨

## 🔄 자동 실행 스케줄

배포 완료 후:
- **매일 오전 9시 (KST)** 자동 실행
- **평일/주말 모두** 실행 (거래일에만 데이터 생성)

## 🐛 문제 해결

### 문제 1: Workflow 실행 실패

**증상**: Actions 탭에서 빨간색 X 표시

**해결**:
```
1. 실행 로그 확인:
   - Actions → 실패한 workflow 클릭 → 로그 확인

2. 일반적인 원인:
   - Secrets 미설정: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID 확인
   - 권한 부족: Workflow permissions 확인
   - Python 패키지 오류: requirements.txt 확인
```

### 문제 2: Telegram 알림 없음

**증상**: Workflow는 성공했지만 Telegram 알림 없음

**해결**:
```
1. Bot Token 확인:
   - Secrets에 정확히 입력되었는지 확인
   - Token이 유효한지 확인

2. Chat ID 확인:
   - Secrets에 정확히 입력되었는지 확인
   - Bot과 대화를 시작했는지 확인 (최소 1회 메시지 전송)

3. 테스트:
   - Bot에게 /start 메시지 전송
   - workflow 다시 실행
```

### 문제 3: 데이터 파일 생성 안 됨

**증상**: Workflow는 성공했지만 market_data/ 디렉토리 없음

**해결**:
```
1. Workflow permissions 확인:
   Settings → Actions → General
   'Read and write permissions' 선택되어 있는지 확인

2. Commit and Push 단계 로그 확인:
   - "nothing to commit" 메시지 확인
   - 권한 오류 메시지 확인
```

### 문제 4: 주말에 실행되지 않음

**증상**: 주말에 workflow가 실행되지 않음

**설명**: 이것은 정상입니다
```
- 주말은 거래일이 아니므로 데이터가 없음
- Workflow는 실행되지만 "거래일을 찾을 수 없습니다" 메시지와 함께 종료
- 다음 거래일에 정상 실행됨
```

## 📞 추가 지원

### 디버깅 팁
```bash
# 로컬에서 테스트
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
python foreign_investment_analysis.py

# 에러 메시지 확인
# Telegram 알림 수신 확인
# 생성된 파일 확인
```

### 유용한 링크
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [pykrx 문서](https://github.com/sharebook-kr/pykrx)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 🎉 배포 성공!

축하합니다! 이제 매일 자동으로 외국인 순매수 분석이 실행됩니다.

다음 할 일:
1. 첫 알림 대기 (익일 오전 9시)
2. 데이터 누적 확인 (며칠 후)
3. 분석 결과 활용

---

**Happy Analyzing! 📊**
