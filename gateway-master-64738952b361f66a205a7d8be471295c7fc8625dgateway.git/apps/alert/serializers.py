from rest_framework import serializers
from .models import Alert
from django.conf import  settings
import time
import re

class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = '__all__'

    def to_internal_value(self, data):
        #print('data ====> {}'.format(data))
        post_data = {}
        for item in data['alerts']:
            post_data['status'] = item['status']
            post_data['alertname'] = item['labels']['alertname']
            post_data['instance'] = item['labels']['instance']
            post_data['severity'] = item['labels'].get('severity','warning')
            post_data['description'] = item['annotations']['description']
            post_data['summary'] = item['annotations']['summary']
            post_data['startsAt'] = item['startsAt'].replace('T',' ').replace('Z','')
            post_data['namespace'] = item['labels'].get('namespace','default')
            post_data['pod'] = item['labels'].get('pod','')
            post_data['platform'] = settings.PLATFORM
            if post_data['status'] == 'firing':
                post_data['status'] = 0
            else:
                post_data['status'] = 1
            self.create_alert(post_data)
        #print('post_data =====> {}'.format(post_data))
        return super(AlertSerializer, self).to_internal_value(post_data)

    def create_alert(self,data):
        """
        to_internal_value 方法传递过来的数据
        如果数据库中查不到记录，就直接添加一条
        如果能查到记录，则更新记录
        """

        try:
            alert_obj = Alert.objects.get(alertname=data['alertname'],
                                          instance=data['instance'],
                                          startsAt=data['startsAt'],
                                          summary=data['summary'])
            alert_obj.status = data['status']
            alert_obj.description = data['description']
            # 根据alertname是否是restart，来处理description字段以及first_restarts和second_restarts的值
            if data['alertname'].find('restart') != -1:
                alert_obj.first_restarts = alert_obj.second_restarts
                tmp_str = data['description'].split(' ')[-1]
                second_restarts = re.search('\d+',tmp_str).group()
                alert_obj.second_restarts = second_restarts
            alert_obj.save()
            return alert_obj
        except Alert.DoesNotExist:
            return Alert.objects.create(**data)

    def create(self, validated_data):
        #print('validated_data ====> {}'.format(validated_data))
        alert_obj = self.create_alert(validated_data)
        return alert_obj

    def to_representation(self, instance):
        ret = super(AlertSerializer, self).to_representation(instance)

        startsAt = ret['startsAt']
        ret['startsAt'] = startsAt.split('.')[0]
        if ret['status'] == 0:
            ret['status'] = '告警中'
        if ret['status'] == 1:
            ret['status'] = '已恢复'
        return ret