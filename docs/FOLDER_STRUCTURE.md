# 외국인 순매수 분석 - 프로젝트 폴더 구조

## 📁 전체 디렉토리 구조

```
your-repository/
├── .github/
│   └── workflows/
│       └── foreign_investment_analysis.yml    # GitHub Actions workflow
│
├── market_data/
│   └── foreign_investment/
│       ├── foreign_analysis_20241127.json     # 일별 JSON 데이터
│       ├── foreign_analysis_20241127.xlsx     # 일별 Excel 데이터
│       ├── foreign_analysis_20241126.json
│       ├── foreign_analysis_20241126.xlsx
│       └── ...                                # 과거 데이터 누적
│
├── analysis_reports/
│   └── foreign_investment/
│       ├── foreign_analysis_20241127.md       # 일별 Markdown 리포트
│       ├── foreign_analysis_20241126.md
│       └── ...                                # 과거 리포트 누적
│
├── foreign_investment_analysis.py             # 메인 Python 스크립트
│
├── README_FOREIGN_INVESTMENT.md               # 프로젝트 문서
│
└── .gitignore                                 # Git 제외 파일 설정 (선택)
```

## 📂 디렉토리 설명

### `.github/workflows/`
- **목적**: GitHub Actions 자동화 설정
- **파일**: `foreign_investment_analysis.yml`
- **역할**: 매일 오전 9시 자동 실행 스케줄 관리

### `market_data/foreign_investment/`
- **목적**: 원본 데이터 저장
- **형식**: JSON, Excel
- **명명규칙**: `foreign_analysis_YYYYMMDD.{json,xlsx}`
- **특징**: 
  - 날짜별로 파일 누적
  - Git으로 버전 관리
  - 히스토리 데이터 보존

### `analysis_reports/foreign_investment/`
- **목적**: 분석 리포트 저장
- **형식**: Markdown
- **명명규칙**: `foreign_analysis_YYYYMMDD.md`
- **내용**:
  - 분석 요약
  - 상위 10개 종목 테이블
  - 분석 기준 설명

### 루트 디렉토리
- `foreign_investment_analysis.py`: 메인 실행 스크립트
- `README_FOREIGN_INVESTMENT.md`: 프로젝트 문서

## 📋 파일 명명 규칙

### 데이터 파일
```
foreign_analysis_YYYYMMDD.json   # 예: foreign_analysis_20241127.json
foreign_analysis_YYYYMMDD.xlsx   # 예: foreign_analysis_20241127.xlsx
foreign_analysis_YYYYMMDD.md     # 예: foreign_analysis_20241127.md
```

### 날짜 형식
- **YYYYMMDD**: 8자리 숫자 (예: 20241127)
- **분석 기준일**: 해당 날짜의 전일 장마감 데이터

## 🔧 초기 설정 방법

### 1. 디렉토리 생성 (자동)
스크립트 실행 시 자동으로 생성됩니다:
```python
os.makedirs('market_data/foreign_investment', exist_ok=True)
os.makedirs('analysis_reports/foreign_investment', exist_ok=True)
```

### 2. 수동 생성 (선택)
```bash
mkdir -p .github/workflows
mkdir -p market_data/foreign_investment
mkdir -p analysis_reports/foreign_investment
```

### 3. 파일 배치
```bash
# workflow 파일
mv foreign_investment_analysis.yml .github/workflows/

# Python 스크립트 (루트에 위치)
# foreign_investment_analysis.py는 이미 루트에 있음

# README (루트에 위치)
# README_FOREIGN_INVESTMENT.md는 이미 루트에 있음
```

## 📊 데이터 파일 예시

### JSON 구조
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
      "주가변동_단기": 2.3,
      ...
    }
  ]
}
```

### Markdown 리포트 예시
```markdown
# 외국인 순매수 + 주가 분석

**분석 기준일**: 2024-11-27
**분석 종목 수**: 45개
**생성 시각**: 2024-11-27 09:00:00

## 상위 10개 종목

| 순위 | 종목명 | 시총순위 | 외국인비중(단기) | 주가변동(단기) |
|------|--------|----------|------------------|----------------|
| 1    | 삼성전자 | 1      | 15.5%           | 2.3%          |
...
```

## 🚀 배포 체크리스트

- [ ] `.github/workflows/` 디렉토리 생성
- [ ] `foreign_investment_analysis.yml` 업로드
- [ ] `foreign_investment_analysis.py` 업로드
- [ ] `README_FOREIGN_INVESTMENT.md` 업로드
- [ ] GitHub Secrets 설정
  - [ ] `TELEGRAM_BOT_TOKEN`
  - [ ] `TELEGRAM_CHAT_ID`
- [ ] Repository Settings → Actions → General
  - [ ] "Read and write permissions" 활성화
- [ ] 수동 실행으로 테스트
- [ ] `market_data/`, `analysis_reports/` 디렉토리 생성 확인

## 📝 .gitignore 권장 설정

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# 임시 파일
*.tmp
*.log

# 제외하지 않을 파일 (데이터는 Git으로 관리)
!market_data/
!analysis_reports/
```

## 🔄 데이터 누적 방식

### 일별 데이터 저장
- 매일 새로운 파일 생성
- 기존 파일 덮어쓰지 않음
- Git으로 모든 히스토리 보존

### 예시 (1주일 실행 후)
```
market_data/foreign_investment/
├── foreign_analysis_20241127.json
├── foreign_analysis_20241127.xlsx
├── foreign_analysis_20241126.json
├── foreign_analysis_20241126.xlsx
├── foreign_analysis_20241125.json
├── foreign_analysis_20241125.xlsx
├── foreign_analysis_20241124.json
└── foreign_analysis_20241124.xlsx
```

## 💡 활용 팁

1. **과거 데이터 조회**: `market_data/foreign_investment/` 디렉토리에서 날짜별 파일 확인
2. **트렌드 분석**: 여러 날짜의 JSON 파일을 비교하여 외국인 매수 패턴 분석
3. **리포트 공유**: `analysis_reports/` 디렉토리의 Markdown 파일을 바로 GitHub에서 확인
4. **데이터 백업**: Git 히스토리로 자동 백업 (별도 백업 불필요)

## 🔗 관련 문서

- [README_FOREIGN_INVESTMENT.md](README_FOREIGN_INVESTMENT.md) - 프로젝트 상세 문서
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [pykrx 문서](https://github.com/sharebook-kr/pykrx)
