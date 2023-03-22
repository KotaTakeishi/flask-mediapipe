# flask-mediapipe

## 概要

[mediapipe](https://mediapipe.dev/)という人体検知の機械学習ライブラリがあったので遊んでみた。  
flaskと組み合わせてブラウザで表示できるようにした。UIは最低限。  
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