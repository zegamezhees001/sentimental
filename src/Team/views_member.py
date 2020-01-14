from django.shortcuts import render, redirect
import json
from .models import TeamModel
from BaseSettings.respone_data import responseData, message_handle
from django.contrib.auth.decorators import user_passes_test
from BaseSettings.permissions import check_user_is_admin
from .presenters.members.MemberModel import MemberModel


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
    except Exception as e:
        return render(
            req,
            "add_member.html",
            {"message": "some thibg worng", "team": [], "stattus": 500},
        )


@user_passes_test(check_user_is_admin, login_url="Users:login")
def add_member(req):
    try:
        member = json.loads(req.body)
        memberModel = MemberModel(member)
        message = memberModel.add_member()
        return responseData(message_handle(message, []), 200)
    except Exception as e:
        return responseData(message_handle("err message: {}".format(e), []), 500)


@user_passes_test(check_user_is_admin, login_url="Users:login")
def show_member_list_by_team(req):
    try:
        if req.GET.get("id_team"):
            id_team = req.GET.get("id_team")
            find_datas = MemberModel("").find_member_by_team(id_team=id_team)
            message_ = message_handle("Show member list success.", find_datas)
            return responseData(message_, 200)
        else:
            return responseData(message_handle("id_team is not found", []), 404)
    except Exception as e:
        return responseData(message_handle("err message:{}".format(e), []), 500)


@user_passes_test(check_user_is_admin, login_url="Users:login")
def delete_member_from_id_role(req):
    try:
        if req.GET.get("id_role"):
            id_role = req.GET.get("id_role")
            message_role = MemberModel("").delete_member_by_id_role(id_role)
            message_ = message_handle(message_role, [])
            return responseData(message_, 200)
        else:
            message_ = message_handle("can not found id_role: {}".format(id_role), [])
            return responseData(message_, 200)
    except Exception as e:
        return responseData(message_handle("err message:{}".format(e), []), 500)

