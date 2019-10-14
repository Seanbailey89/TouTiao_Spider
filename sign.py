import execjs


with open('sign.js', 'r') as f:
    js = f.read()
context = execjs.compile(js)
data = context.call('tac')
print(data)


