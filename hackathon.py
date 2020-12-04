import binascii
import nfc
import time
import csv
import gspread
import gc
import threading
import requests
import json
import os
import numpy as np
from pygame import mixer
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta

dict01={}
#testchannel
url = 'チャンネル'
service_code = 0x09CB
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/gmail.send']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'Key',
        scope)
gc = gspread.authorize(credentials)
wb = gc.open('ファイル名').sheet1


def getNextRow():
    values_list = wb.col_values(1)
    emptyrow = str(len(values_list)+1)
    return emptyrow

def on_connect_nfc(tag):
    global dict01
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            #print('  ' + '\n  '.join(tag.dump()))
            row = getNextRow()
            sc = nfc.tag.tt3.ServiceCode(service_code >> 6 ,service_code & 0x3f)
            bc1 = nfc.tag.tt3.BlockCode(0,service=0)
            bc2 = nfc.tag.tt3.BlockCode(1,service=0)
            data = tag.read_without_encryption([sc],[bc1,bc2])
            
            now_date = datetime.now()
            td = now_date.strftime('%Y')+"-" + now_date.strftime('%m')+"-"+ now_date.strftime("%d")
            td_time = now_date.strftime('%H')+":" + now_date.strftime('%M')+":" + now_date.strftime('%S')

            sid = str(data[2:10])
            oecuname = sid[12:20]
            name_str = ''.join(oecuname)
            name_list = [name_str]
            name_str2 = ''.join(td)
            name_list2 = [name_str2]
            name_str3 = ''.join(td_time)
            name_list3 = [name_str3]
            wb.update_acell('A'+row,oecuname)
            wb.update_acell('B'+row,td)
            wb.update_acell('C'+row,td_time)

            if not name_str in dict01:
                dict01 [name_str] = [name_str2,True]
                d=0
                mixer.init()
                mixer.music.load("音声Path")
                mixer.music.play(1)
            elif dict01[name_str] == [name_str2,True]:
                dict01 [name_str] = [name_str2,False]
                d=1
                mixer.init()
                mixer.music.load("音声Path")
                mixer.music.play(1)
            elif dict01[name_str] == [name_str2,False]:
                dict01 [name_str] = [name_str2,True]
                d=0
                mixer.init()
                mixer.music.load("音声Path")
                mixer.music.play(1)

            if(d==0):
                wb.update_acell('D'+row,'M206 Enter')
                status='M206 Enter'
                data2 = {'text': oecuname + '   ' + td + '   ' + td_time + '   ' + 'M206 Enter'}
                webhook = os.environ.get('hayalab_hackathon',url)
                requests.post(webhook, json.dumps(data2))
            elif(d==1):
                wb.update_acell('D'+row,'M206 Exit')
                status='M206 Exit'
                data2 = {'text': oecuname + '   ' + td + '   ' + td_time + '   ' + 'M206 Exit'}
                webhook = os.environ.get('hayalab_hackathon',url)
                requests.post(webhook, json.dumps(data2))

            status_str = ''.join(status)
            status_list = [status_str]
            sum_info = [name_list] + [name_list2] + [name_list3] + [status_list]
            print(sum_info)

            with open('ファイルPath', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(sum_info)

        except Exception as e:
            print ("error1: %s" % e)

def main():
    print('This program exit is CTRL + C ')
    clf = nfc.ContactlessFrontend('usb')
    try:
        while True:
            clf.connect(rdwr={'on-connect': on_connect_nfc})
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n!!!!!!!!!!Finish!!!!!!!!!!")

if __name__ == "__main__":
    main()