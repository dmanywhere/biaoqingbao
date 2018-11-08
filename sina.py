import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Referer': 'https://m.weibo.cn/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/70.0.3538.77 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_weibo_page(page):
    params = {
        'containerid': '102803',
        'penApp': '0',
        'page': page
    }

    url = base_url + urlencode(params)
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print(e.args)


def parse_weibo_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            if not item:
                continue
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            #print(weibo)
            yield weibo

if __name__ == '__main__':
    for page in range(1,10):
        json = get_weibo_page(page)
        results = parse_weibo_page(json)
        for result in results:
            print(result)