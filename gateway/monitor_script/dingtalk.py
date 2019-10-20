# encoding: utf-8
import requests
import json

url = 'https://oapi.dingtalk.com/robot/send?access_token=c4544097c2614d779b38fbefc0714df58e8f48901928991f845dd4aafa18eedb'


def send_message_dingtalk(msg,url):
    data = {
        'msgtype': 'text',
        'text': {
            'content': '{}'.format(msg)
        },
        'at': {
            'atMobiles': []
            }
    }
    headers = {
        'Content-Type': 'application/json',
        'Charset': 'utf-8'
    }
    requests.post(url, headers=headers, data=json.dumps(data))


if __name__ == '__main__':
    msg = '测试信息'
    send_message_dingtalk(msg,url)