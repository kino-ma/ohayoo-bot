# -*- coding:utf-8 -*-
from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
CHANNEL_ACCESS_TOKEN = "LdHbJ8lgjSAb/D82JovFpLCRRN+niO3FsUQanUJwzzw0wxd/xpe9p8o6xayKTZIpSCS5HhZ/AG96A5GKJaliodjUNqv7Y5KPUkCDv1D1D/n2wQJ3cnYbqCZrKxhKscqIPrN9REVqtMdbDzPRU2NuNQdB04t89/1O/w1cDnyilFU=" # os.environ["ACCESS_TOKEN"]
CHANNEL_SECRET ="LdHbJ8lgjSAb/D82JovFpLCRRN+niO3FsUQanUJwzzw0wxd/xpe9p8o6xayKTZIpSCS5HhZ/AG96A5GKJaliodjUNqv7Y5KPUkCDv1D1D/n2wQJ3cnYbqCZrKxhKscqIPrN9REVqtMdbDzPRU2NuNQdB04t89/1O/w1cDnyilFU=" # os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
