from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
import requests
import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
raspberrypi_host = (config.get('line-bot', 'raspberrypi_host'))
# 接收 LINE 的資訊
@app.route("/callback",methods=['POST',"GET"])
def callback():
    if request.method == 'GET':
        print("receive get request")
        with open('id.txt', 'r') as f:
            user_id = f.read()
        f.close()
        sensor_signal = request.args.get(key='SENSOR')
        if (sensor_signal=="ON"):
            line_bot_api.broadcast(TextSendMessage(text='SENSOR IS ON SIGNAL'))#廣播通知全部人
            line_bot_api.broadcast(TextSendMessage(text='This is a broadcast message'))#廣播通知全部人
            line_bot_api.push_message(user_id, TextSendMessage(text='Message from Desktop send to specific id'))#向特定人傳送訊息
            line_bot_api.push_message(user_id,#向特定人傳送訊息
                                      ImageSendMessage(original_content_url=raspberrypi_host+"/photo_page",
                                                       preview_image_url=raspberrypi_host+"/photo_page"))#若圖片無法顯示請在圖片網址後面請加上一個#符號

        return "OK"
    elif request.method == 'POST':
        signature = request.headers['X-Line-Signature'] # LINE 憑證驗證

        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
        try:
            print(body, signature)
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return 'OK'
        
# 學我說話
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    if event.message.text == "setreply":#設定使用者ID
        var_id = (event.source.user_id)
        with open('id.txt', 'w') as f:
            f.write(str(var_id))
            f.close()
    elif (event.message.text == "photo"):#下自訂義指令叫樹梅派拍照
        pass
        data = {
            "name": "Jason",
            "photo": "ON"
        }
        print(data.keys())
        # "message from desktop"
        r = requests.get(raspberrypi_host, params=data)
        r.close()
    else:
        pass
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
