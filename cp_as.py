import execjs

def get_cp_as():
    with open('cp_as.js', 'r') as f:
        js = f.read()

    context = execjs.compile(js)
    # 调用函数
    data = context.call('getHoney')
    return data

get_cp_as().get('as')