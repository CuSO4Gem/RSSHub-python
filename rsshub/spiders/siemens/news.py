from bs4 import BeautifulSoup    
import requests
from rsshub.utils import DEFAULT_HEADERS


domain = 'https://w1.siemens.com.cn'

def parseRow(devRow):
    aTagsWithHref = devRow.select('a[href]')
    href = aTagsWithHref[0].get('href')
    link = domain + href
    title = aTagsWithHref[0].find('b').text.strip()

    content = ''
    contentTbTags = devRow.find('div', class_='p clearfix newList').find_all('td')
    for contentTbTag in contentTbTags:
        content += contentTbTag.text.strip()

    # print(aTagsWithHref[0].find('b')text.strip())

    item = {}
    item['title'] = title
    item['description'] = content
    item['link'] = link
    return item


def ctx(local=''):
    url = f'{domain}/news/news_articles/default.aspx'
    posts = requests.get(
        url,
        headers=DEFAULT_HEADERS,
    ).text

    soup = BeautifulSoup(posts, 'html.parser')
    items = []
    for devRow in soup.find_all('div', class_='row'):
        #  所有具备 **href** 属性的 <a> 标签
        item =  parseRow(devRow)
        items.append(item)

    print(items[0])

    return {
        'title' : 'Siemens News',
        'link' : f'{domain}/news/news_articles/default.aspx',
        'description' : 'Siemens News',
        'author': 'lin',
        'items': items,
    }
    