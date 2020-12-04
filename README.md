# 入退室管理システムの開発
ラズベリーパイ4とNFCカードリーダーを用いた入退室管理を行う。

# 運用動画URL
https://drive.google.com/file/d/15iLmMW84r0WHwjWL_qhZJJN9oR6jkln5/view?usp=sharing

# システム機能
・学生番号、時間、部屋情報を取得

・一台のNFCで、入室と退室を両方管理

・それらの情報を、Googleスプレッドシート、Slackの指定したチャネルに同時投稿

・インターネット接続が途切れた時用に、CSVにも保存

・タッチした際、音によるフィードバック

# 環境
Python version
```bash
python -v
Python 3.7.3
```
# Crontab
日付変更のタイミングで強制再起動を行う。再起動後、自動的に入退室プログラムを起動させる。
```bash
00 0 * * * /sbin/reboot
@reboot sleep 10 && bash /home/pi/Desktop/hoge.sh 2>>/home/pi/Desktop/error.log
```

# ライブラリのインストール
必要なライブラリのインストールを行う。

NFCカードリーダーを使用するライブラリ
```bash
pip instal nfcpy
```
Googleスプレッドシートに記入を行うライブラリ
```bash
pip install gspread
```
API取得のKeyを読み込むライブラリ
```bash
pip install oauth2client
```
音によるフィードバックに使用したライブラリ
```bash
pip install pygame
```

# プログラムの実行
```bash
sudo python3 hackathon.py
```
