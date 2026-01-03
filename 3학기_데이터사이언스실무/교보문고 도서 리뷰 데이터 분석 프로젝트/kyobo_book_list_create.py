"""
교보문고 도서 URL 데이터 처리 스크립트
- 중복 항목 제거
- URL에서 도서 코드 추출 및 컬럼 추가
- 처리된 데이터를 새 CSV 파일로 저장
"""

import os
import pandas as pd
import re
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("homework/data/data_processing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def extract_book_code(url):
    """
    URL에서 도서 코드를 추출하는 함수
    
    Args:
        url (str): 도서 상세 페이지 URL
        
    Returns:
        str: 추출된 도서 코드 또는 빈 문자열
    """
    try:
        # URL에서 마지막 부분 추출 시도 (예: https://product.kyobobook.co.kr/detail/S000001234567)
        match = re.search(r'/detail/([A-Za-z0-9]+)$', url)
        if match:
            return match.group(1)
        
        # 다른 형식의 URL에 대한 대비책
        match = re.search(r'[?&]barcode=([A-Za-z0-9]+)', url)
        if match:
            return match.group(1)
            
        # 추가 패턴
        match = re.search(r'[?&]goods_id=([A-Za-z0-9]+)', url)
        if match:
            return match.group(1)
            
        logger.warning(f"도서 코드를 추출할 수 없음: {url}")
        return ""
    except Exception as e:
        logger.error(f"도서 코드 추출 중 오류: {str(e)}")
        return ""

def process_kyobo_data():
    """
    교보문고 도서 URL 데이터 처리 함수
    - 중복 제거
    - 도서 코드 추출 및 추가
    - 결과 저장
    """
    try:
        # 디렉토리 확인 및 생성
        os.makedirs("homework/data", exist_ok=True)
        
        input_file = "homework/data/kyobo_book_url.csv"
        output_file = "homework/data/kyobo_book_list.csv"
        
        logger.info(f"파일 읽기 시작: {input_file}")
        
        # CSV 파일 읽기
        df = pd.read_csv(input_file)
        original_count = len(df)
        logger.info(f"원본 데이터 로드 완료: {original_count}개 항목")
        
        # 중복 확인 및 제거
        # '상세페이지 URL' 기준으로 중복 제거
        df = df.drop_duplicates(subset=['상세페이지 URL'])
        deduplicated_count = len(df)
        logger.info(f"중복 제거 완료: {original_count - deduplicated_count}개 중복 항목 제거됨")
        
        # 도서 코드 추출 및 컬럼 추가
        logger.info("도서 코드 추출 시작")
        df['도서코드'] = df['상세페이지 URL'].apply(extract_book_code)
        
        # 최종 데이터 저장
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"처리된 데이터 저장 완료: {output_file} ({deduplicated_count}개 항목)")
        
        # 간단한 통계 정보 출력
        missing_codes = df['도서코드'].isna().sum() + (df['도서코드'] == '').sum()
        logger.info(f"도서코드 추출 결과: 성공 {deduplicated_count - missing_codes}개, 실패 {missing_codes}개")
        
        return True
    
    except FileNotFoundError:
        logger.error(f"파일을 찾을 수 없음: {input_file}")
        return False
    except Exception as e:
        logger.error(f"데이터 처리 중 오류 발생: {str(e)}")
        return False

def main():
    """메인 함수"""
    logger.info("교보문고 도서 데이터 처리 시작")
    success = process_kyobo_data()
    status = "성공" if success else "실패"
    logger.info(f"교보문고 도서 데이터 처리 {status}")

if __name__ == "__main__":
    main()