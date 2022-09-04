import requests
import bs4
from pprint import pprint
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

base_url = 'https://habr.com'
full_url = f'{base_url}/ru/all'

HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
'Connection': 'keep-alive',
'Cookie': 'hl=ru; fl=ru; _ga=GA1.2.204020777.1659128231; _ym_uid=16591282311005742073; _ym_d=1659128231; __gads=ID=706ffeaa414b90ea-22547adcdfcd00cf:T=1659128234:S=ALNI_MYUpMw_taANvQ9HrMTdS3B0hbvehg; habr_web_home_feed=/all/; _gid=GA1.2.1558690067.1662297810; _ym_isad=2',
'Host': 'habr.com',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0' }

def set_key_words_pattern():
    pattern = ''
    for keyword in KEYWORDS:
        pattern += f'{keyword}|'
    pattern = pattern[:-1]
    return pattern

def check_articles_preview(pattern):
    response = requests.get(full_url, headers=HEADERS)
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')

    for article in articles:
        meta_text = ''
        pre_content_text = ''

        username = article.find(class_='tm-user-info__username')
        meta_text += f'{username.text.strip()} '

        pub_data = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs.get('title')

        title_article_a = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').find('a')
        title_article_href = f"{base_url}{title_article_a.attrs.get('href')}"
        title_article = title_article_a.text.strip()

        meta_text += f'{title_article} '

        hubs = article.find_all(class_='tm-article-snippet__hubs-item')
        hubs_text_lst = [hub.text.strip() for hub in hubs]
        hubs_text = ' '.join(hubs_text_lst)

        meta_text += hubs_text

        if re.search(pattern, meta_text):
            print(f"{pub_data.split(',')[0]} - {title_article} - {title_article_href}")
        else:
            pre_content = article.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-2')

            if pre_content:
                pre_content_text += pre_content.text
            else:
                if article.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-1'):
                    pre_content_text += article.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-1').text
            if re.search(pattern, pre_content_text):
                print(f"{pub_data.split(',')[0]} - {title_article} - {title_article_href}")


if __name__ == '__main__':
    pattern = set_key_words_pattern()
    check_articles_preview(pattern)

