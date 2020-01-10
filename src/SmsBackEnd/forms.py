from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User,Group
from Users.models import Profile
from django.core.files.images import get_image_dimensions
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


# Create Admin Signup form in django form
class AdminSignUpForm(UserCreationForm):
    USER_GROUPS=[
        ('Admin','Admin'),
        ('Administrator','Administrator'),
        ('User','User'),
        ]

        # ('User','User'),
        # ('Administrator','Administrator'),
        # ('Curator','Curator'),
        # ('Collector','Collector'),
        # ('Brooks','Brooks'),
        # ('Plant_lab','Specimen lab'),
        # ('Herbarium_lab','Herbarium lab'),
        # ('Molecular_lab','Molecular lab'),
        # ('Tissue_lab','Tissue lab')
        # ]
  
    username = forms.CharField(required=True, label=_('Username'), widget=forms.TextInput(attrs={'placeholder': _('Username'),'class':'form-control mb-4'}))
    first_name = forms.CharField(required=True, label=_('FirstName'), widget=forms.TextInput(attrs={'placeholder': _('FirstName'),'class':'form-control mb-4'}))
    last_name = forms.CharField(required=True, label=_('Lastname'), widget=forms.TextInput(attrs={'placeholder': _('Lastname'),'class':'form-control mb-4'}))
    email = forms.EmailField(required=True, label=_('Email'), widget=forms.TextInput(attrs={'placeholder': _('Email'),'class':'form-control mb-4'}))
    password1 = forms.CharField(required=True, label=_('Password'),
                                widget=forms.TextInput(attrs={'placeholder': _('Password'), 'type': 'password','class':'form-control mb-4'}))
    password2 = forms.CharField(required=True, label=_('Confirm Password'),
                                widget=forms.TextInput(attrs={'placeholder': _('Confirm Password'), 'type': 'password','class':'form-control mb-4'}))
    bio = forms.CharField(max_length=500, label=_('Profile'), widget=forms.TextInput(attrs={'placeholder': _('Profile'),'class':'form-control mb-4'}))
    location = forms.CharField(max_length=150, label=_('Location'), widget=forms.Textarea(attrs={'rows':'4','placeholder': _('Location'),'class':'form-control mb-4'}))
    tel = forms.CharField(max_length=10, label=_('Tel'), widget=forms.TextInput(attrs={'placeholder': _('Tel'), 'class':'form-control mb-4'}))
    user_group = forms.CharField(label='Select user group',widget=forms.Select(choices=USER_GROUPS,attrs={'class':'form-control mb-4'}))
    avatar = forms.ImageField(label = 'Select a file',help_text= 'Jpg, jpeg only')
    class Meta: 
        model = User 
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'bio','tel','location','avatar') 


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
            user_profile = Profile(bio=self.cleaned_data.get('bio'), user_id=user.id,location=self.cleaned_data.get('location'),tel=self.cleaned_data.get('tel'),avatar=self.cleaned_data.get('avatar'))
            user_profile.save()
    
    def update(self, commit=True):
        user = super(AdminSignUpForm, self).save(commit=False)

        if commit:
            user.is_active = False
            user_profile = Profile.objects.filter(user_id = user.id).update(bio=self.cleaned_data.get('bio'),location=self.cleaned_data.get('location'),tel=self.cleaned_data.get('tel'),avatar=self.cleaned_data.get('avatar'))
          


