from django.conf.urls import url
from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from . import views, view_dashboards, views_accounts, views_admin
from . import views_qrcode
from .view_api import load_events, insert_events

# app_name = 'SmsBaseApp'
app_name = "SmsBackEnd"

# set url with function in view SmsBaseApp
urlpatterns = [
    # main page for all user
    path(
        "ibiobank_admin/",
        view_dashboards.ibiobank_main_admin,
        name="ibiobank_main_admin",
    ),
    path("equipment_admin/", view_dashboards.equipment_admin, name="equipment_admin"),
    path("equipment_Lo/", view_dashboards.equipment_Lo, name="equipment_Lo"),
    path(
        "equipment_Student/",
        view_dashboards.equipment_Student,
        name="equipment_Student",
    ),
    path(
        "equipment_Booster/",
        view_dashboards.equipment_Booster,
        name="equipment_Booster",
    ),
    # accouts
    path("manage_accounts/", views_accounts.manage_accounts, name="manage_accounts"),
    path(
        "edit_accounts/?P<user_id>", views_accounts.edit_accounts, name="edit_accounts"
    ),
    path("edit_account/?P<user_id>", views_accounts.edit_account, name="edit_account"),
    path("view_account/?P<user_id>", views_accounts.view_account, name="view_account"),
    path("create_accounts/", views_accounts.create_accounts, name="create_accounts"),
    path("active_accounts/", views_accounts.active_accounts, name="active_accounts"),
    path("status_message/", views_accounts.status_message, name="status_message"),
    re_path(
        r"^user/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views_accounts.activate_account,
        name="activate_account",
    ),
    re_path(
        r"^user/reset/password/request/$",
        views_accounts.password_reset_request,
        name="password_reset_request",
    ),
    re_path(
        r"^user/reset/password/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<date>[0-9A-Za-z_\-]+)/(?P<time>[0-9A-Za-z_\-]+)/$",
        views_accounts.activate_password_reset,
        name="activate_password_reset",
    ),
    re_path(
        r"^user/reset/password/change/$",
        views_accounts.reset_change_password_request,
        name="reset_change_password",
    ),
    re_path(
        r"^user/change_password/$",
        views_accounts.change_password,
        name="change_password",
    ),
    path("del_user/?P<username>", views_accounts.del_user, name="del_user"),
    path(
        "delete_user_sessions/?P<username>",
        views_accounts.delete_user_sessions,
        name="delete_user_sessions",
    ),
    path(
        "django_image_and_file_upload_ajax/",
        views_accounts.django_image_and_file_upload_ajax,
        name="django_image_and_file_upload_ajax",
    ),
    # Admin
    path("admin_manage_user/", views_admin.admin_manage_user, name="admin_manage_user"),
    path("add_equipment/", views_admin.add_equipment, name="add_equipment"),
    # url for user logged in
    path("profile/", views.profile, name="profile"),
    path("notification/", views.notification, name="notification"),
    path("setting/", views.setting, name="setting"),
    # backup
    path("backup/", views.backup, name="backup"),
    path("backup_database/", views.backup_database, name="backup_database"),
    path("backup_web_content/", views.backup_web_content, name="backup_web_content"),
    # logs
    path("logs/", views.logs, name="logs"),
    # QRcode generator
    path("qrcode_generator/", views.qrcode_generator, name="qrcode_generator"),
    path(
        "qrcode_printing/<last_times>/", views.qrcode_printing, name="qrcode_printing"
    ),
    path("qrcode_detail/", views.qrcode_detail, name="qrcode_detail"),
    path(
        "qrcode_generator_new/", views.qrcode_generator_new, name="qrcode_generator_new"
    ),
    path(
        "qrcode_generator_query/",
        views.qrcode_generator_query,
        name="qrcode_generator_query",
    ),
    path(
        "qrcode_printing_custom/",
        views.qrcode_printing_custom,
        name="qrcode_printing_custom",
    ),
    # QRcode new
    path("my_qrcode/", views_qrcode.my_qrcode, name="my_qrcode"),
    path("create_qrcode/", views_qrcode.create_qrcode, name="create_qrcode"),
    path("help_qrcode/", views_qrcode.help_qrcode, name="help_qrcode"),
    path("qrcode_detail/", views_qrcode.qrcode_detail, name="qrcode_detail"),
    path("insert_events/", insert_events, name="insert_events"),
    path("load_events/", load_events, name="load_events"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
