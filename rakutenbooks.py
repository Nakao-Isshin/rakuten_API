import requests
from pandas import json_normalize
from dotenv import load_dotenv
import os


load_dotenv("./.env")

# https://webservice.rakuten.co.jp/documentation/books-game-search


# urlの作成
# ランキングAPIのベースとなるURL
base_url = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404?'
# genre_url = 'https://app.rakuten.co.jp/services/api/BooksGenre/Search/20121128?'
item_parameters = {
    'applicationId': os.environ['applicationId'],  # アプリID
    'title': "ゼルダの伝説",
    'booksGenreId': "006514006001",
    'outOfStockFlag': 1,
    'limitedFlag': 1,
    'genreInformationFlag': 1
}


# jsonデータの取得
r = requests.get(base_url, params=item_parameters)
jsondata = r.json()
# print(json.dumps(jsondata, indent=2,ensure_ascii=False))
# print(jsondata)
# jsondata内のItemsにアクセスした後に、データフレームに格納
df = json_normalize(jsondata['Items'])
if df.empty:
    print("not found")
    print(jsondata)
    exit()
# 必要な情報だけ抽出
df_pickup = df.loc[:,
                   ['Item.title',
                    'Item.author',
                    'Item.isbn',
                    'Item.jan',
                    'Item.itemCaption',
                    'Item.affiliateUrl',
                    'Item.itemPrice',
                    'Item.availability',
                    'Item.largeImageUrl',
                    'Item.publisherName',
                    'Item.salesDate',
                    'Item.reviewAverage',
                    'Item.reviewCount']]

# 項目の日本語辞書作成
rename_dic = \
                {'Item.title': 'タイトル',
                 'Item.author': '著者名',
                 'Item.isbn': 'ISBNコード',
                 'Item.jan': 'JANコード',
                 'Item.itemCaption': '商品説明文',
                 'Item.affiliateUrl': 'アフィリエイトURL',
                 'Item.itemPrice': '税込価格',
                 'Item.availability': '在庫状況',
                 'Item.largeImageUrl': '商品画像URL',
                 'Item.publisherName': '出版社名',
                 'Item.salesDate': '出版日/発売日',
                 'Item.reviewAverage': 'レビュー平均',
                 'Item.reviewCount': 'レビュー件数'}

# 項目名変更
df_pick_rename = df_pickup.rename(columns = rename_dic)

# データフレームCSVに出力
df_pick_rename.to_csv('rakuten_books.csv', index=False, encoding='utf_8_sig')
