from django.shortcuts import render
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle
from Users.models import Permission


def add_permission_page(req):
    return render(req , "add_permission.html")


def add_permission(req):
    permissionData = json.loads(req.body)
    try:
        if permissionData.get("name_permission"):  
            name_permission = permissionData.get("name_permission");
            permission = Permission(name_permission=name_permission)
            permission.save();
        return responseData(message_handle("permission successfully saved." , [] , 200))

    except :
        return responseData(message_handle("permission is not saved." , [] , 500))
        