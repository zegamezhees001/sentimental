from django.urls import include, path,re_path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views_users_admin import *
app_name = 'Users'

#set name url with function in views  manage user

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('status_message/', status_message, name='status_message'),
    path('admin_create_user_page/', admin_create_user_page, name='admin_create_user_page'),
    path('admin_create_user/', create_new_user, name='create_new_user'),
    path('user_all/', user_all, name='user_all'),

    re_path(r'^user/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate_account, name='activate_account'),
    re_path(r'^user/reset/password/request/$', password_reset_request,name='password_reset_request'),
    re_path(r'^user/reset/password/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<date>[0-9A-Za-z_\-]+)/(?P<time>[0-9A-Za-z_\-]+)/$',activate_password_reset, name='activate_password_reset'),
    re_path(r'^user/reset/password/change/$', reset_change_password_request,name='reset_change_password'),
    re_path(r'^user/change_password/$', change_password,name='change_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
