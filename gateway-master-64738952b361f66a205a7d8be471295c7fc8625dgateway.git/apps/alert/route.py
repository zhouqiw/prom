from rest_framework.routers import DefaultRouter
from .views import AlertViewset

alert_router = DefaultRouter()
alert_router.register(r'alert', AlertViewset, base_name='alert')