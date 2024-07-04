from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

@app.route('/')
def home():
    url = "https://finance.naver.com/"
    response = requests.get(url, headers=headers)
    response.encoding = 'euc-kr'
    soup = BeautifulSoup(response.text, 'html.parser')
    kospi_index = soup.select_one('.kospi_area')

    # 뉴스 정보 불러오기
    news_url = "https://finance.naver.com/news/mainnews.naver"
    response_news = requests.get(news_url, headers=headers)
    response_news.encoding = 'euc-kr'
    soup_news = BeautifulSoup(response_news.text, 'html.parser')
    # 수정된 셀렉터 부분
    news_list = soup_news.select('.newsList > li')
    news_articles = []
    for news in news_list:
        thumb_url = news.select_one('.thumb img')['src'] if news.select_one('.thumb img') else None
        title = news.select_one('.articleSubject').text.strip()
        link = news.select_one('.articleSubject a')['href']
        summary = news.select_one('.articleSummary').text.strip() if news.select_one('.articleSummary') else ''
        
        news_articles.append({
            'thumb_url': thumb_url,
            'title': title,
            'link': link,
            'summary': summary
        })

    return render_template('index.html', kospi_index=kospi_index, news_articles=news_articles)


if __name__ == '__main__':
    app.run(debug=True)
