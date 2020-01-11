from django.shortcuts import render
from BaseSettings.respone_data import responseData , message_handle
import json
from .presenters.user_model import UserModel

def admin_create_user_page(req):
    return render(req , "admin/create_user.html")


def create_new_user(req):
    try:
        if req.method == "POST":
            userModelClass = UserModel(json.loads(req.body))
            dataCb = userModelClass.create_user_data()
            return responseData(message_handle("username {} is created. \n message:{}".format(userModelClass.username , dataCb) , []) , 200)
        else :
            return responseData(message_handle("not found" , []) , 404)
    except Exception as e:
        return responseData(message_handle("err message: {}".format(e) , []) , 500)