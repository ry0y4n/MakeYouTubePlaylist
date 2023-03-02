# 特定チャンネルの動画の動画をプレイリストにまとめるプログラム

### 使用方法

[YouTbe Data API](https://developers.google.com/youtube/v3/getting-started?hl=ja)を使用するので，Googleアカウントと共にGCP上でAPIを有効にした上で，OAuthクライアントID（認証情報）を作成し，フォルダ配下に置く必要がある（`client_secrets.json`）．

```
pip install -r requirements.txt
python makePlaylist.py
```

### 動機

あるチャンネルの動画が全部好きで，それを作業用BGMとして流すためにプレイリストにしたくなった．
