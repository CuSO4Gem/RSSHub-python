from bs4 import BeautifulSoup    
import requests
import arrow
import re
from rsshub.utils import DEFAULT_HEADERS

MAX_ITEMS = 6

domain = 'https://www.ndrc.gov.cn'
categoryMap = {
    # 'all': '/xxgk/',
    'fzggwl': '/xxgk/zcfb/fzggwl/',
    'ghxwj': '/xxgk/zcfb/ghxwj/',
    'ghwb': '/xxgk/zcfb/ghwb/',
    'gg': '/xxgk/zcfb/gg/',
    'tz': '/xxgk/zcfb/tz/',
}

titleMap = {
    # 'all': '发改委 - 全部',
    'fzggwl': '发改委 - 发展改革委令',
    'ghxwj': '发改委 - 规范性文件',
    'ghwb': '发改委 - 规范文本',
    'gg': '发改委 - 公告',
    'tz': '发改委 - 通知',
}

def parseRow(urlPrefix, devRow):
    aTagsWithHref = devRow.find('a', href=True)
    href = aTagsWithHref.get('href')
    link = urlPrefix + href
    title = aTagsWithHref.text.strip()
    timeStr = devRow.find('span').text.strip()
    pubData = arrow.get(timeStr, 'YYYY/MM/DD').isoformat()

    # 获取正文内容
    url = link
    response = requests.get(url, headers=DEFAULT_HEADERS)
    rspContent = response.content.decode('utf-8')
    soup = BeautifulSoup(rspContent, 'html.parser')
    content = soup.find('div', class_='article')

    return {
        'title': title,
        'link': link,
        'pubDate': pubData,
        'description': content,
    }


def getCategoryItems(category):
    url = domain + categoryMap[category]
    response = requests.get(url, headers=DEFAULT_HEADERS)
    content = response.content.decode('utf-8')

    soup = BeautifulSoup(content, 'html.parser')

    rows = soup.find('ul', class_='u-list').find_all('li', recursive=False)
    items = []

    itemCount = 0
    for row in rows:
        if 'empty' in row.get('class', []):
            continue
        if itemCount >= MAX_ITEMS:
            break
        itemCount += 1
        items.append(parseRow(url, row))
    
    return items

def ctx(category='fzggwl'):
    items = []
    items = getCategoryItems(category)

    return {
        'title' : titleMap[category],
        'link' : domain + categoryMap[category],
        'description' : titleMap[category],
        'items' : items,
    }