import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.font_manager as fm
import os
from collections import Counter

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# 폰트 경로 찾기
def find_korean_font():
    korean_fonts = ['NanumGothic', 'Malgun Gothic', 'AppleGothic', 'NanumBarunGothic']
    for font in korean_fonts:
        font_list = [f for f in fm.findSystemFonts() if font in f]
        if font_list:
            return font_list[0]
    return fm.findfont(fm.FontProperties(family='sans-serif'))

# 데이터 로드
def load_data():
    try:
        df = pd.read_csv('data/kyobo_book_sentiment_analysis.csv')
        return df
    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {e}")
        return None

# 워드클라우드 생성
def create_wordcloud(text_dict, title, output_path, font_path):
    wordcloud = WordCloud(
        font_path=font_path,
        width=800,
        height=400,
        background_color='white',
        max_words=100,
        relative_scaling=0.5,
        random_state=42
    ).generate_from_frequencies(text_dict)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16, pad=20, fontfamily='NanumGothic')
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def process_keywords(keywords_series):
    # 키워드 텍스트를 분리하고 빈도수 계산
    all_keywords = []
    for keywords in keywords_series:
        if isinstance(keywords, str):
            all_keywords.extend(keywords.split('|'))
    
    # 빈도수 계산 및 상위 100개 선택
    keyword_freq = Counter(all_keywords)
    return dict(keyword_freq.most_common(100))

def main():
    # 폰트 경로 설정
    font_path = find_korean_font()
    print(f"사용할 폰트 경로: {font_path}")

    # 데이터 로드
    df = load_data()
    if df is None:
        return

    # 감성점수 기준으로 상위/하위 20개 도서 선정
    df['도서_감성평균'] = df.groupby('도서코드')['감성점수'].transform('mean')
    top_20_books = df.sort_values('도서_감성평균', ascending=False)['도서코드'].unique()[:20]
    bottom_20_books = df.sort_values('도서_감성평균')['도서코드'].unique()[:20]

    # 긍정/부정 리뷰 키워드 추출
    positive_reviews = df[(df['도서코드'].isin(top_20_books)) & (df['감성'] == '긍정')]
    negative_reviews = df[(df['도서코드'].isin(bottom_20_books)) & (df['감성'] == '부정')]

    # 워드클라우드 생성
    os.makedirs('result/images', exist_ok=True)
    
    positive_keywords = process_keywords(positive_reviews['키워드'])
    negative_keywords = process_keywords(negative_reviews['키워드'])
    
    create_wordcloud(
        positive_keywords,
        '긍정적 리뷰의 주요 키워드',
        'result/images/positive_wordcloud.png',
        font_path
    )
    
    create_wordcloud(
        negative_keywords,
        '부정적 리뷰의 주요 키워드',
        'result/images/negative_wordcloud.png',
        font_path
    )

    print("워드클라우드 생성 완료!")

if __name__ == "__main__":
    main() 