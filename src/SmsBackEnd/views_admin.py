from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .helper import dictfetchall
from django.db import connection

# function main for user group curator
@login_required(login_url="/Users/login/")
def admin_manage_user(request):
    try:
        user_session = request.session.get('user_session')
        if user_session == 'Admin':

            if request.method == 'POST':

                user_id = request.POST.get('user_id','')
                print(user_id)
                
                cursor = connection.cursor()
                cursor.execute("UPDATE auth_user SET is_active = 1 WHERE auth_user.id = "+ user_id)
                cursor.close()
                
                return redirect("/SmsBackEnd/admin_manage_user/")
            else:
                cursor = connection.cursor()
                cursor.execute("SELECT auth_user.first_name, auth_user.id, auth_user.last_name FROM auth_user WHERE auth_user.is_active = 0")
                user = dictfetchall(cursor)
                cursor.close()

                context ={
                    "user" : user,
                }
                return render(request, 'admin/admin_manage_user.html', context)
        else:
            return redirect('/Users/login/')
    except Exception as e:  # contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')

# function main for user group curator
@login_required(login_url="/Users/login/")
def add_equipment(request):
    try:
        user_session = request.session.get('user_session')
        if user_session == 'Admin':

            if request.method == 'POST':
                return redirect("/SmsBackEnd/add_equipment/")
            else:
                return render(request, 'admin/add_equipment/add_equipment.html')
        else:
            return redirect('/Users/login/')
    except Exception as e:  # contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')