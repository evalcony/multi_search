from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
from PIL import Image
import re
import argparse
import html

# from slimit import ast
# from slimit.parser import Parser
# from slimit.visitors import nodevisitor
import esprima

def test_pattern(pattern, urls, titles, descs):
    if pattern:
        print(f'url {len(urls)}')
        print(f'titles {len(titles)}')
        print(f'descs {len(descs)}')

def google(s, query, test=False, rrange=20):
    result = []
    result.append('-' * 30)
    result.append('谷歌')

    url_pattern = 'yuRUbf'
    title_pattern = 'LC20lb MBeuO DKV0Md'
    desc_pattern = 'VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb'
    for start in range(0,rrange,10):  #搜索前20条
        URL = f"https://google.com/search?q={query}&start={start}"
        html=s.get(URL, proxies={'https': 'http://127.0.0.1:50078'}).text
        # print(html)
        
        bs=BeautifulSoup(html, "html.parser")
        urls=[bs.find_all('div',{'class':url_pattern})[i].find('a')['href'] for i in range(len(bs.find_all('div',{'class':url_pattern})))]
        titles=[bs.find_all('h3',{'class':title_pattern})[i].text for i in range(len(bs.find_all('h3',{'class':title_pattern})))]
        descs=[bs.find_all('div',{'class':desc_pattern})[i].text for i in range(len(bs.find_all('div',{'class':desc_pattern})))]
        test_pattern(test, urls, titles, descs)
        if not test:
            for i in range(min(min(len(urls),len(titles)),len(descs))):
                result.append('\n'.join([urls[i],titles[i],descs[i]]))
                result.append('')
    return result

# def decode(string):
#     decoded_str = html.unescape(string)
#     # 将单引号替换为双引号，以符合 JSON 格式
#     json_str = decoded_str.replace("&#39;", "'").replace("'", '"')
#     # 解析 JSON 字符串
#     data = json.loads(json_str)
#     return data

def sougou_zhihu(s, query, test=False, rrange=5):
    result = []
    result.append('-' * 30)
    result.append('搜狗知乎')
    # 这个提取的url不完整，无法使用
    # url_pattern = 'vr-title'
    # 这个是直接url
    url_pattern = 'r-sech ext_query r-sech-test_02 result_list click-better-sugg'
    title_pattern = 'vr-title'
    desc_pattern = 'star-wiki'
    for page in range(1,rrange):
        URL = f"https://www.sogou.com/sogou?query={query}&ie=utf8&pid=sogou-wsse-ff111e4a5406ed40&insite=zhihu.com&aria=0&w=&sut=1151&sst0=1640656254812&lkt=1%2C1640656254645%2C1640656254645&page={page}"
        html=s.get(URL).text
        # print(html)

        bs=BeautifulSoup(html, "html.parser")
        # urls=['https://www.sogou.com'+bs.find_all('h3',{'class':url_pattern})[i].a['href'] for i in range(len(bs.find_all('h3',{'class':url_pattern})))]
        urls=[bs.find_all('div',{'class':url_pattern})[i].get('data-url') for i in range(len(bs.find_all('div',{'class':url_pattern})))]
        titles=[bs.find_all('h3',{'class': title_pattern})[i].text.strip() for i in range(len(bs.find_all('h3',{'class':title_pattern})))]
        descs=[bs.find_all('p',{'class':desc_pattern})[i].text.strip() for i in range(len(bs.find_all('p',{'class':desc_pattern})))]    
        test_pattern(test, urls, titles, descs)
        if not test:
            for i in range(min(min(len(urls),len(titles)),len(descs))):
                result.append('\n'.join([urls[i],titles[i],descs[i]]))
                result.append('')
    return result

def bilibili(s, query, test=False, rrange=5):
    result = []
    result.append('-' * 30)
    result.append('bilibili')

    title_pattern = 'bili-video-card__info--tit'
    url_pattern = 'bili-video-card__info--right'
    descs_pattern = 'bili-video-card__info--author'

    for page in range(1,rrange):
        URL=f"https://search.bilibili.com/all?keyword={query}&from_source=webtop_search&spm_id_from=333.851&page={page}"
        html=s.get(URL).text
        bs=BeautifulSoup(html, "html.parser")
        # print(html)

        titles=[bs.find_all('h3',{'class':title_pattern})[i]['title'] for i in range(len(bs.find_all('h3',{'class':title_pattern})))]
        urls=['https://'+bs.find_all('div',{'class':url_pattern})[i].find('a')['href'].strip('/') for i in range(len(bs.find_all('div',{'class':url_pattern})))]
        descs=['up: '+bs.find_all('span',{'class':descs_pattern })[0].text for i in range(len(bs.find_all('span',{'class':descs_pattern})))]
        test_pattern(test, urls, titles, descs)
        if not test:
            for i in range(min(min(len(urls),len(titles)),len(descs))):
                result.append('\n'.join([urls[i],titles[i],descs[i]]))
                result.append('')
    return result

def axriv(s, query, test=False, rrange=100):
    result = []
    result.append('-' * 30)
    result.append('axriv')
    for start in range(1,rrange,50):
        URL = f"https://arxiv.org/search/?query={query}&searchtype=all&source=header&start={start}"
        html=s.get(URL).text

        bs=BeautifulSoup(html, "html.parser")
        urls=[bs.find_all('p',{'class':'list-title is-inline-block'})[i].a['href'] for i in range(len(bs.find_all('p',{'class':'list-title is-inline-block'})))]
        titles=[bs.find_all('p',{'class':'title is-5 mathjax'})[i].text.strip() for i in range(len(bs.find_all('p',{'class':'title is-5 mathjax'})))]
        descs=[bs.find_all('span',{'class':'abstract-short has-text-grey-dark mathjax'})[0].text.strip() for i in range(len(bs.find_all('span',{'class':'abstract-short has-text-grey-dark mathjax'})))]
        test_pattern(test, urls, titles, descs)
        if not test:
            for i in range(min(min(len(urls),len(titles)),len(descs))):
                result.append('\n'.join([urls[i],titles[i],descs[i]]))
                result.append('')
            # for i in range(min(min(len(urls),len(titles)),len(descs))):
            #     print('\n'.join([urls[i],titles[i],descs[i]]))
            #     print()
    return result


# # 递归函数遍历 AST 节点
# def traverse(node, visit, values):
#     for key, child in node.items():
#         if isinstance(key, list):
#             print('list')
#             for item in key:
#                 traverse(item, visit, values)
#         elif isinstance(key, dict):
#             print('dict')
#             visit(key, values)
#             for k, cld in child.items():
#                 traverse(cld, visit, values)
#         # elif isinstance(node, str):
#         #     return
#         # elif isinstance(node, int):
#         #     return
#         # else:
#         #     print('else')
#         #     visit(node, values)
#         #     for key, child in node.items():
#         #         print(key)
#         #         print('-' * 30)
#         #         traverse(child, visit, values)

# def visit(node, values):
#     # node_type = node.get('type', None)
#     # if node_type:
#     #     print(f"Visiting node type: {node_type}")
#     # print(node)
#     # return
#     return
#     # try:
#     #     if node.get('type', None) == 'VariableDeclarator' and node['id']['name'] == 'videoRenderer':
#     #         value = json.loads(node['init'].get('raw').replace("'", '"').strip())
#     #         values.append(value)
#     # except json.JSONDecodeError:
#     #     try:
#     #         value = json.loads(node['init'].get('raw').replace('"','|||').replace("'", '"').strip())
#     #         values.append(value)
#     #     except json.JSONDecodeError:
#     #         pass

# def youtube(s, query):
#     print('\nyoutube')
#     URL=f'https://www.youtube.com/results?search_query={query}'
#     html=s.get(URL).text
#     # print(html)
#     bs=BeautifulSoup(html, "html.parser")

#     script=None
#     for i in bs.find_all('script',{'nonce':re.compile('.*')}):
#         if 'ytInitialData' in str(i):
#             script=i
#             break

#     tree = esprima.parseScript(BeautifulSoup(str(script), "html.parser").script.get_text(), options={"range": True, "tokens": True})
#     values=[]
#     # print(tree)
#     traverse(tree, visit, values)
#     print(values)


    # for node in nodevisitor.visit(tree):
    #     if isinstance(node, ast.Assign):
    #         if getattr(node.left, 'value', '').strip('"') == "videoRenderer":
    #             try:
    #                 value = json.loads(node.right.to_ecma().replace("'", '"').strip())
    #             except:
    #                 try:
    #                     value = json.loads(node.right.to_ecma().replace('"','|||').replace("'", '"').strip())
    #                 except:
    #                     pass
    #             values.append(value)

    # urls=['https://www.youtube.com/watch?v='+value['videoId'] for value in values]
    # titles=[value['title']['runs'][0]['text'] for value in values]
    # descs=['' if 'detailedMetadataSnippets' not in value else value['detailedMetadataSnippets'][0]['snippetText']['runs'][0]['text'] for  value in values]
    # for i in range(min(min(len(urls),len(titles)),len(descs))):
    #     print('\n'.join([urls[i],titles[i],descs[i]]))
    #     print()

def print_result(results):
    for r in results:
        print(r)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, default='', help='搜索内容')
    parser.add_argument('-p', type=str, default='', help='只搜索某个渠道的内容[google, bili, sougou, axriv]')
    parser.add_argument('-t', action='store_true', help='测试模式')
    args = parser.parse_args()

    if args.s == '':
        return

    s = requests.session()            # 爬虫主体对象
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})

    query = args.s.replace(' ', '+')
    if args.p == 'google':
        print_result(google(s, query, args.t))
    elif args.p == 'sougou':
        print_result(sougou_zhihu(s, query, args.t))
    elif args.p == 'bili':
        print_result(bilibili(s, query, args.t))
    elif args.p == 'axriv':
        print_result(axriv(s, query, args.t))
    else:
        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            # 提交任务并收集 future 对象
            futures = []
            futures.append(executor.submit(google, s, query, args.t, rrange=20))
            futures.append(executor.submit(sougou_zhihu, s, query, args.t, rrange=5))
            futures.append(executor.submit(bilibili, s, query, args.t, rrange=5))
            futures.append(executor.submit(axriv, s, query, args.t, rrange=100))
            # 等待所有线程完成并获取结果
            for future in as_completed(futures):
                fresult = future.result()
                if fresult is not None:
                    results += fresult
            print_result(results)

if __name__ == '__main__':
    main()