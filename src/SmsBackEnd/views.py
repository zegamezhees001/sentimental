from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, FileResponse, HttpResponseServerError , JsonResponse ,HttpResponseBadRequest ,HttpResponseRedirect
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
from .forms import AdminSignUpForm
from .helper import date_format, encode, decode, dictfetchall, rename_to_upload_photo, deleteImage
from PIL import Image
from .models import *
from django.http.response import JsonResponse

import os
from .helper import *
import django_excel as excel
import time, datetime , openpyxl , json
from django.db.models import Max, Count
from django.db import connection
from django.dispatch import receiver

# # Main page for other users
# @login_required(login_url="/Users/login/")
# def ibiobank_main_admin(request):
#     try:
#         user_session = request.session.get('user_session')
#         if user_session == 'Administrator' or user_session == 'Curator' or user_session == 'Collector':
#             breadcrumb = ['Home','Specimen','Carana']
#             return render(request, 'dashboards/ibiobank_main_admin.html',
#                           {'user_session': user_session,'breadcrumb':breadcrumb})
#         else:
#             return redirect('/Users/login/')
#     except Exception as e: #contains my own custom exception raising with custom messages.
#         return HttpResponseServerError(e)
#     finally:
#         print('=== end ibiobank main ===')


@login_required(login_url="/Users/login/")
def qrcode_generator(request):
    try:
        if request.method == "POST":
            title = 'nbp'
            num = request.POST.getlist('num[]','')
            size = request.POST.getlist('size[]','')
            dup = request.POST.getlist('dup[]','')
            date_create = request.POST.get('date_create','')
            date_create = date_format(date_create)
            user_id = str(request.user.id)
            data = []
            last_times = generated_qrcode.objects.aggregate(Max('times'))
            if last_times['times__max'] == None:
                last_times = '1'
            else:
                last_times = int(last_times['times__max'])+1
            for num,size,dup in zip(num,size,dup):
                num = int(num)
                for n in range(num):
                    last = generated_qrcode.objects.aggregate(Max('id'))
                    if last['id__max'] == None:
                        last = title+'{0:04}'.format(1)
                    else:
                        last = title+'{0:04}'.format(last['id__max']+1)
                    generated_qrcode.objects.create(
                    qrcode=str(last), 
                    times=last_times, 
                    size=str(size), 
                    duplicate=dup,
                    date_create=date_create,
                    user_create=user_id
                    )
            
            encode_last_times = encode(last_times)
            return redirect('/SmsBackEnd/qrcode_printing/'+str(encode_last_times))
        else:
            cursor = connection.cursor()
            cursor.execute('SELECT iBioBank_generated_qrcode.id as id, \
                iBioBank_generated_qrcode.date_create as date_create, \
                count(iBioBank_generated_qrcode.qrcode) as qrcode , \
                CONCAT(auth_user.first_name ," ", auth_user.last_name) as name ,\
                iBioBank_generated_qrcode.times as times \
                FROM iBioBank_generated_qrcode , auth_user \
                where iBioBank_generated_qrcode.user_create = auth_user.id \
                group by iBioBank_generated_qrcode.times \
                order by iBioBank_generated_qrcode.date_create desc ')
            table = dictfetchall(cursor)
            
            content = {
                'table':table
            }
            return render(request, 'qrcode_generator/qrcode_generator.html', content)
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end qrcode generator ==')

@login_required(login_url="/Users/login/")
def qrcode_printing(request,last_times):
    try:
        if request.method == "POST":
            pass
        else:
            last_times = decode(last_times)
            data = generated_qrcode.objects.filter(times=str(last_times)).order_by('size')
            
            content = {
                'data':data
            }
            return render(request, 'qrcode_generator/qrcode_printing.html', content)
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end qrcode generator ==')

@login_required(login_url="/Users/login/")
def qrcode_printing_custom(request):
    try:
        if request.method == "POST":
            qrcode = request.POST.getlist('qrcode[]','')
            size = request.POST.getlist('size[]','')
            dup = request.POST.getlist('dup[]','')
            dup_origin = request.POST.getlist('dup_origin[]','')

            data = []
            for name,size,dup,dup_ori in zip(qrcode,size,dup,dup_origin):
                dup = int(dup)
                data.append({'qrcode':name,'duplicate':dup,'size':size })
                up_dup = int(dup) + int(dup_ori)
                generated_qrcode.objects.filter(qrcode=name).update(duplicate=up_dup)

            content = {
                'data':data
            }
            return render(request, 'qrcode_generator/qrcode_printing.html', content)
        else:
            return render(request, 'qrcode_generator/qrcode_printing.html', content)
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end qrcode generator ==')

@login_required(login_url="/Users/login/")
def qrcode_detail(request):
    try:
        if request.method == "GET":
            times = request.GET.get('times','')
            data = generated_qrcode.objects.filter(times=times).values('id','qrcode','size','duplicate')
            
            return JsonResponse(list(data) ,safe=False)
        else:
            return JsonResponse({})
    except:
        print('erro render add_plant_data ')

@login_required(login_url="/Users/login/")
def qrcode_generator_new(request):
    try:
        if request.method == "POST":
            data = None
            tag_id = request.POST.getlist('tag_id[]','')
            if tag_id:
                data = generated_qrcode.objects.filter(id__in=tag_id).values()



            new_print = request.POST.getlist('new_print[]','')
            if new_print:
                data = generated_qrcode.objects.filter(id__in=new_print).values()

            content = {
                'data':data
            }
            return render(request, 'qrcode_generator/qrcode_generator_new.html', content)
        else:
            return render(request, 'qrcode_generator/qrcode_generator_new.html', {})
    except:
        print('erro render add_plant_data ')

@login_required(login_url="/Users/login/")
def qrcode_generator_query(request):
    try:
        if request.method == "POST":            
            qr = request.POST.get('sh_qr','')
            data = generated_qrcode.objects.filter(qrcode=qr).values()

            return JsonResponse(list(data),safe=False)
        else:
            return render(request, 'qrcode_generator/qrcode_generator_new.html', {})
    except:
        print('erro render add_plant_data ')


# function main logs
def logs(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'logs/logs.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function logs ==')

# function users profile 
def profile(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'profiles/profile.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end  function profile ==')

# function user notification
def notification(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'profiles/notification.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function notification ==')

# function users setting
def setting(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'profiles/setting.html', {})
    except:
        print('  render setting')



# function backup page list history backup
def backup(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'databases/backup.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end  function backup database ===')


#function backup database use for backup database mysql , 
def backup_database(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'databases/backup_database.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end function backup database ===')



# function backup web content for save file content 
def backup_web_content(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'databases/backup_web_content.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end function log database ===')



