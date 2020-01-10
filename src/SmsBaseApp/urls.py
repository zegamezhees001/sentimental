from django.conf.urls import url
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import index,status_message

app_name = 'SmsBaseApp'

# set url with function in view SmsBaseApp
urlpatterns = [
    path('', index),
    path('SmsBaseApp/home', index, name='home'),
    path('SmsBaseApp/status_message', status_message),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
