import urllib
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
from PIL import Image
import re
import argparse
import html

def google(s, query):
    print('-' * 30)
    print('\n谷歌')
    url_pattern = 'yuRUbf'
    title_pattern = 'LC20lb MBeuO DKV0Md'
    desc_pattern = 'VwiC3b yXK7lf lVm3ye r025kc hJNv6b'
    for start in range(0,20,10):  #搜索前20条
        URL = f"https://google.com/search?q={query}&start={start}"
        html=s.get(URL, proxies={'https': 'http://127.0.0.1:50078'}).text
        # print(html)
        
        bs=BeautifulSoup(html, "html.parser")
        urls=[bs.find_all('div',{'class':url_pattern})[i].find('a')['href'] for i in range(len(bs.find_all('div',{'class':url_pattern})))]
        titles=[bs.find_all('h3',{'class':title_pattern})[i].text for i in range(len(bs.find_all('h3',{'class':title_pattern})))]
        descs=[bs.find_all('div',{'class':desc_pattern})[i].text for i in range(len(bs.find_all('div',{'class':desc_pattern})))]
        for i in range(min(min(len(urls),len(titles)),len(descs))):
            print('\n'.join([urls[i],titles[i],descs[i]]))
            print()

# def decode(string):
#     decoded_str = html.unescape(string)
#     # 将单引号替换为双引号，以符合 JSON 格式
#     json_str = decoded_str.replace("&#39;", "'").replace("'", '"')
#     # 解析 JSON 字符串
#     data = json.loads(json_str)
#     return data

def sougou_zhihu(s, query):
    print('-' * 30)
    print('\n搜狗知乎')
    for page in range(1,10):
        URL = f"https://www.sogou.com/sogou?query={query}&ie=utf8&pid=sogou-wsse-ff111e4a5406ed40&insite=zhihu.com&aria=0&w=&sut=1151&sst0=1640656254812&lkt=1%2C1640656254645%2C1640656254645&page={page}"
        html=s.get(URL).text

        bs=BeautifulSoup(html, "html.parser")
        urls=['https://www.sogou.com'+bs.find_all('h3',{'class':'vr-title'})[i].a['href'] for i in range(len(bs.find_all('h3',{'class':'vr-title'})))]
        titles=[bs.find_all('h3',{'class':'vr-title'})[i].text.strip() for i in range(len(bs.find_all('h3',{'class':'vr-title'})))]
        descs=[bs.find_all('p',{'class':'star-wiki'})[i].text.strip() for i in range(len(bs.find_all('p',{'class':'star-wiki'})))]    
        for i in range(min(min(len(urls),len(titles)),len(descs))):
            print('\n'.join([urls[i],titles[i],descs[i]]))
            print()

def bilibili(s, query):
    print('-' * 30)
    print('\nbilibili')

    title_pattern = 'bili-video-card__info--tit'
    url_pattern = 'bili-video-card__info--right'
    descs_pattern = 'bili-video-card__info--author'

    for page in range(1,5):
        URL=f"https://search.bilibili.com/all?keyword={query}&from_source=webtop_search&spm_id_from=333.851&page={page}"
        html=s.get(URL).text
        bs=BeautifulSoup(html, "html.parser")
        # print(html)

        titles=[bs.find_all('h3',{'class':title_pattern})[i]['title'] for i in range(len(bs.find_all('h3',{'class':title_pattern})))]
        urls=['https://'+bs.find_all('div',{'class':url_pattern})[i].find('a')['href'].strip('/') for i in range(len(bs.find_all('div',{'class':url_pattern})))]
        descs=['up: '+bs.find_all('span',{'class':descs_pattern })[0].text for i in range(len(bs.find_all('span',{'class':descs_pattern})))]
        for i in range(min(min(len(urls),len(titles)),len(descs))):
            print('\n'.join([urls[i],titles[i],descs[i]]))
            print()

def axriv(s, query):
    print('-' * 30)
    print('\narxiv')
    for start in range(1,100,50):
        URL = f"https://arxiv.org/search/?query={query}&searchtype=all&source=header&start={start}"
        html=s.get(URL).text

        bs=BeautifulSoup(html, "html.parser")
        urls=[bs.find_all('p',{'class':'list-title is-inline-block'})[i].a['href'] for i in range(len(bs.find_all('p',{'class':'list-title is-inline-block'})))]
        titles=[bs.find_all('p',{'class':'title is-5 mathjax'})[i].text.strip() for i in range(len(bs.find_all('p',{'class':'title is-5 mathjax'})))]
        descs=[bs.find_all('span',{'class':'abstract-short has-text-grey-dark mathjax'})[0].text.strip() for i in range(len(bs.find_all('span',{'class':'abstract-short has-text-grey-dark mathjax'})))]    
        for i in range(min(min(len(urls),len(titles)),len(descs))):
            print('\n'.join([urls[i],titles[i],descs[i]]))
            print()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, default='', help='搜索内容')
    args = parser.parse_args()

    if args.s == '':
        return

    s = requests.session()            # 爬虫主体对象
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})

    query = args.s.replace(' ', '+')
    google(s, query)
    sougou_zhihu(s, query)
    bilibili(s, query)
    axriv(s, query)

if __name__ == '__main__':
    main()