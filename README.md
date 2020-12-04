# 入退室管理システムの開発
ラズベリーパイ4とNFCカードリーダーを用いた入退室管理を行う。
# 環境
Python version
```bash
python -v
Python 3.7.3
```
# Crontab

```bash
00 0 * * * /sbin/reboot
@reboot sleep 10 && bash /home/pi/Desktop/hoge.sh 2>>/home/pi/Desktop/error.log
```
