from rest_framework import viewsets
from .models import Alert
from .serializers import AlertSerializer

class AlertViewset(viewsets.ModelViewSet):
    queryset = Alert.objects.filter(status=0)
    #queryset = Alert.objects.all()
    serializer_class = AlertSerializer
