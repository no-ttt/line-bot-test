from flask import Flask, request, abort
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import *

import os
import requests
import json

LINE_CHANNEL_ACCESS_TOKEN = 'Yshg4CA3SLnkkrL7QaXjugcLEMJHJzPSnCfsKAfieCy/uGIKKP6FSmd8mRCxpSjKjKKY8pL2gSrpM3BPQnycXONqzVsHalkROLFXEwIlHDMoZ7/WTUWdxIEECeNIxPFL9Obnjzh/SSkCVSAbee73LwdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '7151206af393ef579bc413445141c067'

SALES_MENU = 'richmenu-d61ed077772018d11eaa26ac06f36738'
CUSTOMER_MENU = 'richmenu-4d8a81caf3c2bb858d3f35d9d840fdc1'


app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
	role = "customer"
	user_id = event.source.user_id

	# Assign rich menu based on user role
	link_rich_menu(role, user_id)
	welcome_message = TextSendMessage(text="Welcome! Welcome!")
	line_bot_api.reply_message(event.reply_token, welcome_message)

# Message event
@handler.add(MessageEvent)
def handle_message(event):
	message_type = event.message.type
	user_id = event.source.user_id
	reply_token = event.reply_token
	message = event.message.text

	line_bot_api.reply_message(reply_token, TextSendMessage(text = message))


@handler.add(PostbackEvent)
def handle_postback(event):
	if event.postback.data == 'action=travel':
		labelText = "前往投保旅平險"
		uri_action = URIAction(label="go go go!", uri="https://dev.robinstech.com.tw/travel_black/")

		flex_message = FlexSendMessage(
		alt_text='travel_info',
		contents={
			"type": "bubble",
			"body": {
				"type": "box",
				"layout": "vertical",
				"contents": [
					{
						"type": "text",
						"text": labelText,
						"weight": "bold",
						"size": "xl"
					},
					{
						"type": "button",
						"action": uri_action
					}
				]
			}
		})

		line_bot_api.reply_message(event.reply_token, flex_message)


	if event.postback.data == 'action=car':
		labelText = "前往投保車險"
		uri_action = URIAction(label="go go go!", uri="https://dev.robinstech.com.tw/car_cathay/")

		flex_message = FlexSendMessage(
		alt_text='car_info',
		contents={
			"type": "bubble",
			"body": {
				"type": "box",
				"layout": "vertical",
				"contents": [
					{
						"type": "text",
						"text": labelText,
						"weight": "bold",
						"size": "xl"
					},
					{
						"type": "button",
						"action": uri_action
					}
				]
			}
		})

		line_bot_api.reply_message(event.reply_token, flex_message)


	if event.postback.data == 'action=bonus':
		with open('test.json', 'r') as file:
			flex_contents = json.load(file)

		flex_message = FlexSendMessage(
			alt_text='hello',
			contents=flex_contents
		)
		line_bot_api.reply_message(event.reply_token, flex_message)

def link_rich_menu(role, user_id):
	rich_menu_ids = {
		"sales": SALES_MENU,
		"customer": CUSTOMER_MENU
	}

	rich_menu_id = rich_menu_ids.get("sales") if user_id == "Uc79c50d0da1c0c115957999fa197dff8" else rich_menu_ids.get("customer")
	# rich_menu_id = rich_menu_ids.get("sales") if role == "sales" else rich_menu_ids.get("customer")

	url = f"https://api.line.me/v2/bot/user/{user_id}/richmenu/{rich_menu_id}"
	headers = {
		"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
	}
	response = requests.post(url, headers=headers)

	return response.status_code

if __name__ == "__main__":
	link_rich_menu("sales", "Uc79c50d0da1c0c115957999fa197dff8")
	
	port = int(os.environ.get('PORT', 80))
	app.run(host='0.0.0.0', port=port)