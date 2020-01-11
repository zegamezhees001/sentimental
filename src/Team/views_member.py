from django.shortcuts import render , redirect
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle
from django.contrib.auth.decorators import user_passes_test
from BaseSettings.permissions import check_user_is_admin



@user_passes_test(check_user_is_admin, login_url="Users:login")
def add_member_page(req):
    try:
        id_team = req.GET.get("id_team")
        if id_team:
            print(id_team)
            team = TeamModel.objects.get(id_team=id_team)
            return render(req, "add_member.html", {"message": "find", "team": team})
        else:
            return redirect("Team:show_team_page")
    except:
        return render(
            req,
            "add_member.html",
            {"message": "some thibg worng", "team": [], "stattus": 500},
        )

@user_passes_test(check_user_is_admin, login_url="Users:login")
def add_member(req):
    pass
    # try:
    #     pass
    # except :
    #     return responseData("something worng" , [] , 500)

