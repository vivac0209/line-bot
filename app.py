# 寫一個伺服器 放在雲端上執行 來接收line轉載過來的訊息
# 這伺服器要跟line的程式做互動
# 先接收再回復 
# SDK
# software development kit
# 這邊是要用line官方釋出的SDK import來用
# 這是伺服器的主要程式 取名要叫app.py
# 這邊就是架設伺服器 flask架設伺服器

from flask import Flask, request, abort

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

line_bot_api = LineBotApi('6A4fUVNQqiAL/ngoZkxTP4fP3uxy5Hm/nnrPG1HyfAD/2cDaIOyGwdCIkdFk7C8mVqIKATrCXVSYzHgCODS9IxmGVxFN7+rYBcZx8Lq01E/MOKRS6T91ve5kV6JKgOKD5ofZtFbR1C1LphszfZm9uAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e74a08b730227a8092882d49944e65e6')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	msg = event.message.text
	r = '看不懂'

	if msg == 'hi':
		r = 'hello'
	elif msg == '吃飯了嗎':
		r = '還沒'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))

if __name__ == "__main__":
    app.run()