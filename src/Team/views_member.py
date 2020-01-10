from django.shortcuts import render
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle


def add_member_page(req):
    try:
        id_team = req.GET.get("team")
        if id_team is not None:
            print(id_team)
            team = TeamModel.objects.get(id_team=id_team)
            return render(req, "add_member.html", {"message": "find", "team": team})
        else:
            return render(
                req,
                "add_member.html",
                {"message": "id_team is required", "team": [], "stattus": 404},
            )
    except:
        return render(
            req,
            "add_member.html",
            {"message": "some thibg worng", "team": [], "stattus": 500},
        )


def add_member(req):
    pass
    # try:
    #     pass
    # except :
    #     return responseData("something worng" , [] , 500)

