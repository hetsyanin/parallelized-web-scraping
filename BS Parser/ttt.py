import requests
from bs4 import BeautifulSoup as bs
import csv
from datetime import datetime
from multiprocessing import Pool
import sys


def get_html(url):
    r = requests.get(url)  # response

    return r.text  # returns html code


def get_all_links(html):
    soup = bs(html, 'lxml')
    item_headers = soup.find('div', class_='article').find_all('h3', class_='lister-item-header')
    links = []

    for h3 in item_headers:
        href = h3.find('a').get('href')
        link = 'https://www.imdb.com' + href
        links.append(link)

    return links


def get_nextpage_link(html):
    soup = bs(html, 'lxml')
    next_page = soup.find('div', class_='article').find('div', class_='desc')
    try:
        href = next_page.find('a', class_='lister-page-next next-page').get('href')
        next_link = 'https://www.imdb.com' + href
    except:
        next_link = '---exception---'

    return next_link


def check_exception(next_link):
    if next_link == '---exception---':
        parse(url.pop(0))


def get_page_data(html):
    soup = bs(html, 'lxml')

    try:
        title = soup.find('div', class_='title_wrapper').find('h1').next.strip()
    except:
        title = ''

    try:
        year = soup.find('span', id='titleYear').find('a').text.strip()
    except:
        year = ''

    try:
        genre = soup.find('div', class_='subtext').find('a').text.strip()
    except:
        genre = ''

    try:
        rating = soup.find('span', itemprop='ratingValue').text.strip()
    except:
        rating = ''

    data = {'title': title,
            'year': year,
            'genre': genre,
            'rating': rating}

    return data


def write_csv(data):
    # with open('imdb_multi.csv', 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow((data['title'],
    #                      data['year'],
    #                      data['genre'],
    #                      data['rating']))
    print(data['title'], data['year'], data['genre'], data['rating'], 'parsed')


def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def parse(url):
    html = get_html(url)
    next_page_link = get_nextpage_link(html)
    print(next_page_link)
    all_links = get_all_links(html)

    with Pool(4) as p:
        p.map(make_all, all_links)

    try:
        parse(next_page_link)
    except:
        check_exception(next_page_link)


def main():
    global start, url
    start = datetime.now()
    print(start)

    url = ['https://www.imdb.com/search/title/?countries=ao',
           'https://www.imdb.com/search/title/?countries=ly',
           'https://www.imdb.com/search/title/?countries=ad',
           'https://www.imdb.com/search/title/?countries=bi',
           'https://www.imdb.com/search/title/?countries=ao',
           'https://www.imdb.com/search/title/?countries=ao',
           'https://www.imdb.com/search/title/?countries=ao',
           # 'https://www.imdb.com/search/title/?countries=ao',
           # 'https://www.imdb.com/search/title/?countries=ao',
           # 'https://www.imdb.com/search/title/?countries=ly',
           ]

    parse(url.pop(0))

    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()
