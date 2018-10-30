# Flickrで写真を検索して、ダウンロードする
from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

# API Keyの設定（書き換えてご利用ください）
key = "a6f73208e823b9a6946f7cbe7fdf2e72"
secret = "63d67b7c2c94e6e8"
# ダウンロード後の待機時間（1以上を指定）
wait_time = 1 

# キーワードをチェックする
if len(sys.argv) < 2:
  print("python dl.py (keyword)")
  sys.exit()
keyword = sys.argv[1]
savedir = "./" + keyword
if not os.path.exists(savedir):
  os.mkdir(savedir) # フォルダーを作る

# Flickr APIで写真を検索
flickr = FlickrAPI(key, secret, format='parsed-json')
res = flickr.photos.search(
  text = keyword,           # 検索語
  per_page = 500,           # 取得件数（最大500件）
  media = 'photos',         # 写真を検索
  sort = "relevance",       # 検索語の関連順に並べる
  safe_search = 1,          # セーフサーチ（1を指定）
  extras = 'url_q,license') # 取得する

# 検索結果を確認
photos = res['photos']
pprint(photos)
try:
  # 1つずつ画像をダウンロードする
  for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir+'/'+photo['id']+'.jpg'
    if os.path.exists(filepath): continue
    print(str(i + 1) + ":download=", url_q)
    urlretrieve(url_q, filepath)
    time.sleep(wait_time)
except:
  import traceback
  traceback.print_exc()

