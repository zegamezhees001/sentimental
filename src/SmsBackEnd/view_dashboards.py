from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import EmailMessage
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django import forms
from django.views.generic import View
from SmsBackEnd.utils import render_to_pdf
from django.views import View
from .models import *
from Users.models import UserSession, Profile
from django.contrib.sessions.models import Session
import django_excel as excel
import time
import datetime
import openpyxl
import json
from django.db import connection
from django.db.models import Q  # check !=
from .helper import date_format, encode, decode, dictfetchall
from collections import Counter
import collections

# function main for user group curator
@login_required(login_url="/Users/login/")
def equipment_admin(request):
    try:
        user_session = request.session.get('user_session')
        if user_session == 'Admin':

            if request.method == 'POST':
                pass
            else:
                return render(request, 'dashboards/equipment_main_admin.html')
        else:
            return redirect('/Users/login/')
    except Exception as e:  # contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')

# function main for user group curator
@login_required(login_url="/Users/login/")
def equipment_Lo(request):
    try:
        user_session = request.session.get('user_session')
        if user_session == 'Lo':

            if request.method == 'POST':
                pass
            else:
                return render(request, 'dashboards/equipment_main_Lo.html')
        else:
            return redirect('/Users/login/')
    except Exception as e:  # contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')

# function main for user group curator
@login_required(login_url="/Users/login/")
def equipment_Booster(request):
    try:
        user_session = request.session.get('user_session')
        if user_session == 'Booster':

            if request.method == 'POST':
                pass
            else:
                return render(request, 'dashboards/equipment_main_Booster.html')
        else:
            return redirect('/Users/login/')
    except Exception as e:  # contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')

# function main for user group curator
@login_required(login_url="/Users/login/")
def equipment_Student(request):
    try:
        user_session = request.session.get('user_session')
        if user_session == 'Student':

            if request.method == 'POST':
                pass
            else:
                return render(request, 'dashboards/equipment_main_Student.html')
        else:
            return redirect('/Users/login/')
    except Exception as e:  # contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')

# function main for user group admin
@login_required(login_url="/Users/login/")
def ibiobank_main_admin(request):
    try:
        user_session = request.session.get('user_session')
        cursor = connection.cursor()
        if user_session == 'Administrator' or user_session == 'Curator' or user_session == 'Collector':
            if request.method == 'POST':
                session = request.POST.get('session','')
                if session:
                    session = decode(session)
                    UserSession.objects.filter(session_id = session).delete()
                    Session.objects.filter(session_key = session).delete()

                cursor.execute(
                    'select man_session.user_id, user.username, man_session.last_login, man_session.session_id ,onlin_user.last_activity\
                    from auth_user user, users_usersession man_session ,online_users_onlineuseractivity onlin_user\
                    where man_session.user_id = user.id AND\
                    onlin_user.user_id = user.id \
                    order by man_session.last_login, user.username'
                )
                users_online = []

                for row in cursor.fetchall():
                    online = []
                    for index, value in enumerate(row):
                        if index in [2,4]:
                            online.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                        elif index == 3:
                            online.append(encode(value))
                        else:
                            online.append(value)
                    users_online.append(online)
                return HttpResponse([users_online])
            else:

                # User online ///////////////////////////////////////////////////////////////////////////////////////////////////
                cursor.execute(
                    'select man_session.user_id, user.username, man_session.last_login, man_session.session_id ,onlin_user.last_activity\
                    from auth_user user, users_usersession man_session ,online_users_onlineuseractivity onlin_user\
                    where man_session.user_id = user.id AND\
                    onlin_user.user_id = user.id \
                    order by man_session.last_login, user.username'
                )
                users_online = []

                for row in cursor.fetchall():
                    online = []
                    for index, value in enumerate(row):
                        if index in [2,4]:
                            online.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                        elif index == 3:
                            online.append(encode(value))
                        else:
                            online.append(value)
                    users_online.append(online)
                # User online ///////////////////////////////////////////////////////////////////////////////////////////////////

                # User group ////////////////////////////////////////////////////////////////////////////////////////////////////
                cursor.execute(
                    'SELECT auth_group.name , auth_user.username\
                     FROM auth_group, auth_user, auth_user_groups\
                     WHERE auth_user_groups.user_id = auth_user.id AND\
                     auth_user_groups.group_id = auth_group.id AND\
                     auth_user.is_active = 1'

                )
                users_group = [['Administrator',0],['Coordinator',0],['Principal Investigator',0],['Researcher',0],['Site user',0],['Curator',0],['Technician',0],['Collector',0]]
                
                for row in cursor.fetchall():
                    for group in users_group:
                        if group[0] == row[0]:
                            group[1] = group[1]+1
                group = []
                for i in users_group:
                    if i[1] > 0:
                        group.append({ "value": i[1], "name": i[0],"label": {"color": "#464646"} })
                users_group = group
     
                # Head page card ////////////////////////////////////////////////////////////////////////////////////////////////
                user_count = User.objects.filter(is_active = 1).count()
                user_request = User.objects.filter(is_active = 0).count()

                content = {
                    'user_count':user_count,
                    'user_request':user_request,
                    'users_online': users_online,
                    'users_group':users_group,
                }

                return render(request, 'dashboards/ibiobank_main_admin.html',content)
        else:
            return redirect('/Users/login/')
    except Exception as e: #contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main ===')
