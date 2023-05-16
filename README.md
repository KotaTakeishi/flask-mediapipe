# flask-mediapipe

## 概要

[mediapipe](https://developers.google.com/mediapipe)という機械学習ライブラリがあったので使ってみた。  
flaskと組み合わせてブラウザで表示できるようにした。 mediapipeを使った部分は、プログラミングを始めて3か月くらいに書いたコードをそのまま使用しているため、非常に見にくい。
※PCの内蔵カメラを使用します。


## 環境構築

リポジトリをクローン
```
git clone git@github.com:KotaTakeishi/flask-mediapipe.git
```

ライブラリをインストール
```
pip install flask
pip install mediapipe
```

Webサーバを立てる
```
python app.py
```

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)にアクセス
