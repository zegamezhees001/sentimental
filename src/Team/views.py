from django.shortcuts import render
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle

# Create your views here.


def create_team_page(request):
    return render(request, "create_team.html")


def create_team(req):
    teamData = json.loads(req.body)
    name_team = teamData["name_team"]
    try:
        create_team = TeamModel(name_team=name_team)
        create_team.save()
        return reponseData(message_handle("Add Team", [], 200))
    except:
        data = message_handle(message_handle("something wrong", [], 500))
        return responseData(data)
    return render(req, "create_team.html")



def zip_team_object(tData):
    zipDatas = []
    if len(tData) > 0:
        for d in tData:
            object_ = {
                "id_team": d.id_team,
                "name_team": d.name_team,
                "create_date": d.create_date.strftime("%d/%m/%YT%H:%M:%S")
            }
            zipDatas.append(object_)
    return zipDatas


def show_team_all(req):
    try:
        datas = TeamModel.objects.all()
        datas_to_show = zip_team_object(datas)
        goBackData = message_handle("load data success", datas_to_show, 200)
        return responseData(goBackData)
    except:
        return responseData(message_handle("something worng", [], 500))


def show_team_page(req):
    return render(req, "show_team.html")


