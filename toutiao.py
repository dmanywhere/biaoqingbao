import requests
from urllib.parse import urlencode
import re
import os
from hashlib import md5
from multiprocessing.pool import Pool


headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.77 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

pattern = re.compile('//(.*?/)list(.*)')


def get_page(offset):
    base_url = 'https://www.toutiao.com/search_content/?'
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '表情包',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url = base_url + urlencode(params)
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print(e.args)

def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if not images:
                continue
            for image in images:
                if not isinstance(image, dict):
                    continue
                img_url = re.findall(pattern, image.get('url'))
                #print(img_url)
                yield {
                    'title': title,
                    'img_url': 'http://' + 'large'.join(img_url[0])
                }


def save_image(item):
    if not os.path.exists('表情包合集'):
        os.mkdir('表情包合集')

    try:
        r = requests.get(item.get('img_url'), headers=headers)
        if r.status_code == 200:
            img_content = md5(r.content)
            file_path = '{0}/{1}.{2}'.format('表情包合集', img_content.hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                print(file_path, '写入成功')
            else:
                print(file_path, '文件已存在。')
    except requests.ConnectionError as e:
        print('获取失败。')
        print('错误详情：', e.args)

def main(offset):
    json = get_page(offset)
    items = get_image(json)
    for item in items:
        save_image(item)


if __name__ == '__main__':
    pool = Pool()
    group = ([i for i in range(0, 401, 20)])
    pool.map(main, group)
    pool.close()
    pool.join()
