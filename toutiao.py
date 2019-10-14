import execjs
import requests
import time

headers = {
    'referer': 'https://www.toutiao.com/ch/news_tech/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

def get_cp_as():
    with open('cp_as.js', 'r') as f:
        js = f.read()
    context = execjs.compile(js)
    cp_as = context.call('getHoney')
    return cp_as

def get_signature():
    with open('sign.js', 'r') as f:
        js = f.read()
    context = execjs.compile(js)
    signature = context.call('tac')
    return signature

def get_url(behot_time):
    url = 'https://www.toutiao.com/api/pc/feed/'
    params = {
        'category': 'news_tech',
        'utm_source': 'toutiao',
        'widen': '1',
        'max_behot_time': behot_time,
        'max_behot_time_tmp': behot_time,
        'tadrequire': 'true',
        'as': get_cp_as().get('as'),
        'cp': get_cp_as().get('cp'),
        '_signature': get_signature(),
    }
    return (url, params)

def parse_html(url, params):
    try:
        res = requests.get(url, params=params, headers=headers)
        result = res.json()
    except Exception as e:
        print(e)
    if result['data'] == []:
        time.sleep(1)
        # continue
    else:
        next = result['next']
        for item in result['data']:
            title = item['title']
            group_id = item['group_id']
            article_url = 'https://www.toutiao.com/' + group_id
            print({'title': title, 'url': article_url})

        # break
        return next

if __name__ == '__main__':
    behot_time = parse_html(*get_url(0))
    # print(behot_time)
    while True:
        behot_time = parse_html(*get_url(behot_time))
    