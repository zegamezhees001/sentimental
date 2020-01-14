from django.urls import include, path, re_path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views_attachment import *
from .views_member import *
from .views_permission import *
from .views import *

app_name = "Team"
# set name url with function in views  manage user
urlpatterns = [
    path("show_team_all/", show_team_all, name="show_team_all"),
    path("show_team_page/", show_team_page, name="show_team_page"),
    path("create_team/", create_team_page, name="create_team"),
    path("create_team_save/", create_team, name="create_team_save"),
    path("add_member_page/", add_member_page, name="add_member_page"),
    path("add_member/", add_member, name="add_member"),
    path(
        "delete_member_from_id_role/",
        delete_member_from_id_role,
        name="delete_member_from_id_role",
    ),
    path(
        "show_member_list_by_team/",
        show_member_list_by_team,
        name="show_member_list_by_team",
    ),
    path("add_attachment_page/", add_attachment_page, name="add_attachment_page"),
    path("add_attachment/", add_attachment, name="add_attachment"),
    path("show_attachments/", show_attachments, name="show_attachments"),
    path("delete_attachment/", delete_attachment, name="delete_attachment"),
    path("add_permission_page/", add_permission_page, name="add_permission_page"),
    path("add_permission/", add_permission, name="add_permission"),
    path("show_permissions/", show_permissions, name="show_permissions"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
