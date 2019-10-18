from django.db import models


class Alert(models.Model):
    STATUS = (
        (0,'告警'),
        (1,'已恢复')
    )
    severity = models.CharField(verbose_name='告警级别', max_length=50)
    alertname = models.CharField(verbose_name='告警类别', max_length=50)
    instance = models.CharField(verbose_name='告警主机', max_length=100)
    summary = models.CharField(verbose_name='告警主题', default='Null',max_length=500)
    platform = models.CharField(verbose_name='告警区域', default='ceshi',max_length=30)
    description = models.CharField(verbose_name='告警详情', max_length=500)
    startsAt = models.CharField(verbose_name='告警时间',max_length=500)
    first_restarts = models.IntegerField(verbose_name='重启次数',default=0)
    second_restarts = models.IntegerField(verbose_name='重启次数', default=0)
    status = models.IntegerField(verbose_name='告警状态', default=0)
    namespace = models.CharField(verbose_name='名称空间',default='default',max_length=30)
    pod = models.CharField(verbose_name='容器名称',blank=True,null=True,max_length=100)

    def __str__(self):
        return self.instance