# encoding: utf-8
from readconfig import ReadConfig
from dingtalk import send_message_dingtalk
import requests
import sys
import re

class GatewayMonitor:

    def __init__(self,env):
        self.env = env
        self.url = None
        self.receive = None
        self.alert_msg = []

    """
    获取每个环境下对应的参数信息
    """
    def get_platform_env(self):
        result = ReadConfig(self.env).run()
        self.url = result['url']
        self.receive = result['receive']

    def get_alerts(self):
        res = requests.get(self.url)
        alert_list = res.json()
        if len(alert_list) > 0:
            for item in alert_list:
                alertname = '告警标题： ' + item['alertname'] + '\n'
                instance = '告警主机： ' + item['instance'] + '\n'
                startsAt = '告警时间： ' +  item['startsAt'] + '\n'
                status = '告警状态： ' + item['status'] + '\n'
                severity = '告警级别： ' + item['severity'] + '\n'
                platform = '告警平台： ' + item['platform'] + '\n'
                restart_counts = item['second_restarts'] - item['first_restarts']       # 计算2次告警之间重启次数
                """
                如果pod容器在5分钟内重启超过5次，就发送告警通知，否则忽略
                """
                alertname_search = re.search('restart',item['alertname'])
                try:
                    if alertname_search.group():
                        if item['second_restarts'] == 0 :
                            continue
                        if item['first_restarts'] == 0 and item['second_restarts'] != 0:
                            continue
                        if restart_counts > 5:
                            description = '告警详情： ' + 'namespace {}下的pod  {}在5分钟内的重启次数大于{}次\n'.format(
                                                                                                    item['namespace'],
                                                                                                    item['pod'],
                                                                                                    restart_counts)
                        else:
                            continue
                except:
                    description = '告警详情： ' + item['description'] + '\n'
                msg = alertname + instance + description + startsAt + status + severity + platform
                self.alert_msg.append(msg)

    def send_alert_msg(self):
        if len(self.alert_msg) > 0:
            for msg in self.alert_msg:
                send_message_dingtalk(msg,self.receive)

    def run(self):
        self.get_platform_env()
        self.get_alerts()
        self.send_alert_msg()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: python {} test|shanxi'.format(sys.argv[0]))
    gateway_monitor = GatewayMonitor(sys.argv[1])
    gateway_monitor.run()