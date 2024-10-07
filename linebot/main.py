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
    print('reply_token: ', reply_token)


@handler.add(PostbackEvent)
def handle_postback(event):
	if event.postback.data == 'action=show_flex':
		flex_message = FlexSendMessage(
			alt_text='hello',
			contents={ # 就把JSON貼過來吧
				"type": "bubble",
				"hero": {
					"type": "image",
					"url": "https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png",
					"size": "full",
					"aspectRatio": "20:13",
					"aspectMode": "cover",
					"action": {
						"type": "uri",
						"uri": "https://line.me/"
					}
				},
				"body": {
					"type": "box",
					"layout": "vertical",
					"contents": [
						{
							"type": "text",
							"text": "Brown Cafe",
							"weight": "bold",
							"size": "xl"
						},
						{
							"type": "box",
							"layout": "baseline",
							"margin": "md",
							"contents": [
								{
									"type": "icon",
									"size": "sm",
									"url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
								},
								{
									"type": "icon",
									"size": "sm",
									"url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
								},
								{
									"type": "icon",
									"size": "sm",
									"url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
								},
								{
									"type": "icon",
									"size": "sm",
									"url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
								},
								{
									"type": "icon",
									"size": "sm",
									"url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
								},
								{
									"type": "text",
									"text": "4.0",
									"size": "sm",
									"color": "#999999",
									"margin": "md",
									"flex": 0
								}
							]
						},
						{
							"type": "box",
							"layout": "vertical",
							"margin": "lg",
							"spacing": "sm",
							"contents": [
								{
									"type": "box",
									"layout": "baseline",
									"spacing": "sm",
									"contents": [
										{
											"type": "text",
											"text": "Place",
											"color": "#aaaaaa",
											"size": "sm",
											"flex": 1
										},
										{
											"type": "text",
											"text": "Flex Tower, 7-7-4 Midori-ku, Tokyo",
											"color": "#666666",
											"size": "sm",
											"flex": 5
										}
									]
								},
								{
									"type": "box",
									"layout": "baseline",
									"spacing": "sm",
									"contents": [
										{
											"type": "text",
											"text": "Time",
											"color": "#aaaaaa",
											"size": "sm",
											"flex": 1
										},
										{
											"type": "text",
											"text": "10:00 - 23:00",
											"color": "#666666",
											"size": "sm",
											"flex": 5
										}
									]
								}
							]
						}
					]
				},
				"footer": {
					"type": "box",
					"layout": "vertical",
					"spacing": "sm",
					"contents": [
						{
							"type": "button",
							"style": "link",
							"height": "sm",
							"action": {
								"type": "uri",
								"label": "CALL",
								"uri": "https://line.me/"
							}
						},
						{
							"type": "button",
							"style": "link",
							"height": "sm",
							"action": {
								"type": "uri",
								"label": "WEBSITE",
								"uri": "https://line.me/"
							}
						},
						{
							"type": "box",
							"layout": "vertical",
							"contents": [],
							"margin": "sm"
						}
					],
					"flex": 0
				}
			}
		)
		line_bot_api.reply_message(event.reply_token, flex_message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)