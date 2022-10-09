import os
import json
import requests
from urllib.parse import quote

key = input('请输入您要下载的歌曲或歌手名: ')

data = {"req": {"method": "DoSearchForQQMusicDesktop",
                "module": "music.search.SearchCgiService",
                "param": {
                    "query": f"{quote(key)}",
                    "page_num": 1,  # 页数
                    "num_per_page": 30  # 每页的数量
                }
                }
        }

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'cookie': 'uin=1234567890; qm_keyst=Q_H_L_5MBXVx4TfTmI9iBREbZKrJ_YjwE_zRVa_ghg0Qtx7WCnaq_DxYNUM1Q'  # 绿砖cookie，过期替换
}

search_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data=' + (json.dumps(data).replace('\"', '%22'))

response = requests.get(search_url, headers=headers)

musics = response.json()['req']['data']['body']['song']['list']

print('为您找到以下结果: ')
print('-' * 20)
print('序号', '歌曲', '歌手')

mid_list = []
song_list = []
singer_list = []

for index, music in enumerate(musics):
    mid = music['mid']
    song = music['name']
    singers = music['singer']
    singer = ''
    for idx, singer_info in enumerate(singers):
        if idx == 0:
            singer += singer_info['name']
        else:
            singer += '&' + singer_info['name']

    mid_list.append(mid)
    song_list.append(song)
    singer_list.append(singer)

    print(index + 1, song, singer)

print('-' * 20)

ans = int(input('请输入您要下载的歌曲序号: '))

mid = mid_list[ans - 1]
song = song_list[ans - 1]
singer = singer_list[ans - 1]

data1 = {"req": {"module": "vkey.GetVkeyServer",
                 "method": "CgiGetVkey",
                 "param": {
                     "guid": "0",
                     "songmid": [f"{quote(mid)}"]
                 }
                 }
         }

info_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data=' + (json.dumps(data1).replace('\"', '%22'))

resp = requests.get(info_url, headers=headers)

music_url = 'https://dl.stream.qqmusic.qq.com/' + resp.json()['req']['data']['midurlinfo'][0]['purl']

res = requests.get(music_url, headers=headers)

if not os.path.exists('music'):
    os.mkdir('music')

with open(f'music/{song}-{singer}.m4a', 'wb') as f:
    f.write(res.content)
    print(f'{song}-{singer}.m4a 下载完成！')