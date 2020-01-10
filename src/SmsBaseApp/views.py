from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.template.loader import get_template
from django.template import Context
import subprocess
import shlex
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rolepermissions.checkers import has_permission
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.db.models import Max
# from SmsBackEnd.helper import dictfetchall
from PIL import Image
# from SmsBackEnd.helper import *


# Home page
# @login_required(login_url="/Users/login/")
def index(request):
    try:
        group = Group.objects.get(name="user")
        return render(request, "home_page.html", {})
    except Exception as a:
        print("line 26", a)
        return render(request, "home_page.html")


# Status message
def status_message(request):
    args = {}

    try:
        args["goto"] = request.session["goto"]
        sm_value = request.session["sm_value"]
        args["type"] = sm_value["type"]
        args["message_header"] = sm_value["message_header"]
        args["message_detail"] = sm_value["message_detail"]

        del request.session["goto"]
        del request.session["sm_value"]

        return render(request, "status_message.html", args)

    except KeyError:

        return redirect("/SmsBaseApp/home/")

