import time
import requests
from pyfcm import FCMNotification
 
APIKEY = "AAAAFUI13GU:APA91bE6-gnUQyOvC7UlPjzz7mZbWYNi_RNHnsT5KxMre4AsGP1ct8Ov-XfQ-bvD7yGStC4DtwgA5Vdh9PcrSGV1oViruNo3hBp_ZDpD1t-lSmUxOzwgrejhCKMPuJTXlX3g5mkteYTm"
# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(APIKEY)
TOKEN = "d7qfriT3g7M:APA91bFvsbTQ9qYUtDLGGjos6ajxM1bhrc3gMBof15PH-2HYqt5ZNdG71uSwautQbYieVwC6lAFjop6YF9mbSnjHhzn8dmYftEdRCEZPlMCtx_nBkETal9hwAt9F4kq86H932eGQO_wd"
temp = None

def sendMessage(body, title):
    # 메시지 (data 타입)
    data_message = {
        "notification":{
            "title": title,
            "body": body,
            "sound":"default",
            "click_action":"FCM_PLUGIN_ACTIVITY",
            "icon":"fcm_push_icon"
        },
        "data":{
            "title": title,
            "body": body,
        },
        "to":TOKEN,
        "priority":"high",
        "restricted_package_name":"temperature-push-service"
    }
    message_title = title
    message_body = body
 
    # 토큰값을 이용해 1명에게 푸시알림을 전송함
    result = push_service.notify_single_device(registration_id=TOKEN, message_title=message_title, message_body=message_body)

    # 전송 결과 출력
    print(result)

while True:
    now = requests.get('http://127.0.0.1:5000/api/temp').json()
    if now != temp:
        tempRange = requests.get('http://127.0.0.1:5000/api/temp/range').json()
        temp = float(now['temp_c'])
        if temp > float(tempRange['upper']) or temp < float(tempRange['lower']):
            sendMessage("온도 범위를 벗어났어요!", "현재 온도 : " + str(temp))
    sendMessage("푸시 수신 확인", "현재 온도 : " + str(temp))
    time.sleep(10)