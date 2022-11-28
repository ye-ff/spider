import os
import json
import requests
from base64 import b64encode
from Crypto.Cipher import AES

keyword = input('请输入您要下载的歌曲或歌手名：')

search_url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='

data = {
    'hlposttag': "</span>",
    'hlpretag': "<span class=\"s-fc7\">",
    'limit': 30,
    'offset': 0,
    's': f"{keyword}",
    'total': 'true',
    'type': "1"
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = 'mEHlXeK2hb4tflex'


def get_encSecKey():
    return 'cac03616eea07c2bcf232f38b2954956ad8d4de7f07ee07f5f8872e633282d305d1bef6c25af2951c8fe63e92b8a854632649bf486e4d804a00216f3313b55ccdf7c906632275e1690a03a711cad970237418e6c9fc5dc1833c7530c35dcf0b00849e81b1858de9c2d837a0c14753d188044d8668a40b82274ef31f8693c1fb5'


def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def enc_pamas(data, key):
    iv = '0102030405060708'
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)
    bs = aes.encrypt(data.encode('utf-8'))
    return str(b64encode(bs), 'utf-8')


def get_params(data):
    first = enc_pamas(data, g)
    second = enc_pamas(first, i)
    return second


response = requests.post(search_url, data={
    'params': get_params(json.dumps(data)),
    'encSecKey': get_encSecKey()
}, headers=headers)

musics = response.json()['result']['songs']

print('为您找到以下结果：')
print('=' * 30)
print('序号', '歌曲', '歌手', '专辑')

song_list = []
singer_list = []
id_list = []

for index, music in enumerate(musics):
    id = music['id']
    song = music['name']
    singer = music['ar'][0]['name']
    album = '《' + music['al']['name'] + '》'

    id_list.append(id)
    song_list.append(song)
    singer_list.append(singer)

    print(index + 1, song, singer, album)

print('=' * 30)

ans = int(input('请输入您要下载的歌曲序号：'))

song = song_list[ans - 1]
singer = singer_list[ans - 1]
id = id_list[ans - 1]

music_url = f'http://music.163.com/song/media/outer/url?id={id}.mp3'

res = requests.get(music_url, headers=headers)

if not os.path.exists('music'):
    os.mkdir('music')

with open(f'music/{song}-{singer}.mp3', 'wb') as f:
    f.write(res.content)
    print(f'{song}-{singer}.mp3下载完毕！')