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


@login_required

# function Owner qr code 
def my_qrcode(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            cursor = connection.cursor()
            cursor.execute('SELECT GROUP_CONCAT(DISTINCT qrcode) as qrcode_name , iBioBank_generated_qrcode.times as times, iBioBank_generated_qrcode.date_create as date_create, count(iBioBank_generated_qrcode.times) as time , CONCAT(auth_user.first_name ," ", auth_user.last_name) as name , iBioBank_generated_qrcode.times as times FROM iBioBank_generated_qrcode , auth_user where iBioBank_generated_qrcode.user_create = auth_user.id group by iBioBank_generated_qrcode.times order by iBioBank_generated_qrcode.date_create desc')
            table = dictfetchall(cursor)
            
            content = {
                'table':table
            }
            return render(request, 'qrcode_generator/my_qrcode.html', content)

    except Exception as e:  #contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('== end function my qr code ==')

# function Create QR code 
def create_qrcode(request):
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
            content = {}
            return render(request, 'qrcode_generator/create_qrcode.html', content)

    except Exception as e:  #contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('== end function Create QR code ==')

# function Owner qr code 
def help_qrcode(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            content = {}
            return render(request, 'qrcode_generator/help_qrcode.html', {content})

    except Exception as e:  #contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('== end function my qr code ==')

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

