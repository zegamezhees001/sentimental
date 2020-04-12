"""Sentimenttal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sentimental import views
from  django.conf import  settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('contact/',views.contact, name="contact"),
    path('about/',views.about, name="about"),
    path('visual/',views.visual, name="visual"),
    path('table_search/',views.table_search, name="table"),
    path('table_show/',views.table_show, name="table_show"),
    path('search/',views.searchdata,name="search"),
    path('api/chart/data/',views.ChartData.as_view(), name='api-data'),
    path('api/chart/datapositive/',views.ChartDataPositive.as_view(), name='api-datapositive'),
    path('api/chart/datanegative/',views.ChartDataNegative.as_view(), name='api-datanegative'),
    path('api/chart/dataneutral/',views.ChartDataNeutral.as_view(), name='api-dataneutral'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)







