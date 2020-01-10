from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from .models import Profile
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


# Create Signup form in django form
class SignUpForm(UserCreationForm):
    BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
    USER_GROUPS=[
        ('User','ผู้ร่วมวิจัย'),
        ('Student','นักศึกษาฝึกงาน'),
        ('Lo','Lo'),
        ('Booster','ผู้ช้วย'),
        ('Admin','Admin'),
        ('Administrator','Administrator'),
        ]

    username = forms.CharField(required=True, label=_('Username'), widget=forms.TextInput(attrs={'placeholder': _('ชื่อผู้ใช้'),'class':'form-control mb-4'}))
    first_name = forms.CharField(required=True, label=_('FirstName'), widget=forms.TextInput(attrs={'placeholder': _('ชื่อ'),'class':'form-control mb-4'}))
    last_name = forms.CharField(required=True, label=_('Lastname'), widget=forms.TextInput(attrs={'placeholder': _('นามสกุล'),'class':'form-control mb-4'}))
    email = forms.EmailField(required=True, label=_('Email'), widget=forms.TextInput(attrs={'placeholder': _('Email'),'class':'form-control mb-4'}))
    password1 = forms.CharField(required=True, label=_('Password'),
                                widget=forms.TextInput(attrs={'placeholder': _('Password'), 'type': 'password','class':'form-control mb-4'}))
    password2 = forms.CharField(required=True, label=_('Confirm Password'),
                                widget=forms.TextInput(attrs={'placeholder': _('Confirm Password'), 'type': 'password','class':'form-control mb-4'}))
    bio = forms.CharField(max_length=500, label=_('Profile'), widget=forms.TextInput(attrs={'placeholder': _('Profile'),'class':'form-control mb-4'}))
    phone_No = forms.CharField(required=True, label=_('phone_No'), widget=forms.TextInput(attrs={'placeholder': _('เบอร์โทรศัพท์'),'class':'form-control mb-4'}))
    employee_ID = forms.CharField(required=True, label=_('Employee_ID'), widget=forms.TextInput(attrs={'placeholder': _('รหัสพนักงาน'),'class':'form-control mb-4'}))
    user_group = forms.CharField(label='Select user group',widget=forms.Select(choices=USER_GROUPS,attrs={'class':'form-control mb-4'}))
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES,attrs={'class':'form-control col-3 '}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'employee_ID', 'phone_No', 'email', 'user_group', 'bio','birth_date')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(_('This email is already used'))
        return email

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)

        if commit:
            
            user.is_active = False
            user.save()
            user_profile = Profile(bio=self.cleaned_data.get('bio'), user_id=user.id,birth_date=self.cleaned_data.get('birth_date'))
            user_profile.save()


 
# Create Admin Signup form in django form
class AdminSignUpForm(UserCreationForm):
    username = forms.CharField(required=True, label=_('Username'), widget=forms.TextInput(attrs={'placeholder': _('Username'),'class':'form-control mb-4'}))
    first_name = forms.CharField(required=True, label=_('FirstName'), widget=forms.TextInput(attrs={'placeholder': _('FirstName'),'class':'form-control mb-4'}))
    last_name = forms.CharField(required=True, label=_('Lastname'), widget=forms.TextInput(attrs={'placeholder': _('Lastname'),'class':'form-control mb-4'}))
    email = forms.EmailField(required=True, label=_('Email'), widget=forms.TextInput(attrs={'placeholder': _('Email'),'class':'form-control mb-4'}))
    password1 = forms.CharField(required=True, label=_('Password'),
                                widget=forms.TextInput(attrs={'placeholder': _('Password'), 'type': 'password','class':'form-control mb-4'}))
    password2 = forms.CharField(required=True, label=_('Confirm Password'),
                                widget=forms.TextInput(attrs={'placeholder': _('Confirm Password'), 'type': 'password','class':'form-control mb-4'}))
    bio = forms.CharField(max_length=500, label=_('Profile'), widget=forms.TextInput(attrs={'placeholder': _('Profile'),'class':'form-control mb-4'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'bio')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(_('This email is already used'))
        return email

    def save(self, commit=True):
        user = super(AdminSignUpForm, self).save(commit=False)

        if commit:
            user.is_active = False
            user.save()
            user_profile = Profile(
                bio=self.cleaned_data.get('bio'), 
            user_id=user.id)
            user_profile.save()




# Create Login form in django form
class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username',
                               widget=forms.TextInput(attrs={'placeholder': _('Username'),'class':'form-control mb-4'}))
    password = forms.CharField(required=True, label='Password',
                               widget=forms.TextInput(attrs={'placeholder': _('Password'),'class':'form-control mb-4', 'type': 'password'}))

    def __int__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                raise forms.ValidationError(_("Please confirm your email."))
        else:
            raise forms.ValidationError(_("Invalid username or password."))

        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={'placeholder': _('Email'),'class':'form-control mb-4'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).count() == 0:
            raise forms.ValidationError(_('Invalid email'))
        return email


class ResetChangePasswordForm(forms.Form):
    password1 = forms.CharField(required=True, label='Password',
                                widget=forms.TextInput(attrs={'placeholder': _('Password'), 'type': 'password'}))
    password2 = forms.CharField(required=True, label='Confirm Password',
                                widget=forms.TextInput(attrs={'placeholder': _('Confirm Password'), 'type': 'password'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(_("The password didn't match"))

        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    password0 = forms.CharField(required=True, label='Old Password',
                                widget=forms.TextInput(attrs={'placeholder': _('Old Password'), 'type': 'password'}))
    password1 = forms.CharField(required=True, label='New Password',
                                widget=forms.TextInput(attrs={'placeholder': _('New Password'), 'type': 'password'}))
    password2 = forms.CharField(required=True, label='Confirm Password',
                                widget=forms.TextInput(attrs={'placeholder': _('Confirm Password'), 'type': 'password'}))

    def __int__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(_("The password didn't match"))

        return self.cleaned_data
