from django.shortcuts import render
from BaseSettings.respone_data import responseData, message_handle
import json
from .presenters.UserModel import UserModel
from django.contrib.auth.decorators import user_passes_test
from .models import Profile
from BaseSettings.permissions import check_user_is_admin


@user_passes_test(check_user_is_admin, login_url="Users:login")
def admin_create_user_page(req):
    return render(req, "admin/create_user.html")


@user_passes_test(check_user_is_admin, login_url="Users:login")
def create_new_user(req):
    try:
        if req.method == "POST":
            userModelClass = UserModel(json.loads(req.body))
            dataCb = userModelClass.create_user_data()
            return responseData(
                message_handle(
                    "username {} is created. \n message:{}".format(
                        userModelClass.username, dataCb
                    ),
                    [],
                ),
                200,
            )
        else:
            return responseData(message_handle("not found", []), 404)
    except Exception as e:
        return responseData(message_handle("err message: {}".format(e), []), 500)


@user_passes_test(check_user_is_admin, login_url="Users:login")
def user_all(req):
    try:
        profiles = Profile.objects.all()
        zip_datas = UserModel("").zip_data_profiles(profiles)
        return responseData(message_handle("get data.", zip_datas), 200)
    except Exception as e:
        print(e)
        return responseData(message_handle("err message: {}".format(e), []), 500)
