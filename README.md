# 외국인 순매수 + 주가 분석 시스템

KOSPI 시장의 외국인 투자자 순매수 동향과 주가 변동률을 자동으로 분석하여 데이터를 수집, 저장, 알림하는 GitHub Actions 기반 시스템입니다.

## 🎯 주요 기능

### 1. 외국인 순매수 분석
- **기간별 순매수 순위**: 1일, 3일, 1주, 2주, 1개월, 3개월, 6개월, 1년
- **외국인 비중 계산**: 전체 거래량 대비 외국인 순매수 비중
- **투자자별 분석**: 외국인, 개인, 기관, 기타법인, 기타외국인 순매수 추적

### 2. 주가 변동률 분석
- **기간별 변동률**: 1일, 3일, 1주, 2주, 1개월, 3개월, 6개월, 1년
- **통합 평가**: 단기(1일~2주), 중기(1개월~3개월), 장기(6개월~1년)

### 3. 자동화 기능
- **데이터 수집**: pykrx API를 통한 한국거래소 공식 데이터 수집
- **데이터 저장**: JSON, Excel, Markdown 형식으로 자동 저장
- **Git 자동 커밋**: 수집된 데이터를 자동으로 GitHub에 push
- **Telegram 알림**: 분석 결과 요약을 Telegram으로 전송

## 📁 프로젝트 구조

```
your-repository/
├── .github/
│   └── workflows/
│       └── foreign_investment_analysis.yml    # GitHub Actions workflow
│
├── market_data/
│   └── foreign_investment/
│       ├── foreign_analysis_YYYYMMDD.json     # 일별 JSON 데이터
│       └── foreign_analysis_YYYYMMDD.xlsx     # 일별 Excel 데이터
│
├── analysis_reports/
│   └── foreign_investment/
│       └── foreign_analysis_YYYYMMDD.md       # 일별 분석 리포트
│
├── foreign_investment_analysis.py             # 메인 Python 스크립트
├── requirements.txt                           # Python 패키지 의존성
├── .gitignore                                 # Git 제외 파일
└── README.md                                  # 이 파일
```

## 🚀 빠른 시작

### 1. Repository 설정

```bash
# 1. 이 저장소를 클론하거나 파일들을 복사
git clone <your-repository-url>
cd <your-repository>

# 2. 필요한 파일들이 제자리에 있는지 확인
# - .github/workflows/foreign_investment_analysis.yml
# - foreign_investment_analysis.py
# - requirements.txt
```

### 2. GitHub Secrets 설정

Repository Settings → Secrets and variables → Actions에서 다음 Secrets를 추가:

- `TELEGRAM_BOT_TOKEN`: Telegram Bot Token
- `TELEGRAM_CHAT_ID`: Telegram Chat ID

#### Telegram Bot 설정 방법

1. **Bot 생성**:
   - Telegram에서 [@BotFather](https://t.me/botfather) 찾기
   - `/newbot` 명령어로 새 봇 생성
   - Bot Token 복사 → `TELEGRAM_BOT_TOKEN`에 저장

2. **Chat ID 확인**:
   - 생성한 봇과 대화 시작 (아무 메시지나 전송)
   - 브라우저에서 `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` 접속
   - `"chat":{"id":` 부분의 숫자 복사 → `TELEGRAM_CHAT_ID`에 저장

### 3. GitHub Actions 권한 설정

Repository Settings → Actions → General → Workflow permissions:
- ✅ **Read and write permissions** 선택
- ✅ **Allow GitHub Actions to create and approve pull requests** 체크

### 4. 실행

#### 자동 실행 (권장)
- 매일 오전 9시 (KST) 자동 실행됩니다.
- 첫 실행을 기다리거나 수동으로 테스트할 수 있습니다.

#### 수동 실행
1. GitHub Repository → Actions 탭
2. "Foreign Investment Analysis" workflow 선택
3. "Run workflow" 버튼 클릭

#### 로컬 실행 (테스트용)
```bash
# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# 실행
python foreign_investment_analysis.py
```

## 📊 데이터 구조

### JSON 파일 구조
```json
{
  "analysis_date": "2024-11-27",
  "timestamp": "2024-11-27T09:00:00",
  "total_stocks": 45,
  "data": [
    {
      "종목명": "삼성전자",
      "시총순위": 1,
      "시가총액_억원": 4500000,
      "외국인비중_단기": 15.5,
      "분자_단기": "양수",
      "분모_단기": "음수",
      "주가변동_단기": 2.3,
      "외국인비중_중기": 12.8,
      "주가변동_중기": 5.1,
      "외국인비중_장기": 10.2,
      "주가변동_장기": 8.7,
      "외국인_단기평가": 5,
      "외국인_중기평가": 8,
      "외국인_장기평가": 12,
      "1일": 2,
      "주가변동_1일": 0.5,
      ...
    }
  ]
}
```

### Excel 파일 내용
- 모든 분석 데이터를 포함한 스프레드시트
- 필터링, 정렬, 차트 작성에 활용 가능

### Markdown 리포트 내용
- 분석 요약 정보
- 상위 10개 종목 테이블
- 분석 기준 설명

## 🔍 분석 알고리즘

### 외국인 비중 계산
```
외국인비중 = (외국인순매수 / 전체활동량) × 100

전체활동량 = |외국인순매수| + |개인순매수| + |기관순매수| + |기타순매수|

조건: 전체활동량 > 100만원
```

### 주가 변동률 계산
```
주가변동률 = ((현재가 - 과거가) / 과거가) × 100

영업일 기준:
- 1일 = 1 영업일 전
- 1주 = 5 영업일 전
- 1개월 = 20 영업일 전
- 1년 = 240 영업일 전
```

### 통합 평가 계산
```
단기평가 = rank(1일 순위 + 3일 순위 + 1주 순위 + 2주 순위)
중기평가 = rank(1개월 순위 + 3개월 순위)
장기평가 = rank(6개월 순위 + 1년 순위)

※ 순위가 낮을수록(숫자가 작을수록) 좋은 평가
```

### 정렬 기준
1. **1차**: 외국인비중_단기 내림차순 (높은 값이 위로)
2. **2차**: 시총순위 오름차순 (작은 값이 위로)

## 📱 Telegram 알림

### 알림 내용
- 분석 기준일
- 분석 종목 수
- 상위 5개 종목 상세 정보
  - 종목명
  - 외국인비중(단기)
  - 주가변동(단기)
  - 시총순위

### 알림 예시
```
📊 외국인 순매수 + 주가 분석

📅 분석일: 2024-11-27
📈 분석 종목: 45개

상위 5개 종목

1. 삼성전자
   외국인비중(단기): 15.5%
   주가변동(단기): 2.3%
   시총순위: 1

2. SK하이닉스
   외국인비중(단기): 12.8%
   주가변동(단기): -1.2%
   시총순위: 2

...

💾 상세 데이터: GitHub Repository 참조
```

## 📦 필수 패키지

```
pykrx>=1.0.47       # 한국거래소 데이터 API
pandas>=2.0.0       # 데이터 처리
openpyxl>=3.1.0     # Excel 파일 생성
requests>=2.31.0    # HTTP 요청 (Telegram)
```

## ⚙️ 설정 옵션

### 스케줄 변경
`.github/workflows/foreign_investment_analysis.yml` 파일에서 cron 표현식 수정:

```yaml
on:
  schedule:
    # 매일 오전 9시 (KST) = UTC 0시
    - cron: '0 0 * * *'
    
    # 변경 예시:
    # - cron: '0 1 * * *'  # 오전 10시 (KST)
    # - cron: '0 0 * * 1-5'  # 평일만 오전 9시
```

### 분석 대상 변경
`foreign_investment_analysis.py`에서 수정 가능:

```python
# 시가총액 TOP 30 → TOP 50으로 변경
df_top30 = df_cap.head(50).copy()  # 30 → 50

# 최소 활동량 기준 변경
if total_activity > 1000000:  # 100만원 → 다른 값으로 변경
```

## 📈 데이터 활용 예시

### 1. 과거 데이터 조회
```bash
# 특정 날짜 데이터 확인
cat market_data/foreign_investment/foreign_analysis_20241127.json

# 여러 날짜 데이터 비교
ls market_data/foreign_investment/
```

### 2. Python으로 데이터 분석
```python
import json
import pandas as pd

# JSON 파일 읽기
with open('market_data/foreign_investment/foreign_analysis_20241127.json') as f:
    data = json.load(f)

# DataFrame으로 변환
df = pd.DataFrame(data['data'])

# 외국인비중 상위 10개
top10 = df.nlargest(10, '외국인비중_단기')
print(top10[['종목명', '외국인비중_단기', '주가변동_단기']])
```

### 3. Excel 파일 활용
- Excel에서 직접 열기
- 피벗 테이블, 차트 생성
- 필터링, 정렬로 원하는 종목 찾기

## ⚠️ 주의사항

1. **거래일 기준**: 영업일(거래일) 기준으로 데이터 수집
2. **데이터 지연**: 전일 장마감 데이터 기준 (당일 데이터 아님)
3. **종목 범위**: 
   - 시가총액 TOP 30
   - 각 기간별 외국인 순매수 상위 30
   - 중복 제거 후 통합
4. **최소 활동량**: 전체활동량 100만원 이상인 종목만 비중 계산
5. **공휴일**: 거래일이 아닌 날은 데이터가 생성되지 않음
6. **API 제한**: pykrx API 호출 제한이 있을 수 있음

## 🐛 문제 해결

### GitHub Actions 실행 실패
1. Actions 탭에서 실행 로그 확인
2. Secrets 설정 확인 (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`)
3. Repository 권한 확인 (Read and write permissions)

### Telegram 알림 안 옴
1. Bot Token 확인
2. Chat ID 확인
3. 봇과 대화 시작했는지 확인 (최소 1회 메시지 전송 필요)

### 데이터 저장 안 됨
1. GitHub Actions 권한 확인
2. workflow 파일의 `permissions: contents: write` 확인
3. Git commit 로그 확인

### pykrx 오류
1. 한국거래소 서버 점검 시간 확인
2. 거래일인지 확인 (주말, 공휴일은 데이터 없음)
3. 네트워크 연결 확인

## 📝 라이센스

MIT License

## 🤝 기여

이슈와 풀 리퀘스트를 환영합니다!

## 📧 문의

GitHub Issues를 통해 문의해주세요.

---

**Made with ❤️ for Korean Stock Market Analysis**
