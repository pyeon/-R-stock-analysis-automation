"""
외국인 순매수 + 주가 변동률 분석 (GitHub Actions)
- 데이터 수집 → JSON/Excel/Markdown 저장 → Git push → Telegram 요약 전송
"""

import os
import json
from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 환경변수
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 저장 디렉토리
DATA_DIR = 'market_data/foreign_investment'
REPORT_DIR = 'analysis_reports/foreign_investment'

def setup_directories():
    """디렉토리 생성"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

def get_latest_trading_date():
    """최근 거래일 찾기"""
    today = datetime.now()
    for i in range(10):
        check_date = today - timedelta(days=i)
        date_str = check_date.strftime('%Y%m%d')
        try:
            df = stock.get_market_cap(date_str, market="KOSPI")
            if len(df[df['시가총액'] > 0]) > 0:
                return date_str, check_date
        except:
            continue
    return None, None

def get_trading_date_before(base_date_str, business_days):
    """N 영업일 전 날짜 찾기"""
    base_date = datetime.strptime(base_date_str, '%Y%m%d')
    search_days = business_days * 2 + 10
    start_search = base_date - timedelta(days=search_days)
    
    try:
        df = stock.get_market_ohlcv_by_date(
            start_search.strftime('%Y%m%d'),
            base_date_str,
            "005930"
        )
        
        if len(df) > business_days:
            target_date = df.index[-business_days-1]
            return target_date.strftime('%Y%m%d')
        else:
            return (base_date - timedelta(days=business_days * 1.5)).strftime('%Y%m%d')
    except:
        return (base_date - timedelta(days=business_days * 1.5)).strftime('%Y%m%d')

def get_market_cap_top30(date_str):
    """시가총액 상위 30개 + 전체 순위"""
    df_cap = stock.get_market_cap(date_str, market="KOSPI")
    df_cap = df_cap.sort_values('시가총액', ascending=False).reset_index()
    df_cap['전체_시총순위'] = range(1, len(df_cap) + 1)
    df_top30 = df_cap.head(30).copy()
    
    tickers = df_top30['티커'].tolist()
    names = [stock.get_market_ticker_name(ticker) for ticker in tickers]
    
    result = pd.DataFrame({
        '종목명': names,
        '시총순위': range(1, 31),
        '시가총액': df_top30['시가총액'].values,
        '티커': tickers
    })
    
    return result, df_cap[['티커', '전체_시총순위', '시가총액']]

def get_foreign_net_buy_all(start_date_str, end_date_str):
    """외국인 + 주요 투자자 순매수 조회"""
    try:
        df_foreign = stock.get_market_net_purchases_of_equities(
            start_date_str, end_date_str, "KOSPI", "외국인"
        )
        df_foreign = df_foreign.sort_values('순매수거래대금', ascending=False).reset_index()
        df_foreign['순위'] = range(1, len(df_foreign) + 1)
        df_foreign = df_foreign.rename(columns={'순매수거래대금': '외국인순매수'})
        
        df_individual = stock.get_market_net_purchases_of_equities(
            start_date_str, end_date_str, "KOSPI", "개인"
        )
        df_individual = df_individual.reset_index()
        df_individual = df_individual.rename(columns={'순매수거래대금': '개인순매수'})
        
        df_inst = stock.get_market_net_purchases_of_equities(
            start_date_str, end_date_str, "KOSPI", "기관합계"
        )
        df_inst = df_inst.reset_index()
        df_inst = df_inst.rename(columns={'순매수거래대금': '기관순매수'})
        
        df_corp = stock.get_market_net_purchases_of_equities(
            start_date_str, end_date_str, "KOSPI", "기타법인"
        )
        df_corp = df_corp.reset_index()
        df_corp = df_corp.rename(columns={'순매수거래대금': '기타법인순매수'})
        
        df_other_foreign = stock.get_market_net_purchases_of_equities(
            start_date_str, end_date_str, "KOSPI", "기타외국인"
        )
        df_other_foreign = df_other_foreign.reset_index()
        df_other_foreign = df_other_foreign.rename(columns={'순매수거래대금': '기타외국인순매수'})
        
        df_merged = df_foreign.merge(
            df_individual[['종목명', '개인순매수']], on='종목명', how='left'
        ).merge(
            df_inst[['종목명', '기관순매수']], on='종목명', how='left'
        ).merge(
            df_corp[['종목명', '기타법인순매수']], on='종목명', how='left'
        ).merge(
            df_other_foreign[['종목명', '기타외국인순매수']], on='종목명', how='left'
        )
        
        df_merged['개인순매수'] = df_merged['개인순매수'].fillna(0)
        df_merged['기관순매수'] = df_merged['기관순매수'].fillna(0)
        df_merged['기타법인순매수'] = df_merged['기타법인순매수'].fillna(0)
        df_merged['기타외국인순매수'] = df_merged['기타외국인순매수'].fillna(0)
        
        df_merged['기타순매수'] = df_merged['기타법인순매수'] + df_merged['기타외국인순매수']
        df_merged['전체활동량'] = (
            abs(df_merged['외국인순매수']) + 
            abs(df_merged['개인순매수']) + 
            abs(df_merged['기관순매수']) +
            abs(df_merged['기타순매수'])
        )
        
        df_merged['순매수_억원'] = (df_merged['외국인순매수'] / 100000000).round(0)
        
        return df_merged[[
            '종목명', '순위', '순매수_억원', 
            '외국인순매수', '개인순매수', '기관순매수', '기타순매수', '전체활동량'
        ]]
    except Exception as e:
        print(f"데이터 조회 오류: {e}")
        return pd.DataFrame()

def get_all_prices_on_date(date_str, target_stocks):
    """특정 날짜의 필요한 종목들 가격 조회"""
    prices = {}
    
    print(f"     대상: {len(target_stocks)}개 종목 조회 중...", end=" ")
    
    success_count = 0
    for stock_name in target_stocks:
        try:
            tickers = stock.get_market_ticker_list(date_str, market="KOSPI")
            ticker = None
            
            for t in tickers:
                if stock.get_market_ticker_name(t) == stock_name:
                    ticker = t
                    break
            
            if ticker:
                df = stock.get_market_ohlcv_by_date(date_str, date_str, ticker)
                if not df.empty:
                    prices[stock_name] = df['종가'].iloc[0]
                    success_count += 1
        except:
            continue
    
    print(f"{success_count}개 성공")
    return prices

def calculate_price_changes(df_master, base_date_str):
    """주가 변동률 계산"""
    print("\n6️⃣ 주가 변동률 계산 중...")
    
    period_mapping = {
        '1일': 1,
        '3일': 3,
        '1주': 5,
        '2주': 10,
        '1개월': 20,
        '3개월': 60,
        '6개월': 120,
        '1년': 240
    }
    
    target_stocks = df_master['종목명'].tolist()
    
    print(f"   • 기준일({base_date_str}) 가격 조회 중...")
    current_prices = get_all_prices_on_date(base_date_str, target_stocks)
    print(f"     ✅ {len(current_prices)}개 종목")
    
    past_prices = {}
    for period_name, business_days in period_mapping.items():
        print(f"   • {period_name} 전({business_days} 영업일) 가격 조회 중...")
        
        past_date_str = get_trading_date_before(base_date_str, business_days)
        print(f"     날짜: {past_date_str}", end=", ")
        prices = get_all_prices_on_date(past_date_str, target_stocks)
        past_prices[period_name] = prices
    
    print("\n   • 변동률 계산 중...")
    for period_name in period_mapping.keys():
        col_name = f'주가변동_{period_name}'
        changes = []
        
        for _, row in df_master.iterrows():
            stock_name = row['종목명']
            
            if stock_name in current_prices and stock_name in past_prices[period_name]:
                current = current_prices[stock_name]
                past = past_prices[period_name][stock_name]
                
                if past > 0:
                    change_pct = ((current - past) / past) * 100
                    changes.append(round(change_pct, 2))
                else:
                    changes.append('-')
            else:
                changes.append('-')
        
        df_master[col_name] = changes
    
    print("   • 통합 평가(단기/중기/장기) 계산 중...")
    
    for _, row_idx in enumerate(df_master.index):
        short_values = []
        for p in ['1일', '3일', '1주', '2주']:
            val = df_master.loc[row_idx, f'주가변동_{p}']
            if val != '-' and pd.notna(val):
                short_values.append(val)
        df_master.loc[row_idx, '주가변동_단기'] = round(sum(short_values) / len(short_values), 2) if short_values else '-'
        
        mid_values = []
        for p in ['1개월', '3개월']:
            val = df_master.loc[row_idx, f'주가변동_{p}']
            if val != '-' and pd.notna(val):
                mid_values.append(val)
        df_master.loc[row_idx, '주가변동_중기'] = round(sum(mid_values) / len(mid_values), 2) if mid_values else '-'
        
        long_values = []
        for p in ['6개월', '1년']:
            val = df_master.loc[row_idx, f'주가변동_{p}']
            if val != '-' and pd.notna(val):
                long_values.append(val)
        df_master.loc[row_idx, '주가변동_장기'] = round(sum(long_values) / len(long_values), 2) if long_values else '-'
    
    print("   ✅ 주가 변동률 계산 완료")
    
    return df_master

def send_telegram_message(message):
    """텔레그램 메시지 전송"""
    import requests
    
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ 텔레그램 설정 없음")
        return None
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"❌ 텔레그램 전송 오류: {e}")
        return None

def save_to_json(data, filename):
    """JSON 저장"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 저장: {filepath}")

def save_to_excel(df, filename):
    """Excel 저장"""
    filepath = os.path.join(DATA_DIR, filename)
    df.to_excel(filepath, index=False, engine='openpyxl')
    print(f"✅ Excel 저장: {filepath}")

def save_to_markdown(df, analysis_date, filename):
    """Markdown 리포트 저장"""
    filepath = os.path.join(REPORT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# 외국인 순매수 + 주가 분석\n\n")
        f.write(f"**분석 기준일**: {analysis_date}\n")
        f.write(f"**분석 종목 수**: {len(df)}개\n")
        f.write(f"**생성 시각**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 상위 10개 종목\n\n")
        f.write("| 순위 | 종목명 | 시총순위 | 외국인비중(단기) | 주가변동(단기) | 외국인비중(중기) | 주가변동(중기) |\n")
        f.write("|------|--------|----------|------------------|----------------|------------------|----------------|\n")
        
        for idx, row in df.head(10).iterrows():
            f.write(f"| {idx+1} | {row['종목명']} | {row['시총순위']} | ")
            f.write(f"{row['외국인비중_단기']}% | {row['주가변동_단기']}% | ")
            f.write(f"{row['외국인비중_중기']}% | {row['주가변동_중기']}% |\n")
        
        f.write("\n## 분석 기준\n\n")
        f.write("- **외국인비중**: 전체 거래량 대비 외국인 순매수 비중\n")
        f.write("- **주가변동**: 기간별 주가 변동률 (%)\n")
        f.write("- **정렬**: 외국인비중_단기 내림차순 → 시총순위 오름차순\n")
    
    print(f"✅ Markdown 저장: {filepath}")

def main():
    print("=" * 80)
    print("📊 외국인 순매수 + 주가 분석 (GitHub Actions)")
    print("=" * 80)
    
    setup_directories()
    
    end_date_str, end_date = get_latest_trading_date()
    
    if end_date_str is None:
        print("❌ 최근 거래일을 찾을 수 없습니다.")
        return
    
    report_date = end_date.strftime('%Y-%m-%d')
    print(f"\n📅 기준일: {report_date}\n")
    
    # 1. 시가총액 TOP 30
    print("1️⃣ 시가총액 정보 조회... ", end="")
    df_master, df_all_cap = get_market_cap_top30(end_date_str)
    print(f"✅ {len(df_master)}개")
    df_master['시가총액_억원'] = (df_master['시가총액'] / 100000000).round(0).astype(int)
    
    # 2. 기간별 순매수 데이터
    periods = {
        '1일': 1, '3일': 3, '1주': 7, '2주': 14,
        '1개월': 30, '3개월': 90, '6개월': 180, '1년': 365
    }
    
    print("\n2️⃣ 기간별 외국인 순매수 순위 조회")
    
    period_data = {}
    for period_name, days in periods.items():
        start_date = end_date - timedelta(days=days + 5)
        start_date_str = start_date.strftime('%Y%m%d')
        
        print(f"   • {period_name:4s} 조회 중... ", end="")
        df_period = get_foreign_net_buy_all(start_date_str, end_date_str)
        
        if not df_period.empty:
            period_data[period_name] = df_period
            df_period_top30 = df_period[df_period['순위'] <= 30].copy()
            df_period_top30 = df_period_top30.rename(columns={'순위': period_name})
            df_master = df_master.merge(
                df_period_top30[['종목명', period_name]], on='종목명', how='left'
            )
            print(f"✅")
        else:
            df_master[period_name] = None
            print("❌")
    
    # 3. 외국인 비중 계산
    print("\n3️⃣ 외국인 순매수 비중 계산 중...")
    
    ratio_periods = {
        '외국인비중_단기': '2주',
        '외국인비중_중기': '3개월',
        '외국인비중_장기': '1년'
    }
    
    for ratio_col, period_name in ratio_periods.items():
        print(f"   • {ratio_col} ({period_name} 기준)... ", end="")
        
        numerator_col = ratio_col.replace('외국인비중', '분자')
        denominator_col = ratio_col.replace('외국인비중', '분모')
        
        if period_name in period_data and not period_data[period_name].empty:
            foreign_ratios = {}
            numerator_signs = {}
            denominator_signs = {}
            
            for _, row in df_master.iterrows():
                stock_name = row['종목명']
                stock_net = period_data[period_name][period_data[period_name]['종목명'] == stock_name]
                
                if not stock_net.empty:
                    foreign_net = stock_net.iloc[0]['외국인순매수']
                    individual_net = stock_net.iloc[0]['개인순매수']
                    inst_net = stock_net.iloc[0]['기관순매수']
                    other_net = stock_net.iloc[0]['기타순매수']
                    total_activity = stock_net.iloc[0]['전체활동량']
                    
                    if total_activity > 1000000:
                        numerator_signs[stock_name] = "양수" if foreign_net >= 0 else "음수"
                        rest_sum = individual_net + inst_net + other_net
                        denominator_signs[stock_name] = "양수" if rest_sum >= 0 else "음수"
                        ratio = (foreign_net / total_activity) * 100
                        foreign_ratios[stock_name] = round(ratio, 2)
                    else:
                        foreign_ratios[stock_name] = "-"
                        numerator_signs[stock_name] = "-"
                        denominator_signs[stock_name] = "-"
                else:
                    foreign_ratios[stock_name] = "-"
                    numerator_signs[stock_name] = "-"
                    denominator_signs[stock_name] = "-"
            
            df_master[ratio_col] = df_master['종목명'].map(foreign_ratios)
            df_master[numerator_col] = df_master['종목명'].map(numerator_signs)
            df_master[denominator_col] = df_master['종목명'].map(denominator_signs)
            print("✅")
        else:
            df_master[ratio_col] = "-"
            df_master[numerator_col] = "-"
            df_master[denominator_col] = "-"
            print("❌")
    
    # 4. 추가 종목 수집
    print("\n4️⃣ 기간별 순매수 상위 종목 추가 수집")
    all_top_stocks = set(df_master['종목명'].tolist())
    
    for period_name, df_period in period_data.items():
        if not df_period.empty:
            top30_stocks = df_period[df_period['순위'] <= 30]['종목명'].tolist()
            all_top_stocks.update(top30_stocks)
    
    print(f"   총 {len(all_top_stocks)}개 고유 종목 발견")
    
    existing_stocks = set(df_master['종목명'].tolist())
    missing_stocks = all_top_stocks - existing_stocks
    
    if missing_stocks:
        print(f"   시가총액 30위 밖 종목 {len(missing_stocks)}개 추가 중...")
        
        for stock_name in missing_stocks:
            ticker = None
            all_tickers = stock.get_market_ticker_list(market="KOSPI")
            for t in all_tickers:
                if stock.get_market_ticker_name(t) == stock_name:
                    ticker = t
                    break
            
            new_row = {
                '종목명': stock_name,
                '시총순위': '-',
                '시가총액': 0,
                '시가총액_억원': '-',
                '티커': ticker if ticker else '-'
            }
            
            if ticker and ticker != '-':
                cap_info = df_all_cap[df_all_cap['티커'] == ticker]
                if not cap_info.empty:
                    new_row['시총순위'] = int(cap_info.iloc[0]['전체_시총순위'])
                    new_row['시가총액'] = cap_info.iloc[0]['시가총액']
                    new_row['시가총액_억원'] = int(cap_info.iloc[0]['시가총액'] / 100000000)
            
            for ratio_col, period_name in [('외국인비중_단기', '2주'), ('외국인비중_중기', '3개월'), ('외국인비중_장기', '1년')]:
                numerator_col = ratio_col.replace('외국인비중', '분자')
                denominator_col = ratio_col.replace('외국인비중', '분모')
                
                if period_name in period_data and not period_data[period_name].empty:
                    stock_net = period_data[period_name][period_data[period_name]['종목명'] == stock_name]
                    if not stock_net.empty:
                        foreign_net = stock_net.iloc[0]['외국인순매수']
                        individual_net = stock_net.iloc[0]['개인순매수']
                        inst_net = stock_net.iloc[0]['기관순매수']
                        other_net = stock_net.iloc[0]['기타순매수']
                        total_activity = stock_net.iloc[0]['전체활동량']
                        
                        if total_activity > 1000000:
                            new_row[numerator_col] = "양수" if foreign_net >= 0 else "음수"
                            rest_sum = individual_net + inst_net + other_net
                            new_row[denominator_col] = "양수" if rest_sum >= 0 else "음수"
                            ratio = (foreign_net / total_activity) * 100
                            new_row[ratio_col] = round(ratio, 2)
                        else:
                            new_row[ratio_col] = "-"
                            new_row[numerator_col] = "-"
                            new_row[denominator_col] = "-"
                    else:
                        new_row[ratio_col] = "-"
                        new_row[numerator_col] = "-"
                        new_row[denominator_col] = "-"
                else:
                    new_row[ratio_col] = "-"
                    new_row[numerator_col] = "-"
                    new_row[denominator_col] = "-"
            
            for period_name in periods.keys():
                if period_name in period_data and not period_data[period_name].empty:
                    rank_data = period_data[period_name][period_data[period_name]['종목명'] == stock_name]
                    if not rank_data.empty:
                        rank = rank_data.iloc[0]['순위']
                        new_row[period_name] = rank if rank <= 30 else None
                    else:
                        new_row[period_name] = None
                else:
                    new_row[period_name] = None
            
            df_master = pd.concat([df_master, pd.DataFrame([new_row])], ignore_index=True)
    
    # 5. 평가 계산
    print("\n5️⃣ 외국인 단기/중기/장기 평가 계산 중...")
    
    MISSING_PENALTY = 31
    df_eval = df_master.copy()
    
    for col in ['1일', '3일', '1주', '2주', '1개월', '3개월', '6개월', '1년']:
        df_eval[col] = pd.to_numeric(df_eval[col], errors='coerce').fillna(MISSING_PENALTY)
    
    df_eval['단기합산'] = df_eval['1일'] + df_eval['3일'] + df_eval['1주'] + df_eval['2주']
    df_eval['중기합산'] = df_eval['1개월'] + df_eval['3개월']
    df_eval['장기합산'] = df_eval['6개월'] + df_eval['1년']
    
    df_eval['외국인_단기평가'] = df_eval['단기합산'].rank(method='min').astype(int)
    df_eval['외국인_중기평가'] = df_eval['중기합산'].rank(method='min').astype(int)
    df_eval['외국인_장기평가'] = df_eval['장기합산'].rank(method='min').astype(int)
    
    df_master['외국인_단기평가'] = df_eval['외국인_단기평가']
    df_master['외국인_중기평가'] = df_eval['외국인_중기평가']
    df_master['외국인_장기평가'] = df_eval['외국인_장기평가']
    
    print("✅ 평가 완료")
    
    # 6. 주가 변동률 계산
    df_master = calculate_price_changes(df_master, end_date_str)
    
    # 7. 최종 칼럼 순서
    final_columns = ['종목명', '시총순위', '시가총액_억원']
    
    final_columns += ['외국인비중_단기', '분자_단기', '분모_단기', '주가변동_단기']
    final_columns += ['외국인비중_중기', '분자_중기', '분모_중기', '주가변동_중기']
    final_columns += ['외국인비중_장기', '분자_장기', '분모_장기', '주가변동_장기']
    
    final_columns += ['외국인_단기평가', '외국인_중기평가', '외국인_장기평가']
    
    for period in ['1일', '3일', '1주', '2주', '1개월', '3개월', '6개월', '1년']:
        final_columns.append(period)
        final_columns.append(f'주가변동_{period}')
    
    df_final = df_master[final_columns].copy()
    df_final = df_final.fillna('-')
    
    # 정렬
    print("\n7️⃣ 정렬 중...")
    
    df_final['외국인비중_단기_정렬용'] = df_final['외국인비중_단기'].apply(
        lambda x: float(x) if x != '-' else -999
    )
    
    df_final['시총순위_정렬용'] = df_final['시총순위'].apply(
        lambda x: int(x) if isinstance(x, int) or (isinstance(x, str) and x != '-') else 9999
    )
    
    df_final = df_final.sort_values(
        ['외국인비중_단기_정렬용', '시총순위_정렬용'],
        ascending=[False, True]
    )
    
    df_final = df_final.drop(['외국인비중_단기_정렬용', '시총순위_정렬용'], axis=1).reset_index(drop=True)
    
    print(f"✅ 정렬 완료 (외국인비중_단기↓ → 시총순위↑)")
    print(f"\n✅ 통합 테이블 완성: {len(df_final)}개 종목")
    
    # 8. 미리보기
    print("\n" + "=" * 80)
    print("📊 결과 미리보기 (상위 5개)")
    print("=" * 80)
    display_cols = ['종목명', '시총순위',
                    '외국인비중_단기', '주가변동_단기',
                    '외국인비중_중기', '주가변동_중기']
    print(df_final[display_cols].head(5).to_string(index=False))
    
    # 9. 데이터 저장
    print("\n" + "=" * 80)
    print("💾 데이터 저장 중...")
    print("=" * 80)
    
    # JSON 저장
    json_data = {
        "analysis_date": report_date,
        "timestamp": datetime.now().isoformat(),
        "total_stocks": len(df_final),
        "data": df_final.to_dict('records')
    }
    save_to_json(json_data, f'foreign_analysis_{end_date_str}.json')
    
    # Excel 저장
    save_to_excel(df_final, f'foreign_analysis_{end_date_str}.xlsx')
    
    # Markdown 저장
    save_to_markdown(df_final, report_date, f'foreign_analysis_{end_date_str}.md')
    
    # 10. Telegram 요약 전송
    print("\n" + "=" * 80)
    print("📤 Telegram 요약 전송 중...")
    print("=" * 80)
    
    summary = f"📊 <b>외국인 순매수 + 주가 분석</b>\n\n"
    summary += f"📅 분석일: {report_date}\n"
    summary += f"📈 분석 종목: {len(df_final)}개\n\n"
    summary += "<b>상위 5개 종목</b>\n"
    
    for idx, row in df_final.head(5).iterrows():
        summary += f"\n{idx+1}. <b>{row['종목명']}</b>\n"
        summary += f"   외국인비중(단기): {row['외국인비중_단기']}%\n"
        summary += f"   주가변동(단기): {row['주가변동_단기']}%\n"
        summary += f"   시총순위: {row['시총순위']}\n"
    
    summary += f"\n💾 상세 데이터: GitHub Repository 참조"
    
    result = send_telegram_message(summary)
    if result and result.get('ok'):
        print("✅ Telegram 전송 성공")
    else:
        print("⚠️ Telegram 전송 실패 (환경변수 확인)")
    
    print("\n" + "=" * 80)
    print("✅ 완료!")
    print("=" * 80)
    
    return df_final

if __name__ == "__main__":
    df_result = main()
