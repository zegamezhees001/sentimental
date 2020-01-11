from django.shortcuts import render
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle
from Users.models import Permission 
from django.contrib.auth.decorators import user_passes_test
from BaseSettings.permissions import check_user_is_admin



def permissionObjectToJsonFunc(permissionData):
    zipDatas = []
    if len(permissionData) > 0:
        for permission in permissionData:
            zipData = {
                "id_permission" : permission.id_permission,
                "name_permission": permission.name_permission
            }
            zipDatas.append(zipData)
    return zipDatas

@user_passes_test(check_user_is_admin, login_url="Users:login")
def add_permission_page(req):
    return render(req , "add_permission.html")
    
@user_passes_test(check_user_is_admin, login_url="Users:login")
def add_permission(req):
    try:
        permissionData = json.loads(req.body)
        if req.method == "POST" and permissionData.get("name_permission"):  
            name_permission = permissionData.get("name_permission");
            permission = Permission(name_permission=name_permission)
            permission.save();
        return responseData(message_handle("permission successfully saved." , [] , 200))

    except :
        return responseData(message_handle("permission is not saved." , [] , 500))

@user_passes_test(check_user_is_admin, login_url="Users:login")
def show_permissions(req):
    try:
        permissions = Permission.objects.all()
        permissionObjectToJson = permissionObjectToJsonFunc(permissions)
        return responseData(message_handle("show permission success" , permissionObjectToJson , 200))
    except Exception as e:
        return responseData(message_handle("err show:{}".format(e) , []) , 500)