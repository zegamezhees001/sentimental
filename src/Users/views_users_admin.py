from django.shortcuts import render
from BaseSettings.respone_data import responseData , message_handle
import json
from .presenters.user_model import UserModel
from django.contrib.auth.decorators import user_passes_test
from .models import Profile
from BaseSettings.permissions import check_user_is_admin
def zip_data_profiles(profiles):
    zip_datas = []
    if len(profiles):
        for profile in profiles:
            bd = "" 
            if (profile.birth_date is not None): 
                bd = profile.birth_date.strftime("%d/%m/%YT%H:%M:%S") 
            else: 
                bd =profile.birth_date
            print(profile.birth_date is not None , profile.birth_date , bd)
            data = {
                "avatar" : str(profile.avatar),
                "bio" : profile.bio,
                "tel": profile.tel,
                "birth_date": bd,
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name,
                "employeeID": profile.user.employeeID ,
                "is_staff": profile.user.is_staff ,
                "is_active": profile.user.is_active ,
                "id_user": profile.id 
            }
            zip_datas.append(data)
    return zip_datas


@user_passes_test(check_user_is_admin, login_url="Users:login")
def admin_create_user_page(req):
    return render(req , "admin/create_user.html")

@user_passes_test(check_user_is_admin, login_url="Users:login")
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


@user_passes_test(check_user_is_admin, login_url="Users:login")
def user_all(req):
    try:
        profiles = Profile.objects.all()
        zip_datas = zip_data_profiles(profiles)
        return responseData(message_handle("get data." , zip_datas) , 200)
    except Exception as e:
        print(e)
        return responseData(message_handle("err message: {}".format(e) , []) , 500)
