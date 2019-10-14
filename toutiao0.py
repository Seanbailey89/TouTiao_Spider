import execjs
import requests
import time

headers = {
    #    'cookie': 'tt_webid=6731181496139384324; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6731181496139384324; csrftoken=c73ecbc9df06a4ae0d23e05d37fb8b03; UM_distinctid=16ce5e8d711901-077cddbf26490d-f353163-144000-16ce5e8d712443; uuid="w:0eab1ab0084845a18c7108ace948c421"; __tasessionId=ejvfe2fta1567265113476; CNZZDATA1272960458=693129193-1567223451-https%253A%252F%252Fwww.baidu.com%252F%7C1567266006',
       'referer': 'https://www.toutiao.com/ch/news_tech/',
       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
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

    # 注意最后一个/要写，否则报错
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
        '_signature': get_signature()
    }

    return (url,params)


def parse_html(url, params):     
    while True:              
        response = requests.get(url, params=params ,headers=headers)
        result = response.json()    

        if result['data'] == []:  # 避免请求多次才有数据进行判断
            time.sleep(1)
            continue
        else:
            next = result['next']['max_behot_time']
            # next = result.get('next')
            for item in result['data']:
                title = item['title']
                group_id = item['group_id']
                article_url = 'https://www.toutiao.com/a' + group_id
                print({'title': title, 'url': article_url})

            break
    return next


if __name__ == '__main__':
    behot_time = parse_html(*get_url(0))
    while True:
        behot_time = parse_html(*get_url(behot_time))