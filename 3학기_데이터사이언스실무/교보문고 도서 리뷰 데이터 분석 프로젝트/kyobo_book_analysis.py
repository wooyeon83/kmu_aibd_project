"""
교보문고 리뷰 감성분석 스크립트
- homework/data/kyobo_reviews 디렉토리의 리뷰 파일을 분석
- homework/data/kyobo_book_url.csv 파일의 도서 정보 활용
- LLM을 사용한 감성분석 결과를 CSV 파일로 저장
"""

import os
import glob
import pandas as pd
import numpy as np
import json
import re
import logging
import time
import random
from datetime import datetime
from tqdm import tqdm
import openai

# 디렉토리 생성
os.makedirs("result", exist_ok=True)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("result/review_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KyoboReviewAnalyzer:
    """교보문고 리뷰 데이터 감성분석 클래스"""
    
    def __init__(self, reviews_dir, book_info_file, output_file):
        """
        초기화 함수
        
        Args:
            reviews_dir: 리뷰 파일들이 저장된 디렉토리 경로
            book_info_file: 도서 정보가 포함된 CSV 파일 경로
            output_file: 분석 결과를 저장할 CSV 파일 경로
        """
        self.reviews_dir = reviews_dir
        self.book_info_file = book_info_file
        self.output_file = output_file
        self.book_info = {}  # 도서코드 -> 도서정보 매핑
        self.results = []  # 분석 결과 저장
        
        # OpenAI API 키 설정 (환경 변수에서 가져오거나 직접 설정)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            logger.warning("OpenAI API 키가 설정되지 않았습니다. 테스트 모드로 실행됩니다.")
        
        # LLM 모델 설정
        self.model = "gpt-3.5-turbo"
        
        # 감성분석 프롬프트 템플릿
        self.prompt_template = """
        다음은 도서에 대한 리뷰입니다. 이 리뷰의 감성을 분석해주세요.
        
        리뷰: {review}
        
        다음 형식의 JSON으로만 응답해주세요:
        {{
            "sentiment": "긍정" 또는 "부정" 또는 "중립",
            "score": -1부터 1 사이의 감성 점수(긍정: 0~1, 부정: -1~0, 중립: 0 부근),
            "keywords": [감성을 판단하는데 중요한 단어 또는 구문 3개],
            "summary": "리뷰의 핵심 내용을 한 문장으로 요약"
        }}
        
        JSON 형식으로만 응답해주세요.
        """
        
        logger.info("리뷰 분석기 초기화 완료")
    
    def load_book_info(self):
        """
        도서 정보 파일에서 도서코드와 제목 정보를 로드
        
        Returns:
            bool: 로드 성공 여부
        """
        try:
            logger.info(f"도서 정보 파일 로드 중: {self.book_info_file}")
            
            # CSV 파일 읽기
            df = pd.read_csv(self.book_info_file)
            
            # URL에서 도서코드 추출
            if '상세페이지 URL' in df.columns:
                logger.info("상세페이지 URL에서 도서코드 추출 시도")
                for idx, row in df.iterrows():
                    url = row['상세페이지 URL']
                    # URL에서 도서코드 추출 (예: https://product.kyobobook.co.kr/detail/S000001952246)
                    match = re.search(r'/detail/([A-Za-z0-9]+)', url)
                    if match:
                        book_code = match.group(1)
                        self.book_info[book_code] = {
                            '제목': row.get('도서 제목', f'제목 없음 ({book_code})'),
                            '리뷰 수': row.get('리뷰 수', 0)
                        }
            
            logger.info(f"도서 정보 로드 완료: {len(self.book_info)}개 항목")
            return len(self.book_info) > 0
            
        except Exception as e:
            logger.error(f"도서 정보 로드 중 오류: {str(e)}")
            return False
    
    def extract_book_code_from_filename(self, filename):
        """
        파일명에서 도서코드 추출
        
        Args:
            filename: 파일명
            
        Returns:
            str: 도서코드 또는 None
        """
        # 파일명 패턴: reviews_S000001234567_2023-12-31.csv 또는 다른 패턴
        match = re.search(r'_([A-Za-z0-9]+)_', filename)
        if match:
            return match.group(1)
        return None
    
    def get_book_title(self, book_code):
        """
        도서코드로 제목 조회
        
        Args:
            book_code: 도서코드
            
        Returns:
            str: 도서 제목
        """
        if book_code in self.book_info:
            return self.book_info[book_code]['제목']
        return f"알 수 없는 도서 ({book_code})"
    
    def analyze_sentiment(self, review_text):
        """
        LLM을 이용해 리뷰 감성 분석
        
        Args:
            review_text: 분석할 리뷰 텍스트
            
        Returns:
            dict: 감성분석 결과
        """
        if not openai.api_key:
            # API 키가 없는 경우 가상의 결과 반환 (테스트용)
            return self.simulate_sentiment_analysis(review_text)
        
        try:
            # 리뷰 텍스트 정제 (500자로 제한)
            if not isinstance(review_text, str):
                review_text = str(review_text)
            
            review_text = review_text[:500] if len(review_text) > 500 else review_text
            
            # 프롬프트 생성
            prompt = self.prompt_template.format(review=review_text)
            
            # OpenAI API 호출
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 도서 리뷰의 감성을 분석하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            # 응답 텍스트 추출
            result_text = response.choices[0].message.content.strip()
            
            # JSON 형태가 아닌 경우 처리
            if not result_text.startswith('{') or not result_text.endswith('}'):
                # JSON 부분만 추출 시도
                json_start = result_text.find('{')
                json_end = result_text.rfind('}')
                
                if json_start != -1 and json_end != -1:
                    result_text = result_text[json_start:json_end+1]
                else:
                    # 기본값 반환
                    return {
                        "sentiment": "중립",
                        "score": 0,
                        "keywords": ["분석 불가"],
                        "summary": "분석 불가"
                    }
            
            # JSON 파싱
            result = json.loads(result_text)
            return result
            
        except Exception as e:
            logger.error(f"감성분석 중 오류: {str(e)}")
            # 오류 발생 시 기본값 반환
            return {
                "sentiment": "오류",
                "score": 0,
                "keywords": ["오류 발생"],
                "summary": f"오류: {str(e)}"
            }
    
    def simulate_sentiment_analysis(self, review_text):
        """
        API 키가 없을 때 감성분석 시뮬레이션 (테스트용)
        
        Args:
            review_text: 분석할 리뷰 텍스트
            
        Returns:
            dict: 가상의 감성분석 결과
        """
        # 간단한 감성 분석 규칙 (실제 분석과는 다름)
        positive_words = ['좋', '훌륭', '추천', '최고', '재미', '만족', '행복']
        negative_words = ['별로', '실망', '후회', '싫', '나쁨', '불만', '최악']
        
        # 긍정/부정 단어 수 계산
        positive_count = sum([1 for word in positive_words if word in str(review_text)])
        negative_count = sum([1 for word in negative_words if word in str(review_text)])
        
        # 감성 결정
        if positive_count > negative_count:
            sentiment = "긍정"
            score = min(0.5 + (positive_count - negative_count) * 0.1, 1.0)
            keywords = [word for word in positive_words if word in str(review_text)][:3]
        elif negative_count > positive_count:
            sentiment = "부정"
            score = max(-0.5 - (negative_count - positive_count) * 0.1, -1.0)
            keywords = [word for word in negative_words if word in str(review_text)][:3]
        else:
            sentiment = "중립"
            score = 0.0
            keywords = ["중립적", "보통", "평범"]
        
        # 키워드 부족한 경우 보완
        while len(keywords) < 3:
            keywords.append("기타")
        
        return {
            "sentiment": sentiment,
            "score": score,
            "keywords": keywords,
            "summary": f"이 리뷰는 {sentiment}적인 내용입니다. (시뮬레이션)"
        }
    
    def process_reviews(self, max_files=None, max_reviews_per_file=10):
        """
        리뷰 파일들을 처리하여 감성분석 수행
        
        Args:
            max_files: 처리할 최대 파일 수 (None이면 모두 처리)
            max_reviews_per_file: 각 파일에서 분석할 최대 리뷰 수
            
        Returns:
            bool: 처리 성공 여부
        """
        try:
            # 도서 정보 로드
            if not self.book_info:
                if not self.load_book_info():
                    return False
            
            # 리뷰 파일 목록 가져오기
            review_files = glob.glob(os.path.join(self.reviews_dir, "*.csv"))
            
            if not review_files:
                logger.warning(f"리뷰 파일을 찾을 수 없음: {self.reviews_dir}")
                return False
            
            logger.info(f"총 {len(review_files)}개 리뷰 파일 발견")
            
            # 이미 결과 파일이 있는 경우 로드
            if os.path.exists(self.output_file):
                try:
                    existing_results = pd.read_csv(self.output_file)
                    self.results = existing_results.to_dict('records')
                    logger.info(f"기존 분석 결과 로드: {len(self.results)}개 항목")
                except Exception as e:
                    logger.error(f"기존 결과 로드 중 오류: {str(e)}")
            
            # 이미 처리된 파일/리뷰 확인
            processed_reviews = set()
            if self.results:
                for result in self.results:
                    if '파일명' in result and '리뷰번호' in result:
                        key = f"{result['파일명']}_{result['리뷰번호']}"
                        processed_reviews.add(key)
            
            # 파일 처리
            if max_files and max_files < len(review_files):
                review_files = review_files[:max_files]
            
            for file_idx, file_path in enumerate(review_files):
                file_name = os.path.basename(file_path)
                logger.info(f"파일 처리 중 ({file_idx+1}/{len(review_files)}): {file_name}")
                
                # 도서코드 추출
                book_code = self.extract_book_code_from_filename(file_name)
                if not book_code:
                    logger.warning(f"파일명에서 도서코드를 추출할 수 없음: {file_name}")
                    continue
                
                # 도서 제목 가져오기
                book_title = self.get_book_title(book_code)
                
                try:
                    # 리뷰 데이터 로드
                    reviews_df = pd.read_csv(file_path)
                    
                    if reviews_df.empty:
                        logger.warning(f"빈 리뷰 파일: {file_name}")
                        continue
                    
                    # 필수 컬럼 확인
                    if '리뷰내용' not in reviews_df.columns:
                        logger.warning(f"리뷰내용 컬럼이 없음: {file_name}")
                        continue
                    
                    # 리뷰 샘플링 (최대 개수 제한)
                    if max_reviews_per_file and len(reviews_df) > max_reviews_per_file:
                        reviews_df = reviews_df.sample(max_reviews_per_file, random_state=42)
                    
                    # 각 리뷰 처리
                    for idx, row in tqdm(reviews_df.iterrows(), total=len(reviews_df), desc=f"분석 중: {file_name}"):
                        # 이미 처리된 리뷰인지 확인
                        review_id = row.get('리뷰번호', str(idx))
                        review_key = f"{file_name}_{review_id}"
                        
                        if review_key in processed_reviews:
                            continue
                        
                        # 리뷰 내용 확인
                        review_text = row.get('리뷰내용', '')
                        if not isinstance(review_text, str) or not review_text.strip():
                            continue
                        
                        # 리뷰 메타데이터
                        reviewer = row.get('회원ID', '')
                        date = row.get('작성일시', '')
                        rating = row.get('평점', 0)
                        
                        # 감성 분석
                        sentiment_result = self.analyze_sentiment(review_text)
                        
                        # 결과 저장
                        result = {
                            '파일명': file_name,
                            '도서코드': book_code,
                            '도서제목': book_title,
                            '리뷰번호': review_id,
                            '회원ID': reviewer,
                            '작성일시': date,
                            '평점': rating,
                            '리뷰내용': review_text[:100] + ('...' if len(review_text) > 100 else ''),
                            '감성': sentiment_result.get('sentiment', ''),
                            '감성점수': sentiment_result.get('score', 0),
                            '키워드': ', '.join(sentiment_result.get('keywords', [])),
                            '요약': sentiment_result.get('summary', '')
                        }
                        
                        self.results.append(result)
                        processed_reviews.add(review_key)
                        
                        # API 요청 사이에 대기 (1-2초)
                        time.sleep(random.uniform(1, 2))
                    
                    # 각 파일 처리 후 중간 결과 저장
                    self.save_results()
                    
                except Exception as e:
                    logger.error(f"파일 처리 중 오류: {file_name} - {str(e)}")
            
            # 최종 결과 저장
            self.save_results()
            logger.info(f"모든 리뷰 처리 완료: {len(self.results)}개 항목")
            return True
            
        except Exception as e:
            logger.error(f"리뷰 처리 중 오류: {str(e)}")
            # 오류 발생 시에도 중간 결과 저장
            if self.results:
                self.save_results()
            return False
    
    def save_results(self):
        """분석 결과를 CSV 파일로 저장"""
        try:
            if not self.results:
                logger.warning("저장할 결과가 없습니다.")
                return
            
            df = pd.DataFrame(self.results)
            df.to_csv(self.output_file, index=False, encoding='utf-8-sig')
            logger.info(f"결과 저장 완료: {self.output_file} ({len(self.results)}개 항목)")
            
        except Exception as e:
            logger.error(f"결과 저장 중 오류: {str(e)}")


# 메인 실행 코드
if __name__ == "__main__":
    # 설정
    reviews_dir = "homework/data/kyobo_reviews"
    book_info_file = "homework/data/kyobo_book_url.csv"
    output_file = "result/kyobo_book_sentiment_analysis.csv"
    
    # 감성분석 객체 생성 및 실행
    analyzer = KyoboReviewAnalyzer(reviews_dir, book_info_file, output_file)
    
    # 모든 리뷰 처리 (필요에 따라 파일 수와 리뷰 수 제한 가능)
    # max_files=None: 모든 파일 처리
    # max_reviews_per_file=10: 각 파일에서 최대 10개 리뷰만 처리 (테스트용, 실제로는 더 많이 처리 가능)
    success = analyzer.process_reviews(max_files=None, max_reviews_per_file=None)
    
    if success:
        print(f"감성분석 완료! 결과가 {output_file}에 저장되었습니다.")
    else:
        print("감성분석 중 오류가 발생했습니다. 로그를 확인하세요.")