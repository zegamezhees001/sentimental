from django.contrib.auth import login as dj_login, logout as dj_logout
from django.contrib.auth.signals import user_logged_in
from .models import UserSession
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.mail import EmailMessage
import os.path
from .forms import SignUpForm, LoginForm
from rolepermissions.roles import assign_role
from SmsBackEnd.helper import date_format, encode, decode
from datetime import datetime
# import datetime
from django.utils.translation import ugettext_lazy as _
from .forms import SignUpForm,AdminSignUpForm, LoginForm, PasswordResetRequestForm, ResetChangePasswordForm, ChangePasswordForm
from django.contrib.auth.models import Group
projectPath = '/Users'
homePath = '/'
superadminPath = '/SmsBackEnd/ibiobank_admin/'
adminPath = '/SmsBackEnd/equipment_admin/'
loPath = '/SmsBackEnd/equipment_Lo/'
BoosterPath = '/SmsBackEnd/equipment_Booster/'
StudentPath = '/SmsBackEnd/equipment_Student/'
loginPath = '/Users/login/'


# Signup function
def signup(request):
    args = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        # Check register button
        if 'registerbtn' in request.POST:
            print("test")
            if form.is_valid():
            #     user = form.save()
            #     user = User.objects.filter(username=form.cleaned_data.get('username')).first()
            #     group = Group.objects.get(name='user')
            #     user.groups.add(group)

            #     # email confirmation
            #     current_site = get_current_site(request)
            #     subject = _('Confirm registration from SmsBaseApp')
            #     message = render_to_string('acc_active_email.html', {
            #         'user': user,
            #         'domain': current_site,
            #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #         'token': account_activation_token.make_token(user),
            #     })
            #     # user.email_user(subject, message) #request User Activate
            #     # assign_role(user, 'doctor')
            #     email = EmailMessage(subject, message, to=['wanattapong1997@gmail.com']) #ส่งไปที่ Email Admin
            #     email.send()
            #     message_header =_('สมัคร สำเร็จ.')
            #     message_detail =_('กรุณาเข้ารับการฝึกอบรม.')
            #     message_header_json = str(message_header)
            #     message_detail_json = str(message_detail)
            #     request.session['sm_value'] = {'message_header': message_header_json,
            #                                    'message_detail': message_detail_json,
            #                                    'type': 'success',
            #                                    'displaytime': '10'}
            #     request.session['goto'] = loginPath

                return redirect(projectPath+'/status_message/')

            else:
                print(form.errors.as_data())

    else:
        # if not post show form signup
        form = SignUpForm()

    args['form'] = form
    return render(request, 'signup.html', args)


def staff_is(staffId):
    if staffId is not False:
        try:
            group = Group.objects.get(id=staffId)
            return group.name
        except Exception as e:
            print(e)
            return False
    return False
# Login function
def login(request):
    if staff_is(request.user.is_staff):
        g = staff_is(request.user.is_staff)
        print(g)
        if str(g) == "Admin":
            return redirect("Team:create_team")
    user_session = ''
    args = {}
    form = LoginForm(request.POST or None)

    # check if post button login check user pass
    if request.method == 'POST':
        if 'loginBtn' in request.POST and form.is_valid():

            user = form.login(request)

            request.session['user_id'] = user.id
            # check new user create storage folder
            check_create_storage(request)
            if user is not None:
                dj_login(request, user)
                print('----------------------------')
                user_logged_in_handler('joe',request,user)
                
                # if 'next' in request.POST:
                #     return redirect(request.POST.get('next'))
                if is_user(request , user):
                    return redirect(homePath) 
                elif is_superadmin(request, user):
                    return redirect(superadminPath)   
                elif is_admin(request, user):
                    return redirect(adminPath) 
                elif is_Lo(request, user):
                    return redirect(loPath) 
                elif is_Booster(request, user):
                    return redirect(BoosterPath) 
                elif is_Student(request, user):
                    return redirect(StudentPath) 
                
                return redirect(homePath)
            
        elif 'test' in request.POST:
            message_header =_('Register successfully.')
            message_detail =_('Please confirm your email.')
            message_header_json = str(message_header)
            message_detail_json = str(message_detail)
            request.session['sm_value'] = {'message_header': message_header_json,
                                           'message_detail': message_detail_json,
                                           'type': 'success',
                                           'displaytime': '10'}
            


            return redirect(projectPath + '/status_message/')  


    args['form'] = form
    return render(request, 'login.html', args)


def is_user(request,user):
    request.session.modified = True
    request.session['user_session'] = "user" 
    if user.groups.filter(name='user').exists(): 
        return True
    else:
        return False   

def is_superadmin(request,user):
    request.session.modified = True
    request.session['user_session'] = "Administrator"
    if user.groups.filter(name='Administrator').exists():  
        return True
    else:
        return False

def is_admin(request,user):
    request.session.modified = True
    request.session['user_session'] = "Admin"
    if user.groups.filter(name='Admin').exists():  
        return True
    else:
        return False

def is_Lo(request,user):
    request.session.modified = True
    request.session['user_session'] = "Lo"
    if user.groups.filter(name='Lo').exists():  
        return True
    else:
        return False

def is_Student(request,user):
    request.session.modified = True
    request.session['user_session'] = "Student"
    if user.groups.filter(name='Student').exists():  
        return True
    else:
        return False

def is_Booster(request,user):
    request.session.modified = True
    request.session['user_session'] = "Booster"
    if user.groups.filter(name='Booster').exists():  
        return True
    else:
        return False



def activate_account(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #dj_login(request, user)
        message_header =_('Confirm email successfully.')
        message_detail =_('Enjoy using our system.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {'message_header': message_header_json,
                                       'message_detail': message_detail_json,
                                       'type': 'success',
                                       'displaytime': '10'}
        request.session['goto'] = loginPath

        return redirect(projectPath+'/status_message/')
    else:
        message_header =_('Confirm email failed.')
        message_detail =_('Please contact officer.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {'message_header': message_header_json,
                                       'message_detail': message_detail_json,
                                       'type': 'error',
                                       'displaytime': '10'}

        request.session['goto'] = homePath


        return redirect(projectPath+'/status_message/')



# Check and Create folder
def check_create_storage(request):

    try:
        user_id = request.session.get('user_id')
        path = str(user_id)
        default_path = os.path.abspath(settings.MEDIA_ROOT+"/storage/"+path)
        if not os.path.exists(settings.MEDIA_ROOT+"/storage/"+path):
            os.makedirs(default_path)
    except OSError as e:
        if e.errno == 17:
            return False




def status_message(request):
    args = {}

    try:
        args['goto'] = request.session['goto']
        sm_value = request.session['sm_value']
        args['type'] = sm_value['type']
        args['message_header'] = sm_value['message_header']
        args['message_detail'] = sm_value['message_detail']
        args['displaytime'] = sm_value['displaytime']

        del request.session['goto']
        del request.session['sm_value']

        return render(request, 'status_message.html', args)

    except KeyError:
        return redirect(homePath)


def password_reset_request(request):
    args = {}
    form = PasswordResetRequestForm(request.POST or None)
    if request.method == 'POST':
        if 'resetBtn' in request.POST and form.is_valid():
            user = User.objects.filter(email=form.cleaned_data.get('email')).first()

            # email confirmation
            current_site = get_current_site(request)
            subject = _('Confirm password change from SmsBaseApp')
            message = render_to_string('acc_reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # decode
                'token': account_activation_token.make_token(user),
                'date': urlsafe_base64_encode(force_bytes(datetime.now().strftime('%y%m%d'))), # decode
                'time': urlsafe_base64_encode(force_bytes(datetime.now().strftime('%H%M'))), # decode
            })
            user.email_user(subject, message)
            message_header =_('Request a Password Change')
            message_detail =_('Please confirm the password at your email')
            message_header_json = str(message_header)
            message_detail_json = str(message_detail)

            request.session['sm_value'] = {'message_header': message_header_json,
                                           'message_detail': message_detail_json,
                                           'type': 'info',
                                           'displaytime': '10'}
            request.session['goto'] = homePath

            return redirect(projectPath+'/status_message/')

    args['form'] = form
    return render(request, 'password_reset_request.html', args)


def activate_password_reset(request, uidb64, token, date, time):
    email_expired = 30

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        date = force_text(urlsafe_base64_decode(date))
        time = force_text(urlsafe_base64_decode(time))
        dt = datetime.strptime(date + time, '%y%m%d%H%M')
        diff_dt = datetime.now() - dt
        #diff_dt_minute = divmod(diff_dt.days * 86400 + diff_dt.seconds, 60)
        diff_dt_minute = (diff_dt.days * 86400 + diff_dt.seconds)/60
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # request correct
    if user is not None and account_activation_token.check_token(user, token) and diff_dt_minute <= email_expired:
        request.session['reset_password'] = {'user': uid,
                                             'dt': datetime.now().strftime('%y%m%d%H%M')}
        # dj_login(request, user)
        return redirect(projectPath+'/user/reset/password/change/')

    # request expired
    elif user is not None and account_activation_token.check_token(user, token) and diff_dt_minute > email_expired:
        message_header =_('Reset password failed.')
        message_detail =_('Reset Passwords request expired. Please login again')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {'message_header': message_header_json,
                                       'message_detail': message_detail_json,
                                       'type': 'error',
                                       'displaytime': '10'}
        request.session['goto'] = homePath

        return redirect(projectPath + '/status_message/')

    else:
        message_header =_('Reset password failed.')
        message_detail =_('Please contact officer.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {'message_header': message_header_json,
                                       'message_detail': message_detail_json,
                                       'type': 'error',
                                       'displaytime': '10'}
        request.session['goto'] = homePath

        return redirect(projectPath+'/status_message/')


def reset_change_password_request(request):
    args = {}
    form = ResetChangePasswordForm(request.POST or None)

    # if not request.user.is_authenticated():
    #     return redirect(homePath)

    if request.method == 'POST':
        if 'resetBtn' in request.POST and form.is_valid():
            try:
                user = User.objects.get(pk=request.session['reset_user'])
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                del request.session['reset_user']
                message_header =_('Reset password successfully')
                message_detail =_('New password is saved successfully')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {'message_header': message_header_json,
                                               'message_detail': message_detail_json,
                                               'type': 'success',
                                               'displaytime': '10'}
                request.session['goto'] = homePath

                return redirect(projectPath + '/status_message/')

            except KeyError:
                message_header =_('Reset password failed.')
                message_detail =_('Please a new request.')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {'message_header': message_header_json,
                                               'message_detail': message_detail_json,
                                               'type': 'error',
                                               'displaytime': '10'}
                request.session['goto'] = homePath

                return redirect(projectPath + '/status_message/')

    else:
        try:
            rs_value = request.session['reset_password']
            user = User.objects.get(pk=rs_value['user'])
            dt = datetime.strptime(rs_value['dt'], '%y%m%d%H%M')
            diff_dt = datetime.now() - dt
            diff_dt_minute = (diff_dt.days * 86400 + diff_dt.seconds) / 60
            del request.session['reset_password']

            request.session['reset_user'] = rs_value['user']

        except KeyError:
            message_header =_('Reset password failed.')
            message_detail =_('Please a new request.')
            message_header_json = str(message_header)
            message_detail_json = str(message_detail)
            request.session['sm_value'] = {'message_header': message_header_json,
                                           'message_detail': message_detail_json,
                                           'type': 'error',
                                           'displaytime': '10'}
            request.session['goto'] = homePath

            return redirect(projectPath + '/status_message/')

    args['form'] = form
    return render(request, 'reset_change_password.html', args)


def change_password(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
    else:
        return redirect(homePath)

    args = {}
    form = ChangePasswordForm(request.POST or None)

    if request.method == 'POST':
        if 'cpBtn' in request.POST and form.is_valid():
            chk_old_pass_flag = user.check_password(form.cleaned_data.get('password0'))

            if chk_old_pass_flag:
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                message_header =_('Reset password successfully')
                message_detail =_('New password is saved successfully. Please login again')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {'message_header': message_header_json,
                                               'message_detail': message_detail_json,
                                               'type': 'success',
                                               'displaytime': '10'}
                request.session['goto'] = homePath

                return redirect(projectPath + '/status_message/')
            else:
                message_header =_('Reset password failed.')
                message_detail =_('The old password incorrect. Please login again')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {'message_header': message_header_json,
                                               'message_detail': message_detail_json,
                                               'type': 'error',
                                               'displaytime': '3'}
                request.session['goto'] = projectPath + '/user/change_password/'

                return redirect(projectPath + '/status_message/')

    args['form'] = form
    return render(request, 'change_password.html', args)


def logout(request):
    try:
        dj_logout(request)
        return redirect(loginPath)

    except KeyError:
        pass
        return redirect(request,loginPath)

def user_logged_in_handler(sender, request, user, **kwargs):
    time = str(datetime.now()).split('.')
    # time = str(datetime.datetime.now()).split('.')
    time = time[0]+'.000000'
    UserSession.objects.get_or_create(
        user = user,
        session_id = request.session.session_key,
        last_login = time
    )
user_logged_in.connect(user_logged_in_handler)



