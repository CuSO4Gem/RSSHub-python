from bs4 import BeautifulSoup    
import requests
import arrow
import re
from rsshub.utils import DEFAULT_HEADERS


domain= { 'cn': 'https://w1.siemens.com.cn',
          'global': 'https://press.siemens.com',
        }

def parseRowCn(devRow):
    aTagsWithHref = devRow.select('a[href]')
    href = aTagsWithHref[0].get('href')
    link = domain["cn"] + href
    title = aTagsWithHref[0].find('b').text.strip()
    pubData = devRow.find('p').text.strip()

    content = ''
    contentTbTags = devRow.find('div', class_='p clearfix newList').find_all('td')
    for contentTbTag in contentTbTags:
        content += contentTbTag.text.strip()

    # print(aTagsWithHref[0].find('b')text.strip())

    item = {}
    item['title'] = title
    item['description'] = content
    item['link'] = link
    item['pubDate'] = arrow.get(pubData, "YYYY年M月D日").isoformat()
    return item

def ctxCn():
    url = f'{domain["cn"]}/news/news_articles/default.aspx'
    posts = requests.get(
        url,
        headers=DEFAULT_HEADERS,
    ).text

    soup = BeautifulSoup(posts, 'html.parser')
    items = []
    for devRow in soup.find_all('div', class_='row'):
        #  所有具备 **href** 属性的 <a> 标签
        item =  parseRowCn(devRow)
        items.append(item)

    return {
        'title' : 'Siemens News - CN',
        'link' : f'{domain["cn"]}/news/news_articles/default.aspx',
        'description' : 'Siemens News',
        'author': 'lin',
        'items': items,
    }

def parseRowGlobal(devRow):
    aTagsWithHref = devRow.select('a[href]')
    href = aTagsWithHref[0].get('href')
    link = domain["global"] + href

    title = aTagsWithHref[0].text.strip()
    content = devRow.find('div', class_='views-field views-field-field-press-teaser').text

    pubDataString = devRow.find('div', class_='search-result-footer-event-meta').text.strip()
    # 使用正则表达式匹配日期信息
    match = re.search(r'\d{2} \w{3} \d{4}', pubDataString)
    pubData = ''
    if match:
        date_str = match.group()
        pubData = arrow.get(date_str, "DD MMM YYYY").isoformat()
    
    item = {}
    item['title'] = title
    item['description'] = content
    item['link'] = link
    item['pubDate'] = pubData
    return item

    

def ctxGlobal():
    url = f'{domain["global"]}/global/en/press-search?facets_query='
    posts = requests.get(
        url,
        headers=DEFAULT_HEADERS,
    ).text

    soup = BeautifulSoup(posts, 'html.parser')
    items = []
    # for devRow in soup.find_all('div', class_='press-search-results-view-row content-type-c2-ct-press-feature views-row'):
    for devRow in soup.find_all('div', class_=re.compile(r'press-search-results-view-row content-type-c2-ct-press-')):
        print(devRow)
        item = parseRowGlobal(devRow)
        items.append(item)
    
    return {
        'title' : 'Siemens News - Global',
        'link' : f'{domain["global"]}/global/en/press-search',
        'description' : 'Siemens News',
        'author': 'lin',
        'items': items,
    }


def ctx(local=''):
    if local == "cn":
        return ctxCn()
    else:
        return ctxGlobal()