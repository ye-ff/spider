import os
import requests
from urllib.parse import quote

key = quote(input("请输入您要下载的歌曲或歌手名: "))

headers = {
    'Cookie': 'kw_token=HAPR7Y94ZLL',
    'csrf': 'HAPR7Y94ZLL',
    'Referer': f'http://www.kuwo.cn/search/list?key={key}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

search_url = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={key}&pn=1&rn=30'  # pn：页数  rn：每页的数量

response = requests.get(search_url, headers=headers)

musics = response.json()['data']['list']

print("为您找到以下结果: ")
print("-" * 40)
print("序号", "歌曲", "歌手", "专辑")

rid_list = []
song_list = []
singer_list = []

for index, music in enumerate(musics):
    rid = music['rid']
    song = music['name'].replace("&nbsp;", " ")
    singer = music['artist'].replace("&nbsp;", " ")
    album = music['album'].replace("&nbsp;", " ")

    rid_list.append(rid)
    song_list.append(song)
    singer_list.append(singer)

    print(index + 1, song, singer, album)

print("-" * 40)

ans = int(input("请输入您要下载的歌曲序号: "))

rid = rid_list[ans - 1]
song = song_list[ans - 1]
singer = singer_list[ans - 1]

info_url = f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3&br=320kmp3'  # convert_url3也可写为mp3

resp = requests.get(info_url, headers=headers)

music_url = resp.json()['data']['url']

res = requests.get(music_url, headers=headers)

if not os.path.exists('music'):
    os.mkdir('music')

with open(f'music/ {song}-{singer}.mp3', 'wb') as f:
    f.write(res.content)
    print(f'{song}-{singer}.mp3 下载完成！')