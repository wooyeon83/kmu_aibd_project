"""
교보문고 2024년 종합연간베스트 페이지 크롤링 스크립트
- 리뷰 수 500개 이상인 도서의 상세 페이지 URL 수집
- 도서 제목, 상세페이지 URL, 리뷰 수를 CSV 파일로 저장
"""

import os
import re
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import random

# 로깅 설정 - 파일과 콘솔에 함께 출력
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("kyobobook_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KyoboBookScraper:
    """교보문고 베스트셀러 도서 정보 스크래핑 클래스"""
    
    def __init__(self):
        """
        스크래퍼 초기화 - 웹드라이버 설정 및 기본 변수 초기화
        """
        # 결과 저장을 위한 리스트와 최소 리뷰 수 설정
        self.results = []
        self.min_review_count = 500
        self.initialize_driver()
        
        logger.info("스크래퍼 초기화 완료")
        
    def initialize_driver(self):
        """웹드라이버 초기화 - 세션 무효화 문제 해결을 위해 별도 메서드로 분리"""
        # 웹드라이버 옵션 설정
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")  # 헤드리스 모드 비활성화(문제 해결을 위해)
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 감지 방지
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 관련 플래그 제거
        self.chrome_options.add_experimental_option("useAutomationExtension", False)  # 자동화 확장 비활성화
        
        # 웹드라이버 초기화
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        
        # 타임아웃 설정 늘리기
        self.driver.set_page_load_timeout(60)
        
        # 자바스크립트 실행으로 WebDriver 특성 숨기기
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("웹드라이버 초기화 완료")

    def extract_review_count_method1(self, soup):
        """
        방법 1: review_desc 클래스를 가진 span 요소에서 리뷰 수 추출
        
        Args:
            soup: BeautifulSoup 객체
            
        Returns:
            int 또는 None: 리뷰 수 또는 추출 실패 시 None
        """
        try:
            review_element = soup.select_one('span.review_desc')
            if review_element:
                review_text = review_element.text.strip()
                count_match = re.search(r'(\d+)개의 리뷰', review_text)
                if count_match:
                    return int(count_match.group(1))
        except Exception as e:
            logger.error(f"방법 1 추출 오류: {str(e)}")
        return None

    def extract_review_count_method2(self, soup):
        """
        방법 2: 리뷰 관련 다른 클래스를 사용하여 리뷰 수 추출
        
        Args:
            soup: BeautifulSoup 객체
            
        Returns:
            int 또는 None: 리뷰 수 또는 추출 실패 시 None
        """
        try:
            # 다양한 클래스 선택자 시도
            selectors = [
                'div.review_klover_box span.review_count', 
                'span.kloverTotal', 
                'div.prod_review span',
                'div.prod_rating_area span.review_count'
            ]
            
            for selector in selectors:
                review_element = soup.select_one(selector)
                if review_element:
                    review_text = review_element.text.strip()
                    count_match = re.search(r'(\d+)', review_text)
                    if count_match:
                        return int(count_match.group(1))
        except Exception as e:
            logger.error(f"방법 2 추출 오류: {str(e)}")
        return None

    def extract_review_count_method3(self, soup):
        """
        방법 3: 텍스트 내용을 기반으로 모든 span 요소를 검색하여 리뷰 수 추출
        
        Args:
            soup: BeautifulSoup 객체
            
        Returns:
            int 또는 None: 리뷰 수 또는 추출 실패 시 None
        """
        try:
            # 모든 span 요소에서 리뷰 수 검색
            for span in soup.find_all('span'):
                text = span.text.strip()
                if '개의 리뷰' in text:
                    count_match = re.search(r'(\d+)개의 리뷰', text)
                    if count_match:
                        return int(count_match.group(1))
                # 또 다른 형식의 리뷰 표시 방법 대응
                elif '리뷰' in text:
                    count_match = re.search(r'리뷰\s*(\d+)', text)
                    if count_match:
                        return int(count_match.group(1))
        except Exception as e:
            logger.error(f"방법 3 추출 오류: {str(e)}")
        return None
    
    def extract_review_count_with_selenium(self):
        """
        방법 4: Selenium을 사용하여 리뷰 수 추출 - 동적으로 로드되는 요소에 유용
        
        Returns:
            int 또는 None: 리뷰 수 또는 추출 실패 시 None
        """
        try:
            # 다양한 선택자로 시도
            selectors = [
                'span.review_desc', 
                'div.klover_review_box span.review_count',
                'span.text.kloverTotal',
                'div.prod_rating_area span.review_count'
            ]
            
            for selector in selectors:
                try:
                    # 명시적 대기 추가
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    review_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    review_text = review_element.text.strip()
                    
                    if '개의 리뷰' in review_text:
                        count_match = re.search(r'(\d+)개의 리뷰', review_text)
                        if count_match:
                            return int(count_match.group(1))
                    else:
                        count_match = re.search(r'(\d+)', review_text)
                        if count_match:
                            return int(count_match.group(1))
                except (NoSuchElementException, TimeoutException):
                    continue
        except Exception as e:
            logger.error(f"Selenium 리뷰 수 추출 오류: {str(e)}")
        return None

    def get_book_title(self, soup):
        """
        도서 제목 추출 - 여러 방법 시도
        
        Args:
            soup: BeautifulSoup 객체
            
        Returns:
            str: 도서 제목 또는 추출 실패 메시지
        """
        try:
            # 방법 1: 일반적인 제목 요소
            title_element = soup.select_one('h1.prod_title')
            if title_element:
                return title_element.text.strip()
            
            # 방법 2: 다른 구조의 제목 요소
            title_element = soup.select_one('div.prod_title_box h1')
            if title_element:
                return title_element.text.strip()
                
            # 방법 3: 메타 데이터에서 제목 찾기
            meta_title = soup.select_one('meta[property="og:title"]')
            if meta_title and meta_title.get('content'):
                return meta_title.get('content').strip()
        except Exception as e:
            logger.error(f"BeautifulSoup 제목 추출 오류: {str(e)}")
        
        # 방법 4: Selenium으로 시도
        try:
            title_element = self.driver.find_element(By.CSS_SELECTOR, 'h1.prod_title')
            return title_element.text.strip()
        except Exception as e:
            logger.error(f"Selenium 제목 추출 오류: {str(e)}")
        
        return "제목 추출 실패"

    def is_driver_valid(self):
        """웹드라이버 세션이 유효한지 확인"""
        try:
            # 간단한 명령을 실행해서 세션 상태 확인
            self.driver.current_url
            return True
        except (InvalidSessionIdException, WebDriverException):
            return False

    def restart_driver_if_needed(self):
        """필요한 경우 드라이버 재시작"""
        if not self.is_driver_valid():
            logger.warning("세션이 무효화되었습니다. 드라이버를 재시작합니다.")
            try:
                self.driver.quit()
            except Exception:
                pass  # 이미 종료된 경우 무시
            
            self.initialize_driver()
            return True
        return False

    def get_page_with_retry(self, url, max_retries=5):
        """
        세션 무효화 문제를 처리하며 페이지 로드
        
        Args:
            url: 로드할 URL
            max_retries: 최대 재시도 횟수
            
        Returns:
            bool: 성공 여부
        """
        for retry in range(max_retries):
            try:
                # 드라이버 상태 확인 및 필요시 재시작
                if self.restart_driver_if_needed():
                    logger.info("드라이버 재시작 후 페이지 로드 시도")
                
                # 페이지 로드 시도
                logger.info(f"페이지 로드 시도 {retry+1}/{max_retries}: {url}")
                self.driver.get(url)
                
                # 충분한 로딩 시간 부여 (8~12초)
                time.sleep(random.uniform(8, 12))
                return True
                
            except InvalidSessionIdException as e:
                logger.error(f"세션 무효화 오류 발생 (시도 {retry+1}/{max_retries}): {str(e)}")
                self.restart_driver_if_needed()
                if retry < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                logger.error(f"페이지 로드 중 오류 발생 (시도 {retry+1}/{max_retries}): {str(e)}")
                self.restart_driver_if_needed()
                if retry < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
        
        return False

    def get_book_info(self, book_url):
        """
        각 도서의 상세 페이지에서 정보(제목, URL, 리뷰 수) 추출
        
        Args:
            book_url: 도서 상세 페이지 URL
            
        Returns:
            tuple: (도서 제목, URL, 리뷰 수)
        """
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                logger.info(f"도서 상세 페이지 방문: {book_url} (시도 {retry_count+1}/{max_retries})")
                
                # 세션 무효화 문제 처리하며 페이지 로드
                if not self.get_page_with_retry(book_url, max_retries=3):
                    retry_count += 1
                    if retry_count < max_retries:
                        continue
                    else:
                        return "페이지 로드 실패", book_url, 0
                
                # 페이지 HTML 가져오기
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # 도서 제목 가져오기
                book_title = self.get_book_title(soup)
                
                # 여러 방법으로 리뷰 수 추출 시도 (순차적으로 시도하며 성공하면 중단)
                review_count = None
                
                # 방법 1: span.review_desc 요소에서 추출
                review_count = self.extract_review_count_method1(soup)
                if review_count is not None:
                    logger.info(f"방법 1로 리뷰 수 추출 성공: {review_count}")
                    return book_title, book_url, review_count
                
                # 방법 2: 다른 클래스 선택자 시도
                review_count = self.extract_review_count_method2(soup)
                if review_count is not None:
                    logger.info(f"방법 2로 리뷰 수 추출 성공: {review_count}")
                    return book_title, book_url, review_count
                
                # 방법 3: 텍스트 기반 검색
                review_count = self.extract_review_count_method3(soup)
                if review_count is not None:
                    logger.info(f"방법 3로 리뷰 수 추출 성공: {review_count}")
                    return book_title, book_url, review_count
                
                # 방법 4: Selenium으로 시도
                review_count = self.extract_review_count_with_selenium()
                if review_count is not None:
                    logger.info(f"Selenium으로 리뷰 수 추출 성공: {review_count}")
                    return book_title, book_url, review_count
                
                # 모든 방법 실패 시 재시도
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"리뷰 수 추출 실패, 재시도 중... ({retry_count}/{max_retries})")
                    time.sleep(random.uniform(2, 4))
                    continue
                
                logger.warning(f"모든 방법으로 리뷰 수 추출 실패: {book_url}")
                return book_title, book_url, 0
                
            except InvalidSessionIdException as e:
                logger.error(f"도서 정보 추출 중 세션 무효화 오류: {str(e)}")
                self.restart_driver_if_needed()
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(random.uniform(3, 5))
                    continue
                
            except Exception as e:
                logger.error(f"도서 정보 추출 중 오류 발생: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"오류 발생, 재시도 중... ({retry_count}/{max_retries})")
                    time.sleep(random.uniform(3, 5))
                    continue
                
        return "오류", book_url, 0

    def scrape_bestseller_list(self):
        """
        종합연간베스트 페이지에서 도서 목록을 스크랩하고 리뷰 수가 500개 이상인 도서 정보만 저장
        """
        try:
            # 1~10 페이지 순회
            for page in range(1, 11):
                # 직접 URL을 사용하여 요청
                url = f"https://store.kyobobook.co.kr/bestseller/total/annual?page={page}"
                logger.info(f"페이지 방문: {url} ({page}/10)")
                
                # 세션 무효화 문제 처리하며 페이지 로드
                if not self.get_page_with_retry(url, max_retries=5):
                    logger.error(f"페이지 {page} 로드 실패, 다음 페이지로 넘어갑니다.")
                    continue
                
                # 페이지가 로드되면 도서 링크 추출
                logger.info(f"페이지 {page} 로드 성공, 도서 링크 추출 시작")
                
                # 도서 링크 추출 전략들
                book_urls = []
                
                # 전략 1: Selenium으로 prod_link 클래스를 가진 a 태그 찾기
                try:
                    book_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.prod_link')
                    if book_elements:
                        book_urls = [element.get_attribute('href') for element in book_elements if element.get_attribute('href')]
                        logger.info(f"전략 1로 {len(book_urls)}개의 도서 URL 추출")
                except Exception as e:
                    logger.error(f"전략 1 실패: {str(e)}")
                
                # 전략 2: Selenium으로 다른 선택자 시도
                if not book_urls:
                    try:
                        book_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.prod_item a[href*="detail"]')
                        book_urls = [element.get_attribute('href') for element in book_elements if element.get_attribute('href')]
                        logger.info(f"전략 2로 {len(book_urls)}개의 도서 URL 추출")
                    except Exception as e:
                        logger.error(f"전략 2 실패: {str(e)}")
                
                # 전략 3: BeautifulSoup 사용
                if not book_urls:
                    try:
                        page_source = self.driver.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')
                        book_elements = soup.select('div.prod_item a.prod_link, div.prod_item a[href*="detail"]')
                        book_urls = [element.get('href') for element in book_elements if element.get('href')]
                        logger.info(f"전략 3으로 {len(book_urls)}개의 도서 URL 추출")
                    except Exception as e:
                        logger.error(f"전략 3 실패: {str(e)}")
                
                # URL 정규화 (상대 경로를 절대 경로로 변환)
                book_urls = [url if url.startswith('http') else f"https://store.kyobobook.co.kr{url}" for url in book_urls]
                
                # URL이 없으면 다음 페이지로
                if not book_urls:
                    logger.warning(f"페이지 {page}에서 도서 URL을 찾을 수 없습니다.")
                    continue
                    
                logger.info(f"페이지 {page}에서 {len(book_urls)}개의 도서 URL 추출 완료")
                
                # 각 도서의 상세 정보 추출
                for i, book_url in enumerate(book_urls):
                    try:
                        logger.info(f"도서 정보 추출 중 ({i+1}/{len(book_urls)}): {book_url}")
                        
                        # 세션 무효화 확인 및 필요시 재시작
                        if self.restart_driver_if_needed():
                            logger.info("드라이버 재시작 후 도서 정보 추출 시도")
                        
                        book_title, url, review_count = self.get_book_info(book_url)
                        
                        # 리뷰 수가 500개 이상인 경우만 저장
                        if review_count >= self.min_review_count:
                            self.results.append({
                                '도서 제목': book_title,
                                '상세페이지 URL': url,
                                '리뷰 수': review_count
                            })
                            logger.info(f"저장 대상: {book_title} (리뷰 수: {review_count})")
                        else:
                            logger.info(f"저장 제외: {book_title} (리뷰 수: {review_count})")
                            
                        # 서버 부하를 줄이기 위한 랜덤 대기 (3~5초)
                        time.sleep(random.uniform(3, 5))
                        
                    except InvalidSessionIdException:
                        logger.error("도서 정보 추출 중 세션 무효화 오류 발생")
                        self.restart_driver_if_needed()
                        
                    except Exception as e:
                        logger.error(f"도서 정보 추출 중 오류: {str(e)}")
                        continue
                
                # 진행상황 저장 (페이지마다 중간 결과 저장)
                self.save_results(f"kyobo_book_url_page_{page}.csv")
                
                # 다음 페이지 방문 전 충분한 대기 (8~15초)
                logger.info(f"페이지 {page} 처리 완료, 다음 페이지로 이동 전 대기 중...")
                time.sleep(random.uniform(8, 15))
                
        except Exception as e:
            logger.error(f"베스트셀러 리스트 스크랩 중 오류: {str(e)}")
        
        finally:
            # 최종 결과를 CSV 파일로 저장
            self.save_results()
            # 브라우저 종료
            try:
                self.driver.quit()
            except Exception:
                pass

    def save_results(self, filename="kyobo_book_url.csv"):
        """
        수집한 결과를 CSV 파일로 저장
        
        Args:
            filename: 저장할 파일명
        """
        try:
            # 결과가 없는 경우 처리
            if not self.results:
                logger.warning(f"{filename}에 저장할 결과가 없습니다.")
                return
                
            # DataFrame 생성 및 CSV 저장
            df = pd.DataFrame(self.results)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logger.info(f"총 {len(self.results)}개의 도서 정보가 {filename}에 저장되었습니다.")
        except Exception as e:
            logger.error(f"결과 저장 중 오류: {str(e)}")

def main():
    """
    메인 함수: 스크래퍼 초기화 및 실행
    """
    logger.info("교보문고 2024년 종합연간베스트 도서 스크래핑 시작")
    scraper = KyoboBookScraper()
    scraper.scrape_bestseller_list()
    logger.info("교보문고 2024년 종합연간베스트 도서 스크래핑 완료")

if __name__ == "__main__":
    main()