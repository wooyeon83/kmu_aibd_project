"""
교보문고 도서 리뷰 추출 스크립트
- homework/data/kyobo_book_list.csv 파일에서 도서 코드를 읽어옴
- ch03/ref/scraper_kyobo.py의 함수를 활용하여 각 도서의 리뷰 정보 추출
- 추출된 리뷰 정보를 homework/data/kyobo_reviews/ 폴더에 저장
"""

import os
import sys
import pandas as pd
import logging
from datetime import datetime
import time
import random

# ch03/ref 경로를 시스템 경로에 추가하여 scraper_kyobo 모듈을 임포트할 수 있게 함
sys.path.append(os.path.abspath('ch03/ref'))
from scraper_kyobo import scrap_review

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("homework/data/kyobo_reviews_extraction.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def extract_reviews_from_booklist():
    """
    kyobo_book_list.csv 파일에서 도서 코드를 읽어와 리뷰 정보 추출
    """
    try:
        # 디렉토리 확인 및 생성
        os.makedirs("homework/data/kyobo_reviews", exist_ok=True)
        
        input_file = "homework/data/kyobo_book_list.csv"
        output_dir = "homework/data/kyobo_reviews"
        
        logger.info(f"파일 읽기 시작: {input_file}")
        
        # CSV 파일 읽기
        df = pd.read_csv(input_file)
        total_books = len(df)
        logger.info(f"도서 데이터 로드 완료: 총 {total_books}권")
        
        # 도서 코드가 없는 항목 필터링
        df = df[df['도서코드'].notna() & (df['도서코드'] != '')]
        valid_books = len(df)
        
        if valid_books < total_books:
            logger.warning(f"도서 코드가 없는 항목 {total_books - valid_books}개 제외됨")
        
        # 리뷰 추출 결과 추적
        success_count = 0
        empty_count = 0
        failure_count = 0
        
        # 각 도서에 대해 리뷰 추출
        for idx, row in df.iterrows():
            book_code = row['도서코드']
            book_title = row['도서 제목']
            
            logger.info(f"도서 리뷰 추출 시작 ({idx+1}/{valid_books}): {book_title} (코드: {book_code})")
            
            try:
                # scrap_review 함수를 사용하여 리뷰 추출
                # output_path를 지정하여 리뷰를 CSV 파일로 저장
                result = scrap_review(book_code, output_path=output_dir)
                
                # 결과 메시지 확인으로 성공/실패 여부 판단
                if "저장되었습니다" in result:
                    review_count = int(result.split('총 ')[1].split('개의 리뷰')[0])
                    if review_count > 0:
                        success_count += 1
                        logger.info(f"리뷰 추출 성공: {book_title} - {review_count}개의 리뷰")
                    else:
                        empty_count += 1
                        logger.warning(f"리뷰 없음: {book_title}")
                else:
                    failure_count += 1
                    logger.error(f"리뷰 추출 실패: {book_title} - {result}")
                
                # 서버 부하 방지를 위한 랜덤 대기 시간 (2~5초)
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                failure_count += 1
                logger.error(f"리뷰 추출 중 오류 발생: {book_title} - {str(e)}")
                time.sleep(random.uniform(2, 5))  # 오류 발생 시에도 대기
                
            # 진행 상황 로깅 (5권마다)
            if (idx + 1) % 5 == 0:
                logger.info(f"진행 상황: {idx+1}/{valid_books} 완료 (성공: {success_count}, 빈 리뷰: {empty_count}, 실패: {failure_count})")
        
        # 최종 결과 로깅
        logger.info("=" * 50)
        logger.info(f"리뷰 추출 완료")
        logger.info(f"총 처리 도서: {valid_books}권")
        logger.info(f"성공: {success_count}권 (리뷰 있음)")
        logger.info(f"빈 리뷰: {empty_count}권 (리뷰 없음)")
        logger.info(f"실패: {failure_count}권 (오류 발생)")
        logger.info("=" * 50)
        
        return True
    
    except FileNotFoundError:
        logger.error(f"파일을 찾을 수 없음: {input_file}")
        return False
    except Exception as e:
        logger.error(f"리뷰 추출 중 오류 발생: {str(e)}")
        return False

def main():
    """메인 함수"""
    start_time = datetime.now()
    logger.info("교보문고 도서 리뷰 추출 시작")
    success = extract_reviews_from_booklist()
    end_time = datetime.now()
    duration = end_time - start_time
    
    status = "성공" if success else "실패"
    logger.info(f"교보문고 도서 리뷰 추출 {status}")
    logger.info(f"총 소요 시간: {duration}")

if __name__ == "__main__":
    main()