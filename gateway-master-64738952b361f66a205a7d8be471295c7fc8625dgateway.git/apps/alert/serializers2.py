from rest_framework import serializers
from .models import Alert
from django.conf import  settings

class AlertSerializer(serializers.ModelSerializer):
    #startsAt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Alert
        fields = '__all__'

    def to_internal_value(self, data):
        print('alertmanager data ==> {}'.format(data))
        post_data = {}
        for item in data['alerts']:
            post_data['status'] = item['status']
            post_data['alertname'] = item['labels']['alertname']
            post_data['instance'] = item['labels']['instance']
            post_data['severity'] = item['labels']['severity']
            post_data['description'] = item['annotations']['description']
            post_data['summary'] = item['annotations']['summary']
            post_data['startsAt'] = item['startsAt'].replace('T',' ').replace('Z','')
            post_data['platform'] = settings.PLATFORM
            if post_data['status'] == 'firing':
                post_data['status'] = 0
                print('post_data ==> {}'.format(post_data))
                self.create_alert(post_data)
            else:
                post_data['status'] = 1
                print('post_data ==> {}'.format(post_data))
                self.update_alert(post_data)
        return super(AlertSerializer, self).to_internal_value(post_data)

    def create_alert(self,data):
        alert_queryset = Alert.objects.filter(alertname=data['alertname'],
                                         instance=data['instance'],
                                         startsAt=data['startsAt'])
        if len(alert_queryset) == 0:
           return Alert.objects.create(**data)
        else:
            alert_obj = alert_queryset[0]
            for item in alert_queryset[1:]:
                item.delete()
            alert_obj.status = data['status']
            alert_obj.save()
            return alert_obj

    def update_alert(self,data):
		# 这里得重写，create方法处理最后一条，所以得判断status的值为几
		# 如果为0 则alert_obj.status = data['status']
		# 如果为1 则alert_obj.delete() 删除该条记录
        print('data ==> {}'.format(data))
        if data['status'] == 0:
            alert_obj = Alert.objects.get(alertname=data['alertname'],
                                          instance=data['instance'],
                                          startsAt=data['startsAt'])
            alert_obj.status = data['status']
            alert_obj.save()
        if data['status'] == 1:
            alert_obj = Alert.objects.filter(alertname=data['alertname'],
                                          instance=data['instance'],
                                          startsAt=data['startsAt']   )
            if len(alert_obj) > 1:
                alert_obj = alert_obj[0]
                queryset = alert_obj[1:].delete()
                for item in queryset:
                    item.delete()
            else:
                alert_obj = alert_obj[0]
                alert_obj.status = data['status']
            alert_obj.save()
        return alert_obj

    def create(self, validated_data):
        alert_obj = self.update_alert(validated_data)
        return alert_obj

    def to_representation(self, instance):
        ret = super(AlertSerializer, self).to_representation(instance)
        time_stamp = ret['startsAt']
        print('startsAt ==> {}'.format(time_stamp))
        if ret['status'] == 0:
            ret['status'] = '告警中'
        if ret['status'] == 1:
            ret['status'] = '已恢复'
        return ret