from django.shortcuts import render
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def check_user_is_admin(user):
    try:
        return user.is_superuser
    except Exception as e:
        return True

def zip_team_object(tData):
    zipDatas = []
    if len(tData) > 0:
        for d in tData:
            object_ = {
                "id_team": d.id_team,
                "name_team": d.name_team,
                "create_date": d.create_date.strftime("%d/%m/%YT%H:%M:%S"),
            }
            zipDatas.append(object_)
    return zipDatas


@user_passes_test(check_user_is_admin, login_url="Users:login")
def create_team_page(request):
    return render(request, "create_team.html")

@user_passes_test(check_user_is_admin, login_url="Users:login")
def create_team(req):
    teamData = json.loads(req.body)
    name_team = teamData["name_team"]
    try:
        create_team = TeamModel(name_team=name_team)
        create_team.save()
        return responseData(message_handle("Add Team", [], 200) , 200)
    except Exception as e:
        print(e)
        data = message_handle("err message : {}".format(e), [], 500)
        return responseData(data , 500)
    return render(req, "create_team.html")



@user_passes_test(check_user_is_admin, login_url="Users:login")
def show_team_all(req):
    try:
        datas = TeamModel.objects.all()
        datas_to_show = zip_team_object(datas)
        # datas_to_show = []
        goBackData = message_handle("load data success", datas_to_show, 200)
        return responseData(goBackData)
    except Exception as e:
        return responseData(message_handle("err message: {}".format(e), [], 500))


@user_passes_test(check_user_is_admin, login_url="Users:login")
def show_team_page(req):
    return render(req, "show_team.html")

