'''
Docstring for notify
依照 Google Gemini 給出的範例進行修改。

呼叫 send_line_notification() 可以將訊息傳送給手機上的 LINE。
呼叫 send_line_image() 可以傳送訊息以及影像資料。
image_data 是圖檔的二進位資料。可以使用 open(image_file, "rb) 取得。

呼叫 send_telegram_message() 可以將訊息發送給手機上的 Telegram 通訊App。

<< 設定 Telegram Bot 的步驟 >>
1. 手機上先安裝 Telegram Messenger，並完成註冊。
2. 在 Telegram 搜尋 @BotFather (住要要有官方認證符號，因為會有假帳號。)
3. 輸入 /newbot
4. 依照指示設定一個 名稱 和 使用者名稱 (使用者名稱必須以 bot 結尾)
5. 完成後，會給你一串 HTTP API Token (例如 123456789:ABCDefgh...)，請保存好。

<< 如何取得收訊者的 Chat ID >>
1. 傳送訊息給已建立的 Bot
2. 在瀏覽器輸入 https://api.telegram.org/bot<BOT Token>/getUpdates
3. 從回傳的 JSON 裡找 Chat ID
'''
import requests
from datetime import datetime


URL_LINE_NOTIFY = "https://notify-api.line.me/api/notify"

def send_line_notification(message, token):
    headers = {
        "Authorization": "Bearer " + token
    }

    # Prepare the message
    payload = {
        "message": message
    }

    # Send the POST request
    try:
        response = requests.post(URL_LINE_NOTIFY, headers=headers, data=payload)

        if response.status_code == 200:
            print("LINE notify sent successfully.")
        else:
            print(f"Failed! Status Code: {response.status_code}")
    except Exception as e:
        print(f"Network Error: {e}")


def send_line_image(message, token, image_data):
    headers = {
        "Authorization": "Bearer " + token
    }
    payload = {
        "message": message
    }
    files = {
        "imageFile": image_data
    }
    try:
        response = requests.post(URL_LINE_NOTIFY, headers=headers, data=payload, files=files)

        if response.status_code == 200:
            print("LINE notify sent successfully.")
        else:
            print(f"Failed! Status Code: {response.status_code}")
    except Exception as e:
        print(f"Network Error: {e}")


def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            print("Send message via Telegram successfully.")
        else:
            print(f"Failed! Status Code: {response.status_code}")
    except Exception as e:
        print(f"Network Error: {e}")


if __name__ == "__main__":
    # testing
    with open("token.txt", "rt") as f:
        token = f.readline().rstrip()
        chat_id = f.readline().rstrip()

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    #msg = "\nWarning!!\nAbnormal temperature detected by Raspberrry Pi."
    msg = f"\n警告！\n溫度超標！\n{timestamp} 從樹莓派發送。"
    send_telegram_message(token, chat_id, msg)

