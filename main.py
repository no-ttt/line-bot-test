from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('Yshg4CA3SLnkkrL7QaXjugcLEMJHJzPSnCfsKAfieCy/uGIKKP6FSmd8mRCxpSjKjKKY8pL2gSrpM3BPQnycXONqzVsHalkROLFXEwIlHDMoZ7/WTUWdxIEECeNIxPFL9Obnjzh/SSkCVSAbee73LwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7151206af393ef579bc413445141c067')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    line_bot_api.reply_message(reply_token, TextSendMessage(text = message))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)