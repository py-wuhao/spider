import requests

url = 'https://jobs.51job.com/wuhan/111574829.html?s=01&t=0'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Referer': 'https://www.51job.com/',
}

res = requests.get(url, headers=headers, verify=False)
# 编码方式不固定
character_set = {'GB2312', 'utf-8'}
for e in character_set:
    try:
        res.content.decode(e)
    except Exception:
        pass
    else:
        break
else:
    print('解码失败')
    character_set.add(res.apparent_encoding)
pass
